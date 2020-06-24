#### RDBMS(relational database management system)关系型数据库，包括mysql，oracle
mysql图形界面：navicat（解压后删除.navicat64，取消安装wine）

* 数据类型：INT，CHAR（max_char_number),一般用VARCHAR（动态大小），TEXT（0-65535字节），decimal（5， 2）共存5位数，2位小数
* 约束：主键（primary key）-物理上的存储顺序，外键（foreign key）-其他表的主键，非空（not null）， 唯一（unique，此字段的值不允许重复），默认（default）
* 外键约束会减慢修改的速度。为保证有消息，可以在**逻辑层**进行控制。

登陆: mysql -uroot -pmysql

* 显示已有数据库： show databases;  // 以；结束命令输入
* 查看语句具体进行的操作，使用show： show create database base_name charset=utf8;
* 显示时间，版本： select now(); select version();  // 使用select选择函数来显示，而非show

1.数据库操作
* 注释： -- 注释内容
* 创建数据库： create database base_name charset=utf8; // charset默认为latin
* 删除数据库： drop database base_name  // 若数据库名带-，则需输入\`base-name\`。
* 使用数据库： use base_name
* 显示当前使用中的数据库名称： select database();  // 需先用use使用数据库。

2.数据表操作
* 显示当前数据库的所有数据表： show tables;
* 创建数据表: create table [if not exist ]table_name(字段 类型 约束[, 字段 类型 约束]) [select语句];  // int unsigned
* 删除数据表： drop table table_name
* 查看表格本身（而非表中数据）的结构： desc table_name;  // desc是describe的缩写？

3.修改表格结构（alter）
* 增加字段： alter table table_name add 字段名 类型 约束；
* 修改字段： alter table table_name modifiy 字段名 类型 约束；
* 修改已有字段为新字段： alter table table_name change 原字段 新字段名 类型 约束[ ,change 原字段 新字段名 类型即约束]；
* 删除字段： alter table table_name drop 字段名 类型 约束；  // 会将数据一并删除
* **链接到外键**： alter table table_1 add foreign key (需要被外键约束的字段） references table_2 (table_2中的字段）；
* **删除外键**： alter table table_1 drop foreign key 外键名称（需要先show create table table_1 找出外键约束名）；


4.数据修改（curd：create,update,retrive,delete)
* 显示整个表格的数据： select \* from table_name [where 字段=值];  //条件也可以是字段>值
* 插入数据： insert into table_name [(要插入数据的字段1， 字段2， 字段3)] values(具体数值）[,(具体数值)];
* 修改某一字段的数据： update students set 字段=值[,字段=值] where id=5;
* 删除数据： delete from table_name where 字段=值;  // 没有where就会删除所有数据
* **将查询结果插入表格**： insert into table_name [(要插入数据的字段)] select语句；
* **关联修改某一字段的数据**： update table_name as 别名 inner join table_2 on 条件 set 字段=值；

对于一个用户一般只标记已经删除而非真正删除。
alter table table_name add user_deleted bit default 0;
update table_name set user_deleted=1 where user_id=13; // 1表示账户已无效。

5.数据查询(select)
* select [distinct] 别名.字段[,别名.字段] from table_name as 别名；  // distinct去重

where 条件1 and 条件2;
where not (条件1 and 条件2);
1. 条件查询： 
* where 字段=值  -- 表示精确查询
* where 字段 like 值%  -- 表示模糊查询，%替换1或多个，_替换1个。
* where 字段 rlike 值%  -- 表示正则查询

2. 范围查询
* where 字段 not in (值1， 值2， 值3）；
* where [not] (字段 [not] between int1 and 值2);  // not可前可后，括号内为1个条件整体
* where 字段 is null；

6.对查询到的数据排序，在最后加上order
* order by 字段 asc/desc [,字段 asc/desc];  //先判断前边的条件（ascend，descend）

7.聚合函数(求和、求数量、求平均值等）、分组
* select count(*) from table_name where 条件；  // count计算数据条数
* select round(sum(字段)/count(*), 2) from table_name where 条件；
此时显示结果为1个值

* select **gender**, sum(age)/group_concat(name, " ", age)[,avg(age)] from table_name where 条件 group by **gender** having avg（age) > 20;  -- group字段为gender，所以前边的字段也要为gender

1. 先用where确定所选内容，
2. 使用group按字段中不同的值来分组。
3. 使用having仅显示符合筛选条件的组(筛选计算后的值）。
4. 对不同的组都1.求出值，或2.使用group_concat()显示组中的每条数据的字段内容。

7.分页
* 最后加上 limit 每页显示数量；
* 或者 limit 开始项， 每页显示数量； --开始项从0开始，放在order后边。

8.链接查询（多个表，会显示2个表的内容）
* select ... from table_1 [left] inner join table_2 on 条件;  // left表示显示table_1中的所有内容，table_2不符合条件的部分显示为null
* select table_1.字段/*，table2.字段 from table_1 left inner join table_2 on 条件/table_1.字段=table_2.字段 having 字段=null;

9.自关联（省市县）
使用链接查询，将1个表命名为2个别名作为2个表使用

10.子查询(效率较低）
将查询结果作为另一个查询的条件
* select * from students where height=(select max(height) from students);

11.数据库（数据表）设计
1. 第一范式： 不能再拆分
2. 第二范式： 表必须有1个主键。没有包含在主键中的列必须完全依赖于主键，而不能只依赖于主键的一部分。
3. 另外非主键列必须直接依赖于主键，不能存在传递依赖。即不能存在：非主键列A依赖于非主键列B，B依赖于主键的状况。

E-R模型
E表示entry/实体，像定义类一样，
R表示relationship/关系，描述两个实体间的对应规则，关系有1对1，多对多，1对多。关系也是一种数据，需要存储

***
* as: 起别名
* where： 筛选每条数据符合的条件
* having： 筛选计算后的结果作为条件
* on： 筛选表与表间的符合条件的项。（也可以是1个表的2个别名）
***

### 3.mysql与python

```python
from mysql import *
conn = connect(host='localhost', port=3305, user='root', password='mysql', database='jindong', charset='utf8')
curs1 = conn.cursor()
curs1.execute('''sql code''')  # 执行后得到1张元组表，由多个元组构成
curs1.fetch()  # 获取1个元组
curs1.fetchmany(3)  # 获取3个元组
curs1.fetchall()
conn.commit()  # 提交之前做的所有修改，真正写入数据库
conn.rollback()  # 取消这条语句到上一个conn.commit()间的所有修改语句，但有auto_increment的字段不commit也会增加
cur1.close()  # 这两条写到__delete__方法中，自动调用
conn.close()
```
### 防止SQL注入，巫云
> 可构造一个列表或元组存储外界输入信息

```mysql
qe = input("输入商品名")
sql = """select * from goods where name='%s'"""
curs1.excecute(sql, [qe])  // 构造参数列表
sql_注入 = ' or 1=1 or '1
若不安全就会 执行 
select * from goods where name='' or 1=1 or '1'
此时1=1成立
```

### 4.高级
1.视图：curs1.execute('''sql code''')后返回的结果的虚拟的表,会根据表数据变化相应的变化。不可在视图中修改原表数据。
创建视图: create view v_tablename as select语句

2.事务：操作序列。序列中的语句全部执行或全不执行。银行的资金转移
原子性、一致性、隔离性、持久性《高性能sql》
```sql
start transaction; --或者 begin；
--多条sql语句
commit；
```

3.索引:提高查询效率（但影响update和insert的速度）
是一种特殊的文件（innoDB数据表上的索引是表空间的一个组成部分），它们包含对数据表里所有记录的引用指针。
开启运行时间的监测：set profiling=1;
查看执行时间：show profiles;
创建索引：create index index_name on table_name(字段（[字符串类型的数据长度]））;

原理：不断缩小想要获得的数据的范围，同时把随机事件变成顺序事件。

4.账户管理：
查看用户： desc user;
* select host, user, authentication_string from user;
创建账户并授予权限：
* grant select,insert on database_name.* to 'new_user_name'@'localhost/%/具体ip' identified by 'password';  // select,insert只授予查询和插入数据的权限，可换成all privileges，%表示可从任何ip登陆

* 查看用户权限： grant user_name

* 修改权限: grant select on database to 'user_name'@'ipaddress' with grant option;
* 刷新权限：flush privileges;
* 修改用户密码： update user set authentication_string=password('new_password') where user='user_name';
* 删除账户1：drop user 'user_name'@'ipaddress';
* 删除账户2：delete from user where user='user_name';

* 先将/etc/mysql/mysql.conf.d/mysqld.cnf的bind-addr = 127.0.0.1用#注释
* 远程登陆（应当ssh登陆电脑，而非直接远程登陆数据库）： mysql -h172.16.7.137 -unew_user_name -p

5.mysql主从（自动备份）
* 手动备份： mysqldump -uroot -p database_name > a_back_file.sql;
* 恢复数据： mysql -uroot -p new_database_name < a_back_file.sql;
导出的sql文件内容格式（包含表信息）：
1. drop table if exist
2. create table
3. insert into table

* 在主服务器上备份：mysqldump -uroot -ppass_word --all-databases --lock-all-tables > ~/path/a_back_file.sql;  --此时输出还包含了数据库名
* 在从服务器上恢复数据： mysql -uroot -ppass_word < a_back_file.sql;  --无需数据库名
* 配置主服务器：sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf 将server-id和log_bin去除注释
* 配置从服务器：sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf 将server-id改为不同值
* 重启mysql服务： sudo service mysql restart
* 主服务器创建新用户： grant replication slave on *.* to 'slave_name'@'%' identified by 'password';
* 查看主服务器信息： show master status;
* ubantu从服务器先登陆自己的root,然后连接到主服务器： change master to master_host='host_ip',master_user='username',master_password='password',master_log_file='mysql-bin.00006',master_log_pos=590;
* 查看从服务器查看信息： show slave status \G; --slave I/O running,slave sql running 表示连接成功

配置windows从服务器：
1. C/ProgramData/MySQL/MySQL Server 5.7/my.ini修改server-id
2. services.msc打开MySQL57服务
3. 其他相同
