

import sys
import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite
from pumpkin2.exemples.test_level.game_status import Status
from pumpkin2.exemples.test_level import levels as lv

status = Status()

class FigureRect(Sprite):
    def __init__(self, group, screen, rect, color, border, id):
        super().__init__()
        self.group = group
        x, y, width, height = rect
        self.color = color
        self.id = id
        self.screen = screen
        self.border = border
        # Загрузка изображения тайла и получение прямоугольника.


        self.surface = pygame.Surface((width, height),
                                      pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, width, height)
        if self.color[3] < 255:
            self.surface.set_alpha(self.color[3])
        self.surface.fill(color)
        # self.group.add(self.surface)

    def draw(self, screen):
        print(2222)
        if self.surface is not None:
            if self.border:
                return pygame.draw.rect(screen, self.color, self.rect,
                                        self.border)
            else:
                return screen.blit(self.surface, self.rect)




def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.
    levels = lv.Levels(screen)
    group = Group()
    f = FigureRect(group, screen, (0, 0, 50, 50), (255, 0, 0, 100), 0, 0)

    while True:
        # Отслеживание событий клавиатуры и мыши.
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_1:
                status.level = 1
            if e.type == pygame.KEYDOWN and e.key == pygame.K_2:
                status.level = 2
        screen.fill(pygame.Color('#D8D8D8'))
        # Отображение последнего прорисованного экрана.
        f.draw(screen)
        levels.draw(status.level)
        pygame.display.flip()

run_game()
