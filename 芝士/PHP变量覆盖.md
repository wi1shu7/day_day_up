[TOC]

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

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230717004044838.png)

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