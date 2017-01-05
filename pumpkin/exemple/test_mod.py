

class A:
    def __init__(self):
        self.x = "a"

    def title(self):
        return self.x.title()

class B:
    def __init__(self, y):
        self.y = y
        self.a = A()

    def title(self):
        return self.a.title()


a = A()
print(a.title())

b = B('r')
print(b.title())

