// Rust: ownership & borrowing - no GC, no manual free, memory-safety enforced at compile time.

struct Buffer {
    data: Vec<i32>,
}

fn take_ownership(buf: Buffer) {
    println!("Owned buffer len: {}", buf.data.len());
} // buf dropped here -> heap memory freed automatically

fn borrow_buffer(buf: &Buffer) {
    println!("Borrowed buffer sum: {}", buf.data.iter().sum::<i32>());
} // borrow ends, no drop (doesn't own it)

fn main() {
    let buf1 = Buffer { data: vec![1, 2, 3, 4, 5] }; // heap alloc

    borrow_buffer(&buf1);      // immutable borrow, buf1 still valid after
    println!("Still usable: {:?}", buf1.data);

    take_ownership(buf1);      // ownership MOVED into function
    // println!("{:?}", buf1.data); // would NOT compile: use after move (compiler prevents dangling access)

    let mut buf2 = Buffer { data: vec![10, 20, 30] };
    {
        let r = &mut buf2;     // mutable borrow, scoped
        r.data.push(40);
    } // borrow ends here
    println!("buf2 after scoped mutation: {:?}", buf2.data);
} // buf2 dropped automatically, memory freed, no leak, no double free possible
