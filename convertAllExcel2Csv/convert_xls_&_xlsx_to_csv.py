import csv
import pyexcel as xsl_conv
from openpyxl import load_workbook
import glob
import re
# By default openpyxl does not guard against quadratic blowup or billion laughs xml attacks. To guard against these attacks install defusedxml.


xsl_file_list = glob.glob('*.xls')

def xls_to_xlsx (current_filename) -> None:
  ''' receives a file xls file name from the same directory converts it to .xlsx file'''
  
  new_file_name = re.sub('.xls','.xlsx',current_filename)
  xsl_conv.save_book_as(file_name=current_filename, dest_file_name=new_file_name)
  return 


# converts all xsl files in the dir
for file in xsl_file_list:
  xls_to_xlsx(file)


extension = '.xlsx'


def fileListBuild(extension):
  ''' Returns a list of file names for the given extension parameter.'''
  return glob.glob(f"*{extension}")

filelist = fileListBuild(extension)



# ask user input for sheets

print("* "*20)
print("\nThe script will convert all the xlsx files in the current directory.\n")
print("* "*20)
print("\n")
print("To convert only the first sheet type 1 to convert all the sheets in a workbook type 2 and hit enter")
user_input = input("your choice:")


all_Sheets = False
if user_input == "2":
  all_Sheets = True


def csvWriter(sheetData,workBookName,sheetName):
  ''' receives a sheet data in list format  and the workbookname(excel file name) and sheet name to create a csv file.'''
  
  with open (f"{workBookName.strip()}_{sheetName}.csv",'w') as csv_output:
    writer = csv.writer(csv_output, delimiter=',')
    for line in sheetData:
      writer.writerow(line)
  

def allSheets(filename):
  ''' receives an file name from the same directory and calls the convert2Csv function for all the sheets.'''
  
  wb = load_workbook(filename=filename)
  
  for sheet in wb.sheetnames:
    sheetName = sheet
    csv_data = []
    sheet = wb[sheet]
    for value in sheet.iter_rows(values_only=True):
      csv_data.append(list(value))
    filename = re.sub('\.xlsx','',filename)
    csvWriter(csv_data,filename,sheetName)


def firstSheet(filename):

  ''' receives an file name from the same directory and calls the convert2Csv function for the active sheet(first sheet).'''

  csv_data = []
  wb = load_workbook(filename=filename)
  sheet = wb.active
  for value in sheet.iter_rows(values_only=True):
    csv_data.append(list(value))
    filename = re.sub('\.xlsx','',filename)
    csvWriter(csv_data,filename,"")


if all_Sheets == True :
  print("all sheets wanted")
  for file in filelist:
    allSheets(file)
else:
  for file in filelist:
    firstSheet(file)
