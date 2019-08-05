#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 23:59:15 2018

@author: nagarjun
"""

from oops import Data,DataPreProcessing
from RNN import RNN
import pandas as pd

df = pd.read_csv('CCD_new_data.csv')
data=df[df['ITEM_ID']=='A339'] # Pass dataframe containing data here
forecastMeasure='qty' # Pass the name of the forecast measure column
date_column='Date' # Pass the name of the date column
productCol='ITEM_ID' # Pass the name of the product column
n_lag = 3
n_preds = 3
nvars = 1

dpp = DataPreProcessing(data.copy(),forecastMeasure,date_column,productCol)

m_count = dpp.DataStates['Standardized_data'].di['ForecastMeasure_Missing_count']
m_perc = dpp.DataStates['Standardized_data'].di['ForecastMeasure_Missing_perc']
i_count = dpp.DataStates['Standardized_data'].di['ForecastMeasure_Invalid_count']
i_perc = dpp.DataStates['Standardized_data'].di['ForecastMeasure_Invalid_perc']
for i in dpp.outlier_dict.keys():
    dpp.DataStates[i] = Data(dpp.outlier_treatment(dpp.DataStates['Standardized_data'].df,forecastMeasure,outlier_type=i),forecastMeasure,m_count,m_perc,i_count,i_perc)
    dpp.imputation(dpp.DataStates[i].df,forecastMeasure,outlier_type=i)
    
l = set(dpp.DataStates.keys()) - set(['Standardized_data','Normal_Distribution','boxplot'])

d = {'Dataset':[],'Predictions':[]}
for i in range(n_preds):
    d['t+'+str(i+1)+' RMSE'] = list()

for i in l:
    rnn = RNN(dpp.DataStates[i].df.copy(),forecastMeasure,n_lag,n_preds,nvars)
    x, y, scaler = rnn.prepare_data(dpp.DataStates[i].df.copy())
    x_train,x_test = rnn.train_test_split(x,test_size=0.3)
    y_train,y_test = rnn.train_test_split(y,test_size=0.3)
    model = rnn.fit([10,10],x_train, y_train)
    forecasts = rnn.forecast(model, x_test)
    forecasts = rnn.inverse_transform(forecasts, scaler)
    actual = rnn.inverse_transform(y_test.values, scaler)
    rmse = rnn.evaluate_forecasts(y_test.values, forecasts)
    d['Dataset'].append(i)
    for i in range(n_preds):
        d['t+'+str(i+1)+' RMSE'].append(rmse[i])
    d['Predictions'].append(forecasts)
    
fdf = pd.DataFrame(d)
n = fdf[fdf['t+1 RMSE']==min(fdf['t+1 RMSE'])]['Dataset'].item()
rnn = RNN(dpp.DataStates[n].df.copy(),forecastMeasure,n_lag,n_preds,nvars)
x, y, scaler = rnn.prepare_data(dpp.DataStates[n].df.copy())
x_train,x_test = rnn.train_test_split(x,test_size=0.7)
y_train,y_test = rnn.train_test_split(y,test_size=0.7)
k = list(x_test.iloc[-1,:]) + list(y_test.iloc[-1,:])
model = rnn.fit([10,10],x_test, y_test)
forecasts = rnn.forecast(model, k[-n_lag:])
forecasts = rnn.inverse_transform(forecasts, scaler)[0].tolist()
