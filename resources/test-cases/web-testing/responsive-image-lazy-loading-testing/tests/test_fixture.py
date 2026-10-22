import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "picture.html").read_text()


class TagCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs, self.sources, self.links = [], [], []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "img":
            self.imgs.append(d)
        elif tag == "source":
            self.sources.append(d)
        elif tag == "link":
            self.links.append(d)


@pytest.fixture(scope="module")
def tags():
    c = TagCollector()
    c.feed(HTML)
    return c


def test_srcset_has_three_w_candidates(tags):
    hero = next(i for i in tags.imgs if i.get("id") == "hero")
    candidates = [c.strip().split() for c in hero["srcset"].split(",")]
    assert len(candidates) == 3
    assert all(len(c) == 2 and c[1].endswith("w") for c in candidates)
    widths = sorted(int(c[1][:-1]) for c in candidates)
    assert widths == [400, 800, 1600]


def test_sizes_and_dimensions_present_on_content_images(tags):
    hero = next(i for i in tags.imgs if i.get("id") == "hero")
    assert hero["sizes"] == "100vw"
    assert hero["width"] and hero["height"]


def test_hero_is_eager_and_lazy_is_deferred(tags):
    hero = next(i for i in tags.imgs if i.get("id") == "hero")
    lazy = next(i for i in tags.imgs if i.get("id") == "lazy-img")
    assert hero.get("loading") == "eager"
    assert hero.get("fetchpriority") == "high"
    assert lazy.get("loading") == "lazy"


def test_picture_sources_have_media_and_img_fallback(tags):
    assert all("media" in s for s in tags.sources)
    assert any("min-width:1024px" in s["media"] for s in tags.sources)
    assert any("min-width:600px" in s["media"] for s in tags.sources)
    # the img inside picture is the smallest-viewport fallback
    assert any(i["src"] == "img/narrow.svg" for i in tags.imgs)


def test_every_content_image_has_alt(tags):
    assert all("alt" in i for i in tags.imgs)


def test_preload_link_includes_imagesrcset(tags):
    pre = [l for l in tags.links if l.get("rel") == "preload" and l.get("as") == "image"]
    assert pre, "hero preload missing"
    assert "imagesrcset" in pre[0] and "imagesizes" in pre[0]


def test_referenced_variants_exist_on_disk():
    for name in ["hero-400.svg", "hero-800.svg", "hero-1600.svg",
                 "square.svg", "wide.svg", "narrow.svg", "lazy-bottom.svg"]:
        assert (ROOT / "img" / name).exists(), f"missing variant {name}"
    assert re.search(r'hero-\d+\.svg \d+w', HTML)
