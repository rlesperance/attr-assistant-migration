import arcpy, os
import pandas as pd

basePath = r"C:\AttributeRulesWork"
GDB = os.path.join(basePath, "TargetDatabase.gdb") #This can be an SDE connection

#Get the file with the sequences
file = os.path.join(basePath, "DB_Sequence_List.xlsx")
seqList = pd.read_excel(file,  engine='openpyxl')

dbSequences = arcpy.da.ListDatabaseSequences(GDB)

add = True
for index, source_item in seqList.iterrows():
    seqName = source_item["Name"]
    startID = source_item["StartingID"]
    for dbSeq in dbSequences:
        if dbSeq.name == seqName:
            print ("Sequence {} exists.".format(seqName))
            add = False
    if add:
        print ("Sequence to add: {}".format(seqName))
        arcpy.management.CreateDatabaseSequence(GDB, seq_name=seqName, seq_start_id=startID)
        print ("Added sequence {}".format(seqName))
    add = True

print("\n")
print("Finished adding sequences")
