import os
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sa
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
plt.style.use('ggplot')
PATH = r"E:\study\python\spider\iris"

download_dir = requests.get("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data")

if os.path.exists(PATH) == False:
    os.makedirs(PATH)

filename = "\iris.data"
with open(PATH+filename,'w') as f:
    f.write(download_dir.text)

df = pd.read_csv(PATH +filename,names=['sepal length','sepal width','petal length','petal width','class'], encoding='utf-8')
# print(df.head())
# print(df[df['class']=='Iris-virginica'])
# print(df.count())
# print(df[(df['class']=='Iris-virginica') & (df['petal width']>2.2)])

# fig,ax=plt.subplots(figsize=(6,4))
# ax.hist(df['petal width'],color='black')
# ax.set_ylabel('Count',fontsize=12)
# ax.set_xlabel("Width",fontsize=12)
# plt.title('Petal Width Hist',fontsize=16)
# plt.show()

# fig,ax=plt.subplots(figsize=(6,6))
# ax.scatter(df['petal width'],df['petal length'],color='green')
# ax.set_ylabel('petal length',fontsize=12)
# ax.set_xlabel("petal width",fontsize=12)
# plt.title('Petal Width Scatter',fontsize=16)
# plt.show()
#
# ax.plot(df['petal length'],color='blue')
# ax.set_ylabel('petal length',fontsize=12)
# ax.set_xlabel("petal width",fontsize=12)
# plt.title('Petal Width Plot',fontsize=16)
# plt.show()
#
# sns.pairplot(df,hue="class")
# sns.plt.show()

df["class"] = df["class"].map({"Iris-setosa":"flower1","Iris-versicolor":"flower2","Iris-virginica":"flower3"})
# print(df)
#映射函数 花蕾的宽度作为变量
# df['wide petal'] = df['petal width'].apply(lambda v:1 if v>1.3 else 0)
# print(df)
df['petal area'] = df.apply(lambda r: r['petal length'] * r['petal width'], axis=1)
# print(df)
# df.applymap(lambda v: np.log(v) if isinstance(v,float) else v)
df.groupby('class').mean()
# print(df.groupby('class').mean())
# print(df.groupby('class').describe())
# print(df.groupby('petal width')['class'].unique().to_frame())
# print(df.groupby('petal length')['class'].unique().to_frame())
# print(df.groupby('sepal width')['class'].unique().to_frame())
# print(df.groupby('sepal width')['class'].unique().to_frame())
# print(df.groupby('class')['petal width'].agg({'delta': lambda x: x.max() - x.min(), 'max': np.max, 'min': np.min}))
# print(df.groupby('class')['petal length'].agg({'delta': lambda x: x.max() - x.min(), 'max': np.max, 'min': np.min}))
#映射函数 花蕾的宽度作为变量
# df["high petal"] = df["petal length"].apply(lambda v:1 if v > 1 else 0)
# df.applymap(lambda v:np.log(v) if isinstance(v,float) else v)
# fig,ax=plt.subplots(figsize=(6,6))
# ax.scatter(df['petal width'],df['petal length'],color='green')
# ax.set_ylabel('petal length',fontsize=12)
# ax.set_xlabel("petal width",fontsize=12)
# plt.title('Petal Width Scatter',fontsize=16)
# plt.show()

#建模
# x = df["petal width"][:50]
# y = df["petal length"][:50]
# x = sa.add_constant(x)
# # y = sa.add_constant(y)
# results = sa.OLS(y,x).fit()  #二次建立回归的模型
# # results = sa.OLS(x,y).fit()
# print(results.summary())
#
# fig,ax = plt.subplots(figsize=(7,7))
# ax.plot(x,results.fittedvalues,label="regression line")
# ax.scatter(x,y,label="data point",color='r')
# # ax.plot(y,results.fittedvalues,label="regression line")
# # ax.scatter(x,y,label="data point",color='r')
# ax.set_ylabel("petal length",fontsize=12)
# ax.set_xlabel("petal width", fontsize=12)
# plt.title("petal width scatter",fontsize=16)


clf = RandomForestClassifier(max_depth=5, n_estimators=10)
X = df.ix[:,:4]
y = df.ix[:,4]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
rf = pd.DataFrame(list(zip(y_pred, y_test)), columns=['predicted', 'actual'])
rf['correct'] = rf.apply(lambda r: 1 if r['predicted'] == r['actual'] else 0, axis=1)
print(rf)
print(rf['correct'].sum()/rf['correct'].count())