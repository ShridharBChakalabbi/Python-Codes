#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:04:28 2019

@author: shridhar
"""

import datetime as dt
import pandas as pd
import numpy as np
#import matplotlib as plt

#Final = pd.read_csv("/home/shridhar/optimisation project/optimisation/Finaldata.csv")
Final=pd.read_csv("/home/shridhar/optimisation project/optimisation/Month5data.csv")
del Final['Unnamed: 0']
Final.columns
Final.info()
Final.dtypes
Final['AuthDate']=pd.to_datetime(Final['AuthDate'])
aa=Final['AuthDate'].value_counts()
Final['month'] = Final['AuthDate'].dt.month
bb=Final['month'].value_counts()
Final1=Final[Final['month']==1]
Final['Budget'].mean()
Final['Profit'] = Final.PrdNetAmount - Final.PrdGrossAmount
Final['Target']=np.where(Final['Budget']>=63652,'High','Low')

UP1 = Final.PrdNetAmount/Final.BaseQty
UP2 = Final.PrdGrossAmount/Final.BaseQty
Final['PrdGrossAmount/BaseQty'] = UP2
Final['PrdNetAmount/BaseQty'] = UP1


Final['Profit'] = Final['Profit'].abs()

####################### RFM Analysis #####################################

import warnings
warnings.filterwarnings('ignore')

temp=['Profit','PrdGrossAmount/BaseQty','PrdNetAmount/BaseQty','SchDsc', 'AuthDate', 'SchId','BaseQty','PrdGrossAmount']
RFM_data=Final[temp]
RFM_data.shape

RFM_data.head()

RFM_data['AuthDate'] = pd.to_datetime(RFM_data['AuthDate'])
RFM_data['AuthDate'].max()


########################## RFM TABLE #################################


##################### Create the RFM Table ########################### 

import datetime as dt
NOW = dt.datetime(2014,5,21)


RFM_table=RFM_data.groupby('SchDsc').agg({'AuthDate': lambda x: (NOW - x.max()).days, # Recency
                                                'SchDsc': lambda x: len(x.unique()), # Frequency
                                                'PrdNetAmount/BaseQty': lambda x: x.sum()})    # Monetary 

RFM_data['AuthDate'] = RFM_data['AuthDate'].astype(int)

RFM_table.rename(columns={'AuthDate': 'recency', 
                         'SchDsc': 'frequency',
                         'PrdNetAmount/BaseQty': 'monetary_value'}, inplace=True)

RFM_table.head()

quantiles = RFM_table.quantile(q=[0.25,0.5,0.75])
quantiles


# Converting quantiles to a dictionary, easier to use.
quantiles = quantiles.to_dict()
quantiles 


#################### RFM Segmentation ####################

RFM_Segment = RFM_table.copy()

# Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
def R_Class(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1
    
# Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
def FM_Class(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4


RFM_Segment['R_Quartile'] = RFM_Segment['recency'].apply(R_Class, args=('recency',quantiles,))
RFM_Segment['F_Quartile'] = RFM_Segment['frequency'].apply(FM_Class, args=('frequency',quantiles,))
RFM_Segment['M_Quartile'] = RFM_Segment['monetary_value'].apply(FM_Class, args=('monetary_value',quantiles,))

RFM_Segment['RFMClass'] = RFM_Segment.R_Quartile.map(str) \
                            + RFM_Segment.F_Quartile.map(str) \
                            + RFM_Segment.M_Quartile.map(str)






#What are the best products to invest? (BY RFMClass = 444)
RFM_Segment[RFM_Segment['RFMClass']=='444'].sort_values('monetary_value', ascending=False).head(5)                            


#Which products are at the verge of churning?
#Products which recency value is low

RFM_Segment[RFM_Segment['R_Quartile'] <= 2 ].sort_values('monetary_value', ascending=False).head(5)

#Which are products customers?
#products who's recency, frequency as well as monetary values are low 

RFM_Segment[RFM_Segment['RFMClass']=='111'].sort_values('recency',ascending=False).head(5)

#Which are your loyal products?
#products with high frequency value

RFM_Segment[RFM_Segment['F_Quartile'] >= 3 ].sort_values('monetary_value', ascending=False).head(5)
RFM_Segment.reset_index(level=0, inplace=True)

###############################  Linear Optimisation #######################

from pulp import *
prob = LpProblem("Product Problem",LpMinimize)

# Read the first few rows dataset in a Pandas DataFrame
# Create a list of the product desc items
prod_items = list(RFM_Segment['SchDsc'])

# Create a dictinary of costs for all food items
costs = dict(zip(prod_items,RFM_Segment['monetary_value']))  

# =============================================================================
# # Create a dictionary of calories for all food items
# Discount = dict(zip(prod_items,RFM_Segment['recency']))
# # Create a dictionary of total fat for all food items
# Discount = dict(zip(prod_items,RFM_Segment['recency']))
# =============================================================================
# 
# =============================================================================
# 
# 
# # Create a dictionary of total fat for all food items
# BaseQty = dict(zip(prod_items,Final['BaseQty']))
# 
# # Create a dictionary of carbohydrates for all food items
# Budget = dict(zip(prod_items,Final['Budget']))
# 
# =============================================================================
Prod_vars = LpVariable.dicts("prod",prod_items,lowBound=0,cat='Integer')
prob += lpSum([costs[i]*Prod_vars[i] for i in prod_items])


prob += lpSum([costs[f] * Prod_vars[f] for f in prod_items]) >= float(input("Minimum_Budget: "))
prob += lpSum([costs[f] * Prod_vars[f] for f in prod_items]) <= float(input("Maximum_Budget: "))
 
# =============================================================================
# # costs
# 
# prob += lpSum([costs[f] * Prod_vars[f] for f in prod_items]) >= float(input("Minimum_price: ")),"Minimum_price"
# prob += lpSum([costs[f] * Prod_vars[f] for f in prod_items]) <= float(input("Maximum_maximum: ")),"Maximum_Price"
# 
# =============================================================================
# =============================================================================
# # profits
# prob += lpSum([profits[f] * Prod_vars[f] for f in prod_items]) >= float(input("Minimum_profits: ")),"profitsMinimum"
# prob += lpSum([profits[f] * Prod_vars[f] for f in prod_items]) <= float(input("Maximum_profits: ")),"profitsMaximum"
# 
# =============================================================================
prob
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

prob.variables()


for v in prob.variables():
    if v.varValue>0:
        print(v.name, "=", v.varValue)



# =============================================================================
# The full solution contains all the variables including the ones with 
# zero weights. But to us, only those variables are interesting which have
#  non-zero coefficients i.e. which should be included in the optimal discounts
#  plan. So, we can scan through the problem variables and print out only 
#  if the variable quantity is positive.
# 
# =============================================================================

obj = value(prob.objective)
print("The total optimised profit is in: Rs{}".format(round(obj,2)))