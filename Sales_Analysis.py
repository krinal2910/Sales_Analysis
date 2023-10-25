#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## importing  pandas library


# In[1]:


import pandas as pd 
import os


# ## Merging 12 months of data into single csv file 

# In[150]:


df = pd.read_csv(r"/Users/krinalpatel/Desktop/project/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_April_2019.csv")

all_months_data = pd.DataFrame()
files = [file  for file in os.listdir('/Users/krinalpatel/Desktop/project/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data')]

for file in files:
    df = pd.read_csv("/Users/krinalpatel/Desktop/project/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/"+file)
    all_months_data= pd.concat([all_months_data, df])
    
all_months_data.to_csv("all_data.csv", index= False)


# ## Read in updated dataframe

# In[156]:


df = pd.read_csv("all_data.csv")
df


# ## Cleaning the data

# In[157]:


#To find how many and where NaN are
nan_df = df[df.isna().any(axis=1)]
nan_df


# In[158]:


#Removing NaN
df = df.dropna(how ='all')
df


# In[159]:


## find 'or' and delete it
df = df[df['Order Date'].str[0:2] != 'Or']


# ## Q-1 What is the best month for sale ? how much was earned that month?

# In[161]:


df.loc[:, 'Month'] = df['Order Date'].str[0:2].astype('int32')


# In[162]:


## convert columns into correct data types
df.loc[:,'Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'])  
df.loc[:,'Price Each'] = pd.to_numeric(df['Price Each']) 


# In[165]:


## Add Sales column
df.loc[:, 'Sales'] = df['Quantity Ordered'] * df['Price Each']
df


# In[166]:


results = df.groupby('Month').sum()['Sales']
results


# In[169]:


import matplotlib.pyplot as plt


# In[170]:


months = range(1,13)
plt.bar(months, results)
plt.xticks(months)
plt.ylabel('Sales in USD $')
plt.xlabel('Month number')

#Answer : According to results December is the best month with 4613443.34 $USD sale


# ## Q-2 which city has the highest number of sales?

# In[168]:


##Adding city column
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]
df.loc[:, 'City'] = df['Purchase Address'].apply(lambda x: get_city(x) + ' (' + get_state(x) + ')')
df


# In[171]:


results = df.groupby('City').sum()['Sales']
results


# In[172]:


City = [city for city, df in df.groupby('City')]

plt.bar(City, results)
plt.xticks(City, rotation = 'vertical', size=8)
plt.ylabel('Sales in USD $')
plt.xlabel('Cities')

##Answer: Based on numbers and chart San Fancisco city with 8262203.9 $USD highest number of sale 


# ## Q-3 what time should we display advertisment to maximize likelihood of customer buying product ?

# In[190]:


df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%y %H:%M', errors='coerce')
print(df['Order Date'].dtype)


# In[191]:


df.loc[:, 'Hour'] = df['Order Date'].dt.hour
df.loc[:, 'Minute'] = df['Order Date'].dt.minute
df


# In[192]:


hours = [hour for hour, df in df.groupby('Hour')]

plt.plot(hours, df.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of orders')
plt.grid()
plt.show()

##Answer: Based on chart 11AM and 7PM are peak time. So its best time to display advertisment to maximize liklihood of customer buying product


# # Q-4 what products are more often sold together?

# In[194]:


df = df[df['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df[['Order ID', 'Grouped']].drop_duplicates()


# In[202]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
        row_list = row.split(',')
        count.update(Counter(combinations(row_list, 2)))

count.most_common(10)

##Answer : iphone with lightning charging cable more often were sold together.


# # Q-5 What product sold the most ? and why you think it sold the most?

# In[196]:


product_grouped = df.groupby('Product')


# In[197]:


df['Quantity Ordered'] = df['Quantity Ordered'].astype(int)


# In[222]:


# Group the data by 'Product' and calculate the sum of 'Quantity Ordered'
quantity_grouped = df.groupby('Product')['Quantity Ordered'].sum()

plt.bar(products, quantity_grouped)
plt.xticks(rotation='vertical')  
plt.ylabel('Quantity ordered')
plt.xlabel('Products')  
plt.show()

#Answer: based on chart 'USB charging cable' sold most.


# In[217]:


prices = df.groupby('Product')['Price Each'].mean()
prices


# In[227]:


fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, product_grouped, color='g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('product grouped', color='g')
ax2.set_ylabel('Price', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)
plt.show()


##Answer: Prices are inversely proportional to the quantity of items sold of each item


# In[ ]:




