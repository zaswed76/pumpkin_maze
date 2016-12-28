# -*- coding: utf-8 -*-

source_lst = [
    {'email': 'user1@mail.ru', 'name': 'name1', 'count': 1},
    {'email': 'user1@mail.ru', 'name': 'name1', 'count': 1},
    {'email': 'user1@mail.ru', 'name': 'name1', 'count': 1},
    {'email': 'user1@mail.ru', 'name': 'name1', 'count': 1},
     {'email': 'user2@mail.ru', 'name': 'name1', 'count': 1},
     {'email': 'user2@mail.ru', 'name': 'name1', 'count': 1},
     {'email': 'user2@mail.ru', 'name': 'name1', 'count': 1},
     {'email': 'user3@mail.ru', 'name': 'name1', 'count': 1},
     {'email': 'user3@mail.ru', 'name': 'name1', 'count': 1},
     {'email': 'user3@mail.ru', 'name': 'name1', 'count': 1}
]

d2 = [{'email': 'user1@mail.ru', 'name': 'name1', 'count': 2},
      {'email': 'user2@mail.ru', 'name': 'name1', 'count': 1},
      {'email': 'user3@mail.ru', 'name': 'name1', 'count': 1}]









def uniq(source, key):
    target_dct = dict()
    for data in source_lst:
        if data[key] in target_dct:
            target_dct[data[key]]['count'] += 1
        else:
            target_dct[data[key]] = data
    return target_dct.values()

print(uniq(source_lst, 'email'))





