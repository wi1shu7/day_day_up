from os import system

a = lambda b: 'whoami'


@system
@a
class MyClass:
    pass


"""
测试部分
"""

b = lambda x: print(x)


@b
class MyClass2:
    pass
