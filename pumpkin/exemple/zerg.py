# -*- coding: utf-8 -*-
from collections import ChainMap

object_cfg = {"color": "cian"}
layer_cfg = {"color": "red"}
cm = ChainMap(object_cfg, layer_cfg)
print(cm["color"])




