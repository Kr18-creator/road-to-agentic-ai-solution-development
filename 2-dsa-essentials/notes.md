# Essentials of Algorithms and Data Structure

## Why Algorithmic Thinking?

- *"An Algorithm is any well-defined computational procedure that takes some value, or set of values, as input and produces some value, or set of values, as output in a finite amount of time. An algorithm is thus a sequence of computational steps that transform the input into the output."*
- It can be viewed as a tool for solving well-specified computational problem.
- Example:
    - **Problem:** Sort a sequence of numbers into monotonically increasing order.
    - **Input:** A Sequence of n numbers: $<a_1, a_2, ...., a_n>$
    - **Output:** A Permutation or a eordering: $<a_1', a_2',....,a_n'>$
    - **Instance**: Given $<31, 41, 59, 26, 41, 58>$, the output should be $<26, 31, 41, 41, 58, 59>$

## Let's Begin

### Insertion Sort

```
Insertion-Sort(A,n)

1 for i = 2 to n
2     key = A[i]
3     // Insert A[i] into the sorted aubarray A[1:i-1]
4     j = i - 1
5     while j > 0 and A[j] > key
6         A[j + 1] = A[j]
7         j = j - 1
8     A[j + 1] = key
```

A **Loop Invariant** is a formal way to prove that an algorithm works correctly. It is a statement or condition that is true before and after each iteration of a loop.

Think of it like a "truth" that never changes, even as the data within the loop is being moved around. If you can prove the invariant holds true at the start, middle, and end, you’ve mathematically proven your loop does what it's supposed to do.

To use a loop invariant to prove correctness, you must satisfy three specific conditions:
1. **Initialization:** It is true prior to the first iteration of the loop.
2. **Maintenance:** If it is true before an iteration of the loop, it remains true before the next iteration.
3. **Termination:** When the loop terminates, the invariant gives us a useful property that helps show that the algorithm is correct.


#### Analysis of Algorithm

1. Cost: $c_1$, times: $n$
2. Cost: $c_2$, times: $n-1$
3. Cost: 0, time: $n-1$
4. Cost: $c_4$, times: $n-1$
5. Cost: $c_5$, times: $\sum_{i=2}^{n}t_i$
6. Cost: $c_6$, times: $\sum_{i=2}^{n}(t_i - 1)$
7. Cost: $c_7$, times: $\sum_{i=2}^n(t_i-1)$
8. Cost: $c_8$, times: $n-1$

**Best Case Running Time:** $T(n) = c_1n + c_2(n-1) + c_4(n-1) + c_5(\sum_{i=2}^nt_i) + c_6(\sum_{i=2}^n(t_i - 1)) + c_7(\sum_{i=2}^n(t_i-1)) + c_8(n-1)$

### Merge Sort

```
MERGE(A, p, q, r)
n_L = q - p + 1
n_R = r - q
let L[0:n_L-1] and R[0:n_R-1] be new arrays
for i = 0 to n_L - 1
    l[i] = A[p+i]
for j = 0to n_R - 1
    R[j] = A[q + j + 1]
i = 0
j = 0
k = p

while i < n_L and j < n_R
    if L[i] <= R[j]
        A[k] = L[i]
        i = i + 1
    else A[k] = R[j]
        j = j + 1
    k = k + 1

while i < n_L
    A[k] = L[i]
    i = i + 1
    k = k + 1
while j < n_R
    A[k] = R[j]
    j = j + 1
    k = k + 1


MERGE-SORT(A, p, r)
if p >= r
    return
q = [(p + r)/2]
MERGE-SORT(A, p, q)
MERGE-SORT(A, q+1, r)
MERGE(A, p, q, r)

```