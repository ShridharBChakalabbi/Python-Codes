# -*- coding: utf-8 -*-
"""
Created on Wed May 16 19:36:22 2018

@author: admin
"""

import pandas as pd
import pymysql.cursors
from datetime import date, timedelta
from functools import partial
import re
import datetime

# Connect to the database
connection = pymysql.connect(host='34.214.211.162',user='mobiloansteam',password='team123456',db='mobiloans',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

seq1 = str(date.today())
seq2 = str(date.today() - timedelta(days=30))

############### auto and manual dialer file 
def get_data(seq1,seq2):
    au=pd.read_sql("SELECT * FROM mobiloans.mobiloans_auto_dialer where date(date)>="+'"'+seq2+'"'+' and date(date)<='+'"'+seq1+'"',con=connection)
    ma=pd.read_sql("SELECT * FROM mobiloans.mobiloans_manual_dialer where date(date)>="+'"'+seq2+'"'+' and date(date)<='+'"'+seq1+'"',con=connection)
    au=au.drop(au.columns[[2]], axis=1)
    ma=ma.drop(ma.columns[[20,21,22]], axis=1)
    ma.columns=au.columns
    oa=pd.concat([au,ma])
    oa=oa.reset_index()
    return(oa)

dialer_data=get_data(seq1,seq2)


dialer_data['remaining_days']=60-dialer_data['DaysPastDue'].astype(int)
to_datetime_fmt = partial(pd.to_datetime, format='%Y/%m/%d')
dialer_data['date']= dialer_data['date'].apply(to_datetime_fmt)
dialer_data['last_date']=dialer_data['date'] -  pd.to_timedelta(dialer_data['remaining_days'], unit='d')

dialer_data_agg = dialer_data[dialer_data.groupby('AccountNumber').date.transform('max') == dialer_data['date']]
dialer_data_agg=dialer_data_agg.reset_index()



pay=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where  transaction_code in ('121','127','135') and transaction_effective_date>="+'"'+re.sub(' 00:00:00','',str(min(dialer_data_agg['last_date'])))+'"'+" and transaction_effective_date<="+'"'+re.sub(' 00:00:00','',str(max(dialer_data_agg['last_date'])))+'"',con=connection)
pay['AccountNumber1']=pay['loan_number'].isin(dialer_data['AccountNumber'])
pay['AccountNumber1']=pay[pay['AccountNumber1']==True]
pay['date']=(pd.to_datetime(pd.Series(pay['transaction_effective_date']))).dt.date


rev_pay=pd.read_sql("select * FROM mobiloans.mobiloans_payment_file where reversal_transaction_id!='' and transaction_effective_date>="+'"'+re.sub(' 00:00:00','',str(min(dialer_data_agg['last_date'])))+'"'+" and transaction_effective_date<="+'"'+re.sub(' 00:00:00','',str(max(dialer_data_agg['last_date'])))+'"',con=connection)
rev_pay['AccountNumber1']=rev_pay['loan_number'].isin(dialer_data['AccountNumber'])
rev_pay['AccountNumber1']=rev_pay[rev_pay['AccountNumber1']==True]
rev_pay['date']=(pd.to_datetime(pd.Series(rev_pay['transaction_effective_date']))).dt.date



dialer_data1=get_data(seq1=re.sub(' 00:00:00','',str(max(dialer_data_agg['last_date']))),seq2=re.sub(' 00:00:00','',str(min(dialer_data_agg['last_date']))))
dialer_data1['AccountNumber1']=dialer_data1['AccountNumber'].isin(dialer_data['AccountNumber'])
dialer_data2=dialer_data1[dialer_data1['AccountNumber1'] == True]
dialer_data2['date']= dialer_data2['date'].apply(to_datetime_fmt)
dialer_data2=dialer_data2.reset_index()


results=[]
for i in range(0,len(dialer_data_agg)):
    w= pay[(pay['loan_number']==dialer_data_agg['AccountNumber'][i]) & (pay['date']>=datetime.datetime.strptime((re.sub(' 00:00:00','',str(dialer_data_agg['last_date'][i]))),'%Y-%m-%d').date()) & (pay['date'] <=datetime.datetime.strptime((re.sub(' 00:00:00','',str(dialer_data_agg['date'][i]))),'%Y-%m-%d').date())]
    w1= rev_pay[(rev_pay['loan_number']==dialer_data_agg['AccountNumber'][i]) & (rev_pay['date']>=datetime.datetime.strptime((re.sub(' 00:00:00','',str(dialer_data_agg['last_date'][i]))),'%Y-%m-%d').date()) & (rev_pay['date'] <=datetime.datetime.strptime((re.sub(' 00:00:00','',str(dialer_data_agg['date'][i]))),'%Y-%m-%d').date())]
    w2= dialer_data2[(dialer_data2['AccountNumber']==dialer_data_agg['AccountNumber'][i]) & (dialer_data2['date']>=datetime.datetime.strptime((re.sub(' 00:00:00','',str(dialer_data_agg['last_date'][i]))),'%Y-%m-%d').date())]
    w3=[w2['AccountNumber'].iloc[0],w2['CurrentBalance'].iloc[0],w2['AmountDue'].iloc[0],w2['PastDue'].iloc[0],w2['CreditLimit'].iloc[0],sum(w['transaction_amount'].astype(float)),sum(w1['transaction_amount'].astype(float))]
    results.append(w3)
    print(i)
    
results=pd.DataFrame(results)
results.columns = (['AccountNumber','CurrentBalance','AmountDue','PastDue','CreditLimit','payment','rev_payment'])
 
