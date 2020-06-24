> 直接使用 **API函数** 写效率过低且容易出错。
MFC(Microsoft Fundation Classes,Microsoft基础类库）是对API函数的简单封装，简化开发过程
开发者的MFC类库设计过程

### 5.1运行时类信息（CRuntimeClass类）
> 在程序运行过程中辨别对象是否属于特定类的技术叫动态类型识别（Runtime Type Information，RTTI）
1.用于函数识别其参数类型。2.用于针对对象所属类编写特定目的的代码。

框架程序使用RTTI管理应用程序，用户可以设计自己的类，框架程序可在程序执行过程知道这个类的类名、大小等信息，并能创建类对象。

#### 动态类型识别和动态创建
给类使用唯一标识（同进程ID一样）。一个类的所有实例拥有相同的标识。继承的类需要创建新的标识（不同于父类的标识）。
> 类的静态成员（python中的类属性、类方法？）不属于（实例）对象的一部分，而是类的一部分。定义类时，编译器已经为类的静态成员分配内存了，不论多少实例，静态成员只有一份。因此，给每个类安排1个静态成员变量，它的内存地址即是类的唯一标识。
```C++
class RecoClass{
	public:
		// 定义GetRuntimeClass()返回静态成员的地址值
		const int* GetRuntimeClass(){
			return (int*)&classAddress;  //是否要加上(int*)或者(const int*)？
			}
		stacic const int classAddress;
};
// 初始化一个任意值，其他类创建的静态成员也可以是相同值，因为它们地址值不同。
const int RecoClass::classAddress = 1;
```
>只是创建1个int类型变量不能传达有效信息，需要创建1个静态成员结构体,如果为每个类都写一个创建该类的全局函数，就能从文件或用户输入中取得此函数的内存地址，从而创建用户动态指定的类，这就是**动态创建**。
>并将该结构体存入1个可被所有其他类继承的基类，方便调用。

```C++
#ifndef__AFX_H__
#define__AFX_H__
#include <windows.h>
class CObject;
struct CRuntimeClassStaticMember{
	// 属性
	LPCSTR m_lpszClassName;  //1. 类名
	int m_nObjectSize;  // 2.类大小
	UINT m_wSchema;  // 3.类的版本号
	CObject* (__stdcall* m_pfnCreateObject)();  // 4.(创建类的函数)的指针，以支持动态创建
	// 5.其基类中CRuntimeClassStaticMember结构的地址，即判断当前类是否是继承自含CRuntimeClassStaticMember的基类
	CRuntimeClassStaticMember* m_pBaseClass;  
	
	// 操作
	CObject* CreateObject();  // 方便调用m_pfnCreateObject指向的函数
	BOOL IsDerivedFrom(const CRuntimeClassStaticMember* pBaseClass) const;  // 判断基类的函数
	// 内部实现（implementation）
	CRuntimeClassStaticMember* m_pNextClass;  // 将所有CRuntimeClassStaticMember对象用简单的链表连在一起
};

// 操作的具体函数1
CObject*CRuntimeClassStaticMember::CreateObject(){
	if(m_pfnCreateObject == NULL)
		return NULL;
	return (*m_pfnCreateObject)();  //返回这个函数指针
}
// 操作的具体函数2
BOOL CObject*CRuntimeClassStaticMember::IsDerivedFrom(const CRuntimeClassStaticMember* pBaseClass) const{
	const CRuntimeClassStaticMember* pThisClass = this;
	while (pClassThis != NULL){
		if （pClassThis == pBaseClass）{
			return True;
		pClassThis = pClassThis->m_pBaseClass;}
	return FALSE;}
// 加上类的其他定义
#endif //__AFX_H__

// 定义基类
class CObject{
public:
	virtual CRuntimeClassStaticMember* GetRuntimeClass() const;
	virtual ~CObject();
	stacic const int classAddress;
public:
	BOOL IsKindOf(const CRuntimeClassStaticMember* pClass) const;  // 判断当前类是否继承自pClass或pClass的派生类
public:
	static const CRuntimeClassStaticMember cObjectAddress;  // 基类的静态成员地址
};
	
inline CObject::~CObject(){
}
// 定义1个宏来返回唯一类标识。
define RUNTIME_CLASS(class_name)((CRuntimeClassStaticMember*）&class_name::class##class_name)
```
CObjectAddress静态成员的初始化代码和类的实现代码都在OBJCORE.CPP文件中。

```C++
const struct CRuntimeClassStaticMember CObject::cObjectAddress = {
	"CObject"/*类名*/, sizeof(CObject)/*大小*/, 0xffff/*无版本号*/,NULL/*不支持动态创建*/，NULL/*没基类*/， NULL};
在此处定义基类的静态成员创建后，
CRuntimeClassStaticMember* CObject::GetRuntimeClass() const{
	return RUNTIME_CLASS(CObject);
	// 等同 return ((CRuntimeClassStaticMember*）&(CObject::cObjectAddress));
	// 返回地址值,即类的唯一标识，地址值的数据类型是CRuntimeClassStaticMember类型
}
BOOL CObject::IsKindOf(const CRuntimeClassStaticMember* pClass) const{
	const CRuntimeClassStaticMember* pClassThis = GetRuntimeClass();
	return pClassThis->IsDerivedFrom(pClass);
}
```
### 对动态库类的实际使用

```C++
#include "path/_afx.h"
class CNewC: public CObject{
public:
	virtual CRuntimeClassStaticMember* GetRuntimeClass() const{
		return ((CRuntimeClassStaticMember*）&cNewCAddress);}
	static const CRuntimeClassStaticMember cNewCAddress;
	//为使CNewC类支持动态创建，在初始化类中传递1个创建CNewC对象的函数的地址的静态成员函数。
	static CObject* __stdcall createObject(){
		return new CNewC;}  // 由系统来控制创建。
}；
const CRuntimeClassStaticMember CNEWC::cNewCAddress = {
	"CNewC", sizeof(CNewC),0xffff,
	&CNewC::CreateObject,  // 现在就能支持动态创建
	(CRuntimeClassStaticMember*)&(CObject::cObjectAddress),  // 父类的标识地址
	Null};
void main(){
	CObject* pMyObject = new CNewC;  // 创建对象
	if (pMyObject->IsKindOf(RUNTIME_CLASS(CNEWC)))  // 判断对象是否继承自CNweC类或其派生类
	{
		CNewC* pNewInstance = (CNewC*)pMyObject;
		cout<<" 创建了CNweC类对象的实例\n";
		delete pNewInstance;}  // 使用完成后删除对象以释放空间
	else{
		delete pMyObject;}
}
```

>此时只要得到CNewC类中CRuntimeClassStaticMember结构记录的类的信息，就可以动态创建CNewC类，而不用给出类名。可以是用户输入的，也可是磁盘上取得的。

```C++
void main(){
	CRuntimeClassStaticMember* pNoNameClass = RUNTIME_CLASS(CNewC);
	CObject* pNewObject = pNoNameClass->CreateObject();
	}
```

### 5.2 调试支持

### 5.3 框架程序的映射
例如窗口类CWnd控制线程中所有窗口，线程中的每个窗口的窗口句柄都应该对应唯一的CWnd指针。
这要求封装1个类来保存有映射关系的数据。如果是指针映射到指针，将类命名为CMapPtrToPtr,如果是指针到双字的映射，就命名为CMapPtrToWord。

```C++
// 这个结构表示给定1个key，仅有1个value与其对应，并链接到下一个CAssoc结构
struct CAssoc{
	CAssoc* pNext;
	void* key;
	void* value;
	};
```
但如果2个CAssoc结构占用不连续的内存空间，这空间又不足容纳1个CAssoc结构，就会产生**内存碎片**。需要先1次性申请较大的空间。

```C++
// 创建1个链表结构，头部有pHead指针来释放所有空间。
struct CHead{
	CHead* pNext;
	void* data(){
		return this + 1;
	}  // 记录链表的数据量
	// 申请内存的全局函数,申请cbElement大小的空间nMax个
	 static CHead* Create(CHead* &pHead, UINT nMax, UINT cbElement);
	 // 释放当前对象为首地址（this指针）的内存链中的所有内存
	 void FreeeDataChain;
	 };
	
	};
```
