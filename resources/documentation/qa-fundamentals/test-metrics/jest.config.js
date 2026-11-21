// Jest 30 — CI fails if coverage drops below the floor.
// Run: npx jest --coverage --coverageReporters=text-summary
module.exports = {
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
