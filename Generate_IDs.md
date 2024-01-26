# Generate Unique IDs from sequences

These snippets of Arcade code will take existing named sequences in a database and turn them into unique IDs in your layer.  Usually this is just an INSERT rule for new features. 
Database sequences are not necessarily an Esri managed artifact in the database.  The geoprocessing tool to add a sequence to a geodatabase is just generating a database native sequence that you can use.
The sequence will iterate each time it is referenced

## Simple use of sequence

Utilizing the sequence can be this simple.   This is the entire rule code for just a sequenced ID with a prefix. 
```js
return "PREFIX-" + NextSequenceValue('SeqName')
```

## ID generation based on attributes or intersections

This snippet is using the sequence along with a grid reference layer to determine where the feature is. 
It is then evaluating an attribute already existing in the layer (presumably because of a feature template that already contains the attribute). 

```js
var valveType = $feature.VALVETYPE
var facilityID = $feature.FACILITYID
var intxField = "TAG_VALUE"
var intxFeatureSet = FeatureSetByName($datastore, 'MapPage', [intxField], true)
var intxFeature = First(Intersects(intxFeatureSet, $feature))

var gridID = "0000"
if (!IsEmpty(intxFeature) && intxFeature != null)
  {   gridID = intxFeature[intxField]   }

var returnVal = gridID + "-RB" + NextSequenceValue('SequenceName')

if (valveType == "Option1") 
  {
  return Replace(returnVal, "RB", "RR")
  }

if (valveType == "Option2") 
  {
  return Replace(returnVal, "RB", "RO")
  }

return returnVal
```
