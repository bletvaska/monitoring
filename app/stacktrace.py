#!/usr/bin/env python3

def f3():
    print(">> f3")
    raise Exception('Failure')


def f2():
    print(">> f2")
    f3()


def f1():
    print(">> f1")
    f2()

f1()

