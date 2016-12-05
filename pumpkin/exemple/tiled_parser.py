

class A:
    def __init__(self):
        pass

    def update(self):
        print('update A')


class B(A):
    def __init__(self):
        super().__init__()

    def update(self):
        super().update()
        print('update B')


b = B()
b.update()
