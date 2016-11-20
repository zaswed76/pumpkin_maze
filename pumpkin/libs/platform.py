import pygame
from pygame.sprite import Sprite


class Platform(Sprite):
    def __init__(self, screen, image, x, y):
        super().__init__()
        self.image = image
        self.screen = screen
        # Загрузка изображения корабля и получение прямоугольника.

        _, _, width, height = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(x, y, width, height)




    def blitme(self):
        self.screen.blit(self.image, self.rect)

