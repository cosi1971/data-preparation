# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 16:31:05 2019

@author: pohch
"""
''' this is a profiling package practice
'''
import pandas as pd
import pandas_profiling as pd_prof
data1 = pd.read_csv(r'C:\Users\pohch\Google Drive\Python notebook\bank.csv')
data2 = pd.read_csv(r'C:\Users\pohch\Google Drive\Python notebook\ToyotaCorolla.csv')
#%%
#pandas_profiling.ProfileReport(data1) 
#data.profile_report()
#%%
profile1 = pd_prof.ProfileReport(data1)
profile2 = pd_prof.ProfileReport(data2) 
#data.profile_report(title='bank profile report')
profile1.to_file(outputfile=r"C:\Users\pohch\Google Drive\Python notebook\bank_profiling.html") 
profile2.to_file(outputfile=r"C:\Users\pohch\Google Drive\Python notebook\ToyotaCorolla.html") 
