"""TC-GQL-008 — a mutation publishes the expected subscription event."""
import asyncio
import json

import websockets

from conftest import CREATE, UPDATE, graphql


def test_tc008_mutation_triggers_subscription(base_url, ws_url):
    async def scenario():
        async with websockets.connect(ws_url) as ws:
            created = graphql(
                base_url, CREATE,
                {'input': {'email': 'qa.sub@test.invalid'}})['data']['createUser']
            graphql(base_url, UPDATE,
                    {'id': created['id'], 'input': {'displayName': 'Sub Event'}})
            msg = await asyncio.wait_for(ws.recv(), timeout=5)
            event = json.loads(msg)
            assert event['type'] == 'userUpdated'
            assert event['payload']['id'] == created['id']
            assert event['payload']['displayName'] == 'Sub Event'
    asyncio.run(scenario())
