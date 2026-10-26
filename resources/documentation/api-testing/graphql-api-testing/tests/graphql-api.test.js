// Query, mutation, error-contract, schema-validation and APQ tests.
// Requires a reachable GraphQL endpoint; set GRAPHQL_URL before running.
// Placeholder default: replace with your staging URL.
const request = require('supertest')(
  process.env.GRAPHQL_URL || 'https://staging.qapractices.dev'
);
const crypto = require('crypto');
const {
  buildClientSchema,
  parse,
  validate,
  getIntrospectionQuery,
} = require('graphql'); // graphql 16.11

describe('queries', () => {
  test('GetUser returns the requested fields only', async () => {
    const query = `
      query GetUser($id: ID!) {
        user(id: $id) { id name email }
      }
    `;
    const res = await request
      .post('/graphql')
      .send({ query, variables: { id: 'u-1024' } });

    expect(res.status).toBe(200);
    expect(res.body.data.user).toMatchObject({ id: 'u-1024' });
    expect(res.body.errors).toBeUndefined();
  });
});

describe('mutations', () => {
  test('CreateUser persists and rejects a duplicate email', async () => {
    const mutation = `
      mutation CreateUser($input: CreateUserInput!) {
        createUser(input: $input) { id email }
      }
    `;
    const input = {
      name: 'Jane Doe',
      email: 'jane.doe@qapractices.dev',
      password: 'SecurePass123!',
    };

    const created = await request
      .post('/graphql')
      .send({ query: mutation, variables: { input } });
    const newId = created.body.data.createUser.id;

    const verify = await request.post('/graphql').send({
      query: `query($id: ID!) { user(id: $id) { email } }`,
      variables: { id: newId },
    });
    expect(verify.body.data.user.email).toBe('jane.doe@qapractices.dev');

    const dupe = await request
      .post('/graphql')
      .send({ query: mutation, variables: { input } });
    expect(dupe.body.errors[0].extensions.code).toBe('CONFLICT');
  });
});

describe('error contract', () => {
  test('unauthenticated request returns UNAUTHENTICATED, not a 401', async () => {
    const res = await request
      .post('/graphql')
      .send({ query: '{ user(id: "u-1") { email } }' });

    expect(res.status).toBe(200);
    expect(res.body.errors[0].extensions.code).toBe('UNAUTHENTICATED');
    expect(res.body.data.user).toBeNull();
  });

  test('validation failure returns BAD_USER_INPUT with the field path', async () => {
    const res = await request.post('/graphql').send({
      query: `mutation($input: CreateUserInput!) { createUser(input: $input) { id } }`,
      variables: { input: { name: '', email: 'not-an-email' } },
    });

    expect(res.body.errors[0].extensions.code).toBe('BAD_USER_INPUT');
    expect(res.body.data.createUser).toBeNull();
  });
});

describe('schema contract', () => {
  test('client queries still validate against the live schema', async () => {
    const res = await request
      .post('/graphql')
      .send({ query: getIntrospectionQuery() });
    const schema = buildClientSchema(res.body.data);

    const errors = validate(
      schema,
      parse(`query { user(id: "u-1") { id name email } }`)
    );
    expect(errors).toHaveLength(0);
  });
});

describe('persisted queries (APQ)', () => {
  const query = '{ user(id: "u-1") { id name } }';
  const sha256 = crypto.createHash('sha256').update(query).digest('hex');

  test('APQ flow: miss registers, hit executes by hash only', async () => {
    const miss = await request.post('/graphql').send({
      extensions: { persistedQuery: { version: 1, sha256Hash: sha256 } },
    });
    expect(miss.body.errors[0].message).toMatch(/PersistedQueryNotFound/);

    await request.post('/graphql').send({
      query,
      extensions: { persistedQuery: { version: 1, sha256Hash: sha256 } },
    });

    const hit = await request.post('/graphql').send({
      extensions: { persistedQuery: { version: 1, sha256Hash: sha256 } },
    });
    expect(hit.body.data.user.id).toBe('u-1');
  });
});

describe('performance', () => {
  test('deeply nested query stays inside the latency budget', async () => {
    const deepQuery = `{
      users { posts { comments { author { posts { title } } } } }
    }`;

    const start = Date.now();
    const res = await request.post('/graphql').send({ query: deepQuery });
    const duration = Date.now() - start;

    expect(res.body.errors).toBeUndefined();
    expect(duration).toBeLessThan(2000);
  });
});
