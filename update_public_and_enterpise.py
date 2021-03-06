import arcpy

# import smtplib for emails
import smtplib

# import os for environment variables
import os

# Set workspace
arcpy.env.workspace = "G:/A_STAFF/DanWhaland/PRA Percent for Art/PRA_P4A_Final.gdb"

# Allow overwrite of existing files
arcpy.env.overwriteOutput = 'TRUE'

# Since arcpy.env.overwriteOutput does not seem to be working in ArcPro 2.4, use this line to delete the two _rev layers before creating them again
if arcpy.Exists("Percent_for_Art_Enterprise_rev"):
    arcpy.Delete_management("Percent_for_Art_Enterprise_rev")

if arcpy.Exists("Percent_for_Art_Public_rev"):
    arcpy.Delete_management("Percent_for_Art_Public_rev")

# Create variables
Master_P4A = "Percent_for_Art_Master"
New_P4A_Public = "Percent_for_Art_Public_rev"
New_P4A_Enterprise = "Percent_for_Art_Enterprise_rev"

# first, copy all the features from master to enterpise_rev. rename fields, remove fields, etc. THEN, select the Active features and copy them to public_rev
arcpy.CopyFeatures_management(Master_P4A, New_P4A_Enterprise)

# Change field names to match metadata 
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_P4A_ID", "P4A_ID", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Image", "Image", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Status", "Status", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Artist", "Artist", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Title", "Title", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Date", "Date_", "Date")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Location_N", "Location_Name", "Location Name")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Address", "Address", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Location_1", "Location_Note", "Location Note")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Medium", "Medium", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Neighborho", "Neighborhood", "Neighborhood")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Owner", "Owner", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Note", "Note", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Google_Str", "Google_Streetview_Link", "Google Street View Link")

# Delete extra fields
arcpy.DeleteField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Artist")
arcpy.DeleteField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Title")
arcpy.DeleteField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Image")
arcpy.DeleteField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__P4A_ID")
arcpy.DeleteField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__OBJECTID")
arcpy.DeleteField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__ObjectID_1")
arcpy.DeleteField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Shape_Leng")

# Select Active, In Progress, and Inaccessible Status features so you can copy them to the public_rev layer
arcpy.SelectLayerByAttribute_management(New_P4A_Enterprise, "NEW_SELECTION", "Status = 'Active' Or Status = 'In Progress' Or Status = 'Inaccessible'", None)

# Copy active status features to public_rev
arcpy.CopyFeatures_management(New_P4A_Enterprise, New_P4A_Public)

# Delete fields that shouldn't be in the public layer
arcpy.DeleteField_management(New_P4A_Public, "Owner")
arcpy.DeleteField_management(New_P4A_Public, "Note")

# email variables
sender = os.environ.get('DPDAppsProd_Email')
receivers = [os.environ.get('Dan_Email')]
password = os.environ.get('DPDAppsProd_password') 

message = """Subject: Percent for Art Ready for Upload

The working versions of the Percent for Art layers have been updated and are ready for upload. 

-DPD GIS
"""

smtpObj = smtplib.SMTP(host='smtp.office365.com', port=587)
smtpObj.starttls()
smtpObj.login(sender,password)

# send the email 
smtpObj.sendmail(sender, receivers, message)
smtpObj.quit()
