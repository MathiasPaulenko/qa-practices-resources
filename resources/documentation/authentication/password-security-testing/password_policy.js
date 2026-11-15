// NIST 800-63B-style password policy validator.
// Length first, blocklist second — the opposite of the old
// "one uppercase, one symbol" composition rules.

const BLOCKLIST = ['password', '123456', 'qwerty', 'letmein', 'welcome1'];
const MIN_LENGTH = 12;

function isValidPassword(password) {
  if (password.length < MIN_LENGTH) return false;
  if (BLOCKLIST.includes(password.toLowerCase())) return false;
  return true;
}

module.exports = { isValidPassword, BLOCKLIST, MIN_LENGTH };

// Quick self-check: `node password_policy.js`
if (require.main === module) {
  const cases = [
    ['Thorough!2026', true],
    ['C0mpl3x!P@ss', true],
    ['Correct-Horse-Battery-Staple!', true],
    ['password123', false],
    ['Abc1!', false],
    ['aaaaaaaa', false],
  ];
  let failed = 0;
  for (const [pw, expected] of cases) {
    const got = isValidPassword(pw);
    const mark = got === expected ? 'PASS' : 'FAIL';
    if (got !== expected) failed++;
    console.log(`${mark} isValidPassword(${JSON.stringify(pw)}) === ${expected}`);
  }
  process.exit(failed ? 1 : 0);
}
