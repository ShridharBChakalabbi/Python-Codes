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
from modelling import Modelling


class SARIMAX_Modelling(Modelling):
    
    def __init__(self,data,forecastMessure,p,d,q):
        Modelling.__init__(self,data,forecastMessure)
        self.data=data
        self.p=p
        self.d=d
        self.q=q
        self.forecastMessure=forecastMessure
        
   
    def  fit_best_pdq(self,ytrain,p,d,q,forecastMessure):
        # Generate all different combinations of p, q and q triplets
        self.ytrain=ytrain
        pdq = list(itertools.product(self.p, self.d, self.q))
                
        # Generate all different combinations of seasonal p, q and q triplets
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(self.p, self.d, self.q))]
        aic = []
        params= []
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                    mod = sm.tsa.statespace.SARIMAX(self.ytrain[self.forecastMessure],
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)
                #model=mod.fit()
                    results = mod.fit()
                    aic.append(results.aic)
                    params.append([param,param_seasonal])
                
                        
        index = np.where(aic ==np.min(aic))[0][0]    
        bestParams = params[index]   
        self.bestpdq = bestParams[0]
        self.best_paramsea = bestParams[1]
        return self.bestpdq,self.best_paramsea
        
    def  fit(self,bestpdq,best_paramsea,forecastMessure):
        model = sm.tsa.statespace.SARIMAX(self.ytrain[self.forecastMessure],
                                        order= bestpdq,
                                        seasonal_order=best_paramsea ,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        self.model_result=model.fit()
      
     
    def forecast(self,forecastday):
        self.pred=self.model_result.forecast(forecastday)
        return self.pred












