

import sys
import pygame
from pygame.sprite import Group

from pumpkin2.exemples.test_level.game_status import Status
from pumpkin2.exemples.test_level import levels as lv

status = Status()
levels = lv.Levels()
def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.
    rect_1 = (0,0,100,100)
    rect_1_color = (255,0,0)
    pygame.draw.rect(screen, rect_1_color, rect_1)
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
        # pygame.draw.rect(screen, rect_1_color, rect_1)
        levels.draw(status.level)
        pygame.display.flip()

run_game()
