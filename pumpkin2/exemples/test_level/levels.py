# -*- coding: utf-8 -*-

import sys
import pygame
from pygame.sprite import Group
from pumpkin2.exemples.test_level import msprites as spr

def lvss():
    lvs = list()
    lvs.append(spr.ABCSprite(spr.Rect, size=(50, 50), pos=(0, 0), color='green'))
    lvs.append(spr.ABCSprite(spr.Rect, size=(50, 50), pos=(110, 110), color='red'))
    return lvs
class Levels(list):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.__create_levels()

    def __create_levels(self):
        for lv in lvss():
            group = Group()
            group.add(lv)
            self.append(group)


    def draw(self, level):
        print(level)
        self[level].draw(self.screen)