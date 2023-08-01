class MyClass:
    def __new__(cls, *args, **kwargs):
        # 创建一个新的对象实例
        instance = super().__new__(cls)
        print("Creating a new instance.")
        return instance

    def __init__(self, x):
        self.x = x
        print("Initializing the instance.")

obj = MyClass(42)

