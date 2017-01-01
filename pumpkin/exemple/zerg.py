# -*- coding: utf-8 -*-


class A:
    def __init__(self, **kwargs):
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        if self.x is not None:
            assert isinstance(self.x, int), 'должно быть числом'
            print(self.x, 'x')
        elif self.y is not None:
            assert isinstance(self.y, str), 'должно быть строкой'
            print(self.y, 'y')
        else:
            raise Exception('параметры не определены')


a = A(x='')
print(a.y)

