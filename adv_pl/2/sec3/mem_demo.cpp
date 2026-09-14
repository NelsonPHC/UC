// C++: manual memory management — programmer controls new/delete

#include <iostream>
#include <memory>

struct Buffer {
    int* data;
    size_t size;
    Buffer(size_t n) : data(new int[n]), size(n) { std::cout << "allocated " << n << " ints\n"; }
    ~Buffer() { delete[] data; std::cout << "freed buffer\n"; }
};

int* make_dangling() {
    int local = 42;
    return &local; // returning address of a stack var
} // 'local' destroyed when function returns

void leak_example() {
    int* leaked = new int[1000];
    (void)leaked;                // memory leak: allocated and never deleted
}

int main() {
    // 1. Correct manual management
    Buffer* buf = new Buffer(5);
    buf->data[0] = 100;
    std::cout << "buf->data[0] = " << buf->data[0] << "\n";
    delete buf; // be sure to free, or it leaks

    // 2. Dangling pointer (undefined behavior if dereferenced)
    int* dangling = make_dangling();
    std::cout << "dangling pointer value (UB, may look valid): " << *dangling << "\n";

    // 3. Deliberate leak (would show up in a memory profiler)
    leak_example();

    // 4. RAII fix: smart pointer manages lifetime automatically
    {
        std::unique_ptr<Buffer> safe = std::make_unique<Buffer>(3);
        safe->data[0] = 7;
        std::cout << "smart-pointer buffer[0] = " << safe->data[0] << "\n";
    } // destructor runs automatically here, no leak possible

    return 0;
}
