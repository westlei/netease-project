import os
import pandas as pd, numpy as np, datetime
from PyQt5.QtWidgets import QMessageBox
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

def data_classification(data, cate, name):
    sort = np.unique(cate[:, 0])
    lenth = len(cate[:, 0])
    namesort = []
    for i in range(0, len(data[:, 3])):
        for j in range(0, lenth):
            if data[:, 3][i] == cate[(j, 3)] and cate[(j, 0)] == name:
                namesort.append(data[i].tolist())

    return np.array(namesort)


def data_class(namenumber):
    if int(namenumber) == 1:
        name = 'AI/数据科学'
    elif int(namenumber) == 2:
        name = '产品与运营'
    elif int(namenumber) == 3:
        name = '生活兴趣'
    elif int(namenumber) == 4:
        name = '电商运营'
    elif int(namenumber) == 5:
        name = '编程与开发'
    elif int(namenumber) == 6:
        name = '职业考试'
    elif int(namenumber) == 7:
        name = '职场提升'
    elif int(namenumber) == 8:
        name = '设计创意'
    else:
        name = '语言学习'
    return name

def get_daysdata(kind,opt,num,dataDraw,dataTime):
    days=0
    while days<365:
        try:
                oneday=datetime.timedelta(days=days)
                today=datetime.date.today()
                day=(today-oneday).strftime("%Y_%m_%d")
                file_cat='./data/'+day+'.csv'
                day=(today-oneday).strftime("%m.%d")
                data=pd.read_csv(file_cat)
                data_category = pd.read_csv('./category/categorydata.csv')
                data=np.array(data)[:,1:]
                cate=np.array(data_category)[:,1:]
                if int(num)!=0:
                    if opt==1:
                        if kind==0:
                            dataDraw.append(data[:,8].mean())
                            dataTime.append(day)
                        else:
                            dataDraw.append(data_classification(data,cate,data_class(kind))[:,8].astype(float).mean())
                            dataTime.append(day)
                    elif opt==2:
                        if kind==0:
                            dataDraw.append(data[:,9].mean())
                            dataTime.append(day)
                        else:
                            data=data_classification(data,cate,data_class(kind))
                            dataDraw.append(data[:,9].astype(float).mean())
                            dataTime.append(day)
                    else:
                        if kind==0:
                            dataDraw.append((data[:,7].astype(float)*data[:,8].astype(float)).mean())
                            dataTime.append(day)
                        else:
                            data=data_classification(data,cate,data_class(kind))
                            dataDraw.append((data[:,7].astype(float)*data[:,8].astype(float)).mean())
                            dataTime.append(day)
                    num-=1
                if num==0:
                    days=400
        except:
            pass
        days+=1
    if days<400:
        QMessageBox.information(None, "提示", "读取数据出错，可能是没有储存足够多的数据，将打印所有您拥有的全部数据", QMessageBox.Yes)

def trend_days(kind, opt, num):
    dataDraw = []
    dataTime = []
    get_daysdata(kind, opt, num, dataDraw, dataTime)
    dataDraw.reverse()
    dataTime.reverse()
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.figure(num='网易云课堂数据分析助手', figsize=(10, 8))
    if opt == 1:
        if kind == 0:
            plt.xlabel('日期', size=15)
            plt.ylabel('总人数/课程数', size=15)
            plt.title('课程平均学习人数随时间变化图', size=20)
        else:
            plt.xlabel('日期', size=15)
            plt.ylabel('总人数/课程数', size=15)
            plt.title(('{}类课程平均学习人数随时间变化图'.format(data_class(kind))), size=20)
    elif opt == 2:
        if kind == 0:
            plt.xlabel('日期', size=15)
            plt.ylabel('当日平均得分', size=15)
            plt.title('课程平均得分随时间变化图，课程评分满分为5', size=20)
        else:
            plt.xlabel('日期', size=15)
            plt.ylabel('当日平均得分', size=15)
            plt.title(('{}类课程平均得分随时间变化图，课程评分满分为5'.format(data_class(kind))), size=20)
    elif kind == 0:
        plt.xlabel('日期', size=15)
        plt.ylabel('总收入/课程数', size=15)
        plt.title('课程平均收入随时间变化图', size=20)
    else:
        plt.xlabel('日期', size=15)
        plt.ylabel('总收入/课程数', size=15)
        plt.title(('{}类课程平均收入随时间变化图'.format(data_class(kind))), size=20)
    number = range(len(dataDraw))
    x = np.array(number)
    y = np.array(dataDraw)
    x_shift, y_shift = (0, 0)
    if num > 3:
        y_smooth = interp1d(x, y, kind='cubic')
        x_new = np.linspace(min(x), max(x), num * 10)
        plt.plot(x_new, (y_smooth(x_new)), linewidth='3')
        if opt == 2:
            x_shift, y_shift = (1e-05, 1e-05)
        else:
            x_shift, y_shift = (0.1, 0.1)
    else:
        plt.plot(x, y, linewidth='3')
    plt.xticks(x, dataTime)
    plt.scatter(x, y)
    if opt == 1:
        for i in range(len(x)):
            plt.annotate(('%.1f人' % dataDraw[i]), xy=(x[i], y[i]), xytext=(x[i] + x_shift, y[i] + y_shift))

    elif opt == 2:
        for i in range(len(x)):
            plt.annotate(('%.4f分' % dataDraw[i]), xy=(x[i], y[i]), xytext=(x[i] + x_shift, y[i] + y_shift))

    else:
        for i in range(len(x)):
            plt.annotate(('%.1f元' % dataDraw[i]), xy=(x[i], y[i]), xytext=(x[i] + x_shift, y[i] + y_shift))

    plt.show()
