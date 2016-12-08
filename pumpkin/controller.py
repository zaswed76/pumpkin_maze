import sys
import pygame



class Player:
    def __init__(self):

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

class KeyAlias:
    def __init__(self):
        self.levels = {
            1: pygame.K_1,
            2: pygame.K_2,
            3: pygame.K_3,
            4: pygame.K_4,
            5: pygame.K_5,
            6: pygame.K_6,
            7: pygame.K_7,
            8: pygame.K_8,
            9: pygame.K_9
        }

class Controller(KeyAlias):
    
    def __init__(self, game_stat, player=Player, level=()):
        """

        :type player: pygame.sprite.Sprite
        """

        super().__init__()
        self.game_stat = game_stat
        if player is None:
            pass
        else:
            player = player
        # print(player)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                self.mouse_collide(x, y, level)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                player.directs['up'] = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                player.directs['down'] = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                player.directs['left'] = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                player.directs['right'] = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                pass


            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                 player.directs['up'] = False
            if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                player.directs['down'] = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                player.directs['right'] = False
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                player.directs['left'] = False

            self.set_level(e, level)

    def set_level(self, e, level):
        for key, pygame_key in self.levels.items():
            if e.type == pygame.KEYDOWN and e.key == pygame_key:
                level.clear()
                self.game_stat.level = key-1
                level.create_levels(self.game_stat.level)



    def mouse_collide(self, x, y, level):
        print(x,y)
        for lay in level:
            for n, l in lay.all_layers.items():
                for z in l:
                    clicked = z.rect.collidepoint(x, y)
                    if clicked:
                        print(z, '!!!!!!!!!!!!!!!!!!!!!!!!!!!')



