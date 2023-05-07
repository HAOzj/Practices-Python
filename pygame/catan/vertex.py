# -*- coding:utf-8 -*-
"""
Created on May 03 2023

@author : woshihaozhaojun@sina.com
"""
import pygame

from conf import INIT_COLOR
from util import draw_colorized_contour


class Vertex(pygame.sprite.Sprite):
    """

    Attributes:
        x, y(float): coordinate of the top left
        color(str): color representing the owner
        screen(pygame.surface.Surface): the screen on which self is shown
        edges(list): the list of edges that are incident on self
    """
    WIDTH, HEIGHT = 15, 15

    def __init__(self, x, y, screen, color=None):
        super().__init__()
        x, y = int(x), int(y)
        self.screen = screen
        self.topleft = (x, y)
        self.rect = pygame.rect.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.image = pygame.surface.Surface((self.WIDTH, self.HEIGHT))
        self.color = color
        self.edges = list()
        self.level = 0

    def _change_image(self, file_path="../images/catan/hut.jpeg"):
        self.image = pygame.image.load(file_path)
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))

    def show(self):
        # colorize the contour
        _color = pygame.Color(self.color)
        draw_colorized_contour(
            rect=self.rect,
            width=int(self.WIDTH / 5),
            color=_color,
            screen=self.screen
        )

    def change_color(self, color):
        self.color = color
        if color != INIT_COLOR:
            self.level += 1
            self._change_image()

    def upgrade(self):
        self.level += 1
        self._change_image('../images/catan/town.jpeg')

    def __hash__(self):
        return hash(self.topleft)

    def __eq__(self, other):
        return self.topleft == other.topleft
