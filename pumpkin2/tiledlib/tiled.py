import json
from pumpkin2 import paths
from pumpkin2.tiledlib.printer import *



class TileSets:
    def __init__(self, **sets):
        pass


class Tiled:
    def __init__(self):
        pass

    @staticmethod
    def load_map(pth_map: str) -> dict:
        with open(pth_map, "r") as f:
            return json.load(f)


if __name__ == '__main__':
    path_map = paths.get_map('level_1')
    maps = Tiled.load_map(path_map)
    # print_dict(maps)
    print('#######################')
    print_sets(maps['layers'][0]['objects'])