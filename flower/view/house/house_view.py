import csv
import json
import os
import random
import time
from urllib import parse

import patsy
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
# from flower.view.house.spiderHouse import spiderHouse
import random
from multiprocessing import Process, Queue
import requests
from bs4 import BeautifulSoup
import statsmodels.api as sm

from flower.models import AllHouse
import os
import pandas as pd
import requests
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split

import xlrd
PATH = r"flower/flowerData/house/"
FILENAME = r"house.csv"
FILENAME2 = r"workinghouse.csv"
defaultStart = 14
defaultEnd = 15
def house_index(request):
    all_data = AllHouse.objects.all()
    context = {
        "all_house":all_data
    }
    return render(request,'house.html',context)

def collectData(request):
    start = time.time()
    # try:
    main()
    # except:
    #     return HttpResponse("failed")
    print("[info]耗时",(time.time()-start))
    num = AllHouse.objects.all().count()
    # try:
    #
    # except:
    #     return HttpResponse("failed")
    return HttpResponse(num)

def exportData(request):
    data = AllHouse.objects.all()
    if os.path.exists(PATH) == False:
        os.makedirs(PATH)
    header = ["title","village","area","type","size","ori","info","rent","people","dist"]
    #csv的读取
    with open(PATH+FILENAME,"w",encoding="utf-8",newline="") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        #正常点的写
        for i in data:
            all_info = [i.title, i.village, i.are, i.type, i.size, i.ori, i.info, i.rent, i.people, i.dist]
            f_csv.writerow(all_info)
    f = open(PATH+FILENAME, 'rb')
    response = FileResponse(f)
    response['Content-Type'] = 'application/octet-stream;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="' + parse.quote("house") + ".csv" + '"'
    return response

def workingData(request):
    # data = list(list(AllHouse.objects.all().values_list("dist","rent","size","type")))
    data = AllHouse.objects.all()
    # header = ["区域", "租房价格", "房间数量", "房屋面积"]
    # csv的读取
    with open(PATH + FILENAME2, "w", encoding="utf-8", newline="") as f:
        f_csv = csv.writer(f)
        # f_csv.writerow(header)
        # 正常点的写
        for i in data:
            all_info = [i.dist, int(i.rent), parse_houseNumber(i.type),parse_houseArea(i.size)]
            f_csv.writerow(all_info)
    f = open(PATH + FILENAME2, 'rb')
    response = FileResponse(f)
    response['Content-Type'] = 'application/octet-stream;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="' + parse.quote("workinghouse") + ".csv" + '"'
    return response


def forecasePlace(request):
    place = int(request.POST.get("place"))
    print(place)
    p = forecaseData()
    result = p.forecase_place(place)
    return HttpResponse(result)

def forecaseArea1(request):
    area = int(request.POST.get("area"))
    p = forecaseData()
    result = p.forecase_area1(area)
    return HttpResponse(result)

def forecaseArea2(request):
    area = int(request.POST.get("area"))
    num = int(request.POST.get("num"))
    p = forecaseData()
    result = p.forecase_area2(area,num)
    return HttpResponse(result)
##################数据处理#######################
#加工房间数量
def parse_houseNumber(num):
    rooms = num.strip().split("室")[0]
    halls = num.strip().split("室")[1].strip().split("厅")[0]
    result = int(rooms) + int(halls)
    return result

#加工房屋面积
def parse_houseArea(area):
    return area.strip().split("平米")[0]


class spiderHouse(Process):
    def __init__(self,url,q,dist):
        #重写父类的__init__方法
        super(spiderHouse, self).__init__()
        self.url = url
        self.q = q
        self.dist = dist
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
            'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
            ]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': self.user_agent[random.randint(0, 5)],
            'Content-type': 'text/html;charset=UTF-8',

        }

    def run(self):
        self.parse_page()

    def send_request(self,url):
        '''
        :param url: 用来发送请求的方法
        :return: 返回网页源码
        '''
        #请求出错时，重复请求三次
        i = 0
        while i <= 3:
            try:
                print("1请求的url:",url)
                return requests.get(url=url,headers=self.headers)
            except Exception as e:
                print("2[INFO] %s%s" %(e,url))
                i += 1

    def parse_page(self):
        response = self.send_request(self.url)
        response.encoding = "utf-8"
        html = response.text
        soup = BeautifulSoup(html)
        for tag in soup.find('ul', id='house-lst').find_all('div', class_='info-panel'):
            ss = []
            for aa in tag.find_all('a'):
                # print(aa.string)
                ss.append(aa.string)

            for bb in tag.find_all('span'):
                # print(bb.string)
                ss.append(bb.string)

            self.q.put("长度：",len(ss))

            if len(ss) == 15:
                AllHouse.objects.create(title=ss[0],village=ss[1],are=ss[2],type=ss[4],size=ss[6],ori=ss[7],info=ss[11],rent=ss[13],people=ss[14],dist=self.dist)
            elif len(ss) == 18:
                AllHouse.objects.create(title=ss[0],village=ss[1],are=ss[2],type=ss[4],size=ss[6],ori=ss[7],info=ss[11],rent=ss[16],people=ss[17],dist=self.dist)
            elif len(ss) == 12:
                AllHouse.objects.create(title=ss[0], village=ss[1], are=ss[2], type=ss[4], size=ss[6],ori=ss[7], info=ss[8], rent=ss[10], people=ss[9], dist=self.dist)
            else:
                continue
#处理爬虫的数据
def main():
    dist_dict = {
        # "furong":6,
        # "yuhua":63,
        # "yuelu":42,
        # "tianxin":18,
        # "kaifu":24
        "furong": defaultStart,
        "yuhua": defaultStart,
        "yuelu": defaultStart,
        "tianxin": defaultStart,
        "kaifu": defaultStart
    }
    # 创建一个队列用来保存进程获取到的数据
    q = Queue()
    #构造所有的url
    all_url_list = []

    for k,v in dist_dict.items():
        base_url = "http://cs.lianjia.com/zufang/"+k+"/pg"
        for i in range(defaultStart,defaultEnd):
            base_url2 = base_url+str(i)
            all_url_list.append(base_url2)
    #保存进程
    # print(all_url_list)
    Process_list = []
    for url in all_url_list:
        dist = url.split("http://cs.lianjia.com/zufang/")[1].split("/pg")[0]
        print(dist)
        p = spiderHouse(url,q,dist)
        p.start()
        Process_list.append(p)

    #让主进程等待子进程执行完成
    for j in Process_list:
        j.join()
    while not q.empty():
        print(q.get())

class forecaseData:
    def __init__(self):
        self.path = PATH
        self.filename = FILENAME2
        self.df = pd.read_csv(PATH + FILENAME2, names=[ "cs_dist","cs_rent","cs_type", "cs_size"])
        self.clf = RandomForestClassifier(max_depth=5, n_estimators=10)
        self.X = self.df.ix[:, ["cs_type", "cs_size", "cs_dist"]]
        self.df.loc[:, 'cs_rent'] = self.df['cs_rent']#.astype(int)

        self.y = self.df.ix[:, ["cs_rent"]]
    def forecase_place(self,place):
        self.df.to_csv(self.path+"workinghouse2.csv", index=False, header=False)
        f = 'cs_rent ~ cs_dist'
        y, X = patsy.dmatrices(f, self.df, return_type='dataframe')
        results = sm.OLS(y, X).fit()
        # print(results.summary())
        to_pred_idx = X.iloc[0].index
        # print(to_pred_idx)
        to_pred_zeros = np.zeros(len(to_pred_idx))
        tpdf = pd.DataFrame(to_pred_zeros, index=to_pred_idx, columns=['value'])
        tpdf['value'] = place
        tpdf.loc['Intercept'] = 1
        # tpdf.loc['Beds'] = 2
        # 区域
        # tpdf.loc['cs_dist[T.furong]'] = 1
        # tpdf.loc['cs_dist[T.tianxin]'] = 2
        # tpdf.loc['cs_dist[T.kaifu]'] = 3
        # tpdf.loc['cs_dist[T.yuelu]'] = 4
        # tpdf.loc['cs_dist[T.yuhua]'] = 5
        # print(tpdf.loc['cs_dist[T.yuhua]'])
        pred = results.predict(tpdf['value'])

        return pred[0]

    def forecase_area1(self,area):
        # 根据房屋面积、房屋价格的历史数据，建立线性回归模型
        # 建立线性回归模型
        regr = linear_model.LinearRegression()
        # 拟合
        regr.fit(self.X['cs_size'].reshape(-1, 1), self.y)
        # 注意此处.reshape(-1, 1)，因为X是一维的！
        # 不难得到直线的斜率、截距
        a, b = regr.coef_, regr.intercept_
        # 给出待预测面积
        area = int(area)
        # 方式1：根据直线方程计算的价格
        # print(a * area + b)
        # 方式2：根据predict方法预测的价格
        # print(regr.predict(area))
        result = regr.predict(area)
        #print(result.tolist())
        return result[0]
        # 画图
        # 1.真实的点
        # plt.scatter(self.X['cs_size'], self.y, color='blue')
        # 2.拟合的直线
        # plt.plot(self.X['cs_size'], regr.predict(self.X['cs_size'].reshape(-1, 1)), color='red', linewidth=4)
        # plt.show()
    def forecase_area2(self,area,size):
        X = self.df.ix[:,[ "cs_size","cs_type"]]
        X_train, X_test, y_train, y_test = train_test_split(X, self.y, test_size=.3)

        regr = linear_model.LinearRegression()
        # print(X_train)
        # print(y_train)
        regr.fit(X_train, y_train)

        # print(X_test)
        # construct test data
        # rent: 3100
        data = [[area,size]]
        # index = [0]
        # 面积和数量
        columns = ["cs_size", "cs_type"]
        X_test2 = pd.DataFrame(data=data, columns=columns)
        y_pred = regr.predict(X_test2)
        a, b = regr.coef_, regr.intercept_
        # print('theta0 is:%s;\ntheta1 is:%s;\ntheta2 is:%s' % (b[0], a[0][0], a[0][1]))
        return y_pred[0]