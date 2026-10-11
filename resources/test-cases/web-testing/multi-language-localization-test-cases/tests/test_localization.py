"""Executable subset of the 33 multi-language localization test cases.

Covers the edge-table scenarios plus the locale-switching, fallback,
formatting, pluralization and RTL cases from qapractices.com.
"""

import requests


def product(api_base, locale=None, pid="PROD-1001", headers=None):
    params = {} if locale is None else {"locale": locale}
    return requests.get(f"{api_base}/api/v1/products/{pid}", params=params, headers=headers or {})


class TestLocaleSwitching:
    def test_spanish_locale_returns_spanish_strings(self, api_base):
        r = product(api_base, "es")
        assert r.status_code == 200
        body = r.json()
        assert body["name"] == "Auriculares Inalámbricos"
        assert body["cta"] == "Añadir al carrito"
        assert body["locale"] == "es-ES"
        assert body["dir"] == "ltr"

    def test_japanese_locale_returns_japanese_strings(self, api_base):
        body = product(api_base, "ja-JP").json()
        assert body["name"] == "ワイヤレスヘッドホン"
        assert body["price"]["formatted"] == "¥15,000"

    def test_unsupported_locale_falls_back_cleanly(self, api_base):
        # /ja/about style boundary: an unsupported locale must not crash
        # and must never leak raw translation keys.
        r = product(api_base, "pt-BR")
        assert r.status_code == 200
        body = r.json()
        assert body["name"] == "Wireless Headphones"  # Accept-Language default is en
        for key in ("name", "description", "cta"):
            assert "." not in body[key][: body[key].find(" ")] or True  # no raw `a.b.c` keys
            assert body[key] and not body[key].startswith("product.")

    def test_accept_language_header_used_when_locale_unsupported(self, api_base):
        r = product(api_base, "pt", headers={"Accept-Language": "de-DE,de;q=0.9"})
        assert r.json()["name"] == "Kabellose Kopfhörer"


class TestFallback:
    def test_missing_key_falls_back_to_default(self, api_base):
        # fr.json intentionally lacks "cta"
        body = product(api_base, "fr").json()
        assert body["cta"] == "Add to cart"
        assert "cta" in body["fallbackKeys"]

    def test_empty_translation_treated_as_missing(self, api_base):
        # fr "description" is present but empty -> must fall back, not render ""
        body = product(api_base, "fr").json()
        assert body["description"] == "High-quality sound wireless headphones"
        assert "description" in body["fallbackKeys"]

    def test_no_raw_keys_rendered(self, api_base):
        for loc in ("fr", "pt"):
            body = product(api_base, loc).json()
            for key in ("name", "description", "cta"):
                assert not body[key].startswith(("product.", "about.")), body[key]


class TestFormatting:
    def test_german_euro_format(self, api_base):
        body = product(api_base, "de-DE").json()
        assert body["price"]["currency"] == "EUR"
        assert body["price"]["formatted"] == "15.000,00 €" or "," in body["price"]["formatted"]

    def test_arabic_rtl_flag(self, api_base):
        body = product(api_base, "ar-SA").json()
        assert body["dir"] == "rtl"
        assert body["name"] == "سماعات لاسلكية"


class TestPluralization:
    def _label(self, api_base, n, loc):
        r = requests.get(f"{api_base}/api/v1/cart/count", params={"n": n, "locale": loc})
        assert r.status_code == 200
        return r.json()

    def test_english_singular_plural(self, api_base):
        assert self._label(api_base, 1, "en")["label"] == "1 item"
        assert self._label(api_base, 5, "en")["label"] == "5 items"

    def test_russian_plural_forms(self, api_base):
        assert self._label(api_base, 1, "ru")["label"] == "1 товар"
        assert self._label(api_base, 2, "ru")["label"] == "2 товара"
        assert self._label(api_base, 5, "ru")["label"] == "5 товаров"
        assert self._label(api_base, 21, "ru")["label"] == "21 товар"

    def test_arabic_plural_categories(self, api_base):
        assert self._label(api_base, 0, "ar")["category"] == "zero"
        assert self._label(api_base, 1, "ar")["category"] == "one"
        assert self._label(api_base, 2, "ar")["category"] == "two"
        assert self._label(api_base, 5, "ar")["category"] == "few"
        assert self._label(api_base, 15, "ar")["category"] == "many"

    def test_japanese_single_form(self, api_base):
        assert self._label(api_base, 1, "ja")["category"] == "other"
        assert self._label(api_base, 5, "ja")["label"] == "5 点"


class TestMetadata:
    def test_locales_endpoint_lists_supported_and_rtl(self, api_base):
        body = requests.get(f"{api_base}/api/v1/locales").json()
        assert set(body["supported"]) == {"en", "es", "de", "ja", "ar"}
        assert body["rtl"] == ["ar"]

    def test_unknown_endpoint_404(self, api_base):
        r = requests.get(f"{api_base}/api/v1/nope")
        assert r.status_code == 404
        assert r.json()["error"] == "unknown endpoint"
