# -*- coding:utf-8 -*-
"""
Created on May 03, 2023

@author : woshihaozhaojun@sina.com
"""
# 屏幕
WIDTH, HEIGHT = 1500, 1200
BACKGROUND = (200, 200, 200)
CAPTION = '妹多局之卡坦岛'

# 资源
RESOURCES = 'wool lumber wheat ore brick desert'.split(' ')

# tile
RADIUS = 30

# vertex
INIT_COLOR = 'white'

# 玩家配置
WIN_POINT = 10
HUT_MAX, TOWN_MAX = 5, 4
names = ['小蓝', '小紫', '小红', '小绿']
colors = ['blue', 'purple', 'red', 'green']
xs = [0] * 4
ys = [0, HEIGHT / 4, HEIGHT / 2, HEIGHT / 4 * 3]

for i in range(len(ys)):
    ys[i] += 30
