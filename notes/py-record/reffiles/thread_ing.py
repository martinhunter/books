import threading
import time


class Nth(threading.Thread):
    def fun1(self):
    # 可以换成udp接收数据的函数
    for i in range(4):
        print("func1 running\n")
        time.sleep(1)


    def fun2(self, ras):
    # 可以换成udp发送数据的函数
    for i in range(ras):
        print("func2 running\n")
        time.sleep(1)
        
        
    def run(self):
        self.fun1()
        self.fun2(4)
        
        
def mainNth():
    autorun = Nth()
    autorun.start()  # 此时autorun会自动调用Nth类中的run方法,run中的所有函数被当做线程
    
# ***********************************以上是方法1
    
    
def fun1():
    # 可以换成udp接收数据的函数
    for i in range(4):
        print("func1 running\n")
        time.sleep(1)


def fun2(ras):
    # 可以换成udp发送数据的函数
    for i in range(ras):
        print("func2 running\n")
        time.sleep(1)


def main():
    t1 = threading.Thread(target=fun1)
    t2 = threading.Thread(target=fun2, args=(6,))
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()
