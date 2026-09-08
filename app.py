"""Student-friendly visual image duplicate detector.

This application compares image files and visual appearance only. It is not
biometric identification software.
"""

from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from itertools import combinations

import numpy as np
import streamlit as st
from PIL import Image, ImageChops

MAX_IMAGES = 5
MAX_FILE_SIZE_MB = 10
NORMALIZED_SIZE = (128, 128)


@dataclass
class ComparisonResult:
    first: int
    second: int
    exact_match: bool
    similarity: float
    difference: float
    decision: str


def sha256_bytes(data: bytes) -> str:
    """Return a reproducible hash for the original file bytes."""
    return hashlib.sha256(data).hexdigest()


def open_image(data: bytes) -> Image.Image:
    """Load an image safely as grayscale."""
    with Image.open(io.BytesIO(data)) as image:
        return image.convert("L")


def normalized_pixels(data: bytes) -> np.ndarray:
    """Convert an image into normalized grayscale pixels."""
    image = open_image(data).resize(NORMALIZED_SIZE)
    pixels = np.asarray(image, dtype=np.float32)
    pixels = (pixels - pixels.mean()) / (pixels.std() + 1e-8)
    return pixels


def visual_similarity(first: bytes, second: bytes) -> float:
    """Return a simple normalized-pixel similarity score from 0 to 1."""
    first_pixels = normalized_pixels(first)
    second_pixels = normalized_pixels(second)
    mean_squared_error = float(np.mean((first_pixels - second_pixels) ** 2))
    return 1.0 / (1.0 + mean_squared_error)


def compare_pair(
    first: bytes, second: bytes, first_number: int, second_number: int, threshold: float
) -> ComparisonResult:
    first_hash = sha256_bytes(first)
    second_hash = sha256_bytes(second)
    exact_match = first_hash == second_hash
    similarity = visual_similarity(first, second)
    difference = 1.0 - similarity

    if exact_match:
        decision = "Exact duplicate file"
    elif similarity >= threshold:
        decision = "Visual duplicate detected"
    else:
        decision = "Different visual image"

    return ComparisonResult(
        first=first_number,
        second=second_number,
        exact_match=exact_match,
        similarity=similarity,
        difference=difference,
        decision=decision,
    )


def difference_image(first: bytes, second: bytes) -> Image.Image:
    """Create a visual difference image for learning and debugging."""
    first_image = open_image(first).resize(NORMALIZED_SIZE)
    second_image = open_image(second).resize(NORMALIZED_SIZE)
    return ImageChops.difference(first_image, second_image)


def render_comparison(result: ComparisonResult, files: list[bytes]) -> None:
    first, second = files[result.first - 1], files[result.second - 1]
    st.subheader(f"Upload {result.first} vs Upload {result.second}")
    columns = st.columns(3)
    with columns[0]:
        st.image(first, caption=f"Upload {result.first}", use_container_width=True)
    with columns[1]:
        st.image(second, caption=f"Upload {result.second}", use_container_width=True)
    with columns[2]:
        st.image(
            difference_image(first, second),
            caption="Difference image",
            use_container_width=True,
        )

    st.metric("Visual similarity", f"{result.similarity:.3f}")
    st.progress(min(max(result.similarity, 0.0), 1.0))
    st.write(f"**Decision:** {result.decision}")
    st.caption(
        "The score compares normalized pixels. It is an educational visual score, "
        "not a biometric identity score."
    )


def main() -> None:
    st.set_page_config(
        page_title="Visual Duplicate Detector",
        page_icon="🔎",
        layout="wide",
    )
    st.title("🔎 Visual Duplicate Detector")
    st.write(
        "Upload up to five images and learn how exact hashes and visual similarity "
        "produce a transparent comparison result."
    )
    st.warning(
        "Responsible use: this project compares image files and visual appearance. "
        "It does not identify people or verify biometric identity."
    )

    with st.sidebar:
        st.header("Settings")
        threshold = st.slider(
            "Visual duplicate threshold",
            min_value=0.50,
            max_value=1.00,
            value=0.95,
            step=0.01,
            help="Higher values require images to be more visually similar.",
        )
        st.caption("This threshold is for visual testing only.")

    uploaded_files = st.file_uploader(
        "Upload five images",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        help="Select up to five images. Each file must be 10 MB or smaller.",
    )

    if not uploaded_files:
        st.info("Start by uploading one to five images.")
        return

    if len(uploaded_files) > MAX_IMAGES:
        st.error(f"Please upload no more than {MAX_IMAGES} images.")
        return

    valid_files: list[bytes] = []
    for uploaded in uploaded_files:
        data = uploaded.getvalue()
        if len(data) > MAX_FILE_SIZE_MB * 1024 * 1024:
            st.error(f"{uploaded.name} is larger than {MAX_FILE_SIZE_MB} MB.")
            return
        try:
            open_image(data)
        except (OSError, ValueError):
            st.error(f"{uploaded.name} is not a readable image.")
            return
        valid_files.append(data)

    st.success(f"Uploaded images: {len(valid_files)}")

    if len(valid_files) < 2:
        st.info("Upload at least two images to compare them.")
        return

    results = [
        compare_pair(first, second, i + 1, j + 1, threshold)
        for (i, first), (j, second) in combinations(enumerate(valid_files), 2)
    ]

    exact_matches = [result for result in results if result.exact_match]
    visual_matches = [
        result
        for result in results
        if result.similarity >= threshold and not result.exact_match
    ]

    if exact_matches or visual_matches:
        st.success(
            f"Match found: {len(exact_matches) + len(visual_matches)} pair(s) "
            "met the selected duplicate criteria."
        )
    else:
        st.info("No duplicate met the selected criteria.")

    st.subheader("Comparison summary")
    st.dataframe(
        [
            {
                "Pair": f"{result.first} vs {result.second}",
                "Similarity": round(result.similarity, 3),
                "Exact file": result.exact_match,
                "Decision": result.decision,
            }
            for result in results
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("How the decision was made")
    st.markdown(
        "1. **SHA-256** checks whether the original file bytes are identical.\n"
        "2. **Normalization** converts both images to grayscale and the same size.\n"
        "3. **Similarity** compares normalized pixel patterns.\n"
        "4. **Threshold** turns the score into a transparent visual decision."
    )

    for result in results:
        with st.expander(
            f"Upload {result.first} vs Upload {result.second}: {result.decision}"
        ):
            render_comparison(result, valid_files)


if __name__ == "__main__":
    main()
