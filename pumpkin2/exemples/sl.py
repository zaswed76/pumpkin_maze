# -*- coding: utf-8 -*-


from pumpkin2.tiledlib import *

# простой пример
from collections import namedtuple

Point = namedtuple('Point', ['y'])
p = Point(11, 22)     # создаём экземпляр с позиционными или именованными аргументами
             # поля доступны и по именам

                # метод __repr__ с форматом name=value
print(p)

import sys
from PyQt5 import QtWidgets

QtWidgets.QLabel

