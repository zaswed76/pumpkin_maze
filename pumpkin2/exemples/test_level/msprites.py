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
        if isinstance(image, str):
            self.surface = pygame.image.load(image).convert_alpha()
        elif isinstance(image, pygame.Surface):
            self.surface = image
        else:
            raise TypeError('не тот тип изображения')
        self.rect = self.surface.get_rect()



    def draw(self, screen):
        surface_blit = screen.blit
        return surface_blit(self.surface, self.rect)


class Rect:
    def __init__(self, **kwargs):
        self.surface = pygame.Surface(kwargs['size'])
        self.surface.fill(pygame.Color(kwargs['color']))
        self.rect = self.surface.get_rect()
        self.rect.x = kwargs['pos'][0]
        self.rect.y = kwargs['pos'][1]

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
    def __init__(self, sprite_object, **kwargs):
        super().__init__()
        self.sprite_object = sprite_object(**kwargs)

    def set_pos(self, pos):
        self.sprite_object.rect.x = pos[0]
        self.sprite_object.rect.y = pos[1]

    @property
    def image(self):
        return self.sprite_object.surface

    @property
    def rect(self):
        return self.sprite_object.rect

    def draw(self, screen):
        return self.sprite_object.draw(screen)









