class A:
    def who_am_i(self):
        print("I am A")

    @staticmethod
    def shout():
        print('shout A')

class B(A):
    def who_am_i(self):
        print("I am B")

    @staticmethod
    def shout():
        print('shout B')

class C(A):
    def who_am_i(self):
        print("I am C")

    @staticmethod
    def shout():
        print('shout C')

class D(B, C):
    def who_am_i(self):
        print("I am D")
        print('super(B, D).who_am_i -> ' + str(type(super(B, D).who_am_i)))
        print('super(B, self).who_am_i -> ' + str(type(super(B, self).who_am_i)))
        super(B, D).who_am_i(self)
        super(B, D).shout()
        super(B, self).who_am_i()

d = D()
d.who_am_i()