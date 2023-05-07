# -*- coding:utf-8 -*-
"""
Created on May 03 2023

@author : woshihaozhaojun@sina.com
"""
from collections import deque
from time import sleep

import pygame

from conf import (
    CAPTION, WIDTH, HEIGHT, BACKGROUND, WIN_POINT,
    xs, ys, colors, names
)
from player import (
    Player, WarningMessage
)
from tile import Hexagon
from util import (
    init_layout, drop_duplicate_and_befriend_edge_vertex
)


def init_resource(hexs, color2player):
    """玩家选择初始位置后获取初始资源"""
    for tile in hexs:
        resource = tile.res
        for vertex in [vertex for vertex in tile.vertices if vertex.color in color2player]:
            if vertex.level == 2:
                color2player[vertex.color] + resource

    print('---initialize resource---')
    for jugador in color2player.values():
        print(f"for {jugador.name}, {jugador.resources}")


def init_tiles(screen):
    """初始化tile并且记录数字和tile的映射关系

    Args:
        screen: 显示的屏幕

    Returns:
        list[Tile]
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
            for _ in range(vertex.level):
                jugador + resource

    print(f"{turno} round, {joueur.name} has rolled {no}")


def build_road(player: Player, tile: Hexagon, j: int, edge2edge: dict, edge2ver: dict, is_check: bool = True):
    """建造道路

    如果需要检查，则验证附近是否已经有建筑或者道路；
    若没有则提示这是飞地
    """
    road = tile.edges[j - 1]
    if road.color != Hexagon.INIT_COLOR:
        player.warning(message=WarningMessage.OCCUPIED)
    elif not is_check or any(
            [adj.color == player.color for adj in edge2edge[road]] +
            [adj.color == player.color for adj in edge2ver[road]]
    ):
        if player.build_road():
            tile.change_edge_color(j - 1, player.color)
        else:
            player.warning(obj='road')
    else:
        player.warning(message=WarningMessage.ENCLAVE)
    sleep(0.5)


def build_village(player: Player, tile: Hexagon, j: int, ver2edge: dict, ver2ver: dict, is_check: bool = True):
    """建造村庄

    若需要检查，则检查是否有相连的道路；
    再检查邻近是否已经有建筑

    Args:
        player:
        tile:
        j: 角在tile的序号，从1开始
        ver2edge: 角和连接边的关系
        ver2ver: 角和相邻角的关系
        is_check: 是否检查
    """
    village = tile.vertices[j - 1]
    if village.color != Hexagon.INIT_COLOR:
        player.warning(message=WarningMessage.OCCUPIED)
    elif not is_check or any([edge.color == player.color for edge in ver2edge[village]]):
        if any([ver.color != Hexagon.INIT_COLOR for ver in ver2ver[village]]):
            player.warning(message=WarningMessage.OVERCROWDED)
        elif player.build_village():
            tile.change_vertex_color(j - 1, player.color)
            player.point += 1
        else:
            player.warning(obj='village')
    else:
        player.warning(message=WarningMessage.ENCLAVE)
    sleep(0.5)


def upgrade_village(player: Player, tile: Hexagon, j: int):
    """升级村庄

    Args:
        player:
        tile:
        j: 角在tile的序号，从1开始
    """
    village = tile.vertices[j - 1]
    if village.color != player.color:
        player.warning(message=WarningMessage.OCCUPIED)
    elif player.update_village():
        tile.upgrade_vertex(j - 1)
        player.point += 1
    else:
        player.warning(message=WarningMessage.SHORTAGE)
    sleep(0.5)


def demolish_road(player: Player, tile: Hexagon, j: int):
    road = tile.edges[j - 1]
    player.demolish_road(road=road, color=Hexagon.INIT_COLOR)
    sleep(0.5)


def demolish_village(player: Player, tile: Hexagon, j: int):
    village = tile.vertices[j - 1]
    player.demolish_village(village=village, color=Hexagon.INIT_COLOR)
    player.point -= 1
    sleep(0.5)


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
    ver2edge, ver2ver, edge2edge, edge2ver = drop_duplicate_and_befriend_edge_vertex(tiles)

    # for v, es in ver2edge.items():
    #     print(v.topleft, [e.mid for e in es])

    # 初始化精灵组
    hex_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    ver_group = pygame.sprite.Group()
    for tile in tiles:
        hex_group.add(tile)
    for player in players:
        player_group.add(player)
    for vertex in ver2edge:
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
            roll(player, no2tiles, color2player, turno)

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

            tiles[i].chosen_one(color=player.color)

            keys = pygame.key.get_pressed()
            # 左右键来调整要操作的tile
            if keys[pygame.K_LEFT]:
                i -= 1
                sleep(0.5)
            elif keys[pygame.K_RIGHT]:
                i += 1
                sleep(0.5)
            elif keys[pygame.K_UP]:
                i -= 5
                sleep(0.5)
            elif keys[pygame.K_DOWN]:
                i += 5
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
                build_road(player, tile=tiles[i], j=j, edge2edge=edge2edge, edge2ver=edge2ver, is_check=i > 8)
            elif keys[pygame.K_v]:
                build_village(player, tiles[i], j, ver2edge=ver2edge, ver2ver=ver2ver, is_check=i > 8)
            elif keys[pygame.K_u]:
                upgrade_village(player, tiles[i], j)
            elif keys[pygame.K_t]:
                demolish_road(player, tile=tiles[i], j=j)
            elif keys[pygame.K_b]:
                demolish_village(player, tile=tiles[i], j=j)

            for jugador in players:
                jugador.show_card()

            for vertex in ver_group:
                vertex.show()
            ver_group.draw(screen)

            pygame.display.update()

            if player.point >= WIN_POINT:
                print(f'GAME OVER!')
                pygame.quit()
                exit()

            # pass over to the next player
            if keys[pygame.K_0]:
                break


if __name__ == "__main__":
    main()
