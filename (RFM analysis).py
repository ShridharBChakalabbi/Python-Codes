#Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

#Data preparation
df=pd.read_excel("anu data.xlsx",sheetname=0)
df['Rate'] = np.where(df['Rate'] == 111899.0,11.0,df['Rate'])
df['Qty'] = np.where(df['Qty'] == 111899.0,11.0,df['Qty'])
df['Amount'] = np.where(((df['Item Name'] == 'COVER POCKET') & (df['Amount'] == 111899.0)),1.0,df['Amount'])
df['Amount'] = np.where(df['Amount'] == 111899.0,11.0,df['Amount'])
df.sort_values(['Amount'],ascending=False)
df['Calculated Amount'] = df['Rate']*df['Qty']
df['date time']=df['date time'].dt.date

#RFM analysis
rfm = pd.DataFrame()
rfm['Item Name'],rfm['Max of Date'],rfm['F'],rfm['M'] = zip(*df.groupby('Item Name',as_index=False)['date time','Qty','Calculated Amount'].agg({'date time':'max','Qty':'sum','Calculated Amount':'sum'}).values)
rfm.insert(loc=2,column='R',value=((df['date time'].max()-rfm['Max of Date']).dt.days+1))
r_t=np.percentile(rfm['R'],[20,40,60,80,100])
f_t=np.percentile(rfm['F'],[20,40,60,80,100])
m_t=np.percentile(rfm['M'],[20,40,60,80,100])
rfm['R points']=np.where(rfm['R']<=r_t[0],5,np.where(rfm['R']<=r_t[1],4,np.where(rfm['R']<=r_t[2],3,np.where(rfm['R']<=r_t[3],2,1))))
rfm['F points']=np.where(rfm['F']<=f_t[0],1,np.where(rfm['F']<=f_t[1],2,np.where(rfm['F']<=f_t[2],3,np.where(rfm['F']<=f_t[3],4,5))))
rfm['M points']=np.where(rfm['M']<=m_t[0],1,np.where(rfm['M']<=m_t[1],2,np.where(rfm['M']<=m_t[2],3,np.where(rfm['M']<=m_t[3],4,5))))
rfm['RFM score']=(rfm['R points'].map(str)+rfm['F points'].map(str)+rfm['M points'].map(str)).map(int)
rfm.sort_values(['RFM score'],ascending=False,inplace=True)
ax = plt.subplot(111)
x=np.arange(1,6)
ax.bar(x-0.2,rfm.groupby('R points')['R points'].count(),width=0.2)
ax.bar(x,rfm.groupby('F points')['F points'].count(),width=0.2)
ax.bar(x+0.2,rfm.groupby('M points')['M points'].count(),width=0.2)
plt.show()

