from numpy import mean
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
import statsmodels.api as sm
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error
from pandasql import sqldf
import pickle #For saving Model
from datetime import datetime,timedelta
from pandas.io import sql
from sqlalchemy import create_engine
from math import sqrt 
from pyramid.arima import auto_arima
import dataPreparation
from modelling import Modelling

class SMA_Model(Modelling):

    def __init__(self,data,forecastMessure,smaPeriod,seasonal_periods,WStRMSEOpt,WMAPEOpt,product):
        Modelling.__init__(self,data,forecastMessure)
        self.data=data
        self.forecastMessure = forecastMessure
        self.smaPeriod=smaPeriod
        self.seasonal_periods=seasonal_periods
        self.WStRMSEOpt=WStRMSEOpt
        self.WMAPEOpt=WMAPEOpt
        self.product=product
        
        
    def fit(self,data,forecastMessure,model_type,smaPeriod):
        self.data=data
        self.X=data[forecastMessure]
        self.j = next(i for i, x in enumerate(self.X) if x is not None)
        self.our_range = range(len(self.X))[self.j + self.smaPeriod - 1:]
        self.empty_list = [None] * (self.j + self.smaPeriod - 1)
        self.sub_result = [np.mean(self.X[i - self.smaPeriod + 1: i + 1]) for i in self.our_range]
        self.pre=np.array(self.empty_list + self.sub_result)
        return self.pre
        
    
    def data_for_forecast(self,forecastMessure):
        self.data["Forecast"]=pd.DataFrame(self.pre)
        return self.data
        
    def forecast(self,forecastday):
        self.forecastday=forecastday
        self.tes= self.data["Forecast"]
        self.predictions1=list()
        self.his=pd.DataFrame([])
        for i in range(self.forecastday):
            if len(self.his)>1:
                self.his=self.his 
            if len(self.his)==0: 
                self.his=self.tes
            self.yhat1=mean(self.his[len(self.his)-self.forecastday:len(self.his)])
            self.obs1=self.tes[i+self.smaPeriod]
            self.predictions1.append(self.yhat1)
            self.p=pd.DataFrame([self.predictions1[i]])
            self.his=pd.concat([self.his,self.p])
            
        return self.predictions1       
