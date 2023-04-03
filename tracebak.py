def f1():
    print('>> f1()')
    10 / 0
    
def f2():
    print('>> f2()')
    f1()
    
def f3():
    print('>> f3()')
    f2()
    
if __name__ == '__main__':
    f3()
