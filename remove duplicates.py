# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 22:24:25 2019

@author: leeko
"""

# exercise of remove duplicates names to get a namelist
import pandas as pd
import numpy as np
file=r'D:\OneDrive - University of North Florida\Annual report\Kosze_ISQ Data.xlsx'
data =pd.read_excel(file)
#%%
name= data[['Name','Term']]
name['Gender']=name['Name']
dict_name = name['Name'].value_counts()
#%%
names =name[['Name']]
names.count()
#%%
names =name[['Name']].drop_duplicates()
names['Freq']= dict_name.values
names.plot(kind='bar')
#%%
data.groupby('Name').value_counts()