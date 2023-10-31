[python的__get__、__set__、__delete__(1) - 丁壮 - 博客园 (cnblogs.com)](https://www.cnblogs.com/flashBoxer/p/9771797.html)

## 描述符

描述符本质就是一个新式类,在这个新式类中,至少实现了`__get__()`，`__set__()`，`__delete__()`中的一个,这也被称为描述符协议 　　

1. `__get__()`:调用一个属性时,触发
2. `__set__()`:为一个属性赋值时,触发
3. `__delete__()`:采用del删除属性时,触发

```python
class Descriptor:
    def __get__(self, instance, owner):
        print("Descriptor __get__()")
        return instance._value

    def __set__(self, instance, value):
        print("Descriptor __set__()")
        instance._value = value
	
    def __delete__(self, instance):
        print('Descriptor __delete__()')
        del instance._value
    
class MyClass:
    descriptor = Descriptor()

    def __init__(self):
        self._value = None
```

## 描述符的作用

描述符的作用是用来代理另外一个类的属性的(必须把描述符定义成这个类的类属性，不能定义到构造函数中)

```python
obj = MyClass()
obj.descriptor = 10  # 调用描述符的 __set__() 方法
print(obj.descriptor)  # 调用描述符的 __get__() 方法
```

## 描述符种类

1. 数据描述符：至少实现了`__get__()`和`__set__()`
2. 非数据描述符：没有实现`__set__()`

```python
#数据描述符
class Foo:
    def __set__(self, instance, value):
        print('set')
    def __get__(self, instance, owner):
        print('get')

#非数据描述符
class Foo:
    def __get__(self, instance, owner):
        print('get')
```

>- 描述符本身应该定义成新式类,被代理的类也应该是新式类
>- 必须把描述符定义成这个类的类属性，不能为定义到构造函数中
>- 要严格遵循该优先级,优先级由高到底分别是
>  1. 类属性
>  2. 数据描述符
>  3. 实例属性
>  4. 非数据描述符
>  5. 魔术方法`__getattr__()`
>
>```python
>import time
># 定义描述符
>class Desc_type: # 有__get__和__set__，为数据描述符
>    def __init__(self,key,value_type):             #传入key用来操作底层属性字典,value_type用来表示期望的数据类型
>        self.key = key
>        self.value_type = value_type
>    def __get__(self, instance, owner):
>        print('执行了__get__')
>        return instance.__dict__[self.key]              #return p2.name
>    def __set__(self, instance, value):
>        print('执行了__set__',self)
>        if not isinstance(value, self.value_type):                   #用来判断用户传入的是否符合要求
>            raise TypeError('%s 传入的不是 %s'%(self.key,self.value_type))      #抛出类型异常，提示用户程序终止
>        instance.__dict__[self.key] = value             #符合要求，则设置属性对应的值
>    def __delete__(self, instance):
>        print('执行了__delete__')
>        instance.__dict__.pop(self.key)
>
># 定义一个人的类（被代理的类）
>class People:
>    name = Desc_type('name', str)  # 用描述符代理了name这个属性，相当于执行了Desc_type中的self.__set__，同时People类中的name属性属于类属性
>    age = Desc_type('age', int)
>    salary = Desc_type('salary', float)
>    def __init__(self, name, age, salary):
>        self.name = name
>        self.age = age
>        self.salary = salary
>        self.time = time.time() # 定义在__init__()内，为实例属性
>
>p2 = People('Meanwey', 24, 11.1)
>
>#访问
>print(p2.name)
>
>#赋值
>p2.name = 'Jery'
>```

>### 注意事项
>
>- 描述符本身应该定义成新式类,被代理的类也应该是新式类
>
>- 必须把描述符定义成这个类的类属性，不能为定义到构造函数中
>
>- 要严格遵循该优先级,优先级由高到底分别是
>
>  - 1类属性
>  - 2数据描述符
>  - 3实例属性
>  - 4非数据描述符
>  - 5找不到的属性触发`__getattr__()`
>
>  
>
>五、描述符的应用

# [python的__get__、__set__、__delete__(1)](https://www.cnblogs.com/flashBoxer/p/9771797.html)

**内容:**
  **描述符引导**
    **摘要**
    **定义和介绍**
    **描述符协议**
    **调用描述符**
    **样例**
    **Properties**
    **函数和方法**
    **静态方法和类方法**
**摘要**
  定义并展示如何调用描述符,展示自定义描述符和几个内置的python描述符,包括函数、属性、静态方法和类方法,通过给出一个Python的示例应用来展示描述符是如何工作的.
  熟练掌握描述符不仅让你拥有python使用的额外技巧,并且可以加深对Python内部如何工作的理解,提升对程序设计的能力,而且体会到python的设计优雅之处

**定义和介绍**
  一般来说,描述符是带有“绑定行为”的对象属性,它的属性访问已经被描述符协议中的方法覆盖了.这些方法是__get__(),__set__(),和__delete__().
  如果一个对象定义了这些方法中的任何一个,它就是一个描述符.

  默认的属相访问是从对象的字典中 get, set, 或者 delete 属性,；例如a.x的查找顺序是:
  a.x -> a.__dict__['x'] -> type(a).__dict__['x'] -> type(a)的基类(不包括元类),如果查找的值是对象定义的描述方法之一,python可能会调用描述符方法来重载默认行为,
  发生在这个查找环节的哪里取决于定义了哪些描述符方法
  注意,只有在新式类中描述符才会起作用(新式类继承type或者object class)
  描述符是强有力的通用协议,属性、方法、静态方法、类方法和super()背后使用的就是这个机制,描述符简化了底层的c代码,并为Python编程提供了一组灵活的新工具


**描述符协议**



```
    descr.__get__(self, obj, type=None) -> value

    descr.__set__(self, obj, value) -> None

    descr.__delete__(self, obj) -> None
```


  定义任何上面三个方法的任意一个,这个对象就会被认为是一个描述符,并且可以在被作为对象属性时重载默认的行为, 如果一个对象定义了__get__() 和 __set__(),它被认为是一个数据描述符.只定义 __get__()被认为是非数据描述符,数据和非数据描述符的区别在于:如果一个实例的字典有和数据描述符同名的属性,那么数据描述符会被优先使用,如果一个实例的字典实现了无数据描述符的定义,那么这个字典中的属性会被优先使用,实现只读数据描述符,同时定义__get__()和__set__(),在__set__()中抛出AttributeError.

**描述符调用**

  描述符可以直接用方法名称调用,比如:d.__get__(obj)
   
  然而,描述符更常用的方式是属性访问时被自动调用,例如:obj.d 在obj的字典中查找d,如果d定义了方法__get__(),然后d.__get__(obj)会被通过下面的优先级列表调用
  详细的调用依赖于obj是一个对象还是一个类,不管哪种方式,描述符只工作在新式对象和类,如果一个类是object的子类(继承object),这个类就是一个新式类
   
  对于对象来说,object.__getattribute__() 把b.x 变为 type(b).__dict__['x'].__get__(b, type(b)) .优先级顺序:
  数据描述符 > 实例变量 > 非数据描述符,__getattr__()具有最低优先级(如果实现了的话),C语言的实现可以在 Objects/object.c 中 PyObject_GenericGetAttr() 查看.
   
  对于类来说,type.__getattribute__() 把 B.x 变为 B.__dict__['x'].__get__(None, B),代码实现为:
   

```
        def __getattribute__(self, key):
            "Emulate type_getattro() in Objects/typeobject.c"
            v = object.__getattribute__(self, key)
            if hasattr(v, '__get__'):
                return v.__get__(None, self)
            return v
```


  重点:
    描述符被__getattribute()方法调用
    重载__getattribute__()会阻止描述符自动调用
    __getattribute__()只适用于新式类和对象
    object.__getattribute__()和type.__getattribute__()对__get__()的调用不一样
    数据描述符会重载实例字典
    非数据描述符可能会被实例字典重载
     
   super()返回的对象会使用定制__getattribute__()方法来调用描述符,调用super(B, obj).m() 会在紧邻着B的基类A搜索obj.__class__.__mro__然后返回A.__dict__['m'].__get__(obj, B),如果不是一个描述符,返回未改变的m
   如果不在字典中,m会调用 object.__getattribute__() 查询

   注意:在python2.2,如果m是一个数据描述符,super(B, obj).m() 会调用__get__(),在python2.3,无数据描述符也会执行调用,除非是个旧式类,super_getattro() 的细节在Objects/typeobject.c中

   上面展示的是描述符在object, type, and super() 的 __getattribute__() 方法中的实现机制,继承object的类自动实现或者他们有一个元类提供类似的功能,同样,重载 __getattribute__()可以停止描述符的调用

**描述符例子**
  下面的代码创建了一个类,每次访问get或者set都会打印一条信息.重载__getattribute__()也可以使每个属性实现这一方法,然而,描述符在查看特定的属性时比较有用

```
        class RevealAccess(object):
            """A data descriptor that sets and returns values
               normally and prints a message logging their access.
            """

            def __init__(self, initval=None, name='var'):
                self.val = initval
                self.name = name

            def __get__(self, obj, objtype):
                print 'Retrieving', self.name
                return self.val

            def __set__(self, obj, val):
                print 'Updating', self.name
                self.val = val

        >>> class MyClass(object):
        ...     x = RevealAccess(10, 'var "x"')
        ...     y = 5
        ...
        >>> m = MyClass()
        >>> m.x
        Retrieving var "x"
        10
        >>> m.x = 20
        Updating var "x"
        >>> m.x
        Retrieving var "x"
        20
        >>> m.y
        5
```

  这个协议很简单却又可以提供令人为之一振的可能性.Properties, bound 和 unbound methods, 静态方法和 类方法 都是基于描述符协议

**Properties**
  调用property()是一种建立数据描述符的方便方法,可以在访问一个属性的时候触发方法的调用
  property(fget=None, fset=None, fdel=None, doc=None) -> property attribute

  下面展示一个定义管理属性x的典型的样例:

```
        class C(object):
            def getx(self):return self.__x
            def setx(self, value):self.__x = value
            def delx(self):del self.__x
            x = property(getx, setx, delx, "I'm the 'x' property.")
```

  property()使用纯python方式实现描述符:

```
        class Property(object):
            "Emulate PyProperty_Type() in Objects/descrobject.c"

            def __init__(self, fget=None, fset=None, fdel=None, doc=None):
                self.fget = fget
                self.fset = fset
                self.fdel = fdel
                if doc is None and fget is not None:
                    doc = fget.__doc__
                self.__doc__ = doc

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                if self.fget is None:
                    raise AttributeError("unreadable attribute")
                return self.fget(obj)

            def __set__(self, obj, value):
                if self.fset is None:
                    raise AttributeError("can't set attribute")
                self.fset(obj, value)

            def __delete__(self, obj):
                if self.fdel is None:
                    raise AttributeError("can't delete attribute")
                self.fdel(obj)

            def getter(self, fget):
                return type(self)(fget, self.fset, self.fdel, self.__doc__)

            def setter(self, fset):
                return type(self)(self.fget, fset, self.fdel, self.__doc__)

            def deleter(self, fdel):
                return type(self)(self.fget, self.fset, fdel, self.__doc__)
```


  当用户接口已经授权访问属性,这时候需求发生变化,property()可以提供便利, 例如,一个电子表格类可以通过单元（'b10'）授予对单元格值的访问权.这时候,对程序的后续改进要求在每次访问时重新计算单元格的值;然而,程序员不希望影响现有客户端代码.解决方案是在属性数据描述符中封装对value属性的访问：

```
        class Cell(object):
            . . .
            def getvalue(self):
                "Recalculate the cell before returning value"
                self.recalc()
                return self._value
            value = property(getvalue)
```


**函数和方法**
  python的面向对象是建立在函数的基础上,使用非数据描述符,两者会结合的非常紧密.

  类的字典将方法比作函数存储.在一个类的定义中,使用def和lambda来声明方法,这是用于创建函数的常用工具. 唯一不同之处,就是第一个参数用来表示对象实例,python约定,实例引用可以使self或者this或者其他变量名称

  为了支持方法调用,函数通过__get__()方法来实现属性访问时的方法绑定
  这说明所有的函数都是非数据描述符,它返回绑定或者非绑定方法依赖于它被对象还是类调用
   
  在python中的实现如下:



```
        class Function(object):
            . . .
            def __get__(self, obj, objtype=None):
                "Simulate func_descr_get() in Objects/funcobject.c"
                return types.MethodType(self, obj, objtype)
```


  在解释器中展示函数描述符如何运行:

```
        >>> class D(object):
        ...     def f(self, x):
        ...         return x
        ...
        >>> d = D()
        >>> D.__dict__['f']  # Stored internally as a function
        <function f at 0x00C45070>
        >>> D.f              # Get from a class becomes an unbound method
        <unbound method D.f>
        >>> d.f              # Get from an instance becomes a bound method
        <bound method D.f of <__main__.D object at 0x00B18C90>>
```


  输出说明绑定和未绑定方法是两种不同类型,PyMethod_Type在 Objects/classobject.c 中实际的C实现是一个具有有两种不同表现形式的单一对象,依赖于im_self是set还是null(等价C中的None)

  同样,调用方法对象的效果依赖于im_self,如果set(绑定),原函数(存储在im_func中)被调用,它的第一个参数设置为实例.
  如果unbound,所有的参数不做改变的传给原函数,instancemethod_call()的C实现因为包含一些类型检查会复杂一些

**静态方法和类方法**
  无数据描述符提供一种简单的机制将函数绑定为方法

  简单地说,函数的__get__()方法会将函数被作为属性访问时转换为方法,非数据描述符将 obj.f(*args) 调用为f(obj, *args).调用 klass.f(*args)变为f(*args)

  下面的表格汇总了绑定和它常见的两种变化

​    Transformation   Called from an Object   Called from a Class
​    function     　　f(obj, *args)      　　   f(*args)
​    staticmethod  　 f(*args)        　　　　f(*args)
​    classmethod     f(type(obj), *args)       f(klass, *args)

  调用c.f 或者 C.f等价于 object.__getattribute__(c, "f") 或者 object.__getattribute__(C, "f"),不管从对象还是类中,这个函数都可以访问到

  不需要self变量的方法适合使用静态方法
  例如:一个统计包可能包括用于实验数据的容器类,该类提供了用于计算依赖于数据的平均、平均值、中值和其他描述性统计数据的常规方法.可是可能有一些概念相关但不依赖数据的函数.
  例如:erf(x)是一个不依赖于特定数据集的函数,它可以从一个类或者函数调用:s.erf(1.5) --> .9332 或者 Sample.erf(1.5) --> .9332

  静态方法返回原始函数:

```
        >>> class E(object):
        ...     def f(x):
        ...         print x
        ...     f = staticmethod(f)
        ...
        >>> print E.f(3)
        3
        >>> print E().f(3)
        3
```


  python版本使用非数据描述符的实现方法:

```
        class StaticMethod(object):
            "Emulate PyStaticMethod_Type() in Objects/funcobject.c"

            def __init__(self, f):
                self.f = f

            def __get__(self, obj, objtype=None):
                return self.f
```


  与静态方法不同,类方法在调用函数之前先将类的引用预添加到参数列表中.调用者不管是对象还是类,这种格式是相同的

```
        >>> class E(object):
        ...     def f(x):
        ...         print x
        ...     f = staticmethod(f)
        ...
        >>> print E.f(3)
        3
        >>> print E().f(3)
        3
```


  这种行为在函数只需要有类引用且不关心任何底层数据的情况下是有用的,类方法的一个用途是用来创建不同的类构造器,在python2.3中,类方法dict.fromkeys()可以使用一个key的列表来创建字典,python的实现方式:



```
        class Dict(object):
            . . .
            def fromkeys(klass, iterable, value=None):
                "Emulate dict_fromkeys() in Objects/dictobject.c"
                d = klass()
                for key in iterable:
                    d[key] = value
                return d
            fromkeys = classmethod(fromkeys)
```



 

  现在可以这样创建一个字典:

```
        >>> Dict.fromkeys('abracadabra')
        {'a':None, 'r':None, 'b':None, 'c':None, 'd':None}
```


  classmethod()使用无数据描述符协议实现:



```
        class ClassMethod(object):
            "Emulate PyClassMethod_Type() in Objects/funcobject.c"

            def __init__(self, f):
                self.f = f

            def __get__(self, obj, klass=None):
                if klass is None:
                    klass = type(obj)
                def newfunc(*args):
                    return self.f(klass, *args)
                return newfunc
```

