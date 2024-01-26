# Calculate M values for line

This is more simple than it sounds.  M values for a linear feature are measures applied to each vertex of the line.  
There are complicated reasons to customize the M values as something different than what the geometry length is.  

In this case we are starting at the origin and stepping through each vertex and adding the total length of the line at that point and applying it to the M value for each vertex.
Similar to the Set As Distance function:  https://pro.arcgis.com/en/pro-app/latest/help/data/linear-referencing/update-route-measures.htm


## The Code

```js
var line = Geometry($feature);
var lineGeo = Dictionary(Text(line));

function distance(coord1x, coord1y, coord2x, coord2y) {
  var dx = coord2x - coord1x
  var dy = coord2y - coord1y
  return Sqrt(dx * dx + dy * dy)
  }

var length = 0

var paths = lineGeo['paths']
var prev_coords = paths[0][0]

for (var pathIndx in paths)
 {
  var path = paths[pathIndx]
  for (var vertIndx in path)
    {
      var coords = path[vertIndx];
      var segDist = distance(coords[0], coords[1], prev_coords[0], prev_coords[1])
      length = length + segDist
      coords[-1] = length
      prev_coords = coords;
     }
  }

lineGeo['hasM'] = line['hasM']
lineGeo['hasZ'] = line['hasZ']

return {
  "result": {"geometry": Polyline(lineGeo)}
};
```
