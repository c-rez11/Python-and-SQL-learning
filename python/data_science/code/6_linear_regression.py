#6_linear_regression and logistic regression

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



USAhousing = pd.read_csv('USA_Housing.csv')
print(USAhousing.head())
print(USAhousing.info())
#sns.pairplot(USAhousing)
#sns.distplot(USAhousing['Price'])
#plt.show()

#training a linear regression model

X = USAhousing[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
               'Avg. Area Number of Bedrooms', 'Area Population']] #these are the features to train on

y = USAhousing['Price'] #this is the target variable

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,  test_size=0.4, random_state=101)

from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train,y_train)

#model evaluation
print(lm.intercept_)
coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
print(coeff_df)

#load real sample built into sklearn
from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
print(cancer.DESCR)

predictions = lm.predict(X_test)
#sns.distplot((y_test-predictions),bins=50)
#plt.show()

from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

#eCommerce project example
customers = pd.read_csv("Ecommerce Customers")
y = customers['Yearly Amount Spent']
X = customers[['Avg. Session Length', 'Time on App','Time on Website', 'Length of Membership']]

#train the model
X_train, X_test, y_train, y_test = train_test_split(X, y,  test_size=0.3, random_state=101)
lm = LinearRegression()
lm.fit(X_train,y_train)
print('Coefficints: \n', lm.coef_)

#predict test data
predictions = lm.predict(X_test)

print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

plt.scatter(y_test,predictions)
#sns.histplot((y_test-predictions),bins=50)
#plt.show()

coefficients = pd.DataFrame(lm.coef_,X.columns)
coefficients.columns = ['Coefficient']
print(coefficients)

#logistic regression - famous Titanic data set

train = pd.read_csv('titanic_train.csv')
print(train.head())

sns.heatmap(train.isnull(),yticklabels=False,cbar=False,cmap='viridis')
#plt.show()

#input missing age values based on Pclass
def impute_age(cols):
    Age = cols[0]
    Pclass = cols[1]
    
    if pd.isnull(Age):

        if Pclass == 1:
            return 37

        elif Pclass == 2:
            return 29

        else:
            return 24

    else:
        return Age
train['Age'] = train[['Age','Pclass']].apply(impute_age,axis=1)
train.drop('Cabin',axis=1,inplace=True)

#turn categorical variables into dummy variables
sex = pd.get_dummies(train['Sex'],drop_first=True)
embark = pd.get_dummies(train['Embarked'],drop_first=True)
train.drop(['Sex','Embarked','Name','Ticket'],axis=1,inplace=True)
train = pd.concat([train,sex,embark],axis=1)
print(train.head())

#train-test split
X_train, X_test, y_train, y_test = train_test_split(train.drop('Survived',axis=1), 
                                                    train['Survived'], test_size=0.30, 
                                                    random_state=101)

from sklearn.linear_model import LogisticRegression
logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)

predictions = logmodel.predict(X_test)

#model evaluation
from sklearn.metrics import classification_report
print("Titanic classification matrix")
print(classification_report(y_test,predictions))
from sklearn.metrics import confusion_matrix
print("Titanic confusion matrix")
print(confusion_matrix(y_test,predictions))
#reading the confusion matrix
#           predicted
#            0      1
#actual 0    TN     FP
#       1    FN     TP


#K nearest neighbor
#for example, if I have horse vs dog height/weight data,
#and I'm given a new height/weight combo, how do I predict whether it's a horse or dog?
#K looks at the nearest neighboring points in the training data (K=number of nearest points)
#to determine how this new point should be classified

df = pd.read_csv("Classified Data",index_col=0)

#used to standardize the data to prepare it for the KNN
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(df.drop('TARGET CLASS',axis=1))
scaled_features = scaler.transform(df.drop('TARGET CLASS',axis=1))
df_feat = pd.DataFrame(scaled_features,columns=df.columns[:-1]) #everything but last column

X_train, X_test, y_train, y_test = train_test_split(scaled_features,df['TARGET CLASS'],
                                                    test_size=0.30)


from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train,y_train)
pred = knn.predict(X_test)
print("KNN example")
print('\n')
print(confusion_matrix(y_test,pred))
print(classification_report(y_test,pred))

#elbow method: iterate over many k values to see which has the lowest error rate
error_rate = []

for i in range(1,25):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train,y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != y_test))


#plot the error rate
plt.figure(figsize=(10,6))
plt.plot(range(1,25),error_rate,color='blue', linestyle='dashed', marker='o',
         markerfacecolor='red', markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')
#plt.show()

#looks like k = 23 is our best bet. Let's see how our stats compare to k=1
knn = KNeighborsClassifier(n_neighbors=23)
knn.fit(X_train,y_train)
pred = knn.predict(X_test)
print(confusion_matrix(y_test,pred))
print(classification_report(y_test,pred))
#pretty good stats!