import json

class _Tiled:
    def __init__(self):
        pass


    @property
    def empty_options(self):
        return [k for k, v in self.__dict__.items() if v is None]


    def __repr__(self):
        return '{}'.format(self.__class__.__name__)

class TileSet(_Tiled):
    def __init__(self, tset):
        super().__init__()

        self.columns = tset.get("columns")
        self.firstgid = tset.get("firstgid")
        self.margin = tset.get("margin")
        self.name = tset.get("name")
        self.properties = tset.get("properties")
        self.spacing = tset.get("spacing")
        self.tilecount = tset.get("tilecount")
        self.tileheight = tset.get("tileheight")
        self.tileproperties = tset.get("tileproperties")
        self.tilepropertytypes = tset.get("tilepropertytypes")
        self.tiles = tset.get("tiles")
        self.tilewidth = tset.get("tilewidth")


    def __repr__(self):
        s = super().__repr__()
        z = '{}'.format(self.image)
        return " - ".join((s, z))

class ImageSet(_Tiled):
    def __init__(self, tset):
         super().__init__()
         self.columns = tset.get("columns")
         self.firstgid = tset.get("firstgid")
         self.image = tset.get("image")
         self.imageheight = tset.get("imageheight")
         self.imagewidth = tset.get("imagewidth")
         self.margin = tset.get("margin")
         self.name = tset.get("name")

         self.tilecount = tset.get("tilecount")
         self.tileheight = tset.get("tileheight")
         self.tileoffset = tset.get("tileoffset")
         self.tilewidth = tset.get("tilewidth")

    def __repr__(self):
        s = super().__repr__()
        z = '{}'.format(self.image)
        return " - ".join((s, z))



class TileSets:
    type_sets = dict(image=ImageSet, tile=TileSet)
    def __init__(self, sets: list):
        self.sets = []
        self.create_sets(sets)

    def create_sets(self, sets):
        for s in sets:
            self.sets.append(self.type_sets.get(s['properties']['class'])(s))


    def __repr__(self):
        # return str(self.sets)
        return "\n".join([str(x) for x in self.sets])






class AbcTiled(_Tiled):
    """
    обёртка над словарём предсставляющем карту Tiled Map Editor
    """

    def __init__(self, map_dict: dict):
        # all layers
        """

        :param map_dict: www
        """

        super().__init__()
        self.layers = map_dict.get("layers")
        # Stores the next available ID for new objects.
        self.nextobjectid = map_dict.get("nextobjectid")
        self.orientation = map_dict.get("orientation")
        self.renderorder = map_dict.get("renderorder")
        self.tileheight = map_dict.get("tileheight")
        self.tilesets = TileSets(map_dict.get("tilesets"))
        self.tilewidth = map_dict.get("tilewidth")
        self.tilewidth = map_dict.get("tilewidth")
        self.version = map_dict.get("version")
        self.width = map_dict.get("width")
        self.properties = map_dict.get("properties")
        self.backgroundcolor = map_dict.get("backgroundcolor")
        self.propertytypes = map_dict.get("propertytypes")
        self.height = map_dict.get("height")

    def __str__(self):
        return '''  class - {}
  layers - {}
  user_properties - {}
  width - {} tiles
  height - {} tiles'''.format(self.__class__.__name__,
                              len(self.layers),
                              self.properties,
                              self.width,
                              self.height)

    @staticmethod
    def load_map(pth_map: str) -> dict:
        """

        :param pth_map: path to json map
        :return: map < dict
        """
        with open(pth_map, "r") as f:
            return json.load(f)




if __name__ == '__main__':
    from pumpkin2 import paths
    path_map = paths.get_map('level_1')
    maps = AbcTiled.load_map(path_map)

    # print_dict(maps)
    # layer = maps['layers'][0]
    # print_dict(layer)
    # objects = layer['objects']
    # print_list(objects)
    # print('#######################')
    # print_sets(maps['layers'][0]['objects'])
