import os

root = os.path.dirname(__file__)
resources = os.path.join(root, 'resources')
tilesets = os.path.join(resources, 'sets')
maps = os.path.join(root, 'maps')
css_path = lambda name: os.path.join(root, 'css', name)

icon_path = lambda direct, name, ext: os.path.join(resources, 'icons',
                                                   direct, name + ext)

forms = lambda form: os.path.join(root, 'gui/forms', form)

if __name__ == '__main__':
    pass
    # print(icon_path('32', 'name'))











'D:\save\serg\projects\pumpkin_maze\pumpkin\resources\icons\32\bottom.png'