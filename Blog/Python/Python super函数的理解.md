[TOC]

### MRO

方法解析顺序（Method Resolution Order），简称 MRO

Python 发展至今，经历了以下 3 种 MRO 算法，分别是：

1. 从左往右，采用深度优先搜索（DFS）的算法，称为旧式类的 MRO；
2. 自 Python 2.2 版本开始，新式类在采用深度优先搜索算法的基础上，对其做了优化；
3. 自 Python 2.3 版本，对新式类采用了 C3 算法。由于 Python 3.x 仅支持新式类，所以该版本只使用 C3 算法。

#### 旧式类MRO算法

在使用旧式类的 MRO 算法时，以下面代码为例:

```python
class A:
    def method(self):
        print("CommonA")
class B(A):
    pass
class C(A):
    def method(self):
        print("CommonC")
class D(B, C):
    pass

D().method()
```

通过分析可以想到，此程序中的 4 个类是一个“菱形”继承的关系，当使用 D 类对象访问 method() 方法时，根据深度优先算法，搜索顺序为`D->B->A->C->A`。

旧式类的 MRO 可通过使用`inspect`模块中的`getmro(类名)`函数直接获取。例如 `inspect.getmro(D)` 表示获取 D 类的 MRO。

因此，使用旧式类的 MRO 算法最先搜索得到的是基类 A 中的`method()`方法，即在 Python 2.x 版本中，此程序的运行结果为：

```
CommonA
```

但是，这个结果显然不是想要的，我们希望搜索到的是 C 类中的`method()`方法。

#### 新式类MRO算法

为解决旧式类 MRO 算法存在的问题，Python 2.2 版本推出了新的计算新式类 MRO 的方法，它仍然采用从左至右的深度优先遍历，但是如果遍历中出现重复的类，只保留最后一个。

仍以上面程序为例，通过深度优先遍历，其搜索顺序为`D->B->A->C->A`，由于此顺序中有 2 个 A，因此仅保留后一个，简化后得到最终的搜索顺序为`D->B->C->A`。

新式类可以直接通过 `类名.__mro__ `的方式获取类的 MRO，也可以通过 `类名.mro()` 的形式，旧式类是没有` __mro__` 属性和`mro() `方法的。

可以看到，这种 MRO 方式已经能够解决“菱形”继承的问题，但是可能会违反单调性原则。所谓单调性原则，是指在类存在多继承时，子类不能改变基类的 MRO 搜索顺序，否则会导致程序发生异常。

例如，分析如下程序：

```python
class X(object):
    pass
class Y(object):
    pass
class A(X,Y):
    pass
class B(Y,X):
    pass
class C(A, B):
    pass
```

通过进行深度遍历，得到搜索顺序为`C->A->X->object->Y->object->B->Y->object->X->object`，再进行简化（相同取后者），得到`C->A->B->Y->X->object`

下面来分析这样的搜索顺序是否合理，我们来看下各个类中的 MRO：

- 对于 A，其搜索顺序为 A->X->Y->object；
- 对于 B，其搜索顺序为 B->Y->X->object；
- 对于 C，其搜索顺序为 C->A->B->X->Y->object。

可以看到，B 和 C 中，X、Y 的搜索顺序是相反的，也就是说，当 B 被继承时，它本身的搜索顺序发生了改变，这违反了单调性原则。

#### MRO C3

[为解决 Python 2.2 中 MRO 所存在的问题，Python 2.3 采用了 C3 方法来确定方法解析顺序。多数情况下，如果某人提到 Python 中的 MRO，指的都是 C3 算法。那么，C3 算法是怎样实现的呢？](https://www.zhihu.com/tardis/zm/art/416584599?source_id=1005)

### super函数

在Python中，`super()`函数常用于调用父类（超类）的方法。这个函数有两种常见的使用方式：一种是在子类中调用父类的方法，另一种是在任何地方调用指定类的父类或兄弟类的方法。下面我将详细解释四种情况：

1. `super()`不传参数：这种情况下，`super()`通常在类的方法内部使用，用来引用父类的方法。这种方式下，Python会自动将`self`和当前的类传给`super()`。例如：

   ```python
   class MyParentClass(object):
       def __init__(self):
           print("Parent init")
   
   class SubClass(MyParentClass):
       def __init__(self):
           super().__init__()
           print("Subclass init")
   ```

   在这个例子中，`SubClass`的`__init__`方法通过`super().__init__()`调用了`MyParentClass`的`__init__`方法。

2. `super()`传一个参数：`super()`只传递一个参数时，是一个不绑定的对象，不绑定的话它的方法是不会有用的

   ```python
   class Base:
       def __init__(self):
           print('Base.__init__')
   
   class B(Base):
       def __init__(self):
           super().__init__()
           print('B.__init__')
   
   class C(Base):
       def __init__(self):
           super().__init__()
           print('C.__init__')
   
   
   class D(B, C):
       def __init__(self):
           super(B).__init__()  # 值传递一个参数
           print('D.__init__')
   
   D()
   
   print(D.mro())
   """
   结果
   D.__init__
   [<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.Base'>, <class 'object'>]
   """
   ```

   

3. `super()`传一个类对象和一个实例对象参数：在这种情况下，`super(class, obj)`函数将返回一个临时对象，这个对象绑定的是指定类的父类或兄弟类的方法。obj必须是class的实例或者是子类的实例。例如：

   ```python
   class A:
       def __init__(self):
           print("A's init invoked")
   
   class B(A):
       def __init__(self):
           print("B's init invoked")
   
   class C(B):
       def __init__(self):
           print("C's init invoked")
           super(B, self).__init__()
   
   c = C()
   ```

   在这个例子中，`C`的`__init__`方法通过`super(B, self).__init__()`调用了`A`的`__init__`方法，而不是`B`的`__init__`方法。

4. `super()`传两个类对象参数：`super(class1, class2) `这种情况下，第一个参数通常是子类，第二个参数是父类，用于获取子类的兄弟类。这种用法比较少见，但在处理复杂的类继承关系时可能会用到。例如：

   ```python
   class A:
       def who_am_i(self):
           print("I am A")
   
       @staticmethod
       def shout():
           print('shout A')
   
   class B(A):
       def who_am_i(self):
           print("I am B")
   
       @staticmethod
       def shout():
           print('shout B')
   
   class C(A):
       def who_am_i(self):
           print("I am C")
   
       @staticmethod
       def shout():
           print('shout C')
   
   class D(B, C):
       def who_am_i(self):
           print("I am D")
           print('super(B, D).who_am_i -> ' + str(type(super(B, D).who_am_i)))
           print('super(B, self).who_am_i -> ' + str(type(super(B, self).who_am_i)))
           super(B, D).who_am_i(self)
           super(B, D).shout()
           super(B, self).who_am_i()
   
   d = D()
   d.who_am_i()
   """
   结果
   I am D
   super(B, D).who_am_i -> <class 'function'>
   super(B, self).who_am_i -> <class 'method'>
   I am C
   shout C
   I am C
   """
   ```

   在这个例子中，`D`的`who_am_i`方法通过`super(B, self).who_am_i()`调用了`C`的`who_am_i`方法，而不是`B`的`who_am_i`方法。`super()`传递两个类class1和class2时，得到的也是一个绑定的super对象，但这需要class2是class1的子类，且如果调用的方法需要传递参数时，必须手动传入参数，因为super()第二个参数是类时，得到的方法是函数类型的，使用时不存在自动传参，第二个参数是对象时，得到的是绑定方法，可以自动传参。

super本身其实就是一个类，`super()`其实就是这个类的实例化对象，它需要接收两个参数 `super(class, obj)`,它返回的是`obj`的MRO中`class`类的父类，举个例子：

```python
class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')

class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')


class C(Base):
    def __init__(self):
        super().__init__()
        print('C.__init__')

class D(A, B, C):
    def __init__(self):
        super(B, self).__init__()  # self是B的子类D的实例
        print('D.__init__')

D()
print(D.mro())
"""
Base.__init__
C.__init__
D.__init__
[<class '__main__.D'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.Base'>, <class 'object'>]
"""
```

`super(B, self).__init__()`:

`super`的作用是 **返回的是`obj`的MRO中`class`类的父类**,在这里就表示**返回的是`D`（也就是`self`）的MRO中`B`类的父类**：

1. 返回的是`d`的MRO：`(D, A, B, C, Base, object)`
2. 中`B`类的父类：`C`