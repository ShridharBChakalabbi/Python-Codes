#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 12:29:08 2018
@author: nagarjun
"""

import pandas as pd
import scipy
import numpy as np
from sqlalchemy import create_engine
import sys
from sklearn.model_selection import train_test_split
from scipy.stats import mode
from datetime import timedelta
import fancyimpute as fi
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
from collections import Counter

class Data:
    def __init__(self,df,forecastMessure,m_count,m_perc,i_count,i_perc,date_column='datetime'):
        self.df = df
        self.forecastMessure = forecastMessure
        self.date_column = date_column
        self.Min,self.Avg,self.Median,self.Max,self.Sd,self.q1,self.q3 = self.df[self.forecastMessure].describe()[['min','mean','50%','max','std','25%','75%']].values
        self.Act_days = sum(self.df['actual_imputed']=="Actual")
        self.Imputed_days = sum(self.df['actual_imputed']=="Imputed")
        self.Tenure = len(self.df[self.date_column])
        self.IQR = scipy.stats.iqr(self.df[self.forecastMessure])
        self.hs = self.q3 + 1.5*self.IQR
        self.ls = self.q1 - 1.5*self.IQR
        self.hs_count = sum(self.df[self.forecastMessure] > self.hs)
        self.ls_count = sum(self.df[self.forecastMessure] < self.ls)
        self.di = {'Total_fc_msr_vals' : sum(self.df[self.forecastMessure]),
        'Min' : self.Min,'Avg' : self.Avg,'Median' : self.Median,'Max' : self.Max,'Sd' : self.Sd,
        'Tenure' : self.Tenure,
        'IQR' : self.IQR,
        'StartDate' : min(self.df[self.date_column]),
        'EndDate' : max(self.df[self.date_column]),
        'hs' : self.hs,
        'ls' : self.ls,
        'he' : self.q3 + 3*self.IQR,
        'le' : self.q1 - 3*self.IQR,
        'lower_1sigma' : self.Avg-self.Sd,
        'lower_2sigma' : self.Avg-2*self.Sd,
        'lower_3sigma' : self.Avg-3*self.Sd,
        'upperr_1sigma' : self.Avg+self.Sd,
        'upper_2sigma' : self.Avg+2*self.Sd,
        'upper_3sigma' : self.Avg+3*self.Sd,
        'hs_count' : self.hs_count,
        'ls_count' : self.ls_count,
        'no_of_outliers' : sum([self.hs_count,self.ls_count]),
        'Act_days' : self.Act_days,
        'Imputed_days' : self.Imputed_days,
        'imp_per' : (self.Imputed_days/self.Tenure)*100,
        'ForecastMeasure_Missing_count':m_count,
        'ForecastMeasure_Missing_perc':m_perc,
        'ForecastMeasure_Invalid_count':i_count,
        'ForecastMeasure_Invalid_perc':i_perc
        }

class DataPreProcessing:
    def __init__(self,data,forecastMessure,date_column,productCol):
        self.df,ic = self.data_cleaning(data,date_column,forecastMessure,productCol)
        self.df.sort_values(by=['datetime'],inplace=True)
        self.df.reset_index(drop=True,inplace=True)
        self.df = self.missing_dates_frequency_based(self.df)
        self.df,m_count,m_perc,i_count,i_perc = self.datatype_validation(self.df,ic,forecastMessure)
        if self.df.empty:
            print('The data provided is insufficient as the missing values & invalid values are more than 10% of the data')
            sys.exit()
        data = Data(df=self.df,forecastMessure=forecastMessure,m_count=m_count,m_perc=m_perc,i_count=i_count,i_perc=i_perc)
        self.DataStates = {'Standardized_data':data}
        self.outlier_dict = {'Normal_Distribution':'self.norm_dist(x,forecastMessure,sigma)','boxplot':'self.box_plt(x,forecastMessure,rng)'}
        self.impute_dict = {'single':{'KNN':'x[forecastMessure] = fi.KNN(k=3).fit_transform(x.iloc[:,i:i+1])',
                           'NuclearNormMinimization':'x[forecastMessure] = fi.NuclearNormMinimization().fit_transform(x.iloc[:,i:i+1])',
                           'SoftImpute':'x[forecastMessure] = fi.SoftImpute().fit_transform(x.iloc[:,i:i+1])',
                           'MatrixFactorization':'x[forecastMessure] = fi.MatrixFactorization().fit_transform(x.iloc[:,i:i+1])',
                           'mean':"x[forecastMessure].fillna(eval('x[forecastMessure].mean()'), inplace=True)",
                           'median':"x[forecastMessure].fillna(eval('x[forecastMessure].median()'), inplace=True)",
                           'mode':"x[forecastMessure].fillna(eval('x[forecastMessure].mode()[0]'), inplace=True)"},
            'multiple':{'IterativeImputer':'x = fi.IterativeImputer().fit_transform(x)',
                              'IterativeSVD':'x = fi.IterativeSVD().fit_transform(x)',
                              'KNN':'x = fi.KNN(k=3).fit_transform(x)',
                              'NuclearNormMinimization':'x = fi.NuclearNormMinimization().fit_transform(x)',
                              'SoftImpute':'x = fi.SoftImpute().fit_transform(x)',
                              'MatrixFactorization':'x = fi.MatrixFactorization().fit_transform(x)'}}
    
    def norm_dist(self,x,forecastMessure,sigma):
        m ,sd = x[forecastMessure].describe()[['mean','std']].values
        m=m
        sd=sd
        return [m - sigma * sd , m + sigma * sd]

    def box_plt(self,x,forecastMessure,rng):
        h = rng*scipy.stats.iqr(x[forecastMessure])
        q1,q3 = x[forecastMessure].describe()[['25%','75%']].values
        return [q1-h,q3+h]
    
    def outlier_treatment(self,x,forecastMessure,outlier_type="Normal_Distribution",sigma=2,rng=1.5):        
        
        '''Attributes
        x = dataframe
        forecastMessure = the column name of forecast varible
        outlier_type = The type of outlier treatment method to be used. Available methods are 'Normal_Distribution','boxplot'
        sigma = the sigma value for the Normal Distribution outlier treatment
        rng = the range value for the boxplot outlier tdate_column="datetime"reatment
        Returns the outlier treated dataframe'''
        
        #outlier_dict=norm_dist(x,forecastMessure,sigma)   
        quantiles =eval(self.outlier_dict[outlier_type])
        x.loc[x[forecastMessure]<quantiles[0] ,forecastMessure] = quantiles[0]
        x.loc[x[forecastMessure]>quantiles[1] ,forecastMessure] = quantiles[1]
        return x
    
    def imputation(self,data,forecastMessure,impute_type=None,n_vars='single',outlier_type=''):
        
        ''' Attributes
        x = dataframe
        forecastMessure = the column name of forecast varible
        impute_type = the imputation method to be used. Available methods are KNN,NuclearNormMinimization,
        SoftImpute,MatrixFactorization,IterativeImputer,IterativeSVD,Mean,Median,Mode. Default is 'Mode'
        n_vars = 'Multiple' If the data contains multiple independent variables, default is 'Single'
        '''
        
        data['actual_imputed'] = np.where(data[forecastMessure].isnull(),'Imputed',data['actual_imputed'])
        i=data.columns.get_loc(forecastMessure)
        if pd.isnull(impute_type):
            for j in self.impute_dict[n_vars].keys():
                x = data.copy()
                try:
                    exec(self.impute_dict[n_vars][j])
                    self.DataStates[outlier_type+'_'+j] = Data(x,forecastMessure,0,0,0,0)
                except:
                    pass
        else:
            x = data.copy()
            exec(self.impute_dict[n_vars][impute_type])
            self.DataStates[outlier_type+'_'+impute_type] = Data(x,forecastMessure,0,0,0,0)

        #data=data.fillna(eval("data"+'["'+forecastMessure+'"].'+impute_type+"()"))
        #x.fillna(eval('x[forecastMessure].mean()'), inplace=False)
        #x.loc[x[forecastMessure].isnull(),forecastMessure] = eval("x[forecastMessure]."+impute_type+"()")
        # h = fi.BiScaler().fit_transform(df.iloc[:,0:1]) # getting error
            
    def data_cleaning(self,data,dateCol,forecastMessure,productCol):
        data.rename(columns={productCol:'item_name',dateCol:'datetime'},inplace=True)
        #data.columns = data.columns.str.lower()
        data['datetime'] = pd.to_datetime(data['datetime'],infer_datetime_format=True)
        data['item_name'] = data['item_name'].astype(str)
        data['item_name'] = data['item_name'].str.replace(r'[^A-Za-z0-9]+', '')
        data = data.dropna(subset=['item_name','datetime'], how='any')
        data["actual_imputed"] = "Actual"
        
        if data[forecastMessure].dtype not in [float,int]:
            m_count = data[forecastMessure].isnull().sum()
            data[forecastMessure] = data[forecastMessure].astype(str)
            data[forecastMessure] = data[forecastMessure].apply(lambda x: np.where(pd.isnull(x),x,self.tryconvert(x)))
            data[forecastMessure] = data[forecastMessure].astype(float)
            i_count = data[forecastMessure].isnull().sum() - m_count        
            return data,i_count
        
        else:
            return data,0
            
    def missing_dates_all(self,data,date_column="datetime",frequency=SECONDLY,days=(MO,TU,WE,TH,FR,SA,SU)):
        
        '''Attributes
        data = Dataframe
        date_column = Name of the column containing date time
        frequency = The frequency of the Datetime
        Returns a dataframe which also contains the missing dates'''
    
        dates = list(rrule(frequency, dtstart=min(data[date_column]),until=max(data[date_column]),byweekday=days))
        idx = pd.DataFrame({"datetime":dates})
        #idx = date_format(idx,"datetime")
        s1 = pd.merge(idx, data, how='outer', on=[date_column])
        s1["item_name"] = mode(data.item_name)[0][0]
        return s1
    
    def findFrequency(self,data,dateColName='datetime'):
        
        '''Attributes
        x = Dataframe
        dateColName = Name of the column containing date & time
        Returns the Frequency'''
    
        f = mode(data[dateColName].diff().astype('timedelta64[s]')).mode[0]
        return np.where(f/60>=1.0,
                        np.where(f/3600>=1.0,
                        np.where(f/86400>=1.0,
                        np.where(f/604800>=1.0,
                        np.where(f/2419200>=1.0,
                        np.where(f/7257600>=1.0,
                        np.where(f/29030400>=1.0,YEARLY,'quarter'),MONTHLY),WEEKLY),DAILY),HOURLY),MINUTELY),SECONDLY)
    
    def missing_dates_frequency_based(self,data,date_column="datetime",missing_perc_threshold=80.0):
        freq = int(self.findFrequency(data))
        d = self.missing_dates_all(data,frequency=freq)
        if freq == DAILY:
            j = set(d[date_column]) - set(data[date_column])
            j = Counter(list(map((lambda x: x.weekday()),j)))
            k = Counter(list(map((lambda x: x.weekday()),data[date_column])))
            n = k.most_common(1)[0][1]
            x = []
            for i in j.most_common():
                if i[1]/n*100 > missing_perc_threshold:
                    x.append(i[0])
            wdays = set([0,1,2,3,4,5,6]) - set(x)
            return self.missing_dates_all(data,frequency=freq,days=wdays,date_column=date_column)
        else:
            return d
    
    def tryconvert(self,x):
        try:
            float(x)
            return x
        except:
            return None
        
    def datatype_validation(self,data,i_count,forecastMessure,missing_perc_threshold=10.0):
        count = len(data[forecastMessure])
        m_count = data[forecastMessure].isnull().sum() - i_count
        if ((m_count + i_count)/count)*100 > missing_perc_threshold:
            return pd.DataFrame(),m_count,(m_count/count)*100,i_count,(i_count/count)*100
        else:
            return data,m_count,(m_count/count)*100,i_count,(i_count/count)*100