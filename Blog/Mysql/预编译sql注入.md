预编译处理语句

使用预编译相当于是将数据于代码分离的方式，把传入的参数绑定为一个变量，php中有两种方式，一种用?占位，一种用%s占位，Python中用%s占位，攻击者无法改变SQL的结构。

> **预处理防止sql注入的原理**
>
> 用户在向原有SQL语句传入值之前，原有SQL语句的语法树就已经构建完成，因此无论用户输入什么样的内容，都无法再更改语法树的结构，任何输入的内容都只会被当做值来看待，不会再出现非预期的查询

## 预编译中的sql注入

```sql
sql = "select username, passwd from user where id = %s"
cur.execute(sql, (2,))
```

上述情况下，是可以进行预编译的，因为被标记的位置是一个参数，也就是说他不构成语法结构

>对此的理解：
>
>语法结构就是不能给他用双引号包括的部分。
>
>如果一个参数不是int类型，例如string类型，那么他就能够被引号包裹，我对此的理解就是如果它能够被引号包围还能够正常运行的话，他就是一个参数，而列名，表名这些都无法被引号包围，所以我的理解就是他们构成了这条语句的语法结构

不可参数化的位置：

1. 表名、列名

2. order by、group by

   ```
   SELECT * FROM users ORDER BY %s;
   ```

3. limit

   ```
   SELECT * FROM Users LIMIT %s;
   ```

4. join

   ```
   SELECT columns FROM table1 INNER JOIN table2 ON table1.common_column = table2.common_column;
   ```

   

5. in

   ```
   SELECT * FROM user WHERE uid IN(1,2,'3','c')
   ```

   >in语法后面可以接子查询，所以我的理解就是不把他归类在可参数之中