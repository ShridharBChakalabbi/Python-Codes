from selenium import webdriver

import time

import csv

import pandas as pd

from selenium.webdriver.common.action_chains import ActionChains 

from selenium.webdriver.common.keys import Keys

num="video2"

#driver = webdriver.Firefox()

path_to_chromedriver = 'C:\\Users\\Admin\\Music\\chromedriver'           
 # change path as needed

driver = webdriver.Chrome(executable_path = path_to_chromedriver)

driver.get("https://speech-to-text-demo.ng.bluemix.net/")

action = ActionChains(driver)


def my_func():
  
	userID = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/button[2]').click()

my_func()



def my_fun():    
	
	val = driver.find_element_by_xpath('//*[@id="root"]/div/div[6]/div')    
	
	val1= (val.text)    
	
	vid_text = pd.DataFrame([val1])
   	
	csv_file="extracted_text"+ num+".csv"
   	
	vid_text.to_csv(csv_file,encoding='utf-8')

my_fun()
