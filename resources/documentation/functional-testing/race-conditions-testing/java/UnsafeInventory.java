/**
 * Inventory with a check-then-act race: the stock check and the decrement
 * are not atomic, so two buyers can both pass the check for the last unit.
 */
public class UnsafeInventory {

    private int stock;

    public UnsafeInventory(int stock) {
        this.stock = stock;
    }

    public boolean tryBuy() {
        if (stock > 0) {
            stock--;
            return true;
        }
        return false;
    }

    public int stock() {
        return stock;
    }
}
