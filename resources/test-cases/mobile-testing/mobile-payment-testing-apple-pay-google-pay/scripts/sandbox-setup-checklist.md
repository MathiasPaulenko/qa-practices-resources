# Sandbox setup checklist — mobile payment testing

Before running the payment test cases, verify each environment piece.
Check every line — a missing one is the usual reason a test "fails".

## iOS / Apple Pay

- [ ] Sandbox Apple ID created in App Store Connect → Users and Access → Sandbox Testers.
- [ ] Device signed into the sandbox account under Settings → App Store → Sandbox Account.
- [ ] Merchant ID created in Certificates, Identifiers & Profiles and enabled on the App ID.
- [ ] Apple Pay payment processing certificate uploaded to your PSP or added to `PKPaymentRequest`.
- [ ] Real card added to Wallet (sandbox does not charge it — required anyway).
- [ ] `in-app purchase` products created in App Store Connect with `com.taskflow.*` IDs.
- [ ] App Store Server Notifications webhook URL configured for subscription events.

## Android / Google Pay

- [ ] License test accounts added in Play Console → Setup → License testing.
- [ ] Products created in Play Console with matching `com.taskflow.*` IDs and active states.
- [ ] Google Pay API `environment` set to `TEST` in the payment request JSON.
- [ ] Test card tokenization flow verified through `TokenService` in test mode.
- [ ] Play Integrity / SafetyNet check returns `MEETS_DEVICE_INTEGRITY` on test devices.

## Shared

- [ ] Receipt verification endpoint (`verifyReceipt` / Play Developer API) reachable from CI.
- [ ] Catch-all logging enabled so `pan_in_logs_test.py` can scan the payment flow output.
- [ ] Test devices matrix: Face ID iPhone + fingerprint Android + one low-end device.

## Renewal compression cheat sheet (Apple sandbox)

| Real duration | Sandbox duration |
|---|---|
| 1 week | 3 minutes |
| 1 month | 5 minutes |
| 2 months | 10 minutes |
| 6 months | 30 minutes |
| 1 year | 1 hour |
