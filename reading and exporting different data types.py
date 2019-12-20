# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 09:32:34 2019

@author: leeko
"""
"""
read various type of files and import into dataframe
"""

#--------
#read csv into dataframe
import pandas as pd
#read the passenger csv into dataframe
dataimport = r'c:\Users\leeko\Google Drive\Python notebook\AirPassengers.csv'
# rfor reading \ as char
df=pd.read_csv(dataimport)
#read a single column into a series data
df3=df['Month']

#--------
#read the excel into dataframe
datapath= r'c:\Users\leeko\Google Drive\Python notebook\personalISQ.xlsx'
df1=pd.read_excel(datapath)
#--------

#read a csv into a timeseries
import pandas as pd
importfile = r'C:\Users\leeko\Google Drive\Python notebook\AirPassengers.csv'
##If from local drive, then use r'C:\....\file_name' since the \ special characters needs to be read like text.
rawdata=pd.read_csv(importfile)
#extract the needed columns into the timecol and seriescol and make it a dataframe object
timecol, seriescol= 'Month','#Passengers'
rawts=rawdata[[timecol,seriescol]].copy()
#convert the dataframe object into a timeseries
rawts[timecol]=pd.to_datetime(rawts[timecol],infer_datetime_format=True)
indexedts=rawts.set_index([timecol])
indexedts.describe
#check any missing data
indexedts.isna()
#--------

#read a column into a series data
dataimport = r'c:\Users\leeko\Google Drive\Python notebook\AirPassengers.csv'

#________

#read a sql table or query into a dataframe
from sqlalchemy import create_engine
# Create your engine.
engine = create_engine('sqlite:///:memory:') #using SQLite SQL database engine 
tablename='tablename'
with engine.connect() as conn, conn.begin():
    sql='select ** from '+tablename+' where pay>''50'''
    colnames=[['col1','col2','col3']]
    df2=pd.read_sql(sql,conn, index_col=colnames)
#_______


#%%
"""web-scrape ill-formatted html table and import into dataframe
"""
import pandas as pd

""" scrap tables from website"""
import requests
from bs4 import BeautifulSoup
class HTMLTableParser:
       
    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
#        return [(id,self.parse_html_table(table))\
#                for id,table in enumerate(soup.find_all('table')) ] 
        return [(self.parse_html_table(table))\
        for table in soup.find_all('table')]  
#        return [(self.parse_html_table(table))\ for table in soup.find_all('table'))]
    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        column_names = []
    
        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):
            
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
                    
            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())
    
        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")
    
        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
                
        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
        
        return df
PID='N00899395'
url = "https://banner.unf.edu/pls/nfpo/wksfwbs.p_instructor_isq_grade?pv_instructor="+PID
hp = HTMLTableParser()

#Grabbing the table from the tuple, 6 is used since that is where the table of isq scores are found by manula check
table = hp.parse_url(url)
isq=table[6]
GPAdist=table[8]
isq.isna()
# depending on how the soup is indexed - 
# as a list of data frames or arrays of dataframes
#had to do the next 3 lines since html tag is ill-coded - </t> missing
#isq=table.dropna(axis=1)
#newnames=list(table.columns)
#isq.columns=list(table.columns)

#%%
"""
exporting
"""
