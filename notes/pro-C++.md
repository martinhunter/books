## Prefix

标注：
1. 重要机制： mechanism
2. 范例：exp
3. 注意点：NOTE
4. 未知的问题：ISSUE

## Index


## 变量

### 内存结构
> 运行时会在各个地址之间跳转并获取地址处相应的值
（例如跳转到0x00000004并获取到其中的值11100110）



地址 | 值 |
--- | --- |
0x000001 | 01000110 |
0x000002 | 00000110 |
0x000003 | 01100110 |
0x000004 | 11100110 |
0x000005 | 01110110 |
... | ... |

#### 1.1 变量

> 对象：在C++中，指类的实例

> 仅创建对象（变量）。变量bind的地址不会变化(为方便将地址写为0x123，实际不止这么长)

	int x=2337;  // x会bind一个地址0x123，并保存类型int, 将0x123处的值设为2337
	
	x=2942;  // 跳转到地址0x123，并修改其值
	
	int y = x;  // y会bind另一个地址0x789，并保存类型int,获取地址0x123处的值2942，并设置0x789处的值为2942

#### 1.2 名字(in cpython)

> 创建对象，并创建指向此对象的指针（名字）。变量bind的地址会变化

NOTE: cpython中所有都是PyObject对象

	x=2337  # 创建pyobject对象(地址0x123)，初始化其类型，引用次数，设置值为2337。 创建名字x, bind此对象的地址0x123。将0x123的引用次数+1
	
	x=2942  # 创建pyobject对象(地址0x432)，初始化其类型，引用次数，设置值为2942。x已创建，修改其bind的地址0x123为0x432
	
	y=3  # python内置了简单的字符，数字常量（0-256）的PyObect对象，y=3不生成新的PyObect而是绑定内置对象。

	y=x  # 创建名字y, 获取x bind的地址0x432, y bind地址0x432

exp：

string x = "ssing";  // C++
1. compiler创建string类型的变量x
2. 设置x的类型,所在的地址
2. x{Address: 0x123, type: string }
3. compiler将地址0x123处的值设置为"ssing"(可能会先进行隐式的类型转换)
4. 获取x的值时,compiler会跳转到地址0x123读取数据,并根据类型判断要读取的长度

x = "ssing"  # python
1. 创建匿名的PyObject类型对象anonymous
2. 设置anonymous的类型,所在的地址,被引用次数
2. anonymous{Address: 0x123, refcount: 0, type: string}，数据总长度为string类的长度加上refcount(int类)的长度
3. interpreter将地址0x123处的值设置为"ssing"(可能会先进行隐式的类型转换)
4. 创建名字x
5. 设置x的类型,所在的地址
2. x{type: name/pointer, Address: 0x654}
3. interpreter将地址0x654处的值设置为0x123，然后获取地址0x123处的值，并将anomynous的refcount加1
4. 获取x的值时,interpreter会跳转到地址0x654读取数据,并根据类型判断要读取的长度，得到0x123
5. 由于类型为name/pointer,会再自动访问0x123处的值
 

### 指针变量

形式：`int* var = &value;` // value为一个变量

int*：创建指针，它指向的值的类型为int
&value: 获取value的地址
*pt: pt的值为一个地址，获取此地址中存储的值

exp:

	int value = 4;  // value bind 地址0x123，跳转到此地址并将值为设置4
	
	int * pt = &value;  // 获取value的地址0x123，pt bind 地址0x432, 跳转到0x432处并将值设为0x123
	
	int value2 = *pt;  // 跳转到pt bind的地址0x432，获得值0x123。*处理值0x123，跳转到0x123，获得值4。
					   // value2 bind 地址0x511，跳转到此地址并将值为设置4

### 智能指针：对象超出作用域，如函数执行完毕，自动释放内存

储存在 `memory` 头文件中

- make_unique<clsName>()
- make_share<clsName>()
- make_weak<clsName>()

## 引用

> 为一个已存在的值定义一个新的名字，而不会进行值的复制
>> `引用=变量;` 如果变量bind的地址为x,则引用也bind地址x，类似名字(in cpython), 但bind的地址不能修改(跟变量一样)。相当于变量与名字的结合
>> [references are not objects](https://en.cppreference.com/w/cpp/language/reference)

使用形式：`int & var = value;`  // value为一个变量或const右值

特性：
- 创建时就初始化，因此必须先在ctor中初始化引用数据成员(而不能在函数体内）
- 不能引用未命名的右值，除非使用const修饰引用(形式为`const int &ref = 40;`)

exp:

	int value = 4;  // value bind 地址0x123，跳转到此地址并将值为设置4
	
	int & ref = value;  // 获得value bind的地址0x123，ref也 bind 地址0x123
	
	int value2 = ref;  // 跳转到ref bind的地址0x123，获得值4。

引用 vs 指针：

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


### 左值引用：对一个左值引用，在类型后加符号`&`

> 左值：是一个标识非临时性对象的表达式。一个对象被命名了，它就是一个左值。
> 右值：是一个标识非临时性对象的表达式，非左值都是右值，如常量值，临时对象或临时值。

左值引用：引用左值（函数返回值为右值，不能直接左值引用），一般引用`变量名`（指代一个对象）。

exp: 左值引用尝试引用右值时引发错误:cannot bind non-const lvalue reference of type 'int&' to an rvalue of type 'int'

	//error exp 1
	int & lref = 30;
	//error exp 2
	int func(int arg){return arg}; 
	int & lref = func(arg);
	// 因为右值是临时性对象,只是一个不可变的值，未命名

	string f = "tempVal";
	// 临时地址及其中的值会在赋值后（左值的变量地址中保存了值的复制）被销毁。

左引用的作用：
1. 简化复杂的名称
2. 不创建值的副本（可用于循环中map本身）

exp: 使用左引用

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
	int & func(vector<int> myArray){return myArray[1];}
	int & lref = func(ar);
	if(&lref == &arr[1]){return 0}

### 右值引用：对一个右值(临时量）引用，在类型后加符号`&&`

右值引用：引用右值，右值（可称为匿名变量）一般都是个临时值，字面常量。

(mechanism)：匿名变量（未命名的变量，指某个值未bind一个命名的变量）bind的地址区域会在切换作用域时立即被销毁

exp: 为什么默认是复制右值

	void func(string val){cout << val;}
	func("thisIsLiteral");

1. "thisIsLiteral"是一个匿名变量，在func外界创建
1. 切换到func作用域后，匿名变量"thisIsLiteral"被销毁，其地址范围标记为空闲状态
1. 此时这个对象可能被一个未知的对象使用
1. 若将val直接bind "thisIsLiteral"的地址
1. 无论是未知对象(通常与val大小不同)还是val的值进行了修改，都几乎肯定造成对方的错误。
1. 为避免这种错误，C++对这类右值进行复制（变量bind一个新地址而非bind右值的地址）

exp: 使用右值引用

	string s = "hell";
	string&& pl = s + "wo";

	void func(string&& val){cout << val;}
	func("thisIsLiteral");
	// val绑定匿名变量"thisIsLiteral"的地址，`&&`迫使val离开其作用域前，此匿名变量不被销毁

NOTE: `&&`是一整个符号，并不是代表引用的引用

#### 右值引用 vs 左值引用

右值引用
- 引用右值
- 每个右值同时只能存在一个右值引用
- 右值引用超出作用域后销毁对象

左值引用
- 引用左值
- 每个左值同时可存在多个左值引用
- 左值引用超出作用域后不销毁对象

ISSUE：C++11后添加新符号&&表示右值引用。问：为什么要添加&&，而不是用&同时表示左右值引用？可能的原因为：
1. &只能引用左值（或const右值），为保证兼容性而添加新符号
2. 右值引用超出作用域后应当销毁对象，而左值引用超出作用域后却不应当销毁对象，若不区分左右引用，就会造成错误。（比较合理）

#### std::move 和 std::swap

> 都使用了右值引用

std::move将左值转换为右值，右值拥有可移动性
- std::move()实际上使用了static_cast<typeName &&>()

std::swap将左值与右值中的值互相交换（交换bind的地址值）
- swap实际上是使用了std::move()避免复制

	string b = "turnToRValue";
	// 由于只能存在一个右值引用，当前作用域内b bind 地址改为Null

	string a = std::move(b);

	string c = "swap C to A";

	std::swap(a,c);

	cout<< "a: " << a << "\nb: " << b << "\nc: " << c << endl;



## 函数

> 普通函数是只读的，后期不能进行修改。

> cout所有func，\*func（包括函数指针(\*func) ）的值都为1

NOTE: 函数所有设置默认值的参数都要放到最后（同python的**kwargs）

形式：returnType funcName(paramType param){body; return someValue;}
调用：funcName(args);

- param传递机制: 默认按值传递
- return传递机制: 默认返回右值

exp: 创建及调用函数

	MyClass func(string s){MyClass ll(s); return ll;}
	string bs = "ssss";
	MyClass rr = func(bs);
	
	运行过程：
	1. string s = bs;
	2. MyClass rr = ll;



### 函数指针

- 函数形式:rtType originalFunc(parType1 par1, parType2 par2){}
- 函数指针形式：rtType (*FuncPointer)(parType1, parType2) = originalFunc;  // 在originalFunc前加不加&都没有影响
	- 形式说明：函数指针形式同函数,但要将`originalFunc`改为`(*FuncPointer)`
	- 调用函数指针:调用方式与普通定义的函数相同,`FuncPointer(arg1, arg2);`
	- 特性：函数指针可赋值，因此指向的函数可变，而普通函数不能赋值（只读）
	- 作用：为一个函数起别名

exp: 创建函数指针

	#include <iostream>
	using namespace std;
	
	int ch(double bil, int rr){
	    cout << bil << " and " << rr << endl;
	    return 32;}
	void f1(){ cout << 13 << endl; }
    void f2(){ cout << 26 << endl; }	
	int main(){
	    int (*pt)(double, int) = ch;
	    int (*pt3)(double, int) = ch;
		cout << ch << endl;  // >>> 1
	    cout << *ch << endl;  // >>> 1 
	    cout << pt << endl;  // >>> 1
		cout << *pt << endl;  // >>> 1
	    cout << pt3(2.2,4) << endl;  // >>> 32, 调用了ch()
	    cout << "---seperator---" << endl;
		void (*f3)() = f1;
	    f3();  // >>> 13
		f2 = f1;  // 普通函数只读，因此报错
	    f3 = f2;  // 函数指针可写/可进行赋值，不会报错
	    f3();  // >>> 26

		return 0;
	}
































## （函数的）参数传递&返回值传递

> 默认对一个函数，将函数内相应的形参值初始化为实参的值。如此这个函数获得了实参值的拷贝，而并不会对实参的值产生影响。

原理：使用代换模型，将实参值赋值给形参

exp: 传值调用过程

	arg = 3
	int func(int param){
		param += 1;
		return param
	}
	int returnVal = func(arg)

	// 运用代换模型
	int param = arg;  // 访问arg bind的地址，并获得值3
	param = 3;
	param += 1;
	int returnVal = param  // param为右值，访问param bind的地址，并获得值3赋值给returnVal，param超出作用域后即被销毁
	

exp: 传指针调用过程

	string func(string * param){
		*param += "AnyStr";
		return "arr already changed";
	}
	int main(){
		string arr = "superCo";
		string retArr = func(&arr);
	}

	// 运用代换模型
	string * param = &arr  // param保存了arr bind的地址
	*param += 'AnyStr';  // 跳转至arr的地址，并修改其中的值
	string retArr = "arr already changed";  // "arr already changed"为右值，超出作用域后即被销毁

exp: 传引用调用过程
	
	vector<int> arg = {3,6,8};
	void func(vector<int> & param)
	{
		for(auto & x: param){
			x += 10;
		}
	}
	func(arg)
	if(arg[1] == 13){return 0}
		
	// 运用代换模型
	vector<int> & param = arg;  // arg bind 地址，将param也bind此地址
	auto & x = param[0];  // 获取param[0] bind的地址，并将x也 bind 此地址
	x += 10;  // 跳转至x bind的地址，并修改其中的值
	auto & x = param[1];  // 获取param[1] bind的地址，并将x也 bind 此地址（不再是param[0]的地址）
	x += 10;  // 跳转至x bind的地址，并修改其中的值
	auto & x = param[2];  // 获取param[2] bind的地址，并将x也 bind 此地址不再是param[1]的地址）
	x += 10;  // 跳转至x bind的地址，并修改其中的值
	// 离开作用域，销毁x,param

### 参数传递类型

1.传值调用（call-by-value)

> 是默认的传递方式，函数接收某个值或者对象的副本
> 适用：小的，不改变的实参（对象）
	
	void print2(double a){
		cout<< a << endl;
	}
	
	// 完全复制实参的值，低效
	vector<string> a{"one","two","three"};
	void randomItem(vector<string> arr){
		cout << arr[0];
	}
	reffunc(a);

2.传（左值）引用调用（call-by-lvalue-reference)

> 适用：改变实参的值

	double x = 3;
	double y = 4;
	void swap(double & a,double & b){
		double temp = a;
		a = b;
		b = temp;
	}
	swap(x,y)  // 调用

3.传常量引用调用（call-by-constant-reference)

> 适用：大的，不改变的实参（对象），且赋值代价昂贵。对引用加上const，禁止引用后修改实参。
	vector<string> a{"one","two","three"};
	void reffunc(const vector<string> & arr){
		cout << arr[0];
	}
	reffunc(a);

4.传（右值）引用调用（call-by-rvalue-reference)

> 核心：右值存储要被销毁的临时量，像x=rval(rval为右值)通过`移动而非复制`实现。可给予参数是左值还是右值重载函数实现。

> 适用：实参就是1个大的右值直接传入

	void rhsReffunc(const vector<string> && arr){
		cout << arr[0];
	}
	rhsReffunc({"one","two","three"});

### 返回值传递类型

> 在所有情况下函数调用的结果都是一个右值。
> c++11后，若赋值运算符的右边（或构造函数）是一个右值，那么当对象支持移动操作时，能自动避免复制

1.传值返回

	int func(vector<string> arr){
		int i = 4;
		return i;
	}

2.传引用返回:参数，返回类型，皆设为左值引用类型。有一处未引用都会造成对象的复制（但使用并返回vector对象，类似python列表，则只要将参数设为左值引用类型即可）。
	
	vector<string>& reffunc(vector<string>& arr){
		arr[0] = "newS";
		return arr;
	}
	vector<string> a{"one","two","three"};
	vector<string>& rf = reffunc(a);

3.传常量引用返回

	const string& reffunc(const vector<string>& arr){
		return arr[2];
	}
	vector<string> a{"one","two","three"};
	const string& crf = reffunc(a);

4.右值移动返回（std::move将左值转换为右值，支持移动)

	vector<string> func(vector<string>& arr){
		arr[0] = "333";
		return arr;
	}
	vector<string> a{"one","two","three"};
	vector<string> crf = move(reffunc(a));

	1. 不用右值引用	
	void swap(vector<string> & x, vector<string> & y){
		/*temp，x，y都为左值，会进行3次复制。
		* 改为vector<string>& temp = x; 可减少一次复制。
		* 但是x = y;依然会进行复制，也即跳转至y的地址，获取y的值，然后跳转至x的地址，设为y的值。
		* y = temp同理。
		*/
		vector<string> temp = x;
		x = y;
		y = temp;
	}
	2. 转换类型为右值引用
	void swap(vector<string>& x, vector<string>& y){
		vector<string> tmp = static_cast<vector<string> &&>(x);
		x = static_cast<vector<string> &&>(y);
		t = static_cast<vector<string> &&>(tmp);
	}
	3. move会使用移动语义，将左转化为右值
	void swap(vector<string>& x, vector<string>& y){
		vector<string> tmp = std::move(x);
		x = std::move(y);
		t = std::move(tmp);
	}













#### 类型推断

使用 auto,decltype 自动判断右值的数据类型

最好使用decltype(auto)判断类型：

	const string message = "test";
	const string& foo(){ return message };
	
	const auto & f1 = foo();
	decltype(foo()) f2 = foo()
	decltype(auto) f3 = foo()
	
	/* f1,f2,f3作用相同,
	但f2中foo()调用2次
	推荐使用f3，
	f1也可行，不推荐f2*/

拖尾返回类型：返回类型在参数列表后指定，如此解析的时侯参数名称（及参数类型，t1+t2的类型）已知。（C++14中可省略拖尾返回类型）

	template<typename Type1, typename Type2>
	auto myFunc(const Type1& t1, const Type2& t2) -> decltype(t1+t2)
	{return t1 + t2;}

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

销毁：指将此部分内存标记为空闲状态，空闲的内存可被分配给其他对象

1. string s = "toBeDestroyed"; // s bind的地址为0x61fde0。这个string的范围为0x61fda0~0x61fdc0
1. 销毁s
1. 删除整个变量名s
1. 不会修改0xcdf2fa19处的值
1. 但会将0x61fda0~0x61fdc0标记为空闲（供以后的变量使用）

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

> When using new,memory 
> is allocated on heap,and it's pointer needs to be deleted otherwise it will live and thus causes memory leak.

> But new doesn't always mean memory will be allocated on heap , it depends like if A is local variable (like in a method) it will be on stack memory Or if A is a member of a class then it will be on heap when instance of class is created.

NOTE: if A is static it will be on stack memory always!

2.[delete](http://www.cplusplus.com/reference/new/operator%20delete[]/)的作用：用于deallocate指针所指向的内存块(而不删除指针本身)，释放new创建的存储空间并将指针地址设为无效。

使用delete之后指针本身依然可被调用，因此需新赋值或设为nullptr以免出错。

exp:释放new创建的空间

	delete heapPointer; //删除指针
	heapPointer = nullptr;
	
	delete [] arrayName; //删除数组指针
	arrayName = nullptr;












***
***
***

# 类

> 类默认说明符为private，struct默认说明符为public

形式：`class ClassName{};`

创建(无参数)实例： `ClassName inst;` // 与 ClassName inst{}; 作用相同

NOTE:创建类对象最好使用{}，例如 ClsName instance2{args}。创建无参数的实例对象，使用()会被当做返回值为ClsName的函数处理，从而报错

## 构造函数

作用：创建类对象时自动调用构造函数以初始化对象。

创建对象/为对象分配空间(mechanism)：
- 创建一个实例对象时（例如此对象需要32个字节）
- 将空闲的内存地址(如0xbfdd-0xbffd)分配（绑定）到此对象
- 此时其中的值未进行初始化，都是随机值
- 此时若指针指向随机值并尝试调用会产生不可知的后果（通常是内存访问错误）

对象(成员变量)初始化：将0xbfdd-0xbffd处的值设置为期望的（有效）初始值

形式：与类同名但没有返回值

#### 隐式转换为类对象

当`=`左侧为一个类对象，右侧为其他类型值/对象时，若类有参数为右值类型的构造函数，会将右值作为参数传到此构造函数中，以创建一个临时对象，没有则会报错。
	
exp：隐式转换
	
	class Cell
	{
	public:
		Cell(std::string value);
		Cell(int value);  // 会将10作为参数传入此构造函数并创建临时对象
		Cell(double value);
	};
	Cell ins = 10;
	Cell ins2(10);

#### explicit

只有1个参数的构造函数

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
- private: 仅本类可调用,派生类也不可调用

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

exp: 创建对象

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

- 析构函数（destructor) 所有类必须有，其他几个函数可=delete

- 拷贝构造函数（[copy constructor](https://en.cppreference.com/w/cpp/language/copy_constructor)）
- 移动构造函数（move constructor）
- 拷贝赋值运算符（copy assignment operator)
- 移动赋值运算符（move assignment operator)

> 有动态分配的内存时(new),需提供以上的函数

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

exp: 另一个包含5大函数的类

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

形式： constexpr int foo(){return 10;}  // 函数无参数

也可将变量绑定为字面常量（或模板中的参数）

static consexpr int value = 24;  // static不是必须的



机制及限制：编译期间对constexpr函数求值，函数不允许有任何副作用(mechanism)

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

析构对象的顺序（同创建顺序相反）(mechanism)：

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

作用：运行时判断对象所属类(类型判断)
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

class Child: protected Super{};x：父类所有public方法和数据成员变为protected。
class Child: private Super{};：父类所有public，protected方法和数据成员变为private。

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

### 非局部变量的初始化顺序(mechanism)

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
    // oldName前的&仅为了告诉使用者这是一个函数指针，省略后对结果无影响

	void (*noTypePtr)(int a) = &oldName;
	void (*noTypePtr2)(int a) = &oldName;

	// 使用typedef，将void (*)(int a)类型命名为FuncPtrType
	typedef void (*FuncPtrType)(int a);
	FuncPtrType typedPtr = &oldName;
	FuncPtrType typedPtr2 = &oldName;


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
	// int i = static_cast<int>(el); 添加explicit后需显式调用

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




exp: 模板示例

	template <typename T>
	class Grid
	{
	public:
		explicit Grid(size_t inWidth = kDefaultWidth,
			size_t inHeight = kDefaultHeight)
		:mWidth(inWidth),mHeight(inHeight){
			initializer();
		}
		virtual ~Grid(){}
		void setElementAt(size_t x, size_t y, const T& inElem){
			mCells[x][y] = inElem;
		}
		T& getElmeAt(size_t x, size_t y) {
			return mCells[x][y];
		}
		const T& getElmeAt(size_t, size_t y) const{
			return mCells[x][y];
		}
		size_t getHeight() const {return mHeight;}
		size_t getWidth() const {return mWidth;}
		static const size_t kDefaultHeight = 10;
		static const size_t kDefaultWidth = 10;
	private:
		void initializer(){
			mCells.resize(mWidth);
			for (std::vector<T>& column : mCells) {
				colunm.resize(mHeight);
			}
		}
		std::vector<std::vector<T> > mCells;  // don't use ...<T>> in C++11
		size_t mWidth,mHeight;
	}

template <class T>  # 历史上曾经使用class
template <typename T>
2者作用相同，此处class并不要求T为一个类，而是所有皆可

NOTE：模板要求实现也在头文件（或在最后include实现的文件.h或.cpp），编译器在创建模板实例前，要知道完整的定义包括方法的定义。若无include，则在实现文件.cpp的最后加上`template class Grid<int>;template class Grid<double>;`,如此可以模板限定可实例化的类型。

编译器处理模板的过程：
1. 遇到模板方法定义时，语法检查，但不编译模板（此时未传入参数）
2. 遇到实例化模板，将类定义中的每个参数替换为实例参数，编译器得以生成实例模板代码
3. 为泛型类的所有虚方法（如析构函数必须是虚方法）生成代码，对非虚方法，只为被调用的非虚方法生存代码。
	- exp: 只有这2行代码时
		- Grid<int> myGrid;
		- myGrid.setElementAt(0,0,10);
	- 只为此实例模板生成无参构造函数，析构函数，setElementAt()的代码。
	- 因此，若Grid<T>中定义了如下方法：
		- void ad(const T& elem) {elem++;}
	- 即使传入Grid<T>的类型T不支持++操作，只要不调用ad方法，就不会报错

template参数

template <typename T = double, size_t Width = 12>
typename为类型参数
只有整数类型（不含double，float），枚举类型，指针，引用属于非类型参数
可设置默认值

exp: 调用时,Width必须为字面量,const变量,constexpr

	Grid<> zeroDefault;  // 由于设置了默认值，所以不会报错
	Grid<double> zeroDefault2;  // 由于设置了默认值，所以不会报错
	Grid<double,12> first;  
	const size_t wid = 12;
	Grid<double, wid> second;

	constexpr size_t get(){return 12;}
	Grid<double, get()> third;

方法模板

NOTE: 需要在每个方法模板前都加上template<...>,同时使用2个模板时，要将类模板的声明放在成员模板前边，而不能合并。通常用T，E表示

template <typename T>
template <typename AnotherT>
Grid<T>::Grid(const Grid<AnotherT>& src){
	copyFrom(src);
}

template specialization(模板特例化)

起因：
- 定义模板类Grid<..>,但实例模板对某些类型无意义或不起效，
- 且Grid类已存在，不能重用Grid这个名称，不能再定义一个非模板的class Grid{};（但是函数可以）
- 需要对这些类型模板进行重载（重写），就要模板特例化。

形式：template为空，const char*为要实例化的类型，将所有Grid类改为Grid<const char*>

作用：在已定义普通模板的情况下，默认所有Grid<int>,Grid<double>,Grid<const char*>都会调用普通模板。而Grid<const char*>特例化后,则Grid<const char*>只会调用特例化后的模板

exp: 

	template <>
	class Grid<const char*>{ommited;};
	Grid<const char*>::Grid(size_t inWidth):mWidth(inWidth){}

	Grid<const char*> spec;  // 需显式声明
	spec.ommited;

类模板派生

class Sub: public Super<int>{};  // 继承实例模板不用template

template <typename T>  // 继承类模板
class Sub: public Super<T>{};  // 将所有Sub,Super类替换为Sub<T>,Super<T>即可
template <typename T>
Sub<T>::Sub(size_t inWidth):Super<T>(inWidth){}

模板别名

typedef myTemplate<int , double> aliasName  // specify all

template <typenmae T1, typename T2>  // specify parts
using aliasName = myTemplate<T1, double>;

替换函数语法

原理：返回类型在参数列表后指定（拖尾返回类型），因此解析时参数名称（及参数类型，t1+t2的类型）是已知的。（C++14中可省略拖尾返回类型）

template<typename Type1, typename Type2>
auto myFunc(const Type1& t1, const Type2& t2) -> decltype(t1+t2)
{return t1 + t2;}

###　函数模板

同类模板

	static const size_t NOT_FOUND = (size_t)(-1);
	template <typename T>
	size_t Find(T& value, T* arr, size_t size){
		for (size_t i = 0; i < size; ++i) {
			if (arr[i] == value) {
				return i;
			}
		}
		return NOT_FOUND;
	}

	int x = 3, Ar[] = {1,2,3,4};
	size_t sizeAr = sizeof(Ar);
	size_t result;
	result = Find(x, Ar, sizeAr);  // calls Find<int> by deduction
	result = Find<int>(x, Ar, sizeAr);  // calls Find<int> explicitly

	template <typename T, size_t S>
	size_t Find(T& value, T(&arr)[ S])  // ???
	{ return Find(value,arr,S)}

#### 函数模板特例化

同普通模板特例化

    template<>
	size_t Find<const char*>(const char*& value, const char** arr, size_t size){
		cout << "Specialize" << endl;
		for (strcmp(arr[i], value) == 0) {
			return i;
		}
		return NOT_FOUND;
	}

函数重载：用非模板函数重载, 同特例化作用相同.*非模板的优先级比模板高*。但调用普通函数写法为Find(x, Ar, sizeAr),不会自动推导类型，必须显式声明Find<type>，因此不推荐使用重载。

NOTE：编译器优先选择最具体的版本，即非模板的版本

友元

形式：friend Cls<T> operator+ <T>(paramType param);在operator+后加上<T>以表明operator+本身是一个模板（即一个函数模板）。类模板和函数模板共用参数T

	template <T>
	class Grid;
	template <typename T>
	Grid<T> operator+(const Grid<T>& lhs, const Grid<T>& rhs){
		Grid<T> elem;
		elem.mValue = lhs.mValue + rhs.mValue;
		return elem;
	}

	template <T>
	class Grid{
		..ommited..
		friend Grid<T> operator+ <T>(const Grid<T>& lhs, const Grid<T>& rhs);
	}

可变模板(C++14)

template <typename T>
constexpr T pi = T(3.1415926);

float piInt = pi<float>;
long double piLong = pi<long double>;











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

	} catch (...) { // 用三个点匹配所有异常

	throw runtime_error("deco error");
	} catch (const exception& e) {  // runtime_error继承exception类
		cerr << e.what() << endl;
	}
	
	throw invalid_argument("wrong arguments");
	} catch (const invalid_argument& e) {
	
	throw 5;
	} catch (int e) {
	
	throw "fail open";
	} catch (const char* e) {

建议将对象作为异常抛出：

- 对象的类名称可以传递信息
- 对象可存储信息，包括描述异常的字符串

当程序遇到未捕获的异常时，会调用内建的terminate()函数，这个函数调用 cstdlib 中的abort()来中止程序。可调用set_terminate()函数（返回值为旧的terminate_handler）设置新的terminate_handler,此函数采用指向`回调函数`（无参数，无返回值）的指针做参数

exp:中止未捕获的异常前输出有效信息

    #include <iostream>
	using namespace std;

	/*  
    // terminate_handler,set_terminate的定义大致如下
	typedef void (*terminate_handler)();
	void default_handler();  // 前置声明
	terminate_handler handler = default_handler;

	terminate_handler set_terminate(terminate_handler func)
	{
		terminate_handler temp_prev = handler;
		handler = func;
		return temp_prev;
	}
	// default_handler为默认的回调函数，无返回值
	void default_handler(){ 
		// cout << " default handler " << endl;
        abort();
		// some real handling work
	}
	*/

	void myTerminate()
	{
		cout << "some more info" << endl;
		exit(1);  // 使用exit中止程序
	}
    int main(int argc, char *argv[]){
	    // void (*prevTerminate)() = set_terminate(myTerminate); 2者皆可
	    terminate_handler prevTerminate = set_terminate(myTerminate);

	    // terminate的运行原理(高度概括)
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
    }
	set_terminate(prevTerminater); // 需要myTerminate处理异常的代码段结束后将terminate_handler设为prevTerminater
	someOtherCode；
	
#### throw list：抛出列表

形式：rtType func(args) throw(exception1,exception2,...) { body; }

标记为noexcept的函数抛出异常时，C++调用terminate()中止程序。
函数抛出不在抛出列表中的异常时，C++调用unexpected(),内建的unexpected()调用terminate()

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











priority_queue的定义大致如下:
template <class T, class Container = vector<T>,
		class Compare = less<T> >
- 调用priority_queue<Er>,
- 会创建priority_queue<Er，Container = vector<Er>,Compare = less<Er> >
- 容器为vector<Er>类型
- 插入新元素时，要将其插入到适当的位置
- 会调用less<Er>比较所有元素，即调用Er中的operator<比较所有元素
- 因此必须在Er中实现operator<
- 获取其中优先度最高的元素，p_queue.top()

	bool operator<(const Error& lhs, const Error& rhs){
		return lhs.mPriority < rhs.mPriority;
	}
	std::ostream& operator<<(std::ostream& os, const Error& err){
		os << err.mError << " (priority is " << err.mPriority << " )";
		return os;
	}

	class Error{
	public:
		Error(int priority = 30, const std::string& errMsg)
		:mPriority(priority),mError(errMsg) {}
		int getPriority() const { return mPriority;}
		const std::string& getErrorMsg() const { return mError;}
		friend bool operator<(const Error& lhs, const Error& rhs);
		friend std::ostream& operator<<(std::ostream& os, const Error& err);
	private:
		int mPriority;
		std::string mError;
	};

	class ErrorCorrelator{
	public:
		void addError(const Error& er){
			mErrors.push(er);
		}
		Error getError(){
			if (mErrors.empty()) {
				throw out_of_range("empty queue");
			}
			Error top = mErrors.top();
			mErrors.pop();
			return top();
		}
	private:
		priority_queue<Error> mErrors;
	};

关联容器（键值对）

pair，在<utility>中，每个pair都保存2个数据

相当于
template <typename T1, typename T2>
struct pair{
	T1 first;
	T2 second;
	bool operator<(const T1& lhs, const T2& rhs){
		if (lhs.first < rhs.first && lhs.second < rhs.second) {
			return true;
		}
		return false;
	}
};

创建pair的几种方法

1. pair<string, int> mp("hel",5);

2. pair<string, int> mp(first="hel",second=5);

3. pair<string, int> mp;
mp.first="hel";
mp.second=5;

4. pair<string, int> mpCopy(mp);

5. auto mp = make_pair("hel",5);


Map

insert：不替换旧值，插入的元素也可为pair，也可为iterator

	map<int, Data> myData;
	auto ret = myData.insert({12, Data(10)});  // auto为pair<map<int,Data>::iterator, bool>

	map<int, Data> another;
	myData.insert(begin(another),end(another));

operator[]则会替换旧值，总是需要先创建一个新值对象,并修改myData
myData[12] = Data(10);

find(key),确认元素是否存在，然后用setVal(val)插入新值，可避免报错或不适当的插入
auto it = myData.find(5);
if (it != end(myData)) {
	it-> second.setVal(Data(14));
}

erase(key)删除元素

	class BankAccount{
	public:
		BankAccount(int acctNum, const std::string& name)
		:mAcctNum(acctNum), mName(name){}
		void setAccountNum(int acctNum) {mAcctNum = acctNum;}
		int getAcctNum() const { return mAcctNum;}
		void setClientName(const std::string& name) { mName = name;}
		const std::string& getClientName () const { return mName;}
		void rmAccount(){}
	private:
		int mAcctNum;
		std::string& mName;
	};

	class BankDB{
	public:
		bool addAccount(const BankAccount& acct){
			auto res = mAccounts.insert({acct.getAcctNum,acct});
			return res.second;
		}
		void delAcct(int acctNum){
			mAccounts.erase(acctNum);
		}
		BankAccount& findAccount(int acctNum){
			auto it = mAccounts.find(accNum);
			if (it == end(mAccounts)){
				throw out_of_range("empty");
			}
			return it->second;
		}
		BankAccount& findAccount(const std::string& name){
			for (auto& p : mAccounts) {
				if (p.second.getClientName() == name) 
					return p.second;
			}
			throw out_of_range("not the name");
		}
		void mergeDatabase(BankDB& db){
			mAccounts.insert(begin(db.mAccounts),end(db.mAccounts));
			db.mAccounts.clear();
		}
	private:
		map<int, BankAccount> mAccounts;
	};


multimap

没有operator[],insert始终成功，因为它允许相同的键值对

mark Pg.442


## 算法

将迭代器作为中介操作容器，而不直接操作容器本身
<algorithm>,<numeric>

exp: find

	Contain<..> Container;

	auto it = find(beign(container),end(container),searchValue);
	if (it == end(container)) { cout << "not found" << endl;}

exp:find_if,将元素传入conditionFunc并判断，为true则说明找到

	bool conditionFunc(elemType el)
	{
		elemType SomeValue = ..;
		return el > SomeValue;
	}
	auto it = find_if(beign(container),end(container),conditionFunc);
	if (it == end(container)) { cout << "not found" << endl;}
	else { cout << *it << endl; }

exp: accumulate,返回一个数类型的值,即auto通常为int，double，long int
	
	auto sum = accumulate(beign(container),end(container),initialValue);

### lambda(匿名函数)（是一种仿函数）

> NOTE：仿函数在C++中的作用为闭包

形式：`[](parType1 par1, parType2 par2){ body; }`

形式（Pg.464)：auto rt = [capture_block]\(paramType param) mutable exception_specification attribute_specifier -> return Type{ body };

说明：
- [var]用来捕捉(通常不变的）变量用于直接在lambda的body中使用，默认传值副本,且此变量是`只读`的，要修改需要引用[&var],此时iterator变化时，var的值都会改变。
- (parmaType param)为匿名函数的参数,没有可整个省略
- {},函数体

exp: 通过()整体包裹lambda，直接使用匿名函数

	int value = 2;
	int res = ([value](int mid){return value*6+mid;})(13);  // 13即参数mid

exp: []的使用

	double captureVar = 2.13;
	auto rt = [localStr = "As: ", captureVal]{ cout << localStr << captureVar << param << endl;};

exp: unique_ptr不能复制只能移动,需使用std::move.

	auto mPtr = std::make_unique<double>(3.14);
	auto myLambda = [p = std::move(mPtr)] { std::cout << *p; }

<functional>的function是多态的函数对象，类似函数指针。

形式：function<returnType(paramType,paramType2)> fn(){};无参显式声明void

	// function<int(void)>可由auto替换
	function<int(void)> multiplyBy2Lambda(int x){
		return [x]{ return 2*x; };
	}
	function<int(void)> fn = multiplyBy2Lambda(5);
	cout << fn() << endl;

exp: lambda作为函数参数

	void test(const vector<int>& vec, const function<bool(int)>& callback){
		for (const auto& i :vec) {
			if(!callback(i)) break;
		}
	}
	vector<int> vec{1,2,3,4,5};
	test(vec, [](int i){return i < 6;});

exp:countif,counter记录运行次数，filtered记录符合条件的元素数量

	vector<int> vec{1,2,3,4,5,6};
	int counter = 0;
	int val = 3;
	int filtered = countif(cbegin(vec),cend(vec),[val,&counter](int comp){counter++; return comp > val;})

exp: generate,[&value]每次都会改变

	vector<int> vec(10);
	int value = 1;
	generate(begin(vec),end(vec),[&value]{value*=2; return value;})

### 函数对象（function object）

> 又称仿函数（functor）,是用类对象取代函数指针的技术

算术函数对象:plus，minus，multiplies，divides，modulus

优点：可以回调形式传递给算法

plus<int> mp;
int res = mp(4,5);

double mult = accumulate(cbegin(nums),cend(nums),1, multiplies<int>());

透明运算符仿函数

指忽略模板类型参数，它们是异构的，会自动判断类型，建议使用它

exp: multiplies<>()不要输入参数int，这样不会损失精度

	vector<int> nums{1,2,4};
	double result = acumulate(cbegin(nums),cend(nums),1.1, multiplies<>());

比较函数对象：equal_to,not_equal_to,less,greater,less_equal,greater_equal

priority_queue<int,vector<int>,greater<>> greater_queue;

逻辑函数对象：logical_not,logical_and,logical_or

exp: 实现allTrue()函数

	bool allTrue(const vector<bool>& flags){
		// true值为1，false值为0
		return accumulate(begin(flags), end(flags), true, logical_and<>());
	}

### 函数对象适配器

Pg.470-548



## STL扩展

每个STL容器都接受一个Allocator类型作为模板参数
template <class T, class Allocator = allocator<T>> class vector;
allocator()进行内存分配,deallocator()进行内存释放

迭代器适配器

## 深入了解模板

类型参数，非类型参数，模版参数模板（template template）


模版参数模板

形式： template<..., template<templateTypeParams>,...>
作用： 不用传2次参数，因此以避免错误。

exp: 1,2需要传递2次int，3,4则会自动将int传递给第二个参数。

	// 1. 普通模板
	template<typename T, typename Container>
	class Grid{
	private:
		std::vector<Container> mCells;
	}
	Grid<T,Container>::func(){}

	Grid<int, vector<int>> ins;  // vector<>参数必须与前边相同，否则会报古怪的错误

	// 2. 与1相同，但设置了默认值
	template<typename T, typename Container = std::vector<T>>
	class Grid{
	private:
		std::vector<Container> mCells;
	}
	Grid<T,Container>::func(){}
	Grid<int, vector<int>> ins;

	// 3.模板参数模板
	template<typename T, template<typename E, typename Allocator = std::allocator<E>> class Container = std::vector>
	// 调用时为当作一个类模板，因此为Container<E>
	class Grid{
	private:
		std::vector<Container<T>> mCells;
	};
	Grid<T,Container<T>>::func(){}  // keyPoint
	Grid<int, vector> ins;

	4. 为方便理解，将3改为以下形式
	template <typename E, int sz>
	class myVector{
	public:
		myVector():mSize(sz){}
		void add(E elem) { mEl.push_back(elem);}
		void get(int n){cout << mEl[n] << " : " << mSize << endl;}
	private:
		vector<E> mEl;
		int mSize;
	};

	template<typename T, template<typename E, int sz> class C = myVector>
	class Grid{
	public:
		Grid():mNum(34){}
		void add(C<T,14>& elem){
			mCells.push_back(elem);
		}
	private:
	    const int mNum = 23;
		std::vector< C<T,14> > mCells; 
	};
	C<T,14> Grid<T,C<T,14>>::func(int n){return mCells[n];} 
	int main(){
	    Grid<int,myVector> nel;  // 只要传入T，C即可
	    myVector<int,14> temp;  // 必须与nel中C<T,14>相同才能正确添加（当作同一个类）
	    nel.add(temp);
	    return 0;
	}
	// keyPoint，传入实参给E,sz，对C进行实例化，此处为T，14,且要在每处都加上14，因此可以在template中为sz设置默认值

核心：T作为实参传递给形参E，相当于对模版参数模板进行了实例化，实例化后只要传入T，C即可.

exp: 非类型模板参数

	template <typename T, const T defaultVal = T()>
	class Grid{};
	template <typename T, const T defaultVal>
	Grid<T, defaultVal>::func(){}

	Grid<int,10> mGd;

exp: 引用必须是常量表达式，必须引用具有静态存储时间和外部或内部链接范围的完整对象。

	namespace {
		const int defaultVal = 11;
		const Cell defaultCell(1.3);
	}
	template <typename T, const T& defaultVal>
	class Grid{};
	template <typename T, const T& defaultVal>
	Grid<T, defaultVal>::func(){}

	Grid<int,defaultVal> mGd;
	Grid<Cell,defaultCell> mGdCell;

模板部分特例化

template <typename T, size_t Width>
class Grid{ommited};

// in Gd.cpp
#include "Grid.h"
template <size_t Width>
class Grid<const char*, Width> {ommited};

Grid<int,2> gd;
Grid<const char*,3> gd;

// in Gd2.cpp
#include "Grid.h"
#include <memory>
template <typename T>
class Grid<T*>{
private:
	std::vector<std::vector<std::unique_ptr<T>>> mCells;
}

重载模拟函数部分特例化（原本是T，现在重载为T*）

	template <typename T>
	size_t Find(T*& value, T** arr, size_t size){
		for (size_t i = 0; i < size; ++i) {
			if (arr[i] == value) {
				return i;
			}
		}
		return NOT_FOUND;
	}

### 模板递归

创建多维网格

#include <iostream>
#include <vector>
#include <utility>
using namespace std;





template <typename T>
class OneDGrid
{
public:
	explicit OneDGrid(size_t inSize = kDefaultSize)
	{
		mElems.resize(inSize);
	}
	virtual ~OneDGrid(){}
	T& operator[](size_t x)	{
		return mElems[x];
	}

	const T& operator[](size_t x) const	{
		return mElems[x];
	}
	void resize(size_t newSize)	{
		mElems.reisze(newSize);
	}
	size_t getSize() const { return mElems.size();}
	static const size_t kDefaultSize = 10;
private:
	std::vector<T> mElems;
};

OneDGrid<int> single;
OneDGrid<OneDGrid<int> > twoD;
OneDGrid<OneDGrid<OneDGrid<int> > > threeD;

// 设置递归，并对1特例化
template <typename T, size_t N>
class NDGrid
{
public:
	explicit NDGrid(size_t inSize = kDefaultSize)
	{
		// 内部grid调用默认构造函数，因此NDGrid初始化时需显式调用inner_insstance.resize(parentSize)以使其初始化为父类大小
		resize(inSize);  

	}
	virtual ~NDGrid(){}
	NDGrid<T, N-1>& operator[](size_t x)	{
		return mElems[x];
	}

	const NDGrid<T, N-1>& operator[](size_t x) const
	{
		return mElems[x];
	}
	void resize(size_t newSize)	{
		mElems.reisze(newSize);
		for (auto& element : mElems) {
		    element.resize(newSize);
		}
	}
	size_t getSize() const { return mElems.size();}
	static const size_t kDefaultSize = 10;
private:
	std::vector<NDGrid<T, N-1> > mElems;
};

template <typename T>
class NDGrid<T,1>
{
public:
	explicit NDGrid(size_t inSize = kDefaultSize)
	{
		resize(inSize);
	}
	virtual ~NDGrid(){}
	T& operator[](size_t x)	{
		return mElems[x];
	}

	const T& operator[](size_t x) const	{
		return mElems[x];
	}
	void resize(size_t newSize)	{
		mElems.reisze(newSize);
	}
	size_t getSize() const { return mElems.size();}
	static const size_t kDefaultSize = 10;
private:
	std::vector<T> mElems;
};

### type inference(类型推导)与template结合

exp: in inference.h,声明函数模板

	#include <iostream>

	class MyString;

	class MyInt{
	public:
	    MyInt(int i) : mValue(i) {}
	    MyInt operator+(const MyString& rhs) const;
	    int getInt() const { return mValue; }
	private:
	    int mValue;
	};

	class MyString{
	public:
	    MyString(const std::string& str) :mString(str) {}
	    MyString operator+(const MyInt& rhs) const;
	    const std::string& getString() const { return mString; }
	private:
	    std::string mString;
	};

	template<typename T1, typename T2,typename Result>
	Result DoAddition(const T1& t1, const T2& t2)
	{
		return t1 + t2;
	}

	template<typename T1, typename T2>
	auto DoAdditionUpdate(const T1& t1, const T2& t2) -> decltype(t1 + t2)
	// C++14中 -> decltype(t1 + t2) 可省略
	{
		return t1 + t2;
	}

exp: in inference.cpp

    #include "test.h"
    #include <string>
    using namespace std;


    MyInt MyInt::operator+(const MyString& rhs) const {
       return mValue + stoi(rhs.getString());
    }

    MyString MyString::operator+(const MyInt& rhs) const {
    	std::string str = mString;
    	str.append(to_string(rhs.getInt()));
    	return str;
    }

    int main(){
        MyInt i(4);
        MyString str("5");
        // MyInt a = str + i;
        MyInt a = i + str;
        MyString b = str + i;

        cout << a.getInt() << " :ok: " << b.getString() << endl;

        auto c = DoAddition<MyInt, MyString, MyInt>(i, str);
        auto d = DoAdditionUpdate(i, str);
        auto e = DoAdditionUpdate(str, i);
        
        return 0;
    }

### 可变参数模板(...)

形式： template<typename T1, typename... Types>  // 类型未确定，可传入任意类型

exp: 以类型安全的方式，使用递归来获取每个参数

void handleValue(int val){ cout << "int: " << val << endl; }
void handleValue(string val){ cout << "string: " << val << endl; }
void handleValue(double val){ cout << "double: " << val << endl; }

// calls this while there's only one arg
template<typename T>
void processValues(T arg){
    handleValue(arg);
}

// 每次递归都会复制参数
template<typename T1, typename...Tn>
void processValues(T1 arg1, Tn... args)
{
    handleValue(arg1);
    processValues(args...);
}

// 改进为右值引用(字面量)传递参数
template<typename T>
void processValues(T&& arg){
    handleValue(std::forward<T>(arg));
}

template<typename T1, typename...Tn>
void processValues(T1&& arg1, Tn&&... args)
{
    int numOfArgs = sizeof...(args);
    cout << numOfArgs << endl;
    handleValue(std::forward<T1>(arg1));
    processValues(std::forward<Tn>(args)...);
}

exp: 普通混合类

    class Mix1{
    public:
        Mix1(int i=16) : mValue(i){}
        virtual void mix1func(){cout << "mix1: " << mValue << endl;}
    private:
        int mValue;
    };
    class Mix2{
    public:
        Mix2(int i=43) : mValue(i){}
        virtual void mix2func(){cout << "mix2: " << mValue << endl;}
    private:
        int mValue;
    };

    class MyClass : public Mix1, public Mix2
    {
    public:
        // 调用指定的父类默认构造函数
        // MyClass(const Mix1& mixin1, const Mix2& mixin2): Mix1(mixin1),Mix2(mixin2) {}
        MyClass(const Mix1& mixin1, const Mix2& mixin2) {}  // 调用父类的默认构造函数，或唯一显式声明的构造函数(且需设置默认值)
        virtual ~MyClass() {}
        void getmy(){cout << "my " << mValue;}
    private:
        int mValue;
    };
    int main(){
        MyClass a(Mix1(12), Mix2(33));
        a.mix1func();
        a.mix2func();
        a.getmy();

exp: 混合类

    class Mix1{
    public:
        Mix1(int i) : mValue(i){}
        virtual void mix1func(){cout << "mix1: " << mValue << endl;}
    private:
        int mValue;
    };
    class Mix2{
    public:
        Mix2(int i) : mValue(i){}
        virtual void mix2func(){cout << "mix2: " << mValue << endl;}
    private:
        int mValue;
    };

    template<typename... Mixes>
    class MyClass : public Mixes...
    {
    public:
        MyClass(const Mixes&... mixin): Mixes(mixin)... {}
        virtual ~MyClass() {}
    };
    int main(){
        MyClass<Mix1, Mix2> a(Mix1(12), Mix2(33));
        a.mix1func();
        a.mix2func();

        return 0;
    }

#### template meta programming(模板元编程)

目标：在编译时执行一些计算，而不是运行时执行。

exp:编译时阶乘 

    template<unsigned char f>
    class Factor
    {
    public:
        static const unsigned long long val = (f * Factor<f-1>::val);
    };
    template<>
    class Factor<0>
    {
    public:
        static cosnt unsigned long long val = 1;
    };

exp:编译时展开模板(通常不用)

    template<int i>
    class Loop
    {
    public:
        template<typename FuncType>
        static inline void Do(FuncType func){
            Loop<i-1>::Do(func);
            func(i);
        }
    };

    template<>
    class Loop<0>
    {
    public:
        template<typename FuncType>
        static inline void Do(FuncType /* func */) { }
    };
    void DoWork(int i) { cout << "Working: " << i << endl; }
    void DoWork2(string str, int i) { cout << str << " is Working: " << i << endl; }


    int main(){
        cout << Factor<6>::val << endl;  // 使用::val访问编译时的值

        Loop<5>::Do(DoWork);
        Loop<5>::Do(std::bind(DoWork2, "who", placeholders::_1));  // 使用bind设置多变量
        return 0;
    }

exp: tuple的编译

    #include <iostream>
    #include <string>
    #include <tuple>
    using namespace std;

    template<int n, typename TupleType>
    class Tuple_print{
    public:
        Tuple_print(const TupleType& t)  
        {  // 拷贝构造函数
            Tuple_print<n-1,TupleType> tp(t);
            cout << get<n-1>(t) << endl;
        }
    };
    template<typename TupleType>
    class Tuple_print<0, TupleType>
    {
    public:
        Tuple_print(const TupleType& /* arg */) {}
    };
    // 使用quick_print简化
    template<typename T>
    void quick_print(const T& t){
        Tuple_print<tuple_size<T>::value, T> tp(t);
    };

    int main(){
        using MyTuple = tuple<int, string, bool>;
        MyTuple t1(17,"Test", true);
        Tuple_print<tuple_size<MyTuple>::value, MyTuple> tp(t1);

        auto t2 = make_tuple("quick_test",125,false, 3.4);
        quick_print(t2);
        return 0;
    }

### 类型trait

在<type_traits>头文件中，用以判断类型特征
如is_void, is_integral, is_reference

exp: is_integral的定义及使用

    #include <iostream>
    #include <string>
    // using namespace std;会导致typedef integral_constant<bool, true> true_type;产生歧义

    template <class T, T v>
    struct integral_constant {
        static constexpr T value = v;
        typedef T value_type;
        typedef integral_constant<T,v> type;  // 创建integral_constant<type,arg>类型并保存,不能修改,integral_constant<type,arg>::type以调用此类型
        constexpr operator value_type() const noexcept {return value;}
        constexpr value_type operator()() const noexcept {return value;}
    };
    typedef integral_constant<bool, true> true_type;
    typedef integral_constant<bool, false> false_type;

    template<class T>
    struct is_integral :public false_type {};
    template<>
    struct is_integral<int> :public true_type{};
    template<>
    struct is_integral<bool> :public true_type{};
    // long,char等也继承true_type

    template<typename T>
    void process_helper(const T& t, true_type /*parameter*/)
    {
        std::cout << t << " is int" << std::endl;
    }

    template<typename T>
    void process_helper(const T& t, false_type)
    {
        std::cout << t << " is not int" << std::endl;
    }

    template<typename T>
    void process(const T& t)
    {
        process_helper(t, typename is_integral<T>::type());
    }


    int main(){
		typedef integral_constant<int, 5> int_type;
		int_type ff;
		std::cout << ff << std::endl;  // 调用operator value_type()
		std::cout << int_type::value << std::endl; 
		std::cout << ff() << std::endl;  // 调用operator()()

        process('a');
        if (is_integral<double>::value) {
            std::cout << "int val";
        } else {
            std::cout << "not int";
        }

        return 0;
    }


[injected-class-name](https://en.cppreference.com/w/cpp/language/injected-class-name) is the name of a class within the scope of said class.In a class scope, the name of the current class is treated as if it were a *public member name* and they're inherited

> NOTE:`operator something`,组成一个特殊函数

    operator+(param another);
    operator+=(param another);
    operator++();
    operator()(param another);
    
    param another = 3;
    int y;
    y = x + 3;
    x += 3;
    x ++;
    x(3);
    
> operator的特殊形式:operator someType()
作用:typeid(instance)依然为Cell类,但cout<< instance,instance+3(除了instace.val)等对instance调用的操作,都会调用operator someType(),并使用其返回值进行操作

    template<typename T>
    class Cell{
    public:
        operator int() { return 4;}  // 类型(此处为int)需与返回值匹配
        int val;
    };
    Cell instance;
    cout << instance;  // instance的值为4

#### 使用类型关系

is_same,is_base_of,is_convertible

#### enable_if
NOTE:替换失败不是错误(substitution failure is not an error,SFINAE)

exp:SFINAE

    #include <iostream>
    #include <string>
    #include <type_traits>
    using namespace std;

    template<typename T1, typename T2>
    // second param of enable_if is return type of check_type
    // and it will check
    typename enable_if<is_same<T1,T2>::value, bool>::type  
    check_type(const T1& t1, const T2& t2){
        cout << t1 << " and " << t2 
        << " have the same type" << endl;
        return true;
    }
    template<typename T1, typename T2>
    typename enable_if<!is_same<T1,T2>::value, bool>::type  
    check_type(const T1& t1, const T2& t2){
        cout << t1 << " and " << t2 
        << " are different types" << endl;
        return False;
    }

    int main(){
        check_type(1,32); 
        check_type(1,32.5); 
        return 0;
    }

compiler process of `check_type(1,32.5);`(mechanism)

1. compiler寻找接受int,double的check_type(),未果
1. compilter寻找第一个check_type()函数模板重载,
1. 将T1设为int,T2设为double
1. compiler尝试确定返回类型,调用typename enable_if<is_same<T1,T2>::value, bool>::type
1. is_same<T1,T2>::value返回False,enable_if<false,bool>::type失败/编译错误
1. *SFINAE*起效，编译器先不报错，而是尝试替换
1. compiler回溯并尝试找到另一个check_Type()
1. 尝试确定返回值类型，调用typename enable_if<!is_same<T1,T2>::value, bool>::type
1. !is_same<T1,T2>::value return True, enable_if<false,bool>::type编译成功

enable_if用于构造函数，需将第二个参数设为void
enable_if仅在解析重载歧义时使用(如memcpy(),使用enable_if和trivially_copyable),即无法用特例化，部分特例化等解析重载歧义时使用。

NOTE:使用SFINAE和enable_if禁用重载集中的错误重载，会得到奇怪的编译错误

### SUMMARY of template meta programming

一切发生在编译时，不能通过调试器定位问题，需要添加准确的注释

# 内存管理

内存泄漏/孤立:堆中的数据块无法从栈中直接或间接访问

new vs malloc(), delete vs free()

new不仅分配内存(同malloc),还构建对象(malloc不会)
free()不调用对象的析构函数，只是说myFoo指向的空间不再被占据

class Foo{};
Foo* myFoo = (Foo*)malloc(sizeof(Foo));  // 只分配内存空间，并强制转换类型，可访问成员，但未调用构造函数，不会初始化成员
Foo* myOtherFoo = new Foo();  // 调用构造函数

NOTE:C++不使用malloc(),free(),realloc()

多维数组

若在栈中，char board[3][3],实际上分配了连续的内存

若在堆中,可先定义函数board,board[3][4],
先为board[0],board[1],board[2]分配连续内存,
再为它们各自指向自身的board[n][0],board[n][1],board[n][2],board[n][3]分配连续内存

char** board(size_t x, size_t y)
{
    char** myArray = new char*[x];
    for (size_t i = 0; i < x; i++){
        myArray[i] new char[y];
    }
    return myArray;
}

数组通常可与指针互换:these three function declarations are equal,可接受栈或堆数组

    void doubleInts(int* theArray, size_t innerSize);
    void doubleInts(int theArray[], size_t innerSize);
    void doubleInts(int theArray[3], size_t innerSize);

> C++ Standard §8.3.2/4:
There shall be no references to references, no arrays of references, and no pointers to references.

此行只能接受栈数组，因为栈数组theArray类型为int (&) [4],对stackArray"引用"; 而堆数组heapArray类型则为int\*,引用指针不被允许

    void doubleInts(int (&theArray) [4]);

此代码无法运行，heapArray只是指针类型，但换成stackArray即可运行
	for (auto elem : heapArray) {
		cout << elem << endl;
	}

### 底层内存操作

1. 指针的+-操作

int* ar = new int[8];
ar[2] = 33;
*(myArray + 2) = 33;

2. 自定义内存管理

(mechanism)使用new，程序预留少量空间记录分配了多少内存，确保delete正确释放，
很小的对象或分配大量对象的程序，这部分开销就会比较大

自行管理可事先知道对象大小，避免此开销

3. 垃圾回收
(mechanism)支持垃圾回收的环境(如java,但C++没有),运行时库会自动清理无引用的对象，

垃圾回收的方法，标记和清扫：垃圾回收器定期检查程序中的每个指针，并将其指向的内存标记为仍在使用。必须一轮检查结束(所有都检查了)后，才会将无标记内存回收。
  - 垃圾回收器注册所有指针
  - 所有对象都从一个混入类(如GarbageCollectible)中派生,就可标记对象为使用中
  - 确保垃圾回收器运行时不能修改指针，从而保护对象的并发访问

垃圾回收的缺点：
  - 垃圾回收器运行时，程序可能停止响应
  - 垃圾回收器运行时，析构函数具有不确定性。对象在垃圾回收前不被销毁，所以对象离开作用域时不再立即执行析构函数(而是等待垃圾回收器调用析构函数),那么清理资源的操作(如关闭文件，释放锁)等的时间不确定

### 对象池(C++使用对象池而不使用垃圾回收)

对象使用完成后立即清理，用于使用大量同类型对象，且它们产生开销时。

### 函数指针

优点：可根据实际需要传入不同的函数
Bad command or file name

### 成员/方法指针

指向成员的指针，不能访问非静态成员，或在没对象的情况下调用非静态方法。
指针访问成员/方法，需在对象的上下文中，解除对指针的引用

exp: 如果调用方法指针(一般不会用到)

    #include <iostream>
	using namespace std;

	class Cell{
	public:
		Cell(int val):mVal(val){}
		double getValue(int s) const {return s+mVal+3.14;}
		int mVal;
	};
	// phase 1
	int main(){
		Cell myCell(124);
        // 上下文中解除引用
		double (Cell::*ptr) (int s) const = &Cell::getValue;  // 不像普通函数指针,方法指针必须使用&
        // 通过对象调用非静态方法
		cout << (myCell.*ptr)(31) << endl;

		return 0;
	}
	// phase 2
	int main(){
		Cell myCell(124);
		using MethPtr = double (Cell::*) (int s) const 
		MethPtr ptr = &Cell::getValue;  // 不像普通函数指针,这里必须使用&
		cout << (myCell.*ptr)(31) << endl;

		return 0;
	}
	// phase 3
	int main(){
		Cell myCell(124);
		using MethPtr = double (Cell::*) (int s) const 
		auto ptr = &Cell::getValue;  // 不像普通函数指针,这里必须使用&
		cout << (myCell.*ptr)(31) << endl;

		return 0;
	}

### 智能指针

对象间可能传递多个指针，但普通指针(动态分配内存)只能在正确的时间执行一次delete操作。delete会删除内存中的值，变为随机值。
- 错误的时间执行delete可能会删除还有用的数据
- 多次执行delete会删除已被分配给其他对象的内存数据
- 忘记执行delete则会导致内存泄漏

智能指针：所有内容放在栈上，变量离开作用域自动销毁

auto_ptr:禁止使用(最大缺陷:容器中不能工作)
unique_ptr:(仅支持移动语义)对内存有唯一所有权，离开作用域(函数末尾或抛出异常时)即销毁
shared_ptr:共享资源时，指针有多个副本(aliasing)，应由最后的副本由底层的普通指针调用delete。通过添加了引用计数器实现此功能。

exp: 使用unique_ptr的移动语义，无move()报错

    auto p1 = make_unique<int>(42);
    unique_ptr<int> p3 = move(p1);

经验：总将动态分配的对象保存在堆栈中的unique_ptr实例中

动态分配一个Cell对象的2种方法
- auto smart = make_unique<Cell>();  // 总是推荐使用make_unique
- unique_ptr<Cell> smart(new Cell());

auto dynamicArray = make_unique<int[]>(10);

exp: 自定义new/delete行为，利用此特性可管理其他类型的资源而不仅是内存

    #include <iostream>
    using namespace std;
    
    int* malloc_int(int value)
    {
    	int* p = (int*)malloc(sizeof(int));
    	*p = value;
    	return p;
    }
    int main(){
    	auto deleter = [](int* p){ free(p);}; // a lambda expression
    	unique_ptr<int, decltype(deleter)> smart(malloc_int(42), deleter);
    	return 0;
    }

exp: shared_ptr自动关闭文件

    #include <iostream>
	#include <memory>
	using namespace std;

	void closeF(FILE* filePtr){
		cout << "runs whether f opens or fails" << endl;
		if (filePtr == nullptr) return;
		fclose(filePtr);
		cout << "file closed in the end" << endl;
	}

	int main(){
		FILE* f = fopen("data.txt", "r");  // a,w modes create file if not exist
		shared_ptr<FILE> filePtr(f, closeF);
		if (filePtr == nullptr) {
			cout << "closed"  << endl;
		} else { cout << "opened"  << endl;}
		return 0;
	}

exp: double delete (双重删除的错误)

    void doubleDelete(){
        // 删除此对象2次
        Nothing* myNothing = new Nothing();
        shared_ptr<Nothing> smartPt1(myNothing);
        shared_ptr<Nothing> smartPt2(myNothing);
    }
    
    void noDoubleDelete(){
        auto smartPt1 = make_shared<Nothing>();
        // 复制构造函数建立副本
        shared_prt<Nothing> smartPt2(smartPt1);
    }

weak_ptr:包含由shared_ptr管理的内存引用，离开作用域不销毁指向的内存，但可用于判断内存是否被关联的shared_ptr释放。
TODO: look for more detail about weak_ptr

### 常见内存问题

1. 分配不足的字符串(C中)：没有分配尾部的`\0`哨兵字符,即会超过字符串结尾，而写入未分配的内存
2. 访问内存越界(C中)：丢失`\0`中止字符
3. 内存泄漏(C与C++)：在释放内存前，失去内存引用

检测内存工具：

1. 使用in visual C++，在文件开头添加以下代码

#define _CRTDBG_MAP_ALLOC
#include <cstdlib>
#include <crtdbg.h>

#ifdef _DEBUG  // 仅调试时/debug时用新的new
    #ifndef DBG_NEW
        #define DBG_NEW new ( _NORMAL_BLOCK, __FILE__, __LINE__)
        #define new DBG_NEW
    #endif
#endif

int main(){
    // 在main中开头添加
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);

    // 先调试时出现错误，返回 如{147}，表示第147次分配的内存未释放，再添加以下代码到main()开头
    _CetSetBreakAlloc(147);
}

2. 使用linux:valgrind





















# 多线程

存在问题:
- 竞争:抢夺共有资源因而未按预定顺序执行操作
- 死锁:线程1锁定A,同时线程2锁定B,然后线程1要获取B,同时线程2要获取A
- 撕裂:仅部分数据已写入内存，另一线程读取，获取不到需要的完整数据
- 缓存的一致性:由于cpu的缓存结构存在，一个核心修改了数据，它的缓存like改变，但不会立即同步到使用另一缓存的核心

exp:通过函数创建线程,传入函数及其参数(长度可变)

    #include <iostream>
    #include <thread>
    using namespace std;
    int main(){
    	thread t1([](int s){cout << "tt" << endl;}, 33);
    	thread t2([](double s, int r){cout << "kkkk" << endl;}, 3.2,4);
        // 使用join阻塞主线程，直到t1,t2执行结束，不推荐
    	t1.join();
    	t2.join();
    	return 0;
    }

通过函数对象创建线程,重载operator()(),建议使用{}创建实例:thread t3(Ct{1,3})

NOTE:函数对象总是复制到线程的某个内部存储中，<functional>的thread t3(std::ref(instance))来引用而阻止复制

exp: 通过成员函数创建线程，传入成员函数和实例对象(如此可传入不同实例调用同一方法)

    #include <iostream>
    #include <thread>
    using namespace std;
    
    class Request{
    public:
    	Request(int id):mId(id){}
    	void process(){
    		cout << "process: " << mId << endl;
    	}
    private:
    	int mId;
    };
    
    int main(){
    	Request req(100);
    	thread t1{ &Request::process, &req};
    	t1.join();
    	return 0;
    }

### thread_local(线程本地存储)

线程本地数据(变量):每个线程都有这个变量的独立副本(仅初始化一次)，变量在线程整个生命周期中持续存在
// k唯一，被所有线程共享，n则是每个线程都创建一个n的副本
thread_local int n;
int k;
// thread_local在函数作用域中声明，行为和静态变量相同

取消线程：标准没有一个线程直接取消另一个线程的机制
为2个线程提供某种通信机制，(如共享变量),目标线程定期检查变量，判断是否终止，其他线程可设置这个共享变量

### 多线程异常

异常只在线程内被捕捉，其他线程无法捕获

<exception>定义了:

    exception_ptr current_exception() noexcept;
    
    template<class E>
    exception_ptr make_exception_ptr(E e) noexcept;
    等价于
    try {
        throw e;
    } catch(...) {
        return current_exception();
    }
    
    [[noreturn]] void rethrow_exception(exception_ptr p);

exp: 捕捉内部线程的exception

    #include <iostream>
	#include <thread>
	#include <functional>
	#include <exception>
	using namespace std;

	void doSome(){
		for (int i = 0; i < 5; ++i) {
			cout << i << endl;
		}
		cout << "ex" << endl;
		throw runtime_error("exception");
	}

	void cat(exception_ptr& err){
		try {
			doSome();
		} catch (...) {
			cout << "exp caught" << endl;
            // 若有错误，则返回的err不为空，主线程就可进行处理
			err = current_exception();
		}
	}

	void workThread() {
		exception_ptr error;
		thread t{ cat, ref(error)};
		t.join();
		if (error) {
			cout << "main thread caught exception" << endl;
            // 捕捉到错误，重新抛出异常
			rethrow_exception(error);
		} else {
			cout << "main thread got no exception" << endl;
		}
	}


	int main(){
		try {
			workThread();
		} catch (const exception& e) {
			cout << "main func caught: " << e.what() << endl;
		}
		return 0;
	}

### 原子操作库

    
原子类型允许原子访问，不需额外的同步机制就可执行并发的读写操作。
解决缓存一致性，内存排序，编译器优化等问题

#include <atomic>
atomic<int> counter(0);
++counter;

exp: 非原子操作引起问题，缓存未同步，部分++counter使用了旧缓存

    #include <iostream>
	#include <thread>
	#include <vector>

	using namespace std;

	void func(int& counter)
	{
		for (int i = 0; i< 100;++i){
			++counter;
			std::this_thread::sleep_for(std::chrono::milliseconds(1));
		}
	}

	int main(){
		int counter = 0;
		std::vector<std::thread> threads;
		for (int i = 0; i < 10; ++i) {
			threads.push_back(std::thread { func, std::ref(counter)});
		}
		for (auto& t : threads) {
			t.join();
		}
		std::cout << "Result=" << counter << std::endl;
		return 0;
	}

### 原子操作

bool atomic_compare_exchange_strong(atomic<C>* object, C* expected, C desired);
bool atomic<C>::compare_exchange_strong(C* expected, C desired);
if (*object == *expected) {
    *object = desired;
    return true;
} else {
    *expected = *object;
    return false;
}

支持+=,fetch_add,++等，不支持=,-
atomic<int> value(10);
cout << "Value = " << value << endl;
int fetched = value.fetch_add(4,memory_order=memory_order_seq_cst);
cout << "Fetched = " << fetched << endl;
cout << "Value = " << value << endl;

### 互斥

形式：
- mutex(互斥体)类，分定时（阻塞直到预定时间）和不定时（可能始终阻塞）
- lock(锁)类

### std::call_once

exp: std::call_once(),std::once_flag确保函数只调用一次，其他线程都阻塞直到此函数运行完成
    // template<typename _Callable, typename... _Args>
    // void call_once(once_flag& __once, _Callable&& __f, _Args&&... __args);
    #include <iostream>
    #include <thread>
    #include <vector>
    #include <mutex>
    using namespace std;
    
    once_flag flg;
    void initShared(){
    	cout << "initialize only once " << endl;
    }
    void processingFunc(){
    	call_once(flg, initShared);
    	cout << "processing" << endl;
    }
    
    int main(){
    	std::vector<thread> threads(3);
    	for (auto& t : threads) {
    		t = thread{processingFunc};
    	}
    	for (auto& t : threads) {
    		t.join();
    	}
    	return 0;
    }

exp: 几种锁定方式

    // 不定时锁
    class Counter{
    public:
    	Counter(int id, int iterTimes)
    	:mId(id),mIterTimes(iterTimes){}
    	void operator()() const {
    		for (int i = 0; i < mIterTimes; ++i) {
    			// 每次创建lock_guard<mutex>类的实例，获得mMutex上的锁
    			// 确保同时只有一个线程读写流对象
    			lock_guard<mutex> lock(mMutex);
    			cout << "Counter " << mId << " is " << i << endl;
    		}
    	}
    private:
    	int mId;
    	int mIterTimes;
    	static mutex mMutex;
    };
    mutex Counter::mMutex;

    // 定时锁
    class Counter{
    public:
        Counter(int id, int iterTimes)
        :mId(id),mIterTimes(iterTimes){}
        void operator()() const {
            for (int i = 0; i < mIterTimes; ++i) {
                // 每次创建lock_guard<mutex>类的实例，获得mMutex上的锁
                // 确保同时只有一个线程读写流对象
                unique_lock<timed_mutex> lock(mTimedMutex,std::chrono::milliseconds(200));
                if (lock) {
                    cout << "Counter " << mId << " is " << i << endl;
                } else {}
            }
        }
    private:
        int mId;
        int mIterTimes;
        static timed_mutex mTimedMutex;
    };
    timed_mutex Counter::mTimedMutex;

双重检查锁定：确保变量初始化一次，获得锁前和后都检查initialized变量值，共2次。
第一次检查防止获得不需要的锁，提升性能，
第二次检查确保没有其他线程在第一次initialized检查和获得锁之间执行初始化

    #include <iostream>
    #include <thread>
    #include <vector>
    #include <mutex>
    #include <atomic>
    using namespace std;
    void initShared(){
    	cout << "initialize only once " << endl;
    }
    atomic<bool> initialized(false);
    mutex mut;
    void func(){
    	if (!initialized) {
        // 第一次检查，创建锁
    		unique_lock<mutex> lock(mut);
    		if (!initialized) {
            // 第二次检查，initialized依然为false，负责说明有其他线程已经执行了initialized=true;
    			initShared();
    			initialized = true;
    		}
    	}
    	// something multi thread will do
    	cout << "OK" << endl;
    }
    int main(){
    	std::vector<thread> threads(3);
    	for (auto& t : threads) {
    		t = thread{func};
    	}
    	for (auto& t : threads) {
    		t.join();
    	}
    	return 0;
    }

### 变量条件 (在<condition_cariable>头文件中)

std::condition_variable 只能等待unique_lock<mutex>的条件变量
std::condition_variable 可等待任何对象的条件变量，包括自定义锁

支持的方法：
notify_one() 唤醒一个等待此条件变量的线程，类似windows的auto-rest
notify_all() 唤醒等待此条件变量的所有线程
wait(unique_lock<mutex>& lk)

exp: 使用条件变量

    #include <iostream>
	#include <thread>
	#include <queue>
	#include <vector>
	#include <mutex>
	#include <atomic>
	#include <fstream>
	#include <sstream>
	#include <atomic>
	#include <condition_variable>
	using namespace std;

	class Logger{
	public:
		Logger();
		virtual ~Logger();
		Logger(const Logger& src) = delete;
		Logger& operator=(const Logger& rhs) = delete;
		void log(const std::string& entry);

	private:
		std::atomic<bool> mExit;
		void processEntries();
		std::mutex mMutex;
		std::condition_variable mCondVar;
		std::queue<std::string> mQueue;
		std::thread mThread;
	};

	Logger::Logger() : mExit(false) {
		mThread = thread{ &Logger::processEntries, this};
	}
	Logger::~Logger(){
		{
			unique_lock<mutex> lock(mMutex);
			mExit= true;
			mCondVar.notify_all();
		}
		mThread.join();
	}
	void Logger::log(const std::string& entry){
		unique_lock<mutex> lock(mMutex);
		mQueue.push(entry);
		mCondVar.notify_all();
	}
	void Logger::processEntries(){
		ofstream ofs("log.txt");
		if (ofs.fail()){
			cerr << "fail to open" << endl;
			return;
		}
		unique_lock<mutex> lock(mMutex);
		while (true) {
			std::this_thread::sleep_for(std::chrono::milliseconds(1000));
			if (!mExit) mCondVar.wait(lock);
			lock.unlock();
			while (true){
				lock.lock();
				if (mQueue.empty()){
					break;
				} else {
					ofs << mQueue.front() << endl;
					mQueue.pop();
				}
				lock.unlock();
			}
			if (mExit){
				break;
			}
		}
	}

	void logMessage(int id, Logger& logger) {
		for (int i=0; i < 10; ++i) {
			stringstream ss;
			ss << "log entry " << i << " from thread" << id;
			logger.log(ss.str());
		}
	}

	int main(){
		Logger logger;
		std::vector<thread> threads;
		for (int i=0; i < 10; ++i) {
			threads.emplace_back(logMessage, i, ref(logger));
		}
		for (auto& t : threads) {
				t.join();
		}
		cout << "over";
		return 0;
	}

### 线程池

不动态创建和删除线程，程序预先创建好一定数量的线程，可用如Intel Threading Building Blocks(TBB),Microsoft Parallel Patterns(PPL)库等实现。

## 线程总结

终止程序前，使用join()等待后台线程执行完毕：确保后台线程都有时间进行清理(析构)，避免主线程终止时后台线程也终止
最好没有同步：应当使线程使用共享数据时只能读取，没有写入，或者只写入其他线程不读取的部分
使用单线程的所有权模式：同一时间拥有一个数据块的线程为1，阻止其他线程读写，处理完成后在交给其他线程
使用原子类型和操作：能自动处理同步，不用处理死锁和竞争条件。
使用锁保护可变的共享数据：不能使用原子类型时使用
尽快释放锁
确保按统一顺序获得多个锁：所有线程以同样顺序获得多个锁，可避免死锁
使用支持多线程的分析器：分析性能瓶颈
了解调试器的多线程支持特性：需要能得到程序中运行的线程列表，并查看线程的调用栈
使用线程池：动态创建/销毁线程会导致性能下降
使用高级多线程库：TBB，PPL


# 软件开发过程

## 生命周期模型

分段模型(stagewise model):按步骤构建
规划->设计->实现->单元测试->子系统测试->整合测试->评估
缺点：实际无法完全分离

瀑布模型（waterfall model）（从分段模型改进）：将以上分段模型的箭头改为双向<->
优点：简洁，易于管理。规划是详尽列出所有不需的功能，后续可顺利进行
缺点：不允许大步后退，不够动态。前期设计可能隐藏了巨大风险，导致发现时已晚，难以修正

螺旋模型（spiral model，1988）：风险驱动
基本思想：出错也没关系，下一轮修复。4个步骤迭代
开发->分析->发现->评估->开发->分析->发现->评估->开发->分析->发现->评估
开发：产生规划，包含产品的主要需求
分析：得到战士用户体验的原型
发现：构建一个呗认定是高风险的组件
特点：重视在评估阶段中风险的评估和解决

优点：解决了瀑布模型的隐藏风险问题与难以回溯的问题
缺点：难以将每次迭代的范围界定的足够小，以获得真正的好处。且迭代次数过多就会退化为瀑布模型。
多次迭代增加开销，不同周期协调困难（各团队开发周期不同步）

rational unified process:是一个软件产品，而不仅是理论的过程模型

- 过程本身和软件一样更新和完善
- 提出开发框架及使用此框架的软件工具
- 可部署在整个团队，要求所有成员使用相同的过程和工具
- 可以定制，以满足用户的需求

原则：开发周期每次迭代应有一个有形的成果，过程中，用户创建很多设计，需求文档报告和计划
核心原则：定义精确模型，同一件欧美语言(UML)进行格式描述

## 软件工程方法学
[敏捷(agile methodology)](heep://agilemanifesto.org/):灵活地加入新需求
Scrum：指导了敏捷的实现
Scrum迭代周期称为sprint(为期2-4星期)，每个sprint周期结束，目标是有完全可用且经过测试的版本。并提供给客户，让其反馈

### 角色
PO(product owner):根据用户的描述编写多个高层次的用户需求，并设置其优先级，置入scum的产品需求总表。PO可以决定要留下/实现哪些
SM(Scrum Master)负责过程运行，但不能是团队领导，联络各团队，确保团队正确遵循Scrum过程
Group团队本身：团队最好不要多于10人

### 过程：
强制每日例会(需少于15分钟),每个成员回答：
- 昨天到今天做了什么
- 今天准备做什么
- 要做这个会遇到哪些问题，SM需注意这些问题

每个sprint周期前开会：
决定需事先什么产品特性，记录在sprint需求总表中，直到此周期结束

每个sprint周期后开会：
确定已完成，未完成及原因，使用demo展示成果

Billboard:To do, In progress, Done

Scrum优点：弹性处理不可预知的问题
缺点：
- 成员从billboard自行挑选任务，而不是通过经理或团队管理者分配
- SM对团队的信任非常重要，不能过紧
- 特性蠕动(feature creep),新特性过多，必须制定最终日期

### 极限编程(extreme programming, 1999)

编写代码前编写自动化测试

特点：
最初粗略计划，然后随时计划
2个月（而不是18个月）发布小版本，而不发布设计核心变化和大量发布说明文档的大版本。最终只有最重要的功能进入产品
metaphor:所有尘缘对系统有共同的高层次看法（系统组件的心理模型），用隐喻推进共享的词汇表。
简化设计：避免任意的通用性。修改等到以后
不断测试，单元测试是一小块代码，确保独立的功能正常工作。测试足够完善，所有测试都能通过
必要时重构：识别准备好重构的代码的迹象
结对编程：2人同时编写，一人编写，一人(可能是已有开发软件专精者)思考高层次的方法（如测试，必要的重构和项目整体模型等）
共享代码：集体都对代码有所认识
不断整合：频繁地整合及测试
正常工作的小时数：确保清醒的头脑
客户在场：由于值构建当前必要的功能，客户可提供有价值的建议与沟通，并让开发者迅速开发成型
共同的编码标准：不能有人明显不同的编码标准

### 软件分流(software triage,2003)

项目处于极其糟糕的状态：将剩下的功能组织为`必须有`,`应该有`,`可以有`的列表，以保证按时完成项目

### 构建自己的过程和方法

项目结束后进行评估，其中是否有重大问题。考虑什么方法行得通，什么行不通
建立代码审查的技术，如只审查接口

不要逃避问题

# 高效的C++

高效率：尽快完成指定任务，而非无用功

提升效率：1. 按引用传递。2.设计层次的效率，如高效的算法，避免不需要的步骤

普通程序（非计算密集型，非实时游戏，非系统级软件，非嵌入式系统），不用时间做优化

语言的效率：语言的性能，编译器优化

NOTE:应当仅优化分析器标记为性能瓶颈的部分

### 高效地操纵对象
- 按引用传递
- 按引用返回（但不能返回局部对象的引用，此时使用移动语义）
- 按引用捕捉异常
- 使用移动语义
- 避免创建临时的无名对象：代码需要在较大的表达式中将一个类型的变量转化为另一类型时，编译器都会构造临时对象。主要适用于函数调用，即传入的实参类型与形参(可能是一个类对象)不同，就会将实参强制转换。有事不可避免，但是要记得这个开销
- 返回值优化：通过值返回对象的函数可能会创建一个临时对象，即调用此函数但不将其赋值给变量。通常编译器会优化它。仅在发布版本中启用。
- 使用内联方法和函数，标记为inline，编译器也会自动优化部分

### 设计层次的效率
- 选择优秀的算法，数据结构（STL，Boost库），融入多线程
- 尽可能多的缓存:
  - 磁盘访问：避免多次打开读取同一文件。应尽量将内容保存在内存中
  - 网络通信：当成文件访问，尽可能缓存静态信息
  - 数学计算：复杂计算结果，尽量只执行一次计算并共享。不复杂，进行计算可能比从缓存中提取更快（使用分析器分析）。
  - 对象分配：程序需要大量创建和使用短期对象，使用对象池
  - 线程创建：将线程缓存在线程池中
- 缓存失效：
保存的数据往往是底层信息的一个副本，在缓存的生命周期中，原始数据可能发生变化（如获取缓存配置文件中的值，但配置文件被修改）。`缓存失效机制`，确保停止使用缓存的信息并读取新信息填入缓存。
实现缓存失效：要求管理底层数据的实体通吃程序数据变化。通过程序在管理器中注册一个回调实现。程序可轮询某些出发自动重新填充缓存的时间。
NOTE：维护缓存需要编码，内存，处理时间。可能会产生难以查找的bug，因此仅在分析器清晰地说明性能瓶颈的部分添加缓存。

### 对象池

大量同类型的短期对象，构造函数的开销很大。这些对象的内存分配和释放是瓶颈。
对象池值创建一次对象，因此对象的构造函数只调用一次
适用：构造函数需要为很多对象进行一些设置操作的情况。通过构造函数外的方法调用为对象设置一些实例特有的参数

exp: 创建对象池
    #include <cstddef>
    #include <queue>
    #include <stdexcept>
    #include <memory>
    
    using namespace std;
    
    template <typename T>
    class ObjectPool
    {
    public:
        ObjectPool(size_t chunkSize = kDefaultChunkSize);
        ObjectPool(const ObjectPool<T>& src) = delete;
        ObjectPool<T>& operator=(const ObjectPool<T>& rhs) = delete;
        using Object = std::shared_ptr<T>;
        Object acquireObject();
    
    private:
        std::queue<std::unique_ptr<T> > mFreeList;
        size_t mChunkSize;
        static const size_t kDefaultChunkSize = 10;
        void allocateChunk();
    };
    
    template <typename T>
    ObjectPool<T>::ObjectPool(size_t chunkSize)
    {
        if (chunkSize <= 0) {
            throw std::invalid_argument("chunk size must be positive");
        }
        mChunkSize = chunkSize;
        allocateChunk();
    }
    template <typename T>
    void ObjectPool<T>::allocateChunk()
    {
        for (size_t i = 0; i < mChunkSize; ++i) {
            // create pointer
            mFreeList.emplace(std::make_unique<T>());
        }
    }
    template <typename T>
    // typename ObjectPool<T>::Object declares that Object is a type
    typename ObjectPool<T>::Object ObjectPool<T>::acquireObject()
    {
        if (mFreeList.empty()) {
            allocateChunk();
        }
        // create pointer named obj from freelist
        std::unique_ptr<T> obj(std::move(mFreeList.front()));
        mFreeList.pop();
        // now in namespace ObjectPool<T>::,use Object directely
        Object smartObject(obj.release(),
                           [this](T* t) {
                               mFreeList.push(std::unique_ptr<T>(t));
                           }
        );
        return smartObject;
    }
    
    class UserRequest{
    public:
        UserRequest() {}
        virtual ~UserRequest() {}
    private:
        // not shown
    };
    
    ObjectPool<UserRequest>::Object obtainUserRequest(ObjectPool<UserRequest>& pool){
        auto request = pool.acquireObject();
        return request;
    }
    void processUserRequest(ObjectPool<UserRequest>::Object& req)
    {
        req.reset();
    }
    
    int main()
    {
        ObjectPool<UserRequest> requestPool(10);
        for (size_t i = 0; i < 100; ++i) {
            auto req = obtainUserRequest(requestPool);
            processUserRequest(req);
        }
        return 0;
    }
       



### 90/10法则
> 大部分程序90%的时间执行10%的代码，优化90%的代码，程序运行只改进10%。需要优化在典型负载下程序运行最多的代码

### 性能剖析器
fee
rational purifyplus(from IBM)
free
on windows:very sleepy,luke stackwalker,vc++
on linux: valgrind,gprof

exp: a database

    // NamBD.h
    #include <string>
	#include <vector>
	#include <utility>

	class NameDB{
	public:
		NameDB(const std::string& nameFile);
		int getNameRank(const std::string& name) const;
		int getAbsoluteNumber(const std::string& name) const;
	private:
		std::vector<std::pair<std::string,int> >mNames;
		bool nameExists(const std::string& name) const;
		void incrementNameCount(const std::string& name);
		void addNewName(const std::string& name);
	};

	#include <iostream>
	#include <fstream>
	using namespace std;

	NameDB::NameDB(const string& nameFile)
	{
		ifstream inFile(nameFile.c_str());
		if (!inFile) {
			throw invalid_argument("Unable to open file");
		}
		string name;
		while (inFile >> name) {
			if (nameExists(name)) {
				incrementNameCount(name);
			} else {
				addNewName(name);
			}
		}
		inFile.close();
	}

	int NameDB::getNameRank(const std::string& name) const
	{
		int num = getAbsoluteNumber(name);
		if (num == -1) {
			return -1;
		}
		int rank = 1;
		for (auto& entry : mNames) {
			if (entry.second > num) {
				rank++;
			}
		}
		return rank;
	}

	int NameDB::getAbsoluteNumber(const std::string& name) const
	{
		for (auto& entry : mNames) {
			if (entry.first == name) {
				return entry.second;
			}
		}
		return -1;
	}


	// private
	bool NameDB::nameExists(const std::string& name) const
	{
		for (auto& entry : mNames) {
			if (entry.first == name) {
				return true;
			}
		}
		return false;
	}
	void NameDB::incrementNameCount(const std::string& name)
	{
		for (auto& entry : mNames) {
			if (entry.first == name) {
				entry.second++;
				return;
			}
		}
	}
	void NameDB::addNewName(const std::string& name)
	{
		mNames.push_back(make_pair(name, 1));
	}


    NameDBtest.h
    #include "NameDB.h"
    #include <iostream>
	int main()
	{
		NameDB boys("boys_long.txt");
		cout << boys.getNameRank("Daniel") << endl;
		cout << boys.getAbsoluteNumber("Jacob") << endl;
		cout << boys.getNameRank("William") << endl;
		return 0;
	}

use gprof:

1. gcc -lstdc++ -std=c++11 -pg -o NameDB.cpp NameDBtest.cpp
1. 运行程序，生成gmon.out
1. gprof namedb gmon.out > gprof_analysis.out  // 输出重定向到文件

exp: after improvement

    #include <string>
	#include <map>

	class NameDB{
	public:
		NameDB(const std::string& nameFile);
		int getNameRank(const std::string& name) const;
		int getAbsoluteNumber(const std::string& name) const;
	private:
		std::map<std::string, int> mNames;
		bool nameExistsAndIncrement(const std::string& name);
		void addNewName(const std::string& name);
	};

	#include <iostream>
	#include <fstream>
	using namespace std;

	NameDB::NameDB(const string& nameFile)
	{
		ifstream inFile(nameFile.c_str());
		if (!inFile) {
			throw invalid_argument("Unable to open file");
		}
		string name;
		while (inFile >> name) {
			if (!nameExistsAndIncrement(name)) {
				addNewName(name);
			}
		}
		inFile.close();
	}

	int NameDB::getNameRank(const std::string& name) const
	{
		int num = getAbsoluteNumber(name);
		if (num == -1) {
			return -1;
		}
		int rank = 1;
		for (auto& entry : mNames) {
			if (entry.second > num) {
				rank++;
			}
		}
		return rank;
	}

	int NameDB::getAbsoluteNumber(const std::string& name) const
	{
		auto res = mNames.find(name);
		if (res != end(mNames)) {
			return res->second;
		}
		return -1;
	}

	// private
	bool NameDB::nameExistsAndIncrement(const std::string& name)
	{
		auto res = mNames.find(name);
		if (res != end(mNames)) {
			res->second++;
			return true;
		}
		return false;
	}

	void NameDB::addNewName(const std::string& name)
	{
		mNames[name] = 1;
	}


	int main()
	{
		NameDB boys("boys_long.txt");
		cout << boys.getNameRank("Daniel") << endl;
		cout << boys.getAbsoluteNumber("Jacob") << endl;
		cout << boys.getNameRank("William") << endl;
		return 0;
	}

exp: more improvement

// delete nameExistsAndIncrement and addNewname methods.

while(inFile >> name) {
    auto res = mNames.insert(make_pair(name,1));
    if (res.second == false) {
        res.first->second++;
    }
}

## 调试

1.调试基本定律
要为bug的出现制定好规划

2.bug分类学
灾难性bug
非灾难性bug
cosmetic bug(图形界面显示错误但造作无问题)

3.避免bug
指针和内存管理
编码前设计
(请他人)代码审查
全面测试，再请他人测试
编写自动测试。所有已实现的特性编写单元测试
预计错误条件并处理：规划和处理内存不足的情况
使用智能指针
配置编译器，用较高的警告级别编译
使用静态的代码分析器分析源代码
提高可读性，添加代码注释，使用override关键字

### logging
syslog(form unix),Boost.Log

应当记录的错误
1.不可恢复的错误，如无法分配内存或系统调用失败
2.管理员可采取行动的错误，如内存不足，数据文件格式有误，不能写入磁盘或网络连接关闭
3.意外的错误，没有预计到的代码路径或变量取了意料外的值（如用户输入非法数据时）
4.潜在的安全漏洞，例如网络连接试图访问未经授权的地址，或太多的网络连接尝试（拒绝服务）

调试跟踪(trace)的辅助有效信息
线程ID（多线程）
生成跟踪信息的函数名
生成跟踪信息的代码所在的源文件名称

1.调试模式
启动时调试模式：添加命令行参数，但需要重新启动

exp: log debug

    #include <iostream>
    #include <cstring>
    #include <fstream>
    using namespace std;

    class Logger
    {
    // create logger
    public:
        static void enableLogging(bool enable) {mLoggingEnabled = enable;}
        static bool isLoggingEnabled(){ return mLoggingEnabled;}
        template<typename... Args>
        static void log(const Args&... args) {
            if (!mLoggingEnabled)
                return;
            ofstream ofs(mDebugFileName, ios_base::app);
            if (ofs.fail()) {
                cerr << "unable to open" << endl;
                return;
            }
            logHelper(ofs, args...);
            ofs << endl;
        }        

    private:
        template<typename T1>
        static void logHelper(ofstream& ofs, const T1& t1) {
            ofs << t1;
        }
        template<typename T1,typename... Args>
        static void logHelper(ofstream& ofs, const T1& t1, const Args&... args) {
            ofs << t1;
            logHelper(ofs, args...);
        }
        static bool mLoggingEnabled;
        static const char* mDebugFileName;
    };
    bool Logger::mLoggingEnabled = false;
    const char* Logger::mDebugFileName = "debugfile.out";

    #define log(...) Logger::log(__func__, "(): ", __VA_ARGS__)
    // __VA_ARGS__代表了...
    // log("giv arg", *obj);替换为Logger::log(__func__,"(): ", "giv arg", *obj)

    bool isDebugSet(int argc, char* argv[])
    {
        for (int i = 0; i < argc; ++i) {
            if (strcmp(argv[i], "-d") == 0) {
                return true;
            }
        }
        return false;
    }

    class ComplicatedClass
    {
    public:
        ComplicatedClass(){}
    };
    ostream& operator<<(ostream& ostr, const ComplicatedClass& src) {
        ostr << "ComplicatedClass";
        return ostr;
    }
    class UserCommand
    {
    public:
        UserCommand(){}
    };
    ostream& operator<<(ostream& ostr, const UserCommand& src) {
        ostr << "UserCommand";
        return ostr;
    }
    int counter{ 0 };
    UserCommand getNextCommand(ComplicatedClass* obj)
    {
        UserCommand cmd;
        return cmd;
    }
    void processUserCommand(UserCommand& cmd) {
        cout << cmd << counter++ << endl;
    }
    void trickyFunction(ComplicatedClass* obj)
    {
        log("given arg ", *obj);
        for (size_t i=0; i<100; ++i) {
            UserCommand cmd = getNextCommand(obj);
            log("retrieved cmd ", i, ": ", cmd);
            try {
                processUserCommand(cmd);
            } catch(const exception& e) {
                log("received exception form processUserCommand(): ",e.what());
            }
        }
    }

    int main(int argc, char* argv[])
    {
        Logger::enableLogging(isDebugSet(argc, argv));
        if (Logger::isLoggingEnabled()) {
            for (int i=0; i< argc; ++i) {
                log(argv[i]);
            }
        }
        ComplicatedClass obj;
        trickyFunction(&obj);
        return 0;
    }
    // 运行方式 on windows(.exe可省略)
    // > start STDebug.exe
    // > start STDebug.exe -d

2.编译时调试
预处理指令DEBUG_MODE,#ifdef.编译时定义符号DEBUG_MODE。GCC通过命令行指定-Dsymbol,VC++命令行指定/D symbol
- 优点：调试代码不编译到二进制文件
- 缺点： 发现bug，无法再客户现场调试

3.运行时调试
提供动态控制调试模式的异步接口，如命令菜单。可用于对程序进行跨进程条用（如套接字，远程过程调用）

环形缓冲区
> 启动调试可能为时已晚，应启用跟踪(trace),获取最近的跟踪信息，保存在内存中，在需要时存储到错误或日志文件。

常见方法时使用环形缓冲区保存固定数目的短消息，或在固定大小的内存保存消息，缓冲区填满，重新在开头写消息并覆盖就消息。

exp: ring buffer

    #include <iostream>
    #include <vector>
    #include <sstream>
    #include <fstream>
    #include <iterator>
    using namespace std;

    class RingBuffer{
    public:
        RingBuffer(size_t numEntries = kDefaultNumEntries,
            std::ostream* ostr = nullptr);
        virtual ~RingBuffer();
        template<typename... Args>
        void addEntry(const Args&... args)
        {
            std::ostringstream ostr;
            // input to ostingstream
            addEntryHelper(ostr, args...);
            // now ostringstream is not empty and save it as string in vector
            addStringEntry(ostr.str());
        }
        friend std::ostream& operator<<(std::ostream& ostr, RingBuffer& rb);
        friend std::ofstream& operator<<(std::ofstream& ostr, RingBuffer& rb);
        std::ostream* setOutput(std::ostream* newOstr);
    private:
        std::vector<std::string> mEntries;
        std::vector<std::string>::iterator mNext;
        std::ostream* mOstr;
        bool mWrapped;
        static const size_t kDefaultNumEntries = 20;
        template<typename T1>
        void addEntryHelper(std::ostringstream& ostr, const T1& t1) {
            ostr << t1;
        }
        template<typename T1, typename... Tn>
        void addEntryHelper(std::ostringstream& ostr, const T1& t1, const Tn&... args) {
            ostr << t1;
            addEntryHelper(ostr, args...);
        }
        // 使用&&保存临时字面量
        void addStringEntry(std::string&& entry);
    };

    RingBuffer::RingBuffer(size_t numEntries, ostream* ostr):mEntries(numEntries),
    mNext(begin(mEntries)),mOstr(ostr),mWrapped(false)
    {
    }
    RingBuffer::~RingBuffer(){}

    ostream& operator<<(std::ostream& ostr, RingBuffer& rb)
    {
        if (rb.mWrapped){
            copy(rb.mNext,end(rb.mEntries),ostream_iterator<string>(ostr, "\n"));
        }
        copy(begin(rb.mEntries), rb.mNext, ostream_iterator<string>(ostr, "\n"));
        return ostr;
    }
    ofstream& operator<<(std::ofstream& ostr, RingBuffer& rb)
    {
        for (auto& e : rb.mEntries){
            ostr << e;
        }
        return ostr;
    }
    std::ostream* RingBuffer::setOutput(std::ostream* newOstr)
    {
        // return old os, and set new os
        ostream* ret = mOstr;
        mOstr = newOstr;
        return ret;
    }
    void RingBuffer::addStringEntry(std::string&& entry)
    {
        if(mOstr){
            *mOstr << entry <<endl;
        }
        *mNext = std::move(entry);
        ++mNext;
        if (mNext == end(mEntries)) {
            mNext = begin(mEntries);
            mWrapped = true;
        }
    }

    class ComplicatedClass
    {
    public:
        ComplicatedClass(){}
    };
    ostream& operator<<(ostream& ostr, const ComplicatedClass& src) {
        ostr << "ComplicatedClass";
        return ostr;
    }
    class UserCommand
    {
    public:
        UserCommand(){}
    };
    ostream& operator<<(ostream& ostr, const UserCommand& src) {
        ostr << "UserCommand";
        return ostr;
    }
    int counter{ 0 };
    UserCommand getNextCommand(ComplicatedClass* obj)
    {
        UserCommand cmd;
        return cmd;
    }
    void processUserCommand(UserCommand& cmd, int i) {
        // cout << cmd << counter++ << endl;
        cout << i;
        if (i == 5) {throw invalid_argument("Unable to open file");}
    }

    RingBuffer debugBuf;
    // #define addEntry(...) RingBuffer::addEntry(__func__, "(): ", __VA_ARGS__)
    void trickyFunction(ComplicatedClass* obj)
    {
        debugBuf.addEntry(__func__, "():given arg: ", *obj);
        for (size_t i=0; i<100; ++i) {
            UserCommand cmd = getNextCommand(obj);
            debugBuf.addEntry(__func__, "():retrieved cmd ", i, ": ", cmd);
            try {
                // main process runs here, if got any fault,don't 
                processUserCommand(cmd, i);
            } catch(const exception& e) {
                debugBuf.addEntry(__func__, "():received exception form processUserCommand(): ",e.what());

                ofstream ofs("trace.out", ios_base::app);
                if (ofs.fail()){
                    cerr << "unable to open" << endl;
                    return;
                }
                ofs << debugBuf;
                return;
            }
        }
    }


    int main(int argc, char* argv[])
    {
        for (int i=0; i < argc; ++i) {
            debugBuf.addEntry(argv[i]);
        }
        ComplicatedClass obj;
        trickyFunction(&obj);

        cout << debugBuf;
        return 0;
    }
    // 运行方式 on windows(.exe可省略)
    // > start STDebug.exe
    // > start STDebug.exe -d

### （运行时求值）断言
> <cassert>头文件，定义了assert宏。接受bool表达式，迫使程序在bug来源的确切点公开bug。

NOTE：assert宏行为取决于NDEBUG预处理符号，无此符号则断言。因此常在编译发布版本时定义此符号

静态断言：
static_assert：编译时对断言求值，参数为求值的表达式和字符串
static_assert(INT_MAX >= 0xFFF,
"code requires INT_MAX to be at least 0xFFF");
用法：通常与类型trait结合。

崩溃转储（内存转储，核心转储），先建立符号服务器：用于存储软件发布二进制版本的调试符号，用以解释来自客户的崩溃转储。创建源代码服务器，存储源代码的所有修订。调试崩溃转储时，源代码服务器下载正确的源代码，以修订创建崩溃转储的软件。其价值高于1000个bug报告

### 调试技术
1.重现bug，重现每一步操作，运行自动化测试，运行压力测试，并发测试
2.调试可重复bug
  - 记录调试消息，仅启用日志（会略微改变程序计时），bug可能消失。
  - 使用调试器单步跟踪
3.调试不可重现bug
  - 尝试重现bug
  - 分析错误日志
  - 获取和分析跟踪（如环形缓冲区）
  - 检查内存转储文件（核心文件），平台提供分析这些内存转储文件的工具
  - 检查代码
  - 使用内存观察工具
  - 提交或更新bug报告（还未完全解决）
  - 找到根源后，创建可重现的测试用例（修复bug前），可重现，也可用于尝试修复bug后测试

4.调试退化
  - 查看日志中特性能工作的时间，查看该时间以后的所有改变日志。
  - 对旧版本二进制文件进行二叉树搜索bug

5.调试内存问题

内存释放错误：
  - 内存泄漏
  - 使用不匹配的分配和释放
  - 多次释放
  - 释放未分配的内存：通常导致程序崩溃（delete a not valid pointer）
  - 释放堆栈内存：技术上属于释放未分配的内存的特殊情况

内存访问（读写）错误：通常导致微妙的错误结果，但程序通常能运行

访问无效内存：几乎总导致程序立刻崩溃
再次访问已释放的内存：通常不崩溃，但被另行分配，可能产生奇怪的值
访问不同分配中的内存（超过index）：不崩溃，但有潜在危险
读取未初始化的内存：读取未初始化的值

调试内存错误（purify,valgrind,application verifier）
内存相关bug每次出现在略微不同的位置，表明堆内存损坏.
原理：调试工具是运行时验证，插入自己的内存分配和释放例程，检查动态内存相关的误用
通常查看裸指针的用法

- 类错误
  - 验证带有动态分配内存的类的析构函数是否准确释放了内存
  - 确保类能通过复制构造函数和赋值运算符正确处理复制赋值。确保移动构造函数和移动赋值运算符把原对象中的指针正确设置为nullptr,这样其析构函数不释放盖内存
  - 检查可疑的类型转换，使用dynamic_cast
- 一般内存错误
  - 确保每个new的调用都匹配了一个delete调用
  - 检查缓冲区溢出（C风格字符串）
  - 检查无效指针的解引用
  - 堆上声明指正，确保总是在声明时初始化
  - 确保总是在类的构造函数初始化指针数据成员（赋值或nullptr）

## 调试多线程（存在时序问题）
- 使用调试器：问题如死锁。将阻塞信息与追踪日志比较
- 使用基于消息的调试：在程序临界区之前之后，以及获得锁前，释放锁后添加调试语句（但可能改变时序，隐藏bug）
- 插入前置休眠和上下文切换：是线程睡眠特定时间，强制执行特定的调度行为。<thread>的std::this_thread命名空间中定义了sleep_until(),sleep_for().确保其在释放锁前或堆某个变量条件发出信号前，访问共享数据前休眠几秒。看出竞争条件
- 核查代码：核查线程同步代码，记下哪些是一定无害的


mark pg.665






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

