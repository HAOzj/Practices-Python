# -*- coding:utf-8 -*-
"""
Created on May 03 2023

@author : woshihaozhaojun@sina.com
"""

import pygame


class Edge():
    WIDTH = 5

    def __init__(self, start_pos: tuple, end_pos: tuple, color='yellow'):
        """start_pos和end_pos都是int的tuple2,float会导致不同tile的重合边不重合
        """
        super().__init__()
        self.start_pos, self.end_pos = start_pos, end_pos
        self.color = color
        self.mid = tuple([(s + e) / 2 for s, e in zip(self.start_pos, self.end_pos)])

    #         pygame.draw.line(screen, pygame.Color(self.color), start_pos, end_pos, self.WIDTH)

    def show(self, screen):
        pygame.draw.line(screen, pygame.Color(self.color), self.start_pos, self.end_pos, self.WIDTH)

    def change_color(self, color):
        self.color = color
