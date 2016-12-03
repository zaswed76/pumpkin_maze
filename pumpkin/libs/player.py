import sys
import pygame
from pygame.sprite import Sprite
from libs.sprites import GameObject


class Player(Sprite):
    def __init__(self, stats, screen, speedx, speedy, x, y):
        """Инициализирует корабль и задает его начальную позицию."""

        super().__init__()
        self.directs = dict.fromkeys(('up', 'down', 'left', 'right'),
                                     False)

        self.game_stat = stats
        self.move = True
        self.speedx = speedx
        self.speedy = speedy
        self.speed_x = 0
        self.speed_y = 0
        self.screen = screen
        # Загрузка изображения корабля и получение прямоугольника.
        self.image = pygame.image.load('resources/man.png')

        self.image.convert_alpha()
        # self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect.height = self.rect.height
        self.screen_rect = screen.get_rect()

        # Каждый новый появляется здесь
        self.rect.right = 160
        self.rect.bottom = 64

        # Сохранение вещественной координаты центра игрока.
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def go_right(self):
        self.speed_x = self.speedx
        self.rect.centerx += self.speed_x

    def go_left(self):
        self.speed_x = -self.speedx
        self.rect.centerx += self.speed_x

    def go_up(self):
        self.speed_y = -self.speedy
        self.rect.centery += self.speed_y

    def go_down(self):
        self.speed_y = self.speedy
        self.rect.centery += self.speed_y

    def stand(self):
        self.speed_x = 0
        self.speed_y = 0

    def update(self, platforms, level=()):

        if self.directs['right']:
            self.go_right()
            self.collisions(platforms, level, self.speed_x, 0)

        elif self.directs['left']:
            self.go_left()
            self.collisions(platforms, level, self.speed_x, 0)

        elif self.directs['up']:
            self.go_up()
            self.collisions(platforms, level, 0, self.speed_y)

        elif self.directs['down']:
            self.go_down()
            self.collisions(platforms, level, 0, self.speed_y)

        # стоим, когда нет указаний идти
        if not (self.directs['left'] or self.directs['right'] or
                    self.directs['up'] or self.directs['down']):
            self.stand()

    def _go_portal(self, platform, level, speed_x, speed_y, id_door,
                   lv):
        """
        переход игрока на указанный уровень к указанной двери с
        нужной стороны
        :param platform:
        :param level:
        :param speed_x:
        :param speed_y:
        :param id_door:
        :param lv:
        """
        print(platform)
        level.clear()
        self.game_stat.level = lv
        level.create_levels(self.game_stat.level)
        for l in level:
            for nm, lay in l.all_layers.items():
                if nm == GameObject.Door:
                    for spr in lay.sprites():
                        print(spr.id, id_door)
                        if spr.id == id_door:
                            #  влево <<<<
                            if speed_x < 0:
                                self.rect.right = spr.rect.left
                                self.rect.centery = spr.rect.centery
                            # вправо >>>
                            elif speed_x > 0:
                                self.rect.left = spr.rect.right
                                self.rect.centery = spr.rect.centery
                            # вверх ^
                            if speed_y < 0:
                                self.rect.bottom = spr.rect.top
                                self.rect.centerx = spr.rect.centerx
                            # вниз v
                            elif speed_y > 0:
                                self.rect.top = spr.rect.bottom
                                self.rect.centerx = spr.rect.centerx

    def stand_before_wall(self, speed_x, speed_y, platform):
        if speed_x < 0:
            self.rect.left = platform.rect.right
        elif speed_x > 0:
            self.rect.right = platform.rect.left
        elif speed_y < 0:
            self.rect.top = platform.rect.bottom
        elif speed_y > 0:
            self.rect.bottom = platform.rect.top

    def collisions(self, layers, level, speed_x, speed_y):
        for group in layers:
            platform = pygame.sprite.spritecollideany(self, group)
            if platform:
                if group.class_name == GameObject.Wall:
                    self.stand_before_wall(speed_x, speed_y, platform)
                elif group.class_name == GameObject.Door:
                    if platform.portal is None:
                        print(platform.portal, 222)
                        self.stand_before_wall(speed_x, speed_y,
                                               platform)
                        print('эта дверь никуда не ведёт')
                        return
                    print(platform.portal, 222)
                    # id двери, уровень перехода,
                    id_door, lv, direction = platform.portal
                    if self.directs[direction]:
                        print('go')
                        self._go_portal(platform, level, speed_x,
                                        speed_y, id_door, lv)
                    else:
                        self.stand_before_wall(speed_x, speed_y,
                                               platform)
