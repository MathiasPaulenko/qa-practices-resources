import java.util.concurrent.atomic.AtomicInteger;

/**
 * Same contract as UnsafeInventory, but check-and-decrement is atomic.
 * Run the same stress harness against this class to see the race disappear.
 */
public class SafeInventory {

    private final AtomicInteger stock;

    public SafeInventory(int stock) {
        this.stock = new AtomicInteger(stock);
    }

    public boolean tryBuy() {
        while (true) {
            int current = stock.get();
            if (current <= 0) {
                return false;
            }
            if (stock.compareAndSet(current, current - 1)) {
                return true;
            }
        }
    }

    public int stock() {
        return stock.get();
    }
}
