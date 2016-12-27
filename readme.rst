игра pumpkin_maze
=================

__version__ = '0.1.0'
---------------------

master
------

Платформер бродилка по коридорам с исползованием pygamе

Уровни создаются с помощью Tiled Map Editor Версия 0.17.1

Карта - ортогональная.

Формат слоя тайлов - scv.

FLIP

Excelent!
So the flags in the MSB (most significant byte) seem to be :
0x80 - flip X
0x40 - flip Y
0x20 - flip diagonally

or in rotations (clockwise)
0xA0 - 90 degrees
0xC0 - 180 degrees
0x60 - 270 degrees

thanks