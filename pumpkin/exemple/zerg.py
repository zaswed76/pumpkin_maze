# -*- coding: utf-8 -*-


class A(list):
    def __init__(self):
        super().__init__()
a = A()
print(isinstance(a, list))
print(isinstance(A(), list))



