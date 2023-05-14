# Principal Component Analysis (PCA)
# PCA is an unsupervised statistical technique used to examine correlation among a set of variables
    # in order to identify the underlying structure of those variables

#this isn't a linear line of best fit (like a linear regression would have),
    #but rather an orthogonal (right angle) line of best fit,
    #with N dimensions

#goal of PCA: determine which features explain the most variance of the dataset

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer()
cancer.keys()
print(cancer['DESCR'])
df = pd.DataFrame(cancer['data'],columns=cancer['feature_names'])
#(['DESCR', 'data', 'feature_names', 'target_names', 'target'])

from sklearn.preprocessing import StandardScaler #scale our data so each feature has a single unit variance
scaler = StandardScaler()
scaler.fit(df)
scaled_data = scaler.transform(df)

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(scaled_data)

x_pca = pca.transform(scaled_data)
scaled_data.shape

plt.figure(figsize=(8,6))
plt.scatter(x_pca[:,0],x_pca[:,1],c=cancer['target'],cmap='plasma')
plt.xlabel('First principal component')
plt.ylabel('Second Principal Component')
#each component is a combination of the 30 original features, similar to how
    #K means clustering created center points that were actually incredibly dimensional

df_comp = pd.DataFrame(pca.components_,columns=cancer['feature_names'])
plt.figure(figsize=(12,6))
sns.heatmap(df_comp,cmap='plasma',) #shows the correlation between various features and the principle component (cancer) itself
#this heatmap is our attempt to trace back the 30 features into how they correlate to cancer








plt.show()

