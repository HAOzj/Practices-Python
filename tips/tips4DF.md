# 简介
DataFrame(以下统一简称为DF)是一种结构化的数据储存形式,python的pandas和r中都有.我们讲的是pandas的DF.

## 生成DF

- 直接变量生成
```python3
import pandas as pd
mydict = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},
          {'a': 100, 'b': 200, 'c': 300, 'd': 400},
          {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000 }]
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

df  = pd.read_sql(sql, self.db)
```

## 设立索引
设立索引方便我们对DF进行搜索和合并等操作

```python3
df.set_index()
df.reset_index()
```



## 筛选数据

- iloc
integer-location based indexing for selection by position,顾名思义就是根据整数下标(注意,从0开始)来筛选

具体用法是 df.iloc[<行标> [,<列标>]],其中行标列标可以是list, int或者min;max这样的形式

需要注意的是,返回的数据类型:如果选择单独的一行则返回Series,否则DF
```python3
type(df.iloc[0])  # <class 'pandas.core.series.Series'>

type(df.iloc[[0]])  # <class 'pandas.core.frame.DataFrame'>
```

- loc

loc支持根据以下两种方式来筛选
1. 下标,包括整数下标和通过.set_index设定的下标
2. 逻辑判断


根据逻辑判断来筛选的一个例子
```python
HZJ = df[df["full_name" == "HZJ"]]
df.set_index("name", inplace=True)
Mio = df[["HZJ", "WBB"], ["name", "age"]]  # 取索引为"HZJ"或"WBB"的,名字和年纪的列
```

## udf

主要是三个函数
- apply, 多行为输入
- map, 单行为输入
- applymap, 对每个元素

```
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

df["ctr"] = df_tmp["ctr"].map(convert2float)
df["ctr_wilson"] = df.apply(get_wilson_score, axis=1)
```
