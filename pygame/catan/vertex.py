import pygame

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
        self.image = pygame.image.load("../images/catan/empty.jpeg")
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.color = color
        self.edges = list()

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

    def __hash__(self):
        return self.topleft

    def __eq__(self, other):
        return self.topleft == other.topleft
