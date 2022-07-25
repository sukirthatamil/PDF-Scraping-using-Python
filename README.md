# PDF-Scraping-using-Python
Scraping PDF texts and tables by using tabula,PyPDF2,pandas  and pdfquery


Instructions and Explanation
Install the following Libraries

>>pip install tabula --user
>>pip install PyPDF2 --user
>>pip install pandas --user
>>pip install re --user
>>pip install pdfquery --user

Run the code by using
>>python filename.py

Requirements:
The pdf should be in the same directory as that of python file
Input file - File name provided in code
Output - Prints Json format of extracted texts in console

For extracting data from first page, used pdfquery as the data was in unstructured format and had no key value pairs, the other libraries that I tried didn't extract 
the data in any sequential manner

For extracting values from table, I used tabula(open source library) as it was able to identify table values eventhough there were no lines between table values
and convert table to csv format

Pandas was used to make some modifications in the csv file
1)For splitting one column into 2 (Time and Number)
2)For removing empty columns
3)Converitng them to dataframes and then to json format

PyPDF2 is used to traverse through the entire pdf to find if the term "Roaming call details" and get the page number and use it for table extraction
from that specific page.It is used ince it extracts content page by page.





