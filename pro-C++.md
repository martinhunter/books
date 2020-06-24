运行编译机制注释：(mechanism)



## 对象

对象：是可存储值，地址值，变量等。在C++中，指类的实例

#### 类型推断

使用 auto,decltype 自动判断右值的数据类型

最好使用decltype(auto)判断类型：

	const sreing message = "test";
	const string& foo(){ return message };
	
	const auto & f1 = foo();
	decltype(foo()) f2 = foo()
	decltype(auto) f3 = foo()
	
	/* f1,f2,f3作用相同,
	但f2中foo()调用2次
	推荐使用f3，
	f1也可行，不推荐f2*/

#### 强制类型转换：

exp：类型转换的3种方法，推荐第三种

	float init = 3.14f;

	int var1 = (float) init; // C语言中的转换
	int var2 = float(init); // 将float当做函数的转换
	int var3 = static_cast<int> (init); // C++推荐的类型转换 

NOTE：部分数据类型可自动转换。exp：shot可自动强制转换为long类型数据 `short a = 10; long b = a;`

## 栈和堆

栈：如果当前函数foo()调用另一个函数bar()，任何从foo()传递给bar()的参数都会从foo()栈帧复制到bar()栈帧，bar()执行完销毁内存，其中声明的所有变量都不再占用内存(包括foo()复制过来的参数)，此过程自动执行。

堆：想在函数调用结束后依然保存其中声明的变量，可将变量放到堆中。

NOTE：指针通常指向堆内存，但也可指向栈中的变量（&variable）。

### 使用构造函数创建对象

1.创建`基于栈的对象`

	Employee stackEmployee("Martin","Hunter");
	/*
	定义了有参构造函数而不定义无参构造函数Employee(){}，
	则Employee stackEmployee;会报错。因为此时不再自动生成并调用默认构造函数。
	但若无任何构造函数则调用默认构造函数 Employee()=default;，不再报错。
	但Employee stackEmployee();没有问题
	*/
	stackEmployee.setPassengerName("seman");

2.使用普通指针和new创建`基于堆的对象`,不推荐

	// 想要明确地动态分配内存（置入堆中），就要先声明一个指针（需手动释放），并使用new操作符分配内存。

	int * inter = new int; // inter指向一个整数值的地址，不能后续再加上[]
	Employee * normalPointer = new Employee();
	normalPointer->setPassengerName("seman");
	// 在堆中创建对象时，通过`ptr->`menber访问成员，以替代`（*ptr).`member
	
	delete normalPointer;  // 释放了此地址的内存但指针依然指向此地址，并可能在后来修改此地址的值
	normalPointer=nullptr;

NOTE：delete只对new操作符产生堆空间起作用。

3.使用智能指针创建`基于堆的对象`

	auto smartPointer = make_unique<Employee>();
	smartPointer->setPassengerName("seman");
	// no need to delete normalPointer

### new与delete

1.new的作用：通常用于在堆（也可在栈）中开辟新的内存空间

exp:使用new创建新数据

	创建一个int类型的数据10，并用指针A指向它；
	`int *A = new int{10};`
	
	创建数组，其中存储的数据类型为int\*，因此B是为int\*类型的指针
	`int\* \*B = new int\* [10];`

exp:使用new创建二维数组

	// new creates space,space size == sizeof(type)*n
	type * pt = new type[n];
	pt[i] == *(pt + sizeof(type)*i)
	// example
	mCell * pt = new mCell[m];
	mCell* * pt = new mCell*[o];

> When using new,memory is allocated on heap,and it's pointer needs to be deleted otherwise it will live and thus causes memory leak.

> But new doesn't always mean memory will be allocated on heap , it depends like if A is local variable (like in a method) it will be on stack memory Or if A is a member of a class then it will be on heap when instance of class is created.

NOTE: if A is static it will be on stack memory always!

2.[delete](http://www.cplusplus.com/reference/new/operator%20delete[]/)的作用：用于deallocate指针所指向的内存块，释放new创建的存储空间并将指针地址设为无效。

使用delete之后指针本身依然可被调用，因此需新赋值或设为nullptr以免出错。

exp:释放new创建的空间

	delete heapPointer; //删除指针
	heapPointer = nullptr;
	
	delete [] arrayName; //删除数组指针
	arrayName = nullptr;













## 变量

#### 1.1 变量
>（绑定一个匿名地址，给匿名地址一个名称）：先对`=`左边进行操作

int x=2337;

x默认bind一个不变的地址值（相当于bind了一个不变的对象），由此地址值指向可变的对象.
变量本身的内存地址在被分配后（销毁前）就不再改变，只能改变其中的值

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


求值(eval)：获取变量名所绑定的地址值中所存储的值

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
 

### 指针变量：Var1绑定的地址不变，地址储存的值为其他变量Var2的地址值

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

### 智能指针：对象超出作用域，如函数执行完毕，自动释放内存

储存在 `memory` 头文件中

- make_unique<clsName>()
- make_share<clsName>()
- make_weak<clsName>()

## 引用

> 引用相当于一个变量的别名（Nick的小名是Nif，但Nick和Nif都指Nick这个人），因此其特性也和此变量相同

特性：创建时就初始化，因此必须先在ctor中初始化引用数据成员(而不能在函数体内），不能引用未命名的右值，除非使用const修饰引用



NOTE：初始化一个引用之后，不能再改变它引用的对象（但可改变此对象的值）

原理：引用名Var1绑定的地址变为其他变量Var2的地址值，此地址的值为Var2的值，此时Var1可直接修改Var2中的值

引用相对于指针的优点：

- 安全，不直接处理内存地址而是处理此地址的值，也不会是nullptr
- 也因此文体好，使用与堆栈变量相同的语法，而不用像指针加上*，&。
- 易于使用，加入到风格中没有问题。
- 明确内存所有权，可修改对象，但无法轻易释放对象的内存。

#### [pointers-vs-references](https://www.geeksforgeeks.org/pointers-vs-references-cpp/)

- Use references
	- In function parameters and return types.
- Use pointers:
	- Use pointers if pointer arithmetic or passing NULL-pointer is needed. For example for arrays (Note that array access is implemented 
	-  pointer arithmetic).
	- To implement data structures like linked list, tree, etc and their algorithms because to point different cell, we have to use the concept of pointers.


### 左引用变量：对一个变量引用

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



## 函数

> 普通函数是只读的，不能进行修改。

> cout所有func，\*func（包括函数指针(\*func) ）的值都为1

形式：

	定义：returnType funcName(paramType param){body; return someValue;}
	调用：funcName(args);

- param传递机制: 默认按值传递
- return传递机制: 默认返回右值

ex: 创建及调用函数

	double outp(SomeClass ob){double rt = ob.doubleValue; return rt;}
	SomeClass obInstance;
	outp(obInstance);

### 函数指针

形式：FuncCopy为指向originalFunc的函数指针,调用方式与普通定义的函数相同。

	定义函数:rtType originalFunc(parType1 par1, parType2 par2){}
	定义函数指针：rtType (*FuncCopy)(parType1, parType2) = originalFunc;
	调用：FuncCopy(arg1, arg2);

特性：函数指针可赋值，因此指向的函数可变，而普通函数不能赋值（只读）

exp: 创建函数指针

	#include <iostream>
	using namespace std;
	
	int ch(double bil, int rr){
	    cout << bil << " and " << rr << endl;
	    return 32;
	}

	void f1()
	{
	    cout << 1 << endl;
	}
	
	void f2()
	{
	    cout << 2 << endl;
	}
	
	int main()
	{
	    int (*pt)(double, int) = ch;
	    int (*pt3)(double, int) = ch;
		cout << ch << endl;
	    cout << *ch << endl;
	    cout << pt << endl;
		cout << *pt << endl;
	    cout << pt3 << endl;
	    cout << *pt3 << endl;
	    cout << pt3(2.2,4) << endl;

		void (*f3)() = f1;
	    f3();
		f2 = f1;  // 普通函数只读，因此报错
	    f3 = f2;  // 函数指针可写/可进行赋值，不会报错
	    f3();

		return 0;
	}

### 匿名函数

形式：`[](parType1 par1, parType2 par2){ body; }`






























## 参数传递机制

> 对一个函数，将函数内相应的形参值初始化为实参的值。如此这个函数获得了实参值的拷贝，而并不会对实参的值产生影响。

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

> 是默认的传递方式，函数接收某个值或者对象的副本

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

## 函数返回值传递机制

> 在所有情况下函数调用的结果都是一个右值

1. 传值返回
2. 传引用返回:参数，函数返回值，引用变量，3者数据类型皆设为左值引用类型。有一处未引用都会造成对象的复制（但使用并返回vector对象，类似python列表，则只要将参数设为左值引用类型即可）。
3. 传常量引用返回
4. 右值移动返回


#### std::move

std::move使一个值易于移动，可将左值转换为右值。调用移动构造函数`Clb(Cls && rhs)`
	
	void swap(vector<string> & x, vector<string> & y){
		//temp，x，y都为左值，会进行3次复制
		vector<string> temp = x;
		x = y;
		y = temp;
	}

	// vector<string> 也可是任意其他class	
	void swap(vector<string> & x, vector<string> & y){
		//temp，x，y都为左值，使用std::进行3次移动

		vector<string> temp = std::move(x);
		//或 vector<string> temp（std::move(x));
		x = std::move(y);
		y = std:move(temp);
	}

#### std::swap

std::swap实际上交换了对象的值。左值与右值中的值互相交换。调用移动赋值运算符函数`Cls& operator=(Cls && rhs)`

move和swap在调用对应的函数后，立即调用右值对象的析构函数













***
***
***

# 类

> 类默认说明符为private，struct默认说明符为public

形式：class YourClassName{};

创建实例： YourClassName inst; // 与 YourClassName inst{}; 作用相同

NOTE:创建类对象最好使用{}，例如 ClsName instance2{args}。创建无参数的实例对象，使用()会被当做返回值为ClsName的函数处理，从而报错

## 构造函数

创建对象/为对象分配空间(mechanism)：创建一个实例对象时（此对象需要32个字节），将未被使用的地址0xbfdd-0xbffd分配（绑定）到此对象，其中的值未进行初始化，都是随机值，此时若指针指向随机值并尝试调用会产生不可知的后果（通常是内存访问错误）

成员变量初始化：0xbfdd-0xbffd的值设置为期望的（有效）初始值

形式：与类同名但没有返回值

作用：创建类对象时自动调用以初始化对象。

#### 隐式转换为类对象：

当`=`左侧为一个类对象，右侧为其他类型值/对象时，若类有参数为右值类型的构造函数，会将右值作为参数传到此构造函数中，以创建一个临时对象，没有则会报错。
	
exp：隐式转换
	
	class Cell
	{
	public:
		Cell(std::string value);
		Cell(int value);  // ins = 10; 会将10作为参数传入此构造函数并创建临时对象
		Cell(double value);
	};
	Cell ins;
	ins = 10;

#### explicit

只用于类的构造函数声明，此构造函数不能自动进行隐式转换,如int转换为double，double装换为类

exp:由于重载了operator+，会尝试将10.3隐式转换为Cell类型的对象，explicit阻止了这个转换

	class Cell{
		Cell::Cell(){}
		explicit Cell::Cell(double val){}
		Cell operator+(const Cell& va){}
	};
	Cell ne(10.5);
	Cell added = ne + 10.3; 


#### 类的安全

- public: 本类、派生类、类外皆可调用（包括读取和写入）
- protected: 本类、派生类可调用
- private: 仅本类可调用

#### 赋值与初始化

- **赋值**： 对已经具有值的对象的值进行修改
- **初始化**（有时也叫“复制”）： 设定一个初始值，如int x = 0; string st = ""; Type* pointer = nullptr;

若只声明而不初始化。
如 int x; cout << x;
则x是一个无意义、无效的任意值。

**类对象的创建过程**

1. 创建类对象A
2. 同时创建类成员(内嵌对象)（调用构造函数前必须先创建对象的所有数据成员）
3. 若成员m1是原始类型（如int，double），只是分配空间，不初始化值,此时是一个任意值
4. 若成员m2是类（对象），分配空间并自动调用此成员类的默认构造函数并初始化（自动调用m2的基类构造函数或委托构造函数）
5. 调用A的构造函数，在函数体中
6. 对m1进行初始化操作
7. 对m2进行的值进行修改（已被初始化）
8. 进行其他操作
8. 完成了A的初始化

#### 构造函数初始化器（ctor-initializer）

[Constructors and member initializer lists](https://en.cppreference.com/w/cpp/language/initializer_list)

[initialization](https://en.cppreference.com/w/cpp/language/initialization)

形式：className::constructor(type value1,type value2):parName1(36),parName2(value2){parName1+=value1;};

作用：创建数据成员时赋值

**类对象的创建过程（通过构造函数初始化器）**

1. 创建类对象A（按所传参数，其构造函数已被选定）
2. 在构造函数的ctor中
2. 创建成员(内嵌对象)
3. 若成员m1是原始类型（如int，double），根据ctor传入的值初始化
4. 若成员m2是类（对象），强制不调用m2类本身的默认构造函数，而是直接根据ctor传入的值对m2初始化（依然会调用m2的基类构造函数或委托构造函数）
6. 调用A的构造函数，在函数体中
6. 进行其他操作
8. 完成了A的初始化

	#include <iostream>
	#include <string>
	using namespace std;
	
	class Super{
	public:
		Super(){mEl = 3.4; cout << "super init " << mEl << endl;}
		Super(double d){cout << "super double init " << d << ". value of mEl: " << mEl << endl;}
		double mEl;
	};
	
	class Cell:public Super{
	public:
		Cell():Super(){mEl = 5.6; cout << "cell init: " << mEl << endl;}
		// Cell(double val):Super(val){cout << mEl << endl;mEl = val; cout << "cell init double: " << mEl << endl;}
		Cell(double val):Super(val){cout <<"inherit from parent: " << mEl << endl;mEl = val; cout << "cell init double: " << mEl << endl;}
	};
	
	class Nail{
	public:
		Nail(int s):mc(33.7){
			ma = 5;
		}
	private:
		int ma;
		Cell mc;
	};
	
	int main(){
		Nail bbs{5};
	
		return 0;
	}

	返回结果：
	super double init 33.7. value of mEl: 1.79005e-307
	inherit from parent: 1.79005e-307
	cell init double: 33.7

必须使用初始化器的数据成员 | - |
- | - |
数据类型 | 说明 |
const数据成员 | 创建时即赋值，而不能后续再更改 |
引用数据成员 | 不指定一个量，引用将无法存在 |
没有默认构造函数的对象数据成员 | 会无法初始化 |
没有默认构造函数的基类 | 会无法初始化 |

exp： 定义不同构造函数产生的影响

	// cond:若m1类型中只定义了有参构造函数
	
	class M1{
		M1(int num){
			im2 = 31;
			im2 += num;
		}
		int im1 = 10;
		int im2;	
	};
	class A{
		// branch 1
		A(M1 & el){
			m1 = el;
		}
		M1 m1{41}; //由于必须调用M1的构造函数，所以必须先设置一个任意参数
		// 此时 M1 m1;会报错
	

		// // branch 2
		// A(M1 & el):m1(el){
		//  	m1 = el;
		// }
		// M1 m1; // 由于不调用M1的构造函数,无需传参
		// // M1 m1{41};也不会调用M1的构造函数
	};

### 默认构造函数（零参数构造函数）

> 可在用户不指定值的情况下初始化所有数据成员。不显式提供则由编译器自动生成

> 不声明任何构造函数，则编译器将自动生成一个无参构造函数（也即默认构造函数）。
> 因此若只声明有参构造函数，在尝试建立无参对象（ClsName instance;)时，编译器就不会自动生成无参构造函数(默认构造函数)

- func() = default; //调用默认值。
- func() = delete; //此构造函数不可再调用，即Cons ins;会报错。同时不定义其他构造函数，则可定义一个只有静态方法的类。

## 类的5大函数

- 析构函数（destructor）
- 拷贝构造函数（[copy constructor](https://en.cppreference.com/w/cpp/language/copy_constructor)）
- 移动构造函数（move constructor）
- 拷贝赋值运算符（copy assignment operator)
- 移动赋值运算符（move assignment operator)



exp:一个包含5大函数的类

	class IntCell{
	public:
		explicit IntCell( int initialValue = 0)
			{ storeValue = new int{ initialValue }; }
		~IntCell()
			{delete storedValue;}
	
		IntCell( const IntCell & src )
			// 拷贝构造函数，处理左值
			{ storeValue = new int( *src.storeValue ); }  //*修饰storeValue而非rhs，相当于*(src.storeValue)，解析地址获得值
	
		IntCell(IntCell && rhs）:storeValue{ rhs.storeValue}
			// 移动构造函数，处理右值
			{ rhs.storeValue = nullptr; }
	
		IntCell & operator=(const IntCell & src)
		// 赋值计算必须有返回值，一般返回对象本身。	
		{
			if( this != &src )
				{ *storeValue = *src.storeValue; }
			return *this;
		}
	
		IntCell & operator=(IntCell && rhs)
		// 移动赋值
		{
			std::swap(storeValue, rhs.storeValue);
			return *this;
		}
		int read() const
			{return *storedValue;}
		void write(int x)
			{ *storeValue = x; }
	
		
	private:
		int * storeValue;
	};

	int main(){
		IntCell a{2};  // 调用普通构造函数
		IntCell d(a);  // 调用拷贝构造函数
		IntCell b = a;  // 调用拷贝构造函数
		IntCell c;
		c = b;  // 调用拷贝赋值运算符
		Int d;
		d = c + b // 调用移动赋值运算符（在IntCell类中重载了operator++)
		a.write(4);
		cout << a.read() << b.read() << c.read() << endl;
	
		return 0;
	}

exp: 一个包含5大函数的类

	#include <iostream>
	#include <string>
	using namespace std;
	
	class Sb{
	public:
		Sb(string m):name(m),ct(21){cout << name << " init " << ct << endl;}
		Sb(const Sb& src) {
			if (name == ""){
				name = "cp-UNKNOWN-" + src.name;
			}
			ct = src.ct;
			cout << "address: " << this << ". " << src.name << " is copied. "<< name << " copy construct " << ct << endl;
		}
		Sb(Sb && rhs):ct(rhs.ct) {
			if (this != &rhs) {}
			if (name == ""){
				// name = move(rhs.name);
				name = "mv-UNKNOWN-" + rhs.name;
			}
			cout << name << " move construct " << ct << endl;
		}
		// for operator=,Sb.name is already inited
		Sb& operator=(const Sb& rhs){
			if (this != &rhs) {
				ct = rhs.ct;
			}
			cout << name << " copy-operator= " << ct << endl;
			return *this;
		}
		Sb& operator=(Sb && rhs) {
			std::swap(ct, rhs.ct);
			cout << name << " move-operator= " << ct << endl;
			return *this;
		}
		virtual ~Sb(){
			cout << "address: " << this << ". " << name << " run destructor " << ct << endl;
		}
		// reload ++
		Sb& operator ++(){
			++ct;
			cout << name << " ++i,modified the old object and return ref of new object " << ct << endl;
			return *this; 
		}
		Sb operator ++(int){
			cout << name << " runs i++ start" << endl;
			Sb temp(*this);
			temp.ct = 46;
			++ct;
			cout << name << " runs i++ end, returns the original: " << temp.ct << ". rather than new object: " << ct << endl;
			return temp; 
		}
		int ct;
		string name;
	};
	Sb func(){
		Sb fi("fi");
		return fi;
	}
	Sb f(Sb e){
		return e;
	}
	
	int main(){
		Sb news("news");
		Sb firstRef = ++news;
		cout << "-------------sep-1------------" << endl;
		// the following two lines of code just gives return value of rhs( func() and Sb("fi") here) a name,secondRef calls no function
		// Sb secondRef = func(); 
		// Sb secondRef = Sb("fi");

		// choose 1 from 4, all call move construct
		// Sb secondRef = f(news);
		// Sb secondRef = f(Sb("fi"));
		// Sb secondRef = move(Sb("fi"));
		Sb secondRef = move(func());
		cout << "-------------sep-2------------" << endl;
		Sb thirdRef("thirdRef");
		thirdRef = news;
		thirdRef.ct = 123;
		++news;
		cout << "-------------sep-3------------" << endl;
		cout << "address Of news: " << &news << ", it's news." << endl;
		cout << "address Of firstRef: " << &firstRef << ", it's unknown." << endl;
		cout << "address Of secondRef: " << &secondRef << ", it's fi." << endl;
		cout << "address Of thirdRef: " << &thirdRef << ", it's thirdRef." << endl;
		thirdRef = news++;
		thirdRef = func();
		cout << "-------------sep-4------------" << endl;
	
		return 0;
	}
	


### this

> a pointer points to instance object,used only in Class scope

方法被调用时会传递隐藏的this指针，this指针指向对象，对this指针解引用来访问此对象的数据成员或方法。

this与对象的关系：

	this == &objIns;
	*this == objIns;
	

ex：this的使用

	class Cls
	{
	public:
		void func(value)
		{
			// 调用func时默认传入了this，且this指向此类的inst对象
			this->value = value;
		}
		void func2(value2)
		{
			this->func();
		}
	private:
		int value;
	};
	
	Cls inst;
	inst.func(4);



特点：

- 拷贝/移动构造函数，对象未构建完成，调用时赋值/初始化。
- 拷贝/移动赋值运算符，对象已预先构建完成，调用时修改对象的值
- 移动构造函数/移动赋值运算符调用完成后，立即调用临时对象的析构函数

	Cls f(Cls e){ return e;}
	Cls func(){Cls temp("fi"); return temp;}

	Cls origin;
	Cls copy-cons(origin);
	Cls copy-cons2 = origin;

	// 以下2行代码不能再添加move，否则会调用移动构造函数2次。
	Cls move-cons = f(origin);  // 已有的对象作为参数传入并返回
	Cls move-cons2 = f(Cls("fi"));  // 对象直接创建作为参数传入并返回
	
	// 必须使用move,否则不调用move-constructor
	Cls move-cons3 = move(Cls("fi")); // 直接创建新对象,作为右值传递给move
	Cls move-cons4 = move(func());  // 返回函数内部创建的新对象,作为右值传递给move

	Cls opera;
	opera = origin; // call operator=
	oprta = origin++;  // call move-operator=
	opera = func()  // call move-operator=

### 拷贝构造函数

> 用源对象中相应的数据成员的值，初始化新对象的每个数据成员。采用源对象的const引用作为参数

> 若成员是一个对象，初始化意味着调用它的复制构造函数，无返回值

形式：`ClsName::ClsName(const ClsName & src):m1(src.m1),m2(src.m2){};`

显式调用拷贝构造函数：

	Cell ob(10);
	Cell cpOb(ob); // 参数为其他对象，调用Cell类的拷贝构造函数
	Cell cp2 = ob; // 使用=，调用Cell类的拷贝构造函数

函数参数为对象，或返回值为对象时，自动调用其拷贝构造函数：

	Cls realArg;
	Cls func(Cls par){};
	
	func(realArg); //参数与返回值对象会调用自身类的拷贝构造函数

运行过程：

1. 创建新的形参对象par
1. 调用形参对象的拷贝构造函数
1. 将实参(realArg)作为拷贝构造函数的参数传入，完成形参对象par的初始化,等同于运行了 Cls par(realArg);
1. 运行{}中的代码
1. 脱离作用域后，形参对象par被销毁

NOTE：若只定义拷贝构造函数，而无其他构造函数，那么就无法创建这个类的对象，因而也无法拷贝其他这个类的对象。(若本体无法创建，那么也无法创建复制体）

exp:复制

	class Minor{
	public:
		Minor(){b = 10; cout << "init Minor" << endl;}
		Minor(const Minor& ele):b(ele.b){cout << "minor copy" << endl;}
		int b;
	};
	class Major{
	public:
		Major(){cout << "init Major" << endl;}
	
		Major(const Major& elem):mi(elem.mi),s(elem.s){cout << "major copy" << endl;}
		Minor mi;
		int s;
	};
	int main(){
		Major a;
		
		Major bb(a);
		return 0;
	}

	>>> // 先创建对象,然后调用对象的拷贝构造函数进行复制
	init minor
	Major init 	
	minor copy
	major copy

### 拷贝赋值运算符

默认的C++赋值行为几乎与默认的复制行为相同

形式：

	ClsName& ClsName::operator=(const ClsName & rhs){
		if (this != &rhs) // 避免自赋值
		{
			m1 = rhs.m1; // 对象已被初始化，因此不用初始化列表，而是在函数体内赋值/修改值
			m2 = rhs.m2;
		}

		//需要有返回值，返回对象的引用（如此可以连续赋值），一般用*this指代对象。
		return *this;
	}

exp：`=`其实调用了函数`operator=`

	Cell myCell(5),anotherCell;
	anotherCell = myCell;
	// 调用了antherCell的赋值运算符，参数为myCell.

	myCell = anotherCell = aThirdCell; // 连续赋值

	myCell.operator=(anotherCell.operator=(aThirdCell)); // ***连续赋值的完整形式

NOTE：拷贝构造函数在对象创建/声明（初始化）时使用，拷贝赋值运算符在对象已经构建完成，修改值时使用

### 移动构造函数,移动赋值运算符

调用条件：源对象是在复制或者赋值后会被销毁的临时对象，例如作为函数返回值

运行过程：

- 将成员变量从源对象移动/交换到新对象，然后将源对象的变量设为空（销毁），即将内存所有权从一个对象移动到另一个对象。
- 基本上对成员变量进行表层复制，然后转换已分配内存的所有权，从而阻止悬挂指针和内存泄漏。

NOTE：

1. 源对象有成员mCell，是一个指向数组的指针，
1. 先将mCell指针赋值给新对象，
1. 新对象获得了这块内存，
1. 然后将源对象的mCell指针设为空指针，
1. 这样源对象的析构函数运行时（销毁源对象的mCell），就不会释放这块内存

noexcept:告诉编译器，它不会抛出任何异常，保证兼容标准库

形式：

	Cell(Cell&& src) noexcept;
	Cell& operator=(Cell&& rhs) noexcept;

exp:

	Cell::Cell(Cell&& src) noexcept{
		mWidth = src.mWidth;
		mHeight = src.mHeight;
		mCells = src.mCells;
		// 初始化源对象
		src.mWidth = 0;
		src.mHeight = 0;
		src.mCells = nullptr;
	}

	Cell& Cell::operator=(Cell&& rhs) noexcept{
		if (this == &rhs) {
			return *this;
		}
		freeMemery(); // 同拷贝赋值运算符，必须释放源对象已分配的内存
		mWidth = rhs.mWidth;
		mHeight = rhs.mHeight;
		mCells = rhs.mCells; // 现在是一个空的指针
		// 初始化源对象
		rhs.mWidth = 0;
		rhs.mHeight = 0;
		rhs.mCells = nullptr;
		return *this;
	}

### 析构函数

形式： ~Destruct()

作用:逐一销毁成员，然后删除对象。例如释放内存或关闭文件句柄。对于new创建的裸指针，需析构函数delete，以免内存泄漏

调用条件：一个对象运行超出范围,或使用了delete。

NOTE：在构造函数中抛出异常时不会调用析构函数


### 委托构造函数：

作用：可调用同一个类的其他构造函数（链式调用）

形式：必须放在构造函数初始化器中，且是初始化器中的唯一的成员，以避免多次初始化

exp：Cell类中的参数为int类型的构造函数现在会自动调用以参数为String类型的构造函数，成为了一个委托构造函数
	
	Cell::Cell(int val):Cell(intToString(val)){body;}

### 动态分配内存

数据成员为pointer时产生的问题：内存泄漏

1. 拷贝构造函数产生问题：将源对象作为参数传入函数，新建的形参对象创建指针成员并复制源对象的指针（但并未创建新的heap空间），指向源对象的同一个heap空间，可修改其中的值。且此形参对象对象离开作用域时会析构形参对象的heap空间（也是源对象的heap空间）
2. 拷贝赋值运算符产生问题：使用赋值运算符，导致源对象的heap指针直接指向另一heap，而未销毁原有heap

起因：对于原始类型，int，double，pointer，只提供表层（或者按位）复制或者赋值。

exp：动态分配内存实例

	class Cell{};
	
	class SpreadSheet{
	public:
		~SpreadSheet(){
			for (int i = 0; i < mWidth; i++) {
				delete [] mCells[i];
			}
			delete [] mCells;
			mCells = nullptr;
		}
		SpreadSheet(int inWidth,int inHeight):
			mWidth(inWidth),mHeight(inHeight)
		{
			mCells = new Cell* [ mWidth];
			for (int i = 0; i < mWidth; i++)
			{
				mCells[i] = new Cell[ mHeight];
			}
		}
	private:
		Cell** mCells;
		int mWidth;
		int mHeight;
	};
	
	void printSheet(SpreadSheet s)
	{ 
		std::cout << "print anything" << endl;
	}
	
	int main(){
		SpreadSheet s2(3, 4);
		printSheet(s2); // 此行运行完成后，s2也被销毁

		SpreadSheet s3(5, 6), s4(7, 8);
		s3 = s4;  // s3开辟的内存被遗弃而未销毁，导致内存泄漏
		return 0;
	}

解决方式：需要重新编写拷贝构造函数和赋值运算符，以提供深层的内存复制

1. 拷贝构造函数：原来并未创建heap，所以只需创建新heap，并逐一复制
1. 赋值运算符：原heap大小可能与新heap大小不同。需先释放原有heap，再创建新heap pointer，并逐一复制

exp：重写拷贝构造函数，赋值运算符

	void copyFrom(const SpreadSheet& src){
		mWidth = src.mWidth;
		mHeight = src.mHeight;
		mCells = new Cell* [mWidth];
		for (int i = 0; i < mWidth; i++)
		{
			mCells[i] = new Cell[ mHeight];
		}
		for (int i = 0; i < mWidth; i++)
		{
			for (int j = 0; j < mHeight; j++)
			{
				mCells[i][j] = src[i][j];
			}
		}
	}

	SpreadSheet(const SpreadSheet& src)
	{
		copyFrom(src);
	}
	
	SpreadSheet operator=(const SpreadSheet& rhs)
	{
		if (this == &rhs){
			return *this; // 避免自我赋值
		}
		// 先释放之前的内存
		for (int i = 0; i < mWidth; i++) {
			delete [] mCells[i];
		}
		delete [] mCells;
		mCells = nullptr;

		copyFrom(rhs);
		return *this;
	}

NOTE：将拷贝构造函数和赋值运算符标记为private，且内容为空，来禁用复制、赋值。

## 类与对象

#### 前置声明

形式：class ClassName;
作用：避免类之间互相循环引用

NOTE:引用需在ctor-initializer中先初始化，才能存在

#### static（静态，只修饰类成员、类方法）

static对象，在main(){}执行完成之后，再调用析构函数(mechanism)

> 静态方法不指向特定对象，因此没有this指针

> static方法不需要再加const，因为它不可能改变实例内部的值

静态成员的作用：一些通常不变或只对类有意义的数据，只需在类中存储一份，而不是所有实例中都包含。

普通函数中的静态变量的作用：记住某个函数是否执行了特定的初始化操作，但是confusing，建议只在对象中使用

用法：static类成员需要在类定义的cpp文件中分配内存（初始化），memberType Cls::staticMember;。
实例对象调用static类成员时，实际上调用的是Cls::staticMember，因此若不初始化就会报错。
默认初始化为0或nullptr。

静态方法：方法只用于类对象而非实例对象，不访问特定对象（指非静态的类数据成员）的信息时，可改为静态方法

可以理解为：static方法相当于在类之外（指全局环境）定义的普通函数，但却能访问此类的private和protected静态数据成员

NOTE：某个实例对象调用静态方法时，只会访问这个对象的静态数据成员

静态链接(static linkage)


NOTE：page162.如果同一类型的其他对象对于静态方法可见（例如传递了对象的指针或者引用），静态方法也可以访问其他对象的非静态成员

NOTE：静态方法最后不加const，因为静态方法不指向实例数据成员，更不会改变类成员.`static int foo() const {}; // 应删去const`

## const(常量)

> reference: [cv (const and volatile) type qualifiers](https://en.cppreference.com/
> w/cpp/language/cv)

运行机制：One has to initialize const variable immediately in the constructor because, of course, one cannot set the value later as that would be altering it.

作用：确保const所修饰的值不会变化。

> constants are useful for parameters which are used in the program but do not need to be changed after the program is compiled. It has an advantage for programmers over the C preprocessor ‘#define’ command in that it is understood & used by the compiler itself, not just substituted into the program text by the preprocessor before reaching the main compiler, so error messages are much more helpful [ -- const](http://duramecho.com/ComputerInformation/WhyHowCppConst.html)

exp:在类中声明一个使用const的方法

	// 最左侧的const修饰int，其实应为 int const ，但习惯上写为 const int 

	`const int * const Method3(const int * const & referenceToAPointer) const;`
	

5个const的含义如下(const始终修饰const左侧的符号)：

1. return value points to a constant integer
1. return value is a constant pointer.
1. parameter points to a constant integer
1. parameter is a constant pointer.
1. bans Method3 in ClassObject from altering any member variable of ClassObject(but access/read member is allowed).

第5种const的工作原理：在类方法最后的const，会将方法内用到的数据成员都标记为const引用，因此试图修改数据成员报错。

对于const对象,如`const ClsName inst;`，只能调用有此对象中有第5种const修饰的类方法。

#### 难以分辨const作用的情况

	const int * ptr = new int[10];
	int value = 5;
	ptr = &value; // success
	ptr[1] = 7; // error

第6种const的含义如下：

const修饰int，而非修饰ptr，因此ptr本身可变，而`*ptr`不可变，即ptr[0],ptr[1]等皆不可变

#### const与引用：

对于引用`&`，不需要用const修饰，因为引用指向的对象不变，本身就是const的。

exp：引用/指针变量被const修饰后，不可改变值，但其源变量依然可以改变值

	int z = 3;
	const int* zptr = &z;
	const int& zref = z;
	z = 7;
	*zptr = 8; // error
	zref = 10; // error

NOTE：类数据成员若为常量引用，则只能调用此类数据成员的常量方法

NOTE：将不修改对象的方法声明为const，如此可在程序中引用const对象

NOTE：不要将析构函数设置为const，否则无法正确地销毁const对象

### constexpr(常量表达式)

形式： constexpr int foo(){return 10;}

机制及限制：编译期间对constexpr函数求值，函数不允许有任何副作用

- 是return语句，不含goto，try catch，可调用其他constexpr
- 返回类型是字面量类型，不能是void
- 函数若是类成员，不能是虚函数
- 函数的所有参数都应是字面常量
- 编译单元（translation unit）中定义了constexpr函数之后，才能调用这个函数，因为编译器需要知道完整定义
- 不允许使用dynamic_cast,new,delete

作用：将函数返回值作为数组的参数时`int Array[foo()];`,foo()必须用constexpr修饰

constexpr构造函数：

- 所有参数都是字面量类型
- 同constexpr函数体要求
- 所有数据成员都用常量表达式初始化
- 创建对象时也必须用constexpr修饰

	class Rect{
	public:
		constexpr Rect(int width,int height):mWidth(width),mHeight(height){}
		constexpr int get() const { return mWidth*mHeight;}
	private:
		int mWidth,mHeight;
	}
	
	constexpr Rect(2,5);
	int arr[Rect.get()];

### mutable数据成员

作用："逻辑"上是const，但实际改变了对象的数据成员

exp：在const类方法中，mCounter需要发生变化（其他数据成员不变），使用mutable修饰在const类方法中变化的成员并初始化

class Cell{
public:
	double getValue() const
	{
		mCounter++;
		return mValue;
	}
private:
	double mValue;
	mutable int mCounter = 0;
};

### 重载

作用：函数名称相同，可根据参数类型或数目不同，是否有const，自动调用相应的函数

exp: 可显式删除重载，避免隐式转换

	typeName foo(paramType param) = delete;

NOTE：只在方法声明中指定默认参数，而不在定义中指定

NOTE：所有参数有默认值的构造函数等同于默认构造函数，所以不能同时声明这2种构造函数，否则编译器不知道调用哪一个

### [内联(inline)方法](https://www.geeksforgeeks.org/inline-functions-cpp/)

> 内联比`#define宏`安全

> 类方法/友元函数是隐式的内联方法

起因：默认情况使用函数调用过程开销较大

内联的作用：减少了调用者函数到被调用函数（被调用者）的切换时间的开销。

原理：编译器在编译时替换内联函数的定义，而不是在运行时引用函数定义。

调用函数调用被调用函数的过程（已生成可执行文件/程序）：

1. 遇到函数调用指令
1. CPU存储此指令的地址
1. CPU存储函数参数的复制
1. 跳转到被调用函数的内存位置（控制权转交给被调用函数。）
1. 执行被调用函数代码
1. 存储被调用函数的返回值到预定义的存储位置/寄存器中
1. 然后跳回到执行被调用函数之前已保存的指令的地址（控制权返回给调用函数。）

内联函数编译的过程：

1. 编译器用将函数调用语句替换为函数体或方法体主体的副本。
1. 编译整个代码
1. 程序运行不再执行调用，即不必跳转到另一个位置来执行该函数，然后再跳转回来，因为被调用函数的主体代码已可供调用程序使用。

形式：

1. 在方法·函数前加上`inline`。 `inline typeName foo(){};`
2. 方法定义直接放在类定义中，而不再声明

缺点：

- 对于计算步骤多的函数无效，例如while循环。
- 多次执行一个内联函数，会产生相同函数主体的多份副本,导致更大的可执行文件。大执行文件更加可能内存溢出会，导致计算机性能下降。
- 消耗更多的寄存器以存储变量
- 太多的内联还会降低指令高速缓存的命中率，从而降低了从高速缓存到主存储器的指令获取速度。
- 增加了编译时间
- 内联函数对于许多嵌入式系统可能没有用。因为在嵌入式系统中，代码大小比速度更重要。

exp:使用inline前后的实际效果

	// 编译前是2个函数
	inline type1 calledFoo(param){
		calledFooBody;
	}
	
	type2 caller(){
		calledFoo(realArg);
		other code;
	}
	
	// 编译后等同于转变为1个函数
	
	type2 caller(){
		calledFooBody;  // realArg substitues param in calledFooBody and now consumes additional registers
		other code;
	}

NOTE:编译器会根据实际情况仔细选择是否将内联函数进行内联，若不适合则当做普通函数处理。

NOTE:函数进行I/O类操作则声明为inline也没有任何效果

### 嵌套类

作用：在类中定义类

exp:需要完整的作用域，最好使用别名

	int scop1::scop2::scop3::foo(){body}
	`using scopAlias = scop1::scop2::scop3;` // 别名需在类定义的外部,达到最方便
	
	// 现在可用`scopAlias::foo()`取代`scop1::scop2::scop3::foo()`
	int scopAlias::foo(){body}

#### 枚举

类中存在多个常量时,可在类声明中枚举类并初始化

NOTE:比#define方便，define的函数参数需为int类型而非枚举类

	class Sheet{
	public:
		enum class Cons{Red = 1, Green,Blue};
	private:
		Cons el = Cons::Red;
	};
	// 且外界也可调用
	Cons oter = Sheet::Cons::Green;

#### 友元

定义：其他类，其他类的成员函数或非成员函数`被`某个类声明为友元，友元可访问某个类所有数据和方法（包括private，protected）

理解：是被某人当做朋友，而不能主动声明是某人的朋友（某人并未答应你这样做）。

使用条件：友元可以违反封装的原则，因此只在特定情况（如运算符重载，需要访问private，protected成员）时使用。

exp:友元（如friendSheet，func，friendSheet::func）可调用Sheet中的所有方法
	
	class friendSheet1{};
	class friendSheet2{};

	class Sheet{
	public:
		friend class friendSheet1; // 友元类不用传递参数
		friend bool func(const Sheet& sh); // 这是一个不定义在类中的普通函数
		friend void friendSheet2::func(const Sheet& sh); // 需将类的常量引用作为参数传递给友元函数
	};

## 重载

#### 重载基础运算符

基础运算符是一种简写形式： `a + b;` 的完整写法为 `a.operator+(b);`

phase1：

exp:重载`+`，其函数为operator+

	class Cell{
	public:
		Cell operator+(const Cell& inst) const
		{
			Cell newCell;
			newCell.set(mValue + inst.get());
			return newCell;
		}

	};
	Cell one(4),two(5);
	Cell nCell = one + two; // 此处的 + 已重载，等同于one.operator+(two);

phase2：
	
运算符重载的问题：被加的值产生隐式转换，构造函数会试图将其他类型转换为Cell类型,且会产生一个临时Cell对象，降低效率

解决方法：被加值类型不同，为不同类型都重载`+`
	
	Cell Cell::operator+(double rhs) const
	{
		return Cell(mValue + rhs);
	}

phase3：

运算符重载的问题：`+`左侧为其他类型，右侧为Cell类型，就会出现错误

解决方法：重载全局`+`(由于是重载，不会影响其他加法）

	Cell operator+(const Cell& lhs,const Cell& rhs)
	{
		Cell newCell;
		newCell.set(lhs.get() + rhs.get());
		return newCell;
	}

问题：全局函数不能直接调用类的私有属性

解决方法：将此函数声明为Cell类的友元，类定义中添加如下声明，再重载全局函数

	Cell operator+(const Cell& lhs,const Cell& rhs) { 同上 }
	class Cell{
		friend Cell operator+(const Cell& lhs,const Cell& rhs);
		ommited
	};

NOTE:比较运算符写法相同，但返回值类型改为bool

#### 重载简写算数运算符

`+=`的特性: 修改左值，返回对左值的引用，作为左值类的方法而不是全局函数

exp：

	Cell& operator+=(const Cell& rhs);

	Cell& Cell::operator+=(const Cell& rhs)
	{
		set(mValue + rhs.mValue);
		return *this;
	}

### 创建稳定的接口

实现类(impClass)：就是一个普通的类
接口类：使用实现类的副本，并改为以下形式，private有只有一个数据成员，即指向实现类对象的指针`std::unique_ptr<implClass> mImpl;`,无public数据成员，public成员方法的函数体变为`mImpl->`调用同名方法，构造函数体改为创建一个指向指针的implClass对象。

exp:修改后

	class Cell{
	private:
		std::unique_ptr<implClass> mImpl; //指向对象的指针
	};

	Cell::Cell(params){
		mImpl = std::make_unique<implClass>(params);
	}
	Cell::Cell(const Cell& src){
		mImpl = std::make_unique<implClass>(*src.mImpl); // 复制构造函数
	}
	Cell Cell::operator=(const Celll& rhs){
		*mImpl = *rhs.mImpl; // std::unique_ptr类型初始化后不能再赋值，解引用后强制使用直接对象赋值
		return *this;
	}
	
	Cell& Cell::getCellAt(int x, int y){
		return mImpl->getCellAt(x, y);
	}
	
作用：接口类不需重新编译

## [继承](https://tonyphuah.neocities.org/inheritance.html)

形式： `class Sub : public Super1,public Supre2 {};`

- 所有方法及数据成员都会被继承
- 父类构造函数不会被继承，即派生类对象初始化必须重写。
- 派生类会先自动调用父类默认的构造函数来初始化成员(mechanism)
- 通过ctor选择要调用的父类构造函数,且父类构造函数需放在ctor-initialization的最前边以避免将派生类的成员值覆盖。

#### 禁用继承：在类或方法后使用final

形式： `class ClsName final{};`

#### virtual

作用：派生类中重写方法，若无virtual则派生类，则基类对象的引用或指针使用派生类赋值时，无法调用派生类的函数，且可能导致无法正确析构

1. 先在基类声明时对相应的方法（但不包括构造函数）加上virtual。形式： `virtual void func();`
2. 再在派生类声明在方法最后加上override。形式： `virtual void func() override;`  // 此时virtual可省略，但建议写上
3. 将函数标记为virtual后，其派生类也一直是virtual,但派生类中最好也显式声明virtual
3. 在方法定义中不需要再加virtual和override

NOTE：可将基类所有方法（包括析构函数，但不包含构造函数）加上virtual

exp: 所有析构函数必须加上virtual(显式声明),无virtual，则直接调用Parent类的析构函数，而不调用派生类及其类数据成员的析构函数

	Parent* ptr = new Child();
	// 代码使用delete删除一个实际指向派生类的基类指针时，析构函数调用链将被破坏
	delete ptr;

基类对象的引用或指针与派生类实例的关系：

1. 引用或指针可以指向某个类的对象或者派生类的对象
2. 基类引用对象只能调用基类中已存在的方法
2. 若基类引用对象的方法已在派生类中重写，则会调用派生类中的重写后的方法
3. 基类引用对象尝试调用派生类中新添加的方法会报错

原因：继承是单向的，基类并不知道派生类中的信息（新添加的方法，成员）。

exp:对基类对象的引用或指针使用赋值

	Sub mySub;
	Super& ref = mySub;
	Super* sPtr = new Sub();
	ref.someMethod(); // 调用派生类中的重写后的方法
	sPtr->someMethod(); // 调用派生类中的重写后的方法
	// Sub类中新添加一个方法newSubMethod
	mySub.newSubMethod();
	ref.newSubMethod(); // 尝试调用派生类中新添加的方法，但Super类中无此方法，报错
	sPtr->newSubMethod(); // 报错

exp:对基类对象使用赋值，将遗失派生类的所有信息

	Sub mySub;
	Super assignedObject = mySub;
	assignedObject.someMethod(); // 不会调用重写后的方法

创建对象的步骤(mechanism)：

1. 若类有父类，执行父类的默认构造函数。除非此类的ctor中调用父类特定的构造函数，否则调用默认构造函数（`Sub::Sub():Super(param){}`）
1. 类的非静态数据成员按声明的顺序创建
1. 执行该类的构造函数

递归使用这个顺序，若一个类有父类、祖父类，则先初始化祖父类

析构对象的顺序（同创建顺序相反）：

1. 执行该类的析构函数
1. 类的数据成员按声明的相反顺序销毁
1. 若类有父类，调用父类的析构函数

NOTE：类定义中调用父类或其他派生类方法注意解析正确的类作用域

- 向上转型：使用基类指针或引用，派生类对象转换为父类对象

- 向下转型：父类对象转换为派生类对象(不推荐，对象可能不属于派生类，且作者之外的人可能不清楚传递哪种指针)。`Sub* mySub = 
- _cast<Sub*>(inSuper);`

exp：必须使用向下转型时使用dynamic_cast，以使用对象内建的类型信息，拒绝没有意义的类型转换

	void lessPresumptuous(Super* inSuper)
	{
		Sub* mySub = dynamic_cast<Sub*>(inSuper);
		if (mySub != nullptr) {
			// 成功转换
		}
	}

### 多态

#### 抽象类

纯虚方法：显示说明该方法只需声明，不需要定义其具体实现，而是在派生类中根据实际需要重载
纯虚方法形式 :方法声明最后加上`=0`，`virtual rtTypeName foo() = 0;`

定义：包含至少一个纯虚方法的类称为抽象类

特性：由于纯虚方法的存在，此时类不能产生实例，无法创建对象，但可被继承，必须定义virtual析构函数。



exp：对抽象类，仅其派生类可实例化

	Super mySuper; // 错误，不能实例化抽象类
	Super* ptr = nullptr;
	ptr = new Sub();

NOTE：派生类必须将所有纯虚方法重载，否则派生类也变成抽象类

### 多重继承

定义：继承多个父类

存在问题：

1. 名称歧义：多个父类中具有同名方法。要调用特定父类的方法
	- 解决1.显式向上转型。 dynamic_cast<SuperCls&>(inst).foo();
	- 解决2.调用时限定作用域。inst.SuperCls::foo(); // SuperCls::foo()是一个整体
	- 解决3.直接访问父类方法。void Sub::foo(){ Super::foo(); } 
	- 解决4.在子类声明中添加。 using SuperCls::foo;
2. 从同一个父类继承2次：
	- 解决：是人为错误，需修改类层次结构
3. 基类歧义：类的两个父类具有相同的父类（也是类的祖父类），父类不重写方法就会调用祖父类的方法而产生歧义
	- 解决.将（祖父类）设为纯抽象类，其内所有方法设为纯虚方法（除了构造函数）。这样所有父类都强制需必须重写方法，不再产生歧义

用途：混入类(mix-in)

修改重写方法的特征：

1. 修改返回类型
2. 修改方法的参数

covariant return type（协变返回类型）：原始返回类型是类的指正或引用，重写的方法可以将返回类型改为派生类的指针或引用。

exp:修改返回类型，Cherry\*改为BingCherry\*

	Cherry* CherryTree::pick()
	{
		return new Cherry();
	}

	BingCherry* BingCherryTree::pick()
	{
		auto theCherry = std::make_unique<BingCherry>();
		theCherry->polish();
		return theCherry.release();
	}

exp:修改方法的参数

	class Super{
	pubic:
		Super();
		virtual void someMethod();
	};
	class Sub : public Super
	{
	public:
		Sub();
		
		// 添加2句代码确保即使参数不同，依然是将原方法重载，而非只是在子类中建立新方法。
		using Super::someMethod();
		virtual void someMethod(int i)
	};

override:必须是对父类同名方法（参数也要相同）的重载，若父类无此方法（或者同名但参数不同）则报错

#### 继承构造函数

形式：类定义中添加`using Super::Super;`

限制：1.会继承全部的父类构造函数。2.多重继承时，父类的构造函数的参数相同会导致歧义，报错

解决：类中显式声明参数相同的父类的构造函数。

NOTE:本类的构造函数优先级高于继承的构造函数

NOTE：要确保所有成员变量都正确地初始化

重写方法的特殊情况：

1. 静态基类方法：不能重写静态方法，因为方法不能既是静态的又是虚的。，派生类与基类的同名静态方法互相独立。
2. 重载基类方法：当指定名称和一组参数，以重写某个方法时，编译器隐式地隐藏类中的同名方法的所有其他实例。使用using避免重载该方法的所有版本，`using Super::overload;`。现在所有未在sub中重载的overload(int param)方法不再报错，而是会自动调用Super中的overload(int param)方法。因此为正确报错，应尽量重写重载方法的所有版本，而避免使用using。
3. private或protected基类方法：可重写，但不能调用父类的private方法，换句话说必须重写private方法以调用它。
4. 基类方法具有默认参数：super引用指向sub对象时，调用sub的方法，但会使用Super的默认参数，**`因为
5. 
6. 根据描述对象的表达式类型在编译时绑定默认参数，而不是根据实际的对象类型绑定参数,默认参数不会被继承`(mechanism)**

### 派生类方法修改访问级别

1. 父类的public方法-->子类的protected方法（一般用不到）:
	* 若父类的public方法改为子类的protected方法则子类对象不再能直接调用此方法，而使用父类类型的指针或引用指向的子类对象就可调用。
	* 结论：基类将方法设为public，则派生类方法就没法完全是protected
1. 父类的protectd方法-->子类的public方法（会有用）:
	* 原理同上，但使用父类类型的指针或引用指向的子类对象不再能直接调用此方法

### 派生类的复制构造函数和赋值运算符

- 派生类中未指定时：复制构造函数和赋值运算符默认不继承父类
- 指定时：
	- 未显示链接：会使用默认构造函数初始化对象的父类部分
	- 显示链接： Sub::Sub(const Sub& inSub) : Super(inSub)，才能使用父类的复制构造函数初始化对象的父类部分

exp:链接父类operator=
		
	Sub& Sub::operator=(const Sub& inSub)
	{
		if (&inSub == this)
		{
			return *this;
		}
		Super::operator=(inSub);  // 调用父类的operator=
		// do something
		return *this;
	}

### virtual的真相

C++编译类时，创建一个包含类中所有方法的二进制对象：

branch：非虚情况下，将控制交给正确方法的代码已被硬编码，此时根据编译时的类型来调用方法。
非虚方法重写，实际是创建了新方法（“隐藏”了父类方法），因此Super& ref = mySub时，ref会调用父类方法而非子类方法
branch：虚情况下，使用虚表（vtable）的特定内存区域调用正确的实现.
每个类有一张虚表，这种类的每个实例对象都包含指向虚表的指针.
虚表包含了指向虚方法实现的指针.（父类无虚方法，则没有虚表。子类重写父类虚方法，虚表中存储子类虚方法。子类未重写父类虚方法，则虚表中存储父类虚方法）
当对象调用方法时，实例对象的指针也进入虚表，然后再根据实际的对象类型执行正确版本的方法.
因此虚方法重写，Super& ref = mySub，ref会调用子类方法而非父类

virtual的缺点：程序执行额外操作，对指针解除引用以执行代码，增加开销。指正会占用一点内存

建议：性能影响实际较小，建议所有方法声明为virtual，除了类标记为final的情况。创建对象时，会明确指定类，因此构造函数不能加virtual

### 运行时类型工具(run time type information)

作用：运行时判断对象所属类
- dynamic_cast，可在OO层次结构中进行安全的类型转换
- typeid运算符，`#include <typeifo>`,可在运行时查询对象，判断对象类型`ClsName& inst;typeid(inst) == typeid(ClsName2&)`，但通常应用虚方法提前处理类型。通常typeid的作用只在于日志和调试

exp：typeid的使用

	#include <typeinfo>
	void logObj(const Loggable& inLoggableObj)
	{
		logfile << typeid(inLoggableObj).name() << " ";
		logfile << inLoggableObj.getLogMessage() << endl;
	}

### 非public继承

protected Super：父类所有public方法和数据成员变为protected。
private Super：父类所有public，protected方法和数据成员变为private。

作用：降低父类的访问级别（更难被访问）

### 虚基类：比纯抽象类更好

作用：被共享的父类依然拥有自己的功能实现，且可在类层次结构中避免歧义

定义：Sub，Super，GrandSuper继承关系中，GrandSuper类中可以没有纯虚方法，而是在被Super继承时加上virtual，Sub类继承不变，此时GrandSuper类被称为虚基类。Super中可以不重写方法而不会歧义。

形式：`class Super: public virtual GrandSuper`













## 难点复习

### 引用

指针转换为引用：

```C++
void swap(int& first, int& second){}
int x = 5, y = 6;
int *xp = &x, *yp = &y;
swap(*xp, *yp);
```

按引用传递值:
	- 效率：只传递对象或结构的指针
	- 正确性：并非所有对象都允许按值传递，也可能不支持深度赋值。

引用作为返回值：
	- 若变量在函数结束时会被销毁，则绝不能反悔这个变量的引用

ref vs pointer

- 更加清晰
- 安全，不存在无效引用，不需要显示的解除引用

必须使用指针：

- 需要改变所指地址（改变所指对象），如动态分配内存时（尽量避免动态分配数组，而是使用vector）
- 可选参数，指针参数可定义为带默认值nullptr的可选参数
- 接受变量的代码负责释放相关对象的内存，使用指针，是传递拥有权的推荐方式



左值：是可以获取其地址的一个量，如命名的变量

右值：不是左值，剩下都是右值，如常量、临时对象

右值引用（&&）：临时对象被当做左值，因而能被引用（复制指针而不再复制大量值）。作用：用作函数的参数。

临时对象：指临时创建出来的未命名对象（包括字面量值本身），而非已然存在的变量

	void incr(int& value){
		cout << "src" << endl;
		++value;
	}
	void incr(int&& value){
		cout << "rhs" << endl;
		++value;
	}
	int &&d = 31;  // d即为右值引用，在此处与ab等普通变量并无不同
	int a=10, b=30;
	incr(a);  // call src
	incr(a+b);  // a先与b相加获得40，再将40作为参数传给int&& value，call rhs
	incr(12);  // call rhs

	Cell &&d = 

形式：`typeName&& varName = rhs;`

左值转换为右值：
std::move(varName)

const Vs static

const保护变量不被修改，替换#define来定义常量

### 非局部变量的初始化顺序

> 程序中所有的全局变量和类的静态数据成员都会在main()开始前初始化，且按一个源文件中出现的顺序初始化

问题：非局部变量在不同源文件中初始化顺序未规范，其销毁顺序因此也不确定

结果：在多个文件全局中变量相互依赖时，或全局对象的构造函数访问另一个全局对象，会导致错误

## 类型和类型转换

### typedef

作用：

1. 为`已有类型声明`提供一个新名称。
2. 命名一个函数指针类型

NOTE：函数本身没有别名，也不能被赋值，不能使用typedef。

1.新名称形式：typdef originalType newType;

exp: typedef int* intPtr; typedef std::vector<std::string> StrVector;

2.函数指针类型形式： rtType (\*)(parType par)  // \*旁边的括号不可省略，reType和parType需与原函数相同

exp: 存在多个指向某一函数的指针有用

	void oldName(int a){cout << a;}  // 原函数

	// 不用typedef，noTypePtr为函数指针类型void (*)(int a)的变量

	void (*noTypePtr)(int a) = &oldName;
	void (*noTypePtr2)(int a) = &oldName;

	// 使用typedef，将void (*)(int a)类型命名为FuncPtrType
	typedef void (*FuncPtrType)(int a)
	FuncPtrType typedPtr = &oldName;
	FuncPtrType typedPtrr2 = &oldName;


> C++中函数指针通常被virtual关键字代替

exp:动态链接库获取函数指针

	// 运行时加载的库，由LoadLibrary()核心调用完成
	HMODULE lib = ::LoadLibrary(_T("library name"));
	// 函数MyFunc在库中，从库中加载函数前，要知道函数原型
	int __stdcall MyFunc(bool b, int n, const char* p);
	
	// 定义一个缩写名称MyFuncProc
	typedef int (__stdcall *MyFuncProc)(bool b, int n,const char* p);
	MyFuncProc ptr = :: GetProcAddress(lib, "MyFunc");  // 获取MyFunc函数所在的地址
	// 等价于int (__stdcall *ptr)(bool b, int n,const char* p) = :: GetProcAddress(lib, "MyFunc");
	ptr(true, 3, "Hello world");  // 不用写成(*Proc),函数指针现在自动解引用

### 类型别名（using）

exp:设置普通指针别名的2种方法

	typedef int* AliasName;
	using AliasName = int*;

	int* pt ==(equals to) AliasName pt


exp:设置函数指针的别名的2种方法

	- typedef int (*FuncType)(char,double);
	- using FuncType = int (*)(char,double);
	
	FuncType ptrName = AddressOfFunc;
	ptrName(params);

	int *ptrName(char,double) = AddressOfFunc;

### 类型转换

- static_cast
	- 作用：
		- 显式执行受支持的转换,如int和double的转换
		- 在继承层次结构中执行向下转换，适用于指针和引用
	- 缺点：不执行运行期间的类型检测
- dynamic_cast
	- 为继承层次结构内的类型转换提供运行时检测
	- **NOTE:**运行时类型信息存储在对象的虚表中，至少有一个虚方法才能使用dynamic_cast
- const_cast
	- 作用：将常量转化为非常量，舍弃常量特性
	- 使用场景：（extern 使用第三方库的函数），一个函数需要const变量，但函数体内的（第三方）函数需要非const变量作为参数，需确保第三方函数不修改对象，否则必须重新建构程序
- reinterpret_cast
	- 作用：执行一些在技术上不被C++类型规则允许，但在某些情况下程序员需要的类型转换
	- 使用场景：将引用、指针类型转换为其他引用、指针类型，通常是void*
	- 缺点：更加自由也更不安全

### 作用域

全局作用域没有名称，直接使用`::`。特定作用域使用`scopeName::`。

规则：先解析局部作用域，再解析类作用域













## C++14新特性

### {}统一初始化(uniform initialization)

形式： `int c = {10};` 或 `int c{10};`  // int c{};则初始化为0

作用：

1.自动初始化

2.使用`{字面量}`可避免窄化（自动类型转换） 

	void func(int num){ cout << num << endl;}
	func(3.14)  // num窄化为3
	func({3.14})  // 不会窄化为int类型

3.直接初始化动态分配的数组

	int* ar = new int[4]{1,3,4,6};  // 必须在[]设置数量

4.ctor初始化器中初始化类成员数组。

Cls::Cls():ar{2,4,5} {body;}

### 初始化列表

作用：简化参数数量可变函数的编写

	#include <initializer_list>
	using namespace std;
	int makeSum(initializer_list<int> lst)
	{
		int total = 0;
		for (const auto& value : lst) {
			total += value;
		}
		return total;
	}

	int a = makeSum({1,2,3})

exp:类中的operator int()将类隐式转换为int类型

	class IntWrapper
	{
		public:
			IntWrapper(int i) : mInt(i) {}
			operator int() const { return 3;} // 添加explicit避免隐式转换
		private:
			int mInt;
	};
	
	IntWrapper el(12);
	int i = el; // 类隐式转换为int类型
	// int i = static_cast<int>(el); 添加explicit后需显示调用

### 特性

作用：源代码中添加可选信息或供应商指定的信息

形式：同static，放在函数声明的最前面

- C++11前，————attribute__,__deslspec等.
- C++11,有2个标准特性
	- [[noreturn]],函数永远不会讲控制交还给调用点。使用场景：函数导致某种中止或抛出异常。
	- [[carries_dependency]],不讨论
- C++14,添加了[[deprecated("optional reason to deprecate it")]]，把某个对象标记为废弃，可使用但不推荐.
- 供应商指定的扩展，可取任何名字，但为避免多个供应商冲突，最好限定它。[[supplierName::anyAttr]]

### 字面量（literal）

标准字面量：

'a':字符
"char array":以\0结尾的字符数组
3.14f:浮点数
0xabc: 16进制数

用户自定义字面量：以`_`开头，并通过编写字面量运算符(literal operators)`operator""`来实现

字面量运算符的形式： `rtType operator"" _userDefinedLiteral(type param){ return returnType(param);}`

- 生模式，熟模式用法相同
- 生模式（raw）：字面量12.4,被raw literal operators当做多个字符，'1','2','.','4'
- 熟模式（cooked）：字面量12.4,被cooked literal operators当做浮点数12.4
	- 有unsigned long long,long double,char,wchar_t,char16_t,char32_t类型的参数处理值
	- 有2个参数，第1个是字符数组，第2个是字符数组的长度，用来处理字符串。(const char* str,size_t len)

exp:熟模式，更加简单

	std::complex<double> operator"" _i(long double d){
		return std::complex<double>(0,d);}
	
	std::string operator"" _s(const char* str,size_t len){
		return std::string(str,len);}
	
	std::complex<double> c1 = 3.14_i;
	auto c2 = 1.23_i;
	
	std::string str2 = "Hello World"_s;
	auto str2 = "Hello World"_s;  // 自动推导为std::string
	auto str3 =  "Hello World;  // 自动推导为const char*

exp:生模式，用于regex

	std::complex<double> operator"" _i(const char* pt){
		// 将字面量当做多个字符处理，并转化为std::complex<double>类型
		ommited}
	std::complex<double> c1 = 3.14_i;
	auto c2 = 1.23_i;

### 头文件

作用：为子系统或代码段提供抽象接口。

注意：避免循环引用，避免多次包含同一头文件

解决1：使用ifndef,称为包含文件保护（include guards）

	#ifndef LOGGER_H
	#define LOGGER_H
	
	#include "something.h"
	class SomeClass{code ommited};
	code ommited
	
	#endif

解决2：使用#pragma once

解决3：
将包含头文件改为使用前置声明,`#include "ForwardDeclare4.h"`改为`class ForwardDeclare4;`
优点：编译器只知道在链接后存在这个已命名的类，可减少编译和重编译时间，因为它破坏了一个头文件对另一个头文件的依赖。

### 源于C的工具

1.变长参数列表：不安全

exp:

	#include <cstdio>
	#include <cstdarg>
	bool debug = false;
	void defbugErr(const char* str, ...)
	{
		va_list ap;
		if (debug) {
			va_start(ap,str);  // 第二个参数必须是参数列表最右边的已命名变量
			vfprintf(stderr,str,ap);
			va_end(ap);
		}
	}
	debug = true;
	debugErr("string %s and int %d\n", "Hello", 5);

2.define(预处理器宏)：类似内联函数，但不执行类型检测

#define SHOW(ss) std::cout << #ss << ": " << (ss) << std::endl

define中#ss会当做字符串"ss",cout中(ss)会获得ss中的值

机制：调用宏时，预处理器自动用扩展式替换。

缺点：

- 预处理器并不会真正应用函数调用语义
- 其参数若是一个复杂函数调用，由于其仅是扩展，可能会导致多次调用这个复杂函数
- 调试问题，编写的代码并非编译器看到的，或者调试工具中显示的代码（因为预处理器的查找和替换功能）

exp:缺点

	#define Square(x) (x * x)
	int sq(int elem){ return elem*elem};
	cout << Square(2+3);  // 不会进行理想的解析，获得11而非25

	cout << Square(ComplexCalcu()); // == cout << ((ComplexCalcu())* (ComplexCalcu()));  // 由于只是扩展，若参数是一个复杂的函数，会调用此参数2次
	cout << Sq(ComplexCalcu()); // == elem = ComplexCalcu(); cout << (elem * elem);  // 而普通函数会先计算参数的值，然后进行后续计算，只调用1次
	

解决：使用内联函数替换宏













## 模板（泛型编程）

概念：不仅参数化值，还允许参数化类型，不依赖特定值和特定值类型

### 类模板

作用：主要用于容器，或保存对象的数据结构


形式： template <typename T>; T elem  = SomeInstance;

拷贝构造函数和赋值运算符，需使用`const Grid<T>& inst`，是Grid类模板对某个类型实例化的结果。
表示Grid对象的类型作为方法的传入参数或返回值时，必须使用`Grid<T>`

NOTE:编译器会自动将Grid解释为Grid<T>,但最好显式声明。只有构造函数，析构函数使用Grid即可

定义时,::前的类名为Grid<T>

exp:创建类模板

class Grid{

};


exp:模板实例化.形式：`Grid<typeName>`

	Grid<int> myIntGrid;
	Grid<double> doubleGrid(11,11);
	Grid<vector<int> > gridVectors; // >>间加空格，避免歧义

原理：

- 编译器遇到模板方法定义时，值进行语法检查，不编译模板
- 编译器遇到模板实例时，将类定义中的T换为int，生成一个int版本的Grid类
- 编译器总为所有虚方法生成代码，为被调用（而非所有）非虚方法生成代码。（因此，即使方法不支持模板类型的操作，但不调用不会出错）
- 因此编译器必须同时访问模板类定义和方法定义
	- 将模板定义放在头文件，同类定义放一起，或类定义完成后，再#include包含模板方法的头文件
	- 类定义完成后，再#include包含模板方法的源文件
	- 限制模板类可实例化的类型
		1. 类定义完成
		1. 包含模板方法的源文件开头#include类定义、
		1. 源文件末尾添加template class Grid<double>; // 现在Grid只能实例化double类型

### 模板参数

形式:`templat <typename T, size_t WIDTH, size_t HEIGHT， otherType param>`

非类型的模板参数：只能是整形（char，int，long），枚举，指针，引用

限制：
WIDTH，HEIGHT只能是常量（右值）
只要有一个参数不同就是不同的类型，如WIDTH值为10和11是2个**不同的类**，且无继承关系

类型参数默认值：在类定义前声明默认值后，不需要再在方法前写默认值

形式:`template <typename T = int, size_t WIDTH = 10, size_t HEIGHT = 10， otherType param = ?>`,末尾没有`;`

### 方法模板（双重模板化）

起因：创建2个不同模板类（参数不同）对象后，2者的赋值运算符和拷贝构造函数并不通用

作用：使用方法模板，构建通用的赋值运算符和拷贝构造函数，达成2个不同的类转换

使用方法模板前:

	template <typenam T>
	Grid<T>::Grid(const Grid<T>& src){};	
	Grid<T>& Grid<T>::operator=(const Grid<T>& rhs){}; 
	
	Grid<double> inst;
	Grid<int> inst2;
	// 实例化并调用拷贝构造函数时
	Grid<double> inst(inst2);
	// 实际生成了Grid<double>::Grid(const Grid<double>& src){};
	// 此时Grid<double> != Grid<int>类，报错
	
	void copyFrom(const Grid<E>& src);
	template <typenam E> // 若类中有赋值运算符和拷贝构造函数，需在它们前面都声明一次E
	Grid<T>& Grid<T>::operator=(const Grid<E>& rhs)
	{
		// 不用检查自赋值，因为若E和T是同一类型不会调用此赋值运算符，而是调用默认的赋值运算符
		// 因此调用此赋值运算符永远不会指向自身
		copyFrom(rhs);
		return *this;
	};

NOTE:Grid<T>与Grid<E>并非同一类型，Grid<E>只能访问公共方法





TODO： pg.282













## I/O stream

流：是一种程序与目标设备之间输入、输出数据的机制，除了数据之外，还涉及读写的位置。流在`输出`时自动将程序可识别的类型的数据（如变量）转换为目标设备可识别的类型的数据，`输入`时做相反操作。

> C++中，流面向对象，能很好地处理错误，灵活处理自定义数据类型

> 输入、输出流定义在 iostream 头文件中

> - in,从目标设备输入到程序。
> - out，从程序输出到目标设备
> 目标设备包括控制台，文件，字符串等

cout(console out)：是写入到控制台的内建流, 控制台被称为标准输出

endl:endl会刷新缓存，但过多的缓存区刷新会降低性能，可用`\n`替换就不会刷新缓存

`<<`：是运算符，返回一个流的引用，因此可立即对同一个流再次应用`<<`

	cout << "first" << "second" << endl << "another";
	// 等价于
	cout.operator<<("first".operator<<("second".operator<<(endl.operator<<("another"))));

NOTE: `<<` 输出，变量/字面常量指向流，`>>` 输入，流指向变量

flush()，以下情况,流会自动刷新缓存

- 到达某个标记，如endl
- 流立在作用域被析构
- 要求从对应的输入流输入数据时（要求从cin输入时，cout会刷新）
- 流缓存满时
- 显示要求流刷新缓存时

### 错误处理

cout.good(); // 判断流是否正常
cout.flush(); 
cout.fail(); // flush后，需判断流是否仍然可用

捕捉异常

	cout.exceptions(ios::failbit | ios::badbit | ios::eofbit);
	try {
		cout << "success" << endl;
	} catch (const ios_base::failure& ex) {
		cerr << "caught:" << ex.what() << "errCode:" << ex.code() << endl;
	}

cout.clear(); // 重置流的错误状态

#### manipulator(操作算子)

定义：是能够修改流行为的对象，而不是流操作的数据，对后续输出到流中的内容有些，直到重置操作算子为止，作用类似于`printf("someString %s %d" , VarString2, 13)`

操作算子包括：endl，boolalpha,hex,setw,put_time,put_money等

endl封装了数据和行为，即要求流输出一个行结束序列，并刷新缓存。

### cin

	string userInput;
	int num;
	cin >> userInput >> num;  // 若输入 hello world，则只有hello被存储在变量中

get()：获取一个（字符）数据

	string readName(istream& inStream)
	{
		string name;
		char next;
		while (inStream.get(next)) {
			name += next;
		}
		return name;
	}

unget():将数据塞回滑槽，流回退一个位置

	cin >> noskipws  // 读入空白字符作为标记
	char ch
	while (cin >> ch) {  // 此时每次读取1个字符，
		if (isdigit(ch)) {
			ci.unget();
			if (cin.fail()) {
				cout << "unget failed" << endl;
			}
		}
	}

#### 错误检测

while (cin) {}  // 读取数据后就检测状态，以从异常输入中恢复
while (cin >> ch){}  // 检测时输入数据

cin.good();  // 每次`cin>>`读取数据后，就应当就检测状态cin.good()
cin.bad(),cin.fail(),cin.eof()  // endOfFile

##### 字符串流

作用：构建文本数据，但可选择不将文件输出到控制台或文件，而是显示在GUI元素中

	#include <sstream>
	ostringstream out;
	string tok;
	cin >> tok;
	string tok2;
	cin >> tok2;
	out << tok << tok2 << "\t";
	
	cout << out.str();

### 文件流

> 输出流中的内容，需要经过flush才会被写入文件，seekp、tellp会flush其之前的流并写入文件

主要区别：文件流的构造函数可以接受文件名以及打开文件的模式作为参数。

默认模式：ios_base::out(写文件),会先清空文件内容，直到下次打开文件前不会再清空

其他模式：ios_base::app(指append，每次写入前，移动到文件末尾),ios_base::in(仅读取，不修改)

	#include <fstream> // 析构函数自动关闭底层文件，不需显式调用close()
	
	int main(int argc, char* argv[])
	{
		ofstream outFile("./test.txt", ios_base::trunc);
		if (!outFile.good()) {
			cerr << "err" << endl;
			return -1;
		}
		outFile << "now add " << argc << " arguments to this." << endl;
		for (int i = 0; i <argc; i++) {
			outFile << argv[ i] << endl;
		}
		return 0;
	}

seek(ios_base::beg|end|cur)
seekg()  // 流输入，记住读取位置
seekp()  // 流输出，记住写位置

// 参数为要移动的位置数和起始点
outStream.seekp(-4,ios_base::beg);
ios_base::streampos curPos = inStream.tellg();
if (ios_base::be CurPos)

exp:
	// ofstream fout;
	// fout.open("test.txt"); 先声明，再调用open，或如下直接打开
	ofstream fout("test.txt");
	if (!fout) {
		cerr << "can't open test.txt" << endl;
		return 1; 
	}
	fout << "12345";
	// tellp()会先导致fout流刷新并输出至文件
	ios_base::streampos curPos = fout.tellp();
	if (5 == curPos) {
		cout << "curPos is 5" << endl;
	} else {
		cout << "curPos is not 5" << endl;
	}
	fout.seekp(2, ios_base::beg);
	fout << 0;
	// fout.close()显式关闭
	
	// fin会先强制刷新fout，再读取文件输入流
	ifstream fin("test.txt");
	if (!fin) {
		cerr << "error opening test.txt for reading" << endl;
		return 1;
	}
	// 文件数据通过流输入至程序的变量testVal
	int testVal;
	fin >> testVal;
	const int expected = 12045;
	if (testVal == expected) {
		cout << "value is right" << endl;
	} else {
		cout << "failed" << endl;

#### 流的连接

输入输出流建立连接后，可实现访问时刷新，通常用于文件流
形式：inFile.tie(&outFile);  // inFile.tie(nullptr);解除连接

ifstream inFlie("input.txt");
ofstream outFlie("out.txt");
inFile.tie(&outFile);
outFile << "hellp";
string nextToken;
inFile >> nextToken;

#### 双向IO

iostream是istream，ostream的子类，多重继承，同时拥有读取和写入的能力

通常先读取，再以append模式，通过`seekp(tellg())`跳转到适当的位置进行修改

















## 异常处理

遇到错误的代码抛出异常，处理异常的代码捕获异常，程序停止向下执行并转向异常处理程序（exception handler）。若无处理异常的代码则程序中止。

throw：是抛出异常的唯一方法，在一些库的深处（包括C++运行时）发生。
try/catch：是处理异常的结构，捕捉throw的异常类型

运行过程：
- 若所有的catch异常类型都与实际异常不匹配，则会自动调用terminate()中止程序。
- 若catch到异常类型匹配且无return，则catch语句完成后会继续向下执行

exp: 常见异常类型

	} catch {...) { // 用三个点匹配所有异常

	throw runtime_error("deco error");
	} catch {const exception& e) {  // runtime_error继承exception类
		cerr << e.what() << endl;
	}
	
	throw invalid_argument("wrong arguments");
	} catch {const invalid_argument& e) {
	
	throw 5;
	} catch {int e) {
	
	throw "fail open";
	} catch {const char* e) {

建议将对象作为异常抛出：

- 对象的类名称可以传递信息
- 对象可存储信息，包括描述异常的字符串

当程序遇到未捕获的异常时，会调用内建的terminate()函数，这个函数调用 cstdlib 中的abort()来中止程序。可调用set_terminate()函数（返回值为旧的terminate_handler）设置新的terminate_handler,此函数采用指向`回调函数`（无参数，无返回值）的指针做参数

exp:中止未捕获的异常前输出有效信息

	void myTerminate()
	{
		cout << "some more info" << endl;
		exit(1);  // 使用exit中止程序
	}
	// 将terminate_handler指向新handler函数myTerminate，并保存旧handler
	// void (*prevTerminate)() = set_terminate(myTerminate); 2者皆可
	terminate_handler prevTerminate = set_terminate(myTerminate);

	
	try {
		main(argc,argv);
	} catch (...) {
		if (terminate_handler != nullptr) {
			// 有handler则用terminate_handler函数中止程序
			terminate_handler();
		} else {
			terminate();
		}
	}
	set_terminate(prevTerminater); // 需要myTerminate处理异常的代码段结束后将terminate_handler设为prevTerminater
	someOtherCode；
	
#### throw list：抛出列表

形式：rtType func(args) throw(exception1,exception2,...) { body; }

标记为noexcept的函数抛出异常时，C++调用terminate()中止程序。
函数抛出不再抛出列表中的异常时，C++调用unexpected(),内建的unexpected()调用terminate()

exp: C++11后已被废弃,throw()替换为noexcept(C++14也在继续使用)则不会抛出异常

	void readFile(const string& fileName) throw(runtime_error, invalid_argument)
	{	
		ifstream ins(fileName);
		string content;
		ins >> content;
		cout << "readFile: " << content;
		throw 5; // 内部依然可以抛出其他类型的异常
	};
	unexpected_handler old_handler = set_unexpected(myUnexpected);
	try {} catch() {}
	set_unexpected(old_handler);

### 自定义异常类

exp: 自定义异常类eA及其派生异常类eB,eC，由于virtual函数，catch异常类eA的引用，即可自动显示异常由eB还是eC引起。

	class FileError : public exception
	{
	public:
		FileError(const string& fileIn) : mFile(fileIn){}
		virtual const char* what() const noexcept override { return mMsg.c_str(); }
		const string& getFileName() { return mFile; }
	protected:
		void setMessage(const string& message) { mMsg = message; }
	private:
		string mFile, mMsg;
	};
	
	// 派生类初始化mFile, mMsg，
	class FileOpenError : public FileError
	{
	public:
		FileOpenError(const string& fileNameIn);
	};
	FileOpenError::FileOpenError(const string& fileNameIn) : FileError(fileNameIn)
	{
		setMessage("Unable to open " + fileNameIn);
	}
	
	class FileReadError : public FileError
	{
	public:
		FileReadError(const string& fileNameIn, int linNum);
		int getLineNum() { return mLineNum;}
	private:
		int mLineNum;
	}
	FileReadError::FileReadError(const string& fileNameIn, int linNum)
	: FileError(fileNameIn), mLineNum(linNum)
	{
		ostringstream ostr;
		ostr << "error reading " << fileNameIn << " at line " << LineNum;
		setMessage(ostr.str());
	}
	
	void readIntegerFile(const string& fileName, vector<int>& dest)
	{
		ifstream istr;
		int temp;
		string line;
		int lineNumber = 0;
		istr.open(fileName.c_str());
		if (istr.fail()) {
			throw FileOpenError(fileName);
		}
		while (!istr.eof()) {
			getline(istr,line);
			lineNumber++;
			istringstream lineStream(line);
			while (lineStream >> temp) {
				dest.push_back(temp);
			}
			if (!lineStream.eof()) {
				throw FileReadError(fileName, lineNumber);
			}
		}
	}
	
	int main(){
	
		try {
			readIntegerFile(fileName, myInts);
		} catch (const FileError& e) {
			// readIntegerFile的异常会调用派生类的what()
			cerr << e.what() << endl;
			return 1;
		}
	
		return 0;
	}

#### nested exception(嵌套异常)

作用：避免抛出第二个异常时，丢失正在处理的第一个异常的信息

形式： `throw_with_nested()` 代替 `throw`，使用dynamic_cast访问嵌套的异常，如颞部没有嵌套异常，结果为空指针，如有嵌套异常，调用nested_exception的rethrow_nested()方法

嵌套异常处理过程:

1. throw_exp1
1. caught_by_inner_func
1. nested_throw_epx2，此时exp1被嵌套在exp2中，2个异常同时存在
1. caught_by_outer_func
1. deal_epx2
1. check_nest
1. deal_epx1

exp: 处理过程实例

	#include <string>
	#include <exception>
	
	using namespace std;
	
	class MyException :public exception
	{
	public:
		MyException(const char* st):mMsg(st){}
		virtual const char* what() const noexcept override
		{
			return mMsg.c_str();
		}
	private:
		string mMsg;
	};
	
	void doSome()
	{
		try {
			throw std::runtime_error("runtime_error happened");
		} catch (const std::runtime_error& e) {
			std::cout << "func " << __func__ << " caught error: " << e.what() << endl;
			std::throw_with_nested(MyException("MyException with runtime_error nested"));
		}
	}
	int main(){
	
		try {
			doSome();
		} catch (const MyException& e) {
			std::cout <<  "func " << __func__ << " caught an error: " << e.what() << endl;
			
			
			// branch:检测嵌套异常方法1
			const std::nested_exception* pNested =
			dynamic_cast<const std::nested_exception*>(&e);
			if (pNested) {
				try {
					pNested->rethrow_nested();
				} catch (const std::runtime_error& e) {
					std::cout << "func " << __func__ << " caught an nested error: " << e.what() << endl;
				}
			}
	
			// branch:检测嵌套异常方法2,使用std::rethrow_if_nested(e)，推荐
			try {
				std::rethrow_if_nested(e);
			} catch (const std::runtime_error& e) {
				std::cout << "func " << __func__ << " caught an nested error: " << e.what() << endl;
			}
	
		}
		
		return 0;
	}

1. doSome抛出runtime_error异常，被catch捕捉到
1. doSome的catch中又抛出MyException异常
2. 此时第一个异常runtime_error，被嵌套在第二个异常MyException中
1. MyException异常被main中的catch捕捉到
2. 此时main中只能直接处理MyException,而不能处理doSome中的runtime_error
1. main函数想要再处理runtime_error,就要使用dynamic_cast获得嵌套异常指针，并重新抛出并捕捉runtime_error异常



#### 堆栈的释放和清理

1. 发现一个catch
1. 堆栈释放所有中间堆栈帧，直到跳到定义catch处理程序的堆栈层
2. 若非局部变量，delete ptr, istr.close()可能永远不会被执行到

stack unwinding(堆栈释放): 调用所有具有局部作用域的名称（指局部变量）的析构函数，并忽略在当前执行点之前的每个函数中的所有的代码。但不释放指针变量，不执行其他清理。

解决1：使用智能指针,推荐

解决2：为每个函数，捕获可能抛出的所有异常，执行必要的清理，并重新抛出异常，供堆栈中更高层的函数处理
	
	void funcTwo()
	{
		cout << "two" << endl;
		throw runtime_error("runtime_error here");
	}
	void funOne()
	{
		try {
			funcTwo();
		} catch (...) {
			cout << "one" << endl;
			throw invalid_argument("here");
		}
	}
	int main(){
		try {
			funOne();
		} catch (const exception& e) {
			cout << "exception caught: " << e.what() << endl;
		}
	
		return 0;
	}

以上代码的异常处理过程：

1. throw_exp1
1. caught_by_inner_func
1. throw后不加任何异常，exp2 = exp1，若有，则exp2 = anotherError，此时exp1已丢失
1. caught_by_outer_func
1. deal_epx2

### 常见错误处理

#### 内存分配错误

new,new[]默认抛出bad_alloc类型异常，在new头文件中定义。

使用情境：至少分配大块内存时需处理这种异常。`} catch (const bad_alloc& e) {`

#### callback(回调函数)

定义： 通过函数指针调用的函数（作为调用者函数的参数），在异常/错误处理中可能会被无限次调用

特性：无参数，无返回值。

3个设置回调函数的方式：set_new_handler,set_terminate(),set_unexpected

运行机制：若设置了回调函数，则出现相应错误时，不再抛出异常，而是循环调用回调函数直到不再有此异常，因此可能会出现无限循环。

exp: 内存分配时
1. 内存分配失败
1. loop:不抛出异常
1. 调用一次回调函数以尝试解决
1. 再次尝试分配内存
1. branch:若依然失败，goto loop
1. branch:若成功，则无异常，也不用再回调，得以继续向下执行代码

exp:无限循环 可以理解为有如下代码

	typedef void(*new_handler)();
	new_handler __handler__ = nullptr;  // 一个内置的全局变量__handler__
	
	new_handler set_new_handler(hand){  // set_new_handler类似如下定义
		temp = __handler__;  // 都是指针，直接复制即可
		__handler__ = hand;
		return temp;
	}
	
	// new 可以理解为中有如下代码
	{
		alloc_memory();
		while (alloc.fail()) {
			if (__handler__) {
				__handler__();
				alloc_memory(); // 再次分配内存
			} else {
				throw bad_alloc;
			}
		}
		return语句
	}
	void cb(){
    	cout << "this is callback" << endl;
	}

	int main(){
		new_handler old_handler = new_handler set_new_handler(cb);
		使用new分配内存
		set_new_handler(old_handler);
	}

运行过程：

1. 当new分配失败时，即alloc.fail()
1. branch:默认throw bad_alloc直接跳出此循环，交给catch语句
1. branch:设置了new_handler，运行__handler__();alloc_memory();只有alloc.success()才退出循环

NOTE: 若new_handler函数中没有throw语句（没有异常），其后的代码可不放在try/catch语句中

解决new（内存分配错误）的无限循环：

1. 提供更多的可用内存
	- 程序启动时分配一大块足以完好保存文档的内存，在new_handler中释放这块内存
	- 用于保存用户状态，以免丢失重要数据，如excel就有类似的机制
	- 触发时，释放内存，保存文档，重启程序，重新加载文档
2. 抛出异常
	- 抛出bad_alloc类或派生类异常
	- catch派生类后触发文档保存操作及衬砌应用程序
3. 设置不同的new_handler，在分配内存失败时再设置一个不同的new_handler。不推荐。
4. 终止程序（记录异常，中止异常部分的运行，但整个程序得以继续执行）
	- 记录错误信息，并抛出约定好的异常
	- 顶层函数(如main())中捕获这个异常,并从顶层函数返回进行处理
	- 不显式使用exit(),abort()，而是从顶层函数返回
	- 如此内存分配失败，程序也能继续运行

1.nothrow不抛出异常,出错时返回一个nullptr;
`ptr = new(nothrow) int[nums];`

2.自行构造内存异常处理函数

	class MyHeapError: public bad_alloc {};
	void deal(){
		cerr << "alloc error" << endl;
		throw MyHeapError("my heap");
	}
	try{
		new_handler old_handler = set_new_handler(deal);
		
		int* ptr = new int[numInts];
		
		set_new_handler(old_handler);
	} catch (const MyHeapError& e) {
		cerr << __FILE__ << "(" << __LINE__ << ")" << endl;
		return 1;
	}

#### 构造函数的错误

问题：由于构造函数没有返回值，因此异常出现前，标准的错误处理机制无法运行

解决：构造函数抛出异常，如此就能确定是否成功创建对象。

新问题：如果异常离开了构造函数，对象的析构函数无法被调用

解决：catch(...)语句捕捉所有异常，并在其中析构对象，然后再抛出bad_alloc异常

	#include <cstddef>
	
	class Element
	{
	private:
		int mValue;
	};
	
	class Matrix
	{
	public:
		Matrix(size_t width, size_t height);
		virtual ~Matrix();
	private:
		size_t mWidth;
		size_t mHeight;
		Element** mMatrix;
	};
	
	Matrix::Matrix(size_t width, size_t height)
		:mWidth(width), mHeight(height), mMatrix(nullptr)
	{
		mMatrix = new Element*[width];  // 为空对象，此行出问题不析构也没事
		size_t i = 0;
		
		try{
			for (i = 0; i < width; ++i) {
				mMatrix[ i] = new Element[ height];
			}
		} catch (...) {
			cout << "caught exception" << endl;
			for (size_t j = 0; j < i; j++) {
				delete [] mMatrix[ j];
			}
			delete [] mMatrix;
			mMatrix = nullptr;
			throw bad_alloc();
		}
	}
	
	Matrix::~Matrix()
	{
		for (size_t i = 0; i < mWidth; ++i)
			delete [] mMatrix[ i];
		delete [] mMatrix;
		mMatrix = nullptr;
	}

#### function-try-blocks

可用于普通和构造函数，可在ctor-initializer中抛出异常

形式：用于构造函数时（:<ctor-initializer>跟在try之后）

	MyClass::MyClass()
	try: <ctor-initializer>
	{
		// init-body;
	} catch (const exception& e) {
		// body;
		throw err;  // 供外界的调用代码捕捉
	}

运行过程:
1. <ctor-initializer>由3部分组成{A,B,C}
2. 若{B}出现了异常
2. 异常部分之前的<ctor-initializer>为{A}，已运行
3. {A}中的对象数据成员被构建
4. {A}中的非对象数据成员被初始化
2. 异常部分之后的<ctor-initializer>为{C}，未运行
3. {C}中的所有数据成员都不初始化
4. 构造体的语句都不会被执行
1. 执行catch前:
2. {A}已构建的对象数据成员都会销毁（调用其自身的析构函数）
1. {A}已构建的非对象数据成员不会被销毁，如裸指针
2. 因此catch中尽量不要调用对象数据成员，但非对象数据成员需要在catch中主动释放资源
 

作用：
将<ctor-initializer>的异常转化为其他异常
将信息记录到日志文件
释放在抛出异常前就在<ctor-initializer>中分配了内存的裸资源。

#### 析构函数的错误

说明：必须在析构函数内部处理析构函数引起的错误，不应让析构函数抛出任何异常

不抛出异常的原因
- 堆栈释放过程中析构函数抛出异常，C++运行库会调用std::terminate()，并终止应用程序
- 客户该如何？客户不会显式调用析构函数
- 析构函数是释放对象使用的内存和资源的一个机会，异常退出，可能永远无法再释放内存

TODO:Pg.346

## 运算符重载

作用：
- 自定义类可以具有（接近）内建类型（如int，double，甚至数组，指针，函数）的类似行为
- 获得对程序行为更大的控制权，例如对自定义类重载内存分配和内存释放历程，以控制新对象的内存分配和回收
- 为类的客户提供方便

运算符重载限制：
- 不修改成员变量的运算符用const修饰
- 不能添加新运算符
- 无法重载：`.`,`::`,`sizeof`,`?:`等
- arity为运算符关联的参数或操作数的数量。只能修改函数调用，new，delete的arity。对[]重载产生限制
- 不修改运算符优先级
- 不能对内建类型重定义运算符。运算符必须是类中的一个方法，或者全局重载运算符函数中至少有一个参数必须是一个用户定义的类型（如一个类）。除了内存分配和释放例程，可替换程序中所有内存分配使用的全局例程
- `operator&`不建议重载，否则会异常地修改基础语言行为（获取变量地址），以及`operator&&`，`operator||`不建议重载，否则会使**C++短路求值规则**失效，不建议重载`operator,`

#### 重载为类的方法还是全局函数（通常是类的友元）

- 必须为方法：在类外无意义，如operator=(作为左值修改的返回值，会对成员进行修改，必须是非const，如=，+=，-=）
- 必须为全局函数：允许运算符左侧变量是自定义类之外的任何类，例如[operator>>,operator<<](#-and-)，左侧为iostream对象
- 两者皆可：建议设为方法，方法可是virtual，而友元函数不能

参考重载运算符表：Pg.355

#### 关系运算符 ???

utility头文件中，命名空间std::rel_ops包含operator!=,>,<=,>=的模板。在类中实现operator==,<，就会自动获得这些模板运算符

++i（前缀递增），变量+1，然后返回新值
i++（后缀递增），变量+1，但返回旧值

Cls& operator++();  // 前缀递增
Cls operator++(parType);  // 后缀递增,传入int参数类型，无实际参数，以与前缀递增operator++区分

	// 可返回引用
	Sheet& operator++(){
		set(mValue + 1);
		return *this;
	}
	// 需创建1个临时对象保存原有数据，并返回此临时对象（是本地变量，不能被引用）
	Sheet operator++(int){
		Sheet temp(*this);  // 调用拷贝构造函数
		set(mValue + 1);
		return temp;
	}

++i Vs i++

- 若变量i的类型为类
	- ++i只需修改对象本身的一个元素，返回引用。消耗较少
	- i++需创建临时对象，默认需复制所有元素，返回临时对象。消耗较多
- 若变量i的类型为int，字面常量+1计算结果先保存在寄存器R中
	- ++i，直接修改&i处的值为R值
	- i++开辟临时新空间，用R值对此空间初始化，再使用移动语义，传递给&i。理论上开辟新空间会消耗较多

#### >>and<<

>>,<<左侧为stream类，但不能向stream类添加方法，因此只能在右侧类的<<和>>函数改为stream类的全局友元函数（friend）

	#include <iostream>
	#include <string>
	using namespace std;
	
	class RhsClass{
	public:
	    RhsClass(string ele):mString(ele){}
	    friend std::ostream& operator<<(std::ostream& ostr,
	        const RhsClass& rhs)
	    {
	        ostr << rhs.mString;
	        return ostr;
	    }
	    friend std::istream& operator>>(std::istream& istr,
	         RhsClass& rhs)  // >>会修改rhs对象
	    {
	        string temp;
	        istr >> temp;
	        rhs.set(temp);
	        return istr;
	    }
	    void set(string elem){
	        mString = elem;
	    }
	private:
	    string mString;
	};
	
	int main() {
		RhsClass first("beef");
		// 返回stream（流对象），cout，cin就可进行处理
		cout << first << endl;
		cin >> first;
		cout << first;
	}

NOTE：以下运算符一般不会进行全局重载，只在类中重载

#### 重载下标运算符

exp:建立一个动态分配的数组模板，但每次赋值或获取值需要用get，set，不如使用下标[i]方便

	#include <iostream>
	#include <string>
	using namespace std;
	
	template <typename T>
	class Array
	{
	public:
	    Array(){
	        mCurrentSize = kAllocSize;
	        mElems = new T[mCurrentSize];
	        initializeElements();
	    }
	    virtual ~Array(){
	        delete [] mElems;
	        mElems = nullptr;
	    }
	
	    Array<T>& operator=(const Array<T>& rhs) = delete;
	    Array(const Array<T>& src) = delete;
	
	    T getElementAt(size_t x) const{
	        if (x >= mCurrentSize){
	            throw std::out_of_range("");
	        }
	        return mElems[ x];
	    }
	
	    void setElementAt(size_t x,const T& val){
	        if (x >= mCurrentSize){
	            resize(x + kAllocSize);
	        }
	        mElems[ x] = val;
	    }

		// 通过重载下标运算符，Array<T>类也可通过下标[i]赋值，取值
		T& operator[] (size_t x){
	        if (x >= mCurrentSize){
	            resize(x + kAllocSize);
	        }
			return mElems[ x];
		}
		
	private:
	    static const size_t kAllocSize = 4;
	    void resize(size_t newSize){
	        T* oldElems = mElems;
	        size_t oldSize= mCurrentSize;
	        mCurrentSize = newSize;
	        mElems = new T[newSize];
	        initializeElements();
	        for (size_t i = 0; i < oldSize; i++){
	            mElems[ i] = oldElems[ i];
	        }
	        delete [] oldElems;
	    }
	    void initializeElements(){
	        for (size_t i = 0; i < mCurrentSize; i++){
	            mElems[ i] = T();  // 类型作为函数，并设置初始值，如int() == 0;
	        }
	    }
	    T* mElems;
	    size_t mCurrentSize;
	};

#### 重载函数调用运算符（函数对象运算符）

`operator()`，重载时，这个类的对象就可当做函数指针使用，只能重载为类的非static方法。

现在函数对象可以伪装成函数指针，函数指针类型是模板化时，就可以把函数对象当成回调函数传入需要接受函数指针的例程

与全局函数对比：
- 函数对象可在函数对象运算符重复调用之间在数据成员中保存信息
- 设置数据成员来自定义函数对象的行为，例如比较函数参数和数据成员的值
- 全局函数或静态变量也可以实现上述功能。但函数对象更简洁，且在多线程程序中不会产生问题

exp: 对象可像函数一样的形式被调用

	class FuncPtr{
	public:
		int operator()(int inParam);
		int doSquare(int inParam);
	};
	int FuncPtr::operator()(int inParam) {
		return doSquare(inParam);
	}
	int FuncPtr::doSquare(int inParam){
		return inParam * inParam;
	}
	
	int main(){
	
		int x = 3,xSquared, xSquaredAgain;
		FuncPtr sq;  // 创建类的实例sq

		// 此时调用operator()，sq(x)等同于sq.operator()(x)，虽然看上去奇怪，但编译器能正确识别
		xSquared = sq(x);
		xSquaredAgain = sq.doSquare(x);
	
		return 0;
	}

### 重载解除引用运算符

`operator*`，`operator->`：可将类对象直接当做指针使用

形式：是一元运算符，不需要传入参数，一般不重载全局的*,->

exp:一个简单智能指针类模板

	class Sheet{
	public:
		Sheet();
		Sheet(int width,int height);
		virtual ~Sheet();
		int set(int value){
			mWidth += value;
			return mWidth;
		}
	private:
		int mWidth;
		int mHeight;
	};
	Sheet::Sheet():mWidth(10),mHeight(50){};
	Sheet::Sheet(int width, int height):mWidth(width),mHeight(height){};
	Sheet::~Sheet(){};
	
	template <typename T>
	class Pointer
	{
	public:
		Pointer(T* inPtr);
		virtual  ~Pointer();
	
		T& operator*();
		const T& operator*() const;
	
		T* operator->() {return mPtr;}
		const T* operator->() const {return mPtr;}
	
		Pointer(const Pointer<T>& src) = delete;
		Pointer<T>& operator=(const Pointer<T>& rhs) = delete;
	
	private:
		T* mPtr;
	};

	template <typename T>
	Pointer<T>::Pointer(T* inPtr):mPtr(inPtr){}
	template <typename T>
	Pointer<T>::~Pointer(){delete mPtr; mPtr = nullptr;}
	
	template <typename T>
	T& Pointer<T>::operator*() {return *mPtr;}
	
	template <typename T>
	const T& Pointer<T>::operator*() const {return *mPtr;}
	
	int main(){
		Pointer<int> smartpt(new int);  // int* mPtr = new int，此时new int中的值还未初始化
		* smartpt = 10;
		Pointer<Sheet> smartClsPtr(new Sheet(15,25));
		cout << smartClsPtr.mPtr->set(20) << endl;
	
		return 0;
	}


// 编译器特殊处理：C++会对重载的operator->返回值（如mPtr）应用了另一个operator->（此->为`返回值类.operator->`，而非重载后的`Pointer.operator->()`)

1. smartClsPtr为一个Pointer<Sheet>类型的对象
1. ->需要一个指针来调用
1. 对象未重载而直接调用->就会出错
1. 需要重载Pointer<Sheet>类的operator->
2. 调用Pointer<Sheet>.operator->，获取指向所生成对象new Sheet(12,133)的指针mPtr
2. 对mPtr再应用->set(5)，调用指针类的operator->，获取对象

Pointer<Sheet> smartClsPtr(new Sheet(12,133));

`smartClsPtr->`set(5);
// 实际调用 `(smartClsPtr.operator->())->`set(5);
// 相当于调用 `(smartClsPtr.mPtr)->`set(5)


#### `.*`与`->*`：通过指针访问类成员和方法（很少使用）

`.*`与`.`一样，不要进行重载

	Sheet cel;
	double (Sheet::*pt)(int value) = &Sheet::getValue;
	cout << (cel.*pt)();
	// 此时需显式解引用pt，以免造成歧义，且用()包裹以先一步完成.*计算

`->*`相当于先进行解除对象的引用,再解除函数的引用，可被重载

	Sheet* cel = new Sheet();
	double (Sheet::*pt)(int value) = &Sheet::getValue;
	cout << (cel->*pt)();

### 转换运算符（进行类型转换）

原型：operator std::Typename() const;

exp: Sheet类转换为string类型

	Sheet::operator string() const { return mString; }
	Sheet cell(12);
	string turned = cell;

#### 歧义问题

double d2 = cell + 3.3;  // 现有2种选择因而产生歧义

1. operator double()先将cell转换为double，再执行double加法
1. double构造函数先将3.3转换为Sheet类型，再执行Sheet加法

解决：在operator double()最前加上explicit（而非在构造函数前），如此会自动选择第二种方法，再通过static_cast显式转换

double d = static_cast<double>(cell + 3.3);

#### bool转换

对类添加 operator void*()或operator bool()，将其转换为指针类型，此时可与nullptr比较

	operator void*() const {return mPtr; }
	operator bool() const {return mPtr != nullptr; }

	Sheet p;
	if (p != nullptr);
	if (p != NUll);
	if (!p);

#### 重载new，delete

在可能产生内存碎片（分配/释放大量小对象）时有用

解决方式：编写内存池分配器，以重用固定大小的内存块

NOTE: 重载全局operator new时，不要在其定义中使用new，以免进入无限循环

exp:new/delete表达式不能被重载,不能自定义构造函数/析构函数的调用

	Cell* ce = new Cell();

new表达式，共6种

- new
- new[]
- nothrow new  
- nothrow new[]
- new (ptr)
- new[] (ptr)

operator new，共6种

- 可重载的operator new：
	- void\* operator new(size_t size);
	- void\* operator new[] (size_t size);
	- void\* operator new(size_t size, const std::nothrow_t&) noexcept; // nothrow其实是nothrow_t类型的变量
	- void\* operator new[] (size_t size, const std::nothrow_t&) noexcept;
- 不可重载的operator new，作用(mechanism): **实现内存池**，以便在不释放内存的情况下重用内存
	- void\* operator new(size_t size, void* p) noexcept;
	- void\* operator new[] (size_t size, void* p) noexcept;
	- exp: 不分配新内存，而是在已有的存储段（内存）上调用构造函数，构造对象，称为placement运算符
		- void* ptr = allocateMemorySomehow;
		- Cell* ce = new (ptr) Cell();

delete表达式，共2种

- delete
- delete[]

operator delete，共6种。重载需与operator new对应

- void operator new(void* ptr) noexcept;  // 全都需要声明为noexcept以避免错误
- void operator new[] (void* ptr) noexcept;
- void operator new(void* ptr, const std::nothrow_t&) noexcept;
- void operator new[] (void* ptr, const std::nothrow_t&) noexcept;
- void operator new(void* ptr, void*) noexcept;  // 由于并不删除内存，这2个是空操作
- void operator new[] (void* ptr, void*) noexcept;

exp: 简单的重写

	void* Mem::operator new[] (size_t size, const nothrow_t&) noexcept{
		cout << " rewrite operator new in Mem" << endl;
		return ::operator new[] (size, nothrow);
	}

exp: 设置额外参数，可作为计数器，可提供文件名和行号以识别内存泄漏的代码行

	void* Mem::operator new(size_t size, int extra) {
		cout << "operator new with extra arg " << extra << endl;
		return ::oprerator new(size);
	}
	void Mem::operator delete(void* ptr, int extra) noexcept{
		// 必须重载相应的delete
		cout << "operator delete with extra arg " << extra << endl;
		return ::oprerator delete(ptr);
	}
	Mem* memp = new(6) Mem();  // 6即是int extra，同nothrow相同的形式传递
	delete memp;  // 会自动调用上边的delete(void* ptr, int extra)

exp: 为自定义类编写复杂内存分配释放方案，编写接受size_t参数的operator delete

	void operator delete(void* ptr, std::size_t size) noexcept{
		cout << "operator delete with size" << endl;
		::operator delete(ptr)  // 全局delete未重写，不接受size_t参数
	}

NOTE：类同时声明2个operator delete，一个接受size_t参数，另一个无size_t参数，则不接受size_t参数的总是被调用


































# stdTemplateSLib

> 所有标准库类和函数都在std命名空间中声明

核心：泛型容器，泛型算法

编码原则： 模板和运算符重载

头文件：list,string,regex,ios,iostream,fstream，memory,exception,stdexcept,system_error,complex,valarray,ratio,limits,chrono(时间），random，initializer_list,unity(pair和tuple,存储异构元素),functional,thread,type_traits

### stl容器（都是模板）

作用：提供常用数据结构的实现，如链表和队列

常用容器（Pg.389/410)

摊还常量时间（amortized constant time)：指大部分插入操作在O(1)内完成

顺序容器（存储类容器)：

- vector:用于快速访问元素，而非频繁在中间加减元素。
- list: 是双向链表,使用指针，不保存在连续内存中，同vector相反，用于频繁加减元素，较慢访问元素
- deque(double-ended queue)：快速访问元素，2端加减元素较快，中间慢
- array:大小固定，快速访问

容器适配器（adapter）：是建构在顺序容器上的接口

- queue：先进先出
- priority_queue(在queue头文件中）:设置元素优先级，删除元素后，对元素重新排序，类似银行排队但有vip和普通人
- stack（在stack头文件中）：后进后出。用于错误处理，以读取到最新的错误信息

关联容器，关联键与值：

- set,multiset（可理解为键本身即是值）:有顺序的集合,增删和查询复杂度都是logN
- map,multimap:有顺序的字典，保存键值对

无需关联容器/哈希表，复杂度为平均常量时间

- unordered_map  // 头文件unordered_map
- unordered_multimap
- unordered_set  // unordered_set即是unordered_hash
- unordered_multiset

bitset：位运算，大小固定，对其中的每一bit进行修改

### STL算法（Pg.391/412)

> 在algorithm头文件中

实现原理：STL分离数据（容器）和功能（算法）

泛型算法使用迭代器（iterator）作为中介对容器进行操作。不同容器的不同迭代器遵循标准接口。

### STL的缺陷

多线程访问容器，不安全
不提供泛型的树结构或图结构，，map和set通常实现为平衡二叉树，但并未在接口中公开该实现。例如编写解析器，就要自己实现。

### 容器

运行要求（mechanism）

STL容器对元素使用值语义（value semantic），输入元素时保存元素的副本，通过赋值运算符给元素赋值，析构函数销毁元素，必须保证STL的类时可复制的。请求容器中元素，返回保存的副本的引用。可自行实现引用语义（refrence semantic），保存元素指针的复制（unique_ptr，shared_ptr，如此容器才拥有此指针）而非值。

复制构造函数：插入元素
移动构造函数 noexcept：vector增加容量。  // 添加noexcept确保移动语义正确应用到STL
赋值运算符：使用源元素的副本修改元素
移动赋值运算符 noexcept：右值操作

### 迭代器

增强的智能指针，实现不同，但使用统一接口

理解为指向容器元素的指针，使用operator++移动到下一元素，使用operator*，operator->访问实际元素

公共迭代器typedef和方法：iterator和const_iterator
如vector<int>::const_iterator，使用时不用关心实际类型

特点：使用begin(),end()引用，是双向的，可与int类型相加，减，跳跃（++it;--it;it+=5)

缺点：安全性和普通指针接近，非常不安全。例如迭代器超过最后一个元素会产生错误，但迭代器本身却不执行任何验证操作。

优点（相较于索引使用size()方法遍历）：

- 可任意位置插入删除元素
- 可使用stl算法
- 顺序访问元素，比用索引单独检索每个元素效率要高，此条不适用vector

#### vector

定义：

	template <class T, class Allocator = allocator<T> >
	class vector;

exp: vector的基本使用

	class Some{
	public:
		Some():el(2.2222){icCount();cout<< "default runs as many as param " << counter << endl;}
		Some(double v):el(v){icCount();cout<< "double runs only once " << counter << endl;}
	
		static void icCount(){counter++;}
		static int counter;
		double el;
	};
	int Some::counter = 0;
	
	vector<int> iv(10,32);  // 元素数量为10，并将它们初始化为32，默认值为0
	vector<Some> sv(5);  // 创建5个Some类的实例，运行默认构造函数也要5次
	vector<Some> iv(5,4.4);  // 创建5个Some类的实例，但构造函数只运行1次,剩余的实例都对第一个实例调用拷贝构造函数，深度复制成员数据

	// 使用assign清除所有元素并重新赋值，但类型不可改
	vector<int> iv(3);
	iv.assign(5, 12);
	iv.assign({5,2,6,2});

	// 使用swap交换
	vector<int> iv(3);
	vector<int> ivtwo(5, 12);
	iv.swap(ivtwo);

	默认迭代器
	vector<double> dbVector(5, 4.4);
	// 使用const调用const_iterator
	for (const auto& elem : dbVector) {  
		elem += 1.4;
	}

	显示调用vector迭代器,变量it获取了引用dbVector第一个元素的迭代器，迭代器递增以引用下一个元素
	// vector<double>::iterator可用auto替换
	for (vector<double>::iterator it = begin(dbVector);
		it != end(dbVector);  // end返回的迭代器超过vector尾部，而不是引用最后一个元素
		++it) {
		*it += 1.4;
		// it为对象，则可调用 it->append("here") 
	}

	push_back追加元素，超出范围会自动扩展
	pop_back删除元素
	back()获取最后的元素
	insert()插入元素
	erase(it)删除特定位置的元素
	clear()删除所有元素

	vec.push_back(Element(12,"Twelve")); // 显式写法
	vec.push_back({12,"Twelve"});  // 使用{}初始化器的写法

	vec.emplace_back(12,"Twelve"); // 不用事先创建对象，而是根据传入的参数，直接开辟空间，创建对象

控制vector（超出所需内存，需申请更大的内存，重新分配内存）：

控制vector执行内存分配的时机
重分配内存会使引用vector内元素的所有迭代器实效

size():当前元素数量
capacity()：可保存的元素数量

预分配空间：分配保存一定量的元素的空间
- reserve(),
- 构造函数中resize()

#### typename

- 指定模板参数 
	- template <typename T>
- 访问给予一个或多个模板参数的类型时，必须显式指定typename
	- typename std::vector<T>::iterator mCurElem;
	- 此时模板参数T用于访问迭代器类型，显式指定typename

exp:round-robin(时间片轮转类)，在有限资源列表中分配请求（进程列表及为其分配的时间片，如100ms），轮询循环

	#include <iostream>
	#include <string>
	#include <vector>
	using namespace std;
	
	/*
	* create an iterator
	*/
	template <typename T>
	class RoundRobin{
	public:
		RoundRobin(size_t numExpected = 0);
		virtual ~RoundRobin();
		// 应当实现赋值运算符和赋值构造函数，确保mCurElem在目标对象中可用，此处省略
		RoundRobin(const RoundRobin& src) = delete;
		RoundRobin& operator=(const RoundRobin& src) = delete;
		void add(const T& elem);
		void remove(const T& elem);
		T& getNext();
	private:
		std::vector<T> mElems;
		// 由于mCurElem，这个类避免了赋值和按值传递操作
		typename std::vector<T>::iterator mCurElem;
	
	};
	
	template <typename T>
	RoundRobin<T>::RoundRobin(size_t numExpected)
	{
		mElems.reserve(numExpected);
		mCurElem = end(mElems);
	}
	template <typename T>
	void RoundRobin<T>::add(const T& elem)
	{
		int pos = (mCurElem == end(mElems)) ? -1 : mCurElem - begin(mElems);
		mElems.push_back(elem);
		mCurElem = (pos == -1 ? end(mElems) : begin(mElems) + pos);
	}
	template <typename T>
	void RoundRobin<T>::remove(const T& elem)
	{
		for (auto it = begin(mElems); it !=end(mElems); ++it){
			if (*it == elem) {
				int newPos;
				if (mCurElem <= it) {
					newPos = mCurElem - begin(mElems);
				} else {
					newPos = mCurElem - begin(mElems) -1;
				}
				mElems.erase(it);
				mCurElem = begin(mElems) + newPos;
				return;
			}
		}
	}
	template <typename T>
	T& RoundRobin<T>::getNext()
	{
		if (mElems.empty()){
			throw std::out_of_range("No elem");
		}
		if (mCurElem == end(mElems)) {
			mCurElem = begin(mElems);
		} else {
			++mCurElem;
			if (mCurElem == end(mElems)) {
				mCurElem = begin(mElems);
			}
		}
		return *mCurElem;
	}
	template <typename T>
	RoundRobin<T>::~RoundRobin(){
	
	}
	
	class Process{
	public:
		Process(const string& name) :mName(name) {}
		void workDuringTimeSlice() {
			cout << "Process " << mName << " working during time slice " << endl;
		}
		bool operator==(const Process& rhs) {
			return mName == rhs.mName;
		}
	private:
		string mName;
	};
	
	class Scheduler{
	public:
		Scheduler(const vector<Process>& processes);
		void scheduleTimeSlice();
		void removeProcess(const Process& process);
	private:
		RoundRobin<Process> rr;
	};
	Scheduler::Scheduler(const vector<Process>& processes){
		for (auto& process : processes) {
			rr.add(process);
		}
	}
	void Scheduler::scheduleTimeSlice()
	{
		try {
			rr.getNext().workDuringTimeSlice();
		} catch (const out_of_range&) {
			cerr << "no more processes to schedule." << endl;
		}
	}
	void Scheduler::removeProcess(const Process& process){
		rr.remove(process);
	}
	
	int main(){
		vector<Process> processes = { Process("1"), Process("2"),Process("3")};
		Scheduler sched(processes);
		for (int i = 0; i < 5; ++i){
			sched.scheduleTimeSlice();
		}
		sched.removeProcess(processes[1]);
		cout << "remove second" << endl;
		for (int i=0; i < 5; ++i){
			sched.scheduleTimeSlice();
		}
	
		return 0;
	}

#### vector<bool>特化，保存1 bit空间，可动态改变其大小。但建议使用bitset

定义名为reference的类，用作底层bool（或bit）的代理
调用operator[],at()等方法时，vector<bool>返回reference对象，此对象是实际bool值的代理
因此对bool的引用不能调用方法

NOTE:返回的引用实际是代理时，不能取地址

### list

> 实际不提供operator[]的随机访问操作，只有通过迭代器才能访问单个元素。
只有front(),back(),返回第一个和最后一个元素的引用而不通过迭代器

由于结构问题（由指针连接），list迭代器只能++，--，而不能+n，-n

li.splice(it, anotherLi)向li表的特定位置（通过迭代器）插入另一张li









exp:queue处理网络数据包缓冲。网络层缓存/保存数据包，超过缓存的数据包被丢弃

	#include <iostream>
	#include <queue>
	using namespace std;
	
	template <typename T>
	class PacketBuffer{
	public:
		PacketBuffer(size_t maxSize = 0);
		bool bufferPacket(const T& packet);
		T getNextPacket();
	private:
		std::queue<T> mPackets;
		size_t mMaxSize;
	};
	template <typename T>
	PacketBuffer<T>::PacketBuffer(size_t maxSize):mMaxSize(maxSize){}
	template <typename T>
	bool PacketBuffer<T>::bufferPacket(const T& packet)
	{
		if (mMaxSize > 0 && mPackets.size() == mMaxSize) {
			return false;
		}
		mPackets.push(packet);
		return true;
	}
	template <typename T>
	T PacketBuffer<T>::getNextPacket()
	{
		if (mPackets.empty()) {
			throw out_of_range("empty buffer");
		}
		T temp = mPackets.front();
		mPackets.pop();
		return temp;
	}
	class IPPacket{
	public:
		IPPacket(int id):mID(id) {}
		int getID() const {return mID;}
	private:
		int mID;
	};
	
	int main(int argc, char const *argv[])
	{
		PacketBuffer<IPPacket> ipPackets(5);
		for (int i = 0; i <=6; ++i) {
			if (!ipPackets.bufferPacket(IPPacket(i)))
				cout << "pack " << i << " dropped" << endl;
		}
		while (true) {
			try {
				IPPacket packet = ipPackets.getNextPacket();
				cout << "processing packet " << packet.getID() << endl;
			} catch (const out_of_range&) {
				cout << "queue is empty" << endl;
				break;
			}
		}
	
		return 0;
	}




MARK Pg.422














### C++风格的数组

arr类型为arr中存储的值的类型

int arr1[10] // arr1是常量指针，传递到函数时只传递指针的值而丢失指针大小，需传递数组大小作为函数的另一个参数
int arr1[10] = {10,9,8...}
int *arr2 = new int[n]; // arr2不是常量指针,n动态分配，编译时无问题
delete [] arr2;


### C++字符串

1.C中，空字符`\0`指示结束，并同普通字符一样占据1个字符的空间。

	int realLen = strlen(str2)+1 // 需为空字符分配空间

	char text1[] = "abcde";
	size_t s1 = sizeof(text1); // is 6,sizeof获得数据类型或变量的大小,已包含空字符空间

	const char* text2 = "abcde";
	size_t s2 = sizeof(text1); // sizeof获得const char*的大小，会因32为，64位编译而异

2.C++,字符串字面量（string literal）

只读，编译器对相同字面量值内存中只创建1个实例（称为字面量池），类型为“n个const char的数组”

const char* pt2 = "hello";

char arr[] = "hello"; //编译器创建数组，并将字符串复制到这个数组，此时不是只读，不会只创建1个实例。

3.string（是一个类）

> 所有string对象都创建为堆栈变量（不再内存泄漏），会自动分配内存和调整大小。

operator+=，operator==,operator!=,operator<等运算符都被重载，以操作字符串字符

3.1 数值转换

string s1 = to_string(val);

string s1 = R"(real raw string content)" // 由`R"(`，`)"`包裹










## 设计原则
1.抽象

创建通用接口

2.重用（需确定何时应当重用）

- 对多线程程序代码是否安全
- 库是否要求使用它的代码进行特定的编译器设置？如有必要，项目可以接受吗？
- 库或框架需要什么样的初始化调用或者清理？
- 库或框架依赖于哪些其他库？
- 如果从某个类继承，应该调用哪个构造函数？应该重写哪些虚方法？
- 如果某个调用返回内存指针，谁负责内存的释放：调用者还是库？若是库会在何时释放内存？**强烈建议查看释放可使用智能指针管路由库分配的内存**。
- 库调用检查哪些错误情况？此时做出了什么假定？如何处理错误？如何提醒客户端程序发送了错误？应避免使用弹出消息对话框，将消息传递到stderr/cerr或stdout/cout和中止程序的库。
- 某个调用的全部返回值（按值或引用）有哪些？
- 所有可能的异常有哪些？

3.原型

指最终产品的原型（可能与最终产品完全不同），用来快速测试所引入的库能否满足要求。

## chess design

推荐设计模式：MVC（模型-视图-控制），将数据存储与数据显示明确分离



1. 分出子系统

unified modeling language 

子系统 | 实例数量 | 功能 | 公开的接口 | 使用的接口(其他子系统提供) |
 -| - | - | - | -

2. 确定线程模型
3. 确定子系统中类的层次结构
4. 指定每个子系统的类，数据结构，模式（观察者，仲裁者）
5. 为每个子系统指定错误处理

类的可视化

类 | 相关组件 | 属性 | 行为 |
- | - | - | - |
1 | 2 | 3 | 12345 |












### 名词辨析

数据成员：一个类的内部元素/变量
对象数据成员，类数据成员，class member：都指类型为类的数据，如string，自定义类等
非对象数据成员，非类数据成员，non-class member:都指类型不是类的数据，如int，double，size_t等
sequencing operator，序列运算符，逗号运算符：用于分隔一条语句中的两个表达式，确保从左至右的求值顺序
<<,插入运算符
>>,提取运算符


	mechasnism???
	
	string类默认占28字节
	int类默认占4字节
	
	在类中,若析构函数声明为virtual，类中第一个成员类型为n字节，实例化会用前n个字节不知道干什么，然后再对成员进行初始化。
	但类成员的实例化情况并不明晰
	若第一个成员类型为一个类，则其长度为8字节






# 运行机制：

- 在header声明命名空间，类。
- 在cpp中定义类的函数

声明类对象：

- ClassName2 obj2;
- ClassName2 obj2{};
- ClassName2 obj2{par1,par2};

- ClassName2 obj2(); // 引起歧义，可能是调用函数返回ClassName2类型的值。


## 链接

- 每个源文件单独编译，编译得到的目标文件会彼此链接
- 源文件中每个名称，包括函数和全局变量，都有一个内部或者外部的链接
- 外部链接意味着这个文件在其他源文件中也有效
- 内部链接（静态链接）意味着在其他源文件中无效
- 默认状况下，函数和全局变量都拥有外部链接
- 可在声明前加
- static转变为静态链接
- 可在声明前加extern转变为外部链接（const和
- 默认是内部链接）
- 当指定某个名称为extern时，编译器将这条语句当做声明而不是定义
- 对于变量而言，这意味着编译器不会为这个变量分配空间
- 必须为这个变量提供，单独的，不使用extern关键字的定义行，
- extern int x; int x = 3;
- 或者但也可在同一行初始化
- extern int x = 3;
- 被另一个文件使用时，在另一个文件开头添加声明 `extern typeName foo;`。foo称为全局变量
- 未添加extern则会被当做定义，导致为foo分配空间，链接失败
- 全局变量令人迷惑，建议使用累的静态数据成员和方法

## 运行细节

employee1.h

	#pragma once // 防止文件被包含多次
	#include <iostream>
	class Employee{};
	// header文件中包含iostream,gcc会自动using namespace std,其他ide不会。
	//后续所有代码及其他文件使用employee1.h时都在此命名空间内，慎用。

employee1.cpp

	#include vector
	int main(){
		cout << "no need using namespace std " << endl;
		return 0;
	}

## 编译过程

`-E` preprocess
`-S` compile
`-c` assemble
`-o <targetfile>` link and thus create .exe file

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


## Q&As

1. switch若作为函数，返回值可能不同
