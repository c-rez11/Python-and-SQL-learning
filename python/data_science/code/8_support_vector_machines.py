#support vector machines
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
print(cancer.keys())
#print(cancer['DESCR'])

# We have 30 predictive attributes and 569 data points.
#we have "target" data that shows whether a tumor is malignant or benign

df_feat = pd.DataFrame(cancer['data'],columns=cancer['feature_names'])
#print(df_feat.info())
df_target = pd.DataFrame(cancer['target'],columns=['Cancer'])
print(df_target.head())

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df_feat, np.ravel(df_target), test_size=0.30, random_state=101)

#train the support vector classifier
from sklearn.svm import SVC
model = SVC()
model.fit(X_train,y_train)

predictions = model.predict(X_test)
from sklearn.metrics import classification_report,confusion_matrix
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
#these results show that our model is classifying all of our data into a single class. We need to adjust parameters

#use Gridsearch to help us find the right parameters
param_grid = {'C': [0.1,1, 10, 100, 1000], 'gamma': [1,0.1,0.01,0.001,0.0001], 'kernel': ['rbf']}
from sklearn.model_selection import GridSearchCV
grid = GridSearchCV(SVC(),param_grid,refit=True,verbose=3)

grid.fit(X_train,y_train)
print(grid.best_params_)
print(grid.best_estimator_)

#re-run predictions with these new estimators
grid_predictions = grid.predict(X_test)
print(confusion_matrix(y_test,grid_predictions))
print(classification_report(y_test,grid_predictions))