# Example Output Fragment

## Executable operations

```graphql
query GetOrderById($id: ID!) {
  order(id: $id) {
    ...OrderTestFields
  }
}

query ListOrders($status: OrderStatus, $first: Int) {
  orders(status: $status, first: $first) {
    ...OrderTestFields
  }
}

mutation UpdateOrderStatus($id: ID!, $status: OrderStatus!) {
  updateOrderStatus(id: $id, status: $status) {
    ...OrderTestFields
  }
}

fragment OrderTestFields on Order {
  id
  number
  status
  totalCents
  currency
  customer {
    id
    email
  }
  items {
    productId
    quantity
    unitPriceCents
  }
}
```

## Coverage matrix and review notes

```text
| ID | Scenario | Variables | Expected result |
| --- | --- | --- | --- |
| GQL-01 | Customer reads own paid order | {"id":"ord_1001"} | HTTP 200; data.order.status = PAID; errors absent |
| GQL-02 | Customer reads another user's order | {"id":"ord_2002"} | data.order null or authorization error, per documented rule; no customer email exposed |
| GQL-03 | Unknown order ID | {"id":"ord_missing"} | HTTP 200; data.order = null; errors absent |
| GQL-04 | Invalid enum in mutation | {"id":"ord_1001","status":"REFUNDED"} | validation error; data absent or null; mutation not executed |
| GQL-05 | Pagination lower boundary | {"status":"PAID","first":1} | at most one order returned; no validation error |
| GQL-06 | Unsupported pagination size | {"status":"PAID","first":51} | documented validation or business error; no unbounded result set |

Review notes: the SDL does not define whether unauthorized access returns null or an error, so GQL-02 is a schema question. Treat email as sensitive data; assert it only when the role is allowed to see it.
```
