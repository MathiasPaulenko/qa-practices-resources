"""Stdlib-only mock i18n API for the multi-language localization test cases.

Serves locale-aware product payloads and a cart-count pluralization endpoint.
Supported locales: en, es, de, ja, ar. Unknown or missing `locale` params fall
back to English. The `fr` locale intentionally has a missing key and an empty
value to exercise fallback behavior.

Run standalone: python mock_server.py 8571
"""

import json
import locale as pylocale  # noqa: F401  (kept for parity with real apps that lean on it)
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

SUPPORTED_LOCALES = {"en", "es", "de", "ja", "ar"}
RTL_LOCALES = {"ar"}
FALLBACK = "en"

PRODUCTS = {
    "PROD-1001": {
        "id": "PROD-1001",
        "price": {"amount": 15000, "currency": "JPY"},
        "strings": {
            "en": {"name": "Wireless Headphones", "description": "High-quality sound wireless headphones", "cta": "Add to cart"},
            "es": {"name": "Auriculares Inalámbricos", "description": "Auriculares inalámbricos de alta calidad", "cta": "Añadir al carrito"},
            "de": {"name": "Kabellose Kopfhörer", "description": "Kabellose Kopfhörer mit hochwertigem Klang", "cta": "In den Warenkorb"},
            "ja": {"name": "ワイヤレスヘッドホン", "description": "高品質サウンドのワイヤレスヘッドホン", "cta": "カートに追加"},
            "ar": {"name": "سماعات لاسلكية", "description": "سماعات لاسلكية بصوت عالي الجودة", "cta": "أضف إلى السلة"},
            # fr exists but is incomplete on purpose: missing "cta", empty "description"
            "fr": {"name": "Écouteurs sans fil", "description": "", },
        },
    }
}

PLURALS = {
    # CLDR-derived forms for the cart counter
    "en": {"one": "{} item", "other": "{} items"},
    "es": {"one": "{} artículo", "other": "{} artículos"},
    "de": {"one": "{} Artikel", "other": "{} Artikel"},
    "ja": {"other": "{} 点"},  # Japanese has a single plural category
    "ru": {"one": "{} товар", "few": "{} товара", "many": "{} товаров", "other": "{} товара"},
    "ar": {"zero": "لا عناصر", "one": "{} عنصر", "two": "{} عنصران", "few": "{} عناصر", "many": "{} عنصرًا", "other": "{} عنصر"},
}

CURRENCY_FORMATS = {
    "ja-JP": ("JPY", "¥{:,.0f}"),
    "de-DE": ("EUR", "{:,.2f} €"),
    "es-ES": ("EUR", "{:,.2f} €"),
    "en-US": ("USD", "${:,.2f}"),
    "ar-SA": ("SAR", "{:,.2f} SAR"),
}


def ru_category(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return "one"
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return "few"
    if n % 10 == 0 or 5 <= n % 10 <= 9 or 11 <= n % 100 <= 14:
        return "many"
    return "other"


def ar_category(n: int) -> str:
    if n == 0:
        return "zero"
    if n == 1:
        return "one"
    if n == 2:
        return "two"
    if 3 <= n % 100 <= 10:
        return "few"
    if 11 <= n % 100 <= 99:
        return "many"
    return "other"


def plural_category(n: int, loc: str) -> str:
    if loc == "ru":
        return ru_category(n)
    if loc == "ar":
        return ar_category(n)
    return "one" if n == 1 else "other"


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        locale = params.get("locale", [FALLBACK])[0]
        accept_language = self.headers.get("Accept-Language", FALLBACK).split(",")[0].split("-")[0]

        if parsed.path.startswith("/api/v1/products/"):
            pid = parsed.path.rsplit("/", 1)[-1]
            product = PRODUCTS.get(pid)
            if product is None:
                self._send(404, {"error": "product not found"})
                return
            lang = locale.split("-")[0]
            if lang not in SUPPORTED_LOCALES and lang not in product["strings"]:
                lang = accept_language if accept_language in SUPPORTED_LOCALES else FALLBACK
            strings = dict(product["strings"].get(lang, product["strings"][FALLBACK]))
            fallback_hits = []
            for key in ("name", "description", "cta"):
                if not strings.get(key):
                    strings[key] = product["strings"][FALLBACK][key]
                    fallback_hits.append(key)
            full_locale = locale if "-" in locale else {"en": "en-US", "es": "es-ES", "de": "de-DE", "ja": "ja-JP", "ar": "ar-SA"}.get(lang, locale)
            currency, fmt = CURRENCY_FORMATS.get(full_locale, ("USD", "${:,.2f}"))
            self._send(200, {
                "id": product["id"],
                "name": strings["name"],
                "description": strings["description"],
                "cta": strings["cta"],
                "price": {
                    "amount": product["price"]["amount"],
                    "currency": currency,
                    "formatted": fmt.format(product["price"]["amount"]),
                },
                "locale": full_locale,
                "dir": "rtl" if lang in RTL_LOCALES else "ltr",
                "fallbackKeys": fallback_hits,
            })
            return

        if parsed.path == "/api/v1/cart/count":
            try:
                n = int(params.get("n", ["0"])[0])
            except ValueError:
                self._send(400, {"error": "n must be an integer"})
                return
            lang = locale.split("-")[0]
            forms = PLURALS.get(lang, PLURALS[FALLBACK])
            cat = plural_category(n, lang)
            if cat not in forms:
                cat = "other"  # languages like ja only define "other"
            self._send(200, {"n": n, "locale": lang, "category": cat, "label": forms[cat].format(n)})
            return

        if parsed.path == "/api/v1/locales":
            self._send(200, {"supported": sorted(SUPPORTED_LOCALES), "rtl": sorted(RTL_LOCALES)})
            return

        self._send(404, {"error": "unknown endpoint"})

    def log_message(self, *args):  # quiet
        pass


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8571
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
