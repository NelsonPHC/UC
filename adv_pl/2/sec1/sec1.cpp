// Error introduced: removed the semicolon after total += arr[i].

#include <iostream>
using namespace std;

int calculateSum(int arr[], int size) {
    int total = 0;
    for (int i = 0; i < size; i++) {
        total += arr[i]
    }
    return total;
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    int result = calculateSum(numbers, size);
    cout << "Sum in C++: " << result << endl;
    return 0;
}



// Error message:

// main.cpp: In function ‘int calculateSum(int*, int)’:
// main.cpp:8:24: error: expected ‘;’ before ‘}’ token
//     8 |         total += arr[i]
//       |                        ^
//       |                        ;
//     9 |     }
//       |     ~     

