from os import system


class x:
    def __getitem__(self, x):
        system(x)


# 上面这个写法可以改写为：
class x: pass
x.__getitem__ = system


x()["whoami"]