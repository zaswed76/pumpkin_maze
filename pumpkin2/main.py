import os
import sys

import pygame

from exemples.test_level.game_status import Status
from exemples.test_level import levels as lv

status = Status()







def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Name Game")
    # Запуск основного цикла игры.



    root = os.path.dirname(__file__)
    level = lv.Level(screen, root)




    while True:
        # Отслеживание событий клавиатуры и мыши.
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_1:
                status.level = 0
                print(status.level)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_2:
                status.level = 1
                print(status.level)
        screen.fill(pygame.Color('#D8D8D8'))

        
        # Отображение последнего прорисованного экрана.

        level.draw(screen)
        pygame.display.flip()

run_game()
