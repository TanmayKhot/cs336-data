from __future__ import annotations
import os
from typing import Any

from cs336_data.html_to_text import extract_text_from_html_bytes
from cs336_data.language_identification import identify_language
from cs336_data.mask_pii import mask_emails, mask_phone_numbers, mask_ips
from cs336_data.harmful_content_filter import classify_toxic_speech, classify_nsfw
from cs336_data.quality_check import gopher_quality_filter
from cs336.cs336_data.quality_classifier import classify

def run_extract_text_from_html_bytes(html_bytes: bytes) -> str | None:
    return extract_text_from_html_bytes(html_bytes)
    raise NotImplementedError


def run_identify_language(text: str) -> tuple[Any, float]:
    return identify_language(text)
    raise NotImplementedError


def run_mask_emails(text: str) -> tuple[str, int]:
    return mask_emails(text)
    raise NotImplementedError


def run_mask_phone_numbers(text: str) -> tuple[str, int]:
    return mask_phone_numbers(text)
    raise NotImplementedError


def run_mask_ips(text: str) -> tuple[str, int]:
    return mask_ips(text)
    raise NotImplementedError


def run_classify_nsfw(text: str) -> tuple[Any, float]:
    return classify_nsfw(text)
    raise NotImplementedError


def run_classify_toxic_speech(text: str) -> tuple[Any, float]:
    return classify_toxic_speech(text)
    raise NotImplementedError


def run_classify_quality(text: str) -> tuple[Any, float]:
    print("Result: ", classify(text))
    return classify(text)
    raise NotImplementedError


def run_gopher_quality_filter(text: str) -> bool:
    return gopher_quality_filter(text)
    raise NotImplementedError


def run_exact_line_deduplication(
    input_files: list[os.PathLike], output_directory: os.PathLike
):
    raise NotImplementedError


def run_minhash_deduplication(
    input_files: list[os.PathLike],
    num_hashes: int,
    num_bands: int,
    ngrams: int,
    jaccard_threshold: float,
    output_directory: os.PathLike,
):
    raise NotImplementedError
