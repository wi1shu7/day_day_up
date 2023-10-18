## 属性`__dict__`

`__dict__` 是 Python 中的一个特殊属性，它是一个字典，用于存储对象实例的所有属性和对应的值。

当你创建一个类的实例并给它赋予属性时，这些属性会被存储在对象实例的 `__dict__` 字典中。这样可以动态地为对象实例添加新的属性，而不需要在类定义中预先声明这些属性。

举个简单的例子：

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 创建一个 Person 实例
person = Person('Alice', 30)

# 给实例动态添加属性
person.address = '123 Street'

# 访问 __dict__ 查看实例的所有属性
print(person.__dict__)
# Output: {'name': 'Alice', 'age': 30, 'address': '123 Street'}
```

在这个例子中，`name` 和 `age` 属性是在 `__init__` 方法中赋值的，而 `address` 属性是在实例创建后动态添加的。所有这些属性都存储在对象实例的 `__dict__` 字典中。

可以直接通过 `__dict__` 字典对对象的属性进行访问、修改和删除。然而，直接操作 `__dict__` 并不是常见的做法，通常推荐使用点运算符 (`.`) 来访问对象的属性。

再举个例子

```python
class TestDict(object):

    a = 0
    b = 1

    def __init__(self):
        self.a = 2
        self.b = 3

    def test(self):
        print('a normal func.')

    @staticmethod
    def static_test():
        print('a static func.')

    @classmethod
    def class_test(self):
        print('a class func.')


if __name__ == '__main__':
    obj = TestDict()
    print('class __dict__:', TestDict.__dict__)
	# class __dict__: {'__module__': '__main__', 'a': 0, 'b': 1, '__init__': <function TestDict.__init__ at 0x0000013466102C10>, 'test': <function TestDict.test at 0x00000134073C1550>, 'static_test': <staticmethod object at 0x00000134074DBFD0>, 'class_test': <classmethod object at 0x00000134074DBFA0>, '__dict__': <attribute '__dict__' of 'TestDict' objects>, '__weakref__': <attribute '__weakref__' of 'TestDict' objects>, '__doc__': None}

    
    print('class obj __dict__:', obj.__dict__)
    # class obj __dict__: {'a': 2, 'b': 3}
```

- 类`__dict__`里存放类的静态函数、类函数、普通函数、全局变量以及一些内置的属性。
- 类实例`__dict__`里存放类的属性:self.xxx

## 方法`__setstate__()` 

`__setstate__()` 是 Python 中用于自定义反序列化过程的特殊方法。它允许在反序列化对象时对对象进行额外的处理和初始化。

当使用 Pickle 模块反序列化对象时，如果对象实现了 `__setstate__()` 方法，Pickle 将在反序列化后调用该方法，将反序列化的状态信息传递给对象，以便自定义对象的恢复过程。

方法签名如下：

```python
def __setstate__(self, state):
    # Custom deserialization logic
    pass
```

- `self`：对象实例。
- `state`：包含了反序列化的状态信息的字典或其他数据结构。

开发者可以在 `__setstate__()` 方法中根据自己的需求解析传递进来的状态信息，并据此初始化对象的属性。这允许进行一些定制的初始化操作，以确保对象在反序列化后的状态是正确的。

举个简单的例子：

```python
import pickle

class CustomObject:
    def __init__(self):
        self.value = 0

    def __setstate__(self, state):
        self.value = state.get('value', 0)

    def __repr__(self):
        return f'CustomObject(value={self.value})'

# Serialize an instance of CustomObject
original_object = CustomObject()
original_object.value = 42
serialized_object = pickle.dumps(original_object)

# Deserialize the object and invoke __setstate__()
deserialized_object = pickle.loads(serialized_object)
print(deserialized_object)  # Output: CustomObject(value=42)
```

在上面的例子中，`CustomObject` 实现了 `__setstate__()` 方法，用于在反序列化时根据传递的状态信息更新对象的属性。

## 方法`__reduce__()`



## 方法`__new__()`

`__new__`方法是 Python 中的一个特殊方法，用于创建对象。它是类的内置静态方法，负责在内存中为一个新对象分配空间，并返回该对象的引用。

在 Python 中，对象的创建通常是通过调用类的构造函数 `__init__` 实现的。`__init__` 方法用于对实例进行初始化操作，而 `__new__` 方法则用于实际的对象创建。

当我们创建一个类的实例时，Python 解释器会首先调用 `__new__` 方法来创建一个新的实例对象，并将该实例对象作为第一个参数传递给 `__init__` 方法。然后，`__init__` 方法在这个实例对象上执行初始化操作。

```python
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
"""
在 __new__ 方法中，使用 super().__new__(cls) 创建了一个新的对象实例，并返回该实例。然后，__init__ 方法被调用，用于初始化对象的属性。
"""
```

>```python
>class CapStr(str):
>def __new__(cls, *args):
>   self_in_init = super().__new__(cls, *args)
>   print("__new__ id -> " + str(id(self_in_init)))
>   print("__new__ args -> " + str(args))
>   return self_in_init
>
>def __init__(self, string):
>   print("__init__ string -> " + string)
>   print("__init__ id -> " + str(id(self)))
>
>
>a = CapStr("I love China!")
>print("a id -> " + str(id(a)))
>
>```
>
>__new__ id -> 1799333919200
>__new__ args -> ('I love China!',)
>__init__ string -> I love China!
>__init__ id -> 1799333919200
>a id -> 1799333919200
