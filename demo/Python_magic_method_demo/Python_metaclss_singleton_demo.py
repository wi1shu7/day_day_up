class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        print("SingletonMeta -> __call__")
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class SingletonClass(metaclass=SingletonMeta):
    def __init__(self, value):
        print("SingletonClass -> __init__")
        self.value = value

obj1 = SingletonClass(42)
obj2 = SingletonClass(99)

print(obj1 is obj2)  # 输出：True，因为 obj1 和 obj2 引用的是同一个实例
print(obj1.value)    # 输出：42
print(obj2.value)    # 输出：42
