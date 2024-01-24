# Calc Length of Intersecting Line from origin to point of intersection

ASSUMTIONS:  There is only one intersection of the two lines.  The code assumes the split produces two segments.
There is a more complex calculation that can be done.  See the Esri Attribute Rules Github site.  https://github.com/rlesperance/arcade-expressions/blob/master/attribute_rule_calculation/SplitIntersectingLine.md

Uses the CUT() function to return two geometries.  That function sets the order of the returned geometries depending on what direction the incoming linear feature is. 
Since it's hard to determine what that order is supposed to be, the code below compares the origin point of both lines with the original pre-split line.  

## Expression Template

This Arcade expression will calculates field values from intersecting point layer
```js
var line_fs = FeatureSetByName($datastore, "LineLayerA", ['FIELD_NAME'], true);

var buffer_pnt_distance = 0.1;

function IsEmptyButBetter(data) {
    if (IsEmpty(data)) return true;
    for (var x in data) return false;
    return true;
}

var intersecting_lines;
if (buffer_pnt_distance == null || buffer_pnt_distance <= 0) {
    intersecting_lines = Intersects($feature, line_fs)
} else {
    intersecting_lines = Intersects(Buffer($feature, buffer_pnt_distance), line_fs);
    //intersecting_lines = Intersects(line_fs, Buffer($feature, buffer_pnt_distance));
}

if (IsEmptyButBetter(intersecting_lines)) {
  return 0
}
var line_feature = First(intersecting_lines)

//Need a line to intersect with if feature is a point
var search = Extent(Buffer($feature, .01, "meter"))
var clipsegment = Clip(line_feature, search)
var rotsegment = Rotate(clipsegment, 90)

var new_geoms = Cut(line_feature, rotsegment);

if (IsEmptyButBetter(new_geoms)) {
   return 0  }

var new_geom;
var new_orig;
var intx_orig;
var intx_geom = Geometry(line_feature)

for(var index in new_geoms) {
  new_orig = new_geoms[index]['paths'][0][0];
  intx_orig = intx_geom['paths'][0][0];
  if (text(new_orig)==text(intx_orig)) {new_geom = new_geoms[index]}
}

if (IsEmptyButBetter(new_geoms)) {
   return 0  }

var new_geom_1 = new_geoms[0];
if (count(new_geoms) > 1) {
  new_geom_1 = new_geoms[1] }

var polyline_1_length = Length(new_geom_1, 'feet');

return polyline_1_length
```

## Workflow

Using ArcGIS Pro, use the Add Attribute Rule geoprocessing tool to define this rule on a feature class and optionally on a subtype in that feature class.  
Use the following values when defining the rule, the other options are not required or depend on your situation.
  
  - **Rule Type:** Calculation
  - **Triggering Events:** Insert
