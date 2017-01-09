# -*- coding: utf-8 -*-


import pygame
import sys
from pygame.sprite import Sprite, Group


class MGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def draw(self, surface):
        sprites = self.sprites()
        for spr in sprites:
            rect = spr.draw(surface)
            self.spritedict[spr] = rect
        self.lostsprites = []

class Image:
    def __init__(self, **kwargs):
        image = kwargs['image']
        self.surface = pygame.image.load(image).convert_alpha()
        self.rect = self.surface.get_rect()

    def draw(self, screen):
        surface_blit = screen.blit
        return surface_blit(self.surface, self.rect)


class Rect:
    def __init__(self, **kwargs):
        self.surface = pygame.Surface((50,50))
        self.surface.fill((255, 255, 0))
        self.rect = self.surface.get_rect()

    def draw(self, screen):
        return screen.blit(self.surface, self.rect)

class Circle:
    def __init__(self, **kwargs):
        self.surface = kwargs['surface']
        self.color = kwargs['color']
        self.pos = (100, 100)
        self.radius = kwargs['radius']

        self.surface = pygame.Surface((100, 100),
                                      pygame.SRCALPHA)
        self.surface.fill((255, 255, 0))
        self.rect = self.surface.get_rect()

    def draw(self, screen):
        return pygame.draw.circle(screen, self.color, self.pos, self.radius, 0)

class ABCSprite(Sprite):
    def __init__(self, figure, **kwargs):
        super().__init__()
        self.figure = figure(**kwargs)

    @property
    def image(self):
        return self.figure.surface

    @property
    def rect(self):
        return self.figure.rect

    def draw(self, screen):
        return self.figure.draw(screen)


class MySprite(ABCSprite):
    def __init__(self, figure, **kwargs):
        super().__init__(figure, **kwargs)



def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.
    group = MGroup()

    a = ABCSprite(Circle, surface=screen, color=(255, 0, 0), radius=45)
    # a = ABCSprite(Image, image='cloud.png')
    group.add(a)
    while True:
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Отображение последнего прорисованного экрана.
        screen.fill(pygame.Color('#D8D8D8'))
        group.draw(screen)
        pygame.display.flip()

run_game()







