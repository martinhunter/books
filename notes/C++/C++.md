对象：是可存储值，地址值，变量等


## 栈和堆

栈中：如果当前函数foo()调用另一个函数bar()，任何从foo()传递给bar()的参数都会从foo()栈帧复制到bar()栈帧，bar()执行完消失，其中声明的所有变量都不再占用内存，此过程自动执行。

堆中：想在函数调用结束后依然保存其中声明的变量，可将变量放到堆中
想要明确地动态分配内存（置入堆中），就要先声明一个指针（需手动释放），并使用new操作符分配内存。delete只对new操作符产生堆空间起作用。

指针并发总指向堆内存，也可指向栈中的变量（&variable）。

[delete](http://www.cplusplus.com/reference/new/operator%20delete[]/)：deallocate指针所指向的内存块，释放new创建的存储空间并将指针地址设为无效。此时指针本身依然可被调用，因此需新赋值或设为nullptr以免出错。

自动判断类型

	const sreing message = "test";
	const string& foo(){ return message };
	
	const auto & f1 = foo();
	decltype(foo()) f2 = foo()
	decltype(auto) f3 = foo()
	/* f1,f2,f3作用相同,但f2中foo()调用2次
	推荐使用f3，f1也可行，不推荐f2*/

智能指针：对象超出作用域，如函数执行完毕，自动释放内存

- make_unique<object2>()
- make_share<object2>()
- make_weak<object2>()

1.创建`基于栈的对象`

	Employee stackEmployee;
	stackEmployee.setPassengerName("seman");

2.使用普通指针和new创建`基于堆的对象`,不推荐

	Employee * normalPointer = new Employee;
	normalPointer->setPassengerName("seman");
	delete normalPointer 

3.使用智能指针创建`基于堆的对象`

	auto smartPointer = make_unique<Employee>();
	smartPointer->setPassengerName("seman");
	// no need to delete normalPointer


## 常量（const）

> reference: [cv (const and volatile) type qualifiers](https://en.cppreference.com/
> w/cpp/language/cv)

运行机制：One has to initialise const variable immediately in the constructor because, of course, one cannot set the value later as that would be altering it.

作用：constants are useful for parameters which are used in the program but do not need to be changed after the program is compiled. It has an advantage for programmers over the C preprocessor ‘#define’ command in that it is understood & used by the compiler itself, not just substituted into the program text by the preprocessor before reaching the main compiler, so error messages are much more helpful [ -- const](http://duramecho.com/ComputerInformation/WhyHowCppConst.html)

修饰内容为const左侧符号

### `const int * const Method3(const int * const & referenceToAPointer) const;`  

5个const的含义如下：

1. return value points to a constant integer
1. return value is a constant pointer.
1. parameter points to a constant integer
1. parameter is a constant pointer.
1. ban Method3 in ClassObject from altering any member variables in the object.


由于不可更改的特性，声明lref为对vectorArray（一个匿名变量的值）的常量。C++就不会完整复制，而是直接调用此常量中的值

## 变量（C++中）

#### 1.1 变量
>（绑定一个匿名地址，给匿名地址一个名称）：先对`=`左边进行操作

int x=2337;

x默认bind一个不变的地址值（相当于bind了一个不变的对象），由此地址值指向可变的对象

x=2942;

修改时，x对bind的地址解引用并修改其中的值

int y = x;

y绑定一个

#### 1.2 名字(in python)

>（绑定一个匿名对象，给匿名对象一个名称）：先对`=`右边进行操作.

x=2337

x默认bind一个可变的对象，bind一个可变的地址值，地址值指向一个PyObject.

x=2942  // 将2337改为2942

修改时,一个新的PyObject对象生成，并使x绑定新地址

y=3

python内置了简单的字符，数字常量（0-256）的PyObect对象，y=3不生成新的PyObect而是绑定内置对象。

y=x

x已经是一个PyObject，不用再生成新PyObject，将y绑定此PyObject的地址值


求值：获取变量名所绑定的地址值中所存储的值

*变量的储存形式*：

	{variableName：addressOfVariable,...}
	addressVariable->valueStoredInAddressOfVariable,...

举例：

	int a = 3;
	
	对3求值，获得一个临时值3
	创建变量a,绑定的地址为addressA
	将地址addressA中的值设为3
	
	储存形式：a ~ addressA ~ 3
	
	int b = a;
	
	对a求值，返回a绑定的地址addressA中的值3
	创建变量b,绑定的地址为addressB
	将地址addressB中的值设为3
	
	储存形式：2个3不是同一个3
		a ~ addressA ~ 3
		b ~ addressB ~ 3
	
	a = 4;
	
	对4求值，获得一个临时值4
	获取变量a（键）所绑定的地址addressA（值）
	将地址addressA中的值改为4
	
	储存形式：a ~ addressA ~ 4
	
	
	eval(a) = valueInAddressA = 4
 

## 指针变量：Var1绑定的地址不变，地址储存的值为其他变量Var2的地址值

使用形式：int `*` var2 = value2;

	int variable = 4;
	
	对3求值，获得一个临时值4
	创建变量variable,绑定的地址为addressVariable
	将地址addressVariable中的值设为4
	
	int * pt = &variable，
	
	对&variable求值，获得variable绑定的地址addressVariable
	创建指针变量pt,绑定的地址为addressPt
	将addressPt处的值设为variable的地址值addressVariable
	
	储存形式：
		variable ~ addressA ~ 4
		pt ~ addressPt ~ addressVariable
	
	eval(pt) = addressVariable


## 左引用变量：绑定的地址变为其他变量Var2的地址值，储存的值为Var2的值


> 左值：是一个标识非临时性对象的表达式。
> 一个对象有名字，它就是一个左值。
> 
> 右值：是一个标识非临时性对象的表达式，或字面常量。

> references are not objects.
> [--cppReference](https://en.cppreference.com/w/cpp/language/reference)

左值引用：引用左值（函数返回值为右值，不能直接引用,除非将函数返回值类型设为左值引用），一般引用`变量名`（指代一个对象）。

左值引用尝试引用右值时：

	//exp 1
	int & lref = 30;
	
	// exp 2
	int func(int arg){return arg}; 
	int & lref = func(arg)

	都会报错error:cannot bind non-const lvalue reference of type 'int&' to an rvalue of type 'int'
	// 因为右值是临时性对象,只是一个不可变的值，
	// 临时地址及其中的值会在赋值后（左值的变量地址中保存了值的复制）被销毁。

解决方法：
	
参数，函数返回值，引用变量，3者数据类型皆设为左值引用类型。

	int & func(vector<int> arr){return arr[1];}
	int & lref = func(arr);
	if(&lref == &arr[1]){return 0}

///

	此处似乎有误????
	///
	2.使用const，不报错
	const int & lref2 = 3;
	// 与const int lref2 = 3;相比有何区别，是否进行复制？
	// const创建固定的匿名变量，将此临时值存储到匿名变量的地址中，如此lref就可引用此地址
	// 但现在引用是只读的，只有此引用指向此地址。
///


作用：

1.简化复杂的名称

2.不创建值的副本（可用于循环中map本身）

	<vector>int ar = {10,11,12,13};
	int x = ar[1];
	x += 20;
	if(ar[1] == 11){
		return 0;
	}
	int & y = ar[1];
	y += 20;
	if(ar[1] == 31){
		return 0;
	}

使用形式：int `&` var2 = value2;

	int variable = 4;
	
	int & reflpt = variable;
	
	对variable求值,似乎由于引用不直接求值，而是返回地址addressVariable???

	创建引用变量reflpt，绑定的地址为addressReflpt
	变量类型为引用，因此对variable的求值为
	将reflpt绑定的地址addressReflpt改为addressVariable
	
	储存形式：
		variable ~ addressVariable ~ 4
		reflpt ~ addressVariable ~ 4
	
	eval(reflpt) = valueInAddressVariable = 4

### 右引用变量：储存一个临时值的引用

右值引用：引用右值，一般引用`对象的值`，`字面常量`

使用形式：int `&&` var2 = value2;

int && pt = value

## C++参数传递机制

> 对一个函数，默认对实参求值(eval)，用此值替换函数内相应的形参。如此这个函数获得了实参值的拷贝，二并不会对实参的值进行修改。

### 传值调用过程
	// 定义
	arg = 3
	int func(int param){
		param += 1;
		return param
	}
	func(arg)
	

	
	// 实际运行过程
	// arg地址ad1,Copy3地址ad2，此时Copy3绑定的地址对3进行了复制
	ad2 != ad1
	Copy3 = eval(arg) = 3
	
	// substitute params in function with Copy3
	func(Copy3){
		Copy3 += 1
		return Copy3  // 返回4
	}

### 传指针调用过程
	// 定义
	vector<string> * func(vector<string> * param){
		*param += 'AnyStr';
		return 'arr already changed'
	}
	
	vector<string> arr = 'superCo';
	func(&arr)
	


	// 实际运行过程
	// arr地址值为AdOfArr,此时CopyValue绑定的地址存储了地址AdOfArr
	ad2 != ad1
	CopyValue = eval(&arr) = AdOfArr
	func(CopyValue){
		*CopyValue = 'AnyStr';
		return 'arr already changed'  // Arr的值已被修改
	}
	if(arr == 'superCoAnyString'){
		return 0
	};

### 传引用调用过程
	
	// 定义
	vector<int> arg = {3,6,8};
	void func(vector<int> & param)
	{
		for(auto & x: param){
			x += 10;
		}
	}
	func(arg)
	if(arg[1] == 13){return 0}
	
	
	// 实际运行过程
	// arg地址为AdOfArr，值为valueInArg。此时refValue绑定的地址改为AdOfArr，并不进行复制。
	ad2 == ad1
	refValue = eval(arg) = valueInArg
	// 使用refValue代换后对函数内部求值
	func(refValue)
	{
		// x对param引用，以引用相应的值
		for(auto & x: param){
			x += 10;
		}
	}

1.传值调用（call-by-value)

> 适用：小的，不改变的实参（对象）
	
	void print2(double a){
		cout<< a << endl;
	}
2.传（左值）引用调用（call-by-lvalue-reference)

> 适用：改变实参的值

	double x = 3;
	double y = 4;
	void swap(double & a,double & b);  // 声明
	swap(x,y)  // 调用

3.传常量引用调用（call-by-constant-reference)

> 适用：大的，不改变的实参（对象），且赋值代价昂贵。是为了禁止引用后修改实参而出现的。

	string randomItem(vector<string> arr);  // 传值调用，低效
	string randomItem(constant vector<string> & arr); // 传常量调用，高效

4.传（右值）引用调用（call-by-rvalue-reference)

> 核心：右值存储要被销毁的临时量，像x=rval(rval为右值)通过`移动而非复制`实现。可给予参数是左值还是右值重载函数实现。

> 适用：???

	string randomItem(constant vector<string> & arr); // 传递左值
	string randomItem(vector<string> && arr); // 传递右值

	void f(int&& x) {
	    std::cout << "rvalue reference overload f(" << x << ")\n";
	}
	f(3);  // calls f(int&&)
           // would call f(const int&) if f(int&&) overload wasn't provided

## 返回值传递

> 在所有情况下函数调用的结果都是一个右值

1. 传值返回
2. 传引用返回:参数，函数返回值，引用变量，3者数据类型皆设为左值引用类型。有一处未引用都会造成对象的复制（但使用并返回vector对象，类似python列表，则只要将参数设为左值引用类型即可）。
3. 传常量引用返回
4. 右值移动返回
## std::move

std::move使一个值易于移动，可将左值转换为右值。
	
	void swap(vector<string> & x, vector<string> & y){
		//temp，x，y都为左值，会进行3次复制
		vector<string> temp = x;
		x = y;
		y = temp;
	}
	
	void swap(vector<string> & x, vector<string> & y){
		//temp，x，y都为左值，使用std::进行3次移动
		vector<string> temp = std::move(x);
		x = std::move(y);
		y = std:move(temp);
	}


### new operator

int *A = new int{10};

When using new,memory is allocated on heap,and it's pointer needs to be deleted otherwise it will live and thus causes memory leak.

But new doesn't always mean memory will be allocated on heap , it depends like if A is local variable (like in a method) it will be on stack memory Or if A is a member of a class then it will be on heap when instance of class is created.


! if A is static it will be on stack memory always!


强制类型转换，float转变为int
	
	float var2 = 3.14f;
	int i3 = static_cast<int> (var2);


## 类的5大函数

> 构造函数：与类同名但没有返回值,创建类对象时自动调用

在类中声明变量，在构造函数中初始化变量

- 析构函数（destructor）
- 拷贝构造函数（[copy constructor](https://en.cppreference.com/w/cpp/language/copy_constructor)）
- 移动构造函数（move constructor）
- 拷贝赋值运算符（copy assignment operator)
- 移动赋值运算符（move assignment operator)

1.析构函数

调用条件：一个对象运行超出范围,或使用了delete。默认对对象的每个数据成员调用。

设置默认值：default value exists in function declaration rather than function definition

### C++风格数组

int arr1[10] // arr1是常量指针，传递到函数时只传递指针的值而丢失指针大小，需传递数组大小作为函数的另一个参数
int *arr2 = new int[n]; // arr2不是常量指针,n动态分配，编译时无问题
delete [] arr2;


# 运行机制：

声明类对象：

- ClassName2 obj2{};
- ClassName2 obj2{};
- ClassName2 obj2{par1,par2};

- ClassName2 obj2(); // 引起歧义，可能是调用函数返回ClassName2类型的值。

### 运行细节

name1.h

	#pragma once // 防止文件被包含多次
	#include <iostream>
	class Employee{};
	// g++中，header文件中包含iostream,会自动using namespace std;但在其他编辑器中不可行
	// header中链接了iostream，后续所有代码及其他文件使用name1.h时都在此命名空间内，慎用。

name1.cpp

	#include vector
	int main(){
		cout << "no need using namespace std " << endl;
		return 0;
	}
	

在header声明命名空间，类。在cpp中定义类的函数

构造函数初始化类成员变量的2中方式:

- className::constructor():parName1(value1),parName2(value2){};
- className::constructor(){ parName1=value1;parName2=value2; };


## 测试

### 1.测试左值引用

	#include <iostream>
	#include <string>
	#include <vector>
	using namespace std;
	
	int a2 = 10;
	int a3 = 12;
	vector<int> a4 = {10,11,12};
	vector<int> a5 = {16,26,36};
	
	vector<int> arr = {a2,a3};
	vector<int> arr2 = {10,12};
	vector<vector<int>> arr3 = {a4,a5};
	
	int fin(vector<int> ar)
	{   
	    int xx = ar[1];
	    cout << &xx << endl;
		return xx;
	}
	
	const vector<int> & fin2(const vector<vector<int>> & ar)
	{
		return ar[1];
	}
	
	int main() {
	    string s = "seprator";
	    auto lv = fin(arr);  // true
	    const int & lv2 = fin(arr);
	    auto lv3 = fin(arr2);  // true
	    const vector<int> & lv4 = fin2(arr3);
	    auto &lv5 = a3;
		cout << s << endl;
	    cout << &lv << endl;
	    cout << &lv2 << endl;
	    cout << &lv3 << endl;
	    cout << &lv4 << endl;
	    cout << &lv5 << endl;
	    cout << s << endl;
	    cout << &arr[1] << endl;
	    cout << &arr2[1] << endl;
	    cout << &arr3[1] << endl;
	}

output：

	0x7ffe7eb13cfc
	0x7ffe7eb13cfc
	0x7ffe7eb13cfc
	seprator
	&lv: 0x7ffe7eb13d24
	&lv2:0x7ffe7eb13d2c  // 引用了右值
	&lv3:0x7ffe7eb13d28
	&lv4:0x1ef7cf8
	&lv5:0x601b48
	seprator
	&arr[1]: 0x1ef7c64
	&arr2[1]:0x1ef7c84
	&arr3[1]:0x1ef7cf8 
	&lv4 == &arr3[1]  // 全部引用，才能不复制而引用原地址，const可选

