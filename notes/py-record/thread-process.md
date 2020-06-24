### udp、tcp传输时转码
send("str".encode("UTF-8"),address)
recv(data.decode("UTF-8"))

### 多线程（实际对代码实行操作）
继承threading.Thread类，在新类中重写run方法,参考[thread][lk1]

[lk1]: https://github.com/martinhunter/py-record/tree/master/reffiles/thread_ing.py

避免死锁（两个线程分别占有一部分资源并等待对方的资源）：
1. 添加超时时间。
2. 银行家算法来避免这个问题（先每个人借少量钱，先收回借钱少的人的钱，再给与需要钱更多的人。）即规定各个锁的释放先后时间。

### 多进程（资源分配）
代码写时拷贝

### queue队列： multiprocessing.Queue 完成进程间通信，例如socket 
一个进程产生数据，通过queue传递给另一个进程
参考[process][lk2]

[lk2]: https://github.com/martinhunter/py-record/tree/master/reffiles/multi_processing.py

### 进程池 multiprocessing.Pool,用来生成多个进程代替multingprocessing.Process
```python
po = Pool(3)  # 3 process running at most simultaneously,others will wait
for i in range(10):
    po.apply_async(funcname, (args,))
po.close()  # after 10 process object created,will not receive requests to create more process
po.join()  # wait till these 10 process finish their work

# pool will replace the following code 
# process1 = multiprocessing.Process(target=funcname,(args,))
# process1.start()
```
### 协程，是并发任务，C++中没有，利用迭代器实现
参考[iterator][lk3]

[lk3]: https://github.com/martinhunter/py-record/tree/master/reffiles/iterator1.py
生成器（一种迭代器）： 将函数中的return换成yield，运行时创建了一个生成器对象
> 保证函数执行一部分便返回

```
gen_obj = generator_function(args)  
next_value = next(gen_obj)  # next_value = 第一次到达yield后边的值，yield value整个 = None
generate_next_value = gen_obj.send(args)  # yield value整个 = args "generate_next_value依然返回yield后边的值"
```
使用yield实现多任务,交替进行

    def func1(args):
        while True:
            pass
            yield
    def func2(args):
        while True:
            pass
            yield
    def main():
        t1 = func1(args)
        t2 = func2(args)
        while True:
            next(t1)
            next(t2)
使用greenlet.greenlet替换yield,但若有延时(例如time.sleep(0.5)这两种方法都会等待而不切换。还是人工切换

    def func1(args):
        while True:
            pass
            gre2.switch()
    def func2(args):
        while True:
            pass
            gre1.switch()
    def main():
        gre1 = greenlet(func1)
        gre2 = greenlet(func2)
        gre1.switch()
使用gevent替换greenlet,中间有I/O等费时操作就会自动并迅速切换协程

    import gevent
    from gevent import monkey
    monkey.patch_all()  # 将程序中用到的耗时操作的代码（time.sleep)换为gevent中自己实现的模块
    def func1(args1):
        while True:
            pass
            print（"func1 running"）
            time.sleep(0.5)
    def func2(args2):
        while True:
            pass
            print（"func2 running"）
            time.sleep(0.5)
    def main():
        gev1 = gevent.spawn(func1， args1)
        gev2 = gevent.spawn(func2， args2)
        gev1.join()
        gev2.join()
        gevent.joinall([gev1, gev2])  # join可替换为joinall
