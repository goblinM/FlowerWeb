import os

import pandas as pd
import requests
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sa
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
plt.style.use('ggplot')
PATH = r"flower/flowerData/iris/"
FileName = "iris.data"
first = ("title","village","are","type","size","ori","rent","people","dist")
# Create your views here.
def index(request):
    context = {}
    return render(request, 'flower.html', context)

def flower(request):
    petalWidth = request.POST.get("petalWidth")
    petalLength = request.POST.get("petalLength")
    sepalWidth = request.POST.get("sepalWidth")
    sepalLength = request.POST.get("sepalLength")
    # columns = ["a","b","c","d"]
    # index = ["m"]
    # data = [float(petalWidth), float(petalLength), float(sepalWidth), float(sepalLength)]
    # data_list = pd.DataFrame(data=data, index=index, columns=columns)
    # print(data_list)
    #多维数据
    data_list = [float(petalWidth), float(petalLength), float(sepalWidth), float(sepalLength)]
    # print(data_list)
    # print(type(data_list))
    mechine = MechineStudy()
    result = mechine.preTest(data_list)
    return HttpResponse(result)

class MechineStudy:
    def __init__(self):
        # self.analysisData()

    # def analysisData(self):
        download_dir = requests.get("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data")
        if os.path.exists(PATH) == False:
            os.makedirs(PATH)
        #写入文件
        all_path = PATH+FileName

        with open(all_path, 'w') as f:
            f.write(download_dir.text)
        #读取文件 花萼的长 花萼的宽 花瓣的长 花瓣的宽 花的名字
        df = pd.read_csv(all_path, names=['sepal length', 'sepal width', 'petal length', 'petal width', 'class'],
                         encoding='utf-8')
        #替换花的名字
        # df["class"] = df["class"].map({"Iris-setosa": "flower1", "Iris-versicolor": "flower2", "Iris-virginica": "flower3"})
        df['petal area'] = df.apply(lambda r: r['petal length'] * r['petal width'], axis=1)

    #模型的建立 看准确率是否达到90%来判断模型是否成功
        self.clf = RandomForestClassifier(max_depth=5, n_estimators=10)
        X = df.ix[:, :4]
        y = df.ix[:,4]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)
        self.clf.fit(X_train, y_train)
        print(X_test)
        # y_pred = self.clf.predict(X_test)
        # print(y_pred)

        # rf = pd.DataFrame(list(zip(y_pred, y_test)), columns=['predicted', 'actual'])
        # rf['correct'] = rf.apply(lambda r: 1 if r['predicted'] == r['actual'] else 0, axis=1)
        # print(rf)
        # print(rf['correct'].sum() / rf['correct'].count())
    def preTest(self,data_list):
        result = self.clf.predict([data_list])
        return result[0]