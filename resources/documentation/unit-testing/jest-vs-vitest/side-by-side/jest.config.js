// jest.config.js — Jest 30.5
// Plain-JS demo config. For TypeScript, add the ts-jest preset as shown in the guide.
module.exports = {
  testEnvironment: 'node',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
};
