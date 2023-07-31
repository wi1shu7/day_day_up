[TOC]

在Python中，`@`符号被用作修饰符的标志。修饰符用于修改函数、方法或类的行为，并且可以使代码更加简洁和易读。修饰符是Python的一个强大特性，可以在不修改原始函数或类的情况下，通过附加额外的功能来扩展其行为。

以下是`@`符号在Python中的常见用法：

- 函数修饰符：将修饰符应用于函数，用于增加或修改函数的功能。

```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```



- 类方法修饰符：将修饰符应用于类的方法，用于定义静态方法、类方法或属性。

```python
class MyClass:
    @staticmethod
    def static_method():
        print("This is a static method.")

    @classmethod
    def class_method(cls):
        print("This is a class method.")

    @property
    def my_property(self):
        return "This is a property."

MyClass.static_method()
MyClass.class_method()

my_instance = MyClass()
print(my_instance.my_property)
```



- 类修饰符：将修饰符应用于类，用于修改类的行为或特性。

```python
def add_method_to_class(cls):
    def hello(self):
        print("Hello from the class method!")
    cls.say_hello = hello
    return cls

@add_method_to_class
class MyClass:
    pass

my_instance = MyClass()
my_instance.say_hello()
```