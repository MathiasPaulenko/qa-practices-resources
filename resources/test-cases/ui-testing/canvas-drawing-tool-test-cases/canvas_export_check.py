"""Verify a canvas PNG export actually contains the drawing.

Usage: python canvas_export_check.py <exported.png> [width height]
"""
import io
import sys

from PIL import Image


def check_canvas_export(png_bytes: bytes, expected_size=(600, 400)) -> None:
    img = Image.open(io.BytesIO(png_bytes))
    assert img.size == expected_size, f"unexpected export size {img.size}"
    center = img.convert("RGBA").getpixel((img.width // 2, img.height // 2))
    assert center[3] > 0, "export came out fully transparent"


if __name__ == "__main__":
    path = sys.argv[1]
    size = tuple(int(v) for v in sys.argv[2:4]) if len(sys.argv) >= 4 else (600, 400)
    with open(path, "rb") as f:
        check_canvas_export(f.read(), size)
    print(f"OK: {path} is a non-empty {size[0]}x{size[1]} PNG")
