import pygame

from Vector import Vector


class GameObjectRect:
    def __init__(self, x, y, width, height, colour: str = "black"):
        self.vector = Vector(x, y)
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = pygame.Rect(self.vector.get_tuple(), (self.width, self.height))

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

    def update(self):
        pass


# TODO: learn pygame sprites
