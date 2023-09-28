# how to identify and deal with overfitting
# Early Stopping: with Keras, we can automatically stop training based on a loss condition
    # on the validation data passed through the model.fit() call
# Dropout layer: layer that can be added to "turn off" neurons during training to prevent overfitting
    # each dropout layer will "drop" a user-defined percentage of neurons in the previous layer of each batch

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('C:/Users/User/Desktop/python/c-rez11/Udemy/python/data_science/data/cancer_classification.csv')

print(df.info()) # check for nulls
print(df.describe()) # explore statistical distribution of features

#sns.countplot(x='benign_0__mal_1',data=df) # is this data well-balanced? Are there enough of each for a good model to work?
print(df.corr()['benign_0__mal_1']) # correlation of features to cancer condition

# train / test split
X = df.drop('benign_0__mal_1', axis=1).values
y = df['benign_0__mal_1'].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=101)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
print(X_train.shape) # we only have 400 data points, but 30 variables

model = Sequential()
model.add(Dense(30,activation='relu'))
model.add(Dropout(0.5)) # 50% of the neurons will be randomly turned off
model.add(Dense(15,activation='relu'))
model.add(Dropout(0.5)) # 50% of the neurons will be randomly turned off
model.add(Dense(1,activation='sigmoid')) 
# since this is a binary classification, we use sigmoid in our last node

model.compile(loss='binary_crossentropy',optimizer='adam')

# below is the model WITHOUT early stopping. It has been commented out

#model.fit(x=X_train,y=y_train,epochs=200, validation_data=(X_test,y_test))

#losses = pd.DataFrame(model.history.history)
#losses.plot() # note that the model overfits the data, meaning we have overtrained
    # likely because we used too many epochs

from tensorflow.keras.callbacks import EarlyStopping,Tensorboard

# early stopping allows us to stop training the model when it starts to overfit
early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=25) 
# minimize validation loss, wait 25 epochs to stop

# run the model with early stop
model.fit(x=X_train,y=y_train,epochs=200, validation_data=(X_test,y_test), callbacks=[early_stop])

losses = pd.DataFrame(model.history.history)
losses.plot() 

# how well does the model do?
predictions = model.predict_classes(X_test)
from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))


plt.show()