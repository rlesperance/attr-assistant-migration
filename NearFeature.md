##  Get attribute of nearest feature

This code looks at another layer in the geodatabase and searches for the closest feature in that layer. 
Then the distance from the current feature and that feature is determined
In order not to loop through every feature in the data searching for the closest one, we've searched using a distance tolerance of 1000 feet.

```js
var searchDistance = 1000;
var addresses = FeatureSetByName($datastore, "FeatureClassName", ["FIELD_NAME"], true);

// returns all features within buffer of selected or added feature
var closestFeatures = Intersects(addresses, Buffer($feature, searchDistance, "feet"));
var minDistance = Infinity;
var closestFeature;

// Of the addresses within 200ft of the hydrant,
// the closest one is returned along with the distance
for (var feature in closestFeatures){
  var aDistance = Distance(feature, $feature, "feet");
  if(aDistance < minDistance){
    minDistance = aDistance;
    closestFeature = feature;
  }
};

IF(IsEmpty(closestFeature))
  {
    return "No Feature Found";
  }

return closestFeature["FULLADDR"];
```
