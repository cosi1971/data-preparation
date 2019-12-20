# -*- coding: utf-8 -*-
"""
Created on Thu May 16 08:26:39 2019

@author: leeko
"""
#%%
#import all the libraries
import numpy as np
import scipy as scp
import matplotlib as plt
import pandas as pd

""" scrap tables from website"""
import requests
from bs4 import BeautifulSoup
#%%    
"""html_string = '''
<table>
    <tr>
        <td> Hello! </td>
        <td> Table </td>
    </tr>
</table>
'''

soup = BeautifulSoup(html_string, 'lxml') # Parse the HTML as a string

table = soup.find_all('table')[0] # Grab the first table

new_table = pd.DataFrame(columns=range(0,2), index = [0]) # I know the size 

row_marker = 0
for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    for column in columns:
        new_table.iat[row_marker,column_marker] = column.get_text()
        column_marker += 1

new_table"""
#In [1]
#%%
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
#%%
#import requests
#url = "https://www.fantasypros.com/nfl/reports/leaders/qb.php?year=2015"
#response = requests.get(url)
#response.text[:100] # Access the HTML with the text property
#%%
#define the targeted instructor
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,8
isqdb=list()
PIDlist = ('N00899395','N00824592','N00637168','N00639162','N00634034','N00777345','N00899395')
for PID in PIDlist:
    url = "https://banner.unf.edu/pls/nfpo/wksfwbs.p_instructor_isq_grade?pv_instructor="+PID
    hp = HTMLTableParser()

    #Grabbing the table from the tuple, 6 is used since that is where the isq scores are found by manula check
    table = hp.parse_url(url)[6]

    # depending on how the soup is indexed - as a list of data frames or arrays of dataframes
    isq=table.dropna(axis=1)
    newnames=list(table.columns)[0:13]
    isq.columns=newnames
    #replace the term labels with numerical months
    isq['Term']=isq['Term'].str.replace('Spring','01-01-')
    isq['Term']=isq['Term'].str.replace('Summer','01-05-')
    isq['Term']=isq['Term'].str.replace('Fall','01-08-')
    isq['Term']=isq['Term'].str.replace(' ','')
#    isq.index.rename('ID')
    isq.insert(0, 'PID',PID)
    isqdb.append(isq)
    plt.xlabel('Term')
    plt.ylabel('Mean')
    plt.legend(loc='best')
    plt.plot (isq['Term'],isq['Mean'],label=PID)
plt.show
#%%


