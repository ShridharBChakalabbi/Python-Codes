# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 11:11:30 2018

@author: Sridhar
"""
import os 
import pandas as pd
import cenpy as cen
import pysal
import csv

datasets = list(cen.explorer.available(verbose=True).items())
pd.DataFrame(datasets).head()
dataset = '2012acs1'
cen.explorer.explain(dataset)
con = cen.base.Connection(dataset)
con

print(type(con))
print(type(con.geographies))
print(con.geographies.keys())
con.geographies['fips'].head()
g_unit = 'county:*'
g_filter = {'state':'8'}







var = con.variables
print('Number of variables in', dataset, ':', len(var))
con.variables.head()
cols = con.varslike('B01001A_')
cols.extend(['NAME', 'GEOID'])
data = con.query(cols, geo_unit=g_unit, geo_filter=g_filter)
data.index = data.NAME
data.ix[:5, -5:]

#==============================================================================
# Topologically Integrated Geographic Encoding and Referencing (TIGER) data
# The Census TIGER API provides geomotries for desired geographic regions. For instance, perhaps we want to have additional information on each county such as area.
# 
#==============================================================================

cen.tiger.available()
con.set_mapservice('tigerWMS_ACS2013')
con.mapservice.layers
geodata = con.mapservice.query(layer=84, where='STATE=8')
geodata.ix[:5, :5]
newdata = pd.merge(data, geodata, left_on='county', right_on='COUNTY')
newdata.ix[:5, -5:]
newdata.to_csv("newdata.csv")
os.getcwd()
