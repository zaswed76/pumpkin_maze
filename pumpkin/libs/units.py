import pygame
import math
from pygame.sprite import Sprite, Group, OrderedUpdates
from collections import OrderedDict
from libs import color

a = 1 if 1 else 3


class UGroup(OrderedUpdates):
    Door = 'door'
    Wall = 'wall'

    def __init__(self, name, *sprites):
        super().__init__(*sprites)
        self.type = name


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


class Platform(Sprite):
    def __init__(self, type, screen, image, x, y, gid, properties):
        super().__init__()
        self.properties = properties
        self.gid = gid
        self.type = type
        self.image = image
        self.screen = screen
        # Загрузка изображения корабля и получение прямоугольника.

        _, _, width, height = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(x, y, width, height)

        # print(self.gid, self.properties)

    def blitme(self):
        self.screen.blit(self.image, self.rect)


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

    def collisions(self, platforms, speed_x, speed_y):
        for p in platforms:

            if pygame.sprite.collide_rect(self, p):
                print(p.name)
                if p.name == 'walls':
                    if speed_x < 0:
                        self.rect.left = p.rect.right
                    elif speed_x > 0:
                        self.rect.right = p.rect.left
                    elif speed_y < 0:
                        self.rect.top = p.rect.bottom
                    elif speed_y > 0:
                        self.rect.bottom = p.rect.top
                elif p.name == 'doors':
                    if self.stats.level < self.stats.max_levels:
                        self.stats.level += 1
                        self.rect.right = 160
                        self.rect.bottom = 64


class Rect(Sprite):
    def __init__(self, screen, **cfg):
        super().__init__()
        self.name = cfg['name']

        self.color = color.get_color(cfg['properties']['color'])


        self.x = cfg['x']
        self.y = cfg['y']
        self.width = cfg['width']
        self.height = cfg['height']
        self.angle = cfg['rotation']
        self.screen = screen



        self.sur = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.color[3] < 255:
            self.sur.set_alpha(self.color[3])

        self.sur.fill(self.color)





    def draw(self, screen):
        """Вывод пули на экран."""

        # s = pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        screen.blit(self.sur, self.rect)


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