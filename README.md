# googlesheets_aquaticinformatics_ingester
google appscript updates the .bat file in google drive. local copy gets update which is read by the converter.py file. converter.py then downloads the most recent copy of the google sheet as a xlsx file then runs the vbscript that does the conversion and "cleaning" from xlsx to .csv, ready for import to aquatic informatics' aquarius
