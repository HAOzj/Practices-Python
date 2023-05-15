# -*- coding:utf-8 -*-
"""
Created on May 03, 2023

@author : woshihaozhaojun@sina.com
"""
import math

import pygame

from conf import (
    RADIUS, INIT_COLOR, RESOURCES
)
from edge import Edge
from vertex import Vertex


class Hexagon(pygame.sprite.Sprite):
    """hexagonal tile

    The building block of the catan world, each growing one type of resource
    and representing one number between 2 and 12.

    Attributes:
        no(int): rolling number
        res(str): resource type, options ['wool', 'lumber', 'wheat', 'ore', 'brick', 'desert']
        screen(pygame.surface.Surface): screen on which self is shown
        center_x, center_y(float): coordinate of center
        edges(list[Edge]): six lines, where players can build road
        vertices(list[Vertex]): six vertices, where players can build settlements
    """
    RADIUS = RADIUS
    RESOURCE_TYPES = RESOURCES
    RESOURCE_IMAGES = [pygame.image.load(f"../images/catan/{res}.jpeg") for res in RESOURCE_TYPES]
    TIPO2IMAGE = dict(zip(RESOURCE_TYPES, RESOURCE_IMAGES))
    G3 = math.sqrt(3)
    WIDTH, HEIGHT = RADIUS * 2 * G3 - 2 * Edge.WIDTH, 2 * RADIUS - 2 * Edge.WIDTH
    ANGLES = [i * math.pi / 3 + math.pi / 6 for i in range(6)]
    INIT_COLOR = INIT_COLOR

    def __init__(self, no, resource_type, center_x, center_y, screen):
        super().__init__()
        self.no = no
        self.screen = screen
        self.center_x, self.center_y = center_x, center_y
        self.res = resource_type
        self.image = self.TIPO2IMAGE[self.res]
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.rect = pygame.rect.Rect(center_x - self.WIDTH / 2, center_y - self.RADIUS, self.WIDTH, self.HEIGHT)
        self.font = pygame.font.SysFont('Arial', 25)

        self.vertices, self.edges = None, None
        self._init_vertices()
        self._init_edges()
        self.is_occupied = False

    def host_bandit(self):
        self.image.fill((255, 255, 0))
        self.is_occupied = True

    def remove_bandit(self):
        self.image = pygame.transform.scale(self.TIPO2IMAGE[self.res], (self.WIDTH, self.HEIGHT))
        self.is_occupied = False

    def update(self):
        pass

    def _init_vertices(self):
        self.vertices = [
            Vertex(
                x=self.center_x + self.RADIUS * 2 * math.cos(angle),
                y=self.center_y + self.RADIUS * 2 * math.sin(angle),
                screen=self.screen,
                color=self.INIT_COLOR
            )
            for angle in self.ANGLES
        ]

    def _init_edges(self):
        self.edges = [
            Edge(
                start_pos=self.vertices[i].topleft,
                end_pos=self.vertices[(i + 1) % 6].topleft,
                color=self.INIT_COLOR
            )
            for i in range(6)
        ]

    def show_edges(self):
        for edge in self.edges:
            edge.show(screen=self.screen)

    def show_vertices(self):
        for vertex in self.vertices:
            vertex.show(screen=self.screen)

    def change_edge_color(self, i, color):
        self.edges[i].change_color(color)

    def change_vertex_color(self, i, color):
        self.vertices[i].change_color(color)

    def upgrade_vertex(self, i):
        self.vertices[i].upgrade()

    def show_no(self, color='red'):
        """显示在六边形的上半部"""
        self.screen.blit(
            self.font.render(f"{self.no}", True, pygame.Color(color)),
            (self.rect.x + self.G3 * self.RADIUS, self.rect.y - self.RADIUS / 2)
        )

    def chosen_one(self, color='blue', text='THIS!'):
        """被选中的tile上方显示color色的text字样"""
        self.screen.blit(
            self.font.render(text, True, pygame.Color(color)),
            (self.rect.x + self.G3 * self.RADIUS, self.rect.y - self.RADIUS)
        )

    def befriend_vertices_and_edges(self, vertex2edge: dict, vertex2adj: dict, edge2adj: dict, edge2incident: dict):
        """update the edges of each vertex, adjacents and incidents of each edge
        """
        for i, vertex in enumerate(self.vertices):
            vertex2edge.setdefault(vertex, set()).add(self.edges[i])
            vertex2edge.setdefault(vertex, set()).add(self.edges[i - 1])
            vertex2adj.setdefault(vertex, set()).add(self.vertices[i - 1])
            vertex2adj.setdefault(vertex, set()).add(self.vertices[(i + 1) % 6])

        for i, edge in enumerate(self.edges):
            edge2adj.setdefault(edge, set()).add(self.edges[i - 1])
            edge2adj.setdefault(edge, set()).add(self.edges[(i + 1) % 6])
            edge2incident.setdefault(edge, set()).add(self.vertices[i])
            edge2incident.setdefault(edge, set()).add(self.vertices[(i + 1) % 6])
