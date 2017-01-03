# -*- coding: utf-8 -*-


lst = list(range(4))
lst2 = lst[::-1]
lst.extend(lst2[1:len(lst2)-1])
print(lst)

