
markdown_rules: https://markdown.tw/#overview
### 1. API的调用： 
> \#include<windows.h>

win32 API: 提供与windows 系统相关的函数(内核除外）

### 2 win32程序运行原理
#### 2.1 windows的多任务（进程）实现
* 虚拟内存： 每个进程都有自己的4GB私有空间（32位地址空间），机制依靠cpu帮助操作系统将磁盘空间当做内存空间来使用，在磁盘上应用于这一机制的文件被称为页文件（paging file），页文件属性设置了访问模式标记（用户、内核访问权限）页文件包含了对所有进程都有效的虚拟内存，windows将空间虚拟空间的前一半留给进程，后一半来存储操作系统内部使用的数据，且这一半被保护不能被其他线程访问。用户程序的代码在`用户模式`下运行，系统程序（如系统服务程序和硬件驱动）的代码在`内核模式`下运行。
* 模式切换： 当应用程序调用一个系统函数的时候，会从用户模式切换到内核模式去执行，`例: win32函数ReadFile最终会调用windows内部的从文件中读取数据的程序代码，因为这代码访问了系统内部的数据，所以必须在内核模式下运行。`
* 私有的虚拟空间地址： 包含了所有可执行的或是DLL模块的代码和数据，也是程序动态申请内存的地方，比如线程堆栈和进程堆。

#### 2.2 内核对象
    是系统提供的用户模式代码与内核模式下代码进行交互的基本接口，
    程序读写系统数据在系统的监视下进行，仅仅能被内核模式下的代码访问，
    应用程序必须使用API函数访问内核对象，
    是系统管理进程的小的数据结构。
> 句柄（handle）：调用函数创建内核对象时的返回值，借由句柄才能找到相应的内核对象（相当于地址值）
> 代表内核对象引用次数计数器： 初始值为1，每次打开，系统将计数加1，关闭则减1，引用为0则关闭它。（创建新进程时其实会创建内核句柄和主线程内核句柄，计数器其实为2）

作用： 1.为系统资源提供可识别的名字。
2.在进程间共享资源和数据。
3.保护资源不被未经认可的代码访问。
4.跟踪对象的引用情况，不再被使用，系统便释放空间。

#### 2.3 进程的创建
> SDK文档： “进程是一个正在运行的程序，它拥有自己的虚拟内存地址，拥有自己的代码、数据和其他系统资源，如进程创建的文件、管道、同步对象等。一个进程也包含了一个或者多个运行在此进程内的线程。” 
进程是一个容器，包含了一系列运行在一个程序实例上下文中的线程使用的资源。必须至少有一个运行在它的地址空间的线程来负责执行该进程地址空间的代码。没有线程就会被销毁。

组成windows32进程的两部分：1.进程内核对象。2.私有的虚拟空间地址。

#### 应用程序的启动，如创建控制台应用程序`int main(int argc, char* argv[]);` main为入口函数在程序开始运行时被调用
操作系统先调用`C/C++运行期启用`函数,这个函数会初始化C/C++运行期的库，并保证用户代码执行前所有全局的或静态的C++对象能被正确创建，即执行这些对象构造函数中的代码。
### win32程序启动过程/进程的创建过程
1. 系统调用CreateProcess函数{
创建新进程，当一个线程调用CreateProcess函数时，系统创建一个进程内核对象管理进程，
2. 系统为新的进程创建一个虚拟地址空间，加载应用程序运行时所需要的代码和数据。
3. 系统为新进程创建一个主线程，主线程执行C/C++运行期启动代码开始运行，C/C++运行期启动代码会调用main函数。成功则CreateProcess函数返回True}

CreateProcess函数搜索可执行文件的路径：
1. &optional-文件名中包含的目录
1. 调用进程的可执行文件的目录。
2. 调用进程的当前目录。
3. windows系统目录（system32）
4. windows目录
5. 名为PATH的环境变量中列出的目录。

创建进程被称为父进程，被创建的进程被称为子进程。系统创建新进程时会为新进程指定一个STARTUPINFO(启动信息），包含了父进程传给子进程的一些显示信息。父进程创建子进程的内核句柄、主线程句柄，且父进程要有一个线程来调用CloseHandle关闭句柄释放内存

### 启动notepad
    STARTUPINFO si = {sizeof(si)}; // 初始化STARTUPINFO结构体的大小值，其他值初始化为0，以兼容后续版本结构体成员数量变化
    PROCESS_INFORMATION pi； // 创建进程后返回新建进程的标志信息，如ID号，句柄等。
    char* szCommandLine = "notepad"; // 要传递给执行模块的参数。
    ::CreateProcess(NULL, szCommandLine, NULL, NULL, FALSE, NULL, NULL, NULL, &si, &pi);
#### 2.4 中止进程
* 主线程的入口函数返回。例： 程序入口main函数return时，启动函数会调用C/C++运行期退出函数exit，并将用户返回值传给它
* 进程中的一个线程调用了ExitProcess（一个API函数）。
* 此进程中所有线程都结束了。
* 其他进程中的一个线程调用了`TerminateProcess（HANDLE hProcess// 要结束的进程的句柄， UNIT uExitcode // 指定目标进程的退出代码）函数`

#### 2.5 保护进程
1. 防止此进程被其他进程检测到。
2. 防止此进程被其他进程中止。

对方法1： 检测系统进程时通常用ToolHelp或Process Status函数，hook掉系统对这些函数的调用，使这两个函数返回值不包含此进程。
对方法2： hook掉其他进程对TerminateProcess函数的调用(包括任务管理器也使用TerminateProcess函数）

### 游戏内存修改器
原理：修改游戏所在进程的内存。进程的地址空间相互隔离，利用API函数访问其他函数的内存。

条件是**目标值（例如游戏内金钱数）的内存地址值不会变**
> 读写参数,对每个找到的值进行测试以确定要改变的目标。

    BOOL ReadProcessMemery(
        HANDLE hProcess, // 待读进程的句柄
        LPCVOID lpBaseAddress, // 目标进程中待读内存的起始地址(游戏进程中搜索所需数据的内存地址）
        LPVOID lpBuffer, // 接受读取数据的缓冲区
        DWORD nSize, // 要读取的字节数
        LPDWORD lpNumberOfBytesRead // 供函数返回实际读取的字节数
        );
    WriteProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, lpNumberOfBytesRead);
> 搜索目标地址

    BOOL FindFirst(DWORD dwValue); // 在目标空间中第一次查找
    BOOL FindNext(DWORD dwValue); // 后续查找
    DWORD g_arList[1024]; // 地址列表
    int g_nListCnt; // 有效地址的个数
    HANDLE g_hProcess; // 目标进程句柄
> 测试修改程序
例：游戏现在显示的金钱数现为12325，搜索到多个地址值，在游戏中改变金钱数量为比如12426，再从这些地址值中再次搜索，递归直到找到唯一地址值。
    
    #include<stdio.h>
    int g_nNum;
    int main(int argc, char*argv[]){
        int i = 198;
        g_nNum = 1003;
        while(1){
            pringf("i=%d, addr=%081X; g_nNum=%d, addr=%081X\n",++i,&i,--g_nNum,&g_nNum);
            getchar();
        }
        return 0;
    }
        
