"""Pseudo-localization transform for l10n smoke tests.

Accents every vowel, pads strings with expansion markers, and wraps them
in brackets so concatenated strings show a visible seam. Feed it a string
table (one string per line) or pipe any text through it.

Usage:
    python pseudolocalize.py < strings_en.txt > strings_pseudo.txt
"""

import sys

# Windows consoles may default to cp1252 — print UTF-8 regardless.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Extend this map for your needs — a full pseudo-locale also transforms
# consonants and adds characters from multiple scripts.
ACCENTS = str.maketrans("aeiouAEIOU", "áéíóúÁÉÍÓÚ")

DEFAULT_PAD = "Šẋẋ"


def pseudolocalize(text: str, pad: str = DEFAULT_PAD) -> str:
    """Return `text` accented, expanded ~40% and wrapped in markers."""
    return f"[{pad} {text.translate(ACCENTS)} {pad}]"


if __name__ == "__main__":
    for line in sys.stdin:
        stripped = line.rstrip("\n")
        if stripped:
            print(pseudolocalize(stripped))
