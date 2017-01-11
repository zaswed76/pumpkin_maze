# todo написать метод добывания пути к tilesets

import os
import re
tiled_path = '../../resources/sets/128-32.png'
root1 = r"D:/save/serg/projects/pumpkin_maze/pumpkin2"



# def get_path(rootw, tiled_set_image):
#     suff = os.path.realpath(tiled_set_image).replace(rootw, "").strip()
#     full = os.path.join(os.path.abspath(rootw), suff)
#     return full
#
# print(get_path(root1, tiled_path))

print(os.path.relpath(tiled_path))

tiled_path = '../../resources/sets/128-32.png'
pat = re.compile(r'^[\.]+[/]+')
print(pat.sub('', tiled_path, ), 55)