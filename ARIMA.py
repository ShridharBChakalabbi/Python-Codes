import os
import pandas as pd
import numpy as np
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt 
import statsmodels.tsa.statespace.sarimax
import statsmodels.api as sm
from sklearn.metrics import accuracy_score
#from sklearn.utils import check_array
from sklearn.metrics import mean_absolute_error
from pandasql import sqldf
import pickle #For saving Model
from datetime import datetime 

from pandas.io import sql
from sqlalchemy import create_engine
from datetime import datetime # this for get current datetime
#import Nueral_Network
from pyramid.arima import auto_arima
from statsmodels.tsa.arima_model import ARIMA
import itertools as it
import dataPreparation
from modeling import Modelling

 

class ARIMA_Modelling(Modelling):


    def __init__(self,data,pdq,trend,solver,forecastMessure):
        Modelling.__init__(self, data,forecastMessure)
        self.data=data
        self.pdq = pdq
        self.trend=trend
        self.solver=solver
        self.forecastMessure=forecastMessure
         
       
    def fit(self,y_train,y_test):
         self.y_train=y_train
         self.y_test=y_test
         self.mod = ARIMA(y_train, order=self.pdq)
         self.model_fit = self.mod.fit(disp=False,trend=self.trend,solver=self.solver)
         return self.model_fit
     
    def predict(self,model_fit):
         self.pred= model_fit.predict(start=max(self.y_train.index),end=max(self.y_test.index),dynamic=False)[1:]
         return self.pred 
        
    def forecast(self,forecastday):
        self.fore=self.model_fit.forecast(forecastday)
        return self.fore
