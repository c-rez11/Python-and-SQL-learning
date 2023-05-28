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


# Step 3: train/test split

# Separate features from label
X = df.drop('price',axis=1).values # this is done because tensorflow doesn't like pandas dataframes
y = df['price'].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

# scaling the data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test) # we don't scale our test data because we wouldn't know this 
    # in a real-world application

# Step 4: Create the model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

print(X_train.shape) # we have 19 different features, so we should probably have 19 neurons in our layer

model = Sequential()
# adding the layers
model.add(Dense(19,activation='relu'))
model.add(Dense(19,activation='relu'))
model.add(Dense(19,activation='relu'))
model.add(Dense(19,activation='relu'))
model.add(Dense(1)) # final layer for our output

model.compile(optimizer='adam',loss='mse')

model.fit(x=X_train, y=y_train, validation_data=(X_test,y_test), 
          batch_size=128,epochs=400)
# note on validation: it checks how well the model is performing at each epoch
#   WITHOUT affecting the actual weights of the model
# note on batch_size: the smaller the batch size, longer training will take

losses = pd.DataFrame(model.history.history)
losses.plot() # as we can see in the graph, the loss matches validation loss, meaning we're not overfitting
#   if the validation loss increased as time went on, we know we'd have an overfitting problem

from sklearn.metrics import mean_squared_error,mean_absolute_error,explained_variance_score
predictions = model.predict(X_test)
np.sqrt(mean_squared_error(y_test,predictions)) # root mean squared error
mean_absolute_error(y_test,predictions) # mean absolute error
# definition of both: avg magnitude of errors in a set of predictions WITHOUT considering direction
# RMSE is better if you care about your model's performance against outliers,
    # as RMSE more heavily weights the error of outliers


df['price'].describe() # with an average price of ~$500k, our avg error is $100k

explained_variance_score(y_test, predictions) # how much of the data is explained by our model

plt.scatter(y_test, predictions) # it looks like our model's accuracy is affected by outliers.
    # Because of this, maybe we should consider removing the outliers (very expensive homes),
    # although we'd be sacrificing our model's ability to predict those high-priced homes
    # which we're probably okay with
plt.plot(y_test,y_test,'r') # gets a fit line of our predictions

# let's say we have our model and a new house comes on the market. How would we do?
single_house = df.drop('price',axis=1).iloc[0]
single_house = scaler.transform(single_house.values.reshape(-1,19)) # reshape adds double-brackets which are needed to further progress
    # scale the data the way we did when we initially created the model
model.predict(single_house) 
print(df.head(1)) # model predicts $288k, but actually $221k
# for further accuracy, consider dropping the outliers




#plt.show()
