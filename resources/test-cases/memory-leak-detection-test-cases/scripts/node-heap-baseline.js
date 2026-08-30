const fs = require('fs');
const v8 = require('v8');

// Establish a baseline heap reading
// Usage: node node-heap-baseline.js

const initial = process.memoryUsage();
console.log('Initial heapUsed (MB):', (initial.heapUsed / 1024 / 1024).toFixed(2));

if (global.gc) {
  global.gc();
} else {
  console.warn('Run with --expose-gc to force collection');
}

const afterGC = process.memoryUsage();
console.log('HeapUsed after GC (MB):', (afterGC.heapUsed / 1024 / 1024).toFixed(2));

// Optionally write a heap snapshot
const snapshot = v8.writeHeapSnapshot(`baseline-${Date.now()}.heapsnapshot`);
console.log('Snapshot written:', snapshot);
