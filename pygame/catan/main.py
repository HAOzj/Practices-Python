# -*- coding:utf-8 -*-
"""
Created on May 03 2023

@author : woshihaozhaojun@sina.com
"""
from collections import deque
from time import sleep

import pygame

from conf import (
    CAPTION, WIDTH, HEIGHT, BACKGROUND,
    xs, ys, colors, names
)
from player import Player
from tile import Hexagon
from util import (
    init_layout, drop_duplicate
)


def init_resource(hexs, color2player):
    """玩家选择初始位置后获取初始资源"""
    for tile in hexs:
        resource = tile.res
        for vertex in [vertex for vertex in tile.vertices if vertex.color in color2player]:
            color2player[vertex.color] + resource

    print('---initialize resource---')
    for jugador in color2player.values():
        print(f"for {jugador.name}, {jugador.resources}")


def init_tiles(screen):
    """初始化tile并且记录数字和tile的映射关系

    Args:
        screen: 显示的屏幕

    Returns:
        list(Tile)
        dict
    """
    # x_unit和y_unit表示相邻两层的第一个六边形中心的坐标差
    x_unit = Hexagon.G3 * Hexagon.RADIUS
    y_unit = Hexagon.RADIUS * 3

    # 随机资源类型和点数
    layout = init_layout()

    tiles = list()
    no2tiles = dict()
    for i in range(-3, 4):
        first_x, first_y = 200 + x_unit * (abs(i) + 2), y_unit * (i + 4)
        for j in range(6 - abs(i)):
            tile = layout.pop()
            hexagon = Hexagon(
                no=tile[0],
                center_x=first_x + 2 * x_unit * j,
                center_y=first_y,
                resource_type=tile[1],
                screen=screen
            )
            tiles.append(hexagon)
            no2tiles.setdefault(tile[0], []).append(hexagon)

    return tiles, no2tiles


def roll(joueur: Player, no2tiles: dict, color2player: dict, turno: int):
    """roll two dices and update players' resources"""
    no = joueur.roll_dice()
    tiles = no2tiles[no]
    for tile in tiles:
        resource = tile.res
        for vertex in [vertex for vertex in tile.vertices if vertex.color in color2player]:
            jugador = color2player[vertex.color]
            jugador + resource

    print(f"{turno} round, {joueur.name} has rolled {no}")


def main():
    # 初始化游戏
    pygame.init()
    pygame.mixer.init()
    # 创建游戏窗口
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # 设置游戏标题
    pygame.display.set_caption(CAPTION)

    # 初始化tiles, players
    tiles, no2tiles = init_tiles(screen)

    players = deque([
        Player(color=color, x=x, y=y, name=name, screen=screen)
        for x, y, color, name in zip(xs, ys, colors, names)
    ])

    color2player = dict([(player.color, player) for player in players])
    center2vertex = drop_duplicate(tiles)

    # 初始化精灵组
    hex_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    ver_group = pygame.sprite.Group()
    for tile in tiles:
        hex_group.add(tile)
    for player in players:
        player_group.add(player)
    for vertex in center2vertex.values():
        ver_group.add(vertex)

    # 保持游戏运行状态(游戏循环）
    turno, i, j = 0, 0, 0

    while players:
        player = players.popleft()
        players.append(player)

        turno += 1

        # clockwise放一轮小城后, counter-clockwise放大城
        if turno in [4, 8]:
            players.reverse()

        # 初始资源
        if turno == 9:
            init_resource(tiles, color2player)

        # tile grows resource
        if turno > 8:
            # roll点
            roll(player, no2tiles, color2player,turno)

        # show the current resources of each player
        # by name's alphabetic order
        for joueur in sorted(players, key=lambda x: x.name):
            print(f"{joueur.name}: {joueur.resources}")
        sleep(1)

        while True:
            # 检测事件
            for event in pygame.event.get():
                # 检测关闭按钮被点击的事件
                if event.type == pygame.QUIT:
                    # 退出
                    pygame.quit()
                    exit()

            screen.fill(BACKGROUND)

            for group in [hex_group]:
                group.update()
                group.draw(screen)
            player_group.draw(screen)

            for tile in tiles:
                tile.show_edges()
                tile.show_no()

            tiles[i % len(tiles)].chosen_one(color=player.color)

            keys = pygame.key.get_pressed()
            # 左右键来调整要操作的tile
            if keys[pygame.K_LEFT]:
                i -= 1
                sleep(0.5)
            elif keys[pygame.K_RIGHT]:
                i += 1
                sleep(0.5)
            elif keys[pygame.K_1]:
                j = 1
            elif keys[pygame.K_2]:
                j = 2
            elif keys[pygame.K_3]:
                j = 3
            elif keys[pygame.K_4]:
                j = 4
            elif keys[pygame.K_5]:
                j = 5
            elif keys[pygame.K_6]:
                j = 6
            elif keys[pygame.K_r]:
                if player.build_road():
                    tiles[i % len(tiles)].change_edge_color(j - 1, player.color)
                else:
                    player.warning(obj='road')
                sleep(0.5)
            elif keys[pygame.K_v]:
                if player.build_village():
                    tiles[i % len(tiles)].vertices[j - 1].change_color(player.color)
                else:
                    player.warning(obj='village')
                sleep(0.5)

            for jugador in players:
                jugador.show_card()

            for vertex in ver_group:
                vertex.show()
            ver_group.draw(screen)

            pygame.display.update()

            # pass over to the next player
            if keys[pygame.K_0]:
                break


if __name__ == "__main__":
    main()
