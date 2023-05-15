# -*- coding:utf-8 -*-
"""
Created on May 03, 2023

@author : woshihaozhaojun@sina.com
"""
import random
from collections import defaultdict

import pygame

# from enum import StrEnum
from util import draw_colorized_contour

from conf import RESOURCES


class WarningMessage:
    OVERCROWDED = "there is already settlement in vicinity"
    OCCUPIED = "this {} is already occupied"
    ENCLAVE = "no connected settlement or road"
    SHORTAGE = "no enough res for {}"
    EXCEED = "your {}s have exceeded the capacity"


class DevelopCard:
    KNIGHT = 'knight'
    POINT = 'point'
    ROAD = 'road'
    CARD = 'card'
    MONOPOLY = 'monopoly'


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
    IMAGE = ['11vs8', 'jiahuan', 'xiaoshu', 'giegie']

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
        self.point = 0  # 分数
        self.roads, self.huts, self.towns = set(), set(), set()  # 大城和小城分开是为了保证数量不超
        self.develop_card = list()

        # 文字显示位置
        self.dest = (self.rect.right + 10, self.rect.y)
        self.card_dest = (self.rect.right + 10, self.rect.y + self.HEIGHT)
        self.develop_card_dest = (self.rect.right + 10, self.rect.y + 1.5 * self.HEIGHT)

        # 开始时可以建一座小城和一座大城以及两条路
        for res in self.VILLAGE + self.ROAD:
            self.__add__(res)
            self + res
        for res in self.UPGRADE:
            self + res

    def __add__(self, resource):
        if isinstance(resource, str):
            self.resources[resource] += 1
        elif isinstance(resource, dict):
            for k, v in resource.items():
                if isinstance(v, int):
                    self.resources[k] += v

    def __sub__(self, resource):
        self.resources[resource] -= 1

    @staticmethod
    def roll_dice():
        return random.randint(1, 6) + random.randint(1, 6)

    def pick_resource(self, tile):
        if tile.res in RESOURCES[:-1] and DevelopCard.CARD in self.develop_card:
            self + tile.res
            self.develop_card.remove(DevelopCard.CARD)

    def consume_resource(self, res_list):
        if all([self.resources[res] >= 1 for res in res_list]):
            for res in res_list:
                self - res
            return True
        return False

    def draw_develop_card(self):
        return self.consume_resource(self.DEVELOP_CARD)

    def build_road(self):
        is_road_enough = self.consume_resource(self.ROAD)
        if is_road_enough:
            return True
        elif DevelopCard.ROAD in self.develop_card:
            self.develop_card.remove(DevelopCard.ROAD)
            return True
        return False

    def build_village(self):
        return self.consume_resource(self.VILLAGE)

    def update_village(self):
        return self.consume_resource(self.UPGRADE)

    def demolish_village(self, village, color):
        """拆除村庄

        归还资源，减少分数
        """
        if village.color == self.color:
            self.point -= village.level

            # 归还资源
            for res in self.VILLAGE:
                self + res
            if village.level == 2:
                for res in self.UPGRADE:
                    self + res
                self.towns.remove(village)
            else:
                self.huts.remove(village)
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

        self.screen.blit(
            source=self.font.render(
                ",".join(self.develop_card),
                True,
                pygame.Color(self.color)
            ),
            dest=self.develop_card_dest
        )

    def confiscate(self, res):
        """一种资源被剥夺"""
        num = self.resources[res]
        self.resources[res] = 0
        return {res: num}

    def barter(self, res):
        """用四张同种资源换一张CARD发展卡"""
        if self.resources[res] >= 4:
            self.develop_card.append(DevelopCard.CARD)
            self.resources[res] -= 4

    def get_robbed(self, player):
        for tmp, cnt in self.resources.items():
            if cnt > 0:
                self - tmp
                player + tmp
                return