import json
import os

TILESET_NUM = 0

class TiledParser:
    def __init__(self, json_map, tileset_num=TILESET_NUM):
        self.json_map = self.load_map(json_map)

    def load_map(self, level_map):
        with open(level_map, "r") as f:
            return json.load(f)

if __name__ == '__main__':
    from pumpkin import paths
    pth_map = os.path.join(paths.maps, 'map1.json')
    tmap =
