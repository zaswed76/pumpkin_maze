# -*- coding: utf-8 -*-



class Lst:
    def __init__(self, lst=None):
        self.lst = []
        if lst is not None:
            self.lst.extend(lst)

    def __getitem__(self, key):
        if isinstance(key, slice):
            print(key.start, '!!!')
            return self.lst[key]
        else:
            print(111)

    def __repr__(self):
        return str(self.lst)


lst = Lst([1, 2, 3])
print(lst[0:2])


