# -*- coding: utf-8 -*-

def print_map(dct):
    print('#### BEGIN #####\n')
    for k, v in dct.items():
        print(k, v, sep=' = ')
        print('----------------------------')
    print('#### FINISH #####')


def layers(layers, name):
    for layer in layers:
        if layer['name'] == name:
            print('настройки слоя на котором находится объект')
            print_map(layer)

