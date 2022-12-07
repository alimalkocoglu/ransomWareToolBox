import sys
import re

# the script aims to fix or  the cases below:

#Examples to be weeded out to attention file

#this is  ,less than the header,example, that must end up in attention file.
#this is  ,more than the header,example,,,,this,must end up in attention file.

#Examples to be fixed and added to corrected file
#this is,"more than one,quotation marks","example I made,up",this will be fixed,

#Work on later cases
#(orphan quotation mark)
#item,item2,,F,1979 ,phonenum,"my address           ,,WASHINGTON,DC,200110000


# captures the first (and only) argument passed
file_name = sys.argv[1]


def get_header(csv_file) -> list:
  """  returns the header of a given csv file in a List """
  with open(
      csv_file,
      'r',
  ) as file:
    header_line = file.readline()
  #clean the new line at the end.
  header_line = header_line.replace("\n", "", 1).split(",")
  return header_line


def quation_mark_comma_cleaner(string):
  pattern = r'(,)'
  string = re.split(pattern, string) #split into an list
  cleaned_list = []
  string_to_add = ""

  quatation_opening = False
  quatation_closing = False

  for e in string:

    if e.startswith('"') or e.startswith("'"):
      quatation_opening = True
    if e.startswith('"') and e.endswith("'"):
        #an example would be "namefirst namelast",...
        #the same element is wrapped in quatation_closing
        cleaned_list.append(e.replace('"', ''))
        continue
    elif e.endswith('"') or e.endswith("'"):
      quatation_closing = True

    if quatation_opening and not quatation_closing:
      #build the string till you find the closing ' " '
      string_to_add = string_to_add + " " + e
      continue

    elif quatation_opening and quatation_closing:
      # meaning we reached the closing '"'
      string_to_add = string_to_add + e
      cleaned_list.append(string_to_add.replace(",", "").replace('"', ''))
      string_to_add = ""
      quatation_closing = False
      quatation_opening = False
      continue

    if not e == ",":
      cleaned_list.append(e)

  return (",".join(cleaned_list))


header_elm_num = len(get_header(file_name))

corrected_file_name = re.sub(r".csv$", "", file_name) + "_CORRECTED.csv"
attention_file_name = re.sub(r".csv$", "", file_name) + "_ATTENTION.csv"

# files for appending created here.
with open(attention_file_name, 'w') as attn_file, open(
    corrected_file_name, 'w') as corrected_file, open(file_name,
                                                      "r") as org_file:

  org_file_content = org_file.readlines()
  attn_file.writelines(org_file_content[0])
  #corrected_file.writelines(org_file_content[0])


def to_corrected(line, file=corrected_file_name):
  
  with open(corrected_file_name, 'a') as file:
    file.write(line)

  return


def to_attention(line, file=attention_file_name):

  with open(attention_file_name, 'a') as file:
    file.write(line)

  return


with open(file_name, 'r') as file:
  # Read and print the entire file line by line
  for line in file:
    #print(line)
    if '"' in line:
      new_line = quation_mark_comma_cleaner(line)
      if new_line.count(',') is not header_elm_num - 1:
        #append to original line to the attention neeeded file.
        to_attention(line)
        continue
      to_corrected(new_line)
      continue
    
    if line.count(',') is not header_elm_num - 1:
      to_attention(line)
      continue
    to_corrected(line)
  
