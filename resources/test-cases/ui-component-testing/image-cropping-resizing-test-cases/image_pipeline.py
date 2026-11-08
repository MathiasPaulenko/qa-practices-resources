"""Crop and resize pipeline modeled on the failure points the resource tests.

Each function encodes one rule the UI must honor: EXIF normalization on load,
bounds/min-size/aspect clamping during selection, preview-to-source coordinate
mapping under zoom, alpha-aware export and multi-frame GIF handling. The pytest
suite in tests/ maps cases to the resource's TC ids.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps, ImageSequence

SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP", "GIF"}
MIN_CROP = 50
MAX_BITMAP_PIXELS = 90_000_000  # ~360 MB RGBA; browsers cap texture size near here

Box = tuple[int, int, int, int]  # left, top, right, bottom


class UnsupportedImageError(ValueError):
    """Raised when the file decodes to a format outside SUPPORTED_FORMATS."""


class ImageTooLargeError(ValueError):
    """Raised when the decoded bitmap exceeds MAX_BITMAP_PIXELS."""


def load_image(path: str | Path) -> Image.Image:
    """Decode, sniff the real format and normalize EXIF orientation (TC-13/14/17)."""
    img = Image.open(path)  # raises UnidentifiedImageError on corrupted files
    fmt = img.format  # sniffed from magic bytes, not the extension
    if fmt not in SUPPORTED_FORMATS:
        raise UnsupportedImageError(
            f"{fmt} not supported; expected one of {sorted(SUPPORTED_FORMATS)}"
        )
    img.load()
    if getattr(img, "is_animated", False):
        return img  # animated formats carry no EXIF; transposing would drop frames
    out = ImageOps.exif_transpose(img)
    out.format = fmt  # transpose returns a copy without format
    return out


def clamp_crop_box(
    box: Box,
    size: tuple[int, int],
    min_size: int = MIN_CROP,
    ratio: float | None = None,
) -> Box:
    """Clamp a selection to image bounds, enforce min size and aspect ratio.

    `ratio` is width/height (1.0 for square, 16/9 for widescreen). The lock is
    preserved by deriving each axis from the other after clamping, so a box
    pushed against the image edge shrinks instead of breaking the ratio
    (TC-02/03/11/12).
    """
    width_px, height_px = size
    left, top, right, bottom = box
    w = max(min_size, right - left)
    h = max(min_size, bottom - top)

    if ratio is not None:
        w = min(w, width_px)
        h = min(round(w / ratio), height_px)
        w = min(round(h * ratio), width_px)
    else:
        w = min(w, width_px)
        h = min(h, height_px)
    left = max(0, min(left, width_px - w))
    top = max(0, min(top, height_px - h))
    return (left, top, left + w, top + h)


def preview_to_source(selection: Box, zoom: float) -> Box:
    """Map preview pixels to source pixels; skipping this is the classic offset bug (TC-08)."""
    if zoom <= 0:
        raise ValueError("zoom must be positive")
    return tuple(round(v / zoom) for v in selection)  # type: ignore[return-value]


def crop_image(img: Image.Image, box: Box) -> Image.Image:
    return img.crop(clamp_crop_box(box, img.size))


def resize_image(
    img: Image.Image,
    size: tuple[int, int],
    resample: Image.Resampling = Image.Resampling.LANCZOS,
) -> Image.Image:
    if size[0] * size[1] > MAX_BITMAP_PIXELS:
        raise ImageTooLargeError(f"{size} exceeds the {MAX_BITMAP_PIXELS}px bitmap cap")
    return img.resize(size, resample)


def export_image(
    img: Image.Image,
    path: str | Path,
    fmt: str,
    quality: int | None = None,
) -> Path:
    """Save honoring format semantics: JPEG flattens alpha, PNG keeps it (TC-10/23/26)."""
    out = Path(path)
    save_kwargs: dict = {}
    if fmt == "JPEG":
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        save_kwargs["quality"] = quality if quality is not None else 80
    elif fmt == "PNG":
        img = img.convert("RGBA") if img.mode == "P" else img
    else:
        raise UnsupportedImageError(f"export format {fmt} not supported")
    img.save(out, fmt, **save_kwargs)
    return out


def crop_animation(img: Image.Image, box: Box) -> list[Image.Image]:
    """Crop every frame; shipping only frame 0 silently drops the animation (TC-24)."""
    return [frame.copy().crop(box) for frame in ImageSequence.Iterator(img)]


def batch_resize(
    paths: Iterable[str | Path],
    size: tuple[int, int],
    out_dir: str | Path,
) -> dict[Path, Path | Exception]:
    """Resize each image to `size`; failures are reported, never swallowed (TC-27)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    results: dict[Path, Path | Exception] = {}
    for p in paths:
        p = Path(p)
        try:
            img = load_image(p)
            dest = out_dir / p.name
            export_image(resize_image(img, size), dest, img.format or "PNG")
            results[p] = dest
        except Exception as exc:  # per-file report, batch continues
            results[p] = exc
    return results
