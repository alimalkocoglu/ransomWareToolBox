import csv
import re
from datetime import datetime
import glob


unique_column_names = []
file_list = glob.glob('*.csv')


def header_trim_and_lower (filename) -> None:

  """ trims the spaces around header labels and lowercases them for comparability -- dictionary key:pair values.
      Changes the given file.
  """

  with open(filename, 'r', encoding='utf-8') as file:
    data = file.readlines()

    header = data[0].split(",")
    for i in range (len(header)):
      header[i] = re.sub(r"(^\s*)|(\s*$)","", header[i]).replace('\ufeff','').lower()
    header = ",".join(header)+'\n'
    data[0] = header
  
  with open(filename, 'w', encoding='utf-8') as file:
     file.writelines(data)


  return 

def get_header(csv_file) -> list:

  """  returns the header of a given csv file in a List """
  
  with open(csv_file,'r',) as file:
    header_line = file.readline()
  #clean the new line at the end.
  header_line = header_line.replace("\n","",1).split(",")
  return header_line
  

def unq_col_real(file_list,all_columns_list=unique_column_names) -> None:

  #go through every csv file
  for file in file_list:
    # go through every column in header
    for column in get_header(file):
      # add the new value if doesn't exist.
      if column is None or column == "":
        continue 
      if not (column in all_columns_list):
        all_columns_list.append(column)
  return None


def create_main_file(header_list=unique_column_names) -> str :
  ''' creates main file to a appended to with time stamp based on given header list'''
  now = datetime.now()
  # dd/mm/YY H:M:S
  date_stamp = now.strftime("%d-%m-%Y-%H:%M:%S")
  file_name = date_stamp+'__MERGED.tsv'
  with open(file_name, mode='w',) as tsv_file:
    fieldnames = header_list
    writer = csv.DictWriter(tsv_file, fieldnames=fieldnames,delimiter='\t')
    writer.writeheader()

  return file_name

main_file = create_main_file()

def append_to_main_file(sub_file,main_file = main_file):

  ''' '''
  with open (sub_file, newline='',encoding="utf-8-sig") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
      with open(main_file,mode='a') as main_tsv:
        writer = csv.DictWriter(main_tsv, fieldnames=unique_column_names,delimiter='\t')
        writer.writerow(row)
  return 



for file in file_list:
  header_trim_and_lower(file)

unq_col_real(file_list)
main_file = create_main_file()
print(unique_column_names)

for file in file_list:
  append_to_main_file(file)