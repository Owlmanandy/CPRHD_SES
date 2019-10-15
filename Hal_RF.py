import numpy as np
import time
import scipy.stats as stats
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.linear_model import LinearRegression
from scipy import stats
from sklearn.metrics import log_loss
import pickle
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
import matplotlib.pyplot as plt
from sklearn.metrics import (brier_score_loss, precision_score, recall_score,
                             f1_score)
<<<<<<< Updated upstream

data = pd.read_sas('/home/shared/cprhd/DATA_CPRHD_SES/wnv_2245new.sas7bdat') # In the Cook_Dupage Directory
=======
time_start = time.time()
data = pd.read_sas('/home/jallen17/Downloads/wnv_2245new.sas7bdat') # In the Cook_Dupage Directory
print("Data read in:", time.time() - time_start)

>>>>>>> Stashed changes

time_start = time.time()
x_selected = data[data.drop(columns=['wnvbinary','yrweeks','yrwksfid','yr_hexid','year']).columns[[7,8,9,10,16,17,20]]].values
y_selected = data['wnvbinary'].values
print("Data selected in:", time.time() - time_start)



time_start = time.time()
trainX_sel, testX_sel, trainY_sel, testY_sel = train_test_split(x_selected, y_selected, test_size = 0.2, shuffle = True) # CV
print("data split:", time.time() - time_start)


time_start = time.time()
model_RF_best_2 = RandomForestClassifier(n_estimators=1500,
                                 n_jobs = -1,
                                 max_features=None,
                                 max_depth=None,
                                 bootstrap=True,
                                 min_samples_leaf=2
                                 )
print("Classifier established:", time.time() - time_start)


time_start = time.time()
model_RF_best_2.fit(trainX_sel, trainY_sel)
print("model fit:", time.time() - time_start)


time_start = time.time()
param_grid = {
    'bootstrap': [True],
    'max_depth': [80, None],
    'max_features': ['sqrt', 4],
    'min_samples_leaf': [3, 5],
    'min_samples_split': [8, 12],
    'n_estimators': [500, 1000]
}
<<<<<<< Updated upstream
CV_model_RF_3 = GridSearchCV(model_RF_best_2, param_grid, scoring='neg_log_loss', cv=3)
=======


CV_model_RF_3 = GridSearchCV(model_RF_best_2, param_grid, scoring='neg_log_loss', cv=5)
print("CV model parameterized:", time.time() - time_start)

time_start = time.time()
>>>>>>> Stashed changes
CV_model_RF_3.fit(trainX_sel, trainY_sel)
print("CV model fit:", time.time() - time_start)


def model_RF_test(model_RF, dataX, dataY):
    print("Model performance")
    predict_data = model_RF.predict_proba(dataX)

    # Some stats
    print("Feature Importantce : ")
    print(model_RF.feature_importances_)
    print("Total number of WNV occurence in test set : " + str(len(dataY[dataY > 0])))

    print("Number of WNV occurence the model is able to capture in test set:" + str(
        dataY[np.where(predict_data[:, 1] > 0)].sum()))

    print("Log loss : " + str(log_loss(dataY, predict_data)))

    print(
        "This is to test the performance of random forest model, ideally, the logloss is low and also it is able to capture most of the WNV occurence")

    return None  # Check how many wnv it predicts

model_RF_test(CV_model_RF_3,testX_sel,testY_sel)

pickle.dump(CV_model_RF_3, open('RF_model', 'wb'))
