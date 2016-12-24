from os import path

EXT_MAP = '.json'
MAP_NAME = 'map'

root = path.dirname(__file__)
resources = path.join(root, 'resources')
tilesets = path.join(resources, 'sets')
maps = path.join(root, 'maps')

get_map = lambda level: path.join(maps, level, MAP_NAME+EXT_MAP)