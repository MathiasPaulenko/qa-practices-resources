# features/environment.py
from catalog_service import Catalog
from catalog_db import CatalogDB
from book_server import make_server, store
import sqlite3
import threading
import time
import requests


def before_all(context):
    port = int(context.config.userdata.get('API_PORT', '8765'))
    context.server = make_server('127.0.0.1', port)
    context.server_thread = threading.Thread(target=context.server.serve_forever)
    context.server_thread.daemon = True
    context.server_thread.start()

    base_url = f'http://127.0.0.1:{port}'
    for _ in range(50):
        try:
            requests.get(f'{base_url}/', timeout=0.1)
        except requests.ConnectionError:
            time.sleep(0.05)
        else:
            break

    context.base_url = base_url
    context.real_api_url = context.config.userdata.get('REAL_API_URL')
    context.store = store

    context.db = sqlite3.connect(':memory:')
    context.db.execute(
        'CREATE TABLE books (title TEXT PRIMARY KEY, available INTEGER NOT NULL)'
    )

    # Playwright is initialized on demand for @ui scenarios and kept
    # in a mutable container so it survives across scenario layers.
    context.ui = {'playwright': None, 'browser': None, 'browser_context': None}


def after_all(context):
    context.server.shutdown()
    context.db.close()

    if context.ui['browser_context']:
        context.ui['browser_context'].close()
    if context.ui['browser']:
        context.ui['browser'].close()
    if context.ui['playwright']:
        context.ui['playwright'].stop()


def before_scenario(context, scenario):
    context.catalog = None
    context.results = None
    context.response = None
    context.page = None

    if 'db' in scenario.tags:
        context.db.execute('SAVEPOINT scenario_state')
        context.catalog = CatalogDB(connection=context.db)
    elif 'api' in scenario.tags:
        store.clear()
    elif 'ui' in scenario.tags:
        store.clear()
        _ensure_browser(context)
        context.page = context.ui['browser_context'].new_page()
        context.page.set_viewport_size({'width': 1280, 'height': 720})
    else:
        context.catalog = Catalog()

    if 'integration' in scenario.tags and context.real_api_url:
        context.base_url = context.real_api_url


def after_scenario(context, scenario):
    if 'db' in scenario.tags:
        context.db.execute('ROLLBACK TO SAVEPOINT scenario_state')
        context.db.execute('RELEASE SAVEPOINT scenario_state')

    if context.page:
        context.page.close()
        context.page = None

    store.clear()
    context.catalog = None
    context.results = None
    context.response = None


def after_step(context, step):
    if step.status.name == 'failed' and context.page:
        try:
            safe_name = ''.join(
                c if c.isalnum() or c in (' ', '_', '-') else '_'
                for c in step.name
            ).replace(' ', '_')
            context.page.screenshot(path=f'reports/screenshots/{safe_name}.png')
        except Exception:
            pass


def after_tag(context, tag):
    if tag == 'integration':
        port = context.server.server_address[1]
        context.base_url = f'http://127.0.0.1:{port}'


def _ensure_browser(context):
    if context.ui['browser']:
        return
    from playwright.sync_api import sync_playwright
    context.ui['playwright'] = sync_playwright().start()
    context.ui['browser'] = context.ui['playwright'].chromium.launch(headless=True)
    context.ui['browser_context'] = context.ui['browser'].new_context()
