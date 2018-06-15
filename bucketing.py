"""
Created on the 16th June 2018

@author : woshihaozhaojun@sina.com
"""

import numpy as np
from scipy.stats import chi2

def ChiStatOfNei(Freq1, Freq2):
    ''' 计算两个频数分布的Chi Stat
    
    Args:
        Freq1(np.array)
        Freq2(np.array)
    Returns:
        Chi stat of Freq1 and Freq2
    '''
    if Freq1.size != Freq2.size:
        raise ValueError("Lengths of the two arrays to compare are not identical")
        
    Exp_dist = Freq1+Freq2
    Exp_dist = Exp_dist/sum(Exp_dist)
    
    Exp_freq1 = Exp_dist * sum(Freq1)
    Exp_freq2 = Exp_dist * sum(Freq2)
    
    SqRes1 = (Freq1 - Exp_freq1) ** 2
    SqRes2 = (Freq2 - Exp_freq2) ** 2
    
    Exp_freq1[Exp_freq1 == 0] = 1 # Eij可能为0，避免division 
    Exp_freq2[Exp_freq2 == 0] = 1 #
    
    Chi2 = sum(SqRes1/Exp_freq1 + SqRes2/Exp_freq2)
    
    return Chi2


def ChiMerge(X, y, significanceLevel, min_interval):
    ''' Chi Merge
    
    bottom-up式的分箱方法,
    
    1. 先将序列排序,序列中每个点作为一个bucket,
    2. 计算每对相邻buckets频数分布的Chi Stat,
    3. 选择Chi Stat中最小并小于合并阈值的相邻区间合并
    4. 重复2.3步直到Chi stat全部大于合并阈值或区间数小于等于最少区间数
    
    Args:
        X(np.array) :- 自变量序列
        y(np.array) :- 因变量序列
        sigfnicanceLevel(float) :- 显著性水平,一般是[0.9, 0.95, 0.99]中一个
        min_interval(int) :- 
    Returns:
        X_y(iterables) :- 每个元素为[区间, 区间内种类频数分布]
        classes(iterables) :- 种类列表
        intervals(iterables) :- 元素为区间左边界，升序排列
    '''
    ### 变量检查 ###
    ########## start
    if X.size != y.size :
        raise ValueError("X and y must be of the same length")
    if not 0 < significanceLevel < 1:
        raise ValueError("significance level should be between 0 and 1")

    classes = list(set(y))
    num_class = len(classes)
    
    if len(classes) <2 :
        raise ValueError("种类数小于2")
    ########### end
    
    # 根据种类数和显著性水平得到合并阈值    
    threshold = chi2.ppf( significanceLevel, df = num_class-1 )
    print("一共有{}个类\nChi Statistic的阈值为 {}".format(num_class, threshold))
    
    ### 初始化 ###
    ####### start
    X_y = []
    indices = np.argsort(X) 
    for i in indices:
        freq = np.zeros(num_class)
        freq[ classes.index(y[i])] = 1
        X_y.append([ [X[i]], freq ])
        
    num_interval = len(X_y)
    ######## end
        
    ### 迭代过程 ###
    ########## start
    while num_interval > min_interval :
        # 计算每对相邻区间的Chi Statistic
        chiOfNei = []
        for i in range(num_interval-1):
            chiOfNei.append(
                ChiStatOfNei(
                    X_y[i][1], X_y[i+1][1] 
                )
            )
            
        # 如果存在小于合并阈值的Chi Stat,
        # 选择Chi Stat最小的相邻区间合并            
        if min(chiOfNei)> threshold:
            break
            
        else:
            indices2merge = [ index for index, value in enumerate(chiOfNei) if value == min(chiOfNei)]
            indices2merge = [index for index in indices2merge if index-1 not in indices2merge]

            for index2merge in sorted(indices2merge, reverse= True):
                X_y[index2merge][0].extend(X_y[index2merge+1][0])
                X_y[index2merge][1] += X_y[index2merge+1][1]
                X_y.pop(index2merge+1 )
            
            num_interval = len(X_y)
    ########### end
            
    intervals = [ interval_freq[0][0] for interval_freq in X_y]
    return X_y, classes, intervals

def test():
    X = [1e-2, 0.5, 0.7, 0.9, 0.3, 1, 1.6, 1.8, 1.55, 2.2, 2.5, 2, 10]
    y = ['超低','低',  '低'   , '低'   , '低' , '中'  , '中' , '中' , '中'   , '高'   ,'高'   , '高', '超高']
    X= np.array(X)
    y = np.array(y)

    结果, classes, intervals =ChiMerge(X,y, 0.9, 5)

    print("种类为 {}\n区间分界点为{}".format(classes, intervals))