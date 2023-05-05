# -*- coding:utf-8 -*-
"""
Created on May 03 2023

@author : woshihaozhaojun@sina.com
"""

import pygame


class Edge():
    """Edge of the catan world

    A line on which players can build road and one edge can only have one owner

    Attributes:
        start_pos(tuple): start position of the line
        end_pos(tuple): end position of the line
        color(str): color representing the owner
        mid(tuple): the middle point of the line
        adjacents(list): adjacent edges
        incidents(list): vertices that self is incident on
    """
    WIDTH = 5

    def __init__(self, start_pos: tuple, end_pos: tuple, color='yellow'):
        """start_pos和end_pos都是int的tuple2,float会导致不同tile的重合边不重合
        """
        super().__init__()
        self.start_pos, self.end_pos = start_pos, end_pos
        self.color = color
        self.mid = tuple([(s + e) / 2 for s, e in zip(self.start_pos, self.end_pos)])
        self.adjacents = list()
        self.incidents = list()

    def show(self, screen):
        pygame.draw.line(screen, pygame.Color(self.color), self.start_pos, self.end_pos, self.WIDTH)

    def change_color(self, color):
        self.color = color
