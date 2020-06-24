### re-rules
```python
ret = re.match(r"pattern", string)  # pattern需要从string头开始匹配
ret.group(number)  # 括号从外往内数， number默认为0，代表整个匹配值
re.match(r"(?P<name1>\d*).*(?P=name1)"
# ?P<name1>代表给匹配到的\d*起个名字，后边?P=name1的内容与\d*相同，一般用于http中匹配,如<body>content</body>
re.search(r"pattern", string)  # 匹配string中遇到的第一个符合条件内容

    def add(temp):
        strNum = temp.group()
        num = int(strNum) + 1
        return str(num)
        
    re.sub(r"\d+", add, "python = 992")  # 根据实际用函数动态替换所有符合的内容
```

### http协议
> 若服务器对请求返回302及新地址，就会自动重定向。

http连接：
1. 先解析域名获得IP地址
2. 进行3次握手，4次挥手
3. 服务器返回http内容 

交给网关，mac地址变，ip不变。
格式：头文件（header)\r\n\r\n正文(body)<!DOCTYPE html>...
阿里妈妈放广告

### tcp3次握手，4次挥手
3次握手开始于client_socket.connect()
1. client发送如 syn 11，（server接收到syn 11后加1，将其变为ack 12）
2. server发送ack12 和如 syn 45
3. （client确认ack12是正确的，client开始准备资源/程序运行，并将syn 45转换为ack 46），
client发送ack46，（server确认ack 46正确，server开始准备资源/程序运行,server调用accept（）)。
> （双方都确认才开始准备资源运行）

。。。中间互相传输数据

4次挥手开始于client_socket.close()
1. client发给server--client会关闭发送，（server接收到信息会关闭接收）
2. server发给client--server已经知道client会关闭发送。
3. （server调用 server_new_socket.close()），server发给client--server会关闭发送，
（client接收到信息会关闭接收)。（server在比如4秒超时时间内没有收到第4步client返回的信息
就会持续发送，如果超过4秒server会不再等待client的消息，关闭释放资源并向client发送一条已超时信息）
4. client发给server--client已经知道server会关闭发送。client先不关闭，会等待2*最大传输时间，一般共2-5min，这时间内若有超时信息就处理超时信息，若没有则说明没有问题，client就会关闭释放资源。

如果server先调用close，在2min内server就会有端口被占用的问题，无法打开。
需要server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)后加上

    server_socket.setsockopt(socket.SOL_SOCKET, socker.SO_REUSEADDR, 1)

### 实现返回页面的http服务器
```python
def response_html(new_socket):
    
    try:
        f = open ("./html" + file_name, "rb")
    else:  # try成功执行else，否则执行except
        content = f.read()
        f.close()
        response = "HTTP/1.1 200 OK\r\n"
        respnose += "\r\n"
        new_socket.send(response.encode("UTF-8")
        new_socket.send(content)  # 可以分开发送而不用一起
    excpet:
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += "\r\n"
        response += "file not found"
    new_socket.close()
```

### 并发web服务器
1. 多进程服务器,监听套接字创建后，多线程则不需要`new_socket.close()`
```
while True:
    new_socket, client_addr = tcp_server_socket.accept()
    p = multiprocessing.Process(targer=response_html, args=(new_socket))
    p.start()
    new_socket.close()  # linux中新的进程（子进程）中new_socket被复制出来时指向同一个文件描述符fd，需要再次调用close（）才能真正关闭。
```

### 非堵塞实现并发的原理，原来tcp_server.accept()在接收到一个client的请求后会让后来的client处于等待中，而非阻塞则接收所有的client。

```python
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.setblocking(False)  # 设置套接字为非堵塞
client_list = list()
while True:
    time.sleep(0.5)  # 测试用，间隔运行而非一直运行
    try:
        # 阻塞时若没有客户端请求程序会卡在accept()而不向下执行，循环处于停止状态，改为非阻塞后没有请求accept()也会被执行，循环处于一直运行的状态，但此时是None，会出错，所以用try。
        newcreated_socket, new_addr = tcp_server.accept()  
    except Exception as ret:
        print("no new client connected")
    else:
        print("new client")
        newcreated_socket.setblocking(False)  # 上边生成的套接字设为非堵塞
        client_list.append(new_created_socket)
    # 上一部分用来连接新加入的客户端，下一部分用来遍历这些客户端并为每个客户端服务。
    for ser_for_client in client_list:
        try:
            data = ser_for_client.recv(1024)
        except Exception as retv:
            print("no new data received")
            print("error %s" % retv)
        else:  
            if data:
                print("now do something with new data")
            else:
                # client调用了close
                client_list.remove(ser_for_client)
                ser_for_client.close()
```
 
### HTTP协议的短连接：多次建立连接、数据传输、关闭连接。长连接保持数据传输
长连接时不知道服务器发送过来的数据有没有发完，会一直等待，浏览器就会一直转圈
而不渲染内功，因此加上
`response.header += "Content-length: %d\r\n" % (len(response_body))`
 
而短连接会发送close，服务器也会发来close，这样就知道服务器数据发完了。
 
### epoll技术，实现服务器的高并发（用在ngix中）
> 与内核共享一部分特殊的内存空间（数据不需要从用户内存复制到内核中），以事件通知（客户端数据来了就告诉相应的服务器对象接收数据）而非轮询（从第一个服务器对象遍历到最后一个对象，看它是否接收数据）的方式告诉服务器接收客户端请求
 
```python
import select
tcp_server = socket.socket(...)
tcp_server.bind()
tcp_server.listen(128)
tcp_server.setblocking(False)

epl = select.epoll()
epl.register(tcp_server.fileno(), select.EPOLLIN)  # 将监听套接字对应的fd注册到epl中, select.EPOLLIN表示等待外界传输数据
fd_event_dict = {}
while True:
    fd_event_list = epl.poll()  # 默认堵塞， os检测到数据到来，通过事件通知解堵塞，其值是多个元组(每个元祖2个元素）形成的列表。
    for fd, event in fd_event_list:
        if fd == tcp_server.filno():
            new_socket, addr = tcp_server.accept()
            epl.register(new_socket.fileno(), slect.EPOLLIN)
            fd_event_dict[new_socket.fileno()] = new_socket
        elif event == select.EPOLLIN:
            recv_data = fd_event_dict[fd].recv(1024).decode("UTF-8")
            if recv_data:
                pass
            else:
                fd_event_dict[fd].close()
                epl.unregister(fd)
                del fd_event_dict[fd]
tcp_server.close()        
```

### 网络通信过程
wireshark抓包工具

最早：集线器（hub),连接少数几台，以广播发送数据，会阻塞。
网卡-唯一的物理地址（mac地址），数据要经过网卡，否则即使IP对，也会丢弃数据。除了网卡本身地址，还有地址FF：FF：FF：FF：FF：FF地址是能接收数据的。
发送者电脑进行arp广播给所有电脑，有目标IP的电脑返回数据以及其mac地址，达成两台电脑间单独通信。
后来：交换机，并没有网卡，只有将各个电脑连接的作用？
更复杂的广播： 路由器（router）（能转发数据，相当于代理，又叫网关），连接不同网络的电脑，至少有2个网卡，数据发送的mac地址为路由器的1张网卡，路由器再转发到另一张网卡并发给目标地址来获得目标mac地址。

访问网络服务器：
1. 电脑先发送请求给默认网关（知道其mac地址），通过cloud，到DNS服务器。
2. DNS服务器解析域名对应的IP地址到电脑。
3. 电脑再连接到http服务器
4. 传输过程中目标IP不变， mac地址在不断变化。
