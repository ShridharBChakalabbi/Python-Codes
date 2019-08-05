import os
import pandas as pd
import numpy as np


data = pd.read_csv("C:/Users/Sridhar/twitter_profile.csv", encoding='cp1252')

matched_data = pd.merge(data,mobiloanspii2, how='left', on=['name'])
mobiloanspii2['name'] = mobiloanspii2['AES_DECRYPT(FirstName,123654)']+' '+mobiloanspii2['AES_DECRYPT(LastName,123654)']


import csv
#csv.writer("u1.csv")
matched_data.to_csv('matched_data.csv')
os.getcwd()
