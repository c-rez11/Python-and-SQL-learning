# Decision Trees and Random Forests

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('kyphosis.csv')
print(df.head())
print(df.describe())

sns.pairplot(df,hue='Kyphosis',palette='Set1')
#plt.show()

from sklearn.model_selection import train_test_split

X = df.drop('Kyphosis',axis=1) #this drops the dependent variable from the independent variables
y = df['Kyphosis'] #the dependent variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

#start with training a single decision tree
from sklearn.tree import DecisionTreeClassifier
dtree = DecisionTreeClassifier()
dtree.fit(X_train,y_train)

#evaluate our decision tree
predictions = dtree.predict(X_test)
from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))

from sklearn import tree
plt.figure(figsize=(15,12))
tree_pic = tree.plot_tree(dtree, filled=True, fontsize=8, feature_names=X_train.columns, class_names=['absent','present'])
#plt.show()

#now the random forest
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=100)
rfc.fit(X_train, y_train)
rfc_pred = rfc.predict(X_test)
print(confusion_matrix(y_test,rfc_pred))
print(classification_report(y_test,rfc_pred))