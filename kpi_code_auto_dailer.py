import os
import pandas as pd 
import numpy as np
import pymysql.cursors
import re
import datetime
from datetime import date, timedelta
from uszipcode import ZipcodeSearchEngine
import csv
import uszipcode
from pandasql import sqldf
import time
from datetime import datetime, timedelta

connection = pymysql.connect(host='34.221.148.47',user='mobiloansteam',password='team123456',db='mobiloans_dev',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

mobilaons_pii = pd.read_sql("select AccountNumber,AES_DECRYPT(FirstName,123654), AES_DECRYPT(LastName,123654),AES_DECRYPT(State,123654),AES_DECRYPT(HomePhone,123654),AES_DECRYPT(CellPhone,123654),AES_DECRYPT(WorkPhone,123654),AES_DECRYPT(City,123654) from mobiloans_dev.mbl_master_table where auto_manual = 'Auto_Dialer' ",connection)
mobiloanspii = mobilaons_pii
mobiloanspii = mobiloanspii.astype(str).replace('b','',regex=True)

for i, col in enumerate(mobiloanspii.columns): 
        mobiloanspii.iloc[:, i] = mobiloanspii.iloc[:, i].str.replace(r"[\"\',]", '')


start_date = '2018-03-04'
end_date = '2018-03-31'

data=pd.read_csv(r"/home/anjali/Anjali/BACKUP/Mobiloans/febmarapr.csv",sep=',')
data['ConnectedDate'] = pd.to_datetime(data['ConnectedDate']).dt.date

pay=sqldf("SELECT * FROM data where date(ConnectedDate) >='"+start_date+"' and date(ConnectedDate) <='"+end_date+"' and  CallDirection = 'Outbound' ")
levels=sqldf("select distinct(DisplayUserName) from pay" )
a = pay[(pay['CallDurationSeconds'] >=50)]
count=sqldf("SELECT DisplayUserName , count(DisplayUserName) as count FROM pay group by DisplayUserName ")

auto=sqldf("SELECT * FROM data where date(ConnectedDate) >='"+start_date+"' and date(ConnectedDate) <='"+end_date+"' and CallDirection = 'Outbound' ")

Outbound=sqldf("SELECT * FROM data where date(ConnectedDate) >='"+start_date+"' and date(ConnectedDate) <='"+end_date+"' and CallDirection = 'Outbound' ")
levels=sqldf("select distinct(DisplayUserName) from Outbound where date(ConnectedDate) >='"+start_date+"' and date(ConnectedDate) <='"+end_date+"'" )

################## Home Phone ###############
Outbound.rename(columns={'Ph_Number':'AES_DECRYPT(HomePhone,123654)'}, inplace=True)
Outbound = pd.merge(Outbound,mobiloanspii[['AccountNumber','AES_DECRYPT(HomePhone,123654)']],on='AES_DECRYPT(HomePhone,123654)', how='left' )
Outbound.rename(columns={'AccountNumber':'Acc_num_HomePhone'}, inplace=True)
################## CellPhone ###############
Outbound.rename(columns={'AES_DECRYPT(HomePhone,123654)':'AES_DECRYPT(CellPhone,123654)'}, inplace=True)
Outbound = pd.merge(Outbound,mobiloanspii[['AccountNumber','AES_DECRYPT(CellPhone,123654)']],on='AES_DECRYPT(CellPhone,123654)', how='left' )
Outbound.rename(columns={'AccountNumber':'Acc_num_CellPhone'}, inplace=True)

################## Workphone ###############
Outbound.rename(columns={'AES_DECRYPT(CellPhone,123654)':'AES_DECRYPT(WorkPhone,123654)'}, inplace=True)
Outbound = pd.merge(Outbound,mobiloanspii[['AccountNumber','AES_DECRYPT(WorkPhone,123654)']],on='AES_DECRYPT(WorkPhone,123654)', how='left' )
Outbound.rename(columns={'AccountNumber':'Acc_num_WorkPhone'}, inplace=True)
a=Outbound.copy()
a=a.drop_duplicates(subset=['AES_DECRYPT(WorkPhone,123654)'])


auto.rename(columns={'Ph_Number':'AES_DECRYPT(WorkPhone,123654)'}, inplace=True)
auto = pd.merge(auto,a[['AES_DECRYPT(WorkPhone,123654)','Acc_num_HomePhone','Acc_num_CellPhone','Acc_num_WorkPhone']],on='AES_DECRYPT(WorkPhone,123654)', how='left' )
auto.rename(columns={'ConnectedDate':'date'}, inplace=True)

##############################################################################
auto_dialer=pd.read_sql("SELECT * FROM mobiloans_dev.mbl_auto_dialer where dialer_company = 'yessio' and date(date)>= '"+start_date+"' and date(date)<= '"+end_date+"'",connection)

auto1=auto.copy()

auto_dialer.rename(columns={'AccountNumber':'Acc_num_HomePhone'}, inplace=True)

auto_dialer['date'] = pd.to_datetime(auto_dialer['date']).dt.date
auto1['date'] = pd.to_datetime(auto1['date']).dt.date
auto1[['Acc_num_HomePhone','Acc_num_CellPhone','Acc_num_WorkPhone']] = auto1[['Acc_num_HomePhone','Acc_num_CellPhone','Acc_num_WorkPhone']].apply(pd.to_numeric, errors='coerce')

o = pd.merge(auto1,auto_dialer[['Acc_num_HomePhone','date','DaysPastDue']],on=['Acc_num_HomePhone','date'], how='left' )
o.rename(columns={'DaysPastDue':'Acc_num_HomePhone_DaysPastDue'}, inplace=True)

auto_dialer.rename(columns={'Acc_num_HomePhone':'Acc_num_CellPhone'}, inplace=True)

o= pd.merge(o,auto_dialer[['Acc_num_CellPhone','date','DaysPastDue']],on=['Acc_num_CellPhone','date'], how='left' )
o.rename(columns={'DaysPastDue':'Acc_num_CellPhone_DaysPastDue'}, inplace=True)

auto_dialer.rename(columns={'Acc_num_CellPhone':'Acc_num_WorkPhone'}, inplace=True)
o= pd.merge(o,auto_dialer[['Acc_num_WorkPhone','date','DaysPastDue']],on=['Acc_num_WorkPhone','date'], how='left' )
o.rename(columns={'DaysPastDue':'Acc_num_WorkPhone_DaysPastDue'}, inplace=True)

v=o.fillna(0)

###################################################################################
trail=v.copy()

def func(trail):
          if (trail['Acc_num_HomePhone']==trail['Acc_num_CellPhone']==trail['Acc_num_WorkPhone']):
              val=trail['Acc_num_HomePhone']
          elif  (trail['Acc_num_HomePhone']==trail['Acc_num_CellPhone']):
              val=trail['Acc_num_HomePhone']
          elif (trail['Acc_num_HomePhone']==trail['Acc_num_WorkPhone']):
              val=trail['Acc_num_HomePhone']
          elif (trail['Acc_num_CellPhone']==trail['Acc_num_WorkPhone']):
              val=trail['Acc_num_CellPhone']
          elif (trail['Acc_num_HomePhone']!=trail['Acc_num_CellPhone']):
              val=trail['Acc_num_HomePhone']
          elif (trail['Acc_num_HomePhone']!=trail['Acc_num_WorkPhone']):
              val=trail['Acc_num_HomePhone']
          elif (trail['Acc_num_CellPhone']!=trail['Acc_num_WorkPhone']):
              val=trail['Acc_num_CellPhone']
          else:
              print("last one")
          return val
trail['acc_num'] = trail.apply(func, axis=1)

def n(trail):
       if trail['acc_num']==0:
           val=trail['Acc_num_HomePhone']+trail['Acc_num_CellPhone']+trail['Acc_num_WorkPhone']
       else:
           val=trail['acc_num']
       return val
trail['acc_num'] = trail.apply(n, axis=1)

###########################################################################################

#trail['acc_num']=trail['Acc_num_HomePhone']+v['Acc_num_CellPhone']+v['Acc_num_WorkPhone']

trail[['Acc_num_HomePhone_DaysPastDue','Acc_num_CellPhone_DaysPastDue','Acc_num_WorkPhone_DaysPastDue']] = trail[['Acc_num_HomePhone_DaysPastDue','Acc_num_CellPhone_DaysPastDue','Acc_num_WorkPhone_DaysPastDue']].apply(pd.to_numeric, errors='coerce')


trail['Days_past_due']=trail['Acc_num_HomePhone_DaysPastDue']+trail['Acc_num_CellPhone_DaysPastDue']+trail['Acc_num_WorkPhone_DaysPastDue']

df = trail.query('acc_num != 0')

df1 = sqldf("select acc_num,Days_past_due, max(date) from df group by acc_num")
##########################################################################################

autodialer_disposition=pd.read_sql("SELECT * FROM mobiloans_dev.mbl_auto_dispositions",connection)
autodialer_disposition['Listdate'] = pd.to_datetime(autodialer_disposition['Listdate']).dt.date

autodialer_disposition_1 = sqldf("SELECT * FROM autodialer_disposition where date(Listdate) >= '"+start_date+"' and date(Listdate) <= '"+end_date+"'")

autodialer_disposition_2 = sqldf("select AccountNumber,max(Listdate),CreditLimit from autodialer_disposition_1 group by AccountNumber")
autodialer_disposition_2.rename(columns={'AccountNumber':'acc_num'}, inplace=True)


autodialer_disposition_3= pd.merge(df1,autodialer_disposition_2[['acc_num','CreditLimit']],on=['acc_num'], how='left' )


autodialer_disposition_3.to_csv("/home/anjali/Anjali/BACKUP/Mobiloans/Auto_dialer_yessio/kpi_file_04mar_to_31mar_creditlimit.csv",sep=',',index=False)

###################################################################################


data2=pd.read_csv(r"/home/anjali/Anjali/BACKUP/Mobiloans/paid_list_march2018.csv",sep=',')
data2.rename(columns={'accountnumber':'acc_num','Sum - actual_payment':'actual_payment'}, inplace=True)
data2[['acc_num']] = data2[['acc_num']].apply(pd.to_numeric, errors='coerce')

acc_paid_list =pd.merge(df,data2[['acc_num','actual_payment']],on='acc_num', how='left' )

acc_paid_list.to_csv("/home/anjali/Anjali/BACKUP/Mobiloans/Auto_dialer_yessio/kpi_file_04mar_to_31mar_paid.csv",sep=',',index=False)

###################################################################################################################

ActionCode = pd.read_sql("select distinct(ActionCodeDescription),count(ActionCodeDescription) as count from mbl_auto_dispositions where date(Listdate) >= '"+start_date+"' and date(Listdate) <= '"+end_date+"' group by ActionCodeDescription",connection)

ActionCode.to_csv("/home/anjali/Anjali/BACKUP/Mobiloans/Auto_dialer_yessio/ActionCodeDescription_count.csv",sep=',',index=False)

#####################################################################################
diaplayname=sqldf("SELECT DisplayUserName,SUM(HoldDurationSeconds) FROM data where CallDirection = 'Outbound' group by DisplayUserName")

diaplayname.to_csv("/home/anjali/Anjali/BACKUP/Mobiloans/Auto_dialer_yessio/diaplayname_with_totalofholdtime.csv",sep=',',index=False)

#######################################################################################

data5 = sqldf("select CallDirection,count(CallDurationSeconds),LocalName from data where CallDurationSeconds >= 50 and CallDirection = 'Outbound' and date(ConnectedDate) >= '2018-03-04'  and date(ConnectedDate) <= '2018-03-31' group by LocalName")

data5.to_csv("/home/anjali/Anjali/BACKUP/Mobiloans/Auto_dialer_yessio/call_duration_eqandgrt50.csv",sep=',',index=False)

#######################################################################################

unique_acc_called = sqldf("select DisplayUserName,count(acc_num) as count_accnum,acc_num from df group by DisplayUserName,acc_num ")

#data2=pd.read_csv(r"/home/anjali/Mobiloans/Paid_List-Feb.csv",sep=',')
#data2.rename(columns={'accountnumber':'acc_num'}, inplace=True)

unique_acc_called_paidlist =pd.merge(data2,unique_acc_called,on='acc_num', how='left' )

unique_acc_called_paidlist.to_csv("/home/anjali/Anjali/BACKUP/Mobiloans/Auto_dialer_yessio/unique_acc_called_paidlist.csv",sep=',',index=False)

#############################################################################################

autodialer_disposition_1.rename(columns={'AccountNumber':'acc_num'}, inplace=True)
autodialer_disposition_5 = sqldf("select distinct(acc_num),ActionCodeDescription from autodialer_disposition_1 group by acc_num")

action_code_paid =pd.merge(data2,autodialer_disposition_5,on='acc_num', how='left' )

actioncode_paid = sqldf("select acc_num,sum(actual_payment),ActionCodeDescription from action_code_paid group by ActionCodeDescription,acc_num")

actioncode_paid.to_csv("/home/anjali/Anjali/BACKUP/Mobiloans/Auto_dialer_yessio/actioncode_paid_list.csv",sep=',',index=False)
