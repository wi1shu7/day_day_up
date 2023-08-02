// 按两次 Shift 打开“随处搜索”对话框并输入 `show whitespaces`，
// 然后按 Enter 键。现在，您可以在代码中看到空格字符。

import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Main {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException, IOException {
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
//            Process result = (Process)execMethod.invoke(runtimeInstance, "calc.exe");

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

        Class<?> clazz = Class.forName("java.lang.ProcessBuilder");
        ((ProcessBuilder)clazz.getConstructor(String[].class).newInstance(new String[][]{{"calc.exe"}})).start();
//        clazz.getMethod("start").invoke(clazz.getConstructor(String[].class).newInstance((Object[]) new String[]{"calc.exe"}));
        clazz.getMethod("start").invoke(clazz.getConstructor(String[].class).newInstance(new String[][]{{"calc.exe"}}));

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