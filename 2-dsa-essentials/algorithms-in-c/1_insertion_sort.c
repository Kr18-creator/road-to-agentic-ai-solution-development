#include <stdio.h>

void insertionSort(int A[], int n) {
    for (int i = 1; i < n; i++) {
        int key = A[i];
        // Insert A[i] into the sorted subarray A[0...i-1]
        int j = i - 1;

        /* Move elements of A[0..i-1], that are greater than key, 
           to one position ahead of their current position */
        while (j >= 0 && A[j] > key) {
            A[j + 1] = A[j];
            j = j - 1;
        }
        A[j + 1] = key;
    }
}

int main() {
    int A[] = {5, 2, 4, 6, 1, 3};
    int n = sizeof(A) / sizeof(A[0]);

    insertionSort(A, n);

    printf("Sorted array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", A[i]);
    }
    return 0;
}