import pygame
import math
from pygame.sprite import Sprite, Group, OrderedUpdates
from collections import OrderedDict

from libs.sprites import GameObject



class Inventory(OrderedUpdates):
    def __init__(self, *sprites, **kwargs):
        super().__init__(*sprites)

    @property
    def check_breaks(self):
        for v in self.sprites():
            if v.breaks:
                return True
        else:
            return False

    def __repr__(self):
        return '{}'.format(self.sprites())


class OrderedGroupLayer(OrderedUpdates):
    def __init__(self, name, class_name, properties):
        """

         группа с сохранением порядка добавления
        :param name: имя слоя
        :param class_name: тип слоя (пользовательские свойства)
        :param properties: (пользовательские свойства)
        :param sprites: pygame.sprites
        """
        super().__init__()
        self.properties = properties
        print(self.properties, 'properties11111111111111111111111')

        self.doors_portal = (
            eval(self.properties.get('doors', '{}')))
        self.name = name
        print(self.name, 'name')
        self.class_name = class_name
        print(self.class_name, 'class name')

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for s in self.sprites():
            r = spritedict[s]
            newrect = s.draw(s.screen)
            if r:
                if newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                else:
                    dirty_append(newrect)
                    dirty_append(r)
            else:
                dirty_append(newrect)
            spritedict[s] = newrect
        return dirty


class AllLayers(OrderedDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw(self, screen):
        for lay in self.values():
            lay.draw(screen)
            lay.update(screen)

    def get_groups(self):
        return self.values()


