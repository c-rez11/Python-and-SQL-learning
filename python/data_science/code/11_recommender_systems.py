# Recommender Systems
# Most common types: Content-Based and Collaborative Filtering

# Content-based: focus on the attributes of the items and give recommendations
    # based on the similarities between them

#Collaborative Filtering: recommendations based on the knowledge of users' attitude to items.
    # This is more common in the real world


#this will be a content-based recommendation exercise

import numpy as np
import pandas as pd

#user ratings of different items (aka movies)
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('C:/Users/User/Desktop/python/c-rez11/learning/python/data_science/data/u.data', sep='\t', names=column_names)
print(df.head())

# dictionary of item IDs and movie titles
movie_titles = pd.read_csv("C:/Users/User/Desktop/python/c-rez11/learning/python/data_science/data/Movie_Id_Titles")
movie_titles.head()

df = pd.merge(df,movie_titles,on='item_id') # this is like a SQL join
print(df.head())

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')

# average rating and number of ratings
print(df.groupby('title')['rating'].mean().sort_values(ascending=False).head())
print(df.groupby('title')['rating'].count().sort_values(ascending=False).head())
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
print(ratings.head())

# movie title, avg rating, and number of ratings
ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())
ratings.head()

# some visuals of the data
plt.figure(figsize=(10,4))
ratings['num of ratings'].hist(bins=70)
sns.jointplot(x='rating',y='num of ratings',data=ratings,alpha=0.5)

# Recommendation algorithm
moviemat = df.pivot_table(index='user_id',columns='title',values='rating')
print(moviemat.head()) # a lot of N/A because most users have only seen a few movies

# let's pick two of the highest-rated movies: Star Wars and Liar Liar
print(ratings.sort_values('num of ratings',ascending=False).head(10))

# user ratings for the two movies
starwars_user_ratings = moviemat['Star Wars (1977)']
liarliar_user_ratings = moviemat['Liar Liar (1997)']
print(starwars_user_ratings.head())

# use corrwith() to get correlations between two pandas series
similar_to_starwars = moviemat.corrwith(starwars_user_ratings)
similar_to_liarliar = moviemat.corrwith(liarliar_user_ratings)

# clean this by removing N/A values and using a df instead of series
corr_starwars = pd.DataFrame(similar_to_starwars,columns=['Correlation'])
corr_starwars.dropna(inplace=True)
print(corr_starwars.head())

# sort by correlation
#print(corr_starwars.sort_values('Correlation',ascending=False).head(10))

# however, the results look weird (because a lot of movies were only watched one time
#   by users who watched Star Wars)

# filter out movies with less than 100 reviews (based on histogram from earlier)

#print(corr_starwars[corr_starwars['num of ratings']>100].sort_values('Correlation',ascending=False).head())
# these results make sense. Star Wars has perfect correlation (obviously)
# and the two Star Wars sequels are right behind it

# now the same for Liar Liar
corr_liarliar = pd.DataFrame(similar_to_liarliar,columns=['Correlation'])
corr_liarliar.dropna(inplace=True)
corr_liarliar = corr_liarliar.join(ratings['num of ratings'])
print(corr_liarliar[corr_liarliar['num of ratings']>100].sort_values('Correlation',ascending=False).head())

plt.show()

