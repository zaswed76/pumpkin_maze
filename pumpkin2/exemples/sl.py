# -*- coding: utf-8 -*-




# простой пример
from collections import namedtuple

Point = namedtuple('Point', ['y'])
p = Point(11, 22)     # создаём экземпляр с позиционными или именованными аргументами
             # поля доступны и по именам

                # метод __repr__ с форматом name=value
print(p)


