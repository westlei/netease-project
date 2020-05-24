import requests, re, lxml.html, json, datetime
import pandas as pd, numpy as np
from PyQt5.QtWidgets import QMessageBox, QProgressDialog
from pandas.api import types
#需要cssselect库依赖

def get_data():
    try:
        today = datetime.date.today().strftime('%Y_%m_%d')
        file_cat = './data/' + today + '.csv'
        data = pd.read_csv(file_cat)
        data_category = pd.read_csv('./category/categorydata.csv')
        data = np.array(data)[:, 1:]
        cate = np.array(data_category)[:, 1:]
        QMessageBox.information(None, '提示', '数据已经成功获取！', QMessageBox.Yes)
    except:
        flag = 0
        while flag < 1:
            try:
                data, cate = data_capture()
                flag = 10
            except:
                flag += 1

        if flag < 10:
            try:
                days = 1
                while days < 365:
                    try:
                        oneday = datetime.timedelta(days=days)
                        today = datetime.date.today()
                        day = (today - oneday).strftime('%Y_%m_%d')
                        file_cat = './data/' + day + '.csv'
                        data = pd.read_csv(file_cat)
                        data_category = pd.read_csv('./category/categorydata.csv')
                        data = np.array(data)[:, 1:]
                        cate = np.array(data_category)[:, 1:]
                        days = 365
                    except:
                        days += 1

            except:
                file_cat = './data/2020_02_17.csv'
                data = pd.read_csv(file_cat)
                data_category = pd.read_csv('./category/categorydata.csv')
                data = np.array(data)[:, 1:]
                cate = np.array(data_category)[:, 1:]

            QMessageBox.information(None, '提示', '数据已经成功获取！', QMessageBox.Yes)

    return (data, cate)

def sortcols(df):
    col_str = []
    col_num = []
    col_unc = []
    for column in df.columns:
        if types.is_string_dtype(df[column]):
            col_str.append(column)
        elif types.is_numeric_dtype(df[column]):
            col_num.append(column)
        else:
            col_unc.append(column)
    return (col_str, col_num, col_unc)


def data_capture():
    QMessageBox.information(None, '提示', '正在网上爬取实时信息，数据收集完成会提醒您，请稍候！', QMessageBox.Yes)
    url_main = 'https://study.163.com'
    r = requests.get(url_main)
    html_text = r.content.decode()
    tree = lxml.html.fromstring(html_text)
    items1 = tree.cssselect('a.f-f0.first.cat2.tit.f-fl')
    list_category = []
    items = items1
    for idx, item in enumerate(items):
        try:
            c_name = item.text_content()
            c_parent = item.get('data-index')
            c_child = item.get('data-name')
            c_url = item.get('href')
            list_category.append([c_name, c_parent, c_child, c_url])
        except:
            pass
    items2 = tree.cssselect('p.cate3links > a.f-f0')
    items = items2
    for idx, item in enumerate(items):
        try:
            c_name = item.text_content()
            c_parent = item.get('data-index')
            c_child = item.get('data-name')
            c_url = item.get('href')
            list_category.append([c_name, c_parent, c_child, c_url])
        except:
            pass
    data_category = pd.DataFrame(list_category, columns=['name', 'parent', 'child', 'url'])
    data_category['name'] = data_category['name'].apply(lambda x: x.replace('\n', ''))
    data_category['parent'] = data_category['parent'].apply(lambda x: x.replace('_类目框', ''))
    data_category['cat_id'] = data_category['url'].apply(lambda x: x.split('/')[(-1)])
    data_category['url'] = data_category['cat_id'].apply(lambda x: 'https://study.163.com/category/' + x)
    data_category = data_category.drop_duplicates(subset=['cat_id'])
    data_category.loc[(data_category['name'] != data_category['child'])]
    del data_category['name']
    data_category = data_category.loc[data_category['cat_id'].apply(str.isnumeric)]
    data_category.to_csv('./category/categorydata.csv')
    data_category = pd.read_csv('./category/categorydata.csv')
    headers_cat = {'Referer':'https://study.163.com/category/480000003124027', 
     'cookie':'NTESSTUDYSI=c2b373320c9e4bdcbaaf3e472e82f2d6; EDUWEBDEVICE=affc57a4b6aa408091a8f0c9752b08d9; utm=eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly9zdHVkeS4xNjMuY29tL2NhdGVnb3J5LzQ4MDAwMDAwMzEyNDAyNw==; __utma=129633230.1300737634.1560475613.1560475613.1560475613.1; __utmc=129633230; __utmz=129633230.1560475613.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=129633230.2.10.1560475613', 
     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
    dt = datetime.datetime.now()
    timestamp = dt.replace(tzinfo=(datetime.timezone.utc)).timestamp()
    mark = 1
    for cat_id in data_category['cat_id']:
        url_cat = 'https://study.163.com/j/web/fetchPersonalData.json?categoryId=' + str(cat_id)
        url_check = 'https://study.163.com/category/' + str(cat_id)
        headers_cat['Referer'] = url_check
        r_cat = requests.get(url_cat, headers=headers_cat)
        try:
            html_text = r_cat.content.decode()
            html_json = json.loads(html_text)
            modules = html_json['result']
            for module in modules:
                courses = module['contentModuleVo']
                tmp_df = pd.DataFrame.from_dict(courses)
                if mark == 1:
                    data_courses_raw1 = tmp_df
                    mark = 0
                else:
                    data_courses_raw1 = pd.concat([data_courses_raw1, tmp_df], axis=0)

        except:
            pass
    data_courses_bak1 = data_courses_raw1
    col_empty = []
    col_notemp = []
    row_cnt, col_cnt = data_courses_raw1.shape
    for column in data_courses_raw1.columns:
        rcnt_empty = sum(pd.isna(data_courses_raw1[column])) + sum(data_courses_raw1[column].apply(lambda x: str(x).replace(' ', '')) == '') + sum(data_courses_raw1[column].apply(lambda x: str(x).upper()) == 'NULL')
        if rcnt_empty >= row_cnt * 0.9:
            col_empty.append(column)
        else:
            col_notemp.append(column)
    data_courses_raw1 = data_courses_raw1[col_notemp]
    log_file = './data/product_check.txt'
    col_str, col_num, col_unc = sortcols(data_courses_raw1)
    f = open(log_file, 'wb')
    for column in data_courses_raw1.columns:
        tmp_stat = data_courses_raw1.groupby(column)[column].count()
        f.write(bytes(str(tmp_stat), 'utf-8'))
        f.write(bytes('\n*************************************\n', 'utf-8'))
    f.close()
    log_file = './data/data_check.txt'
    f = open(log_file, 'wb')
    row_num = data_courses_raw1.shape[0]
    for column in col_str:
        val_cnt = len(pd.unique(data_courses_raw1[column]))
        if val_cnt >= row_num / 3 or val_cnt >= 15:
            f.write(bytes(column + ' 属于离散枚举值', 'utf-8'))
        else:
            tmp_stat = data_courses_raw1.groupby(column)[column].count()
            f.write(bytes(str(tmp_stat), 'utf-8'))
        f.write(bytes('\n*************************************\n', 'utf-8'))
    f.close()
    col_selected1 = [
     'productId', 'productName', 'description', 'categoryId',
     'provider', 'targetUrl',
     'originalPrice', 'discountPrice',
     'learnerCount', 'score', 'scoreLevel',
     'productType', 'isTopGrade', 'topGrade']
    data_courses_1 = data_courses_raw1[col_selected1]
    data_courses_1 = data_courses_1.drop_duplicates(subset=['productId'])
    today = datetime.date.today().strftime('%Y_%m_%d')
    file_cat = './data/' + today + '.csv'
    category = data_category.fillna(0)
    data = data_courses_1.fillna(0)
    data = data.replace(to_replace=(-1), value=0)
    data.to_csv(file_cat)
    QMessageBox.information(None, '提示', '数据已经成功获取！', QMessageBox.Yes)
    return (np.array(data), np.array(category)[:, 1:])
