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
import time
from datetime import datetime, timedelta
import numpy as np



user="mobiloansteam" 
pw='team123456'
data_base="mobiloans"
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user=user,pw=pw,db=data_base))
       
db = pymysql.connect('34.214.211.162','mobiloansteam' ,'team123456','mobiloans')
cur = db.cursor(pymysql.cursors.DictCursor)
UserId = 'mobiloansteam'


seq1 = 3
seq_date1, space, time =(str(datetime.now() - timedelta(days=seq1))).partition(' ')
seq2 = 7 + seq1
seq_date2, space, time=str(datetime.now() - timedelta(days=seq2)).partition(' ')
seq_date3 = 15 + seq1
seq_date3, space, time =(str(datetime.now() - timedelta(days=seq_date3))).partition(' ')
seq_date4 = 30 + seq1
seq_date4, space, time =(str(datetime.now() - timedelta(days=seq_date4))).partition(' ')


auto_dialer=pd.read_sql("SELECT * FROM mobiloans.mobiloans_auto_dialer where date = '"+seq_date1+"'",db)
manual_dialer=pd.read_sql("select * from mobiloans.mobiloans_manual_dialer where date = '"+seq_date1+"'",db)

manual_dialer=manual_dialer.replace(r'^\s*$', np.nan, regex=True)



auto_dialer1=auto_dialer.drop(auto_dialer.columns[[2]],axis=1)
manual_dialer1=manual_dialer.drop(manual_dialer.columns[20:23],axis=1)
################changing manual dialer column names ##########################
a=list(manual_dialer1.columns.values)
b=list(auto_dialer1.columns.values)
c=dict(zip(a,b))
manual_dialer1=manual_dialer1.rename(columns=c)
com=pd.concat([auto_dialer1,manual_dialer1])

pay=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where date(transaction_effective_date)>='"+seq_date2+"' and date(transaction_effective_date)<='"+seq_date1+"'",con=db)

sql_payment=pd.read_sql("select loan_number as AccountNumber,(transaction_amount) as payment,date(transaction_effective_date) as pay_date from mobiloans.mobiloans_payment_file where transaction_type_description='Payment' and transaction_code in (121,127,135) and date(transaction_effective_date)>='"+seq_date2+"'  and date(transaction_effective_date)<= '"+seq_date1+"'",db)

s_pay = sqldf("select loan_number as AccountNumber,count(transaction_amount) as count_of_payment, sum(transaction_amount) as payment from pay where transaction_code in (121,127,135) group by loan_number")

pay["reversal_transaction_id"]=pay["reversal_transaction_id"].replace(r'^\s*$', np.nan, regex=True)

pay['transaction_type_description'] = pay['transaction_type_description'].astype('str') 
is_string_dtype(pay['transaction_type_description'])
 
pay['transaction_type_description'] =pay['transaction_type_description'].map(lambda x: re.sub(r'\W+', '', x))
pay1=pay.dropna(subset = ["reversal_transaction_id"]) 
pay1['transaction_amount']=pd.to_numeric(pay1['transaction_amount'])
s= pay1.groupby('loan_number', as_index=False)['transaction_amount'].sum()
s.rename(columns={'transaction_amount': 'rev_paid_amnt'}, inplace=True)
s.rename(columns={'loan_number': 'AccountNumber'}, inplace=True)


s_pay = pd.merge(s_pay,s[['AccountNumber','rev_paid_amnt']],on='AccountNumber', how='left' )
if len(s)==0:
    s_pay['rev_paid_amnt']==0
    
    
s_pay['actual_payment'] =s_pay['payment'].sub(s_pay['rev_paid_amnt'],fill_value=0)


sql_payment['pay_date']= pd.to_datetime(sql_payment['pay_date'])
sql_payment['pay_day']= sql_payment['pay_date'].dt.weekday_name
sql_payment['payment'] = sql_payment['payment'].apply(pd.to_numeric, errors='coerce')
max_pay_90=sql_payment.groupby(['AccountNumber', 'pay_date']).agg({'payment':'sum'}).reset_index()
max_pay_90.rename(columns={'payment':'max_amount'}, inplace=True)


max_pay_90=max_pay_90.groupby(['AccountNumber','pay_date']).agg({'max_amount':['max','min']}).reset_index()
max_pay_90.columns = ["AccountNumber","pay_date","max_amount","min_amount"]



d5=pay.groupby(['loan_number']).size().reset_index(name='Count')


max_date=pay.groupby(['loan_number']).agg({'transaction_effective_date':'max'}).reset_index()
max_date = pd.merge(max_date,d5[['loan_number','Count']],on='loan_number', how='left' )
max_date.rename(columns={'transaction_effective_date':'max_date'}, inplace=True)
max_date.rename(columns={'loan_number':'AccountNumber'}, inplace=True)
max_date['max_date'] = pd.to_datetime(max_date['max_date']).dt.date



max_call_date= com.groupby('AccountNumber', as_index=False)['date'].max()
max_call_date.rename(columns={'date': 'max_call_date'}, inplace=True)


acc_num=com.AccountNumber.unique()
acc_num=pd.DataFrame(acc_num)
acc_num.columns = ["AccountNumber"]

acc_num=acc_num.dropna(subset = ["AccountNumber"]) 




acc_num= pd.merge(acc_num, s_pay[['AccountNumber', 'count_of_payment']],how='left', on=['AccountNumber'])
acc_num= pd.merge(acc_num,s_pay[['AccountNumber','payment']],on='AccountNumber', how='left' )
acc_num.rename(columns={'payment': 'gross_payment'}, inplace=True)
acc_num= pd.merge(acc_num,s_pay[['AccountNumber','rev_paid_amnt']],on='AccountNumber', how='left' )
acc_num.rename(columns={'rev_paid_amnt': 'reversed_payment'}, inplace=True)

acc_num= pd.merge(acc_num,s_pay[['AccountNumber','actual_payment']],on='AccountNumber', how='left' )


### (1)
##### Interval days b/w max of call date and max of paid date  ###############
acc_num= pd.merge(acc_num,max_call_date[['AccountNumber','max_call_date']],on='AccountNumber', how='left' )
acc_num= pd.merge(acc_num,max_date[['AccountNumber','max_date']],on='AccountNumber', how='left' )
max_call_date.rename(columns={'date': 'max_call_date'}, inplace=True)
acc_num.rename(columns={'max_date': 'max_transaction_date'}, inplace=True)

acc_num['max_call_date'] = pd.to_datetime(acc_num['max_call_date']).dt.date
acc_num['max_transaction_date'] = pd.to_datetime(acc_num['max_transaction_date']).dt.date
acc_num['interval_days'] =acc_num['max_call_date']-acc_num['max_transaction_date']
acc_num['interval_days'] = acc_num['interval_days'] / np.timedelta64(1, 'D')
acc_num['max_transaction_date']=acc_num['max_transaction_date'].fillna(0)


########## R-score calculation ########################

    r= sql_payment.groupby('AccountNumber', as_index=False)['pay_date'].max()

    i=max_date['max_date'].max()
    r['max_date']=str(i)

    r['max_date']= pd.to_datetime(r['max_date']).dt.date
    r['pay_date'] = pd.to_datetime(r['pay_date']).dt.date
    r['recency'] =(r['max_date']-r['pay_date']) 
    r['recency'] = r['recency'] / np.timedelta64(1, 'D')
    r['recency']=r['recency'] +1
    r=r.sort_values(by=['recency'])

    r_t=np.percentile(r['recency'],[20,40,60,80,100])
    r['R_points']=np.where(r['recency']<=r_t[0],1,np.where(r['recency']<=r_t[1],2,np.where(r['recency']<=r_t[2],3,np.where(r['recency']<=r_t[3],4,5))))



########## F-score calculation #########################
freq=sql_payment.groupby(['AccountNumber']).size().reset_index(name='freq')
r_f=np.percentile(freq['freq'],[20,40,60,80,100])
freq['F_points']=np.where(freq['freq']<=r_f[0],1,np.where(freq['freq']<=r_f[1],2,np.where(freq['freq']<=r_f[2],3,np.where(freq['freq']<=r_f[3],4,5))))

######### M -score calculation ###########################

monitery= s_pay.groupby('AccountNumber', as_index=False)['actual_payment'].sum()
monitery=monitery.fillna(0)
r_m=np.percentile(monitery['actual_payment'],[20,40,60,80,100])
monitery['m_points']=np.where(monitery['actual_payment']<=r_m[0],1,np.where(monitery['actual_payment']<=r_m[1],2,np.where(monitery['actual_payment']<=r_m[2],3,np.where(monitery['actual_payment']<=r_m[3],4,5))))

r= pd.merge(r,freq[['AccountNumber','freq']],on='AccountNumber', how='left' )
r= pd.merge(r,freq[['AccountNumber','F_points']],on='AccountNumber', how='left' )
r= pd.merge(r,monitery[['AccountNumber','actual_payment']],on='AccountNumber', how='left' )
r= pd.merge(r,monitery[['AccountNumber','m_points']],on='AccountNumber', how='left' )

###### % Amount paid in last 15 days ##########
seq1 = 1
seq_date1, space, time =(str(datetime.now() - timedelta(days=seq1))).partition(' ')
seq2 = 15 + seq1
seq_date2, space, time=str(datetime.now() - timedelta(days=seq2)).partition(' ')

pay2=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where date(transaction_effective_date)<='"+seq_date1+"' and date(transaction_effective_date)>='"+seq_date2+"'",db)
a_pay=pd.read_sql("Select loan_number as AccountNumber, count(transaction_amount) as count_of_payments,sum(transaction_amount) as payment from mobiloans.mobiloans_payment_file where transaction_type_description='Payment' and transaction_code in (121,127,135) and date(transaction_effective_date)<='"+seq_date1+"'and date(transaction_effective_date)>= '"+seq_date2+"' group by loan_number",db)

pay2["reversal_transaction_id"]=pay2["reversal_transaction_id"].replace(r'^\s*$', np.nan, regex=True)
pay2['transaction_type_description'] =pay2['transaction_type_description'].map(lambda x: re.sub(r'\W+', '', x))
pay3=pay2.dropna(subset = ["reversal_transaction_id"]) 
pay2['reversal_transaction_id'].isnull().sum()
pay3['transaction_amount'] = pay3['transaction_amount'].apply(pd.to_numeric, errors='coerce')

s2=pay3.groupby('loan_number', as_index=False).agg({'transaction_amount':'sum'})
s2.rename(columns={'transaction_amount':'rev_paid_amnt'}, inplace=True)
s2.rename(columns={'loan_number':'AccountNumber'}, inplace=True)

a_pay= pd.merge(a_pay,s2[['AccountNumber','rev_paid_amnt']],on='AccountNumber', how='left' )
if len(s)==0:
    a_pay['rev_paid_amnt']==0


a_pay['actual_payment'] =a_pay['payment'].sub(a_pay['rev_paid_amnt'],fill_value=0)

d2= com.groupby('AccountNumber', as_index=False)['date'].min()
d2=pd.merge(com,d2,left_on=['AccountNumber','date'],right_on=['AccountNumber','date'],how ='inner')
a_pay= pd.merge(a_pay,d2[['AccountNumber','AmountDue']],on='AccountNumber', how='left' )
a_pay['actual_payment'] = a_pay['actual_payment'].apply(pd.to_numeric, errors='coerce')
a_pay['AmountDue'] = a_pay['AmountDue'].apply(pd.to_numeric, errors='coerce')

a_pay['per_paid_15days']=(a_pay['actual_payment']/a_pay['AmountDue'])*100

###### % Amount paid in last 30 days ##########


pay_30=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where date(transaction_effective_date)<='"+seq_date1+"' and date(transaction_effective_date)>='"+seq_date4+"'",db)
a_pay_30 =pd.read_sql("Select loan_number as AccountNumber, count(transaction_amount) as count_of_payments,sum(transaction_amount) as payment from mobiloans.mobiloans_payment_file where transaction_type_description='Payment' and transaction_code in (121,127,135) and date(transaction_effective_date)<='"+seq_date1+"' and date(transaction_effective_date)>= '"+seq_date4+"' group by loan_number",db)

pay_30["reversal_transaction_id"]=pay["reversal_transaction_id"].replace(r'^\s*$', np.nan, regex=True)
pay_30['reversal_transaction_id'].isnull().sum()
pay_30['transaction_type_description'] =pay['transaction_type_description'].map(lambda x: re.sub(r'\W+', '', x))
pay_30['transaction_type_description'] = pay_30['transaction_type_description'].astype('str') 
is_string_dtype(pay['transaction_type_description'])
pay_4=pay2.dropna(subset = ["reversal_transaction_id"]) 
pay_4['transaction_amount'] = pay_4['transaction_amount'].apply(pd.to_numeric, errors='coerce')

pay_4['reversal_transaction_id'].isnull().sum()


pay3['transaction_amount'] = pay3['transaction_amount'].apply(pd.to_numeric, errors='coerce')

s3=pay_4.groupby('loan_number', as_index=False).agg({'transaction_amount':'sum'})
s3.rename(columns={'transaction_amount':'rev_paid_amnt'}, inplace=True)
s3.rename(columns={'loan_number':'AccountNumber'}, inplace=True)

a_pay_30= pd.merge(a_pay_30,s3[['AccountNumber','rev_paid_amnt']],on='AccountNumber', how='left' )
if len(s)==0:
    a_pay['rev_paid_amnt']==0


a_pay_30['actual_payment'] =a_pay_30['payment'].sub(a_pay_30['rev_paid_amnt'],fill_value=0)

d3= com.groupby('AccountNumber', as_index=False)['date'].min()
d3=pd.merge(com,d3,left_on=['AccountNumber','date'],right_on=['AccountNumber','date'],how ='inner')
a_pay_30['actual_payment'] = a_pay_30['actual_payment'].apply(pd.to_numeric, errors='coerce')
d3['AmountDue'] = d3['AmountDue'].apply(pd.to_numeric, errors='coerce')

a_pay_30['per_paid_15days']=(a_pay_30['actual_payment']/d3['AmountDue'])*100


a_pay_30= pd.merge(a_pay,d2[['AccountNumber','AmountDue']],on='AccountNumber', how='left' )
a_pay['actual_payment'] = a_pay['actual_payment'].apply(pd.to_numeric, errors='coerce')
d2['AmountDue'] = d2['AmountDue'].apply(pd.to_numeric, errors='coerce')

a_pay_30['per_paid_30days']=(a_pay['actual_payment']/d2['AmountDue'])*100




#################################### % Amount paid in last 60 days ############################


seq5 = 1
seq_date5, space, time =(str(datetime.now() - timedelta(days=seq5))).partition(' ')
seq6 = 60 + seq5
seq_date6, space, time=str(datetime.now() - timedelta(days=seq6)).partition(' ')
seq_date3 = 15 + seq1

auto_dialer=pd.read_sql("SELECT * FROM mobiloans.mobiloans_auto_dialer where date = '"+seq_date5+"'",db)
manual_dialer=pd.read_sql("select * from mobiloans.mobiloans_manual_dialer where date = '"+seq_date5+"'",db)

manual_dialer=manual_dialer.replace(r'^\s*$', np.nan, regex=True)



auto_dialer1=auto_dialer.drop(auto_dialer.columns[[2]],axis=1)
manual_dialer1=manual_dialer.drop(manual_dialer.columns[20:23],axis=1)

a=list(manual_dialer1.columns.values)
b=list(auto_dialer1.columns.values)
c=dict(zip(a,b))
manual_dialer1=manual_dialer1.rename(columns=c)
com=pd.concat([auto_dialer1,manual_dialer1])

pay_60=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where date(transaction_effective_date)<='"+seq_date5+"' and date(transaction_effective_date)>='"+seq_date6+"'",db)
pay_60.rename(columns={'loan_number':'AccountNumber'}, inplace=True)

a_pay_60=pd.read_sql("Select loan_number as AccountNumber, count(transaction_amount) as count_of_payments,sum(transaction_amount) as payment from mobiloans.mobiloans_payment_file where transaction_type_description='Payment' and transaction_code in (121,127,135) and date(transaction_effective_date)<='"+seq_date5+"'and date(transaction_effective_date)>= '"+seq_date6+"' group by loan_number",db)
pay_60["reversal_transaction_id"]=pay_60["reversal_transaction_id"].replace(r'^\s*$', np.nan, regex=True)
pay_60['transaction_type_description'] =pay_60['transaction_type_description'].map(lambda x: re.sub(r'\W+', '', x))

rev_60=pay_60.dropna(subset = ["reversal_transaction_id"]) 
rev_60['transaction_amount'] = rev_60['transaction_amount'].apply(pd.to_numeric, errors='coerce')

rev_sum=rev_60.groupby('AccountNumber', as_index=False).agg({'transaction_amount':'sum'})
rev_sum.rename(columns={'transaction_amount':'rev_paid_amnt'}, inplace=True)
a_pay_60= pd.merge(a_pay_60,rev_sum[['AccountNumber','rev_paid_amnt']],on='AccountNumber', how='left' )
if len(s)==0:
    a_pay_60['rev_paid_amnt']==0

a_pay_60['actual_payment'] =a_pay_60['payment'].sub(a_pay_60['rev_paid_amnt'],fill_value=0)

au_ma= com.groupby('AccountNumber', as_index=False)['date'].min()
au_ma=pd.merge(com,au_ma,left_on=['AccountNumber','date'],right_on=['AccountNumber','date'],how ='inner')
a_pay_60= pd.merge(a_pay_60,au_ma[['AccountNumber','AmountDue']],on='AccountNumber', how='left' )
a_pay_60['actual_payment'] = a_pay_60['actual_payment'].apply(pd.to_numeric, errors='coerce')
a_pay_60['AmountDue'] = a_pay_60['AmountDue'].apply(pd.to_numeric, errors='coerce')
a_pay_60['per_paid_60days']=(a_pay_60['actual_payment']/a_pay_60['AmountDue'])*100


#################################### % Amount paid in last 90 days ############################
seq7 = 1
seq_date7, space, time =(str(datetime.now() - timedelta(days=seq7))).partition(' ')
seq8 = 90 + seq7
seq_date8, space, time=str(datetime.now() - timedelta(days=seq8)).partition(' ')

pay_90=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where date(transaction_effective_date)<='"+seq_date7+"' and date(transaction_effective_date)>='"+seq_date8+"'",db)
pay_90.rename(columns={'loan_number':'AccountNumber'}, inplace=True)

a_pay_90=pd.read_sql("Select loan_number as AccountNumber, count(transaction_amount) as count_of_payments,sum(transaction_amount) as payment from mobiloans.mobiloans_payment_file where transaction_type_description='Payment' and transaction_code in (121,127,135) and date(transaction_effective_date)<='"+seq_date7+"'and date(transaction_effective_date)>= '"+seq_date8+"' group by loan_number",db)

pay_90["reversal_transaction_id"]=pay_90["reversal_transaction_id"].replace(r'^\s*$', np.nan, regex=True)
pay_90['transaction_type_description'] =pay_90['transaction_type_description'].map(lambda x: re.sub(r'\W+', '', x))

rev_90=pay_90.dropna(subset = ["reversal_transaction_id"]) 
rev_90['transaction_amount'] = rev_90['transaction_amount'].apply(pd.to_numeric, errors='coerce')

rev_sum_90=rev_90.groupby('AccountNumber', as_index=False).agg({'transaction_amount':'sum'})
rev_sum_90.rename(columns={'transaction_amount':'rev_paid_amnt'}, inplace=True)
a_pay_90= pd.merge(a_pay_90,rev_sum_90[['AccountNumber','rev_paid_amnt']],on='AccountNumber', how='left' )

a_pay_90['actual_payment'] =a_pay_90['payment'].sub(a_pay_90['rev_paid_amnt'],fill_value=0)
au_ma= com.groupby('AccountNumber', as_index=False)['date'].min()
au_ma=pd.merge(au_ma,com,left_on=['AccountNumber','date'],right_on=['AccountNumber','date'],how ='inner')
a_pay_90= pd.merge(a_pay_90,au_ma[['AccountNumber','AmountDue']],on='AccountNumber', how='left' )
a_pay_90['actual_payment'] = a_pay_90['actual_payment'].apply(pd.to_numeric, errors='coerce')
a_pay_90['AmountDue'] = a_pay_90['AmountDue'].apply(pd.to_numeric, errors='coerce')
a_pay_90['per_paid_90days']=(a_pay_90['actual_payment']/a_pay_90['AmountDue'])*100

############Count of gross payments made in 15 days.
pay2=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where date(transaction_effective_date)<='"+seq_date1+"' and date(transaction_effective_date)>='"+seq_date3+"'",db)

count15 = sqldf("select count(transaction_amount) as count_gross from pay2 where transaction_code == 121 group by loan_number")

############Count of gross payments made in 30 days.]
pay_30=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where date(transaction_effective_date)<='"+seq_date1+"' and date(transaction_effective_date)>='"+seq_date4+"'",db)
count30 = sqldf("select count(transaction_amount) from pay_60 where transaction_code == 121 group by loan_number")

############Count of gross payments made in 60 days.]
pay_60=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where date(transaction_effective_date)<='"+seq_date1+"' and date(transaction_effective_date)>='"+seq_date4+"'",db)
count90 = sqldf("select count(transaction_amount) from pay_60 where transaction_code == 121 group by loan_number")

############Count of gross payments made in 90 days.]
pay_90=pd.read_sql("SELECT * FROM mobiloans.mobiloans_payment_file where date(transaction_effective_date)<='"+seq_date1+"' and date(transaction_effective_date)>='"+seq_date4+"'",db)
count90 = sqldf("select count(transaction_amount) from pay_90 where transaction_code == 121 group by loan_number")

############Count of reversal payments made in 15 days.
count_rev15 = sqldf("select count(transaction_amount) as count_gross from pay2 where transaction_code == 211 group by loan_number")

############Count of reversal payments made in 30 days.
count_rev30 = sqldf("select count(transaction_amount) from pay_30 where transaction_code == 211 group by loan_number")

############Count of reversal payments made in 60 days.
count_rev30 = sqldf("select count(transaction_amount) from pay_60 where transaction_code == 211 group by loan_number")

############Count of reversal payments made in 90 days.
count_rev30 = sqldf("select count(transaction_amount) from pay_90 where transaction_code == 211 group by loan_number")

## Calculating credit exposure
com['CurrentBalance'] = com['CurrentBalance'].apply(pd.to_numeric, errors='coerce')
com['CreditLimit'] = com['CreditLimit'].apply(pd.to_numeric, errors='coerce')
com['CreditExposure'] =com['CurrentBalance']/com['CreditLimit']

## Amount due / Current Balance
com['AmountDue'] = com['AmountDue'].apply(pd.to_numeric, errors='coerce')
com['CurrentBalance'] = com['CurrentBalance'].apply(pd.to_numeric, errors='coerce')
com['AmtDue_AmtPaid'] = com['AmountDue']/com['CurrentBalance']