## 关系型数据库
> RDBMS(relational database management system)
> 关系型数据库，包括mysql，oracle. [关系型数据库的起源](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf)

理论基础： 集合论(set theory), 基于关系模型建立数据库

原理： 每张表是一个集合，各个集合之间存在关系（如交集）,如此可将不同的表关联起来。

### 核心概念：[key](https://www.studytonight.com/dbms/database-key.php)(键)

> 作用：每个key都是唯一的，如此可快速找到一条唯一记录，并对(且仅对)此条记录修改。

* 主键（primary key） 性质：非空（not null）， 唯一（unique，此字段的值不允许重复），默认（default）
* 外键（foreign key）与引用表相关联（此外键是引用表的主键）。不同主键可对应同一外键，但反过来不行。
	* 外键的作用：设定了可选值的集合，表格的外键仅可从此集合中获取值（除非为空值），而不能随意设置值
* 候选键（candidate key，又可称为候选主键）: 1个或多个非主键的组合，能与主键一样定位一条唯一的记录，且使用最少的属性（无冗余）
* 超键（super key）：1个或多个非主键的组合，能与主键一样定位一条唯一的记录，超键就是这些组合的集合
* [复合键（composite key）](https://beginnersbook.com/2015/04/keys-in-dbms/)：2个或多个键组合生成一个唯一结果，能与主键一样定位一条唯一的记录。符合此条件的主键、超键、候选键都可称复合键

* 每一列又可称为一个属性(attribute)
* 主键属性：是候选键列或其一部分
* 非主键属性：非候选键的列

* 外键约束会减慢修改的速度。为保证有消息，可以在**逻辑层**进行控制。

### 描述表的关系

一对一：2个表主键相同（主键和外键是同一个），其他列都不同，通常用于隔离机密信息，分隔后可加快查询，或避免空值插入

一对多：普通表将引用表作为外键，引用表为一，普通表为多

多对多：是前2者的集合。先创建一个中间表。中间表创建2个外键，引用2张表。

### 规范化

起因：一个表格中过多列，且这些列之间的关系混乱，(例如将作者，书籍，出版社，销售量等所有记录都放在一个表中），导致插入更新删除行都操作困难。

常用解决方法：根据列的关系，将一个表拆分为多个表

NOTE：规范化不是消除冗余，而是减少冗余。
每个范式（normal form）都先要满足前一个范式

- 第一范式
    - 列仅包含原子值（不能再细分）
	    - exp: 作者列的一个单元格不能放多个作者
    - 同一列的数据，它们的类型需相同（如此才能进行快速的批量操作）
    - 列名不重复
    - 没有重复的组（2个或多个逻辑相关联的列的集合）
	    - 例如一本书有多个作者，不应创建多个作者列，因为作者是逻辑相关联的，只应创建一个作者列
    - solve：在现有表中将1本书的多作者分成多行，并复制多次书信息。但是会违反第二范式
    - solve2: 将author放入新的表，与books表创建多对多的关系,[见范例,符合第二范式](#after-2nd-normal-form)
- 第二范式
    - 不是部分依赖的，而是完全依赖。`A->B`表示B依赖于A,`{A,B}->C`表示C依赖于AB复合键
        - 依赖性/函数依赖（dependency/function dependency）：表格的所有其他列只通过主键获得,主键外的列并不能推得其他列的值
        - 完全依赖：非主键列依赖了主键（候选键）的全部以筛选出唯一行，而非部分
        - 部分依赖：非主键列只依赖了主键（候选键）的一部分就能筛选出唯一值，而不需要全部主键
        	- exp： {A,B}组成候选键,C只依赖于B，而不依赖于A，C是部分依赖。
        - solve: 部分依赖的列C移出，用这些列及它们依赖的候选键部分B创建1张表。
    - 作用：更加清晰
- 第三范式
    - 不能传递依赖（transitive dependency）
        - 依赖传递：A->B,但A,B都不是主键属性，但prime_key->A，因此称为传递依赖
        - solve1: A是超键
        - solve2: B是主键属性,但会违反Boyce-Codd范式
        - solve: 将此非主键列及依赖的非主键移出并创建新表，创建ID作为主键
    - 作用：减少数据复制
- 以下是更高级的范式：关系模型不需要，但会用来避免冗余
- Boyce-Codd范式
	- > 又称3.5范式，是第三范式的拓展
    - 候选键列的一部分不能依赖于非主键列
    - solve: B是主键属性，A->B，则A必须是超键
- 第四范式
    - 不能多值依赖（Multi-valued Dependency）
        - 多值依赖出现的条件：
        - A->B,单一A值对应多个B值,可能就会有多值依赖
        - 至少有3列
- 第五范式
    - 没有连接依赖（join Dependency）
        - 连接依赖：将表格拆分，然后重组，依然能得到原表格，而信息不丢失
        - 没有连接依赖的表格，拆分重组后，会信息丢失或创建新条目
    - 没有连接依赖的表格说明已经到达最小的程度，已不可再分。
    - 但不是所有的表格都要达到没有连接依赖的程度。

### exp: 一个有范式问题的表格

book_id(primary key) | publisher | title | author | pub_date |
--- | --- | --- | --- | --- |
OSN21329 | Oraley | insight | Mark,Twin | 1947-4-7
OSN21132 | Oraley | outsight | Mark,Town | 1952-4-15
OSN21343 | BkTown | brief tour | Bill,Twin | 1947-4-24
OSN21124 | Oraley | Great town | Mark,Alan,Willy | 1953-5-27

#### after 1st normal form.

{book_id,author}组成候选键才能定位一条记录。
但其他列(如pub_date)与author无关，
不需要author，只需要book_id即可筛选出唯一的pub_date, 
因此pub_date只是部分依赖于主键（候选键），违反了第二范式

book_id | publisher | title | author | pub_date |
--- | --- | --- | --- | --- |
OSN21329 | Oraley | insight | Mark | 1947-4-7
OSN21329 | Oraley | insight | Twin | 1947-4-7
OSN21132 | Oraley | outsight | Mark | 1952-4-15
OSN21132 | Oraley | outsight | Town | 1952-4-15
OSN21343 | BkTown | brief tour | Bill | 1947-4-24
OSN21343 | BkTown | brief tour | Twin | 1947-4-24
OSN21124 | Oraley | Great town | Mark | 1953-5-27
OSN21124 | Oraley | Great town | Alan | 1953-5-27
OSN21124 | Oraley | Great town | Willy | 1953-5-27

#### after 2nd normal form

增加一列出版社排行

> pub_rank不是主键，且只依赖publisher（非主键，依赖于主键），与主键/候选键无关，违反了第三范式

book_id(primary key) | publisher | title | pub_date | pub_rank | 
--- | --- | --- | --- | --- |
OSN21329 | Oraley | insight | 1947-4-7 | 1
OSN21132 | Oraley | outsight | 1952-4-15 | 1
OSN21343 | BkTown | brief tour | 1947-4-24 | 4
OSN21124 | Oraley | Great town | 1953-5-27 | 1
OSN21117 | Meeter | bulid palace | 1923-4-21 | 2


title | author_id |
--- | --- |
OSN21329 | 1
OSN21329 | 2
OSN21132 | 1
OSN21132 | 3
OSN21343 | 2
OSN21343 | 4
OSN21124 | 1
OSN21124 | 5
OSN21124 | 6

> 可为作者设置id，以避免重名问题，若无其他作者信息，则可以不要这张表

author_id(primary key) | author | Age | contry |
--- | --- | --- | --- |
1 | Mark | 26 | Ame
2 | Twin | 32 | Bri
3 | Town | 31 | France
4 | Bill | 24 | Ame
5 | Alan | 37 | Japan
6 | Willy | 42 | Germany

#### after 3rd normal form

> 将pub_rank列移出，并创建publisher表

publisher | pub_rank |
--- | --- |
Oraley | 1
Meeter | 2
BkTown | 4

#### before 4th normal form

> name->address，hobby和course则多值依赖于name，且hobby与course互相独立

name | address | hobby | course |
--- | --- | --- | --- |
Mar | Wall Street | piano | French
Mar | Wall Street | piano | Chemistry
Mar | Wall Street | baseball | French
Mar | Wall Street | baseball | Chemistry
Mar | Wall Street | reading | French
Mar | Wall Street | reading | Chemistry

solve: 以name为主键分为3张表

#### a table qualified for 5th normal form

> 由于两两相关，必须要拆分成3张表才可,
但3张表再次组合却不会得到原来的表，而会多出许多（不在原表内的）信息。
因此此表符合第五范式

supplier | product | customer |
--- | --- | --- |
KFC | chicken | Malin
McNaldo | chicken | Pielo
KFC | french fries | Pielo
McNaldo | french fries | Nindo
KFC | coffee | Pielo
McNaldo | coffee | Shroud
Walles | coffee | Nindo

### exp: 范式问题的代数化展示

preset: {A,B}组成候选键,C,D不是主键属性。`A->B`表示B依赖于A,`{A,B}->C`表示C依赖于AB复合键

- 不符第2范式
    - {A,B}->D; B->C
    - solve: move B,C in new_table，B refered
- 不符第3范式
    - {A,B}->C; C->D
    - solve1: move C,D in new_table, C refered
    - solve2: {A,D}成为候选键，{A,D}->B; C->D
- 不符第3.5范式
    - {A,B}->D; C->B
    - solve: move C,B in new_table, C refered

### 非规范化

规范化会导致表数量不断增加，减慢查询时间。因此有时要特意非规范化

非规范化的特性：

- 会牺牲数据的完整性
- 难以理解
- 加快查询，降低更新速度
- 增加了插入不一致数据的风险
- 适用：应当只用于插入（如日志），而不能用来更新已有数据

## mySql简介

### 1. basics

* 数据类型：INT，CHAR（max_char_number),一般用VARCHAR（动态大小），TEXT（0-65535字节），decimal（5， 2）共存5位数，2位小数
* 不区分大小写
* 使用`;`为一个命令结尾

mysql图形界面：navicat（解压后删除.navicat64，取消安装wine）
登陆: mysql -u root -p mysql

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

exp： 创建表格，插入数据实例

    drop table authors;
    create table authors
    (
        au_id char(3) not null,
        au_fname varchar(15) not null,
        au_lname varchar(15) not null,
        phone varchar(12),
        address varchar(20),
        city varchar(15),
        state char(2),
        zip char(5),
        constraint pk_authors primary key (au_id)
        );
    insert into authors value('A01','Franz','Kafka','','','Österreich-Ungarn','','');

3.修改表格结构（alter）
* 增加字段： alter table table_name add 字段名 类型及约束；
* 修改字段： alter table table_name modifiy 字段名 类型及约束；
* 修改已有字段为新字段： alter table table_name change 原字段 新字段名 类型及约束[ ,change 原字段 新字段名 类型及约束]；
* 删除字段： alter table table_name drop 字段名 类型及约束；  // 会将数据一并删除
* **链接到外键**： alter table table_1 add foreign key (需要被外键约束的字段） references table_2 (table_2中的字段）；
* **删除外键**： alter table table_1 drop foreign key 外键名称（需要先show create table table_1 找出外键约束名）；


4.数据修改（curd：create,update,retrive,delete)
* 显示整个表格的数据： select \* from table_name [where 字段=值];  //条件也可以是字段>值
* 插入数据： insert into table_name[(col1,vol2,vol3...)] VALUES (val1,val2,val3...);
* 修改某一字段的数据： update students set 字段=值[,字段=值] where id=5;
* 删除数据： delete from table_name where 字段=值;  // 没有where就会删除所有数据
* **将查询结果插入表格**： insert into table_name(col1,vol2,vol3...) select语句；
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

1. 先用where筛选行，
2. 使用group按字段中不同的值来分组。
3. 使用having筛选符合条件的组。
4. 对不同的组都1.求出值，或2.使用group_concat()显示组中的每条数据的字段内容。
5. 使用on进行联结筛选

7.分页
* 最后加上 limit 每页显示数量；
* 或者 limit 开始项， 每页显示数量； --开始项从0开始，放在order后边。

8.链接查询（多个表，会显示2个表的内容）
* select ... from table_1 [left] inner join table_2 on 条件;  // left表示显示table_1中的所有内容，table_2不符合条件的部分显示为null
* select table_1.字段/\*，table2.字段 from table_1 left inner join table_2 on 条件/table_1.字段=table_2.字段 having 字段=null;

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

### 2.mysql与python

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
 防止SQL注入，巫云
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

### 3.高级
1.视图：curs1.execute('''sql code''')后返回的结果的虚拟的表,会根据表数据变化相应的变化。不可再视图中修改原表数据。
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

4.账户管理(user也是一个数据库)：
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

## 数据库详解

NOTE: sql不区分大小写，但可将sql关键字都大写，如此更加清晰。

### exp: 简单的查询

    SELECT [all|distinct] city as "c",
        code as "cd",
        au_name as "an",
        state,
		price * sales As "total"
    FROM table_country[,table2[,table3]
    ORDER BY 4 [asc | desc],
             2 [asc | desc],
             an [asc | desc];

- 默认为all，distinct表示去除重复项
TODO：测试是否每一列都可用distinct
- as起别名后可供order使用。
- order by 的数字代替select中的列名(更加简洁)。也可以输入全名。
- price*sales会相乘并将结果保存为虚拟的新列total（派生列）

NOTE：可用select的列(此处为c,cd,an,state)之外的列进行排序，但不建议使用（因为如此排序后没有意义）

NOTE：null的排序取决于dbms，mysql与oracle的null排序不同



### 条件筛选

> (**mechanism**):where,having,on等筛选条件的作用，是最早发生的，它们会遍历表格的每一行，并将符合条件的行置入一个临时表中，供select，order等使用

where形式：`WHERE col op value;`。逻辑的and,or，not连接不同的筛选条件

条件 | 等价于 |
--- | --- |
not (not p) | p
not (p and q) | (not p) or (not q)
not (p or q) | (not p) and (not q)

    select title,price,sales,pub_date,product_date
        price * sales As "total"
    from table_country
    WHERE ((price * sales > 1000)
        AND (pub_date >= DATE '2003-02-07'))
        OR (title = "live")
        OR NOT (title = "fail")
        OR title LIKE '_ke%'
        OR product_date BETWEEN DATE '2001-03-08'  // NOTE: 必须是date对象才能进行比较，因为2个字符串不能>,<比较
                        AND DATE '2002-03-08';

NOTE：用<>表示不等，而不是！=, 用=表示相等，而不是==。最好将语句放在()中

- 普通操作符：<,>,>=,<>,=等
- 特殊操作符：like,between,in,is null
	- LIKE进行相似匹配，其value为一个正则字符串,`_`匹配单个字符，`%`匹配任意数量的字符
		- where col LIKE '%str%'
	- BETWEEN 判断范围
		- 等同于where col>= val1 and col<=val2
	- IN判断值在其中
		- where col IN (val1,val2,val2)
	- IS NULL判断值为空：
		- where col IS NULL

NOTE: **null**值不进行任何匹配，>,<,=,<>等都不匹配null值,只有is null能确定是否为null

### 计算操作（函数操作）

    select f_name || ' ' || l_name AS full_name,
        SUBSTRING(pub_id from 2 for 4)
        AS "from 2 and select 4 chars",
        trim(leading 'H' from publisher)
    FROM authors
    WHERE EXTRACT(MONTH FROM pubdate)
        between 6 and 9
        and pubdate between
            (current_timestamp - interval 90 day)
            and (current_timestamp + interval 90 day)
    order by position('st' in f_name) asc

- `||`连接字符串获得作者全名
- substring()函数选取部分
- upper(),lower()修改大小写
- trim([[leading|trailing|both] ['trim_chars'] from] string/column),
删除前/后的trim_chars,默认为空格
- charactr_length()返回字符个数
- position(string in column)返回字符串第一次出现的位置
- extract(field from datetime_column_or_interval)提取时间
- current_date,current_time,current_timestamp获取当前时间,current_time(6)为秒添加6位精度
- CURRENT_USER为当前用户
- cast(column as data_type)类型转换

case: 同C++中的case

	select
		name,
		price
		CASE quality
			WHEN "good" then price*1.5
			WHEN "bad" then price*0.8
			ELSE price
		END
			as 'new_price'

- coalesce检测每项是否为空值，都不能匹配则填充最后一个值
	- coalesce(state,user, 'N/A') as "not_null_col",
- nullif(exp1,exp2) as "eq is null",exp1,2相等则返回空值，否则返回exp1的值

### 汇总（聚合）

聚合函数：min,max,sum,avg,count。都忽略空值，除了count(*),count返回行数

特性：
- 聚合表达式不可出现在where语句中
- select作用域中，仅分组列可混合使用费聚合表达式和聚合表达式
- 聚合函数不可嵌套（因为聚合函数处理一系列值，返回一个值，再嵌套没有意义）

NOTE：where语句生效之后再进行聚合计算

先distinct column,再进行聚合计算，distinct count(price)没有意义

	select
		COUNT(distinct price)

#### 分组

> 聚合函数会对每个组进行计算

GROUP BY col: col列中相同值的行被分为一组。一组为一行。这些行组成新表。

创建表格elems:

title | price | time |
--- | --- | --- |
one | 10 | June
one | 10 | July
two | 22 | June
two | 28 | October
three | 34 | December
three | 45 | January
two | 22 | May
one | 10 | Septemper

exp: GROUP BY col

	select
		title,price,time,max(price) as "max_price"
	from elems
	GROUP BY
		title

	先执行group by：类似以下python代码

	groups = {}
	for i in range(len(title)):
		# 每遇到一个新title，就保存它的行数
		k = title[i]
		if k in groups.keys():
			groups[k].append(i)
		else:
			groups[k] = [i]

	再执行select title,price,time, max(price)：类似以下python代码

	select_list = []
	for v in groups.values():
		# 聚合函数则会进行特殊处理
		maxVal = 0
		for index in v:
			cur = price[index]
			if cur > maxVal:
				maxVal = cur
		i = v[0]
		# 每个group为1行，且为groups[k][0]行
		select_list.append( (title[i],price[i],time[i], maxVal) )

结果为：

title | price | time | max_price
--- | --- | --- | --- |
one | 10 | June | 10
two | 22 | June | 28
three | 34 | December | 45

exp: GROUP BY a,b

	select
		title,price,time,max(price) as "max_price"
	from elems
	GROUP BY
		title，price

	先执行group by：类似以下python代码

	groups = {}
	for i in range(len(title)):
		# 每遇到一个新title，就保存它的行数.
		# 每列的数据类型都不会变化，除了空值,将数字转换为字符串
		k = str(title[i])+str(price[i])
		# k完全相同，才会当做一组
		if k in groups.keys():
			groups[k].append(i)
		else:
			groups[k] = [i]

	再执行select title,price,time, max(price)：同上
		
结果为：

title | price | time | max_price
--- | --- | --- | --- |
one | 10 | June | 10
two | 22 | June | 28
two | 28 | October | 28
three | 34 | December | 45
three | 45 | January | 45

exp: 与case组合

    select
		au_id,pub_id, count(sales) as "numbooks"
    from title_authors
    GROUP BY au_id,pub_id

    select 
        case
            when sales is null
                then 'unknown'
            when sales <= 1000
                then 'no more than 1000'
            when sales <= 10000
                then '1000-10000'
            else 'over 10000'
        END
            as 'sales category'
        count(*) as 'num titles'
    from titles
    GROUP BY
        'sales category'
    order by min(sales) asc; 

having: group后会有多个group,having对每个group进行操作，以筛选所需的group，因此一般用聚合函数

	select
		type,count(price) as "pri",
		avg(price*sales) as 'avg recenue'
	from titles
	group by type
	having avg(price * sales) > 10000
		and avg(price) > 200;

## 联结

> 限定列名为 table_name.column,无歧义且提高性能

作用: 从多个表中检索行并以一张表展现.

运行机制：A为主表，B为join的表，对A的每行，遍历B所有行尝试匹配。O(n**2)。

	for rowA in listA:
		result = []
		for rowB in listB:
			if satify_on(rowA,rowB):
				// 返回第一个满足的rowB, 
				result.append(somejoin(rowA,rowB))
				break
	print(result)

NOTE： `from table_name [AS] alias`可设置table别名为alias,加上AS更为清晰?

exp: 联结后会先将所有列组合到一起，

	// 筛选出authors中所有行中满足inner join条件的
	select
		au_id,a.city
	from authors a
	inner join publishers p
		on a.city = p.city;
			
	select
		a.au_id,a.city,p.state,t.title
	from authors a
	inner join publishers p
		on a.city = p.city
	inner join titles t
		on t.title_id = a.title_id
	where p.state in ('AR', 'RE');

联结类型 | description |
--- | --- |
cross join | 显示表1的每行和表2的所有行组合得到的所有行
inner join | 最常用，用比较操作符比较2个表共同列的值，显示与操作符匹配的行
natural join | 是inner join的一种，使用=比较操作符（不可修改）,同名的（主键）列只保留1列
self-join | 自联结，使用inner join
left outer join | 返回左表所有select列的行,右表符合on条件的显示值，否则显示null
right outer join | (outer join至少返回一个行的所有行),与left outer join相反
full outer join | 是左右联结的并集

#### exp: 创建2个基本表格

class table

ID | NAME |
--- | --- |
1 | abhi
2 | adam
3 | anu

class_info table

ID | Address |
--- | --- |
1 | DELHI
2 | MUMBAI
3 | CHENNAI

	SELECT * FROM class 
		CROSS JOIN class_info;

CROSS JOIN 默认会产生m\*n行数据,显示2个表的所有组合，因此通常不用

ID | NAME | ID | Address |
--- | --- | --- | --- |
1 | abhi | 1 | DELHI
2 | adam | 1 | DELHI
4 | alex | 1 | DELHI
1 | abhi | 2 | MUMBAI
2 | adam | 2 | MUMBAI
4 | alex | 2 | MUMBAI
1 | abhi | 3 | CHENNAI
2 | adam | 3 | CHENNAI
4 | alex | 3 | CHENNAI


修改 class table为

ID | NAME |
--- | --- |
1 | abhi
2 | adam
3 | alex
4 | anu

	SELECT * from class
		INNER JOIN class_info
			on class.id = class_info.id;

ID | NAME | ID | Address |
--- | --- | --- | --- |
1 | abhi | 1 | DELHI
2 | adam | 2 | MUMBAI
3 | alex | 3 | CHENNAI

	SELECT * from class NATURAL JOIN class_info;

ID | NAME | Address |
--- | --- | --- |
1 | abhi | DELHI
2 | adam | MUMBAI
3 | alex | CHENNAI

修改 class为

ID | NAME |
--- | --- |
1 | abhi
2 | adam
3 | alex
4 | anu
5 | ashish

修改 class_info为

ID | Address |
--- | --- |
1 | DELHI
2 | MUMBAI
3 | CHENNAI
7 | NOIDA
8 | PANIPAT

	SELECT * FROM class 
		LEFT OUTER JOIN class_info 
			ON (class.id = class_info.id);


ID | NAME | ID | Address |
--- | --- | --- | --- |
1 | abhi | 1 | DELHI
2 | adam | 2 | MUMBAI
3 | alex | 3 | CHENNAI
4 | anu | null | null
5 | ashish | null | null

	SELECT * FROM class 
		FULL OUTER JOIN class_info 
			ON (class.id = class_info.id);

ID | NAME | ID | Address
--- | --- | --- | --- |
1 | abhi | 1 | DELHI
2 | adam | 2 | MUMBAI
3 | alex | 3 | CHENNAI
4 | anu | null | null
5 | ashish | null | null
null | null | 7 | NOIDA
null | null | 8 | PANIPAT

exp: 自联结

	select
		e1.emp_name as "employee",
		e2.emp_name as "Boss"
	from employees e1
	inner join employees e2
		on e1.boss_id = e2.emp_id;
	
### 子查询/内查询

创建一个临时表/列 保存子查询的结果，供外查询（指子查询外的语句）使用

- 语法：同普通查询，但以括号包裹，是单个的select语句
- 特性：
	- 内联结都可以写作子查询，但不能反过来，因为内联结是可交换的
	- 通常子查询效率高于内联结，但是难以差错
	- 子查询的值也可作为字面常量
- 常用情况：column可以是列,表达式等
	- where column op (subquery)
		- op为>,<,=,<>等
	- where column [not] in (subquery)
	- where column op all (subquery)
		- col > all(subquery) 表示 col > 子查询中的所有值
	- where column op any (subquery)
		- col > any(subquery) 表示 col > 子查询中的至少一个值
	- where [not] exists (subquery)
		- subquery为true，通常用于相关子查询

简单子查询： 
- 与外查询无关
- 先完成子查询，返回临时表（且只返回一次）
- 外查询使用此临时表进行筛选

	select
		au_id,city
	from authors
	where city in
		(select
			city
		from publishers);
				
相关子查询： 
- 依赖外部查询
- 为外部查询选择的每一候选执行一次,因此会执行相当多次
- 总是引用外部查询from子句指定的表
- 使用限定列名引用外部查询确定下来的值

形式：

	select
		outer_columns
	from outer_table
	where outer_column_value in
		(select
			inner_column
		from inner_table
		where inner_column = outer_colum)
				
exp: cand.type为外部变量

title_id | type | sales | Address
--- | --- | --- | --- |
1 | history | 256 | DELHI
2 | history | 2516 | MUMBAI
3 | psychology | 732 | CHENNAI
4 | biography | 4528 | null
5 | children | 2156 | null
6 | history | 71113 | NOIDA
7 | children | 815 | PANIPAT
8 | history | 22116 | DELHI
9 | computer | 4724 | MUMBAI
10 | psychology | 244 | CHENNAI
11 | biography | 5528 | null
12 | children | 21556 | null
13 | history | 6113 | NOIDA
14 | children | 1815 | PANIPAT

	select
		cand.title_id,
		cand.type,
		cand.sales
	from titles AS cand
	where sales>=
		(select
			avg(sales)
		from titles as aver
		where aver.type = cand.type);
		
运行过程：
1. 先取第一行的cand.type并传入子查询，根据子查询结果判断此行是否符合外查询
2. 取第二行进行相同操作
3. 直至最后一行
4. 因此操作量相当大，应尽量避免使用

NOTE：空值会使子查询变得复杂，子查询可能隐藏对空值的比较（空值是互不相等的）。应对子查询添加where col is not null


### 各种方法可以实现等价查询
TODO:测试是否如此

	select
		distinct a.au_id
	from authors a
	inner join title_authors ta
		on a.au_id = ta.au_id;

	select
		distinct a.au_id
	from authors a, title_authors ta
	where a.au_id = ta.au_id;

	select
		au_id
	from authors a
	where au_id in
		(select au_id
			from title_authors);

	select
		au_id
	from authors a
	where au_id = any
		(select au_id
			from title_authors);

	select
		au_id
	from authors a
	where exists
		(select *
			from title_authors ta
			where a.au_id = ta.au_id);

	select
		au_id
	from authors a
	where 0 <
		(select count(\*)
			from title_authors ta
			where a.au_id = ta.au_id);
			
## 集合操作

联结 vs 集合
联结会增加列（和行），集合仅增加行

> union，instersect,except，默认都返回集合

特性：
- 每次对2个select语句进行操作
- 它们select的列数量必须相同，且对应类型相同，行数可不同
- 在最后order by，一般的dbms会选择第一个select表的列名，但有些不是如此，因此最好用1,2代替实际列名

运行过程：

1. select后获得表A，表B[，若使用了all,则将所有B行插入表A后就结束]
2. 获得各自的集合，集合A，集合B
3. 尝试将集合B的每一行插入集合A
4. 与A的每一行比较
5. 若有完全相同的行则忽略，否则就将此B行插入集合A

可理解为：
	
	# select_statement1 union select_statement2 转化为
	
	column_titles = get_column_titls(select_statement1)
	# listA,B格式如 [(OBS1230,Auraf),(OBS1130, Beef)...]
	listA = list(select_statement1)
	listB = list(select_statement2)
	def union(listA, listB):
		setA = set(listA)
		setB = set(listB)
		for b in setB:
			for a in setA:
				# 完全相同(每一列都相等)则忽略
				if b != a:
					setA.append(b)
					break
		return setA
	 full_table = column_titles + union(listA, listB)


常见用法：
- union通常只用来处理同一张表
- 或将现有表与一张同结构的其他表整合
- 用来将不同表的聚合计算进行整合。

exp: union的使用，uinon会删除所有重复项，使用all保留所有行

	select au_id as ids, au_name as "mix author and publisher" FROM authors
	UNION [ALL]
	select pub_id, pub_name FROM publishers
	ORDER BY 1 asc, 2 asc;

au_id | au_name
--- | --- |
OBS1230 | Auraf
OBS1130 | Beef
OBS1536 | Philo
OBS1725 | Cryan

pub_id | pub_name
--- | --- |
PB210 | ORELEY
PB130 | PHISHIP
PB153 | NIOTECH
PB172 | HILLGER

ids | mix author and publisher
--- | --- |
OBS1230 | Auraf
OBS1130 | Beef
OBS1725 | Cryan
OBS1536 | Philo
PB172 | HILLGER
PB153 | NIOTECH
PB210 | ORELEY
PB130 | PHISHIP

exp：一个较复杂的示例(此处在select中用case可达到相同效果）

	select title_id, type, price,
		price\*1.1 as "new price"
	from titles
	where type='history'
	UNION
	select title_id, type, price,
		price\*1.2
	from titles
	where type='psychology'
	UNION
	select title_id, type, price,
		price\*0.9
	from titles
	where type not in ('hisory',psychology)

## 修改数据

#### 插入(值插入和查询插入)

exp: 值插入: 每次只能插入一行。

	INSERT INTO authors(
		au_id,
		au_fname,
		au_lname,
		city)
	VALUES(
		'A09',
		'Irene',
		'Bell',
		'Mill Valley');

exp: 查询插入: 将所有搜索结果都插入

	// 将new_authors_to_add表中符合条件的数据插入到authors表中
	INSERT INTO authors(
		au_id,
		au_fname,
		au_lname,
		city)
	select
		au_id,
		au_fname,
		au_lname,
		city
	from new_authors_to_add
	where country <> 'USA';
	
#### 更新(修改原有值)

形式:

	UPDATE table_name
	SET col = new_value,
		col2 = new_value2
	cond_statement

建议：先使用相同where子句的select并查看是否如预期。

exp: 

	UPDATE candies
	SET 
		price = price *
			case type
				when 'sweet' then 1.5
				when 'sour' then 1.2
				else 1
			end
	where price < 150;

set 和where后的pub_id都是titles.pub_id

	UPDATE titles
	SET pub_id = 
		(select 
			pub_id
		from publishers
		where pub_name = 'Abatis Publishers')
	where pub_id = 
		(select
			pub_id
		from publishers
		where pub_name = 'Tenterhooks press');

#### 删除

建议：
- 先使用相同where子句的select并查看是否如预期。
- 创建目标表的临时副本来测试delete语句

形式：将满足特定条件的行从table中删除

	DELETE FROM
		table
	condition_statement

exp: pub_id列不符合条件的行会删除

	DELETE FROM 
		titles
	WHERE pub_id not in
		(select pub_id from publishers);
		
**完全删除**（不可回滚）

	TRUNCATE TABLE table_name

## 修改表结构

### 创建表

	CREATE TABLE new_table
		(col1 data_type1 [col_constraints1],
		col2 data_type2 [col_constraints2]
		[, table_constraints1]
		[, table_constraints2]
		);

约束：
- default
- not null
- unique
- check(只能插入true的值）
- primary key
- foreign key

定义约束：

	// constraint_name是自定义约束名，确保唯一
	CONSTRAINT constraint_name
		constraint_type statement

	CONSTRAINT auth_key
		PRIMARY KEY(col)

	// 确定外键列，并将其与引用的表格、列绑定
	CONSTRAINT fore_key
		FOREIGN KEY(col)
		REFERENCES ref_table(ref_col)

	// 输入数据时检查(最好对每列都检查，且可对一个值进行多种检查）
	// 需确保各检查不会冲突
	CONSTRAINT auth_key
		CHECK (condition)

NOTE:
- mysql中默认值必须是字面量
- oracle中默认值必须在所有列约束的最前

exp: 应当仅使用列约束或仅用表约束，建议使用表约束

	// 直接对列添加约束
	CREATE TABLE pubs(
		pub_id char(3) PRIMARY KEY,
		pub_name varchar(20) DEFAULT 'unknown pub' NOT NULL,
		price decimal(5,2) DEFAULT 0.00 NOT NULL,
		state char(2) NOT NULL
		);

	// 添加表约束
	CREATE TABLE pubs(
		pub_id char(3) NOT NULL UNIQUE,
		pub_name varchar(20) DEFAULT 'unknown pub' NOT NULL,
		price decimal(5,2) DEFAULT 0.00 NOT NULL,
		state char(2) NOT NULL,
		PRIMARY KEY(pub_id)
		);

	// 添加命名的表约束
	CREATE TABLE pubs(
		pub_id char(3) NOT NULL UNIQUE,
		pub_name varchar(20) DEFAULT 'unknown pub' NOT NULL,
		price decimal(5,2) DEFAULT 0.00 NOT NULL,
		state char(2) NOT NULL,
		CONSTRAINT pub_pk
			PRIMARY KEY(pub_id)
		);

	// 添加组合主键,必须使用表约束而非列约束
	CREATE TABLE pubs(
		pub_id char(3) NOT NULL,
		au_id char(3) NOT NULL,
		pub_name varchar(20) DEFAULT 'unknown pub' NOT NULL,
		price decimal(5,2) DEFAULT 0.00 NOT NULL,
		state char(2) NOT NULL,
		CONSTRAINT pub_au_pk
			PRIMARY KEY(pub_id, au_id)
		);

	// 添加外键列约束，reference说明当前列为外键，不再加FOREIGN KEY关键字
	CREATE TABLE pubs(
		pub_id char(3) NOT NULL PRIMARY KEY,
		pub_name varchar(20) DEFAULT 'unknown pub' NOT NULL,
		price decimal(5,2) DEFAULT 0.00 NOT NULL,
		state char(2) NOT NULL,
		pub_id char(3) NOT NULL
			REFERENCES publishers(pub_id)
		);

	// 同时使用主键和外键的表约束
	CREATE TABLE pubs(
		title_id NOT NULL,
		pub_name varchar(20) DEFAULT 'unknown pub' NOT NULL,
		price decimal(5,2) DEFAULT 0.00 NOT NULL,
		state char(2) NOT NULL,
		pub_id char(3) NOT NULL,
		CONSTRAINT title_pk
			PRIMARY KEY(title_id),
		CONSTRAINT pub_fk
			FOREIGN KEY(pub_id)
			REFERENCES publishers(pub_id)
		);

	// 定义组合外键(外键在同一张引用表中）
	CREATE TABLE pubs(
		title_id char(3) NOT NULL,
		au_id char(3) NOT NULL,
		au_order char(3) NOT NULL,
		price decimal(5,2) DEFAULT 0.00 NOT NULL,
		CONSTRAINT title_pk
			PRIMARY KEY(title_id,au_id),
		CONSTRAINT title_au_fk
			FOREIGN KEY(title_id,au_id)
			REFERENCES title_authors(title_id,au_id)
		);

	// check
	CREATE TABLE pubs(
		title_id char(3) NOT NULL,
		title_name varchar(40) NOT NULL,
		type varchar(10)
		pub_id char(3） NOT NULL,
		pages INTEGER,
		price DECIMAL(5,2),
		sales INTEGER,
		pubdate DATE,
		contract SAMLLINT NOT NULL,

		CONSTRAINT title_pk
			PRIMARY KEY(title_id,au_id),
		CONSTRAINT pub_fk
			FOREIGN KEY(pub_id)
			REFERENCES publishers(pub_id),

		CONSTRAINT type_chk
			CHECK (type in ('biography','children',
				'computer','history')),
		CONSTRAINT page_chk
			CHECK (page > 0),
		CONSTRAINT title_id_chk
			CHECK(
				(substring(title_id from 1 for 1) = 'T')
				and
				(cast(substring(title_id from 2 for 2) as integer)
					between 0 and 99)
				)
		);

#### 创建临时列表

> 相对于普通表增加了{LOCAL | GLOBAL} TEMPORARY

	CREATE {LOCAL | GLOBAL} TEMPORARY TABLE table_name
			(col1 data_type1 [col_constraints1],
			col2 data_type2 [col_constraints2]
			[, table_constraints1]
			[, table_constraints2]
			);

local:用户自己可用，dbms进程结束后消失
global:多用户可用，dbms会话和其他引用它的任务结束后消失

#### 用旧表创建新表

	// 用旧表创建新表
	CREATE TABLE new_table
		AS subquery
	// 用旧表创建临时新表
	CREATE {LOCAL | GLOBAL} TEMPORARY TABLE new_table
		AS subquery

exp:

	CREATE TABLE autho
		AS
		select
			a.au_fnam,
			a.au_lname,
			t.title_name
		from
			authors a,
			title_authors ta,
			titles t
		where a.au_id = ta.au_id
			and ta.title_id = t.title_id
			and a.state not in ('CA', 'NY');
	
### 修改表

	ALTER TABLE table alter_action;

alter_action:
- ADD COLUMN col type [constraints]
- ALTER COLUMN col SET DEFAULT expr
- DROP COLUMN col [RESTRICT|CASCADE]
- ADD table_constraint
- DROP CONSTRAINT constraint_name

TODO:sql的alter

sql修改表名:`RENAME TABLE old_name TO new_name`

### 删除表

意味着删除表的结构、数据、索引、约束、授权等

	DROP TABLE table_name;

## 索引

	CREATE [UNIQUE] INDEX index_name
		ON table(index_col);

	DROP INDEX index_name
	ON table;

起因：根据关系模型，表里的行是无顺序的。修改行快速，但是查询和排序效率低下。

索引：是**经过排序**的列表( 因此可通过不同的算法快速查询 )
1. 这个列表中索引列（或列集）的每个不同值和包含该值的行的硬盘地址（物理地址）存储在一起。
2. 无需检索整个表定位行，仅需扫描索引中的地址就可访问相应的行。

- 常进行以下操作的列需要创建索引
	- 查询（where）
	- 排序（order by)
	- 分组（group by）
	- 联结(join)
	- 计算统计顺序(min(),max()
- 以下情况的列不应当建立索引
	- 接受很少的不同值（如性别值为男或女）
	- 很少被查询
	- 只有几行的小表

索引的特性：
- 索引不改变数据
- 除了关键的索引，其他索引动态生成
- 表数据修改后必须更新索引，因此一个表不要创建超过10个索引
- 索引创建后，dbms会自动维护和使用所有
- 列的书序在组合索引中重要。组合索引值作用域定义它的那组列
- 确保唯一性（列中值唯一）可加快排序和检索速度

聚焦(clustered)索引:键值逻辑顺序决定表中相应行的物理顺序的索引。一个表只能有一个（因为数据行本身只能以一种顺序存储。）
非聚焦索引：索引结构与数据行分离

## 视图

> 相当于将常用的select语句封装为一个视图名
> 视图创建后可像普通表一样被select语句使用

	CREATE VIEW view[(view_columns)] [WITH [CASCADED | LOCAL] CHECK OPTION]
		AS select_statement;
	// view_columns数量需与select语句的数量相同，省略则从select语句继承名字
	// WITH [CASCADED | LOCAL] CHECK OPTION用来检测修改（如插入，修改）行是否符合view的select语句的要求

- 存储select语句，返回基于1或多个表检索得到的数据表
- 不是数据值的复制
- sql语句用到时，视图创建，语句结束后消失

exp:

	CREATE VIEW au_titles(LastName, Title)
		AS
		select an.au_lname, t.title_name
		from title_authors ta
		inner join au_names an
			on ta.au_id = an.au_id
		inner join titles t
			on t.title_id = ta.title_id
		where an.au_id in ('A02', 'A05');

视图 vs 临时表

- 视图仅存在于sql语句的生存期
- 临时表存在于进程的生存期

#### 可更新（修改）的视图
- 一对一内联结
- 一对一外联结
- 一对多内联结
- 一对多外联结
- 多对多联结
- UNION和EXCEPT查询

删除视图(删除表不会删除引用它的视图，因此要显式删除视图） `DROP VIEW view_name`

## 事务
> 是一个或多个连接在一起作为一个逻辑单位运行的sql语句。全部执行或全不执行。通常用于银行，如转账必须转入和转出都生效或都不生效。

>>dbms的备份/恢复设备依赖于事务。备份设备获得例行的数据块快照并将它们和随后的事务日志存储在备份盘上。使用的硬盘发生故障，借助恢复设备将最近的数据库备份并执行。或回滚所有快照到故障前最后执行并在日志中提交的事务。即是将数据库恢复到故障前的正确状态。因此要将数据库和事务日志存储在不同的硬盘

	START TRANSACTION;
		SQL_statement;
		[SQL_statement;]
	COMMIT | ROLLBACK;

## sql技巧

不同数据库内置了许多方法/关键字（将特定的语句封装为关键字），方便快速完成特定目的

sql：limit，
oracle: rank() over,rownum

获取随机行（抽取样本）：
`sample(25)`, `where rand() < 0.25` 抽25%的行进行处理

exp: 删除重复行

	delete from dups
		where id < (
			select max(d.id)
			from dups d
			where dups.title_name = d.title_name
				and dups.type = d.type
				and dups.price = d.price);
	// 1.选择一行，传入子查询
	// 2.子查询筛选出所有同值的行，返回其中的最高id。
	// 3.若外查询.id<max(id)则删除
	// 由于子查询的机制，因此每次最多只能删除当前行，后边的同值行任需要再次进行123比较循环

	// 使用group by，未测试
	delete from dups 
	where id not in
		(select max(d.id)
		from dups d
		group by d.title_name, d.type,d.price)

sql的日期: date_format(current_timestamp, %Y)

