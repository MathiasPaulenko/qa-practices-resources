"""TC-GQL-006/007 plus input-validation edges — batch, auth, schema edges."""
from conftest import BATCH, CREATE, DELETE, READ_AUTH, WRITE_AUTH, graphql


def test_tc006_batch_partial_failure(base_url):
    body = graphql(base_url, BATCH,
                   {'users': [{'email': 'qa.valid@test.invalid'},
                              {'email': 'not-an-email'}]})
    results = body['data']['createUsers']
    assert results[0]['ok'] is True
    assert results[1]['ok'] is False
    assert results[1]['error'] is not None


def test_batch_size_over_limit(base_url):
    users = [{'email': f'qa.{i}@test.invalid'} for i in range(101)]
    body = graphql(base_url, BATCH, {'users': users})
    assert body['errors'][0]['extensions']['code'] == 'BAD_USER_INPUT'


def test_tc007_delete_anonymous_is_unauthenticated(base_url):
    created = graphql(base_url, CREATE,
                      {'input': {'email': 'qa.auth@test.invalid'}})['data']['createUser']
    body = graphql(base_url, DELETE, {'id': created['id']})
    assert body['errors'][0]['extensions']['code'] == 'UNAUTHENTICATED'
    # state unchanged — the resource still exists
    assert graphql(base_url, """
        query($id: ID!) { user(id: $id) { id } }""",
        {'id': created['id']})['data']['user'] is not None


def test_tc007_delete_readonly_scope_is_forbidden(base_url):
    created = graphql(base_url, CREATE,
                      {'input': {'email': 'qa.scope@test.invalid'}})['data']['createUser']
    body = graphql(base_url, DELETE, {'id': created['id']}, headers=READ_AUTH)
    assert body['errors'][0]['extensions']['code'] == 'FORBIDDEN'


def test_edge_null_sent_to_non_null_field(base_url):
    body = graphql(base_url, CREATE, {'input': {'email': None}})
    assert body['errors'][0]['extensions']['code'] == 'BAD_USER_INPUT'


def test_edge_enum_outside_domain(base_url):
    body = graphql(base_url, CREATE,
                   {'input': {'email': 'qa.enum@test.invalid',
                              'role': 'SUPERADMIN'}})
    assert body['errors'][0]['extensions']['code'] == 'BAD_USER_INPUT'
