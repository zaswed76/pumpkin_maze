

class Buss:
    def __init__(self, lst = []):
        self.lst = lst

    def sdd(self, pas):
        self.lst.append(pas)


a = Buss()
b = Buss()

a.sdd('serg')
print(b.lst)