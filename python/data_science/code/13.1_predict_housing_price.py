import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# real housing data from Kaggle. housing prices from King County (Seattle)
df = pd.read_csv('C:/Users/User/Desktop/python/c-rez11/Udemy/python/data_science/data/kc_house_data.csv')

# Step 1: Exploratory Data Analysis

print(df.isnull().sum()) #check for missing data
print(df.head()) #get an idea of the data

#sns.distplot(df['price']) # consider removing some of the very high priced homes
print(df.corr()['price'].sort_values()) # look at the correlation of price and each variable
#sns.boxplot(x='bedrooms',y='price', data=df) # boxplot looking at bedroom/price distribution
#plt.figure(figsize=(12,8))
#sns.scatterplot(x='price',y='long',data=df) #using longitude (long) to see where price irregularities appear
    #there appears to be an expensive neighborhood at the -122.2 longitude

#plt.figure(figsize=(12,8))
#sns.scatterplot(x='long',y='lat',data=df) #plots the city. basically a map of Seattle
#plt.figure(figsize=(12,8))
#sns.scatterplot(x='long',y='lat',data=df,hue='price') #create heat map for high prices

# drop outliers
print(df.sort_values('price',ascending=False).head(20))
# it looks like we can cut off the top outliers (also see the distplot from above)

print(len(df)*.01) # there are 215 houses in top 1%. We use this for the below code
non_top_1 = df.sort_values('price',ascending=False).iloc[216:] # new dataset that excludes top 1%

plt.figure(figsize=(12,8))
sns.scatterplot(x='long',y='lat',data=non_top_1,hue='price') #create heat map for non top 1% house prices

# Step 2: Feature Engineering

# date
df = df.drop('id',axis=1)
df['date'] = pd.to_datetime(df['date']) # change data to datetime object, making it easier to further manipulate
df['year'] = df['date'].apply(lambda date: date.year)
# reminder: lambda function is the same as doing this
# def year_extraction(date):
#   return date.year
df['month'] = df['date'].apply(lambda date: date.month)

print(df.groupby('month').mean()['price']) # see if price varies by month. Not a ton of variation
df = df.drop('date',axis=1) # now that we have separated year and month, we don't need the original date anymore

# zipcode
print(df['zipcode'].value_counts()) # with 70 zipcodes, creating dummy variables is impractical.
df = df.drop('zipcode',axis=1) # even though it might serve as a good proxy for school district, we'll drop it for now

# year_renovated
print(df['yr_renovated'].value_counts()) # one concern: zero is not actually a year; it means the house wasn't renovated
    # however, since more recent renovations = higher value, we'll leave it at zero

# sqft_basement
print(df['sqft_basement'].value_counts()) # similar to year_renovated, zero sq ft means no basement
    # because bigger basement = higher value, we'll also keep as continuous variable



#plt.show()
