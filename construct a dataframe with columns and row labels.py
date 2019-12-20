# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 18:34:39 2019

@author: leeko
"""
import pandas as pd
import numpy as np

#%%
#DataFrame([data, index, columns, dtype, copy])
df = pd.DataFrame(index = ['1', '2', '3'], columns=['a', 'b', 'c'])
df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),columns=['a', 'b', 'c'])

