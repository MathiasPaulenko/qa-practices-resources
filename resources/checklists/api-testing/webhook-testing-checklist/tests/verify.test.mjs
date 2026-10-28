import test from "node:test";
import assert from "node:assert/strict";
import { verifySignature, sign, TOLERANCE_SECONDS } from "../webhook-verify.mjs";
import { createReceiver } from "../receiver.mjs";

const SECRET = "whsec_test_secret";
const BODY = JSON.stringify({ type: "invoice.paid", data: { amount: 1999 } });
const ID = "evt_01JTEST";
const NOW = 1_760_000_000_000; // fixed clock for deterministic tests

function freshTimestamp() {
  return Math.floor(NOW / 1000).toString();
}

test("accepts a correctly signed request", () => {
  const timestamp = freshTimestamp();
  const header = sign({ body: BODY, id: ID, timestamp, secret: SECRET });
  assert.equal(
    verifySignature({ rawBody: BODY, signatureHeader: header, timestamp, id: ID, secret: SECRET, now: NOW }),
    true,
  );
});

test("rejects a tampered payload", () => {
  const timestamp = freshTimestamp();
  const header = sign({ body: BODY, id: ID, timestamp, secret: SECRET });
  const tampered = BODY.replace("1999", "1");
  assert.equal(
    verifySignature({ rawBody: tampered, signatureHeader: header, timestamp, id: ID, secret: SECRET, now: NOW }),
    false,
  );
});

test("rejects a signature computed for a different event", () => {
  const timestamp = freshTimestamp();
  const header = sign({ body: BODY, id: ID, timestamp, secret: SECRET });
  assert.equal(
    verifySignature({ rawBody: BODY, signatureHeader: header, timestamp, id: "evt_other", secret: SECRET, now: NOW }),
    false,
  );
});

test("rejects timestamps outside the tolerance window", () => {
  const stale = (Math.floor(NOW / 1000) - TOLERANCE_SECONDS - 60).toString();
  const header = sign({ body: BODY, id: ID, timestamp: stale, secret: SECRET });
  assert.equal(
    verifySignature({ rawBody: BODY, signatureHeader: header, timestamp: stale, id: ID, secret: SECRET, now: NOW }),
    false,
  );
});

test("rejects missing headers and wrong secrets", () => {
  const timestamp = freshTimestamp();
  const header = sign({ body: BODY, id: ID, timestamp, secret: SECRET });
  assert.equal(
    verifySignature({ rawBody: BODY, signatureHeader: "", timestamp, id: ID, secret: SECRET, now: NOW }),
    false,
  );
  assert.equal(
    verifySignature({ rawBody: BODY, signatureHeader: header, timestamp, id: ID, secret: "wrong", now: NOW }),
    false,
  );
});

test("receiver returns 200 for accepted, duplicate stays 200 without reprocessing", async () => {
  const server = createReceiver();
  await new Promise((r) => server.listen(0, r));
  const port = server.address().port;

  const timestamp = Math.floor(Date.now() / 1000).toString();
  const id = "evt_dup_test";
  const signature = sign({ body: BODY, id, timestamp, secret: SECRET });
  const headers = {
    "content-type": "application/json",
    "webhook-id": id,
    "webhook-timestamp": timestamp,
    "webhook-signature": signature,
  };

  const first = await fetch(`http://localhost:${port}/webhooks`, { method: "POST", headers, body: BODY });
  const second = await fetch(`http://localhost:${port}/webhooks`, { method: "POST", headers, body: BODY });

  assert.equal(first.status, 200);
  assert.equal(await first.text(), "accepted");
  assert.equal(second.status, 200);
  assert.equal(await second.text(), "duplicate");

  server.close();
});

test("receiver returns 401 for an unsigned request", async () => {
  const server = createReceiver();
  await new Promise((r) => server.listen(0, r));
  const port = server.address().port;

  const res = await fetch(`http://localhost:${port}/webhooks`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: BODY,
  });
  assert.equal(res.status, 401);

  server.close();
});
