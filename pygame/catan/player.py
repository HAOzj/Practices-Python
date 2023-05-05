# -*- coding:utf-8 -*-
"""
Created on May 03 2023

@author : woshihaozhaojun@sina.com
"""
import random
from collections import defaultdict

import pygame

from util import draw_colorized_contour


class Player(pygame.sprite.Sprite):
    """player

    Rolling dices and build road and settlements to win

    Attributes:
        screen(pygame.surface.Surface): screen on which self is shown
        color(str): color representing self
        resources(dict): current resources
        name(str): name
    """
    WIDTH, HEIGHT = 30, 30
    ROAD = ['brick', 'lumber']
    VILLAGE = ROAD + ['wheat', 'wool']

    def __init__(self, color, x, y, name, screen):
        super().__init__()
        self.color = color
        self.screen = screen
        self.image = pygame.image.load("../images/catan/player.jpeg")
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.rect = pygame.rect.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.resources = defaultdict(int)
        self.name = name
        self.font = pygame.font.SysFont('Arial', 12)

        for res in self.VILLAGE + self.ROAD:
            self.__add__(res)
            self + res

    def __add__(self, resource):
        self.resources[resource] += 1

    def __sub__(self, resource):
        self.resources[resource] -= 1

    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def build_road(self):
        if all([self.resources[res] >= 1 for res in self.ROAD]):
            for res in self.ROAD:
                self - res
            return True
        return False

    def build_village(self):
        if all([self.resources[res] >= 1 for res in self.VILLAGE]):
            for res in self.VILLAGE:
                self - res
            return True
        return False

    def warning(self, obj='road'):
        self.screen.blit(
            source=self.font.render(
                "no enough res for " + obj,
                True,
                pygame.Color(self.color)
            ),
            dest=(self.rect.x, self.rect.y - 10)
        )

    def show_card(self):
        draw_colorized_contour(
            rect=self.rect,
            width=int(self.WIDTH / 5),
            color=pygame.Color(self.color),
            screen=self.screen
        )

        self.screen.blit(
            source=self.font.render(
                ",".join([f"{k}:{v}" for k, v in self.resources.items()]),
                True,
                pygame.Color(self.color)
            ),
            dest=(self.rect.x, self.rect.y + self.HEIGHT)
        )
