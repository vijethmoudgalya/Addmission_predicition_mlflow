import pandas as pd

class data_getter:
    def __init__(self):
            pass
            #self.training_file='Admission_Prediction.csv'
            #self.file_object=file_object
            #self.logger_object=logger_object
    
    def data_get():
                #self.logger_object.log(self.file_object,'Entered the data_get method of data_getter class')
        try:
            data = pd.read_csv('Admission_Prediction.csv')
                    #self.logger_object.log(self.file_object,'Data Load Successful.Exiting the data_get method of the data_getter class')
            return data
        except Exception as e:
                    #self.logger_object.log(self.file_object,'Exception occurred in data_get method of data_getter class, Exception :'+str(e))
            print(e)
                    #self.logger_object.log(self.file_object,'Data Load Unsuccessful.Exited the data_get method of the Data_Getter class')
            raise Exception()
