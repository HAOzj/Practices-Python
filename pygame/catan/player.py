# -*- coding:utf-8 -*-
"""
Created on May 03 2023

@author : woshihaozhaojun@sina.com
"""
import random
from collections import defaultdict

import pygame

# from enum import StrEnum
from util import draw_colorized_contour


class WarningMessage():
    OVERCROWDED = "there is already settlement in vicinity"
    OCCUPIED = "this {} is already occupied"
    ENCLAVE = "no connected settlement or road"
    SHORTAGE = "no enough res for {}"


class Player(pygame.sprite.Sprite):
    """player

    Rolling dices and build road and settlements to win

    Attributes:
        screen(pygame.surface.Surface): screen on which self is shown
        color(str): color representing self
        resources(dict): current resources
        name(str): name
        edges(Edge): owned Edge[s]
        vertices(Vertex): owned Vertex[s]
    """
    WIDTH, HEIGHT = 150, 100
    ROAD = ['brick', 'lumber']
    VILLAGE = ROAD + ['wheat', 'wool']
    UPGRADE = ['wheat'] * 2 + ['ore'] * 3
    DEVELOP_CARD = ['wheat', 'wool', 'ore']
    I = 0
    IMAGE = ['xiaokuan', 'jiahuan', 'xiaoshu', 'giegie']

    def __init__(self, color, x, y, name, screen):
        super().__init__()
        self.i = self.I
        self.__class__.I += 1
        self.color = color
        self.screen = screen
        self.image = pygame.image.load(f"../images/catan/{self.IMAGE[self.i % 4]}.jpeg")
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.rect = pygame.rect.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.resources = defaultdict(int)
        self.name = name
        self.font = pygame.font.SysFont('Arial', 12)
        self.edges, self.vertices = set(), set()
        self.point = 0  # TODO: 计算分数
        self.dest = (self.rect.right + 10, self.rect.y)
        self.card_dest = (self.rect.right + 10, self.rect.y + self.HEIGHT)

        for res in self.VILLAGE + self.ROAD:
            self.__add__(res)
            self + res
        for res in self.UPGRADE:
            self + res

    def __add__(self, resource):
        self.resources[resource] += 1

    def __sub__(self, resource):
        self.resources[resource] -= 1

    @staticmethod
    def roll_dice():
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

    def update_village(self):
        if all([self.resources[res] >= 1 for res in self.UPGRADE]):
            for res in self.UPGRADE:
                self - res
            return True
        return False

    def demolish_village(self, village, color):
        if village.color == self.color:
            for res in self.VILLAGE:
                self + res
            village.change_color(color)
        else:
            self.screen.blit(
                source=self.font.render(
                    "this village is not yours",
                    True,
                    pygame.Color(self.color)
                ),
                dest=self.dest
            )

    def demolish_road(self, road, color):
        if road.color == self.color:
            for res in self.ROAD:
                self + res
            road.change_color(color)
        else:
            self.screen.blit(
                source=self.font.render(
                    "this road is not yours",
                    True,
                    pygame.Color(self.color)
                ),
                dest=self.dest
            )

    def warning(self, obj='road', message=WarningMessage.SHORTAGE):
        text = message.format(obj)
        self.screen.blit(
            source=self.font.render(
                text,
                True,
                pygame.Color(self.color)
            ),
            dest=self.dest
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
            dest=self.card_dest
        )
