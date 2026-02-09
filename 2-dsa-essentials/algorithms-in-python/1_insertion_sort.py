def insertion_sort(A):
    # n is the length of the list
    n = len(A)
    
    # Range starts from 1 (the second element) to n-1
    for i in range(1, n):
        key = A[i]
        
        # Insert A[i] into the sorted subarray A[0:i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j = j - 1
        A[j + 1] = key

# Example usage:
# arr = [5, 2, 4, 6, 1, 2, 3]
arr = [1]
insertion_sort(arr)
print("Sorted array:", arr)