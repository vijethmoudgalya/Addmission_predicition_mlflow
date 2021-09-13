import pandas as pd
import numpy as np
from sklearn.preprocessing  import StandardScaler

class preprocessor:
    def __init__(self):
        pass
        #self.file_object=file_object
        #self.logger_object = logger_object



    def remove_columns(self,data,columns):
        #self.logger_object(self.file_object,'Entered the remove_columns method of preprocessor class')
        self.data = data
        self.columns = columns

        try:
            self.useful_data = self.data.drop(columns = self.columns,axis=1)
            #self.logger_object.log(self.file_object,'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            return self.useful_data
        except Exception as e:
            print(e)
        raise Exception()


    def null_imputer(self,data):
        try:
            self.data['GRE Score'] = self.data['GRE Score'].fillna(self.data['GRE Score'].mean())
            self.data['TOEFL Score'] = self.data['TOEFL Score'].fillna(self.data['TOEFL Score'].mean())
            self.data['University Rating'] = self.data['University Rating'].fillna(self.data['University Rating'].mean())
            #self.logger_object.log(self.file_object,'null values imputer Successful.Exited the null_imputer method of the Preprocessor class')
        except Exception as e:
            print(e)


    def separate_label_feature(self, data, label_column_name):
        try:
            self.x = data.drop(labels = label_column_name,axis=1)
            self.y = data[label_column_name]

            return self.x,self.y
        except Exception as e:
            print(e)
            raise Exception()

    def scale_numerical_columns(self,data,x):
        try:
            self.scalar = StandardScaler()
            self.scaled_data = self.scalar.fit_transform(self.x)
            return self.scaled_data
        except Exception as e:
            print(e)
            raise Exception()
            
