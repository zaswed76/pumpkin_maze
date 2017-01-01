# -*- coding: utf-8 -*-




tiles = {
   "1":
      {
       "image":"..\/..\/resources\/exsets\/8246060_orig.jpg"
      },
   "2":
      {
       "image":"..\/..\/resources\/exsets\/100x50x4.png"
      }
  }


st = sorted(tiles.items(), key=lambda item: item[0])
res = []
for t in st:
    res.append(t[1]['image'])
print(res)