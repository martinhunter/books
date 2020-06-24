### 9.1 动态链接库（dynamic link library,除了dll，系统中某些exe、控件（*.ocx）也可能是动态链接库）
> 作用：API都是从系统动态链接库中导出。方便更新和重用模块化程序更方便。几个程序同时使用相同函数时，减少内存消耗，因程序代码是共享的。
> 概念： 是应用程序的一个模块，用于导出一些函数和数据供程序中其他模块使用。
1. 是应用程序的一部分，本质上与可执行文件相同，都作为模块被进程加载到自己的空间地址。
2. 在程序编译时不会被插入到可执行文件（exe），在程序运行时整个库的代码才会调入内存
3. 多程序用同一动态链接库时，windows在物理内存中止保留1份库的代码，仅仅通过分页机制将这份代码映射到不同进程中。

创建名为09DllDemo的工程文件，入口为DllMain函数
```C++
BOOL APIENTRY DllMain(HANDLE hModule,  // 本模块句柄
		      DWORD ul_reason_for_call,
		      LPVOID lpReserved){
    switch(ul_reason_for_call){
	// 动态链接库刚被映射到某个进程的地址空间
    case DLL_PROCESS_ATTACH:
	// 程序创建新进程
    case DLL_THREAD_ATTACH:
	//程序某个线程正常终止
    case DLL_THREAD_DETACH:
	//动态链接库将被卸载
    case DLL_PROCESS_DETACH:
	break;
    }
    return TRUE;
}
```
DLL定义导出函数和内部函数。
导出函数可被其他模块调用

### 9.2 hook
> **windows程序的运行模式是基于消息驱动，任何线程只要注册窗口类都会有一个消息队列接受用户的输入消息和系统消息**
> 作用：hook应用于各种监测程序中，必须写在动态链接库以便注入其他进程。使用hook来获取特定线程接受或发送的消息。

概念：应用程序可以安装1个子程序（hook函数）以监视特定窗口某种类型的消息，这窗口可以是其他进程创建的。
在消息到达后，目标窗口处理函数处理前，hook允许应用程序截获它进行处理。
hook是一个处理消息的程序段，通过调用相关API函数，将它挂入系统
* hook用来截获系统中的信息流。
* 截获消息后，用于处理消息的子程序叫hook函数，它是应用程序自定义的一个函数，在安装hook时要把这个函数的地址告诉windows
* 系统同一时间可能有多个进程安装hook，多个hook函数组成hook链。所以在处理截获到的消息时，应把消息事件传递下去，以便其他hook有机会处理。
* hook会使系统变慢，它增加了系统对每个消息的处理量。

```C++
// 安装hook，使用SetWindowsHookEx函数
HHook SetWindowsHookEx(
	int idHook,  // 指定hook类型
	HOOKPROC lpfn,  // hook函数的地址。
	HINSTANCE hMod,  // hook函数所在dll的实例句柄。如果是局部的hook，参数为NULL
	DWORD dwThreadId  // 指定要为哪个线程安装hook。如为0，该hook被解释成系统范围内的
);
```
钩子安装后如果有相应的消息发生，windows将调用lpfn参数指向的函数。如idHook值为WH_MOUSE,则目标线程消息队列中有鼠标消息取出时，lpfn指向的函数就会被调用。
* 如果dwThreadId为0，或指定一个有其他进程创建的线程ID，lpfn参数指向的hook函数必须位于dll中。这是因为进程的地址空间是相互隔离的，
发生事件的进程不能调用其他进程地址空间中的hook函数。此时hook函数必须放在dll中，这种hook叫做远程hook
* 如果dwThreadId为进程自身创建的线程ID，不必写入dll，称为局部hook。
* 如果dwThreadId为0，hook函数将关联到系统内的所有线程

```C++
// hook函数的一般形式
// HookProc是应用程序定义的名字。nCode是Hook代码，hook函数用nCode确定任务，其值依赖于Hook类型
LRESULT CALLBACK HookProc(int nCode， WPARAM wParam, LPARAM lParam){
	// 处理消息的代码
	return ::CallNextHookEx(hHook,nCode, wParam, lParam);  // hHook是安装hook时得到的hook句柄（SetWindowsHookEx的返回值）
}
// 卸载hook
BOOL UnhookWindowsHookEx(HHOOK hhk);  // hhk是安装hook时得到的hook句柄（SetWindowsHookEx的返回值）
```

#### 监视键盘输入hook实例
```C++
// create keyhooklib.dll
// 当程序调用GetMessage或PeekMessage函数，并有键盘消息(WM_KEYUP或WM_KEYDOWN)将被处理
// HOOKFILE_EXPORTS宏将定义在hookfile.cpp文件中
#include <windows.h>
#define HOOKFILE_EXPORTS
#include "hookfile.h"

//添加共享数据段并初始化
#pragma data_seg("YCIShard")
HWND g_hWndCaller = NULL;
HHOOK g_hHook = NULL;
#pragma data_seg()
//将共享数据段设为可读写共享

// 1. 创建一个通过内存地址取得磨矿句柄的帮助函数
HMODULE WINAPI ModuleFromAddress(PVOID pv){
    MEMORY_BASIC_INFORMATION mbi;
    // 虚拟内存管理函数VirtualQuery取得调用进程虚拟地址空间中指定内存页的状态，返回指定内存地址所处模块的模块句柄，
    if(::VirtualQuery(pv, &mbi, sizeof(mbi)) != 0){
	return (HMODULE)mbi.AllocationBase;
    }
    else{
	return NULL;
    }
}

//键盘hook函数
LRESULT CALLBACK KeyHookProc(int nCode， WPARAM wParam, LPARAM lParam){
    if(nCode<0 ||nCode == HC_NOREMOVE){
	return ::CallNextHookEx(hHook,nCode, wParam, lParam);
    }
    if(lParam & 0x4000000){
	// 表示消息重复,传递给下一个hook函数
	return ::CallNextHookEx(g_hHook,nCode,wParam,lParam);
    }
    ::PostMessage(g_hWndCaller, HM_KEY,wParam,lParam);
    ::CallNextHookEx(g_hHook,nCode,wParam,lParam);
}

// 安装、卸载hook的函数, bInstall判断进行安装还是卸载
// hWndCaller指定主窗口的句柄，hook函数会想这个窗口发送通知消息
BOOL WINAPI SetKeyHook(BOOL bInstall, DWORD dwThreadId, HWND hWndCaller){
    BOOL bOk;
    g_hWndCaller = hWndCaller;
    if(bInstall){
	g_Hook = ::SerWindowsHookEx(WH_KEYBOARD, KeyHookProc,
				    ModuleFromAddress(KeyHookProc), dwThreadId);
	bOk = (g_hHook != NULL);
    }
    else{
	bOk = ::UnhookWindowHookEx(g_hHook);
	g_hHook = NULL;
    }
    return bOk;
}

/* 使用共享数据段，在每个进程中，hook函数都要使用hook句柄和主窗口句柄，
以便调用CallNExtHookEx函数和想主窗口发送消息。现在的hook监视程序加载
dll并调用其中的导出函数SetKeyHook来安装hook，同时设置了hook句柄和主
窗口句柄。hook成功安装后，windows将dll加载到所有接受键盘消息的其他进程
的地址空间，但这些其他进程中的变量hook句柄和主窗口句柄值没有正确设置，
因为没有线程为它们赋值。
共享数据段中的数据在所有进程共享一块内存，在一个进程中设置共享数据段的
数据，其他进程中同一数据段的数据也随之改变。
在程序中添加额外的数据段使用#pragma data_seg()命令。
共享数据段的数据必须初始化*/

// 3. 创建过程
// hookfile.h
// 定义函数修饰宏，方便引用本dll工程的导出函数
#ifdef HOOKFILE_EXPORTS
#define HOOKFILE_API__declspec(dllexport)
#else
#define HOOKFILE_API__declspec(dllimport)
#endif
#define HM_KEY WM_USER + 101
// 声明要导出的函数
BOOL HOOKFILE_API WINAPI SetKeyHook(BOOL bInstall,
				    DWORD dwThreadId = 0,
				    HWND hWndCaller = NULL);

//下边是hookfile.def文件中的代码，定义了导出函数hookfile
EXPORTS
  hookfile
SECTIONS
    YCIShard  Read Write Shared

// 主工程文件，在主窗口初始化安装hook，关闭时卸载hook，过程中处理hook函数发来的HM_KEY消息
#include "resource.h"
#include "hookfile.h"
#include "/project/hookfile.h"
#pragma comment(lib,"hookfile")
CMyApp theApp;
BOOL CMyApp::InitInstance(){
    CMAinDialog dlg;
    m_pMainWnd = &dlg;
    return FALSE;
}
CMainDialog::CMainDialog(CWNd*pParentWnd):CDialog(IDD_MAIN, pParentWnd){
    
}
BEGIN_MESSAGE_MAP(CMainDialog, CDialog)
ON_MESSAGE(HM_KEY, OnHookKey)
END_MESSAGE_MAP()
BOOL CMainDialog::OnInitDialog(){
    CDialog::OnInitDialog();
    SetIcon(theApp.LoadIcon(IDI_MAIN), FALSE);
    ::SetWindowsPos(m_hWnd, HWND_TOPMOST,0,0,0,0,
		    SWP_NOSIZE|SWP_NOREDRAW|SWP_NOMOVE);
    // install hook
    if(!SetKeyHook(TRUE,0,m_hWnd)){
	MessageBox("failed");
    }
    return TRUE;
}
void CMainDialog::OnCancel(){
    // uninstall hook
    SetKeyHook(FALSE);
    CDialog::OnCancel();
    return;
}
long CMainDialog::OnHookKey(WPARAM wParam,LPARAM lParam){
    char szKey[80];
    ::GetKeyNameText(lParam,szKey,80);
    CString strItem;
    strItem.Format(" user pressed: %s\r\n",szKey);
    CString strEdit;
    GetDlgItem(IDC_KEYMSG)->GetWindowText(strEdit);
    GetDlgItem(IDC_KEYMSG)->SetWindowText(strItem + strEdit);
    ::MessageBeep(MB_OK);
    return 0;
}
```

### hook api 技术
> 指截获特定进程或系统对某个API函数的调用，使得API的执行流程指向指定的代码。
> windows下的应用程序都建立在API函数之上，使得用户有机会敢于其他应用程序的流程。

最常见：改变目标进程中调用API函数的代码，使它们对于API调用变为对用户自定义函数的调用。
> 实现原理：windows下程序有自己的地址空间，只能调用自己地址空间中的函数，因此必须将一个可替代API执行的函数的
执行代码注入目标进程，然后将目标进程的该API调用改为注入函数的调用。（被注入的函数被称为**代理函数**）

方法1. DLL注入：注入代码写到dll中，并让目标进程加载。这代理函数的签名要与原API函数的完全相同。dll初始化时，就会把目标进程
对api的调用改为对代理函数的调用。还可以趁dll在目标进程中初始化的机会创建新线程，此时新线程运行在目标进程的地址空间中。

### 其他侦测技术
#### 使用注册表注入dll

#### 使用远程线程注入dll（好用）
> 创建远程线程的函数CreateRemoteThread
