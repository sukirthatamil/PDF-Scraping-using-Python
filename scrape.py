# Import the required Module
import tabula
import PyPDF2
import re
import pandas as pd
import pdfquery
import json
#For finding the page where "Roaming call details" text is available"
def tablevalues(filename,csvfilename):
	pattern = "Roaming Call Details"
	object = PyPDF2.PdfFileReader(filename)
	numPages = object.getNumPages()
	for i in range(0, numPages):
		pageObj = object.getPage(i)
		text = pageObj.extractText()
		for match in re.finditer(pattern, text):
			globals()['page']=i
	
	#Converted Pdf to csv to perform several cleanups
	tabula.convert_into(filename, csvfilename, output_format="csv", pages=page+1)
	df = pd.read_csv(csvfilename)
	try:
		#While extracting Both time and number were in same column so need to split and remove the column
		df[['Time1', 'Number1']] = df['Time Number'].str.split(' ', 1, expand=True)
		df.drop('Time Number', axis=1,inplace=True)
		#Removal of empty column
		df = df.drop(columns=df.columns[12])
		#Half of the table values were in different columns so seperating it into different dataframes and concatenating inorder to get them in same solumns
		col_list = list(df)
		df1=pd.DataFrame(df,columns=[col_list[0], col_list[1],col_list[2], col_list[3],col_list[4], col_list[5],col_list[6], col_list[7] ])
		df2=pd.DataFrame(df,columns=[col_list[8], col_list[9],col_list[10], col_list[14],col_list[15], col_list[11],col_list[12], col_list[13]])
		df2.columns=df1.columns
		df3=pd.concat([df1, df2], ignore_index=True, sort=False)
		df3.dropna(subset=['Date'], inplace=True)
		#Converted table values to json
		json1 = df3.to_json(orient='records')
		return json1
	except:
		print("Error occured while parsing table(Column names mismatch)")

def firstscrape(filename,json1):
	pdf = pdfquery.PDFQuery(filename)
	pdf.load(0)
	#Used to take coordinates by using xml
	#pdf.tree.write('samplepdf2.xml', pretty_print=True)
	#Took specific values from first page using xml components
	PhoneNumber = pdf.pq('LTTextLineHorizontal:in_bbox("94.2, 630.16, 140.424, 639.12")').text()
	Name= pdf.pq('LTTextLineHorizontal:in_bbox("25.91, 727.75, 96.518, 736.71")').text()
	Address1=pdf.pq('LTTextLineHorizontal:in_bbox("25.12, 715.16, 168.88, 724.12")').text()
	Address2=pdf.pq('LTTextLineHorizontal:in_bbox("25.12, 705.71, 127.68, 714.67")').text()
	Address3=pdf.pq('LTTextLineHorizontal:in_bbox("25.12, 696.27, 135.272, 705.23")').text()
	Address4=pdf.pq('LTTextLineHorizontal:in_bbox("25.12, 686.82, 96.04, 695.78")').text()
	Address5=pdf.pq('LTTextLineHorizontal:in_bbox("25.12, 677.38, 66.496, 686.34")').text()
	InvoicePeriod=pdf.pq('LTTextLineHorizontal:in_bbox("508.68, 761.98, 573.29, 773.18")').text()
	Invoice2=pdf.pq('LTTextLineHorizontal:in_bbox("427.83, 761.98, 490.65, 773.18")').text()
	BetInvoice=pdf.pq('LTTextLineHorizontal:in_bbox("496.12, 761.78, 507.087, 774.1")').text()
	Address=Address1+Address2+Address3+Address4+Address5
	Invoice=InvoicePeriod+BetInvoice+Invoice2
	#Converting data to json
	data = {"Name": Name, "Address": Address, "Mobile Number": PhoneNumber,"Invoice Period": Invoice}
	data1={"Call Details":json1}
	#Combining both data
	return (data|data1)
	

filename='Idea_Sample_1.pdf'
csvfilename="Table1.csv"
js=tablevalues(filename,csvfilename)
a=firstscrape(filename,js)
print(a)
