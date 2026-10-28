import crypto from "node:crypto";

export const TOLERANCE_SECONDS = 300;

/**
 * Verifies a Standard-Webhooks-style signature:
 * header `webhook-signature: v1,<base64-hmac>` over `${id}.${timestamp}.${rawBody}`.
 */
export function verifySignature({
  rawBody,
  signatureHeader,
  timestamp,
  id,
  secret,
  now = Date.now(),
}) {
  if (!signatureHeader || !timestamp || !id || !secret) return false;

  const age = Math.abs(now / 1000 - Number(timestamp));
  if (!Number.isFinite(age) || age > TOLERANCE_SECONDS) return false;

  const expected = crypto
    .createHmac("sha256", secret)
    .update(`${id}.${timestamp}.${rawBody}`)
    .digest("base64");

  return signatureHeader.split(" ").some((sig) => {
    const value = sig.replace(/^v1,/, "");
    return (
      value.length === expected.length &&
      crypto.timingSafeEqual(Buffer.from(value), Buffer.from(expected))
    );
  });
}

/**
 * Signs a payload the same way the verifier expects — used by the test client
 * to produce real signed deliveries.
 */
export function sign({ body, id, timestamp, secret }) {
  const sig = crypto
    .createHmac("sha256", secret)
    .update(`${id}.${timestamp}.${body}`)
    .digest("base64");
  return `v1,${sig}`;
}
