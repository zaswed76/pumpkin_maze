import pygame
from pygame.sprite import Sprite
from libs import color as _color


class AbcSprite(Sprite):
    def __init__(self):
        super().__init__()



class GameObject(Sprite):
    Door = 'door'
    Wall = 'wall'
    Thing = 'thing'

    def __init__(self, group, screen, image, x, y, count):
        """

        :param group:
        :param screen:
        :param image:
        :param x:
        :param y:
        :param count: номер тайла на карте начиная с 0, слева направо
        """
        super().__init__()

        self.group = group
        self._count = count
        self.type = group.class_name
        self.image = image
        self.screen = screen
        # Загрузка изображения тайла и получение прямоугольника.

        _, _, width, height = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(x, y, width, height)

    @property
    def count(self):
        return self._count

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def __repr__(self):
        return '''
        type - {}
        count - {}
        group - {}

        '''.format(self.type, self.count, self.group.name)


class Weapon(GameObject):
    def __init__(self, group, screen, image, x, y, properties, count):
        super().__init__(group, screen, image, x, y, count)
        self.damage = properties.get('damage', 0)
        self.breaks = properties.get('breaks', False)
        self.name = properties.get('name', 'weapon')

    def __repr__(self):
        print(super().__repr__())
        return 'name - {}; breaks = {}; damage = {}'.format(self.name, self.breaks, self.damage)


class Armor(GameObject):
    def __init__(self, group, screen, image, x, y, count):
        super().__init__(group, screen, image, x, y)


class CreateThings:
    th = dict(weapon=Weapon, armor=Armor)

    def __init__(self, group, screen, image, x, y, count, properties):
        self.properties = properties
        self.group_properties = group.properties
        self.create_thing(self.properties['subclass'], group, screen,
                          image, x, y, count, properties)
        group.add(self.thing)

    def create_thing(self, thing, group, screen, image, x, y, count,
                     properties,
                     portal=None, *groups):
        self.thing = self.th[thing](group, screen, image, x, y,
                                    properties, count)


class CreateImagePlatform(GameObject):
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

        super().__init__(group, screen, image, x, y, count)
        self.group_properties = group.properties
        self._count = count

        if portal is not None:
            self.id = portal[0]
            self.portal = portal[1:]
        else:
            self.id = self.portal = None
        group.add(self)


class AbsBackGround(Sprite):
    def __init__(self, group, screen, image, alpha=False, *groups):
        super().__init__()
        self.group = group
        self.image = pygame.image.load(image).convert_alpha()
        self.screen = screen
        self.rect = self.image.get_rect()

        self.group.add(self)


    def update(self, *args):
        pass

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Background(AbsBackGround):
    def __init__(self, group, screen, image, x, y, speed):

        super().__init__(group, screen, image)
        self.speed = speed
        self.name = 'Background'
        self.rect.x = x
        self.rect.y = y
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

    def draw(self, screen):
        self.screen.blit(self.image, self.rect)

    def update(self, *args):
        if self.speed:
            self.center_x += self.speed
        self.rect.centerx = self.center_x


class Background2(Background):
    def __init__(self, screen, image, x, y, speed, group):
        super().__init__(group, screen, image, x, y, speed)

    def update(self, *args):
        if self.speed:
            self.center_y += self.speed
        self.rect.centery = self.center_y


class FigureRect(Sprite):
    def __init__(self, group, screen, rect, color, border, id):
        super().__init__()
        x, y, width, height = rect
        self.color = color
        self.id = id
        self.screen = screen
        self.border = border
        # Загрузка изображения тайла и получение прямоугольника.


        self.surface = pygame.Surface((width, height),
                                      pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, width, height)
        if self.color[3] < 255:
            self.surface.set_alpha(self.color[3])
        self.surface.fill(color)

    @property
    def count(self):
        return self.rect

    def draw(self, screen):
        if self.surface is not None:
            if self.border:
                return pygame.draw.rect(screen, self.color, self.rect,
                                        self.border)
            else:
                return screen.blit(self.surface, self.rect)


class CreateFigure(Sprite):
    figures = {'rect': FigureRect}

    def __init__(self, group, screen, object, layer_properties,
                 user_layer_properties):
        super().__init__()
        self.user_layer_properties = user_layer_properties
        self.layer_properties = layer_properties
        self.object = object
        self.group = group
        self.screen = screen
        self.object_user_properties = self.object.get('properties',
                                                      {})

        self.id = self.object['id']

        self.surface = self.figures[self.figure_type](group, screen, self.rect, self.color, self.border, self.id)
        group.add(self.surface)

    @property
    def rect(self):
        return (self.x, self.y, self.width, self.height)

    @property
    def x(self):
        return self.object['x']

    @property
    def y(self):
        return self.object['y']

    @property
    def width(self):
        return self.object['width']

    @property
    def height(self):
        return self.object['height']

    @property
    def figure_type(self):
        object_type = self.object.get('type')
        if object_type:
            return object_type
        else:
            return self.user_layer_properties.get('figure_type', {})

    @property
    def color(self):
        object_color = self.object_user_properties.get('color')
        if object_color:
            return _color.convert_color(object_color)
        else:
            return _color.convert_color(
                self.layer_properties.get('color'))

    @property
    def border(self):
        object_border = self.object_user_properties.get('border', 0)
        if object_border:
            return object_border
        else:
            return self.layer_properties.get('border', 0)

    def draw(self, screen):
        self.surface.draw(self.screen)

            # print(self.figure_type, 'self.figure_type!!!!!!!!!!!!!!!!!!')
            # if not self.figure_type:
            #     raise Exception('не указан тип фигуры')
            # print(self.figure_type)

            #     self.create_figure(self.type)
            #
            # def __call__(self, *args, **kwargs):
            #     return self.surface
            #
            # def create_figure(self, figure):
            #     getattr(self, figure)(self.screen, self.x, self.y,
            #                           self.width,
            #                           self.height, self.color)
            #
            # def rectangle(self, screen, x, y, width, height, color, *args):
            #     self.surface = FigureRect(screen, (x, y, width, height), None,
            #                               color=color, border=self.border)
            #
            # def line(self, screen, x, y, width, height, color):
            #     self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            #     self.image.fill(color)
            #

            # self.line = pygame.draw.line(screen, self.color, (self.sx, self.sy),
            #                              [self.fx,self.fy], 3)
            # s = pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # try:
            #     screen.blit(self.sur, self.rect)
            # except AttributeError:
            #     print('units.FigureFabric.draw() AttributeError -error')
            #     pass


            # def c_rotate(self, s, angle):
            #     s = pygame.transform.rotate(s,angle)
            #     return s
            #
            # def rot_center(self, image, angle):
            #     """rotate an image while keeping its center and size"""
            #     orig_rect = image.get_rect()
            #     rot_image = pygame.transform.rotate(image, angle)
            #     rot_rect = orig_rect.copy()
            #     rot_rect.center = rot_image.get_rect().center
            #     rot_image = rot_image.subsurface(rot_rect).copy()
            #     return rot_image
            #
            # def rot_center2(self, image, rect, angle):
            #         a = b = rect.width/2
            #         c = math.sqrt((a ** 2) + (b ** 2))
            #         print(c, a, 'gep')
            #         """rotate an image while keeping its center"""
            #         rot_image = pygame.transform.rotate(image, angle)
            #         cx = c + a
            #         cy = (rect.centery/2) + b/2
            #         rot_rect = rot_image.get_rect(center=(cx, cy))
            #         print(rect.x, rect.y)
            #         return rot_image,rot_rect
