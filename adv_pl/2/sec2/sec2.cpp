#include <iostream>
#include <string>

int multiply(int a, int b) {
    return a * b;
}

int main() {
    std::cout << multiply(5, 4) << std::endl; // 20
    // multiply("5", "4"); // Compile-time error
}