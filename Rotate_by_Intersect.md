# Calc Rotation field based on intersecting line

This calculation sets a rotation attribute for a point feature that guides symbology rotation. 

ASSUMPTION:  The selected point is snapped to a line from the referenced layer.  

## Code Notes

Field name in this case is simply:  ROTATION

The code first checks the incoming geometry to see if it moved.  If this is an edit, and the feature didn't move there' no reason to evaluate.

ARITHMETIC vs GEOGRAPHIC

This code checks two different layers for an intersecting line.  When looking at some utility networks, there may be multiple types of main and lateral line layers. 

When it finds an intersecting line, it snips a tiny fragment to determine the angle of the line. 

In the symbology pane for a point feature, when setting the rotation based on an attribute there is an option to choose the method of calculating the rotation based on either Arithmatic or Geographic. 
The calculation in this script needs to account for that.  The code below is for geographic.  If you are using the other method, then remove the line "finalAngle = (450 - finalAngle) % 360" 

## Expression Template

This Arcade expression will calculates rotation
```js
// Did geomtry change?
var curgeom = Geometry($feature)
var prevgeom = Geometry($originalFeature)

function IsEmptyButBetter(data) {
    if (IsEmpty(data)) return true;
    for (var x in data) return false;
    return true;
}

if (!IsEmptyButBetter(prevgeom) && !IsEmptyButBetter(curgeom)) {
  if (curgeom.x == prevgeom.x && curgeom.y == prevgeom.y) {
     return $feature.ROTATION }  }

// Find the first intersecting line from the intersecting class
var lineClass = FeatureSetByName($datastore, "LineLayerA", ["objectid"], true)
var line = First(Intersects(lineClass, $feature))

// If no feature was found, see if there's an intersecting line from another class
if (line == null)
   lineClass = FeatureSetByName($datastore, "LineLayerB", ["objectid"], true)
   line = First(Intersects(lineClass, $feature))

// If no feature was found, return the original value
if (line == null)
   return $feature.rotation

// Buffer the point by a small amount to extract the segment
var search = Extent(Buffer($feature, .01, "meter"))
var segment = Clip(line, search)["paths"][0]

// Get angle of line using the start and end vertex 
var finalAngle = Angle(segment[0], segment[-1]) 
finalAngle = (450 - finalAngle) % 360

return finalAngle
```

## Implementation

Using ArcGIS Pro, use the Add Attribute Rule geoprocessing tool to define this rule on a feature class and optionally on a subtype in that feature class.  
Use the following values when defining the rule, the other options are not required or depend on your situation.
  
  - **Rule Type:** Calculation
  - **Triggering Events:** Insert
