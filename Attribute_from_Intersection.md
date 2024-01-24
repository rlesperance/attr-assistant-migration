# Calc Attributes intersecting feature

This calculation grabs a value from a feature in another dataset in the same geodatabase that intersects the current feature.

## Use cases

Any feature that can intersect another.  Points can be tricky in this regard if they are trying to find a line or another point. 
Note in the code below that it's using a buffer around the edited/added feature to check the intersecting feature class.  

## Workflow

Using ArcGIS Pro, use the Add Attribute Rule geoprocessing tool to define this rule on a feature class and optionally on a subtype in that feature class.  
Use the following values when defining the rule, the other options are not required or depend on your situation.
  
  - **Rule Type:** Calculation
  - **Triggering Events:** Insert

## Expression Template

This Arcade expression will calculates field values from intersecting point layer
```js
intx_field = "FIELD_NAME"
var intx_features = FeatureSetByName($datastore, 'FeatureClassA', intx_field, true)
var intx_feature = First(Intersects(intx_features, Buffer($feature, 0.02)))

if (IsEmpty(intx_feature) || intx_feature == null)
{   return   }


return intx_feature[intx_field];
```

##  More than one layer

In addition, you can query more than one layer to get the result your are looking for. 
For instance, if you have two layers that the feature could intersect, such as a control valve on either a pressurized mainline or a gravity mainline (in this case they were in two different layers).

```js
var intx_field = "FIELD_NAME"
var intx_features = FeatureSetByName($datastore, 'PressurizedMain', [intx_field], true)
var intx_feature = First(Intersects(intx_features, buffer($feature, 0.02)))

if (IsEmpty(intx_feature) || intx_feature == null)
  {   
    var intx_features = FeatureSetByName($datastore, 'GravityMain', [intx_field], true)
    var intx_feature = First(Intersects(intx_features, buffer($feature, 0.02)))
    if (IsEmpty(intx_feature) || intx_feature == null) {
      return $feature.FIELD_NAME }
    return intx_feature[intx_field];
  }

return intx_feature[intx_field];
```
