import sys
import pygame


class Controller:
    def __init__(self, player):
        self.player = player

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                player.up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                player.down = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                player.left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                player.right = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                print('space')

            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                player.up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                player.down = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                player.right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                player.left = False