from PIL import Image
import io

from app import sha256_bytes, visual_similarity


def image_bytes(value: int) -> bytes:
    image = Image.new("L", (20, 20), color=value)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_same_bytes_have_same_sha256():
    data = image_bytes(100)
    assert sha256_bytes(data) == sha256_bytes(data)


def test_different_bytes_have_different_sha256():
    assert sha256_bytes(image_bytes(0)) != sha256_bytes(image_bytes(255))


def test_same_visual_image_has_maximum_similarity():
    data = image_bytes(100)
    assert visual_similarity(data, data) == 1.0


def test_different_visual_images_have_lower_similarity():
    assert visual_similarity(image_bytes(0), image_bytes(255)) < 1.0
