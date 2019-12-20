# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:26:29 2019

@author: pohch
"""

# To find out where the pyspark
import findspark
findspark.init()
#%%
from pyspark.sql import SparkSession
spark1 = SparkSession.builder.appName('Ops').getOrCreate()
data=spark1.read.csv(r'C:\Users\pohch\Desktop\Spark\spark-2.4.4-bin-hadoop2.7\mnt\defg\flight-data\csv\2015-summary.csv', inferSchema=True, header=True)
data.printSchema()