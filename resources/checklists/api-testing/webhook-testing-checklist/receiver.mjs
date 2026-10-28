import http from "node:http";
import { verifySignature } from "./webhook-verify.mjs";

const SECRET = process.env.WEBHOOK_SECRET || "whsec_test_secret";

// Processed event IDs live here; a production receiver would use a datastore
// with a retention window longer than the provider's retry schedule.
const processedIds = new Set();

export function createReceiver() {
  return http.createServer((req, res) => {
    if (req.method !== "POST" || req.url !== "/webhooks") {
      res.writeHead(405).end();
      return;
    }

    let raw = "";
    req.on("data", (chunk) => (raw += chunk));
    req.on("end", () => {
      const id = req.headers["webhook-id"];
      const timestamp = req.headers["webhook-timestamp"];
      const signature = req.headers["webhook-signature"];

      const ok = verifySignature({
        rawBody: raw,
        signatureHeader: signature,
        timestamp,
        id,
        secret: SECRET,
      });
      if (!ok) {
        res.writeHead(401).end("invalid signature");
        return;
      }

      if (processedIds.has(id)) {
        res.writeHead(200).end("duplicate");
        return;
      }

      let event;
      try {
        event = JSON.parse(raw);
      } catch {
        res.writeHead(400).end("malformed payload");
        return;
      }

      processedIds.add(id);
      // ACK first, process async — enqueue `event` here in a real receiver.
      res.writeHead(200).end("accepted");
      setImmediate(() => handleEvent(event));
    });
  });
}

function handleEvent(event) {
  // Replace with real side effects. Kept as a log so the lab stays side-effect free.
  console.log("processed event:", event.type);
}

if (process.argv[1] && process.argv[1].endsWith("receiver.mjs")) {
  createReceiver().listen(3000, () => {
    console.log("webhook receiver on http://localhost:3000/webhooks");
  });
}
