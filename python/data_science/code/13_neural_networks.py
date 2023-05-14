# Neural networks and deep learning

# consider the perceptron model of a neuron: a number of inputs feed the nucleus, which determines the output
# this is similar to a simple linear regression where B1x1 + B2x2 = y
# However, a linear regression doesn't learn or dynamically change based on new info.
    # essentially, we need adjustable Betas 
# if x=0, we don't want to lose the adjustable Beta, so we add a 'bias' term
# essentially, instead of B1x1, we get (B1x1+bias)

# Neural network -- a multi-layer neuron model
# each neuron's OUTPUT becomes the INPUT for the next layer of neuron
# this continues to build the multiple layers
# hidden layers -- the layers between the known inputs (first layer) and known output (last layer)
# a neural network becomes a DEEP neural network when it contains 2+ hidden layers

# in classification tasks, it's useful to have all inputs between 0 and 1 so we know the upper/lower limits of our output
# we'll use activation functions to set boundaries to output values from the neuron

# Activation Functions
# we'll refer to them as f(z) where z = Bx+bias
# making your output 0 or 1 doesn't adjust well to small changes in the data or the weights
# we much prefer a range along 0 to 1 so that adjustments have their intended effect
# to do this, we use the sigmoid function: f(z) = 1 / (1+e^(-z)) to get a smooth distribution
# other common functions: hyperbolic tangent tanh(z) = sinh(z) / cosh(z) with output between -1 and 1
# another common one: rectified linear unit (ReLU): if z<0, return 0, otherwise return z
#   ReLU are known for good performance


# Multi-class classifications
# non-exclusive classes: photos can have multiple tags (e.g. photos can have tags of beach, family, vacation)
# mutually exclusive classes: one class to a data point (e.g. black-and-white or color)
# to deal with mutually-exclusive classes, we create dummy variables (similar to what we do with categorical variables in regression models)
# we actually do the same thing with non-exclusive classes...it'll now be possible to have '1' values in multiple categories

# when each data point can only have a single class assigned to it, we use the softmax function
# softmax function: calculates the probabilities distribution of the event over K different events
#   it calculates the probability of each target class over all possible target classes
#   The sum of all probabilities will be equal to 1. Target class is chosen as the highest probability

# Cost Functions and Gradient Descent
# So after a network creates its prediction, how do we evaluate it? How do we update the weights?
# We need to compare the estimated outputs with the real values--keep in mind this is still the training data set
# We'll create a cost function (aka loss function) to reduce our model 'cost' until it converges to the lowest cost possible
# a = neuron's predicted value
# y = true value
# remember: B1*x + bias  = z
# f(z) = a
# most common cost function: quadratic cost function (essentially root mean squared error for multi-dimensional data)
# for classification, we often use the 'cross entropy' loss function
#   which predicts a probability distribution for each class
# cost function is essentially C(W,B,Sr,Er), where:
# w = weight
# b = bias
# Sr = input of a single training sample
# Er = desired output of that training sample
# To find the correct weight, we minimize a cost function--sound familiar??
# The problem with taking the derivative and setting equal to zero 
#     is that we'll have a massive, ever-changing cost function matrix, so it would take forever

# Concept of step size: 
# Imagine you're finding the slope of a point on a curve, and you do that in both directions until you find slope = 0
# You go up and down the line in 'steps'...for example, you might do a step for each tick mark on the horizontal axis
#   too many steps, and your model will be precise, but sacrifice speed
#   too few steps, and your model will be fast, but could struggle with accurately finding slope = 0
# in ML, the step size is called the 'learning rate'

# But hold on: we can have a dynamic step size and adapt it as the gradient gets closer to zero.
#   This is called adaptive gradient descent; the most famous one according to Udemy is the 'Adam' optimizer
#   When dealing with these n-dimensional vectors (tensors), the notation changes from derivative to gradient.

# Backpropagation - going backwards through the neural network to update weights and biases
# notation: the very last layer of the network = L. Second-to-last is L-1, then L-2, etc
# z(L) = w(L)*a(L-1)+ bias(L)
#   a(L-1) is the output of the previous layers' neuron
# a(L) = f(z(L))
# C (cost function) = (a(L)-y)^2

# how sensitive is the cost function to changes in weight (w)?
#   dC / d(w(L)) take the partial derivative to get dz/dw * da/dz * dC/da
# same with the bias term -- how does the bias term change with respect to bias?
#   dC / d(b(L)) partial derivative = dz/db * da/dz * dC/da

# reminder: our initial neuron is z = wx + b (x are the inputs)
#   We then apply an activation function to z to produce a result called 'a'
#   notation: f(z) = a
# 'a' then feeds our next layer the same way our initial x's fed the first layer

# Because we have this formula z(L) = w(L)*a(L-1)+ bias(L), 
#   we see that the a(L-1) will feed the previous layer, and will continue to allow us to adjust by layer

# TensorFlow: deep learning open-source library developed by Google
#   TensorFlow had such a complex python class system for building models
#       that Keras, a TensorFlow API, became widely popular

import pandas as pd
import numpy as np
import seaborn as sns

df = pd.read_csv('fake_reg.csv') # gemstones, their features, and the historical price data
print(df.head())

from sklearn.model_selection import train_test_split
X = df[['feature1','feature2']].values # because of the way TensorFlow works, we have to pass in numpy arrays instead of pandas series
#   Adding .values returns the series as a numpy array
y = df['price'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler() # creates an instance of a scaler.
scaler.fit(X_train) # need to fit the scaler onto the training data. This calculates the parameters needed to scale later on.
#   It's dependent on the min, max, and std dev of the training data
#   We only fit to the training data because fitting to the test data would be cheating (data leakage)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
print(X_train)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# two ways to create a keras-based model. First way: pass in a list of the layers you want
model = Sequential([Dense(4, activation='relu'),
                    Dense(2, activation='relu'),
                    Dense(1, activation='relu')]) # Dense layer: Every neuron in layer X is connected to every neuron in layer X+1
# units = neurons. How many neurons will be in the layer? Here, we say 4 neurons in layer one, 2 in layer 2, and 1 final output
# activation = what activation function should be used? Sigmoid? etc

# preferred method of building model: create empty sequential model and add each layer one at a time
model = Sequential()

# easier to edit or turn off a layer this way
model.add(Dense(4, activation = 'relu'))
model.add(Dense(4, activation = 'relu'))
model.add(Dense(4, activation = 'relu'))
model.add(Dense(1)) # final output will try to predict the price

model.compile(optimizer = 'rmsprop', loss='mse') # mse because our output is a continuous value
# optimizer: what method do you want to optimize with
# loss parameter: depends on what you're trying to do
#   multi-class classification problem: choose 'categorical_crossentropy'
#   binary classification: choose 'binary_crossentropy'
#   for mean squared error regression: choose 'mse'

model.fit(x=X_train,y=y_train,epochs=250, verbose=0) # remove verbose to see the loss decrease
# x = the features that we're training on
# y = the training labels that correspond to the feature points
# epochs = arbitrary cutoff defined as one pass over the entire dataset

loss_df = pd.DataFrame(model.history.history)
import matplotlib.pyplot as plt

#plt.plot(loss_df) # you can see how the loss decreases as the model improves


# let's take this to the test data!
print('start')
print(model.evaluate(X_test,y_test, verbose=0)) # returns mean squared error of 24.97 on data it has NEVER SEEN BEFORE
print('end')
model.evaluate(X_train,y_train, verbose=0) # could do the same for training data. It is 24.1 here.

test_predictions = model.predict(X_test) # predict diamond price based on the two features using our ML algorithm
print(test_predictions)

test_predictions = pd.Series(test_predictions.reshape(300,)) # turn the numpy array back to a pandas series to more easily manipulate it
pred_df = pd.DataFrame(y_test,columns=['Test True Y'])
pred_df = pd.concat([pred_df,test_predictions],axis=1)
pred_df.columns = ['Test True Y', 'Model Predictions']
print(pred_df)
sns.scatterplot(x='Test True Y', y='Model Predictions', data=pred_df)

from sklearn.metrics import mean_absolute_error, mean_squared_error
print(mean_absolute_error(pred_df['Test True Y'],pred_df['Model Predictions'])) # on average, we're about $4 off on our predictions. Not bad for diamonds around $500.

# what if we feed it new data?
new_gem = [[998,1000]]
# first, scale the data
new_gem = scaler.transform(new_gem)
print('the prediction is below')
print(model.predict(new_gem))

# save our model
from tensorflow.keras.models import load_model
model.save('my_gem_model.h5')
# later on, we can load the model


later_model = load_model('my_gem_model.h5')
print(later_model.predict(new_gem))

#plt.show()