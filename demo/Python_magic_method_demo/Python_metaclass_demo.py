class RestrictedMeta(type):
    def __new__(cls, name, bases, dct):
        print("RestrictedMeta -> new")
        # 在创建类对象之前执行一些操作，例如修改类属性
        if name == 'RestrictedClass':
            dct['secret'] = 42
        print(f"super(cls, cls).__new__(cls, name, bases, dct) -> {super(cls, cls).__new__(cls, name, bases, dct)}")
        print(f"cls.__mro__ -> {cls.__mro__}")
        return super(cls, cls).__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        print("RestrictedMeta -> init")
        if 'secret' not in dct:
            raise ValueError("Class must have a 'secret' attribute.")


class RestrictedClass(metaclass=RestrictedMeta):
    def __new__(cls, *args, **kwargs):
        # 创建一个新的对象实例
        instance = super().__new__(cls)
        print("RestrictedClass -> new")
        return instance


print("实例化 -> RestrictedClass")
RestrictedClass()

# class Restricted2Class(metaclass=RestrictedMeta):
#     secret = 43

# # 下面的代码会抛出 ValueError，因为没有定义 'secret' 属性
# try:
#     class AnotherClass(metaclass=RestrictedMeta):
#         pass
# except ValueError:
#     print("AnotherClass -> " + str(ValueError))
