### WSGI协议，miniweb框架介绍
> 配置服务器，用来处理动态请求。参考 [miniweb服务器]，[miniweb框架]。

1. miniweb框架用application(environ, start_response)函数处理外部动态请求，返回body值。
2. environ:一个包含所有http请求的dict对象。
3. start_response: 一个发送HTTP响应内容的函数。存储application中设置的status和header。
start_response的`status+header`+application返回的`body`构成服务器的返回信息

[miniweb服务器]: .\P6-miniweb\basic-miniweb\web-server.py
[miniweb框架]: .\P6-miniweb\basic-miniweb\dynamic\mini_web.py

### 闭包: 是一个函数，并且有传递数据的功能
方法1：实例对象：会传递所有参数
instance = NewClass(k, b)
instance(x)  # 会调用__call__
方法2：line函数内的局部变量k, b作为create_y的全局变量传入。

```python
def line(k, b):
    def create_y(x):  # 内部函数使用nonlocal k来改变k，内部直接改变k会出错
        print(k*x+b)
    return create_y  # 返回函数的引用

line1 = line(2, 3)
line1(5)  # 可创建多个
line1(6)
line1(10)
```

### 装饰器：传递函数与数据
> 每一层装饰器都传入一定的函数或数据作为内层的全局变量。每次只运行一部分函数，等待传入其他参数。
用法：在def func1(param1)上添加@propertyname1，解释器遇到@propertyname1时会执行func1=propertyname1(func1).
**赋值后左侧的func1指向propertyname1()的地址，此时右侧的func1变为一个指向原func1地址的匿名函数anonymousfunc1，不能再被直接调用。**
然后调用func1(param1)函数时即调用propertyname1(anonymousfunc1)(param1).

```python
# 这个闭包是一个通用装饰器
def sf(func):
    def call_func(*args,**kwargs):
        print("new functions added")
        return func(*args,**kwargs)
    return call_func
    
@sf  # 等价于tes1 = sf(tes1),会直接执行sf（test1）中的代码
def tes1(param):
    print("old function")
    print(param)

tes1 = sf(tes1)  # 前边有@sf，这条就可以删除，原有调用不需修改

tes1(param)=sf(tes1)(param)=call_func(param)=tes1(param)
```
多个装饰器由下往上被装载，tes1(param)时由上往下被执行

类装饰器

```python
class Ts(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, par):
        return self.func(par)
        
@Ts  # 等价于tes1 = Ts(tes1),会直接执行Ts（test1）中的代码
def tes1(param):
    print("old function")
    print(param)

tes1(param)
```


```python
# 这个闭包是一个权限限制的装饰器
def setlv(num):
    def sf(func):
        def call_func(*args,**kwargs):
            if num == 1:
                print("you have the privilege to run code in this part")
            print("new functions added")
            return func(*args,**kwargs)
        return call_func
    return sf
    
@setlv(4)  # 会执行tes1 = setlv(num)(tes1),等价于tes1 = sf(tes1)=call_func,已传入tes1且num=4。
def tes1(param):
    print("old function")
    print(param)

# 此时外界调用时不用也不能,没有权限设置参数
tes1(param)=call_func(param)=print("new function added") 及调用tes1(param)
```

### url类型
静态url：类似.html，每个网页都有真实的物理地址
动态url：带有？id=5，是逻辑地址，不存在于服务器硬盘中
SEO：搜索引擎优化
伪静态（url rewrite）：和静态url类似，其实是动态伪装成静态
缺点：服务器要支持重写规则，负担增加。可以robots禁止掉动态地址


### 面向切面
功能已完善，只需要写函数加上已有的装饰器就能添加新功能，用原本的框架自动调用

#### url编解码，排除特殊符号
import urllib.parse
urllib.parse.quote("中国")
输出'%E4%B8...'
urllib.parse.quote('%E4%B8...')
输出'中国'

#### log日志.5个等级
import logging
logging.basicConfig(level=logging.WARNING，
filename='./log.txt',filemode='w',
format='%(asctime)s - %(filename)s[line:%(lineno)d]-%(levelname)s')  # 设置默认等级。

### 元类,类比装饰器
> 通常用于将输入的类属性改变为字典或改变其大小写等。 
> 使用元类创建类,系统会先自动将所写类的class_name, class_parents,class_attr
传入type，然后系统调用type再空间中创建一个类对象。

New_class = type("Original_class_name"，由父类名称组成的元组，包含类属性的字典(名称和值))
使用help（New_class）依然指向Original_class_name

类是一组描述如何生成一个对象的代码块。
使用globals()，其中是字典，保存了所有全局变量
xx = globals()
xx['__builtin__']获得默认加载的内建模块
xx['__builtin__'].print()能调用print

> 动态创建类：不调用默认的type创建类

```python
def infunc():
    pass
New_class = type("Original_class_name",(),{"cls_prop":val1,"infunc":infuc}


def upperattr(class_name, class_parents,class_attr):
    newattr = {}
    for name,value in class_attr.items():
        if not name.startwith("__"):
            new_attr[name.upper()] = value
    return type(class_name, class_parents,class_attr)

此时类调用属性时，所写的类属性可以是大写或小写,但调用时必须大写。
class Up(object, metaclass=upperattr):
    pass
insUp = Up()
insUp.ATTR

# 上边的函数也可放到类中
class Upperattr(type):
    def __new__(cls,class_name, class_parents,class_attr):
        newattr = {}
        for name,value in class_attr.items():
            if not name.startwith("__"):
                new_attr[name.upper()] = value
        return type(class_name, class_parents,class_attr)
        # return type.__new__(cls, class_name, class_parents,class_attr)         
```

### 元类实现django中的ORM
> 创建类对应表 来代替原有的sql

def __init__(self, **kwargs):
    for name, value in kwargs.items():
        setattr(self, name, value) # 设置名称及值，而不能self.name = value
