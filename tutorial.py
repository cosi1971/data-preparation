#!/usr/bin/env python
# coding: utf-8

# # PyCon 2019: Data Science Best Practices with pandas ([video](https://www.youtube.com/watch?v=dPwLlJkSHLo))
# 
# ### GitHub repository: https://github.com/justmarkham/pycon-2019-tutorial
# 
# ### Instructor: Kevin Markham
# 
# - Website: https://www.dataschool.io
# - YouTube: https://www.youtube.com/dataschool
# - Patreon: https://www.patreon.com/dataschool
# - Twitter: https://twitter.com/justmarkham
# - GitHub: https://github.com/justmarkham

# ## 1. Introduction to the TED Talks dataset
# 
# https://www.kaggle.com/rounakbanik/ted-talks

# In[1]:


import pandas as pd
pd.__version__


# In[2]:


import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


ted = pd.read_csv(r'C:\Users\leeko\Google Drive\Python notebook\ted.csv')


# In[4]:
# each row represents a single talk
ted.head()


# In[5]:


# rows, columns
ted.shape


# In[6]:


# object columns are usually strings, but can also be arbitrary Python objects (lists, dictionaries)
ted.dtypes


# In[7]:


# count the number of missing values in each column
ted.isna().count()
#%%
ted.dtypes
#%%
ted.describe()
ted_summary=ted.describe()
# ## 2. Which talks provoke the most online discussion?

# In[8]:
ted.speaker_occupation
#%%
# sort by the number of first-level comments, though this is biased in favor of older talks
ted.sort_values('comments').tail()


# In[9]:


# correct for this bias by calculating the number of comments per view
ted['comments_per_view'] = ted.comments / ted.views
ted.duration


# In[10]:


# interpretation: for every view of the same-sex marriage talk, there are 0.002 comments
ted.sort_values('comments_per_view').tail()


# In[11]:


# make this more interpretable by inverting the calculation
ted['views_per_comment'] = ted.views / ted.comments


# In[12]:


# interpretation: 1 out of every 450 people leave a comment
ted.sort_values('views_per_comment').head()


# Lessons:
# 
# 1. Consider the limitations and biases of your data when analyzing it
# 2. Make your results understandable

# ## 3. Visualize the distribution of comments

# In[13]:


# line plot is not appropriate here (use it to measure something over time)
ted.comments.plot()


# In[14]:


# histogram shows the frequency distribution of a single numeric variable
ted.comments.plot(kind='hist')


# In[15]:


# modify the plot to be more informative
ted[ted.comments < 1000].comments.plot(kind='hist')

#%%
ted[ted.comments < 1000].views.plot(kind='hist')
# In[16]:


# check how many observations we removed from the plot
ted[ted.comments >= 1000].shape


# In[17]:


# can also write this using the query method
ted.query('comments < 1000').comments.plot(kind='hist')


# In[18]:


# can also write this using the loc accessor
ted.loc[ted.comments < 1000, 'comments'].plot(kind='hist')


# In[19]:


# increase the number of bins to see more detail
ted.loc[ted.comments < 1000, 'comments'].plot(kind='hist', bins=20)


# In[20]:


# boxplot can also show distributions, but it's far less useful for concentrated distributions because of outliers
ted.loc[ted.comments < 1000, 'comments'].plot(kind='box')


# Lessons:
# 
# 1. Choose your plot type based on the question you are answering and the data type(s) you are working with
# 2. Use pandas one-liners to iterate through plots quickly
# 3. Try modifying the plot defaults
# 4. Creating plots involves decision-making

# ## 4. Plot the number of talks that took place each year
# 
# Bonus exercise: calculate the average delay between filming and publishing

# In[21]:


# event column does not always include the year
ted.event.sample(10)


# In[22]:


# dataset documentation for film_date says "Unix timestamp of the filming"
ted.film_date.head()


# In[23]:


# results don't look right
pd.to_datetime(ted.film_date).head()


# [pandas documentation for `to_datetime`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html)

# In[24]:


# now the results look right
pd.to_datetime(ted.film_date, unit='s').head()


# In[25]:


ted['film_datetime'] = pd.to_datetime(ted.film_date, unit='s')


# In[26]:


# verify that event name matches film_datetime for a random sample
ted[['event', 'film_datetime']].sample(5)

ted.film_datetime
# In[27]:


# new column uses the datetime data type (this was an automatic conversion)
ted.dtypes


# In[28]:


# datetime columns have convenient attributes under the dt namespace
ted.film_datetime.dt.year.head()


# In[29]:


# similar to string methods under the str namespace
ted.event.str.lower().head()


# In[30]:


# count the number of talks each year using value_counts()
ted.film_datetime.dt.year.value_counts()


# In[31]:


# points are plotted and connected in the order you give them to pandas
ted.film_datetime.dt.year.value_counts().plot()


# In[32]:


# need to sort the index before plotting
ted.film_datetime.dt.year.value_counts().sort_index().plot()


# In[33]:


# we only have partial data for 2017
ted.film_datetime.min()


# Lessons:
# 
# 1. Read the documentation
# 2. Use the datetime data type for dates and times
# 3. Check your work as you go
# 4. Consider excluding data if it might not be relevant

# ## 5. What were the "best" events in TED history to attend?

# In[34]:


# count the number of talks (great if you value variety, but they may not be great talks)
ted.event.value_counts().head()


# In[35]:
ted.groupby('event').views

# use views as a proxy for "quality of talk"
ted.groupby('event').views.mean().head()


# In[36]:


# find the largest values, but we don't know how many talks are being averaged
ted.groupby('event').views.mean().sort_values().tail()


# In[37]:


# show the number of talks along with the mean (events with the highest means had only 1 or 2 talks)
ted.groupby('event').views.agg(['count', 'mean']).sort_values('mean').tail()


# In[38]:


# calculate the total views per event
ted.groupby('event').views.agg(['count', 'mean', 'sum']).sort_values('sum').tail()


# Lessons:
# 
# 1. Think creatively for how you can use the data you have to answer your question
# 2. Watch out for small sample sizes

# ## 6. Unpack the ratings data

# In[39]:


# previously, users could tag talks on the TED website (funny, inspiring, confusing, etc.)
ted.ratings.head()


# In[40]:


# two ways to examine the ratings data for the first talk
ted.loc[0, 'ratings']
ted.ratings[0]


# In[41]:


# this is a string not a list
type(ted.ratings[0])


# In[42]:


# convert this into something useful using Python's ast module (Abstract Syntax Tree)
import ast


# In[43]:


# literal_eval() allows you to evaluate a string containing a Python literal or container
ast.literal_eval('[1, 2, 3]')


# In[44]:


# if you have a string representation of something, you can retrieve what it actually represents
type(ast.literal_eval('[1, 2, 3]'))

# In[45]:


# unpack the ratings data for the first talk
ast.literal_eval(ted.ratings[0])


# In[46]:


# now we have a list (of dictionaries)
type(ast.literal_eval(ted.ratings[0]))


# In[47]:


# define a function to convert an element in the ratings Series from string to list
def str_to_list(ratings_str):
    return ast.literal_eval(ratings_str)


# In[48]:


# test the function
str_to_list(ted.ratings[0])


# In[49]:


# Series apply method applies a function to every element in a Series and returns a Series
ted.ratings.apply(str_to_list).head()

# In[50]:


# lambda is a shorter alternative
ted.ratings.apply(lambda x: ast.literal_eval(x)).head()


# In[51]:


# an even shorter alternative is to apply the function directly (without lambda)
ted.ratings.apply(ast.literal_eval).head()


# In[52]:


ted['ratings_list'] = ted.ratings.apply(lambda x: ast.literal_eval(x))


# In[53]:


# check that the new Series looks as expected
ted.ratings_list[0]


# In[54]:


# each element in the Series is a list
type(ted.ratings_list[0])


# In[55]:


# data type of the new Series is object
ted.ratings_list.dtype


# In[56]:


# object is not just for strings
ted.dtypes


# Lessons:
# 
# 1. Pay attention to data types in pandas
# 2. Use apply any time it is necessary

# ## 7. Count the total number of ratings received by each talk
# 
# Bonus exercises:
# 
# - for each talk, calculate the percentage of ratings that were negative
# - for each talk, calculate the average number of ratings it received per day since it was published

# In[57]:


# expected result (for each talk) is sum of count
ted.ratings_list[0]


# In[58]:


# start by building a simple function
def get_num_ratings(list_of_dicts):
    return list_of_dicts[0]


# In[59]:


# pass it a list, and it returns the first element in the list, which is a dictionary
get_num_ratings(ted.ratings_list[0])


# In[60]:


# modify the function to return the vote count
def get_num_ratings(list_of_dicts):
    return list_of_dicts[0]['count']


# In[61]:


# pass it a list, and it returns a value from the first dictionary in the list
get_num_ratings(ted.ratings_list[0])


# In[62]:


# modify the function to get the sum of count
def get_num_ratings(list_of_dicts):
    num = 0
    for d in list_of_dicts:
        num = num + d['count']
    return num


# In[63]:


# looks about right
get_num_ratings(ted.ratings_list[0])


# In[64]:


# check with another record
ted.ratings_list[1]


# In[65]:


# looks about right
get_num_ratings(ted.ratings_list[1])


# In[66]:


# apply it to every element in the Series
ted.ratings_list.apply(get_num_ratings).head()


# In[67]:


# another alternative is to use a generator expression
sum((d['count'] for d in ted.ratings_list[0]))


# In[68]:


# use lambda to apply this method
ted.ratings_list.apply(lambda x: sum((d['count'] for d in x))).head()


# In[69]:


# another alternative is to use pd.DataFrame()
pd.DataFrame(ted.ratings_list[0])['count'].sum()


# In[70]:


# use lambda to apply this method
ted.ratings_list.apply(lambda x: pd.DataFrame(x)['count'].sum()).head()


# In[71]:


ted['num_ratings'] = ted.ratings_list.apply(get_num_ratings)


# In[72]:


# do one more check
ted.num_ratings.describe()


# Lessons:
# 
# 1. Write your code in small chunks, and check your work as you go
# 2. Lambda is best for simple functions

# ## 8. Which occupations deliver the funniest TED talks on average?
# 
# Bonus exercises:
# 
# - for each talk, calculate the most frequent rating
# - for each talk, clean the occupation data so that there's only one occupation per talk

# ### Step 1: Count the number of funny ratings

# In[73]:


# "Funny" is not always the first dictionary in the list
ted.ratings_list.head()


# In[74]:


# check ratings (not ratings_list) to see if "Funny" is always a rating type
ted.ratings.str.contains('Funny').value_counts()


# In[75]:


# write a custom function
def get_funny_ratings(list_of_dicts):
    for d in list_of_dicts:
        if d['name'] == 'Funny':
            return d['count']



# In[76]:


# examine a record in which "Funny" is not the first dictionary
ted.ratings_list[3]


# In[77]:


# check that the function works
get_funny_ratings(ted.ratings_list[3])


# In[78]:


# apply it to every element in the Series
ted['funny_ratings'] = ted.ratings_list.apply(get_funny_ratings)
ted.funny_ratings.head()


# In[79]:


# check for missing values
ted.funny_ratings.isna().sum()


# ### Step 2: Calculate the percentage of ratings that are funny

# In[80]:


ted['funny_rate'] = ted.funny_ratings / ted.num_ratings


# In[81]:


# "gut check" that this calculation makes sense by examining the occupations of the funniest talks
ted.sort_values('funny_rate').speaker_occupation.tail(20)


# In[82]:


# examine the occupations of the least funny talks
ted.sort_values('funny_rate').speaker_occupation.head(20)


# ### Step 3: Analyze the funny rate by occupation

# In[83]:


# calculate the mean funny rate for each occupation
ted.groupby('speaker_occupation').funny_rate.mean().sort_values().tail()


# In[84]:


# however, most of the occupations have a sample size of 1
ted.speaker_occupation.describe()


# ### Step 4: Focus on occupations that are well-represented in the data

# In[85]:


# count how many times each occupation appears
ted.speaker_occupation.value_counts()


# In[86]:


# value_counts() outputs a pandas Series, thus we can use pandas to manipulate the output
occupation_counts = ted.speaker_occupation.value_counts()
type(occupation_counts)


# In[87]:


# show occupations which appear at least 5 times
occupation_counts[occupation_counts >= 5]


# In[88]:


# save the index of this Series
top_occupations = occupation_counts[occupation_counts >= 5].index
top_occupations


# ### Step 5: Re-analyze the funny rate by occupation (for top occupations only)

# In[89]:


# filter DataFrame to include only those occupations
ted_top_occupations = ted[ted.speaker_occupation.isin(top_occupations)]
ted_top_occupations.shape


# In[90]:


# redo the previous groupby
ted_top_occupations.groupby('speaker_occupation').funny_rate.mean().sort_values()


# Lessons:
# 
# 1. Check your assumptions about your data
# 2. Check whether your results are reasonable
# 3. Take advantage of the fact that pandas operations often output a DataFrame or a Series
# 4. Watch out for small sample sizes
# 5. Consider the impact of missing data
# 6. Data scientists are hilarious
