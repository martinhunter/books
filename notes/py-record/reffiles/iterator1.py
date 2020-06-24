class Iter(object):
    '''这是一个迭代器，有__iter__和__next__方法'''
    def __init__(self, num=10):
        self.num = num
        self.cur_num = 0
        self.a = 0
        self.b = 1


    def __iter__(self):
        '''需要返回一个可迭代对象,即返回值拥有__iter__方法（不管有没有__next__）'''
        return self


    def __next__(self):
        if self.cur_num < self.num:
            ret = self.a
            self.a, self.b = self.b, self.a + self.b
            self.cur_num += 1
            return ret
        else:
            raise StopIteration


fibo = Iter()
for num in fibo:
    print(num)
