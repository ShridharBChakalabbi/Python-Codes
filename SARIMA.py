#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:36:41 2018

@author: shridhar
"""

# SARIMA example

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from math import sqrt
# contrived dataset
data = pd.read_csv("/media/shridhar/9ED2FF76D2FF514F/Vehicle_insurance/buckets_claims/CountOfClaimsSample1&Sample2.csv")
data.set_index('Date',inplace=True)
X = data.values
size = int(len(X) *.91)
train, test = X[0:size], X[size:size+10]
# fit model
model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
model_fit = model.fit(disp=False)
# make prediction
predictions =model_fit.predict(start=len(train), end=len(train)+len(test)-1)
for i in range(len(predictions)):
	print('predicted=%f, expected=%f' % (predictions[i], test[i]))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot results

rmse=sqrt(error)
rmse_accuracy=(100-error)
print (rmse)
print(rmse_accuracy)