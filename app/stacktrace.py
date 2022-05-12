def f1():
    print('>> running f1()')

    10 / 0


def f2():
    print('>> running f2')
    f1()


def f3():
    print('>> running f3')
    f2()


f3()

