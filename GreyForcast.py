# -*- coding:utf-8 -*-
"""
Created on the 15th Jan 2021

@author : woshihaozhaojun@sina.com
"""
import pandas as pd
import numpy as np

# matplotlib inline
import matplotlib.pyplot as plt
import matplotlib

# matplotlib.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


class GrayForecast(object):
    # 初始化
    def __init__(self, data, datacolumn=None, xlabel=None):
        self.xlabel = xlabel
        self.x = list(data[xlabel])
        if isinstance(data, pd.core.frame.DataFrame):
            self.data = data
            try:
                self.data.columns = ['data']
            except Exception as e:
                if not datacolumn:
                    raise Exception('您传入的dataframe不止一列')
                else:
                    self.data = pd.DataFrame(data[datacolumn])
                    self.data.columns = ['data']
        elif isinstance(data, pd.core.series.Series):
            self.data = pd.DataFrame(data, columns=['data'])
        else:
            self.data = pd.DataFrame(data, columns=['data'])

        print(self.data)
        self.forecast_list = self.data.copy()

        if datacolumn:
            self.datacolumn = datacolumn
        else:
            self.datacolumn = None

        self.lambda_k = None

    # 级比校验
    def level_check(self):
        # 数据级比校验
        n = len(self.data)
        lambda_k = np.zeros(n - 1)
        for i in range(n - 1):
            lambda_k[i] = self.data.ix[i]["data"] / self.data.ix[i + 1]["data"]
            if lambda_k[i] < np.exp(-2 / (n + 1)) or lambda_k[i] > np.exp(2 / (n + 2)):
                flag = False
        else:
            flag = True

        self.lambda_k = lambda_k

        if not flag:
            print("级比校验失败，请对X(0)做平移变换")
            return False
        else:
            print("级比校验成功，请继续")
            return True

    # GM(1,1)建模
    def GM_11_build_model(self, forecast=5, x_new=0):
        if forecast > len(self.data):
            raise Exception('您的数据行不够')
        X_0 = np.array(self.forecast_list['data'].tail(forecast))
        #       1-AGO
        X_1 = np.zeros(X_0.shape)
        for i in range(X_0.shape[0]):
            X_1[i] = np.sum(X_0[0:i + 1])
        #       紧邻均值生成序列
        Z_1 = np.zeros(X_1.shape[0] - 1)
        for i in range(1, X_1.shape[0]):
            Z_1[i - 1] = -0.5 * (X_1[i] + X_1[i - 1])

        B = np.append(np.array(np.mat(Z_1).T), np.ones(Z_1.shape).reshape((Z_1.shape[0], 1)), axis=1)
        Yn = X_0[1:].reshape((X_0[1:].shape[0], 1))

        B = np.mat(B)
        Yn = np.mat(Yn)
        a_ = (B.T * B) ** -1 * B.T * Yn

        a, b = np.array(a_.T)[0]

        X_ = np.zeros(X_0.shape[0])

        def f(k):
            return (X_0[0] - b / a) * (1 - np.exp(a)) * np.exp(-a * (k))

        self.forecast_list.loc[len(self.forecast_list)] = f(X_.shape[0])
        self.x.append(x_new)

    # 预测
    def forecast(self, time=5, x_list=None, forecast_data_len=5):
        if x_list is None or len(x_list) != time:
            x_list = range(self.data.shape[0], self.data.shape[0] + time)
        for i in range(time):
            self.GM_11_build_model(forecast=forecast_data_len, x_new=x_list[i])

    # 打印日志
    def log(self):
        res = self.forecast_list.copy()
        if self.datacolumn:
            res.columns = [self.datacolumn]
        return res

    # 重置
    def reset(self):
        self.forecast_list = self.data.copy()

    # 作图
    def plot(self):
        # self.forecast_list.plot()
        print(self.forecast_list)
        plt.plot(self.x, self.forecast_list["data"], "o")
        print("type is ", type(self.forecast_list))
        if self.datacolumn:
            plt.ylabel(self.datacolumn[0] + "(1/100000)")
            # plt.legend(self.datacolumn)
            print(self.x)
            for (ind, x), y in zip(enumerate(self.x), self.forecast_list["data"]):
                if ind % 2 >= 0:
                    plt.text(x-0.5, y, "{}".format(round(y, 2)), fontdict={"size": 10})
            plt.title(f"{self.datacolumn[0]}")
            plt.xlabel(self.xlabel)
            plt.xticks(self.x, self.x, size=5)
            plt.savefig(f"/Users/haozhaojun/Desktop/mortality/{self.datacolumn[0]}.png")
            # plt.show()
            plt.clf()


def main():
    with open("boxIncome.csv", encoding="utf8") as fp:
        df = pd.read_csv(fp)
    df.tail()
    for col in "Total mortality rate,Male mortality rate,Female mortality rate".split(","):
        gf = GrayForecast(df, [col], "year")
        gf.forecast(5, [i + 2021 for i in range(5)], forecast_data_len=4)
        gf.log()
        gf.plot()


if __name__ == "__main__":
    main()