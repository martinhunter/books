import multiprocessing
import time
'''进程之间传递数据'''


def fun1(q):
    for i in range(4):
        print("func1 running\n")
        q.put(i)
        time.sleep(1)


def fun2(q):
    for i in range(4):
        data = q.get()  # 会按传入的顺序获得数据
        print("get data: %d" % data)


def main():
    print('running')
    q = multiprocessing.Queue(3)  # q.put最多3个
    t1 = multiprocessing.Process(target=fun1, args=(q,))
    t2 = multiprocessing.Process(target=fun2, args=(q,))
    t1.start()
    t2.start()


if __name__ == "__main__":
    main()
