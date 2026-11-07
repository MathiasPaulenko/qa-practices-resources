"""WAVE API check — prints issue counts per category for a URL.

Usage:
    WAVE_API_KEY=your-key python wave_api_check.py https://staging.yourstore.com

Get a key at https://wave.webaim.org/api/ (paid, ~$0.03/request at the time
of writing — check their pricing page before wiring it into CI).
"""

import os
import sys

import requests

API_KEY = os.environ.get('WAVE_API_KEY', 'your-wave-api-key')
REPORT_TYPE = 4  # statistics summary, cheapest detail level


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python wave_api_check.py <url>')
        return 2

    target = sys.argv[1]
    resp = requests.get(
        'https://wave.webaim.org/api/request',
        params={'key': API_KEY, 'url': target, 'reporttype': REPORT_TYPE},
        timeout=30,
    )
    resp.raise_for_status()
    result = resp.json()

    categories = result.get('categories', {})
    for name in ('error', 'contrast', 'alert', 'feature', 'structure', 'aria'):
        items = categories.get(name, {}).get('items', {})
        print(f'{name.upper()}: {len(items)} item(s)')

    stats = result.get('statistics', {})
    if stats:
        print(f"\nPage: {stats.get('pagetitle', target)}")
        print(f"WCAG items flagged: {stats.get('allitemcount', '?')}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
