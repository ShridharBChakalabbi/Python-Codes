#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:28:31 2019

@author: shridhar
"""
import numpy as np
import pandas as pd

train=pd.read_excel("/home/shridhar/Desktop/Participants_Data_Final/Data_Train.xlsx")
loatlong=pd.read_csv("/home/shridhar/Desktop/IN.csv")
loatlong.rename(columns={'place_name':'LOCALITY','admin_name1':'CITY'},inplace=True)

train1=train.copy()

train['VOTES1']=train['VOTES'].str.split(" ").str[0]
train['TITLE1']=train['TITLE'].str.split(",").str[0]
train['TITLE2']=train['TITLE'].str.split(",").str[1]

train['singleCUISINE']=train['CUISINES'].str.split(",").str[0]
train['DoubleCUISINES']=train['CUISINES'].str.split(",").str[1]
train['MultipleCUISINES']=train['CUISINES'].str.split(",").str[2]
#train['CUISINES4']=train['CUISINES'].str.split(",").str[3]
#train['CUISINES5']=train['CUISINES'].str.split(",").str[4]
#train['CUISINES6']=train['CUISINES'].str.split(",").str[5]
#train['CUISINES7']=train['CUISINES'].str.split(",").str[6]
#train['CUISINES8']=train['CUISINES'].str.split(",").str[7]

train1.isnull().sum()
train['City'].value_counts(dropna = False)

train['CUISINES_1']=np.where(train['CUISINES1']==0,0,1)
train['singleCUISINE'].fillna(0, inplace=True)
train['DoubleCUISINES'].fillna(0, inplace=True)
train['MultipleCUISINES'].fillna(0, inplace=True)

train['CUISINES4'].fillna(0, inplace=True)
train['CUISINES5'].fillna(0, inplace=True)
train['CUISINES6'].fillna(0, inplace=True)
train['CUISINES7'].fillna(0, inplace=True)
train['CUISINES8'].fillna(0, inplace=True)


train['VOTES1'].fillna(0, inplace=True)
train['TITLE1'].fillna(0, inplace=True)
train['TITLE2'].fillna(0, inplace=True)
train['singleCUISINE']=np.where(train['singleCUISINE']==0,0,1)
train['DoubleCUISINES']=np.where(train['DoubleCUISINES']==0,0,1)
train['MultipleCUISINES']=np.where(train['MultipleCUISINES']==0,0,1)
train['TITLE1']=np.where(train['TITLE1']==0,0,1)
train['TITLE2']=np.where(train['TITLE2']==0,0,1)
train['RATING']=np.where(train['RATING']=='NEW',0,np.where(train['RATING']=='-',0,train['RATING']))
train['6hours']=train['TIME'].str.split(",").str[0]
train['morethan6hours']=train['TIME'].str.split(",").str[1]
train['6hours'].fillna(0, inplace=True)
train['morethan6hours'].fillna(0, inplace=True)

train['6hours']=np.where(train['6hours']==0,0,1)
train['morethan6hours']=np.where(train['morethan6hours']==0,0,1)

aa=pd.read_csv("/home/shridhar/Downloads/out.csv")
aa.rename(columns={'AC':'LOCALITY','District':'CITY'},inplace=True)

full=pd.merge(train1,aa,on='period',how ='inner')
full.isnull().sum()
full1=full.copy()
full1.set_index(['TITLE'],inplace=True)
full1=full1.drop(['None'])
full1.pop('TITLE')
full1.reset_index(inplace=True)
full1['CITY'].unique()
train['CITY'].unique()
###########################################################

# =============================================================================
# aa['period'] = aa[['District', 'AC','PSName']].apply(''.join, axis=1)
# 
# train1.columns
# 
# train1['period'] = train1['CITY'] +' '+ train1['LOCALITY']
# aa['period']=aa['District']+' '+aa['PSName']+' '+aa['AC']
# len(aa['PSName'].unique())
# len(train['CITY'].unique())
# 
# aa1=aa[aa['period'].str.contains("BANGALORE")]
# aa['period1']=aa['PSName'].str.split(" ").str[0]
# aa['period2']=aa['PSName'].str.split(" ").str[1]
# 
# del aa['period']
# del aa['period1']
# del aa['period2']
# del train1['period']
# 
# =============================================================================


test=pd.read_excel("/home/shridhar/Desktop/Participants_Data_Final/Data_Test.xlsx")

test['VOTES1']=test['VOTES'].str.split(" ").str[0]
test['TITLE1']=test['TITLE'].str.split(",").str[0]
test['TITLE2']=test['TITLE'].str.split(",").str[1]

test['singleCUISINE']=test['CUISINES'].str.split(",").str[0]
test['DoubleCUISINES']=test['CUISINES'].str.split(",").str[1]
test['MultipleCUISINES']=test['CUISINES'].str.split(",").str[2]
test['CUISINES4']=test['CUISINES'].str.split(",").str[3]
test['CUISINES5']=test['CUISINES'].str.split(",").str[4]
test['CUISINES6']=test['CUISINES'].str.split(",").str[5]
test['CUISINES7']=test['CUISINES'].str.split(",").str[6]
test['CUISINES8']=test['CUISINES'].str.split(",").str[7]
test['6hours']=test['TIME'].str.split(",").str[0]
test['morethan6hours']=test['TIME'].str.split(",").str[1]
test['6hours'].fillna(0, inplace=True)
test['morethan6hours'].fillna(0, inplace=True)

test['6hours']=np.where(test['6hours']==0,0,1)
test['morethan6hours']=np.where(test['morethan6hours']==0,0,1)

test['VOTES1'].fillna(0, inplace=True)
test['TITLE1'].fillna(0, inplace=True)
test['TITLE2'].fillna(0, inplace=True)
test['singleCUISINE']=np.where(test['singleCUISINE']==0,0,1)
test['DoubleCUISINES']=np.where(test['DoubleCUISINES']==0,0,1)
test['MultipleCUISINES']=np.where(test['MultipleCUISINES']==0,0,1)
test['TITLE1']=np.where(test['TITLE1']==0,0,1)
test['TITLE2']=np.where(test['TITLE2']==0,0,1)
test['RATING']=np.where(test['RATING']=='NEW',0,np.where(test['RATING']=='-',0,test['RATING']))

train.to_csv("/home/shridhar/Desktop/train.csv")
test.to_csv("/home/shridhar/Desktop/test.csv")
