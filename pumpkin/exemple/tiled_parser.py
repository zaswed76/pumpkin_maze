import json

with open('map1.json', "r") as f:
    conf = json.load(f)


for k, v in conf.items():
    print(k, v, sep=' = ')
    print('-----------------')

