import csv
import os
from urllib import parse

import tushare
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from pandas_datareader import data as pdr
# pip install multitasking
# pip install fix_yahoo_finance
import fix_yahoo_finance as yf
import tushare as ts
import pandas as pd
import numpy as np
from pandas_datareader import data, wb
import matplotlib.pyplot as plt
from sklearn.svm import SVR

from flower.models import AllStockBasic, RealTimePens, HISData

yf.pdr_override() #需要调用这个函数
# 获取数据
PATH = r"flower/flowerData/stock/"
FILENAME = r"stock.csv"
FILENAME2 = r"wu.csv"
FILENAME3 = r"wu1.csv"

def index(request):
    return render(request,"stock.html")

def showStock(request):
    data = RealTimePens.objects.all()
    context = {
        "data": data
    }
    return render(request, "ajax/ajax_stock.html", context)

def addStock(request):
    stock = request.POST.get("stock")
    # print(tushare.__version__)
    cf = ts.get_stock_basics()
    if os.path.exists(PATH) == False:
        os.makedirs(PATH)
    if os.path.exists(PATH+FILENAME) == False :
        cf.to_csv(PATH+FILENAME,encoding="utf-8",header=False) #header表示是否需要头部，index表示是否需要行号
        with open(PATH + FILENAME, 'r', encoding="utf-8") as f:
            f_csv = csv.reader(f)
            data = f_csv
            for row in data:
                code, name, industry, area, pe, outstanding, totals, totalAssets, liquidAssets, fixedAssets, reserved, reservedPerShare, esp, bvps, pb, timeToMarket, undp, perundp, rev, profit, gpr, npr, holders = \
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], \
                row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22]
                AllStockBasic.objects.create(code=code, name=name, industry=industry, area=area, pe=pe,
                                             outstanding=outstanding,totals=totals, totalAssets=totalAssets, liquidAssets=liquidAssets,
                                             fixedAssets=fixedAssets, reserved=reserved, reservedPerShare=reservedPerShare,
                                             esp=esp, bvps=bvps, pb=pb, timeToMarket=timeToMarket, undp=undp,
                                             perundp=perundp,
                                             rev=rev, profit=profit, gpr=gpr, npr=npr, holders=holders)

    df = ts.get_realtime_quotes(stock)  # Single stock symbol
    df = df[['code', 'name', 'open','pre_close','price','high','low', 'bid', 'ask', 'volume', 'amount', 'date','time']]
    df.to_csv(PATH+"test.csv",encoding="utf-8",header=False)
    with open(PATH +"test.csv", 'r', encoding="utf-8") as f:
        d_csv = csv.reader(f)
        for row in d_csv:
            try:
                RealTimePens.objects.create(code=row[1],name=row[2],open=row[3],pre_close=row[4],price=row[5],high=row[6],low=row[7],bid=row[8],ask=row[9],volume=row[10],amount=row[11],date=row[12],time=row[13])
            except:
                continue
    data = RealTimePens.objects.all()
    context = {
        "data":data
    }
    return render(request,"ajax/ajax_stock.html",context)

def uploadStock(request):
    code_list = list(RealTimePens.objects.values_list("code",flat=True))
    if len(code_list) != 0:
        for code in code_list:
            df = ts.get_realtime_quotes(code)
            df = df[['code', 'name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume', 'amount', 'date','time']]
            df.to_csv(PATH + "test.csv", encoding="utf-8", header=False)
            with open(PATH + "test.csv", 'r', encoding="utf-8") as f:
                d_csv = csv.reader(f)
                for row in d_csv:
                    try:
                        RealTimePens.objects.filter(code=code).update(name=row[2], open=row[3], pre_close=row[4], price=row[5],
                                                    high=row[6], low=row[7], bid=row[8], ask=row[9], volume=row[10],
                                                    amount=row[11], date=row[12], time=row[13])
                    except:
                        continue
        data = RealTimePens.objects.all()
    else:
        data = []
    context = {
        "data": data
    }
    return render(request, "ajax/ajax_stock.html", context)

def showStockInfo(request):
    context = {}
    code = request.POST.get("code")
    df = ts.get_stock_basics()
    date = df.ix[code]['timeToMarket'] #上市日期YYYYMMDD
    date = str(date)
    startDate = date[:4]+"-"+date[4:6]+"-"+date[-2:]
    context['startDate'] = startDate
    context['code'] = code
    return render(request,'ajax/ajax_stockInfo.html',context)

def getInfoData(request):
    code = request.POST.get("code")
    startTime = request.POST.get("startTime")
    endTime = request.POST.get("endTime")
    df = ts.get_k_data(code)  # 两个日期之间的前复权数据
    # df = ts.get_hist_data(code,start=startTime,end=endTime)  # 两个日期之间的前复权数据
    if os.path.exists(PATH) == False:
        os.makedirs(PATH)
    #存一份到数据库
    if os.path.exists(PATH+FILENAME2) == False:
        df.to_csv(PATH+FILENAME2,encoding="utf-8",header=False,index=False)
        with open(PATH+FILENAME2,'r',encoding="utf-8",newline="") as f:
            d_csv = csv.reader(f)
            for row in d_csv:
                try:
                    HISData.objects.create(code=code, open=row[0], high=row[1], close=row[2], low=row[3],
                                           volume=row[4], price_change=row[5], p_change=row[6], ma5=row[7], ma10=row[8],
                                           ma20=row[9], v_ma5=row[10], v_ma10=row[11],v_ma20=row[12])
                except:
                    continue
    df.to_csv(PATH+"wu2.csv",encoding="utf-8",index=False)
    return HttpResponse("ok")

def exportInfoData(request):
    f = open(PATH + 'wu2.csv', 'rb')
    response = FileResponse(f)
    response['Content-Type'] = 'application/octet-stream;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="' + parse.quote("stockExport") + ".csv" + '"'
    return response

def workingInfoData(request):
    csvFile = open(PATH + 'wu2.csv', "r")
    reader = csv.reader(csvFile)
    with open(PATH+FILENAME3,'w',encoding="utf-8",newline="") as f:
        f_csv = csv.writer(f)
        for item in reader:
            all_info = [item[0],item[1],item[2],item[3],item[4]]
            f_csv.writerow(all_info)
    f = open(PATH + FILENAME3, 'rb')
    response = FileResponse(f)
    response['Content-Type'] = 'application/octet-stream;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="' + parse.quote("stockWorking") + ".csv" + '"'
    return response

def forecaseInfoData(request):
    code = request.POST.get("code")
    stock = analysisStock()
    result = str(stock.closePrice())
    return HttpResponse(result)

def comparedData(request):
    context = {}
    code = request.POST.get("code")
    stock = analysisStock()
    context["data"] = stock.forecasestockStrategy()
    return render(request,'ajax/ajax_stockStrategy.html',context)

###################数据分析处理########################
class analysisStock:
    def __init__(self):
        self.sp = pd.read_csv(PATH+FILENAME3)



    def closePrice(self):
        # 当天的收盘价，在逐一附加过去20天收盘价格 新到久
        for i in range(1, 21, 1):
            self.sp.loc[:, 'Close Minus ' + str(i)] = self.sp['close'].shift(i)
        # print(self.sp)
        sp20 = self.sp[[x for x in self.sp.columns if 'Close Minus' in x or x == 'close']].iloc[20:, ]
        # 将列的顺序颠倒,从左到右就是最早时间到最晚时间
        sp20 = sp20.iloc[:, ::-1]
        # 使用scikit learn的向量机建模
        # 预测内容：从当天的收盘价去预测明天的收盘价，如已知2010-01-04的收盘价信息，想预测假定仍未发生交易的2010-01-05的收盘价
        # 这是每个人的梦想
        clf = SVR(kernel='linear')
        self.defaultTest = 2
        # X数组使用最后的1条记录用于测试，其余用于机器学习
        X_train = sp20[:-self.defaultTest]
        # print(X_train)
        # Y数组仅有一列，Close：收盘价
        # 一样也是使用最后530用于测试，其余1000条用于机器学习
        # Y,上移一位，如2010-01-04交易数据，训练对应的应变量是2010-01-05日期的交易数据
        y_train = sp20['close'].shift(-1)[:-self.defaultTest]
        # print(y_train)
        # 用于测试的X数组从1000条到1530条
        self.default_X_test = len(sp20)-self.defaultTest
        self.defaultData = len(sp20)
        X_test = sp20[self.default_X_test:len(sp20)]
        # 用于测试的X数组从1000条到1530条
        # 上移一位，如2010-01-04交易数据，训练对应的应变量是2010-01-05日期的交易数据
        y_test = sp20['close'].shift(-1)[-len(sp20):-self.default_X_test]  #
        # 用训练数据机器学习
        model = clf.fit(X_train, y_train)
        # 用测试数据预测，方便和实际结果对比，并判断准确率
        preds = model.predict(X_test)
        return preds[0]

    def get_stats(self, s, n=252):
        # 删除NaN数据
        s = s.dropna()
        # 盈利次数：获取每日收益率大于0的所有数据，并计算总数
        wins = len(s[s > 0])
        # 亏损次数：获取每日收益率小于0的所有数据，并计算总数
        losses = len(s[s < 0])
        # 盈亏平衡次数：获取每日收益率等于0的所有数据，并计算总数
        evens = len(s[s == 0])
        # 盈利平均值，round四舍五入，3为小数位数
        mean_w = round(s[s > 0].mean(), 3)
        # 亏损平均值
        mean_l = round(s[s < 0].mean(), 3)
        # 盈利亏损比例
        win_r = round(wins / losses, 3)
        # 平均收益
        mean_trd = round(s.mean(), 3)
        # 标准差
        sd = round(np.std(s), 3)
        # 最大亏损
        max_l = round(s.min(), 3)
        # 最大盈利
        max_w = round(s.max(), 3)
        # 夏普比率：代表投资人每多承担一分风险，可以拿到几分超额报酬；若为正值，代表基金报酬率高过波动风险；若为负值，代表基金操作风险大过于报酬率。
        # 每个投资组合都可以计算Sharpe Ratio,即投资回报与多冒风险的比例，这个比例越高，投资组合越佳。
        # 夏普比率 = （ E(Rp) - Rf ）/ σp  其中E(Rp)：投资组合预期报酬率 Rf：无风险利率 σp：投资组合的标准差
        # 夏普比率 = （平均收益/标准差）* n=252的平方根 , 最后四舍五入
        # 注：年波动率等于收益率的标准差除以其均值，再除以交易日倒数的平方根，通常交易日取252 天。
        sharpe_r = round((s.mean() / np.std(s)) * np.sqrt(n), 4)
        # 交易次数
        cnt = len(s)
        context = {
            "cnt": cnt,
            "wins": wins,
            "losses": losses,
            "evens": evens,
            "win_r": win_r,
            "mean_l": mean_l,
            "mean_w":mean_w,
            "mean_trd": mean_trd,
            "sd": sd,
            "max_l": max_l,
            "max_w": max_w,
            "sharpe_r": sharpe_r,

        }
        return context
        # print('交易次数:', cnt, \
        #       '\n盈利次数:', wins, \
        #       '\n亏损次数:', losses, \
        #       '\n盈亏平衡次数:', evens, \
        #       '\n盈利亏损比例', win_r, \
        #       '\n盈利平均值:', mean_w, \
        #       '\n亏损平均值:', mean_l, \
        #       '\n平均收益', mean_trd, \
        #       '\n标准差:', sd, \
        #       '\n最大亏损:', max_l, \
        #       '\n最大盈利:', max_w, \
        #       '\n夏普比率:', sharpe_r)

        # 随机产生1或0
    def long_stats(self,s,l,n=252):
        # 删除NaN数据
        s = s.dropna()
        # 盈利次数：获取每日每股收益大于长期每股收益的所有数据，并计算总数
        wins = len(s[s > l])
        # 亏损次数：获取每日每股收益率小于长期每股收益的所有数据，并计算总数
        losses = len(s[s < l])
        # 盈亏平衡次数：获取每日每股收益率等于长期每股收益的所有数据，并计算总数
        evens = len(s[s == l])
        # 盈利平均值，round四舍五入，3为小数位数
        mean_w = round(s[s > l].mean(), 3)
        # 亏损平均值
        mean_l = round(s[s < l].mean(), 3)
        # 盈利亏损比例
        win_r = round(wins / losses, 3)
        # 平均收益
        mean_trd = round(s.mean(), 3)
        # 标准差
        sd = round(np.std(s), 3)
        # 最大亏损
        max_l = round(s.min(), 3)
        # 最大盈利
        max_w = round(s.max(), 3)
        # 夏普比率：代表投资人每多承担一分风险，可以拿到几分超额报酬；若为正值，代表基金报酬率高过波动风险；若为负值，代表基金操作风险大过于报酬率。
        # 每个投资组合都可以计算Sharpe Ratio,即投资回报与多冒风险的比例，这个比例越高，投资组合越佳。
        # 夏普比率 = （ E(Rp) - Rf ）/ σp  其中E(Rp)：投资组合预期报酬率 Rf：无风险利率 σp：投资组合的标准差
        # 夏普比率 = （平均收益/标准差）* n=252的平方根 , 最后四舍五入
        # 注：年波动率等于收益率的标准差除以其均值，再除以交易日倒数的平方根，通常交易日取252 天。
        sharpe_r = round((s.mean() / np.std(s)) * np.sqrt(n), 4)
        # 交易次数
        cnt = len(s)
        context = {
            "cnt": cnt,
            "wins": wins,
            "losses": losses,
            "evens": evens,
            "win_r": win_r,
            "mean_l": mean_l,
            "mean_w": mean_w,
            "mean_trd": mean_trd,
            "sd": sd,
            "max_l": max_l,
            "max_w": max_w,
            "sharpe_r": sharpe_r,

        }
        return context
    def get_signal(self, x):
        val = np.random.rand()
        if val > .5:
            return 1
        else:
            return 0


    def forecasestockStrategy(self):
        context = {}
        # 第一行数据 2010-01-04,112.370003
        first_open = self.sp['open'].iloc[0]
        # print(first_open)
        # iloc中的-1代表最后一行，并获取收盘价，2016-03-01,195.009995,198.210007,194.449997,198.110001,
        last_close = self.sp['close'].iloc[-1]
        # print(last_close)
        # 每股收益(2010-01-04 至 2016-03-01) = 最后一天收盘价 减 第一天的开盘价
        benefit_code = last_close - first_open
        # print(benefit_code)

        # 每天盘中一天的每股收益（当天收盘价 - 开盘价），并生成新的列 每日收益
        self.sp['Daily Change'] = pd.Series(self.sp['close'] - self.sp['open'])
        # print(self.sp["Daily Change"])
        # print(self.sp['Daily Change'].sum())
        # 使用numpy计算盘中交易的标准差
        # print(np.std(self.sp['Daily Change']))
        context["long_rtn"] = self.long_stats(self.sp["Daily Change"],benefit_code)
        # 获取隔夜交易收益，当天开盘价 减 前一天的收盘价，shift(1) 上移一天
        self.sp['Overnight Change'] = pd.Series(self.sp['open'] - self.sp['close'].shift(1))
        # 隔夜交易收益
        # print(self.sp['Overnight Change'].sum())
        # 标准差，体现收益的波动性
        # print(np.std(self.sp['Overnight Change']))

        # 交易策略1：每日交易策略，每日回报率=（当前的收盘价 - 上一交易日的收盘价）/上一交易日收盘价
        daily_rtn = ((self.sp['close'] - self.sp['close'].shift(1)) / self.sp['close'].shift(1)) * 100
        # print(daily_rtn)

        # 日间交易策略：收益 = 当天收盘价 - 当天开盘价
        id_rtn = ((self.sp['close'] - self.sp['open']) / self.sp['open']) * 100
        # print(id_rtn)

        # 隔夜交易策略：隔夜交易收益率 = （当天开盘价 - 上一天收盘价）/上一天收盘价 *100 表示百分比
        on_rtn = ((self.sp['open'] - self.sp['close'].shift(1)) / self.sp['close'].shift(1)) * 100
        # print(on_rtn)

        context['daily_rtn'] = self.get_stats(daily_rtn) #每日交易
        context['id_rtn'] = self.get_stats(id_rtn) #日间交易
        context['on_rtn'] = self.get_stats(on_rtn) #隔夜交易

        #自定义交易规则
        # 第一步：计算相关参数，得到上轨Buyline
        # 和下轨Sellline：

        # N日High的最高价HH, N日Close的最低价LC
        #
        # N日Close的最高价HC，N日Low的最低价LL
        HH = max(self.sp["high"])
        LC = min(self.sp['close'])
        HC = max(self.sp['close'])
        LL = min(self.sp['low'])
        Range = max(HH - LC, HC - LL)
        K1 = 0.6
        BuyLine = self.sp['open'].iloc[-1] + K1 * Range
        context["autoDe_rtn"] = self.long_stats(self.sp['open'],BuyLine)

        # 产生新列，从Signal_0到Signal_999, axis=1 表示从上到小的垂直方向，设置随机产生的1或0
        # for i in range(1000):
        #     self.sp['Signal_' + str(i)] = self.sp.apply(self.get_signal, axis=1)
            # print(self.sp['Signal_' + str(i)])
            # self.get_stats(self.sp['Signal_' + str(i)])
        # print(self.sp)
        return context
    # 统计信息方法

