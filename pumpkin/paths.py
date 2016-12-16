import os

root = os.path.dirname(__file__)
resources = os.path.join(root, 'resources')
tilesets = os.path.join(resources, 'sets')
maps = os.path.join(root, 'maps')
css_path = lambda name: os.path.join(root, 'css', name)