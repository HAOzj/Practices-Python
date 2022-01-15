"""
一些节日的计算公式:  
  节气日期  
    通式寿星公式 : Y* D+C -L,  
    其中 Y=年代后两位, D= 0.2422， L=该世纪经过的闰年数, C=f(节气, 年份)  

  复活节  
    y = 年份
    n = y-1900;
    a = mod(n, 19）
    q = floor(n/4）
    b = floor（（7*a+1）/19）
    m = mod（11*a+4-b, 29）
    w = mod(n+q+31-m, 7)
    d = 25-m-w  
    若为正数，月份为4月；否则，月份为3月, 日期为31+d, 比如若为0，则为3月31日。  
"""
  
节日日期列表 = {
  '新年': {'calendar': 'solar', 'date': [1, 1], 'duration': 3},  
  '公历新年': {'calendar': 'solar', 'date': [1, 1], 'duration': 3},  
  '元旦': {'calendar': 'solar', 'date': [1, 1], 'duration': 3},  
  '春节': {'calendar': 'lunar', 'date': [1, 1], 'duration': 7},  
  '除夕': {'calendar': 'lunar', 'date': [1, 1], 'duration': 7},  
  '清明': {'calendar': 'solar', 'date': [4, 5], 'duration': 3},  
  '劳动': {'calendar': 'solar', 'date': [5, 1], 'duration': 3},  
  '国际劳动': {'calendar': 'solar', 'date': [5, 1], 'duration': 3},  
  '五一国际劳动': {'calendar': 'solar', 'date': [5, 1], 'duration': 3},  
  '五一': {'calendar': 'solar', 'date': [5, 1], 'duration': 3},  
  '端午': {'calendar': 'lunar', 'date': [5, 5], 'duration': 3},  
  '七夕': {'calendar': 'lunar', 'date': [7, 7], 'duration': 1},  
  '中秋': {'calendar': 'lunar', 'date': [8, 15], 'duration': 3},  
  '国庆': {'calendar': 'solar', 'date': [10, 1], 'duration': 7},  
  '十一': {'calendar': 'solar', 'date': [10, 1], 'duration': 7},  
  '双十一': {'calendar': 'solar', 'date': [11, 11], 'duration': 1},  
  '双11': {'calendar': 'solar', 'date': [11, 11], 'duration': 1},  
  '双十二': {'calendar': 'solar', 'date': [12, 12], 'duration': 1},  
  '双12': {'calendar': 'solar', 'date': [12, 12], 'duration': 1},  
  '重阳': {'calendar': 'lunar', 'date': [9, 9], 'duration': 1},  
  '腊八': {'calendar': 'lunar', 'date': [12, 8], 'duration': 1}, 

  '情人节': {'calendar': 'solar', 'date': [2, 14], 'duration': 1},  
  '愚人节': {'calendar': 'solar', 'date': [4, 1], 'duration': 1},  
  '万圣节除夕': {'calendar': 'solar', 'date': [10, 31], 'duration': 1},  
  '万圣节前夜': {'calendar': 'solar', 'date': [10, 31], 'duration': 1},  
  '万圣节': {'calendar': 'solar', 'date': [11, 1], 'duration': 1},  
  '平安夜': {'calendar': 'solar', 'date': [12, 24], 'duration': 1},  
  '圣诞节前夕': {'calendar': 'solar', 'date': [12, 24], 'duration': 1},  
  '圣诞节前夜': {'calendar': 'solar', 'date': [12, 24], 'duration': 1},  
  '圣诞节': {'calendar': 'solar', 'date': [12, 25], 'duration': 1},  
  '母亲节': {'calendar': 'variedWithinMonth', 'date': [5, 2],  'weekday': 7, 'duration': 1},   # 实际上是5月第2个周日
  '父亲节': {'calendar': 'variedWithinMonth', 'date': [6, 3],  'weekday': 7, 'duration': 1},  
  '感恩节': {'calendar': 'variedWithinMonth', 'date': [11, 4], 'weekday': 4, 'duration': 1},  
  '复活节': {'calendar': 'other', 'date': [4, 1], 'duration': 1}
}