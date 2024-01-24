import arcpy, os, sys
import pandas as pd
import traceback


basePath = r"C:\AttributeRuleFiles"
crossRefXLS = os.path.join(basePath, "AttributeRules_Add.xlsx")

crossRefXLS = arcpy.GetParameterAsText(0) or crossRefXLS
option = arcpy.GetParameterAsText(1) or "Add"

def addRule(source_item):

    #Set up attribute rule
    inGDB = source_item["GEODATABASE"]
    in_table = source_item["TABLENAME"]
    ruleName = source_item["RULENAME"]
    ruleType = source_item["RULETYPE"]
    fieldName = source_item["FIELDNAME"]
    triggers = source_item["TRIGGERS"]
    exclude = source_item["EXCLUDE"]
    scriptName = source_item["FILENAME"]
    errornum = source_item["error_num"]
    errormess = source_item["error_message"]

    if pd.isna(fieldName):
        fieldName = ""
    if pd.isna(errornum):
        errornum = ""
    if pd.isna(errormess):
        errormess = ""
        

    print ("Adding or modifying {}".format(ruleName))

    text_file = open(os.path.join(basePath, scriptName), "r")
    scriptText = text_file.read()
    text_file.close()

    #Get feature Class
    fClass = os.path.join(inGDB, in_table)
    fClass

    #Check if rule is there
    exists = False
    attRules = arcpy.Describe(fClass).attributeRules
    for attRule in attRules:
        if attRule.name == ruleName:
            print ("  Rule {} exists.".format(ruleName))
            exists = True
            


    #Add rule to feature class
    if option == "Update":
        if not exists:
            print ("  Rule doesn't exist for alter!")
            return
        
        arcpy.management.AlterAttributeRule(in_table=fClass, name=ruleName, 
                                      script_expression=scriptText, triggering_events=triggers,  
                                      exclude_from_client_evaluation=exclude)
        
        print ("  Rule {} modified on feature class {}".format(ruleName, in_table))

    elif option == "Add":
        if exists:
            return
        
        arcpy.management.AddAttributeRule(in_table=fClass, name=ruleName, type=ruleType, 
                                      script_expression=scriptText, triggering_events=triggers,  
                                      field=fieldName, exclude_from_client_evaluation=exclude)

        print ("  Rule {} added to feature class {}".format(ruleName, in_table))
        
    elif option == "Delete":
        if not exists:
            return
        
        arcpy.management.DeleteAttributeRule(in_table=fClass, names=[ruleName], type=ruleType)

        print ("  Rule {} deleted from feature class {}".format(ruleName, in_table))


try:
    
    #Get Xref information for importing rules
    rulesDF = pd.read_excel(crossRefXLS,  engine='openpyxl')

    for index, source_item in rulesDF.iterrows():
        addRule(source_item)

    print ("\n")

except Exception as ex:
    print(ex)
    print(traceback.format_tb(sys.exc_info()[2])[0])

