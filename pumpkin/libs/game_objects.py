import pygame
import math
from pygame.sprite import Sprite, Group, OrderedUpdates
from collections import OrderedDict
from libs import color as _color
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


class AbsSprite(Sprite):
    def __init__(self, screen, image, alpha=False, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(image).convert_alpha()

        self.screen = screen
        self.rect = self.image.get_rect()

    def update(self, *args):
        pass

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Background(AbsSprite):
    def __init__(self, screen, image, x, y, speed, *groups):
        super().__init__(screen, image, *groups)
        self.speed = speed
        self.name = 'Background'
        self.rect.x = x
        self.rect.y = y
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

    def draw(self, screen):
        self.screen.blit(self.image, self.rect)

    def update(self, *args):
        if self.speed:
            self.center_x += self.speed
        self.rect.centerx = self.center_x


class Background2(Background):
    def __init__(self, screen, image, x, y, speed, *groups):
        super().__init__(screen, image, x, y, speed, *groups)

    def update(self, *args):
        if self.speed:
            self.center_y += self.speed
        self.rect.centery = self.center_y




class FigureRect(GameObject):
    def __init__(self, screen, rect, color=None, gid=None,
                 border=0):
        super().__init__()
        x, y, width, height = rect

        self.color = color
        self.gid = gid
        self.screen = screen
        self.border = border
        # Загрузка изображения тайла и получение прямоугольника.


        self.surface = pygame.Surface((width, height),
                                      pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, width, height)
        if self.color[3] < 255:
            self.surface.set_alpha(self.color[3])
        self.surface.fill(color)

    def draw(self, screen):
        if self.surface is not None:
            if self.border:
                return pygame.draw.rect(screen, self.color, self.rect,
                                        self.border)
            else:
                return screen.blit(self.surface, self.rect)

class TailObject(GameObject):
    alias_figure = {'rect': 'rectangle'}

    def __init__(self, screen, color: hex, figure_type: str, layer_properties, **cfg):
        super().__init__()
        self.layer_properties = layer_properties

        self.surface = None
        self.name = cfg.get('name', 'noname')
        self.color = _color.convert_color(color)

        self.type = self.alias_figure.get(figure_type, figure_type)
        self.id = cfg['id']
        self.x = cfg['x']
        self.y = cfg['y']
        self.width = cfg['width']
        self.height = cfg['height']
        self.properties = cfg.get('properties', {})
        self.border = self.properties.get('border', self.layer_properties.get('border', 0))

        self.angle = cfg['rotation']
        self.screen = screen

        self.create_figure(self.type)

    def __call__(self, *args, **kwargs):
        return self.surface

    def create_figure(self, figure):
        getattr(self, figure)(self.screen, self.x, self.y,
                              self.width,
                              self.height, self.color)


    def rectangle(self, screen, x, y, width, height, color, *args):
        self.surface = FigureRect(screen, (x, y, width, height),
                                  color, border=self.border)

    def line(self, screen, x, y, width, height, color):

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)

    def draw(self, screen):
        self.surface.draw(self.screen)
        # self.line = pygame.draw.line(screen, self.color, (self.sx, self.sy),
        #                              [self.fx,self.fy], 3)
        # s = pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # try:
        #     screen.blit(self.sur, self.rect)
        # except AttributeError:
        #     print('units.FigureFabric.draw() AttributeError -error')
        #     pass


        # def c_rotate(self, s, angle):
        #     s = pygame.transform.rotate(s,angle)
        #     return s
        #
        # def rot_center(self, image, angle):
        #     """rotate an image while keeping its center and size"""
        #     orig_rect = image.get_rect()
        #     rot_image = pygame.transform.rotate(image, angle)
        #     rot_rect = orig_rect.copy()
        #     rot_rect.center = rot_image.get_rect().center
        #     rot_image = rot_image.subsurface(rot_rect).copy()
        #     return rot_image
        #
        # def rot_center2(self, image, rect, angle):
        #         a = b = rect.width/2
        #         c = math.sqrt((a ** 2) + (b ** 2))
        #         print(c, a, 'gep')
        #         """rotate an image while keeping its center"""
        #         rot_image = pygame.transform.rotate(image, angle)
        #         cx = c + a
        #         cy = (rect.centery/2) + b/2
        #         rot_rect = rot_image.get_rect(center=(cx, cy))
        #         print(rect.x, rect.y)
        #         return rot_image,rot_rect
