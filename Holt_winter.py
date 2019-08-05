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
from datetime import datetime,timedelta
from pandas.io import sql
from sqlalchemy import create_engine
from math import sqrt # this for get current datetime
from pyramid.arima import auto_arima
import dataPreparation
from itertools import product
from modelling import Modelling


def expand_grid(dictionary):
   return pd.DataFrame([row for row in product(*dictionary.values())], 
                       columns=dictionary.keys())


class Holtwinter(Modelling):
    def __init__(self,data,forecastMessure,seasonal_periods,WStRMSEOpt,WMAPEOpt,product):
        Modelling.__init__(self,data,forecastMessure)
        self.data=data
        self.forecastMessure=forecastMessure
        self.seasonal_periods=seasonal_periods
        self.WStRMSEOpt=WStRMSEOpt
        self.WMAPEOpt=WMAPEOpt
        self.product=product
    
    def grid(self,trend):
        self.dictionary = {'trend':['add'], 
              'seasonal': ['add', 'mul', 'additive', 'multiplicative'],'damped':['True','False'],'seasonal_periods':'12'} 
        self.data_treat_comb=expand_grid(self.dictionary)
        return self.data_treat_comb

    
    def fit(self,train,trend,seasonal):
        self.fit1 = ExponentialSmoothing(np.asarray(train[[self.forecastMessure]]) ,seasonal_periods=self.seasonal_periods,trend=trend,seasonal=seasonal).fit(use_boxcox=True)
        return self.fit1

    def forecast(self,forecastdays=10):
        pred=self.fit1.forecast(forecastdays)
        return pred