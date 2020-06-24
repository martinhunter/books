python高级语法
***
### GIL（全局解释器锁）,导入C语言代码
> 每个线程在执行过程中先获取GIL，保证同一时刻只有一个线程可以执行代码。
> 线程释放GIL锁： 在I/O等可能引起阻塞的system call之前，可暂时释放GIL锁（执行时间到达阈值后，当前线程释放GIL。

多进程程序没有GIL，会利用多核资源，可以每核使用100%资源
多线程的python程序使用cpython解释器运行时，由于GIL的存在，是并发而非并行的，所以双核每核只能使用50%的资源，四核则为25%

解决GIL问题的方法：
1.使用其他解释器。
2.使用其他语言解析，例如c语言
gcc test.c  // 获得a.out文件，通过./a.out可直接运行
将C文件生成xxx.so文件，python加上代码
```python
from ctypes import *
from threading import thread
# 加载动态库
lib = cdll.LoadLibrary("./xxx.so")
t = Thread(target=lib.funcname)  # 加载文件中的函数
```

多进程适用：计算密集型计算
多线程（或协程）适用：I/O密集型计算

### 深拷贝（copy.deepcopy)与浅拷贝（copy.copy),
b = [[1, 2], [3, 4, 5]]  // #id(b)是变量b地址处的数据（值）
1. a = b 时，变量a和b地址处的数据相同，即&a == &b, 这个数据是layer1（目标列表对象的地址值）。
2. a = copy.copy(b) 此时a变量地址值中的数据是layer1指向的数据，（a在1个新空间中复制了b中所有元素的地址，此时&a != &b，但&a.elment1 != &b.element2）这个数据是layer2（1个或多个地址值)，a在new layer1（新地址值）复制了一份layer2。此时b通过layer1改变layer2(比如增加或删除layer2的一些值）时，a中的new layer1依然指向原有的layer2，b中增加此处并不增加，b中删除layer2中地址，由于依然有a指向这个地址所以这个地址并没有被真正删除。
3. a = copy.deepcopy(b) 更深入一层，将layerFinal（所有地址值指向的最终数据）复制了一份new layerFinal到新的地址中，因此a中的所有地址值都是新的。此时b中的layer1，layer2...layerFinal改变都不会影响到a。

当copy.copy拷贝元组时，由于元组值是不可变的，因此与 a = b 效果相同。
a = copy.copy(b) 与 a = b[:] 效果相同

### 私有化，import，封装

\_x: 私有化属性或方法，不属于API函数，禁止被导入，只能被类对象和子类访问,不在类外单独调用(被调用不会出错但不推荐）。只作为当前模块的全局变量，不被其他模块调用。
\_\_x: 并不表示私有，避免与子类的属性命名冲突，无法在外界直接访问（名字其实被自动变为_classname__x)，无法被子类重写（重写依然调用父类的方法）。

import
sys.path  # 一个列表，存储了路径，在这些路径里搜寻模块。
注意点1：
from imp import reload
reload(module_name)  # 重新载入模块，用于在程序运行过程中修改某一部分代码。
注意点2：
from module import GLOBAL_VARIABLE  # 此时全局变量只在本文件中修改生效。
import module  # 此时全局变量不仅在本文件中修改，同时也在原模块中修改生效。
但若GLOBAL_VARIABLE为一个列表，使用append/remove则也在原模块中修改生效。
***
### 重点：多继承（多父类），方法解析顺序表MRO
多继承
问题：当类b,c继承类a，类d继承类b,c时，在d的init方法中手动调用b.__init__(args),c.__init__(args)时，若不处理就会多次调用类a中的方法。

解决：使用super().__init__(all_parent_class_args)继承多个父类(传入所有父类需要的参数）。
根据C3算法，重新调整调用，通过ClassD.__mro__来查看调用父类的顺序。

\*args(参数组成的元组） \*\*kwargs(参数组成的字典），本身作为实参传递而不可单独传递args，kwargs（丢失\*)

```python
def fun2(a, *args, **kwargs):
    print(a)
    print(args)
    print(kwargs)
def fun1(a, *args, **kwargs):
    print(a)
    print(args)
    print(kwargs)
    
    fun2(a, args, kwargs)  # 此时args和kwargs作为*args，输出（（2， 3），{"name": "yihao", "age"="16"}
    fun2(a, *args, **kwargs)  # 此时输出单独的（2， 3， name="yihao", age="16"）
    # 总结： args是一个元组，而*args保持其内单个元素。

fun1（1， 2， 3， name="yihao", age="16")
```

### 类与方法
1.类的实例创建过程，例：调用 instance1 = Class1(args)的时候
1. 先调用\_\_new__创建instance1实例对象（开辟一块内存空间供其使用）
2. 调用\_\_init\_\_,(对这片空间初始化，空间地址内原来的数据不再有效，而存入新的数据）此时self指向instance1对象，并将args赋予给self.arg,即instance1.arg

\_\_class__属性指向类对象（唯一）,作用：记录类对象的地址 。

```python
# 类方法
@classmethod
def class_fun(cls):  # 此处为cls而非self，可以指向类属性和类方法
    pass
```

property属性的创建
* 方法1：装饰器--从调用方法改成像调用一个属性值，使用方便。相当于将 fun(),fun_arg_setter(),fun_arg_deleter()三个函数改为了一个属性值fun便于调用（但与函数调用方式略有不同）

```python
@property  # 获取属性值
def fun2(self):  # 只有self参数，不需要传其他参数,self.original_value在__init__中已设定
    new_value = some_function(self.original_value)
    return new_value

@fun2.setter
def fun2(self, value):
    self.original_value = value  # 修改原始值后，instance1.fun2会重新调用fun2函数

@fun2.deleter
def fun2(self):
    del self.init_value

# 上3个函数使用下三句语句调用
instance1.fun2  # 获取属性值，不需要括号

instance1.fun2 = value  # 设置__init__属性值， 传入参数。
# 由于不同于下面函数的调用方式（参数传入方式），value只能是1个值或列表等而不能是多个值
def price(value2, value_3):
    o_value, discount = value2, value_3
    print(o_value,discount)
# instance1.fun2 = value2, value3 这种方式会出错
    
del instance1.fun2  # 删除属性值
# 删除后，可再次用instance1.fun2 = value设置init属性值
```

* 方法2：类属性
先创建fun(),fun_arg_setter(),fun_arg_deleter()3个函数

```python
#在类中创建1个类属性class_prop
class_prop = property(fun,fun_arg_setter,fun_arg_deleter, "docstring")
# 调用与装饰器相同，将fun2 替换为 类属性class_prop 即可
instance1.fun2
instance1.fun2 = value
del instance1.fun2
```
### 上下文管理器
> 任何实现了__enter__()和__exit__()方法的对象都可称为上下文管理器，enter返回资源对象，exit进行清除
例如with关键字


也可使用@contextmanager装饰器进一步简化上下文管理器
```python
from contextlib import contextmanager
@contextmanager
def op(path, mode):
    f = open(path, mode)
    yield f
    f.close()
with op('out.txt', 'w') as f:  # op('out.txt', 'w')返回值为f
    f.write("someword")
```
通过yield实现，yield之前的语句在__enter__()中执行，yield之后的语句在__exit__()中执行。yield获得函数返回值就是下边调用的返回值。
