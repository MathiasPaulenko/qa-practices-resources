// Ranks modules by defects per KLOC so you can spot the hotspot first.
// Usage: node scripts/defect_density.js
const moduleStats = [
  { name: 'Checkout', kloc: 15, defects: 12 },
  { name: 'Auth', kloc: 8, defects: 14 },
  { name: 'Search', kloc: 22, defects: 8 }
];

const ranked = moduleStats
  .map((m) => ({ ...m, density: m.defects / m.kloc }))
  .sort((a, b) => b.density - a.density);

for (const m of ranked) {
  console.log(`${m.name.padEnd(10)} ${m.density.toFixed(2)} defects/KLOC`);
}
// -> Auth is the hotspot at 1.75 defects/KLOC
