// Java: garbage collection — allocation is explicit (new), freeing is automatic & non-deterministic.

import java.util.ArrayList;
import java.util.List;

public class MemoryDemo {

    static class Node {
        int[] payload = new int[100000]; // ~400KB each, heap allocated
    }

    public static void main(String[] args) throws InterruptedException {
        Runtime rt = Runtime.getRuntime();
        report(rt, "start");

        List<Node> nodes = new ArrayList<>();
        for (int i = 0; i < 50; i++) {
            nodes.add(new Node());   // allocate; JVM manages heap
        }
        report(rt, "after allocating 50 nodes");

        nodes.clear();               // drop all references -> eligible for GC
        System.gc();                 // request (not guarantee) collection
        Thread.sleep(200);           // give collector time to run
        report(rt, "after clear() + gc()");

        // Demonstrating a Java "leak": objects kept reachable unintentionally
        List<Node> leaked = new ArrayList<>();
        for (int i = 0; i < 50; i++) {
            leaked.add(new Node());  // still referenced by 'leaked' -> NOT collectible
        }
        report(rt, "after creating unreachable-but-referenced nodes (logical leak)");
    }

    static void report(Runtime rt, String label) {
        long used = (rt.totalMemory() - rt.freeMemory()) / 1024;
        System.out.printf("[%s] used memory: %d KB%n", label, used);
    }
}