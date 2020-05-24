import os
import pandas as pd, datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from pandas_profiling import plot

def get_pandasdata():
    days = 0
    try:
        while days < 365:
            try:
                oneday = datetime.timedelta(days=days)
                today = datetime.date.today()
                day = (today - oneday).strftime('%Y_%m_%d')
                file_cat = './data/' + day + '.csv'
                data = pd.read_csv(file_cat,header=0,names=['0','课程ID','课程名','描述','类目ID','作者','页面地址','原价','折扣价','学习人数','评分','星级','类别','2','3'])
                days = 365
            except:
                days += 1
    except:
        try:
            file_cat = './data/2020_04_01.csv'
            data = pd.read_csv(file_cat,header=0,names=['0','课程ID','课程名','描述','类目ID','作者','页面地址','原价','折扣价','学习人数','评分','星级','类别','2','3'])
        except:
            pass 
    data=data[['课程名','描述','作者','原价','折扣价','学习人数','评分','星级']]
    return data

class pdReport():
    def __init__(self, profile):
        super(pdReport, self).__init__()
        self.date = profile.date
        self.head = profile.sample["head"]
        self.tail = profile.sample["tail"]
        self.table = profile.description_set["table"]
        self.variables = profile.description_set["variables"]
        self.correlations = profile.description_set["correlations"]
        self.messages = profile.description_set["messages"]
        self.Thead = ['课程名','描述','作者','原价','折扣价','学习人数','星级','评分']

    def getplot(self):
        key_to_data = {
            "pearson": (-1, "Pearson's r"),
            "spearman": (-1, "Spearman's ρ"),
            "kendall": (-1, "Kendall's τ"),
            "phi_k": (0, "Phik (φk)"),
            "cramers": (0, "Cramér's V (φc)"),
            "recoded": (0, "Recoded"),
        }
        for key in self.correlations:
            item=self.correlations[key]
            vmin, name = key_to_data[key]
            img = './report/'+key+'.svg'
            plot.correlation_matrix(item, vmin=vmin, img=img)

    def showimg(self, item):
        summary = self.variables[item]
        if "histogram_bins_bayesian_blocks" in summary:
            plot.histogram(summary["histogram_data"],summary,summary["histogram_bins_bayesian_blocks"],)
        else:
            plot.histogram(summary["value_counts"], summary, 10)
        
    def showlimg(self, item):
        summary = self.variables[item]
        plot.histogram(summary["length"], summary, 20)

                
