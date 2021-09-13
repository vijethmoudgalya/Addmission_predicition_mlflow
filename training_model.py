import warnings
from confuse.templates import REQUIRED
from evaluation import  eval
from dataloader import data_getter
from data_preprocessing import preprocessor
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge,Lasso,RidgeCV,LassoCV,ElasticNet,ElasticNetCV,LinearRegression
import statsmodels.api as sm
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse

class trainmodel:
    def __init__(self):
        pass
    def trainingModel(self):
        try:
            #Getting data
            data = data_getter.data_get()
            
            #remove unwanted columns
            prepross = preprocessor()
            data_preprocess = prepross.remove_columns(data,['Serial No.'])
             
             #Imputing null values
            data_preprocess =prepross.null_imputer(data)

            # create separate features and labels
            x,y = prepross.separate_label_feature(data,label_column_name='Chance of Admit')

            # scale the data
            scaled_data = prepross.scale_numerical_columns(data,x)

            train_x,test_x,train_y,test_y= train_test_split (scaled_data,y,random_state=1,test_size=0.25)

            encv = ElasticNetCV(cv = 10)
            encv.fit(train_x,train_y)

            with mlflow.start_run():
                elr  = ElasticNet(alpha = encv.alpha_,l1_ratio=encv.l1_ratio)
                elr.fit(train_x, train_y)
                prediction = elr.predict(test_x)
                evals = eval()
                (rmse,mae,r2) = evals.eval_metrics(test_y,prediction)


                print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (encv.alpha_, encv.l1_ratio))
                print("  RMSE: %s" % rmse)
                print("  MAE: %s" % mae)
                print("  R2: %s" % r2)


                mlflow.log_param("alpha", encv.alpha_)
                mlflow.log_param("l1_ratio", encv.l1_ratio)
                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)

                tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

                # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(elr, "model", registered_model_name="ElasticnetAdmissionModel")
                else:
                    mlflow.sklearn.log_model(elr,"model")
        except  Exception as e:
            print(e)
trainmodelobj = trainmodel()
trainmodelobj.trainingModel()
