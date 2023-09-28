# K Means Clustering: Unsupervised learning
#method for clustering unlabeled data in an unsupervised learning process

#method
#1. Choose a number of clusters (K)
#2. Randomly assign each point to a cluster
#3. For each cluster, compute the center point of the cluster
#4. Reassign each data point to the cluster whose center point is closest
#5. Repeat until there's no more reassigning

#how to choose the best K value?
#1. Start with sum of squared errors (SSE). Notice how the SSE decreases as K gets larger
#2. Find the point when the rate of SSE decrease takes a dip--this graph would look like an elbow,
    #which is why it's called the elbow method.

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs #this allows us to generate blob-like data to play with
data = make_blobs(n_samples=200, n_features=2, 
                           centers=4, cluster_std=1.8,random_state=101)
#plt.scatter(data[0][:,0],data[0][:,1],c=data[1],cmap='rainbow')
plt.show()

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4)
kmeans.fit(data[0])
kmeans.cluster_centers_
kmeans.labels_ #reports the labels that it thinks are true for the clusters
#if you were working with real data and didn't have the labels, you'd be done here.
#You wouldn't be able to compare the labels to the actual values like we're doing here.

#Because this is unsupervised machine learning, you wouldn't use it to predict labels and see
    #how they compare to the actual labels
#What you'd do is use it to try and FIND labels in your data. You'd do this by playing with the number of clusters.


f, (ax1, ax2) = plt.subplots(1, 2, sharey=True,figsize=(10,6))
ax1.set_title('K Means')
ax1.scatter(data[0][:,0],data[0][:,1],c=kmeans.labels_,cmap='rainbow')
ax2.set_title("Original")
ax2.scatter(data[0][:,0],data[0][:,1],c=data[1],cmap='rainbow')


#project: identify public vs private universities

import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/User/Desktop/python/c-rez11/learning/python/data_science/data/College_Data',index_col=0)
print(df.head())
#df.info()
#df.describe()

#what does the data look like when we separate public vs private?
#here's a plot of grad rate and room/board separated by university type
#sns.set_style('whitegrid')
#sns.lmplot('Room.Board','Grad.Rate',data=df, hue='Private',
#           palette='coolwarm',size=6,aspect=1,fit_reg=False)

#sns.set_style('whitegrid') #undergrad size and out-of-state
#sns.lmplot('Outstate','F.Undergrad',data=df, hue='Private',
#           palette='coolwarm',size=6,aspect=1,fit_reg=False)

#more examples in the lesson

#K means clustering

kmeans = KMeans(n_clusters=2)
kmeans.fit(df.drop('Private',axis=1)) #remove the label so that we can test how we do
#in the real world, we wouldn't know how our predicted outcome compares to reality in such an easy way

kmeans.cluster_centers_ #aka the cluster means.
#this will have the same number of dimensions as we have features.
#we have 17 features, so we have 17 dimensions for public vs private

#THERE ARE STILL ONLY 2 CLUSTERS (PUBLIC AND PRIVATE), BUT EACH CLUSTER HAS 17 DIMENSIONS,
    #SO THE CLUSTER MEAN WOULD LOOK LIKE SOMETHING OUT OF THE MATRIX

def converter(private):
    if private=='Yes':
        return 1
    else:
        return 0
df['Cluster'] = df['Private'].apply(converter)
print(df.head())

from sklearn.metrics import confusion_matrix,classification_report
print(confusion_matrix(df['Cluster'],kmeans.labels_))
print(classification_report(df['Cluster'],kmeans.labels_))

print(df['Private'].describe()) # just to confirm I'm reading the matrices correctly
#plt.show()