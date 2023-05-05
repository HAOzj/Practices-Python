# -*- coding:utf-8 -*-
"""
Created on May 03 2023

@author : woshihaozhaojun@sina.com
"""
# 屏幕
WIDTH, HEIGHT = 1000, 800
BACKGROUND = (200, 200, 200)
CAPTION = '妹多局之卡坦岛'

# tile
RADIUS = 30

# 玩家配置
names = ['小蓝', '小紫', '小红', '小绿']
colors = ['blue', 'purple', 'red', 'green']
xs = [0] * 4
ys = [0, HEIGHT / 4, HEIGHT / 2, HEIGHT / 4 * 3]

for i in range(len(ys)):
    ys[i] += 30
