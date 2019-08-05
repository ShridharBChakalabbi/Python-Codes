
import pandas as pd
import pymysql.cursors
from datetime import date, timedelta
from functools import partial
import numpy as np
import re
import datetime
import os
# Connect to the database
connection = pymysql.connect(host='54.70.109.246',user='mobiloans',password='ambertagmobiloans',db='mobiloans_pii',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

auto_dialer = pd.read_sql("SELECT * FROM mobiloans.mobiloans_auto_dialer",db)

mobilaons_pii =pd.read_sql("select AES_DECRYPT(FirstName,123654), AES_DECRYPT(LastName,123654),AES_DECRYPT(State,123654),AES_DECRYPT(PostalCode,123654),AES_DECRYPT(HomePhone,123654),AES_DECRYPT(CellPhone,123654),AES_DECRYPT(WorkPhone,123654),AES_DECRYPT(City,123654) from mbl_customer_pii",connection)
mobiloanspii = mobilaons_pii

s = pd.Series(mobilaons_pii)
writer = pd.ExcelWriter('mobilaons_pii.xlsx')
mobilaons_pii.to_excel(writer,'Sheet1')    
writer.save()    
os.getcwd() 

import csv
csv.writer('mobilaons_pii.csv')
mobilaons_pii.to_csv('mobilaons_pii.csv')

#==============================================================================
# mobiloanspii = mobiloanspii.str.replace("/b''"," '")
# 
# 
# mobiloanspii = mobiloanspii.replace("b'", np.nan)
# mobiloanspii = mobiloanspii.replace("b'",'')
# mobiloanspii = mobiloanspii.drop(b'')
# mobiloanspii.values = pd.core.frame.DataFrame.replace(mobiloanspii.values.astype(str), 'b''', '')
mobiloanspii = mobiloanspii.astype(str).replace('b','',regex=True)
mobiloanspii2 = mobiloanspii.astype(str).replace('', '',regex = True)
#mobiloanspii2 = mobiloanspii.replace("'", '')

#n = mobiloanspii2.ix[:,mobiloanspii2.dtypes==object].apply(lambda s:s.str.replace('"', ''))
#==============================================================================
# mobiloanspii2['AES_DECRYPT(FirstName,123654)'] = mobiloanspii2['AES_DECRYPT(FirstName,123654)'].str.replace(r"[\"\',]", '')
# mobiloanspii2['AES_DECRYPT(LastName,123654)'] = mobiloanspii2['AES_DECRYPT(LastName,123654)'].str.replace(r"[\"\',]", '')
# mobiloanspii2['AES_DECRYPT(State,123654)'] = mobiloanspii2['AES_DECRYPT(State,123654)'].str.replace(r"[\"\',]", '')
# mobiloanspii2['AES_DECRYPT(LastName,123654)'] = mobiloanspii2['AES_DECRYPT(LastName,123654)'].str.replace(r"[\"\',]", '')
#==============================================================================

for i, col in enumerate(mobiloanspii2.columns): 
        mobiloanspii2.iloc[:, i] = mobiloanspii2.iloc[:, i].str.replace(r"[\"\',]", '')


mobiloanspii3 = mobiloanspii2.iloc[:,0:2]

import tweepy
consumer_key = '5dBlAKQreMfde02aWkTwvj3cv'
consumer_secret = '9s17OqhWmvdhJg50V9H9BljOMzkGycGPtYjiXqFooUbVlnrMLl'
access_token = '1003877817719767041-b57g3SFSPcuhFq0uXjtLng56ZZIezC'
access_token_secret = 'nWv4msdIinp8tbMkQjLN1BxHXQSfeFFFuQgCA3fcUJV2C'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


user = api.get_user(screen_name = 'mobiloanspii3')
user.id


user={}
for x in range(1,10):
        user["mobiloanspii3".format(x)]= api.get_user(screen_name = "")
#==============================================================================


#mobiloanspii = mobiloanspii.astype(str).replace('','',regex=True)
#mobiloanspii = mobiloanspii.replace('*','',regex=False,inplace=True)

#==============================================================================
# mobiloanspii = mobiloanspii.replace(r'b'',^\s*$',np.nan, regex=True)
# mobiloanspii['AES_DECRYPT(FirstName,123654)'] =mobiloanspii['AES_DECRYPT(FirstName,123654)'].map(lambda x: re.sub(r'\b+', '', x))
#  
# mobiloanspii = mobiloanspii.replace('"', '')
#  mobiloanspii = mobiloanspii.replace('\b +''','' )
# 
# mobiloanspii = mobiloanspii.remove("'")
# mobiloanspii = ''.join(mobiloanspii)
# 
#  mobiloanspii = mobiloanspii.replace("b''", "")
# 
#==============================================================================
#==============================================================================
# from Crypto.Cipher import AES
# from Crypto import Random
# 
# key = b'123654'
# iv = Random.new().read(AES.block_size)
# cipher = AES.new(key, AES.MODE_CFB, iv)
# msg = iv + cipher.encrypt(b'mobilaons_pii')
# 
# import pyAesCrypt
# bufferSize = 64 * 1024
# password = "123654"
# pyAesCrypt.decryptFile("mobilaons_pii", "mobilaons_pii1", password, bufferSize)
# 
# 
# 
# import seaborn as sns
# from subprocess import check_output
# print(check_output(['mobilaons_pii']).decode("utf8"))
#==============================================================================


n = mobiloanspii
for i, col in enumerate(n.columns): 
        n.iloc[:, i] = n.iloc[:, i].str.replace(r"[\"\',]", '')