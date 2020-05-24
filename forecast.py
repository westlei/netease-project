import numpy as np
from PyQt5.QtWidgets import QMessageBox
import xgboost as xgb
from sklearn.model_selection import train_test_split
from snownlp import SnowNLP

def course_forecasting(data, x_t, steps):
    if steps == 0:
        QMessageBox.information(None, '提示', '正在训练预测模型，请稍候！', QMessageBox.Yes)
        try:
            x = []
            for i in range(len(data[:, 1])):
                x.append([SnowNLP(data[(i, 1)]).sentiments, SnowNLP(data[(i, 2)]).sentiments, SnowNLP(data[(i, 4)]).sentiments, float(data[(i, 6)]), float(data[(i, 7)])])

            y1 = []
            y2 = []
            for i in range(len(data[:, 1])):
                y1.append(float(data[(i, 8)]))
                y2.append(float(data[(i, 9)]))

            model1 = xgb.XGBRegressor(max_depth=5, learning_rate=0.1, n_estimators=160, silent=False)
            model1.fit((np.array(x)), (np.array(y1)), verbose=True)
            model2 = xgb.XGBRegressor(max_depth=5, learning_rate=0.1, n_estimators=160, silent=False)
            model2.fit((np.array(x)), (np.array(y2)), verbose=True)
            model1.save_model('./prediction_model/learners.model')
            model2.save_model('./prediction_model/star.model')
        except:
            pass
    QMessageBox.information(None, '提示', '模型训练完毕！', QMessageBox.Yes)
    model1 = xgb.XGBRegressor()
    model2 = xgb.XGBRegressor()
    model1.load_model('./prediction_model/learners.model')
    model2.load_model('./prediction_model/star.model')
    x1 = []
    x1.append([SnowNLP(x_t[0]).sentiments, SnowNLP(x_t[1]).sentiments, SnowNLP(x_t[2]).sentiments, float(x_t[3]), float(x_t[4])])
    return (
     model1.predict(np.array(x1))[0], model1.predict(np.array(x1))[0] * float(x_t[4]), 5.0 if model2.predict(np.array(x1))[0] > 5 else model2.predict(np.array(x1))[0])

