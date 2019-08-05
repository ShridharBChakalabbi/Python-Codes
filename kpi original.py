
import pandas as pd
import numpy as np
from numpy import unique
from datetime import datetime 
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import pandas.io.sql as psql
import sqlalchemy as sq
from sqlalchemy import create_engine
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import re
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())
from time import gmtime, strftime
import datetime


db = pymysql.connect('34.214.211.162','mobiloansteam' ,'team123456','mobiloans')
cur = db.cursor(pymysql.cursors.DictCursor)
UserId = 'mobiloansteam'

auto_dialer=pd.read_sql("SELECT * FROM mobiloans_auto_dialer where date >= '20180306' and date <= '20180405' ",con=db)
manual_dialer=pd.read_sql("SELECT * FROM mobiloans_manual_dialer where date >= '20180306' and date <= '20180405' ",db)
sql_payment=pd.read_sql("select loan_number AS AccountNumber,count(transaction_amount) AS Count_payment,sum(transaction_amount) AS payment FROM mobiloans.mobiloans_payment_file WHERE transaction_type_description='Payment' and transaction_effective_date >= '2018-03-06' and transaction_effective_date <= '2018-04-05' GROUP BY loan_number ", db)
pay=pd.read_sql("select * from mobiloans_payment_file where transaction_effective_date >= '2018-03-06' and transaction_effective_date <= '2018-04-05' ",db )

pay["reversal_transaction_id"]=pay["reversal_transaction_id"].replace(r'^\s*$', np.nan, regex=True)
pay['transaction_type_description'] = pay['transaction_type_description'].astype('str') 
is_string_dtype(pay['transaction_type_description'])
 
pay['transaction_type_description'] =pay['transaction_type_description'].map(lambda x: re.sub(r'\W+', '', x))
pay1=pay.dropna(subset = ["reversal_transaction_id"])

pay1['transaction_amount'] = pay1['transaction_amount'].apply(pd.to_numeric, errors='coerce')
s= pay1.groupby('loan_number', as_index=False)['transaction_amount'].sum()
s.rename(columns={'transaction_amount': 'rev_paid_amnt'}, inplace=True)
s.rename(columns={'loan_number': 'AccountNumber'}, inplace=True)

sql_payment=  pd.merge(sql_payment, s, on='AccountNumber', how='left')
sql_payment['rev_paid_amnt']=sql_payment['rev_paid_amnt'].fillna(0)
sql_payment['rev_paid_amnt'] = sql_payment['rev_paid_amnt'].apply(pd.to_numeric, errors='coerce')
sql_payment['actual_payment'] = sql_payment['payment'] - sql_payment['rev_paid_amnt']

auto_dialer1=auto_dialer.drop(auto_dialer.columns[[2]], axis=1)
manual_dialer1=manual_dialer.drop(manual_dialer.columns[[20,21,22]], axis=1)
a=list(manual_dialer1.columns.values)
b=list(auto_dialer1.columns.values)
d=dict(zip(a,b))
manual_dialer1=manual_dialer1.rename(columns=d)

com=pd.concat([manual_dialer1, auto_dialer1],ignore_index=True)
com1=com.sort_values(['AccountNumber', 'date'])
data=com1.copy(deep=True)
data['lag']=data.groupby(['AccountNumber'],as_index=False)['CurrentBalance'].shift(1)

data['CurrentBalance'] = data['CurrentBalance'].apply(pd.to_numeric, errors='coerce')
data.lag =data.lag.astype(float)
data['lag'] = data['lag'].apply(pd.to_numeric, errors='coerce')
data['diff']=data['CurrentBalance']-data['lag']
com=data.copy(deep=True)

d1= com.groupby('AccountNumber', as_index=False).agg({'LastNSFDate':'nunique'})
d2= com.groupby('AccountNumber', as_index=False)['date'].max()
d2=pd.merge(d2,com, left_on=['AccountNumber','date'],right_on=['AccountNumber','date'], how='inner')
d3= com.groupby('AccountNumber', as_index=False)['date'].min()
d3=pd.merge(d3,com, left_on=['AccountNumber','date'],right_on=['AccountNumber','date'], how='inner')
d1 = pd.merge(d1,d2[['AccountNumber','CurrentBalance']],on='AccountNumber', how='left' )
d1.rename(columns={'CurrentBalance': 'Max_date_current_bal'}, inplace=True)
d1 = pd.merge(d1,d3[['AccountNumber','CurrentBalance']],on='AccountNumber', how='left' )
d1.rename(columns={'CurrentBalance': 'Min_date_current_bal'}, inplace=True)
d1 = pd.merge(d1,d2[['AccountNumber','DaysPastDue']],on='AccountNumber', how='left' )
d1.rename(columns={'DaysPastDue': 'max_date_days_past_due'}, inplace=True)

d4=pd.crosstab(index=com['AccountNumber'], columns=[com['ActionCodeDescription']])
d4 = d4.reset_index()
d1=pd.merge(d1,d4, left_on=['AccountNumber'],right_on=['AccountNumber'], how='inner')

d5=com.groupby(['AccountNumber']).size().reset_index(name='No_calls')
d1 = pd.merge(d1,d5[['AccountNumber','No_calls']],on='AccountNumber', how='left' )
h = pd.merge(d5,d2[['AccountNumber','ActionCodeDescription']],on='AccountNumber', how='left' )
h.drop(h.columns[1],axis=1,inplace=True)
d1 = pd.merge(d1,h[['AccountNumber','ActionCodeDescription']],on='AccountNumber', how='left' )
d1.rename(columns={'ActionCodeDescription': 'max_date_actionCodeDescription'}, inplace=True)


d6= com.groupby('AccountNumber', sort=False)["CurrentBalance"].max().reset_index(name ='Max_current_bal')
d1 = pd.merge(d1,d6[['AccountNumber','Max_current_bal']],on='AccountNumber', how='left' )

d1=d1.drop_duplicates(subset=['AccountNumber'])
d1 = pd.merge(d1,com[['AccountNumber','CreditLimit']],on='AccountNumber', how='left' )
d1.rename(columns={'CreditLimit': 'Credit_limit'}, inplace=True)
d1=d1.drop_duplicates(subset=['AccountNumber'])
d1 = pd.merge(d1,sql_payment[['AccountNumber','actual_payment']],on='AccountNumber', how='left' )
d1.rename(columns={'actual_payment': 'payment'}, inplace=True)  #error
d1['payment'].fillna(0, inplace=True)
d1['Credit_limit'] = d1['Credit_limit'].apply(pd.to_numeric, errors='coerce')
d1.Credit_limit =d1.Credit_limit.astype(float)
d1.Max_current_bal =d1.Max_current_bal.astype(float)
d1['credit_exp_ratio'] = d1['Max_current_bal']/d1['Credit_limit']
d1.payment =d1.payment.astype(float)
d1.Credit_limit =d1.Credit_limit.astype(float)

g = d1.columns.to_series().groupby(d1.dtypes).groups


d1['payment_cap'] = d1['payment'] / d1['Credit_limit'] # error
d1=d1.drop_duplicates(subset=['AccountNumber'])
def func(d1):
            if d1['Credit_limit'] > 1500:
                val=">1500"
            elif  d1['Credit_limit'] >1200:
                val="1200-1500"
            elif d1['Credit_limit'] > 800:
                val="800-1200"
            elif d1['Credit_limit'] >200:
                val="200-800"
            else:
                val="200-0"
            return val
d1['credit_group'] = d1.apply(func, axis=1)
d1['max_date_days_past_due'] = d1['max_date_days_past_due'].apply(pd.to_numeric, errors='coerce')
d1.max_date_days_past_due =d1.max_date_days_past_due.astype(float)
def f(d1):
         if d1['max_date_days_past_due']>=45:
             val ="60-45"
         elif d1['max_date_days_past_due']>=30:
             val="30-45"
         elif d1['max_date_days_past_due']>=15:
             val="30-15"
         else:
             val="15-1"
         return val
d1['grp_days_past_due '] = d1.apply(f, axis=1)
        
                  
              
import pandasql as ps
import sqlite3
d7= """select AccountNumber,diff>0, abs(sum(diff)) as loan from com group by AccountNumber,diff>0"""
d8=ps.sqldf(d7, locals())

d1 = pd.merge(d1,d8[['AccountNumber','loan']],on='AccountNumber', how='left' )
d1=d1.drop_duplicates(subset=['AccountNumber'])
d1['loan'].fillna(0, inplace=True)
d1['Fianl_Loan_amount'] = d1['Min_date_current_bal']+d1['loan']
d1 = pd.merge(d1,d2[['AccountNumber','AmountDue']],on='AccountNumber', how='left' )
d1.rename(columns={'AmountDue': 'Amount_Due'}, inplace=True)
d1.rename(columns={'grp_days_past_due ': 'grp_days_past_due'}, inplace=True)
j="""select payment>0,credit_group,grp_days_past_due ,count(distinct AccountNumber) as Count_cust,sum(Fianl_Loan_amount) as Loan_Given ,sum(No_calls) as Number_calls ,sum(payment) as  payment_made,sum(Amount_Due) as Amount_outstanding,sum(Max_date_current_bal) as sum_max_cur from d1 group by payment>0,credit_group,grp_days_past_due """
n1=ps.sqldf(j, locals())
n1['Amount_outstanding_per']=n1['Amount_outstanding']/n1['sum_max_cur']*100

def k(n1):
         if n1['payment>0']>0:
             val ="Paid"
        
         else:
             val="Not_Paid"
         return val
n1['payment>0'] = n1.apply(k, axis=1)
        

b="2018-03-06 to 2018-04-05"
idx=0

n1.insert(loc=idx, column='date', value=b)
n2=d1.groupby('Credit_limit', as_index=False).agg({'Max_date_current_bal':'sum','payment':'sum'})
n2.rename(columns={'Max_date_current_bal': 'Current_balance','payment':'actual_payment'}, inplace=True)
n2.insert(loc=idx, column='date', value=b)
n3=d1.groupby('grp_days_past_due', as_index=False).agg({'Max_date_current_bal':'sum','payment':'sum'})
n3.rename(columns={'Max_date_current_bal': 'Current_balance','payment':'actual_payment'}, inplace=True)
n3.insert(loc=idx, column='date', value=b)


n1.to_csv('kpi2monthly01.csv',sep=',',index=False)
n2.to_csv('kpi4monthly02.csv',sep=',',index=False)
n3.to_csv('kpi5monthly03.csv',sep=',',index=False)
