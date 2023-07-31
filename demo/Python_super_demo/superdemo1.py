class Base:
    def __init__(self):
        print('Base.__init__')
    def shout(self):
        print("shout base")

class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')
    def shout(self):
        print("shout A")

class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')
    def shout(self):
        print("shout B")


class C(Base):
    def __init__(self):
        super().__init__()
        print('C.__init__')
    def shout(self):
        print("shout C")

class D(A, B, C):
    def __init__(self):
        super(B).__init__()
        super(B, self).__init__()  # self是B的子类D的实例
        super(B, self).shout()
        print('D.__init__')


D()

print(D.mro())
