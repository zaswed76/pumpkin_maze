import pygame
from pygame.sprite import Sprite




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
        self.rect.right = 64
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
                if p.name == 'walls':
                    if speed_x < 0:
                        self.rect.left = p.rect.right
                    elif speed_x > 0:
                        self.rect.right = p.rect.left
                    elif speed_y < 0:
                        self.rect.top = p.rect.bottom
                    elif speed_y > 0:
                        self.rect.bottom = p.rect.top
                elif p.name == 'dors':
                    if self.stats.level < self.stats.max_levels:
                        self.stats.level += 1
                        self.rect.right = 64
                        self.rect.bottom = 64
