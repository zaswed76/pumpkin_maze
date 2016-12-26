from os import path

EXT_MAP = '.json'
MAP_NAME = 'map'

RESOURCES = 'resources'
SETS = 'sets'
MAPS = 'maps'

root = path.dirname(__file__)
resources = path.join(root, RESOURCES)
tilesets = path.join(resources, SETS)
maps = path.join(root, MAPS)


def get_map(level):
    return path.join(maps, level, MAP_NAME + EXT_MAP)
