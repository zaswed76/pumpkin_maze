import pygame


def convert_color(color):
    if color is not None:
        if len(color) == 9:
            opacity = int(color[1:3], 16)
            cl = list(pygame.Color(color[0] + color[3:]))
            cl[3] = opacity
            return tuple(cl)
        else:
            return pygame.Color(color)

def get_color(*colors) -> hex:
    """

    :param colors: цвета в порядке приоритета
    :return: hex color возвращает первый же валидный цвет или
     если валидных цветов нет - false
    """

    for c in colors:
        try:
            pygame.Color(c)
        except ValueError as er:
            pass
            # print('{} - {}'.format(c, er))
        else:
            return c
    else:
        return False


if __name__ == '__main__':
    c = convert_color('#0055ff')
    print(c)