import pygame
from pygame.sprite import Sprite


class GameObject(Sprite):
    Door = 'door'
    Wall = 'wall'

    def __init__(self, *groups):
        super().__init__(*groups)

class ImagePlatform(GameObject):
    def __init__(self, group, screen, image, x, y, count, properties,
                 portal=None):
        """
        :param portal tuple < (int, int, int, str)
        (id текущей двери, уроветь перехода, id двери перехода, направление?)
        ?направление - 'up', 'down', 'left', 'right' - куда должен двигаться игрок что бы пройти дверь
        :param group:
        :param screen:
        :param  :
        :param x:
        :param y:
        :param count: номер спрайта на карте. начало от 0
        :param properties:
        """
        super().__init__()
        if portal is not None:
            self.id = portal[0]
            self.portal = portal[1:]
        else:
            self.id = self.portal = None
        self.group = group


        self.properties = properties
        self.count = count

        self.type = group.class_name
        self.image = image
        self.screen = screen
        # Загрузка изображения тайла и получение прямоугольника.

        _, _, width, height = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def __repr__(self):
        return '{}\n{}'.format(self.__class__.__name__, self.properties)

