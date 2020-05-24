import pandas as pd, numpy as np
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QAbstractItemView
from PyQt5.QtCore import Qt

class learnerRank(QWidget):
    def __init__(self, data, cate):
        super(learnerRank, self).__init__()
        self.data = data
        self.cate = cate
        self.setWindowTitle('学习人数排名')
        self.resize(800,540)
        conLayout = QHBoxLayout()
        self.Tb = QTableWidget(1,6)
        self.Tb.setHorizontalHeaderLabels(['类别','小类','名称','作者','价格','学习人数'])
        self.Tb.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Tb.setColumnWidth(0,100)
        self.Tb.setColumnWidth(1,100)
        self.Tb.setColumnWidth(2,200)
        self.Tb.setColumnWidth(3,100)
        self.Tb.setColumnWidth(4,70)
        self.Tb.setColumnWidth(5,110)
        conLayout.addWidget(self.Tb)
        self.setLayout(conLayout)

    def data_hand(self, classdata):
        lenth = len(self.cate[:, 0])
        ll = [int(float(i)) for i in classdata[:, 8].tolist()]
        LearnerCount = np.argsort(ll)
        LearnerCount = LearnerCount[-1:0:-1]
        LearnerCountResult = []
        LearnerCountResult2 = []
        LearnerCountnew = []
        for i in LearnerCount:
            LearnerCountnew.append([classdata[:, 0][i], classdata[:, 1][i], classdata[:, 4][i], classdata[:, 7][i], classdata[:, 8][i]])
            for j in range(0, lenth):
                if int(classdata[:, 3][i]) == self.cate[(j, 3)]:
                    LearnerCountResult.append(self.cate[(j, 0)])
                    LearnerCountResult2.append(self.cate[(j, 1)])
        LearnerCountanalyse = pd.DataFrame({'category':LearnerCountResult,  'type':LearnerCountResult2,  'productName':[i[1] for i in LearnerCountnew],  'provider':[i[2] for i in LearnerCountnew],  'discountPrice':[i[3] for i in LearnerCountnew],  'learnerCount':[i[4] for i in LearnerCountnew]}, index=['%d' % i for i in range(1, len(LearnerCountnew) + 1)])
        namelist = list(LearnerCountanalyse)
        data = np.array(LearnerCountanalyse)
        for i in range(len(data)):
            if data[(i, 3)] == '0':
                data[(i, 3)] = 'NULL'

        self.Tb.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(namelist)):
                iTem = QTableWidgetItem(str(data[(i, j)]))
                iTem.setTextAlignment(Qt.AlignHCenter)
                self.Tb.setItem(i, j, iTem)

        self.show()


class revenueRank(QWidget):

    def __init__(self, data, cate):
        super(revenueRank, self).__init__()
        self.data = data
        self.cate = cate
        self.setWindowTitle('收入排名')
        self.resize(800,540)
        conLayout = QHBoxLayout()
        self.Tb = QTableWidget(1,6)
        self.Tb.setHorizontalHeaderLabels(['类别','小类','名称','作者','价格','收入'])
        self.Tb.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Tb.setColumnWidth(0,100)
        self.Tb.setColumnWidth(1,100)
        self.Tb.setColumnWidth(2,200)
        self.Tb.setColumnWidth(3,100)
        self.Tb.setColumnWidth(4,70)
        self.Tb.setColumnWidth(5,110)
        conLayout.addWidget(self.Tb)
        self.setLayout(conLayout)

    def data_hand(self, classdata):
        lenth = len(self.cate[:, 0])
        l1 = [float(i) for i in classdata[:, 7].tolist()]
        l2 = [float(i) for i in classdata[:, 8].tolist()]
        ll = np.array(l1) * np.array(l2)
        revenueCount = np.argsort(ll)
        revenueCount = revenueCount[-1:0:-1]
        revenueCountResult = []
        revenueCountResult2 = []
        revenueCountnew = []
        for i in revenueCount:
            revenueCountnew.append([classdata[:, 1][i], classdata[:, 4][i], classdata[:, 7][i], ll[i]])
            for j in range(0, lenth):
                if int(classdata[:, 3][i]) == self.cate[(j, 3)]:
                    revenueCountResult.append(self.cate[(j, 0)])
                    revenueCountResult2.append(self.cate[(j, 1)])

        revenueCountanalyse = pd.DataFrame({'category':revenueCountResult,  'type':revenueCountResult2,  'productName':[i[0] for i in revenueCountnew],  'provider':[i[1] for i in revenueCountnew],  'discountPrice':[i[2] for i in revenueCountnew],  'revenue':[i[3] for i in revenueCountnew]}, index=['%d' % i for i in range(1, len(revenueCountnew) + 1)])
        namelist = list(revenueCountanalyse)
        data = np.array(revenueCountanalyse)
        for i in range(len(data[:, 3])):
            if data[(i, 3)] == '0':
                data[(i, 3)] = 'NULL'

        self.Tb.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(namelist)):
                iTem = QTableWidgetItem(str(data[(i, j)]))
                iTem.setTextAlignment(Qt.AlignHCenter)
                self.Tb.setItem(i, j, iTem)

        self.show()
