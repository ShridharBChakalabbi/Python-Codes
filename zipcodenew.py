# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:17:00 2018

@author: Sridhar
"""

import os
import pandas as pd 
import numpy as np
import pymysql.cursors
import re
import datetime
from datetime import date, timedelta
from uszipcode import ZipcodeSearchEngine
import csv

connection = pymysql.connect(host='54.70.109.246',user='mobiloans',password='ambertagmobiloans',db='mobiloans_pii',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

mobilaons_pii =pd.read_sql("select AES_DECRYPT(FirstName,123654), AES_DECRYPT(LastName,123654),AES_DECRYPT(State,123654),AES_DECRYPT(PostalCode,123654),AES_DECRYPT(HomePhone,123654),AES_DECRYPT(CellPhone,123654),AES_DECRYPT(WorkPhone,123654),AES_DECRYPT(City,123654) from mbl_may_customer_pii",connection)
mobiloanspii = mobilaons_pii
mobiloanspii2 = mobiloanspii.astype(str).replace('b','',regex=True)
#mobiloanspii2 = mobiloanspii.astype(str).replace('', '',regex = True)

for i, col in enumerate(mobiloanspii2.columns): 
        mobiloanspii2.iloc[:, i] = mobiloanspii2.iloc[:, i].str.replace(r"[\"\',]", '')
        
        
mobiloanspii2.info()        

CODE=pd.read_csv("C:Users/Sridhar/Downloads/us_postal_codes.csv") 
code1=pd.DataFrame(CODE)    
code1.columns=['Zipcode'] 
censusData = mobiloanspii2[['AES_DECRYPT(FirstName,123654)','AES_DECRYPT(LastName,123654)','AES_DECRYPT(PostalCode,123654)','AES_DECRYPT(State,123654)','AES_DECRYPT(City,123654)']]
censusData.loc[:,'Name'] = censusData['AES_DECRYPT(FirstName,123654)']+' '+censusData['AES_DECRYPT(LastName,123654)']

#from uszipcode import ZipcodeSearchEngine
censusData.rename(columns={'AES_DECRYPT(PostalCode,123654)':'zipcode'},inplace=True)

z2=[]
for i in range(0,len(code1)):
    try:
        search = ZipcodeSearchEngine()
        zipcode = search.by_zipcode(code1.Zipcode[i])
        #z1=[[zipcode.City,zipcode.Density,zipcode.HouseOfUnits,zipcode.Wealthy,zipcode.TotalWages,zipcode.WaterArea,zipcode.LandArea,zipcode.Latitude,zipcode.Longitude,zipcode.Population,zipcode.State,zipcode.ZipcodeType,zipcode.Zipcode]]
        z1=[[zipcode.City,zipcode.Density,zipcode.HouseOfUnits,zipcode.LandArea,zipcode.Latitude,zipcode.Longitude,zipcode.NEBoundLatitude,zipcode.NEBoundLongitude,zipcode.Population,zipcode.SWBoundLatitude,zipcode.SWBoungLongitude,zipcode.State,zipcode.TotalWages,zipcode.WaterArea,zipcode.Wealthy,zipcode.Zipcode,zipcode.ZipcodeType]]
        z2.append(z1)
    except Exception as e:
            print(str(e))
    print(i)
 
Z2=pd.DataFrame(z2)
Z2.to_csv('overallgeo.csv')
os.getcwd()    
Z2.columns=['Geo-Info']

overallgeo=pd.read_csv("C:/Users/Sridhar/Desktop/overallgeo.csv")
code1.rename(columns={'Zip Code':'Zipcode'},inplace=True)
merged=pd.merge(mobiloanspii2,overallgeo,how='left', on=['Zipcode'])
merged.to_csv('overallgeo_may.csv')
os.getcwd()    
