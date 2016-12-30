
from pumpkin2.tiledlib import abctiled


class Tiled(abctiled.AbcTiled):
    """
    класс представляет карту сгенерированую Tiled Map Editor,
    где атрибуты соответствуют ключам словаря сгенерированой карты
    """
    def __init__(self, map_dict: dict, sets_dir: str, **kwargs):
        """
         карта в виде словаря
        :param sets_dir: путь к каталогу с тайлсетами
        :param map_dict:
        :param kwargs:
        """
        super().__init__(map_dict, sets_dir)
        self.sets_dir = sets_dir



if __name__ == '__main__':
    from pumpkin2 import paths
    path_map = paths.get_map('level_1')
    maps = Tiled.load_map(path_map)
    sets_dir = paths.exsets
    tiled_map = Tiled(maps, sets_dir)
    print(tiled_map.tilesets)

