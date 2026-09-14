#include <iostream>
using namespace std;

int add(int a, int b) {
    return a + b;
}

int main() {
    cout << add(5, 3) << endl;       // 8
    // cout << add("5", "3");        // compile error: no matching function
    cout << add(5, '3') << endl;     // 56 (char '3' became its ASCII value 51)
    return 0;
}