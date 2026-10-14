import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Two demos that force race-condition interleavings on purpose.
 *
 *   javac *.java && java RaceDemo
 *
 * Java 17+. No dependencies.
 */
public class RaceDemo {

    public static void main(String[] args) throws InterruptedException {
        lostUpdateDemo();
        oversellDemo();
    }

    /** A plain counter shared by 8 threads loses updates. */
    static void lostUpdateDemo() throws InterruptedException {
        int threads = 8;
        int incrementsPerThread = 50_000;
        UnsafeCounter counter = new UnsafeCounter();
        CountDownLatch gate = new CountDownLatch(1);
        Thread[] workers = new Thread[threads];

        for (int i = 0; i < threads; i++) {
            workers[i] = new Thread(() -> {
                try { gate.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                for (int j = 0; j < incrementsPerThread; j++) counter.increment();
            });
            workers[i].start();
        }
        gate.countDown(); // all threads fire at the same instant
        for (Thread t : workers) t.join();

        long expected = (long) threads * incrementsPerThread;
        System.out.printf("Counter: expected %d, got %d -> %d lost updates%n",
                expected, counter.value(), expected - counter.value());
    }

    /** Two buyers race for the last unit; loop until an oversell appears. */
    static void oversellDemo() throws InterruptedException {
        int oversells = 0;
        int rounds = 20_000;

        for (int round = 0; round < rounds; round++) {
            UnsafeInventory inventory = new UnsafeInventory(1);
            CountDownLatch gate = new CountDownLatch(1);
            CountDownLatch done = new CountDownLatch(2);
            AtomicInteger winners = new AtomicInteger();

            Runnable buyer = () -> {
                try { gate.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                if (inventory.tryBuy()) winners.incrementAndGet();
                done.countDown();
            };
            new Thread(buyer).start();
            new Thread(buyer).start();
            gate.countDown();
            done.await();

            if (winners.get() > 1) oversells++;
        }
        System.out.printf("Oversell: %d rounds out of %d sold the same unit twice%n", oversells, rounds);
        System.out.println("Now swap UnsafeInventory for SafeInventory and watch both numbers go to zero.");
    }

    static class UnsafeCounter {
        private int value;
        void increment() { value++; } // read-modify-write, not atomic
        long value() { return value; }
    }
}
