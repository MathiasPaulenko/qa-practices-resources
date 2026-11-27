# Example Output

```text
Assumptions:
- Android and iOS lifecycle callbacks differ, so automation can drive setup and capture evidence but cannot guarantee identical interruption timing.
- The backend treats repeated order creation with the same idempotency key as one logical order.
- Low-battery behavior is manually verified because reliable battery manipulation depends on the device farm.

| Trigger | App state | Timing | Expected during interruption | Recovery expectation | Risk |
|---|---|---|---|---|---|
| Incoming call/system alert | Foreground payment confirmation | After tapping Pay, before result | Payment UI pauses or is obscured; no duplicate submission | Return to pending/result state without charging twice | Critical |
| Network loss | Foreground submission | Request in flight | Retry policy or offline state becomes visible | Reconcile order status after reconnect; no phantom success | Critical |
| Background + process death | Background after payment submission | Before result returns | System may destroy process | Restore pending order state or safely re-query status | Critical |
| Lock/unlock | Foreground biometric step | During biometric prompt | Sensitive data remains protected | Resume biometric step or request authentication again | High |
| Push notification | Form entry | Cart/payment fields partially filled | User can ignore or open notification | Unfinished input is preserved if app remains in memory | Medium |

---

INT-CALL-001 — incoming call after tapping Pay
Priority: Critical
Platform: Android and iOS physical devices
Initial state: signed-in user, cart ready, saved payment token, biometric confirmation completed
Steps:
1. Open checkout in staging.
2. Tap Pay.
3. Trigger an incoming call or system alert before the payment result appears.
4. Decline or dismiss the interruption.
5. Return to ShopFlow.
Expected during interruption: the app doesn't submit duplicate order requests and doesn't display a final success state before the backend result is known.
Recovery assertions:
- ShopFlow returns to payment pending, success, or failure according to GET /orders/{orderId}.
- Backend logs show one logical order for idempotency key checkout-{cartId}.
- Cart is cleared only after confirmed success.
- No crash, ANR, frozen spinner without timeout, or unauthenticated loop.
Cleanup: cancel or void the staging order and remove local cart state.

INT-NET-002 — airplane mode while order creation is in flight
Priority: Critical
Steps: tap Pay, enable airplane mode before the response, wait for timeout, disable airplane mode, reopen checkout.
Expected: the user sees a retryable or pending state, never both “payment failed” and a later silent duplicate order. After reconnecting, the client checks the order status before offering retry.
Backend assertion: repeated submission with checkout-{cartId} doesn't create a second order.

INT-BG-003 — process death after backgrounding during payment
Priority: Critical
Steps: tap Pay, background the app, terminate the process through developer tooling, relaunch the app.
Expected: checkout doesn't restart as if nothing happened. The app restores a pending order, queries status, or explains that confirmation is required.
State assertion: no successful order is shown without a backend status match; no draft card data or token appears in logs.

INT-LOCK-004 — lock and unlock during biometric confirmation
Priority: High
Steps: reach biometric confirmation, lock the device, wait ten seconds, unlock it.
Expected: sensitive checkout data is protected, the app doesn't bypass authentication, and the user can either continue or cancel safely. A second biometric attempt must not create a second order.

INT-NOTIF-005 — push notification while editing delivery instructions
Priority: Medium
Steps: enter delivery notes, receive a push notification, ignore it, then receive another and open it.
Expected: ignored notifications don't affect the draft. Opening a notification may navigate away, but returning must preserve the draft or explicitly restore the checkout state. Silent loss of typed instructions is a defect.
```
