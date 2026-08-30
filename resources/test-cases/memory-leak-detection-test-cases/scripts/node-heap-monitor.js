// Monitor heap and RSS over time
// Usage: node node-heap-monitor.js

const durationMs = Number(process.argv[2]) || 30 * 60 * 1000;
const intervalMs = Number(process.argv[3]) || 5000;

const baseline = process.memoryUsage();
console.log('Baseline (MB):');
console.log(`  heapUsed: ${(baseline.heapUsed / 1024 / 1024).toFixed(2)}`);
console.log(`  rss:      ${(baseline.rss / 1024 / 1024).toFixed(2)}`);
console.log(`  external: ${(baseline.external / 1024 / 1024).toFixed(2)}`);

const start = Date.now();
const samples = [];

const timer = setInterval(() => {
  const now = Date.now();
  const usage = process.memoryUsage();
  samples.push({
    elapsed: (now - start) / 1000,
    heapUsed: (usage.heapUsed / 1024 / 1024).toFixed(2),
    rss: (usage.rss / 1024 / 1024).toFixed(2),
    external: (usage.external / 1024 / 1024).toFixed(2),
  });

  if (now - start >= durationMs) {
    clearInterval(timer);
    console.table(samples);
    process.exit(0);
  }
}, intervalMs);
