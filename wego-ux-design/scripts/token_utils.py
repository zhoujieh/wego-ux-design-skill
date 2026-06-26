#!/usr/bin/env python3
"""Shared helpers for Wego token generation and validation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "design-library" / "tokens-source.json"
TOKENS_JSON = ROOT / "design-library" / "tokens.json"

CATEGORY_ORDER = [
    "color",
    "typography",
    "spacing",
    "radius",
    "size",
    "layout",
    "elevation",
    "stroke",
    "blur",
    "motion",
    "z-index",
    "copywriting",
]

CATEGORY_TITLES = {
    "color": "Color",
    "typography": "Typography",
    "spacing": "Spacing",
    "radius": "Radius",
    "size": "Size & Touch",
    "layout": "Layout",
    "elevation": "Elevation",
    "stroke": "Stroke",
    "blur": "Blur",
    "motion": "Motion",
    "z-index": "Z-Index",
    "copywriting": "Copywriting",
}

TOKEN_NAME_RE = re.compile(r"^wg\.[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)+$")
REFERENCE_RE = re.compile(r"^\{(wg\.[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)+)\}$")


def load_source() -> dict[str, Any]:
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def css_name(token_name: str) -> str:
    segments = token_name.split(".")[1:]
    if segments[:2] == ["font", "size"] and re.fullmatch(r"f\d+", segments[-1]):
        segments[-1] = segments[-1][1:]
    if segments[:2] == ["font", "lineHeight"] and re.fullmatch(r"f\d+", segments[-1]):
        segments[-1] = segments[-1][1:]
    normalized = [segment.lower() for segment in segments]
    return "--wg-" + "-".join(normalized)


def token_reference(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = REFERENCE_RE.fullmatch(value)
    return match.group(1) if match else None


def css_value(value: Any) -> str:
    reference = token_reference(value)
    return f"var({css_name(reference)})" if reference else str(value)


def css_enabled(entry: dict[str, Any]) -> bool:
    return entry["category"] != "copywriting"


def markdown_value(value: Any) -> str:
    reference = token_reference(value)
    return reference or str(value)


def grouped_tokens(data: dict[str, Any]) -> list[tuple[str, list[tuple[str, dict[str, Any]]]]]:
    tokens = data["tokens"]
    return [
        (
            category,
            [(name, entry) for name, entry in tokens.items() if entry["category"] == category],
        )
        for category in CATEGORY_ORDER
    ]
DESIGN_TOKENS_CSS = ROOT / "design-library" / "tokens.css"
