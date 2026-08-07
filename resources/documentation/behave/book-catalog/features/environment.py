# features/environment.py
import sqlite3
import threading
import time

import requests
from book_server import make_server, store
from catalog_db import CatalogDB
from catalog_service import Catalog


def before_all(context):
    port = int(context.config.userdata.get('API_PORT', '8765'))
    context.server = make_server('127.0.0.1', port)
    context.server_thread = threading.Thread(target=context.server.serve_forever)
    context.server_thread.daemon = True
    context.server_thread.start()

    base_url = f'http://127.0.0.1:{port}'
    for _ in range(50):
        try:
            requests.get(f'{base_url}/books/__health', timeout=0.1)
        except requests.ConnectionError:
            time.sleep(0.05)
        else:
            break

    context.base_url = base_url
    context.real_api_url = context.config.userdata.get('REAL_API_URL')

    context.db = sqlite3.connect(':memory:')
    context.db.execute(
        'CREATE TABLE books (title TEXT PRIMARY KEY, available INTEGER NOT NULL)'
    )


def after_all(context):
    context.server.shutdown()
    context.db.close()


def before_scenario(context, scenario):
    context.catalog = None
    context.results = None
    context.response = None

    if 'db' in scenario.tags:
        context.db.execute('SAVEPOINT scenario_state')
        context.catalog = CatalogDB(connection=context.db)
    elif 'api' in scenario.tags:
        store.clear()
    else:
        context.catalog = Catalog()

    if 'integration' in scenario.tags and context.real_api_url:
        context.base_url = context.real_api_url


def after_scenario(context, scenario):
    if 'db' in scenario.tags:
        context.db.execute('ROLLBACK TO SAVEPOINT scenario_state')
        context.db.execute('RELEASE SAVEPOINT scenario_state')

    context.catalog = None
    context.results = None
    context.response = None


def after_tag(context, tag):
    if tag == 'integration':
        port = context.server.server_address[1]
        context.base_url = f'http://127.0.0.1:{port}'
