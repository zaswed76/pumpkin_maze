# todo написать метод добывания пути к tilesets

import os
import re
tiled_path = '../../resources/sets/128-32.png'
root1 = r"D:\0SYNC\python_projects\games\Games\pumpkin_maze\pumpkin2"



def get_path(dir_name, base_name):
    lst = []
    for root, dirs, files in os.walk(dir_name):  # пройти по директории рекурсивно
        for name in files:
            fullname = os.path.join(root, name)  # получаем полное имя файла
            if base_name in fullname:
                lst.append(fullname) # делаем что-нибудь с ним
    return lst

print(get_path(root1, os.path.basename((tiled_path))))