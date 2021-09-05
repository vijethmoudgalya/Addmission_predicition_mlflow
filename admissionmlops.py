import warnings
from confuse.templates import REQUIRED
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge,Lasso,RidgeCV,LassoCV,ElasticNet,ElasticNetCV,LinearRegression
import statsmodels.api as sm
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse
import logging

logging.basicConfig(filename='logging.log',level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    np.random.seed(40)
    try:
        file_name = 'admission.csv'
        data = pd.read_csv(file_name)
        data
    except Exception as e:
        logger.exception(
            "Unable to Load CSV,Error: %s", e
        )

    data = pd.read_csv('Admission_Prediction.csv')
    # impute missing values
    data['GRE Score'] = data['GRE Score'].fillna(data['GRE Score'].mean())
    data['TOEFL Score'] = data['TOEFL Score'].fillna(data['TOEFL Score'].mean())
    data['University Rating'] = data['University Rating'].fillna(data['University Rating'].mean())

# delete the serial no column
    data.drop(columns=['Serial No.'],inplace=True)

    
    train, test = train_test_split(data)

    # The predicted column is "Chance of Admit" which is a scalar from [3, 9]
    train_x = train.drop(["Chance of Admit"], axis=1)
    test_x = test.drop(["Chance of Admit"], axis=1)
    train_y = train[["Chance of Admit"]]
    test_y = test[["Chance of Admit"]]


    
    with mlflow.start_run():
        lr  = LinearRegression()
        lr.fit(train_x, train_y)

        prediction = lr.predict(test_x)
        (rmse,mae,r2) = eval_metrics(test_y,prediction)
        print("LinearRegression model")
        print("RMSE %s" %rmse)
        print("MAE %s" %mae)
        print("r2 %s" %r2)

        mlflow.log_param("intercept", lr.intercept_)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(lr, "model", registered_model_name="Linear Regression model")
        else:
            mlflow.sklearn.log_model(lr,"model")

