from abc import ABC,abstractmethod

from sklearn.model_selection import train_test_split

import pandas as pd

import sys

from math import sqrt

import numpy as np

from sklearn.metrics import mean_absolute_error,mean_squared_error



class Modelling(ABC):

    def __init__(self,df,forecastMessure):

        if isinstance(df,pd.DataFrame):

            self.df = df

        else:

            print('please pass a DataFrame')

            sys.exit()

        self.forecastMessure = forecastMessure

        

    def trainTestSplit(self,data,testSize,trainSize,rebuild=False):

        totalLength=data.shape[0]

        testLength=round(totalLength*testSize)

        trainLength = round(totalLength*trainSize)

        if rebuild==True:

            train = data[testLength:round(totalLength)]

        if rebuild==False:

            train = data[0:round(trainLength)]

        test = data[round(trainLength):]

        return train,test

    

    @abstractmethod

    def fit(self):

        pass

    

    @abstractmethod

    def forecast(self):

        pass

    
    def accuracy(self,y_act,y_pred,WStRMSEOpt,WMAPEOpt):

	    RMSE = sqrt(mean_squared_error(yact,y_pred))

	    MAPE=abs((yact-y_pred)/yact).mean()

	    MAE=mean_absolute_error(yact,y_pred)

	    SD_act=np.std(yact)

	    SD_forecast=np.std(y_pred)

	    SD_RMSE=RMSE/SD_act

	    SD_Ratio=SD_forecast/SD_act

	    Total_err=(WStRMSEOpt*SD_RMSE)+(WMAPEOpt*MAPE)

	    return RMSE,MAPE,MAE,SD_act,SD_forecast,SD_RMSE,SD_Ratio,Total_err

    

    def save_model (self,opt_model,Model_Id):

	    with open(Model_Id, 'wb') as file:  
            
             pickle.dump(opt_model, file)

	    print("optimised" + "_" + "_"+"model saved in " + os.getcwd(),"//",Model_Id)



    def CI(self,model_data,nxt_Date,forecastMessure):

	    act=model_data[forecastMessure]

	    Fcv=nxt_Date["Forecast"]

	    CI95=1.96

	    CI95Limit=CI95*((np.std(act))/ sqrt(len(act)))

	    nxt_Date["ForecastLowerLimit"]=nxt_Date["Forecast"]-CI95Limit

	    nxt_Date["ForecastUpperLimit"]=nxt_Date["Forecast"]+CI95Limit

	    return nxt_Date

    

    def load_model(self,Model_Id):

	    with open(Model_Id, 'rb') as file:  

             pickle_model = pickle.load(file)

	    return pickle_model

    

    def final_Result(self,Impute_data,trainset,Testdata,fd_val,forecastMessure,forecast_day,Time_Range,product,modeltype):

	    raw_data_fore=Impute_data[["datetime","item_name",forecastMessure]]

	    asi_na= pd.DataFrame([np.repeat(np.nan, [len(trainset)], axis=0)]).T

	    Testdata.reset_index(drop=True,inplace=True)

	    fore_val=pd.DataFrame([Testdata["pred"]]).T  

	    raw=pd.concat([asi_na,fore_val],axis=0,ignore_index=True)

	    raw_data_fore['Forecast']=raw["pred"]

	    raw_data_fore["Error"]=round(raw_data_fore[forecastMessure]-raw_data_fore["Forecast"],2)

	    raw_data_fore["per_Error"]=round(raw_data_fore["Error"]/raw_data_fore[forecastMessure],2)

	    raw_data_fore["sample"]="Model"

	    index1 = raw_data_fore['Forecast'].index[raw_data_fore['Forecast'].apply(np.isnan)]

	    raw_data_fore["sample"][index1.values] = np.nan

	    model_data=raw_data_fore[raw_data_fore["sample"]=="Model"]

	    dates=eval('[result for result in dataPreparation.perdelta(max(model_data["datetime"]), max(model_data["datetime"])+timedelta(days=(forecast_day+1)), timedelta('+Time_Range+'=1))]')

	    nxt_date=pd.DataFrame(dates)

	    nxt_date.reset_index(drop=True,inplace=True)

	    nxt_date["item_name"]=product

	    nxt_date["Forecast"]=round(pd.DataFrame(fd_val),2) 

	    nxt_date.columns=["datetime","item_name","Forecast"]

        #nxt_date["datetime"]=nxt_date["datetime"].dt.date

	    CI_limit=self.CI(model_data,nxt_date,forecastMessure)

	    nxt_date["ForecastLowerLimit"]=round(CI_limit.ForecastLowerLimit,2)

	    nxt_date["ForecastUpperLimit"]=round(CI_limit.ForecastUpperLimit,2)

	    nxt_date["sample"]="Forecast"

	    raw_data_pred_res=pd.concat([raw_data_fore,nxt_date],axis=0,ignore_index=True)    

	    raw_data_pred_res["model_type"]=model_type

	    raw_data_pred_res=raw_data_pred_res[["datetime","item_name",forecastMessure,"Forecast","ForecastLowerLimit","ForecastUpperLimit","Error","per_Error","sample","model_type"]]

	    return raw_data_pred_res
    
    
    
    
    
    



