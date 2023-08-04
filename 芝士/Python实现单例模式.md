[TOC]

### 1. 使用函数装饰器

```python
from functools import wraps

def singleton(cls):
    instances = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

# 1部分
@singleton
class MyClass:
    pass

# 2部分
MyClass()
MyClass()
MyClass()
```

>调用装饰器的阶段是在类的定义阶段而不是对类进行实例化的阶段，所以在1部分的时候将类传进装饰器函数`singleton`中，而不是在2部分才将类传进装饰器函数，所以在定义阶段，`MyClass`就已经被赋成`singleton`里面的`wrapper`函数，这就导致`wrapper`在会被分配内存，从而使其中的变量`instances`一直存在
>
>
>
>在这段代码中，`instances`是`singleton`函数的局部变量，但由于Python的闭包特性，它会在`singleton`函数返回的`wrapper`函数中被保留下来。
>
>闭包是指一种函数，它记住了自己被定义时的环境。在这个例子中，`wrapper`函数就是一个闭包，它记住了`singleton`函数的环境，包括`instances`这个变量。所以，即使`singleton`函数运行完成之后，`instances`变量并不会被销毁，而是会被`wrapper`函数持续引用。
>
>当你下一次实例化`MyClass`的时候，`wrapper`会被调用，`instances`里依然会存在上次存储的类实例。这是因为`instances`是一个字典，用于存储已经实例化过的类和对应的实例。当你尝试实例化一个类时，`wrapper`首先会检查这个类是否已经在`instances`中，如果是，就直接返回对应的实例；否则，它会创建一个新的实例，存入`instances`，然后返回这个新的实例。这就是所谓的单例模式，保证一个类只有一个实例。
>
>所以，虽然`instances`在`singleton`函数中定义为局部变量，但由于闭包的特性，它在函数运行完成后并不会被销毁，而是会被保留下来，用于在后续的类实例化中保证单例模式。

### 2. 使用基类

使用基类 way实现单例,类继承该基类即可:

*[这里](#元类)

```python
class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None 

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance

class Foo(metaclass=Singleton):
    ...
```

### 3. 模块级实例

因为模块天然是单例的,可以直接实现:

```python
# foo.py
class Foo:
  ...

instance = Foo()
```

导入这个模块的其它地方都可以访问instance。

### 4. 共享属性

类的属性是共享的,可以用于单例:

```python
class Foo(object):
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Foo, cls).__new__(cls)
        return cls._instance
```

这些是 Python 实现单例的一些常见方式。每种方式有不同的优劣,可以根据需求选择。