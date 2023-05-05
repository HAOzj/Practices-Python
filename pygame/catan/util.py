# -*- coding:utf-8 -*-
"""
Created on May 03 2023

@author : woshihaozhaojun@sina.com
"""
import random

import pygame


def draw_colorized_contour(rect, width, color, screen):
    for start, end in [
        (rect.topleft, rect.topright),
        (rect.topright, rect.bottomright),
        (rect.bottomleft, rect.bottomright),
        (rect.topleft, rect.bottomleft)
    ]:
        pygame.draw.line(screen, color, start, end, width)


def init_layout():
    # 随机点数和资源
    no_list = [i for i in range(2, 13) if i != 7] * 3
    for i in [2, 12]:
        no_list.remove(i)

    resource_list = ['lumber', 'wool', 'wheat'] * 6 + ['ore', 'brick'] * 5
    random.shuffle(resource_list)
    layout = list(zip(no_list, resource_list))
    layout += [(7, 'desert')] * 2
    random.shuffle(layout)
    return layout


def drop_duplicate(hexs):
    """Drop overlapping vertices and edges

    Args:
        hexs(list):

    Returns:
        topleft2vertex, dict mapping center attribute to Vertex
    """
    # drop duplicate edges and vertices
    topleft2vertex, mid2edge = dict(), dict()
    center2index = dict()

    for i, tile in enumerate(hexs):
        for j, vertex in enumerate(tile.vertices):
            topleft2vertex[vertex.topleft] = vertex
            center2index[vertex.topleft] = (i, j)
        for edge in tile.edges:
            mid2edge[edge.mid] = edge

    for tile in hexs:
        vertices = tile.vertices
        for i, vertex in enumerate(vertices):
            vertices[i] = topleft2vertex[vertex.topleft]
        edges = tile.edges
        for i, edge in enumerate(edges):
            edges[i] = mid2edge[edge.mid]

    return topleft2vertex
