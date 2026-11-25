// Validates every pattern from the cheat sheet against positive and negative
// samples. Zero dependencies — run with: node src/patterns.test.js
const cases = [
  {
    name: 'email',
    re: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    pass: ['qa.user@qapractices.com', 'a.b+tag@staging.example.org'],
    fail: ['user@mail', 'not-an-email', 'a@b.c'],
  },
  {
    name: 'us-phone',
    re: /^\+?1?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/,
    pass: ['555-123-4567', '(555) 123-4567', '+1 555.123.4567'],
    fail: ['55-1234', 'phone', '12345'],
  },
  {
    name: 'url',
    re: /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/,
    pass: ['https://qapractices.com/documentation/api-testing-guide', 'http://staging.example.org/v1/users?id=3'],
    fail: ['notaurl', 'ftp://files.example.org'],
  },
  {
    name: 'date-iso',
    re: /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/,
    pass: ['2026-11-25', '2026-01-01'],
    fail: ['2026-13-01', '11/25/2026', '2026-1-5'],
  },
  {
    name: 'time-24h',
    re: /^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$/,
    pass: ['23:59:59', '00:00:00'],
    fail: ['24:00:00', '12:60:00', '1:30'],
  },
  {
    name: 'ipv4',
    re: /^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$/,
    pass: ['192.168.1.1', '255.255.255.255', '10.0.0.1'],
    fail: ['256.1.1.1', '192.168.1', 'abc.def.ghi.jkl'],
  },
  {
    name: 'uuid',
    re: /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/,
    pass: ['550e8400-e29b-41d4-a716-446655440000'],
    fail: ['550e8400e29b41d4a716446655440000', 'not-a-uuid', '550e8400-e29b-41d4-a716'],
  },
  {
    name: 'us-zip',
    re: /^\d{5}(-\d{4})?$/,
    pass: ['90210', '90210-1234'],
    fail: ['9021', '90210-123', 'ABCDE'],
  },
  {
    name: 'password-policy',
    re: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
    pass: ['SecureP@ss123', 'T3st!ngIsFun'],
    fail: ['password', 'ALLCAPS1!', 'Sh0rt!'],
  },
  {
    name: 'card-shape',
    re: /^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})$/,
    pass: ['4111111111111111', '5500005555555559', '340000000000009'],
    fail: ['1234567890123456', '4111-1111-1111-1111'],
  },
  {
    name: 'mongodb-objectid',
    re: /^[a-f0-9]{24}$/,
    pass: ['507f1f77bcf86cd799439011'],
    fail: ['507F1F77BCF86CD799439011', 'tooshort'],
  },
  {
    name: 'jwt-shape',
    re: /^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]*$/,
    pass: ['eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk'],
    fail: ['not.a jwt', 'singlepart'],
  },
];

let failures = 0;
for (const c of cases) {
  for (const s of c.pass) {
    if (!c.re.test(s)) { failures++; console.error(`FAIL ${c.name}: expected match for "${s}"`); }
  }
  for (const s of c.fail) {
    if (c.re.test(s)) { failures++; console.error(`FAIL ${c.name}: unexpected match for "${s}"`); }
  }
}
console.log(`${cases.length} patterns checked, ${failures} failure(s)`);
process.exit(failures ? 1 : 0);
