# RansomToolKit
This tool box is to help processing ransomware data.
Currently there are 4 tools built.
The first time you rund the scripts you might need to download some of the libraries needed to run the scripts.
This is the first version so please be patient with possible issues and your feedback is very welcomed.

### autoCut
This will cut the csv file based on the list of labels that our server accepts.
Script works on all the files in the current directory.

### convertAllExcel2Csv
This script converts xlsx files into csv files.
User can choose to extract all the sheets or just the first sheet.
Once it's run script will work on all the files with the .xlsx files.

### stackAllCsv
The script can merge csv files with different headers or header value order.
Once it's run it will work on all the files with .csv extension and create one .tsv file.
One important thing is all the header values MUST be server keywords. ( first name >> namefirst) 


### csvfix
The script fixes common mistakes in csv files such as mismatching header numbers in the rows or " marks. 
This script takes one argument, the file name to run. 

# ransomWareToolBox
# ransomWareToolBox
