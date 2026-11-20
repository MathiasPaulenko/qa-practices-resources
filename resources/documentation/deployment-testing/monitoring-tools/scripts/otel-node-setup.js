// OpenTelemetry OTLP tracing setup for Node.js.
// @opentelemetry/sdk-node 0.301.2 + @opentelemetry/exporter-trace-otlp-http 0.301.2
//
// Jaeger accepts OTLP on :4318 since v1.35. For local testing:
//   docker run -p 4318:4318 -p 16686:16686 jaegertracing/all-in-one:1.62
//   OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 node otel-node-setup.js
//
// NOTE: the legacy @opentelemetry/exporter-jaeger package is deprecated in the
// JS SDK — always export via OTLP even when Jaeger is the backend.

const { NodeSDK } = require('@opentelemetry/sdk-node');
const {
  OTLPTraceExporter,
} = require('@opentelemetry/exporter-trace-otlp-http');

const endpoint =
  process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://jaeger:4318';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: `${endpoint}/v1/traces`,
  }),
});

sdk.start();

// Graceful shutdown — without this the last spans of a process are lost.
process.on('SIGTERM', () => {
  sdk
    .shutdown()
    .then(() => console.log('Tracing shut down cleanly'))
    .catch((err) => console.error('Error shutting down tracing', err))
    .finally(() => process.exit(0));
});
