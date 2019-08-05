#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 10:24:03 2019

@author: shridhar
"""

import pandas as pd

Final = pd.read_csv("/home/shridhar/Downloads/Month5data.csv")

Final.columns
del Final['Unnamed: 0']

Final['Profit'] = Final.PrdNetAmount - Final.PrdGrossAmount


# =============================================================================
# MonthData_5 = Final.groupby(['AuthDate','PrdId','SchId','SchDsc'])['BaseQty','PrdNetAmount','PrdGrossAmount','Budget','Profit'].sum()
# MonthData_5=pd.DataFrame(MonthData_5)
# MonthData_5.reset_index(inplace=True)
# MonthData_5.shape
# 
# =============================================================================

UP1 = Final.PrdNetAmount/Final.BaseQty
UP2 = Final.PrdGrossAmount/Final.BaseQty
Final['PrdNetAmount_Per_BaseQty'] = UP1
UP2

Final1=Final.groupby(['SchId','PrdId','SchDsc'])['PrdGrossAmount','BaseQty','Budget','Profit','PrdNetAmount_Per_BaseQty'].sum()
Final1.reset_index(inplace=True)

from pulp import *
prob = LpProblem("Product Problem",LpMinimize)

# Read the first few rows dataset in a Pandas DataFrame
# Create a list of the product desc items
prod_items = list(Final1['SchDsc'])

# Create a dictinary of costs for all food items
costs = dict(zip(prod_items,Final1['PrdNetAmount_Per_BaseQty']))  

# Create a dictionary of calories for all food items
profits = dict(zip(prod_items,Final1['Profit']))

# Create a dictionary of total fat for all food items
BaseQty = dict(zip(prod_items,Final1['BaseQty']))

# Create a dictionary of carbohydrates for all food items
Budget = dict(zip(prod_items,Final1['Budget']))

Prod_vars = LpVariable.dicts("prod",prod_items,lowBound=0,cat='Integer')
prob += lpSum([costs[i]*Prod_vars[i] for i in prod_items])


prob += lpSum([BaseQty[f] * Prod_vars[f] for f in prod_items]) >= float(input("Minimum_BaseQty: "))
prob += lpSum([BaseQty[f] * Prod_vars[f] for f in prod_items]) <= float(input("Maximum_BaseQty: "))

# Budget
prob += lpSum([Budget[f] * Prod_vars[f] for f in prod_items]) >= float(input("Minimum_Budget: ")),"BudgetMinimum"
prob += lpSum([Budget[f] * Prod_vars[f] for f in prod_items]) <= float(input("Maximum_Budget: ")),"BudgetMaximum"

# profits
prob += lpSum([profits[f] * Prod_vars[f] for f in prod_items]) >= float(input("Minimum_profits: ")),"profitsMinimum"
prob += lpSum([profits[f] * Prod_vars[f] for f in prod_items]) <= float(input("Maximum_profits: ")),"profitsMaximum"

prob
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

prob.variables()


for v in prob.variables():
    if v.varValue>=0:
        print(v.name, "=", v.varValue)
        
        
obj = value(prob.objective)
print("The total optimised profit is in: Rs{}".format(round(obj,2)))
