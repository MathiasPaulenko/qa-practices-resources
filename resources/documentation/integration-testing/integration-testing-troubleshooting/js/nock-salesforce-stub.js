// nock 13.x stub for the Salesforce API — keeps CI off the live endpoint
const nock = require('nock');

const stub = nock('https://api.salesforce.com')
  .get('/services/data/v56/sobjects/Contact')
  .reply(200, {
    records: [{ Id: '003123', Name: 'Test Contact', Email: 'test@test.com' }],
    totalSize: 1,
  });

module.exports = { stub };
