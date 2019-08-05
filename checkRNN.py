# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 10:46:15 2018

@author: Chandan
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 15:21:39 2018

@author: Chandan
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
os.chdir(r"C:\Users\Chandan\Desktop\Solar\12Aug_21NovCodes")

# Importing the dataset
dataset = pd.read_csv('workbenchPower.csv')
X = dataset.iloc[:, :30].values
y = dataset.iloc[:, 30].values


# Creating a data structure with considerLast timesteps and 1 output
X_train = []
y_train = []
for i in range(considerLast, len(training_set_scaled)):
    X_train.append(training_set_scaled[i-considerLast:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))


X_test = []
y_test = []
for i in range(considerLast, len(testing_set_scaled)):
    X_test.append(testing_set_scaled[i-considerLast:i, 0])
    y_test.append(testing_set_scaled[i, 0])
X_test, y_test = np.array(X_test), np.array(y_test)

X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 512, kernel_initializer = 'uniform', activation = 'relu', input_dim = 30))
classifier.add(Dense(units = 256, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(units = 256, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(units = 128, kernel_initializer = 'uniform', activation = 'relu'))

classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'relu'))
classifier.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(X_train, y_train, batch_size = 10, epochs =100)

# Part 3 - Making predictions and evaluating the model

# Predicting the Test set results
y_pred = classifier.predict(X_test)


from sklearn.metrics import r2_score

print(r2_score(y_test,y_pred))






