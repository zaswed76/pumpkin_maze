from os import path as __path

__EXT_MAP = '.json'
__MAP_NAME = 'map'

__RESOURCES = 'resources'
__SETS = 'sets'
__EXSETS = 'exsets'
__MAPS = 'maps'

root = __path.dirname(__file__)
resources = __path.join(root, __RESOURCES)
tilesets_dir = __path.join(resources, __SETS)
exsets = __path.join(resources, __EXSETS)
maps = __path.join(root, __MAPS)

def get_exsets(img):
    return __path.join(exsets, img)


def get_map(level):
    return __path.join(maps, level, __MAP_NAME + __EXT_MAP)
