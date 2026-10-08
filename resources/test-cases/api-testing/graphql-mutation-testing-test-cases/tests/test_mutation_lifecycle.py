"""TC-GQL-001..005 — create / update / delete lifecycle cases."""
from conftest import CREATE, DELETE, GET, UPDATE, WRITE_AUTH, graphql


def test_tc001_create_valid_input(base_url):
    body = graphql(base_url, CREATE,
                   {'input': {'email': 'qa.mutation@test.invalid', 'role': 'USER'}})
    user = body['data']['createUser']
    assert user['id']
    assert 'errors' not in body
    fetched = graphql(base_url, GET, {'id': user['id']})['data']['user']
    assert fetched == user


def test_tc002_create_missing_required_field(base_url):
    body = graphql(base_url, CREATE, {'input': {'role': 'USER'}})
    assert body['errors'][0]['extensions']['code'] == 'BAD_USER_INPUT'
    assert body.get('data') is None or body['data']['createUser'] is None


def test_tc003_partial_update_leaves_fields_untouched(base_url):
    created = graphql(base_url, CREATE,
                      {'input': {'email': 'qa.partial@test.invalid',
                                 'role': 'USER',
                                 'displayName': 'Before'}})['data']['createUser']
    graphql(base_url, UPDATE,
            {'id': created['id'], 'input': {'displayName': 'After'}})
    fetched = graphql(base_url, GET, {'id': created['id']})['data']['user']
    assert fetched['displayName'] == 'After'
    assert fetched['email'] == created['email']
    assert fetched['role'] == created['role']


def test_tc004_update_deleted_resource(base_url):
    created = graphql(base_url, CREATE,
                      {'input': {'email': 'qa.deleted@test.invalid'}})['data']['createUser']
    graphql(base_url, DELETE, {'id': created['id']}, headers=WRITE_AUTH)
    body = graphql(base_url, UPDATE,
                   {'id': created['id'], 'input': {'displayName': 'X'}})
    assert body['errors'][0]['extensions']['code'] == 'NOT_FOUND'


def test_tc005_delete_removes_resource(base_url):
    created = graphql(base_url, CREATE,
                      {'input': {'email': 'qa.delete@test.invalid'}})['data']['createUser']
    body = graphql(base_url, DELETE, {'id': created['id']}, headers=WRITE_AUTH)
    assert body['data']['deleteUser']['success'] is True
    fetched = graphql(base_url, GET, {'id': created['id']})['data']['user']
    assert fetched is None
