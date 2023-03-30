# Attribute Assistant Migration Scripts

Code involved with ArcMap Attribute Assistant migration to attribute rules.

The ArcGIS Desktop (ArcMap) Attribute Assistant was a powerful tool for editors to control the attributes managed in feature classes in their environment.  Along with that power, there were a few drawbacks. 
  1. The extension needed to be deployed to every desktop it needed to be used on.  Changes would need to be deployed as well. 
  2. Extension would apply to any feature class that had the target field name.  Hard to control what feature classes were affected. 
  3. ArcMap is going away

With the introduction of ArcGIS Pro, you can create rules around attributes and store them with the feature classes in an Enterprise Geodatabase.  This offers advantages in that the rule is stored with the feature class in the database, and therefore travels with the feature class even if moved.  There is no deployment necessary, so changes to the rules are applied immediately to all editing.  
ArcGIS Server honors these rules as well, so editing in web maps will also fire the rules.
