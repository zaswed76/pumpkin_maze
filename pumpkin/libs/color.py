import pygame


def get_color(color) ->tuple:
    """

    :param color: hex color
    :return:
    """
    if len(color) == 9:
        opacity = int(color[1:3], 16)
        cl = pygame.Color(color[0] + color[3:])

        return (cl, opacity)
    else:
        return pygame.Color((color)), None

if __name__ == '__main__':
    c = get_color('#000000')
    print(c)