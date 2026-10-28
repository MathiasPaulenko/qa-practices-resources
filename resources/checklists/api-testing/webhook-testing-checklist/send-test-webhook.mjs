import { sign } from "./webhook-verify.mjs";

const SECRET = process.env.WEBHOOK_SECRET || "whsec_test_secret";
const URL_ = process.env.WEBHOOK_URL || "http://localhost:3000/webhooks";

/**
 * Sends one signed webhook delivery. `--resend` replays the same event ID so
 * you can watch the deduplication path return `duplicate` instead of `accepted`.
 */
export async function send({ id, body }) {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const signature = sign({ body, id, timestamp, secret: SECRET });

  const res = await fetch(URL_, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "webhook-id": id,
      "webhook-timestamp": timestamp,
      "webhook-signature": signature,
    },
    body,
  });
  return res.status;
}

const isCli = process.argv[1] && process.argv[1].endsWith("send-test-webhook.mjs");
if (isCli) {
  const id = `evt_${Date.now()}`;
  const body = JSON.stringify({ type: "invoice.paid", data: { amount: 1999 } });
  const resend = process.argv.includes("--resend");

  const first = await send({ id, body });
  console.log(`first delivery  → ${first}`);
  if (resend) {
    const second = await send({ id, body });
    console.log(`replay same id  → ${second} (expected 200 duplicate)`);
  }
}
