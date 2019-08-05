#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 12:38:57 2019

@author: shridhar
"""

import os
import pandas as pd 
os.chdir('/home/shridhar/Desktop/CSV/botree_nestle data/csv files')

salesinvoice=pd.read_csv('SalesInvoice.csv')
SalesInvoiceHdAmount=pd.read_csv('SalesInvoiceHdAmount.csv')
SalesInvoiceLineAmount=pd.read_csv('SalesInvoiceLineAmount.csv')
#SalesInvoiceMarketReturn=pd.read_csv('SalesInvoiceMarketReturn.csv')
SalesInvoiceProduct=pd.read_csv('SalesInvoiceProduct.csv',encoding='latin1')
SalesInvoiceProductTax=pd.read_csv('SalesInvoiceProductTax.csv')
#SalesInvoiceQPSCumulative=pd.read_csv('SalesInvoiceQPSCumulative.csv')
#SalesInvoiceQPSRedeemed=pd.read_csv('SalesInvoiceQPSRedeemed.csv')
SalesInvoiceSchemeDtBilled=pd.read_csv('SalesInvoiceSchemeDtBilled.csv')
SalesInvoiceSchemeDtFreePrd=pd.read_csv('SalesInvoiceSchemeDtFreePrd.csv')
#SalesInvoiceSchemeDtPoints=pd.read_csv('SalesInvoiceSchemeDtPoints.csv')
#SalesInvoiceSchemeFlexiDt=pd.read_csv('SalesInvoiceSchemeFlexiDt.csv')
SalesInvoiceSchemeHd=pd.read_csv('SalesInvoiceSchemeHd.csv')
SalesInvoiceSchemeLineWise=pd.read_csv('SalesInvoiceSchemeLineWise.csv')
#SalesInvoiceSchemeQPSGiven=pd.read_csv('SalesInvoiceSchemeQPSGiven.csv')
Salesman=pd.read_csv('Salesman.csv')
SalesmanMarket=pd.read_csv('SalesmanMarket.csv')
SalesReturn=pd.read_csv('SalesReturn.csv')

salesinvoice.dtypes
SalesInvoiceHdAmount.dtypes
SalesInvoiceLineAmount.dtypes
SalesInvoiceProduct.dtypes
SalesInvoiceProductTax.dtypes
SalesInvoiceSchemeDtBilled.dtypes
SalesInvoiceSchemeDtFreePrd.dtypes
SalesInvoiceSchemeHd.dtypes
#SalesInvoiceSchemeLineWise.dtypes
#Salesman.dtypes
#SalesmanMarket.dtypes
#SalesReturn.dtypes

#sales1=pd.merge(salesinvoice,SalesInvoiceHdAmount,on='SalId')
#sales2=pd.merge(SalesInvoiceLine Amount,SalesInvoiceProduct,on='SalId')

sales1 = pd.concat([SalesInvoiceHdAmount,SalesInvoiceLineAmount], axis=0, join='outer', ignore_index=False)
sales2= pd.concat([SalesInvoiceProduct,SalesInvoiceProductTax],axis=0,join='outer',ignore_index=False)
sales3= pd.concat([SalesInvoiceSchemeDtBilled,SalesInvoiceSchemeDtFreePrd],axis=0,join='outer',ignore_index=False)
sales4= pd.concat([SalesInvoiceSchemeHd,SalesInvoiceSchemeLineWise],axis=0,join='outer',ignore_index=False)
sales5= pd.concat([Salesman, SalesmanMarket], axis=0, join='outer', ignore_index=False)
sales6= pd.concat([salesinvoice,SalesReturn],axis=0,join='outer',ignore_index=False)
mainsales1= pd.concat([sales1,sales2], axis=0, join='outer', ignore_index=False)
mainsales2= pd.concat([sales3,sales4], axis=0, join='outer', ignore_index=False)
#mainsales= pd.concat([sales1,sales2], axis=0, join='outer', ignore_index=False)
#mainsales2= pd.concat([sales3,sales4], axis=0, join='outer', ignore_index=False)
mainsales3= pd.concat([sales5,sales6], axis=0, join='outer', ignore_index=False)
MS1=pd.concat([mainsales1,mainsales2], axis=0, join='inner', ignore_index=False)
MS1=pd.concat([mainsales1,mainsales2],axis=0,join='outer',ignore_index=False)
MS2=pd.concat([mainsales2,mainsales3], axis=0, join='outer', ignore_index=False)
MS1=pd.concat([mainsales1,MS2],axis=0,join='outer',ignore_index=False)
MS2=pd.concat([mainsales2,mainsales3], axis=0, join='outer', ignore_index=False)




import glob
path = "/media/shridhar/9ED2FF76D2FF514F/What_If_Analysis/sales/"
for fname in glob.glob(path):
    print(fname)
    
    
import os, sys

path = "/home/shridhar/Desktop/CSV/botree_nestle data/csv files/"
dirs = os.listdir(path)

for file in dirs:
    if file == '*.csv':
        print (file)    
        

import os
files = []
for i in os.listdir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/"):
    if i.endswith('*.csv'):
        files.append(open(i))
# do what you want with all these open files        
dir=pd.DataFrame(dir)        
        
        
        
import os
entries = os.scandir('/home/shridhar/Desktop/CSV/botree_nestle data/csv files/')
entries


import pandas as pd
import os
names=[]
with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        print(entry.name)
        
names=pd.DataFrame(entry.name)        








df.T
df1=df.T
for file in files: 
    print (file)

df1.columns
df1.rename(columns={0:'SalesInvoiceQPSCumulative'},inplace=True)
df1.rename(columns={1:'ReturnSchemeLineDt'},inplace=True)
import os
with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        print(entry.name)

import os
names=[]
with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        print(entry.name)

with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        print(a=entry.name)

with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        aa=entry.name

with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        aa[entry]=entry.name

with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        print(entry.name)

names=[]
with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        print(entry.name).append(names)

with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        print(entry.name.append(names))

with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        print(entry.name)

with os.scandir("/home/shridhar/Desktop/CSV/botree_nestle data/csv files/") as entries:
    for entry in entries:
        print(entry.name.append(names))

entries
file1=files.copy
file1=pd.DataFrame(file1)
file1=files
file1=pd.DataFrame(file1)
file1['Q']=file1[0].str.split('/').str[7]
file1['Q1']=file1['Q'].str.split('.').str[0]
file2=file1[['Q1']]
df2=df.copy
df2.set_index(file2['Q1'])
df2['Q1']=file2['Q1']
df2=df
df2.set_index(file2['Q1'])
df2['Q1']=file2['Q1']
df2.set_index('Q1')
df2=df2.set_index('Q1')
df3=df2.T
df3.to_csv('/home/shridhar/Desktop/Metadata.csv')
import os
import pandas as pd 
os.chdir('/home/shridhar/Desktop/CSV/botree_nestle data/csv files/')
salesinvoice=pd.read_csv('SalesInvoice.csv')
SalesInvoiceHdAmount=pd.read_csv('SalesInvoiceHdAmount.csv')
SalesInvoiceLineAmount=pd.read_csv('SalesInvoiceLineAmount.csv')
SalesInvoiceProductTax=pd.read_csv('SalesInvoiceProductTax.csv')
SalesInvoiceSchemeDtBilled=pd.read_csv('SalesInvoiceSchemeDtBilled.csv')
SalesInvoiceSchemeDtFreePrd=pd.read_csv('SalesInvoiceSchemeDtFreePrd.csv')
SalesInvoiceSchemeHd=pd.read_csv('SalesInvoiceSchemeHd.csv')
SalesInvoiceSchemeLineWise=pd.read_csv('SalesInvoiceSchemeLineWise.csv')
Salesman=pd.read_csv('Salesman.csv')
SalesmanMarket=pd.read_csv('SalesmanMarket.csv')
SalesReturn=pd.read_csv('SalesReturn.csv')
salesinvoice.dtypes
SalesInvoiceHdAmount.dtypes
SalesInvoiceLineAmount.dtypes
SalesInvoiceProduct.dtypes
SalesInvoiceProductTax.dtypes
SalesInvoiceSchemeDtBilled.dtypes
SalesInvoiceSchemeDtFreePrd.dtypes
SalesInvoiceSchemeHd.dtypes
salesinvoice.dtypes
SalesInvoiceHdAmount.dtypes
SalesInvoiceLineAmount.dtypes
SalesInvoiceProduct.dtypes
SalesInvoiceProductTax.dtypes
SalesInvoiceSchemeDtBilled.dtypes
SalesInvoiceSchemeDtFreePrd.dtypes
SalesInvoiceSchemeHd.dtypes