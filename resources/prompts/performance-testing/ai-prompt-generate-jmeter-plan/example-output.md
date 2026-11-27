Assumptions

- Order IDs are returned as JSON `{ "orderId": "..." }` and extracted with a JSON Extractor into `${orderId}`.
- Login happens once per thread at start; the token lives for the whole run.
- GET /products is browsed 3x more often than orders are placed.

## Thread group: checkout-load

- Threads: 500 | Ramp-up: 300 s | Duration: 1 500 s | Loop: infinite until end

## Config elements

- HTTP Request Defaults: staging.orderhub.io, HTTPS, timeout 10 s
- HTTP Header Manager: Content-Type: application/json
- CSV Data Set Config: users.csv, variables username,password, Recycle on EOF

## Samplers

1. HTTP POST /auth/login — once per thread via Once Only Controller; extract token with JSON Extractor (`$.token` -> `${jwt}`).
2. HTTP GET /products?category=electronics — Header `Authorization: Bearer ${jwt}`; weight 3.
3. HTTP POST /orders — body uses `${productId}` extracted above; weight 1; assert 201 + save `${orderId}`.
4. HTTP GET /orders/${orderId} — assert status field = "confirmed" or "processing" within 5 s polling.

## Timers

- Uniform Random Timer: 1 000-3 000 ms on samplers 2-4.

## Assertions

- Response code = expected per sampler.
- Duration assertion: 800 ms on samplers 2-4 (log-only during debug).
- JSON assertion on orderId presence for sampler 3.

## Listeners

- Debug run: View Results Tree + Summary Report.
- Load run: none in the plan; write results.jtl and generate the HTML report afterwards.

## Execution

```bash
jmeter -n -t orderhub-checkout.jmx -l results.jtl -e -o report/
```

Start with a 10-user, 2-minute smoke run before the full 500.

## Validation checklist

- Every thread logged in once (check jtl for 500 login rows).
- No 401s after login (token reuse works).
- orderId correlation: zero unresolved `${orderId}` in request paths.
- Error rate < 1% during the sustained window, not only at the end.
