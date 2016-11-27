import pygame


def get_color(color):
    print(len(color), '1111111111111111111')
    if len(color) == 9:
        opacity = int(color[1:3], 16)
        cl = list(pygame.Color(color[0] + color[3:]))
        cl[3] = opacity
        return tuple(cl)
    else:
        return pygame.Color(color)

if __name__ == '__main__':
    c = get_color('#000000')
    print(c)