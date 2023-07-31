import importlib
import SSTIclassdemo2


def shout1():
    print("all aw")
    return 'all aw'


class aw(object):

    def __init__(self):
        self.name = "aw"

    def shout2(self):
        print("aw")
        return 'aw'

    @staticmethod
    def s_shout2():
        print('static aw')
        return 'static aw'


class awtwo():

    def __init__(self):
        self.name = "aw two"

    def shout3(self):
        print("aw aw")
        return 'aw aw'


class test(dict):
    def __init__(self):
        print(super(test, self).keys.__class__.__call__(eval, '1+1'))
        # 如果是 3.x 的话可以简写为：
        print(super().keys.__class__)
        # super().keys.__class__.__call__(eval, '1+1')


if __name__ == "__main__":
    print(__file__ + " -> __builtins__ : " + str(type(__builtins__)))

    print('__import__' in dir(__builtins__))

    a = SSTIclassdemo2.awthree()
    del a.name
    importlib.reload(SSTIclassdemo2)
    test()

    import math
