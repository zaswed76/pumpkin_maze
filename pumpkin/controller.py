import sys
import pygame


class Player:
    def __init__(self):
        print('init')
        self._up = self._down = self._left = self._right = False

    @property
    def up(self):
        return self._up

    @property
    def down(self):
        return self._down

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right
    @up.setter
    def up(self, bool):
        print('up')
        self._up = bool

    @down.setter
    def down(self, bool):
        self._down = bool

    @left.setter
    def left(self, bool):
        self._left = bool

    @right.setter
    def right(self, bool):
        self._right = bool

class Controller:
    def __init__(self, game_stat, player=Player, level=()):
        """

        :type player: pygame.sprite.Sprite
        """

        self.game_stat = game_stat
        if player is None:
            pass
        else:
            player = player

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                self.mouse_collide(x, y, level)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                self.game_stat.increase_level()
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
            if e.type == pygame.KEYUP and e.key == pygame.K_1:
                self.game_stat.level = 0
            if e.type == pygame.KEYUP and e.key == pygame.K_2:
                self.game_stat.level = 1
    def mouse_collide(self, x, y, level):
        print(level)



