from libcpp.pair cimport pair

cdef extern from "FibonacciHeap.cpp":
    pass

# Declare the class with cdef
cdef extern from "FibonacciHeap.h" namespace "std":
    cdef cppclass Node:
        Node(unsigned int, int, int)
    cdef cppclass FibonacciHeap:
        FibonacciHeap()
        pair[int, int] getMin()
        pair[int, int] extractMin()
        pair[int, bint] getValue(long)
        void push(int, int)
        bint insert(int, int)
        bint decreaseValue(int, int)
        bint deleteNode(int)
        bint empty()
