// math.test.js
const { expect } = require('chai');
const sinon = require('sinon');
const { sum } = require('./math');
describe('math utilities', () => {
  it('sums two numbers', () => {
    expect(sum(2, 3)).to.equal(5);
  });
});
