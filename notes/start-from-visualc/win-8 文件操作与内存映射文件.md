### 8.3 注册表
> 是操作系统和用户应用程序的设置仓库。
注册表可能是存储在磁盘上的静态数据， 也可能是一系列有windows 内核负责维护的内存中的数据

注册表结构:
是一个数据库，结构同逻辑磁盘类似，包含键和值
* HKEY_CURRENT_USER  存储于当前登录用户相关信息
* HKEY_USERS  存储机器上所有账户的信息
* HKEY_CLASSES_ROOT  存储文件关联和COM(Component Object Model，组件对象模型）
* HKEY_LOCAL_MACHINE  存储系统先关信息
* HKEY_PERFORMANCE_DATA  存储性能信息
* HKEY_CURRENT_CONFIG  存储硬件配置信息
键值存储的数据类型
1. REG_DWORD  双字型变量。可存储数字或者布尔类型变量
2. REG_BINARY  二进制数据。可存储超过32位的数字和原始数据，比如加密密码
3. REG_SZ  字符串变量

#### 实例：开机后自动启动
> windows再启动并执行登录操作后， 会将HKEY_LOCAL_MACHINE\Software\Microsoft\WIndows\CurrentVersion\Run子键下的所有键值枚举一遍，
并将所有REG_SZ类型的键值项中的数据当做一个文件名自动执行，所以在这个子键下设置一个键值项，是文件名字符串，便可自动运行文件

```C++
int main(int argc, char*argv[]){
	HKEY hRoot = HEKY_LOACL_MACHINE;
	char* szSubKey = "Software\\Microsoft\\WIndows\\CurrentVersion\\Run";
	HKEY hKey;
	DWORD dwDisposition = REG_OPENED_EXISTING_KEY;  // don't create is not exist
	LONG lRet = ::RegCreateKeyEx(hRoot, szSubKey, 0, NULL,REG_OPTION_NON_VOLATILE,KEY_ALL_ACCESS,NULL,&hKey,&dwDisposition);
	if(lRet!= ERROR_SUCCCESS)
		return -1;
	char szModudle[MAX_PATH];
	::GetModuleFileName(NULL,szModule,MAX_PATH);
	lRet = ::RegSetValueEx(hKey,"SelfRunDemo",0,REG_SZ,(BYTE*)szModule,strlen(szMouule));
	if (lRet == ERROR_SUCCESS){
		printf("success\n")}
	::RegCloseKey(hKey);
	getchar();
	return 0;
}
```
#### 内存映射文件
> （与虚拟内存相似，但虚拟内存数据来自系统页文件）保留一个地址空间区域，在需要时将它提交到物理存储器，数据来自磁盘上相应的文件。
> 一旦文件被映射。就可认为文件加载到了内存中
目的：
1. 系统使用内存映射文件来加载和执行exe和dll，节省系统页文件空间，缩短程序启动时间。
2. 使用内存映射文件访问磁盘上的数据。避免对文件进行文件I/O操作，避免为文件内容申请缓冲区。
3. 使用内存映射文件在多个进程间共享数据。

创建步骤：
1. 使用CreateFileMapping创建内存映射文件内核对象，告诉操作系统内存映射文件需要的威力内存大小，
决定了其用途--为磁盘文件建立内存映射还是为多个进程共享数据建立共享内存。
2. 映射文件映射对象的全部或一部分到进程的地址空间。是为文件中的内容分配线性地址空间，并将线性地址空间和文件内容对应，使用MapViewOfFile。
进程地址空间在逻辑上相互隔离，在物理上是重叠（同时被多个进程使用）的。

#### 读取BMP图片的过程
1. 调用CreateFile函数打开文件，得到文件句柄hFile
2. 调用CreateFileMapping，并将hFile传入，为该文件创建内存映射内核对象，得到内存映射文件句柄hMap
3. 调用MapViewOfFile映射整个文件到内存。返回文件映射到内存后的内存地址。使用指向这个地址的指针来读取文件内容。
4. 调用UnmapViewOfFile解除文件映射
5. 调用CloseHandle关闭内存映射文件对象，必须传入内存映射文件句柄hMap
6.. 调用CloseHandle关闭文件对象，必须传入内存映射文件句柄hFile

线程间通信机制（进程间切换，以免造成堵塞）
例如工作线程通知主窗口线程。发送消息，包括开始工作，当前进度，结束工作。
