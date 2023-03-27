import os
import glob
import re
from datetime import datetime

#creates a directory to keep original files

#somehow avoid the file naming pitfalls 

def file_name_cleaner(filename,extension = ".csv"):

    """ replaces the special chars in file names with "-" """
    
    new_name = re.sub(rf"{extension}", '', filename)
    new_name = re.sub(r"[^a-zA-Z0-9]+", '_', new_name)
    return new_name+extension

def header_trim_and_lower (filename) -> None:

    """ receives a csv file name and trims the spaces around header labels and lowercases them for comparability -- dictionary key:pair values.
    modifies the given file. """
    
    with open(filename, 'r') as file:
        data = file.readlines()

    header = data[0].split(",")
    for i in range (len(header)):
      header[i] = re.sub(r"(^\s*)|(\s*$)","", header[i]).replace('\ufeff','').lower()
    header = ",".join(header)+'\n'
    data[0] = header
  
    with open(filename, 'w') as file:
        file.writelines(data)
    
    return 


def file_mod() -> str:

    """ creates a new folder named original + date and moves the original files there and returns the date string"""
    
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m-%Y-%H:%M:%S")
    os.system(f"mkdir {'input_files_'+dt_string}")
    os.system(f"mkdir {'output_files_'+dt_string}")

    #move the original files into original folder

    os.system(f"cp *.csv ./{'input_files_'+dt_string}")
    file_list = glob.glob('*.csv')
    for file in file_list:
        os.rename(file,file_name_cleaner(file))
    
    return dt_string
  

  
date_stamp = file_mod()

labels_to_keep = {
'namefirst',
'namemid',
'namelast',
'addr1',
'addr2',
'addrcity',
'addrstate',
'addrzip',
'addrcountry',
'phone',
'ssn',
'natlid',
'mmn',
'dob',
'dobyear',
'dobmon',
'dobday',
'dlnumber',
'dlstate',
'email',
'email1',
'email2',
'email3',
'userid',
'password',
'cardnum',
'cardcvn',
'cardpin',
'cardexpdate',
'cardexpyear',
'cardexpmon',
'cardexpday',
'bankname',
'bankphone',
'bankroute',
'bankacct',
'bankpin',
'iban',
'passportnum',
'passportexpdate',
'passportissuedate',
'passportcountry',
'gender',
'medicalid',
'medicalprovider',
'site',
'phone1',
'phone2',
'phone3'
}



def get_header(csv_file) -> list :

    """  returns the header rows of a given csv file in a List format and cleans the spaces around list elements """
    
    with open(csv_file,'r') as file:
        header_line = file.readline()
    
    #clean the new line at the end.
    header_line = header_line.replace("\n","",1).split(",")
    #clean spaces
    for i in range(len(header_line)):
        header_line[i] = re.sub(r"(^\s*)|(\s*$)","", header_line[i] )
    
    return header_line
  

def header_compare (labels_to_keep,csvfile,func = get_header):

    """returns a string for columns  """
    
    headers_to_check = func(csvfile)
    indecies = []
    #add the empty string check here.
    for i in range(len(headers_to_check)):
        if headers_to_check[i] in labels_to_keep:
            indecies.append(str(i+1))

    return ",".join(indecies) #for csvcut creates a string od digits.

def create_clean_csv(file,columns,date_stamp="unspecified_date"):

    ''' create a csv file (csvcut applied) and moves it to output folder. Date_stamp needs to be defined before calling this function'''
  
    os.system(f'csvcut -c {columns} {file} >> "cleaned"_{file}')
    os.system(f"mv 'cleaned_'{file} ./'output_files_'{date_stamp}")


if __name__ == '__main__':

    file_list = glob.glob('*.csv')
    for file in file_list:
        header_trim_and_lower(file)
        columns = header_compare(labels_to_keep,file)
        create_clean_csv(file,columns,date_stamp)
        os.remove(file)

print("Hello, I created a folder called 'input and the date stamp' and moved all the original files so records are safe.")

print("All the finished files will hava a 'cleaned' label at the output and the date stamp directory!"+"\n" +"You can always merge those with csvMerge script !")

