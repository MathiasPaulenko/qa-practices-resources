"""TC-GQL-009/010 plus replay edges — error unions, optimistic concurrency,
idempotency-key replay."""
from conftest import CREATE, CREATE_UNION, GET, UPDATE, graphql


def test_tc009_error_union_payload(base_url):
    body = graphql(base_url, CREATE_UNION,
                   {'input': {'email': 'not-an-email'}})
    result = body['data']['createUser']
    assert result['__typename'] == 'ValidationError'
    assert result['field'] == 'email'
    assert result['message']
    assert 'errors' not in body


def test_tc010_stale_version_conflict(base_url):
    created = graphql(base_url, CREATE,
                      {'input': {'email': 'qa.version@test.invalid'}})['data']['createUser']
    body = graphql(base_url, UPDATE,
                   {'id': created['id'], 'version': 9,
                    'input': {'displayName': 'Race'}})
    assert body['errors'][0]['extensions']['code'] == 'STALE_VERSION'
    fetched = graphql(base_url, GET, {'id': created['id']})['data']['user']
    assert fetched['version'] == created['version']
    assert fetched['displayName'] is None


def test_idempotency_key_replay(base_url):
    variables = {'input': {'email': 'qa.replay@test.invalid'}}
    headers = {'Idempotency-Key': 'req-abc-123'}
    first = graphql(base_url, CREATE, variables, headers=headers)
    second = graphql(base_url, CREATE, variables, headers=headers)
    # replay returns the original result — no duplicate user created
    assert second == first
    assert second['data']['createUser']['id'] == first['data']['createUser']['id']


def test_idempotency_key_mismatch(base_url):
    headers = {'Idempotency-Key': 'req-shared-1'}
    graphql(base_url, CREATE,
            {'input': {'email': 'qa.a@test.invalid'}}, headers=headers)
    body = graphql(base_url, CREATE,
                   {'input': {'email': 'qa.b@test.invalid'}}, headers=headers)
    assert body['errors'][0]['extensions']['code'] == 'IDEMPOTENCY_MISMATCH'
