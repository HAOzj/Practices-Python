# 简介
DataFrame(以下统一简称为DF)是一种结构化的二维数据结构,python的pandas和r中都有.我们讲的是pandas的DF.

## DF和numpy
Pandas包中的数据结构是以numpy包作为基础,只是提供了丰富的数据分析接口，DF也不例外.
numpy中一维和二维数据结构均为ndarray,ndarray中元素类型一致,都是int, float等,由dtype指定.

## DF和Series
二维数组DF是一维数组Series的聚合.  
Series由index和values组成,index是索引,可以指定名字,values是每个索引对应的数值.  
而DF由columns和对应的Series组成,columns中每个column对应于一个Series,不过


```python
import pandas as pd 
import numpy as np 
values = [i for i in range(5)]
index = [i + 2 for i in range(5)]
s = pd.Series(values, index=index, dtype=np.int32)
s.index.name = "index plus two"
assert (s.values == values).all(), print("There exists unequal element") # 每个元素都相等 
```

## 生成DF

- 直接变量生成
```python3
import pandas as pd
mydict = [
    {'a': 1, 'b': 2, 'c': 3, 'd': 4},
    {'a': 100, 'b': 200, 'c': 300, 'd': 400},
    {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000 }
]
df = pd.DataFrame(mydict)
```

- 从数据库获取

以从postgre中获取为例
```python3
import psycopg2
import pandas as pd
db = psycopg2.connect(
    host='',
    user='',
    password='',
    database='',
    port=''
)

sql = "select * from my_table"

df  = pd.read_sql(sql, db)
```

- 读取csv文件
```
df = pd.read_csv(file_path, encoding="gbk")
```

## 设立索引
设立索引方便我们对DF进行搜索和合并等操作

```python3
import pandas as pd 
data = {
   "曝光pv": [1, 2, 3, 4],
   "点击pv": [0, 1, 2, 3],
   "点击率": [0, 0.5, 0.6667, 0.75]
}
df = pd.DataFrame(data)
df.set_index()
df.reset_index()
```

## 重命名和删除字段
```
# 传入字典来重命名
df = df.rename(columns={"曝光pv": "expo", "点击pv": "click", "点击率": "ctr"})

# 删除字段
df = df.drop(columns=["ctr"])
```

## 多行排序
```
df.sort_values(by=["expo", "click"], ascending=[False, True], inplace=True)

# 如果换新的索引
df.reset_index(inplace=True, drop=True)
```

## 填充空值
```
df = df.fillna(0)
```

## 筛选数据

### iloc  
integer-location based indexing for selection by position,顾名思义就是根据整数下标(注意,从0开始)来筛选

具体用法是 df.iloc[<行标> [,<列标>]],其中行标列标可以是
- list
- int
- min:max这样的形式,类似于range,不包含max

需要注意的是,返回的数据类型:如果选择单独的一行则返回Series,否则DF

### loc

loc支持根据以下两种方式来筛选
1. 下标
   1. 整数下标,类似于iloc,不同在于min:max时包含max
   2. 通过.set_index设定的下标
2. 逻辑判断



```python3
import pandas as pd 

df = pd.read_excel("my_file.xlsx")
type(df.iloc[0])  # <class 'pandas.core.series.Series'>
type(df.iloc[[0]])  # <class 'pandas.core.frame.DataFrame'>
HZJ = df[df["full_name" == "HZJ"]] # 根据逻辑判断
df.set_index("name", inplace=True)
Mio = df[["HZJ", "WBB"], ["name", "age"]]  # 取索引为"HZJ"或"WBB"的,名字和年纪的列
Tio = df.loc[:, "name":"age"] 
```

## udf

主要是三个函数
- apply, DF为输入
- map, Series为输入
- applymap, DF为输入,对矩阵的每个元素

| 方法 | 对象| 作用| 例子|
| --- | ---- | ---- | --- |
| apply | DF, Series | 沿着行(axis=1)或者列(axis=0) 或者 对元素值进行操作 | 行列加或者根据年龄分组 |
| map | Series | 用新值来代替旧元素| 跨年了年纪加1|
| applymap | DF | 对DF的每个元素操作，有时候比apply操作开 | 全部元素开方|

```python 
import pandas as pd 
data = {
   "曝光pv": [1, 2, 3, 4],
   "点击pv": [0, 1, 2, 3],
   "点击率": [0, 0.5, 0.6667, 0.75]
}
df = pd.DataFrame(data)
df = df.rename({"点击率": "ctr"})


def get_wilson_score(series):
    expo = series["expo"]
    click = series["click"]
    return wilson_score(click, expo)
    

def wilson_score(pos, total, z=1.96):
    """
    威尔逊得分计算函数
    :param pos: 正例数
    :param total: 总数
    :param p_z: 正太分布的分位数
    :return: 威尔逊得分
    """
    pos_rat = pos * 1. / total * 1.  # 正例比率
    score = (pos_rat + (np.square(z) / (2. * total))
             - ((z / (2. * total)) * np.sqrt(4. * total * (1. - pos_rat) * pos_rat + np.square(z)))) / \
    (1. + np.square(z) / total)
    return score * 100
    
def convert2float(x):
    if isinstance(x, str):
        x = x.strip("%")
    return float(x)

df["ctr"] = df["ctr"].map(convert2float)  # 替代旧列
df["ctr_wilson"] = df.apply(get_wilson_score, axis=1) # 为DF生成新列
df.applymap(lambda x: x+1) # 所有元素加1
```

## 聚合函数
```
import numpy as np

# sum
expo = np.sum(df["expo"])

# 累计百分比,百分比
field = "expo"
df[f"cumsum_{field}"] = df[field].cumsum(axis=0) / sum(df[field])
df[f"pct_{field}"] = df[field] / sum(df[field])
```
