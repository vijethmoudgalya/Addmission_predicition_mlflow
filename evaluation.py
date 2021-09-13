from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
import numpy as np

class eval:

    def __init__(self):
        pass
        #self.file_object=file_object
        #self.logger_object = logger_object

    def eval_metrics(self,actual,pred):

            #self.logger_object.log(self.file_object,'Entered the Evaluation FUnction')
            self.actual = actual
            self.pred = pred

            try:
                rmse = np.sqrt(mean_squared_error(actual, pred))
                mae = mean_absolute_error(actual, pred)
                r2 = r2_score(actual, pred)
                return rmse, mae, r2
            except  Exception as e:
                #self.logger_object.log(self.file_object,'Exception occurred in eval_metrics method eval class. Exception message:'+str(e))
                print(e)