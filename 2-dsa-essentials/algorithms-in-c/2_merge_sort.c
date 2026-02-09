#include <stdio.h>

void merge(int A[], int p, int q, int r) {
    int n_L = q - p + 1;
    int n_R = r - q;

    // Create temporary arrays
    int L[n_L], R[n_R];

    // Copy data to temp arrays L[] and R[]
    for (int i = 0; i < n_L; i++)
        L[i] = A[p + i];
    for (int j = 0; j < n_R; j++)
        R[j] = A[q + 1 + j];

    int i = 0, j = 0, k = p;

    // Merge the temp arrays back into A[p..r]
    while (i < n_L && j < n_R) {
        if (L[i] <= R[j]) {
            A[k] = L[i];
            i++;
        } else {
            A[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy remaining elements of L[], if any
    while (i < n_L) {
        A[k] = L[i];
        i++;
        k++;
    }

    // Copy remaining elements of R[], if any
    while (j < n_R) {
        A[k] = R[j];
        j++;
        k++;
    }
}

void mergeSort(int A[], int p, int r) {
    if (p >= r) return;
    
    int q = p + (r - p) / 2; // Equivalent to floor((p+r)/2)
    mergeSort(A, p, q);
    mergeSort(A, q + 1, r);
    merge(A, p, q, r);
}

int main() {
    int A[] = {12, 11, 13, 5, 6, 7};
    int n = sizeof(A) / sizeof(A[0]);

    mergeSort(A, 0, n - 1);

    printf("Sorted array: ");
    for (int i = 0; i < n; i++) printf("%d ", A[i]);
    return 0;
}