from libc.stdlib cimport malloc, realloc, free
from cpython.ref cimport PyObject, Py_INCREF, Py_DECREF

# Array-based Stack using raw C memory

cdef class CArrayStack:
    cdef PyObject** _array
    cdef Py_ssize_t _size
    cdef Py_ssize_t _capacity
    
    def __cinit__(self, Py_ssize_t capacity=16):
        self._capacity = capacity
        self._size = 0
        self._array = <PyObject**>malloc(capacity * sizeof(PyObject*))
        if self._array == NULL:
            raise MemoryError("Failed to allocate stack")
    
    def __dealloc__(self):
        cdef Py_ssize_t i
        # Decrement reference counts before freeing
        for i in range(self._size):
            Py_DECREF(<object>self._array[i])
        free(self._array)
    
    cdef void _resize(self, Py_ssize_t new_capacity):
        self._array = <PyObject**>realloc(self._array, new_capacity * sizeof(PyObject*))
        if self._array == NULL:
            raise MemoryError("Failed to resize stack")
        self._capacity = new_capacity
    
    cpdef void push(self, object value):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        Py_INCREF(value)
        self._array[self._size] = <PyObject*>value
        self._size += 1
    
    cpdef object pop(self):
        cdef object value
        if self._size == 0:
            raise IndexError("Stack is empty")
        self._size -= 1
        value = <object>self._array[self._size]
        Py_DECREF(value)
        return value
    
    cpdef object peek(self):
        if self._size == 0:
            raise IndexError("Stack is empty")
        return <object>self._array[self._size - 1]
    
    cpdef bint is_empty(self):
        return self._size == 0
    
    def __len__(self):
        return self._size


# Linked List Stack using C structs
cdef struct CNode:
    PyObject* value
    CNode* next

cdef class CLinkedListStack:
    cdef CNode* _top
    cdef Py_ssize_t _size
    
    def __cinit__(self):
        self._top = NULL
        self._size = 0
    
    def __dealloc__(self):
        cdef CNode* current = self._top
        cdef CNode* next_node
        while current != NULL:
            next_node = current.next
            Py_DECREF(<object>current.value)
            free(current)
            current = next_node
    
    cpdef void push(self, object value):
        cdef CNode* new_node = <CNode*>malloc(sizeof(CNode))
        if new_node == NULL:
            raise MemoryError("Failed to allocate node")
        Py_INCREF(value)
        new_node.value = <PyObject*>value
        new_node.next = self._top
        self._top = new_node
        self._size += 1
    
    cpdef object pop(self):
        cdef CNode* old_top
        cdef object value
        if self._top == NULL:
            raise IndexError("Stack is empty")
        old_top = self._top
        value = <object>old_top.value
        self._top = old_top.next
        Py_DECREF(value)
        free(old_top)
        self._size -= 1
        return value
    
    cpdef object peek(self):
        if self._top == NULL:
            raise IndexError("Stack is empty")
        return <object>self._top.value
    
    cpdef bint is_empty(self):
        return self._top == NULL
    
    def __len__(self):
        return self._size

# Integer-only Array Stack (no Python object overhead)

cdef class CIntStack:
    """Ultra-fast stack for integers only - no Python object overhead"""
    cdef long* _array
    cdef Py_ssize_t _size
    cdef Py_ssize_t _capacity
    
    def __cinit__(self, Py_ssize_t capacity=16):
        self._capacity = capacity
        self._size = 0
        self._array = <long*>malloc(capacity * sizeof(long))
        if self._array == NULL:
            raise MemoryError("Failed to allocate stack")
    
    def __dealloc__(self):
        free(self._array)
    
    cdef void _resize(self, Py_ssize_t new_capacity):
        self._array = <long*>realloc(self._array, new_capacity * sizeof(long))
        if self._array == NULL:
            raise MemoryError("Failed to resize stack")
        self._capacity = new_capacity
    
    cpdef void push(self, long value):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._array[self._size] = value
        self._size += 1
    
    cpdef long pop(self):
        if self._size == 0:
            raise IndexError("Stack is empty")
        self._size -= 1
        return self._array[self._size]
    
    cpdef long peek(self):
        if self._size == 0:
            raise IndexError("Stack is empty")
        return self._array[self._size - 1]
    
    cpdef bint is_empty(self):
        return self._size == 0
    
    def __len__(self):
        return self._size