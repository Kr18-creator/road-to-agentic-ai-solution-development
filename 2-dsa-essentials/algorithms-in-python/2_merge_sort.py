def merge(A, p, q, r):
    n_L = q - p + 1
    n_R = r - q
    
    # Create new lists for L and R
    L = [0] * n_L
    R = [0] * n_R
    
    for i in range(n_L):
        L[i] = A[p + i]
    for j in range(n_R):
        R[j] = A[q + 1 + j]
        
    i = 0
    j = 0
    k = p
    
    while i < n_L and j < n_R:
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1
        k += 1
        
    # Copy remaining elements
    while i < n_L:
        A[k] = L[i]
        i += 1
        k += 1
    while j < n_R:
        A[k] = R[j]
        j += 1
        k += 1

def merge_sort(A, p, r):
    if p >= r:
        return
    
    # Using floor division // for integer result
    q = (p + r) // 2
    
    merge_sort(A, p, q)
    merge_sort(A, q + 1, r)
    merge(A, p, q, r)

# Example usage:
arr = [12, 11, 13, 5, 6, 7]
merge_sort(arr, 0, len(arr) - 1)
print("Sorted array:", arr)