import pygame
import math
from pygame.sprite import Sprite, Group, OrderedUpdates
from collections import OrderedDict
from libs import color as _color


class UGroup(OrderedUpdates):
    Door = 'door'
    Wall = 'wall'

    def __init__(self, name, *sprites):
        super().__init__(*sprites)
        self.type = name

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
        # for s in self.sprites():
        #     s.draw(s.screen)


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


class TailObject(Sprite):
    def __init__(self, type, screen, rect, color=None, gid=None,
                 properties=None):
        super().__init__()
        x, y, width, height = rect
        if properties is None:
            self.properties = {}
        else:
            self.properties = properties
        self.color = color
        self.gid = gid
        self.type = type
        self.screen = screen
        self.border = self.properties.get('border', 0)
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


class Platform(Sprite):
    def __init__(self, type, screen, image, x, y, gid, properties):
        super().__init__()
        self.properties = properties
        self.gid = gid
        self.type = type
        self.image = image
        self.screen = screen
        # Загрузка изображения тайла и получение прямоугольника.

        _, _, width, height = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, stats, screen, speedx, speedy, x, y):
        """Инициализирует корабль и задает его начальную позицию."""

        super().__init__()
        self.up = self.down = self.left = self.right = False
        self.stats = stats
        self.move = True
        self.speedx = speedx
        self.speedy = speedy
        self.speed_x = 0
        self.speed_y = 0
        self.screen = screen
        # Загрузка изображения корабля и получение прямоугольника.
        self.image = pygame.image.load('resources/man.png')
        # self.image.set_colorkey((255, 255, 255))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.height = self.rect.height
        self.screen_rect = screen.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.right = 160
        self.rect.bottom = 64

        # Сохранение вещественной координаты центра корабля.
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def update(self, platforms):
        """Обновляет позицию корабля с учетом флага."""

        if self.right:
            self.speed_x = self.speedx

            self.rect.centerx += self.speed_x
            self.collisions(platforms, self.speed_x, 0)

        if self.left:
            self.speed_x = -self.speedx
            self.rect.centerx += self.speed_x
            self.collisions(platforms, self.speed_x, 0)
        if self.up:
            self.speed_y = -self.speedy
            self.rect.centery += self.speed_y
            self.collisions(platforms, 0, self.speed_y)
        if self.down:
            self.speed_y = self.speedy
            self.rect.centery += self.speed_y
            self.collisions(platforms, 0, self.speed_y)

        if not (
                            self.left or self.right or self.up or self.down):  # стоим, когда нет указаний идти
            self.speed_x = 0
            self.speed_y = 0

    def collisions(self, layers, speed_x, speed_y):
        for group in layers:
            # print(group.type)
            platform = pygame.sprite.spritecollideany(self, group)
            if platform:
                print(platform.rect.bottom)
                if speed_y < 0:
                    self.rect.top = platform.rect.bottom
                    # print(list(platforms)[0], '1111')
                    # for p in list(platforms)[0]:
                    #
                    #     if pygame.sprite.collide_rect(self, p):
                    #         print(p, 5555)
                    #         if p.name == 'walls':
                    #             if speed_x < 0:
                    #                 self.rect.left = p.rect.right
                    #             elif speed_x > 0:
                    #                 self.rect.right = p.rect.left
                    #             elif speed_y < 0:
                    #                 self.rect.top = p.rect.bottom
                    #             elif speed_y > 0:
                    #                 self.rect.bottom = p.rect.top
                    # elif p.name == 'doors':
                    #     if self.stats.level < self.stats.max_levels:
                    #         self.stats.level += 1
                    #         self.rect.right = 160
                    #         self.rect.bottom = 64


class FigureFabric(Sprite):
    alias_figure = {'rect': 'rectangle'}

    def __init__(self, screen, color: hex, figure_type: str, **cfg):
        super().__init__()
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
        self.border = self.properties.get('border', 0)
        self.angle = cfg['rotation']
        self.screen = screen
        polyline = cfg.get('polyline')
        if polyline is not None:
            self.sx = cfg['x']
            self.sy = cfg['y']
            self.fx = polyline[1]['x']
            self.fy = polyline[1]['y']
        else:
            self.sx = 0
            self.sy = 0
            self.fx = 0
            self.fy = 0
        self.draw_figure(self.type)

    def __call__(self, *args, **kwargs):
        return self.surface

    def draw_figure(self, figure):
        # try:
            getattr(self, figure)(self.screen, self.x, self.y,
                                  self.width,
                                  self.height, self.color)
        # except AttributeError as err:
        #
        #     print('фигру - {} рисовать не умею'.format(figure))
        #     raise Exception(err)

    def rectangle(self, screen, x, y, width, height, color, *args):
        self.surface = TailObject(1, screen, (x, y, width, height),
                                  color, properties=self.properties)

    def line(self, screen, x, y, width, height, color):
        print('line')
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
