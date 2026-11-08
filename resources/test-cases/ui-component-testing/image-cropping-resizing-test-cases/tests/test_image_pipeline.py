"""Tests mapped to the Image Cropping and Resizing Test Cases resource (TC ids)."""
from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image, UnidentifiedImageError

from image_pipeline import (
    ImageTooLargeError,
    UnsupportedImageError,
    batch_resize,
    clamp_crop_box,
    crop_animation,
    crop_image,
    export_image,
    load_image,
    preview_to_source,
    resize_image,
)


def solid(color, size):
    return Image.new("RGB", size, color)


@pytest.fixture
def jpeg_1200x800(tmp_path):
    p = tmp_path / "photo.jpg"
    solid((200, 120, 40), (1200, 800)).save(p, "JPEG", quality=95)
    return p


@pytest.fixture
def portrait_exif6(tmp_path):
    """Raw sensor pixels 640x480 + Orientation=6 -> should display 480x640."""
    img = solid((30, 60, 90), (640, 480))
    img.getexif()[274] = 6  # EXIF Orientation tag
    p = tmp_path / "portrait.jpg"
    img.save(p, "JPEG", quality=95, exif=img.getexif())
    return p


@pytest.fixture
def rgba_png(tmp_path):
    p = tmp_path / "logo.png"
    img = Image.new("RGBA", (200, 200), (10, 200, 10, 128))
    img.save(p, "PNG")
    return p


@pytest.fixture
def animated_gif(tmp_path):
    frames = [solid((i * 20, 0, 0), (100, 80)) for i in range(12)]
    p = tmp_path / "anim.gif"
    frames[0].save(p, "GIF", save_all=True, append_images=frames[1:], loop=0)
    return p


# --- Selection stage -------------------------------------------------------

def test_tc01_basic_crop_has_no_drift(jpeg_1200x800):
    img = load_image(jpeg_1200x800)
    out = crop_image(img, (100, 100, 500, 500))
    assert out.size == (400, 400)


def test_tc02_ratio_lock_1x1():
    box = clamp_crop_box((0, 0, 500, 200), (1200, 800), ratio=1.0)
    w, h = box[2] - box[0], box[3] - box[1]
    assert w == h


def test_tc03_ratio_lock_16x9():
    box = clamp_crop_box((0, 0, 640, 500), (1200, 800), ratio=16 / 9)
    w, h = box[2] - box[0], box[3] - box[1]
    assert abs(w / h - 16 / 9) < 0.01


def test_tc04_free_crop_any_shape(jpeg_1200x800):
    img = load_image(jpeg_1200x800)
    out = crop_image(img, (0, 0, 350, 120))
    assert out.size == (350, 120)


def test_tc08_zoom_maps_selection_back_to_source():
    # user dragged a 400x400 box at 200% zoom -> source box is 200x200
    assert preview_to_source((0, 0, 400, 400), zoom=2.0) == (0, 0, 200, 200)


def test_tc11_min_size_enforced():
    box = clamp_crop_box((10, 10, 40, 40), (1200, 800), min_size=50)
    assert box[2] - box[0] >= 50 and box[3] - box[1] >= 50


def test_tc12_selection_clamped_to_bounds():
    box = clamp_crop_box((1100, 700, 1400, 1000), (1200, 800))
    assert box[2] <= 1200 and box[3] <= 800
    assert box[0] >= 0 and box[1] >= 0


def test_ratio_lock_survives_small_image():
    # edge table: 16:9 on a 300x200 source keeps the lock inside bounds
    box = clamp_crop_box((0, 0, 1600, 900), (300, 200), ratio=16 / 9)
    w, h = box[2] - box[0], box[3] - box[1]
    assert w <= 300 and h <= 200
    assert abs(w / h - 16 / 9) < 0.01


# --- Load stage ------------------------------------------------------------

def test_tc13_unsupported_format_rejected(tmp_path):
    p = tmp_path / "scan.bmp"
    solid((1, 2, 3), (50, 50)).save(p, "BMP")
    with pytest.raises(UnsupportedImageError):
        load_image(p)


def test_tc14_corrupted_file_raises_clear_error(tmp_path):
    p = tmp_path / "corrupt.jpg"
    p.write_bytes(b"\xff\xd8\xff\xe0truncated")
    with pytest.raises((UnidentifiedImageError, OSError)):
        load_image(p)


def test_magic_bytes_sniffed_not_extension(tmp_path):
    # edge table: PNG bytes renamed .jpg still decode as PNG
    p = tmp_path / "photo.jpg"
    solid((9, 9, 9), (30, 30)).save(p, "PNG")
    img = load_image(p)
    assert img.format == "PNG"


# --- Transform stage -------------------------------------------------------

def test_tc09_resize_to_exact_dimensions(jpeg_1200x800):
    out = resize_image(load_image(jpeg_1200x800), (800, 600))
    assert out.size == (800, 600)


def test_tc15_resize_to_1x1():
    out = resize_image(solid((5, 5, 5), (4000, 3000)), (1, 1))
    assert out.size == (1, 1)


def test_tc16_oversized_resize_blocked():
    with pytest.raises(ImageTooLargeError):
        resize_image(solid((0, 0, 0), (800, 600)), (20000, 20000))


def test_tc17_exif_orientation_normalized(portrait_exif6):
    img = load_image(portrait_exif6)
    assert img.size == (480, 640)  # rotated, not raw 640x480


# --- Export stage ----------------------------------------------------------

def test_tc10_png_exported_as_jpeg(tmp_path, rgba_png):
    out = export_image(load_image(rgba_png), tmp_path / "out.jpg", "JPEG", quality=80)
    assert Image.open(out).format == "JPEG"


def test_tc23_png_alpha_survives_pipeline(tmp_path, rgba_png):
    img = crop_image(load_image(rgba_png), (0, 0, 150, 150))
    out = export_image(img, tmp_path / "crop.png", "PNG")
    assert Image.open(out).mode == "RGBA"


def test_tc24_gif_crop_keeps_all_frames(animated_gif):
    frames = crop_animation(load_image(animated_gif), (0, 0, 50, 50))
    assert len(frames) == 12
    assert all(f.size == (50, 50) for f in frames)


def test_tc26_jpeg_size_grows_with_quality(tmp_path, jpeg_1200x800):
    img = load_image(jpeg_1200x800)
    sizes = [
        export_image(img, tmp_path / f"q{q}.jpg", "JPEG", quality=q).stat().st_size
        for q in (30, 80, 100)
    ]
    assert sizes[0] < sizes[1] < sizes[2]


def test_tc27_batch_resizes_everything(tmp_path, jpeg_1200x800, rgba_png):
    results = batch_resize([jpeg_1200x800, rgba_png], (100, 100), tmp_path / "out")
    assert all(isinstance(v, Path) for v in results.values())
    assert len(results) == 2
