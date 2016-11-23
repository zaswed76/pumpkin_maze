
import pygame

pygame.init()
screen = pygame.display.set_mode(
        (500, 500))
class SubSprite:
    def __init__(self, image, width, height):
        self.image = image
        self.height = height
        self.width = width
        self.sprite = pygame.image.load(image).convert_alpha()
        self.sprite_rect = self.sprite.get_rect()
        self.w_count = self.sprite_rect.width // self.width

        self.h_count = self.sprite_rect.height // self.height


    def get_coord(self, n, width, height, w_count):
        n_y = n // w_count
        x = width * int(n - (n_y * w_count))
        y = height * n_y
        return x, y

    def get_sprite(self, n):
        x, y = self.get_coord(n, self.width, self.height, self.w_count)
        return self.sprite.subsurface((x, y, self.width, self.height))

    def get_sprites(self, s=0, count=None):
        if count is None:
            f = self.w_count * self.h_count
        else: f = s + count + 1
        return [self.get_sprite(x) for x in range(s, f)]

    def get_sprites_back(self, n=None):
        if n is None:
            n = int(self.w_count)
        lst = list(range(n))
        lst.extend(sorted(range(n), reverse=1))
        return [self.get_sprite(x) for x in lst]

    def get_sprite_time(self, s, t):
        return [(x, t) for x in s]

    def __repr__(self):
        return '''
        class - {}
        tileset - {}
        self.w_count - {}
        self.h_count - {}
        size - ({}, {})

        '''.format(self.__class__, self.image, self.w_count,
                   self.h_count, self.width, self.height)

if __name__ == '__main__':
    sub = SubSprite(r'D:\0SYNC\python_projects\games\Games\pumpkin_maze\pumpkin\resources\DungeonCrawl_ProjectUtumnoTileset.png', 32, 32)
    print(sub.get_sprites())