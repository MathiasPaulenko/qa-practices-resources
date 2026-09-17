package support;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Shop {
    private final Map<String, Integer> catalog = new HashMap<>();
    private final Map<String, Integer> cart = new HashMap<>();

    public void stockProduct(String name, int price, int units) {
        catalog.put(name, price);
    }

    public void clearCart() {
        cart.clear();
    }

    public void addToCart(String name) {
        cart.merge(name, 1, Integer::sum);
    }

    public int itemCount() {
        return cart.values().stream().mapToInt(Integer::intValue).sum();
    }

    public void createOrder(List<Map<String, String>> rows) {
        cart.clear();
        rows.forEach(row -> cart.merge(
            row.get("product"),
            Integer.parseInt(row.get("quantity")),
            Integer::sum));
    }

    public int total() {
        return cart.entrySet().stream()
            .mapToInt(e -> catalog.getOrDefault(e.getKey(), 0) * e.getValue())
            .sum();
    }

    public String totalFormatted() {
        return String.format("$%d.00", total());
    }
}
