import pandas as pd, numpy as np, datetime
from matplotlib import pyplot as plt


def learnerDistribution(data, cate):
    sort = np.unique(cate[:, 0])
    number = np.zeros(len(sort))
    lenth = len(cate[:, 0])
    for i in range(0, len(data[:, 3])):
        for j in range(0, lenth):
            if data[:, 3][i] == cate[(j, 3)]:
                number += cate[(j, 0)] == sort

    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.figure(num='网易云课堂数据分析助手', figsize=(6, 6))
    label = sort
    explode = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
    values = number
    plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')
    plt.title('学习人数占比', size=16)
    plt.savefig('./picture/课堂各类型学习人数占比')
    plt.show()


def revenueDistribution(data, cate):
    sort = np.unique(cate[:, 0])
    revenue = np.zeros(len(sort))
    lenth = len(cate[:, 0])
    for i in range(0, len(data[:, 3])):
        for j in range(0, lenth):
            if data[:, 3][i] == cate[(j, 3)]:
                revenue[(cate[(j, 0)] == sort)] += data[(i, 7)] * data[(i, 8)]

    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.figure(num='网易云课堂数据分析助手', figsize=(6, 6))
    label = sort
    explode = revenue / revenue.sum()
    values = revenue
    plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')
    plt.title('收入占比', size=16)
    plt.savefig('./picture/课堂各类型课程利润占比')
    plt.show()


def couseNumber(data, cate):
    sort = np.unique(cate[:, 0])
    freenumber = np.zeros(len(sort))
    earnnumber = np.zeros(len(sort))
    lenth = len(cate[:, 0])
    for i in range(0, len(data[:, 3])):
        for j in range(0, lenth):
            if data[:, 3][i] == cate[(j, 3)]:
                if data[:, 7][i] == 0:
                    freenumber += cate[(j, 0)] == sort
                else:
                    earnnumber += cate[(j, 0)] == sort

    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.figure(num='网易云课堂数据分析助手', figsize=(10, 8))
    n = len(earnnumber)
    X = np.arange(n) + 1
    plt.bar((X - 0.2), freenumber, alpha=0.9, width=0.4, label='免费课程', lw=1)
    for a, b in zip(X, freenumber):
        plt.text((a - 0.2), (b + 0.5), ('%.0f' % b), ha='center', va='bottom', fontsize=12)

    plt.xticks(X, sort, rotation=30)
    plt.tick_params(labelsize=13)
    plt.bar((X + 0.2), earnnumber, alpha=0.9, width=0.4, label='付费课程', lw=1)
    for a, b in zip(X, earnnumber):
        plt.text((a + 0.2), (b + 0.5), ('%.0f' % b), ha='center', va='bottom', fontsize=12)

    plt.ylabel('number', size=15)
    plt.title('数量分布', size=20)
    plt.legend(loc='upper left')
    plt.savefig('./picture/课程主题类别及数量')
    plt.show()
