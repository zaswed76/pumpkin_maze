import pygame
import math
from pygame.sprite import Sprite, Group, OrderedUpdates
from collections import OrderedDict

from libs.sprites import GameObject





class OrderedGroupLayer(OrderedUpdates):
    def __init__(self, name, class_name, properties, *sprites):
        """

        :param name: имя слоя
        :param class_name: тип слоя (пользовательские свойства)
        :param sprites: pygame.sprites
        """
        super().__init__(*sprites)
        self.properties = properties

        self.doors_portal = (
            eval(self.properties.get('doors', '{}')))
        self.name = name
        self.class_name = class_name

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


