### 4. 图形界面
在VC++6版本中
显示图形界面的入口函数不是`int main(int argc, char* argv[]){code block};`而是

```C++
// 应用程序的实例句柄（即模块句柄）,模块句柄的值就是模块在内存中的首地址
hInstance = (HINSTANCE) GetModuleHandle(NULL);  
// *入口函数中的参数（跟main中的参数一样）是系统自动创建（初始化），而不是手动外界传递。
int APIENTRY WinMain(HINSTANCE hInstance,  // 本模块的实例句柄
                      HINSTANCE hPrevInstance,  // 2006年后已不再用
                      LPSTR lpCmdLine,  // 命令行参数， 看是否打开特定文档
                      int nCmdShow){code block}  // 主窗口初始化时的显示方式
```
windows的消息驱动
windows系统不断向程序发送消息，通知程序用户进行了什么操作，将信息作为参数传递给目标程序中的窗口函数（window Procedure或叫消息处理函数）
窗口函数的函数原形`LRESULT CALLBACK MainWndProc(HWND, UNIT, WPARAM, LPARAM);`
1. 先找到目标程序的窗口句柄 hWnd
2. 发送消息 ::sendMessage(hWnd,WM_CLOSE,0,0);  // WM_CLOSE为关闭窗口的消息。

创建窗口的函数：

```C++
// CALLBACK宏是 _stdcall的意思，
LRESULT CALLBACK MainWndProc(HWND, UNIT, WPARAM, LPARAM);
// 下边这个函数用来创建窗口
int APIENTRY WinMain(HINSTANCE hInstance,  HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow){
	char szClassName[] = "MainWClass";
	
	// 设定窗口类，用描述主窗口的参数填充WNDCLASSEX结构，定义窗口的一些主要属性，后边创建的新窗口继承这个类的属性。
	WNDCLASSEX wndclass;  
	wndclass.cbSize = sizeof(wndclass);  // 结构大小
	wndclass.stle = CS_HREDRAW|CS_VREDRAW;  // 如果大小改变就重画
	wndclass.lpfnWndProc = MainWndProc;  // 窗口函数指针，指定窗口消息处理函数的地址
	wndclass.cbClsExrtra = 0;  // 没有额外的类内存
	wmdclass.cnWmdExtra = 0;  // 没有额外的窗口内存
	wndclass.hInstance = hInstance;  // 实例句柄
	wndclass.hIcon = ::LoadIcon(NULL, IPI_APPLICATION);
	wndclass.hCursor = ::LoadCursor(NULL, IDC_ARROW);
	wndclass.hbrBackground = (HBRUSH)::GetStockObject(WHITE_BRUSH);
	wndclass.lpszMenuName = NULL;
	wndclass.lpszClassName = szClasssName;  // 指定窗口类名称，基于此类wndclass创建的窗口都要引用这个类名szClassName
	wndclass.hIconSm = NULL;
	::RegisterClassEx(&wndclass);  // 注册窗口类
	
	 // 创建主窗口， 窗口句柄** HWND唯一地表示了一个窗口（例如要创建一个messagebox也会创建1个HWND）
	HWND hwnd = ::CreateWindowEx(
		0,
		szClassName,
		"my window created",
		WS_OVERLAPPEDWINDOW,
		CW_USEDEFAULT,  //X,初始X坐标
		CW_USEDEFAULT,  //Y,初始Y坐标
		CW_USEDEFAULT,  //nWidth，初始宽度
		CW_USEDEFAULT,  //nHeight，初始高度
		NULL,  // hWdnParent，父窗口句柄
		NULL,  // hMenu，菜单句柄
		hInstance,  //程序实例句柄
		NULL});
	if(hwnd == NULL){
		::MessageBox(NULL, "Creating New Window Failed", "error", MB_OK);
		return -1;}
	// 显示窗口，刷新窗口客户区
	::ShowWindow(hwnd, nCmdShow);
	::UpdateWindow(hwnd);
	
	//window为每个线程维护一个消息队列
	// 从消息队列中取出消息，交给窗口函数处理，知道GetMessage返回FALSE, 结束消息循环
	MSG msg;
	/* GetMessage平时保持阻塞，其初始返回值不为0，只要不传入QUIT, 这返回值就不会变化，不会退出循环，
	消息到达时会先分派到*回调函数*（DispatchMessage）处理后，再传给GetMessage）*/
	while(::GetMessage(&msg, NULL, 0, 0))  // 从消息队列中取出一个消息填充MSG结构
	{
		::TranslateMessage(&msg);  // 转化键盘消息
		::DispatchMessage(&msg);}  // 将消息发送到相应的窗口函数
	return msg.wParam;}
	
// 用来向窗口程序发送消息, 告知用户所进行的操作控制
LRESULT CALLBACK MainWndProc(HWND hwnd, UNIT message, WPARAM wParam, LPARAM lParam){
	char szText[] = "a simple window program"
	switch(message){
		case WM_PAINT:  // 窗口客户区需要重画,有修改如最小化时窗口客户区就会先变为无效
		{
			HDC hdc;
			PAINTSTRUCT ps;
			// 使无效的客户区变为有效，并取得设备环境句柄
			hdc = ::BeginPaint(hwnd, &ps);
			// 显示文字
			::TextOut(hdc, 10, 10, szText, strlen(szText);
			::EndPaint(hwnd, &ps);
			return 0;}
		case WM_DESTROY:  // 销毁窗口
			::PostQuitMessage(0);  //向消息队列投递WM_QUIT消息，使GetMessage返回0，结束消息循环
		return 0;}
	// 不再switch情况中，交给系统自行处理
	return ::DefWindowProc(hwnd, message, wParam, lParam);
}
```
		
def funcre(dir)
	for name in listdir(dir)
		if dir:
			
