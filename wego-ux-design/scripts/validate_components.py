#!/usr/bin/env python3
"""Validate design-library component contracts and Canonical CSS blocks."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DESIGN_LIBRARY = ROOT / "design-library"
COMPONENT_DIR = DESIGN_LIBRARY / "components"
PREVIEW_DIR = DESIGN_LIBRARY / "preview"
INDEX = COMPONENT_DIR / "index.json"

CSS_START_MARKER = "/* @component-css-start */"
CSS_END_MARKER = "/* @component-css-end */"

REQUIRED_INDEX_FIELDS = {
    "slug",
    "name",
    "category",
    "status",
    "preview",
    "contract",
}
REQUIRED_CONTRACT_FIELDS = {
    "schemaVersion",
    "slug",
    "name",
    "category",
    "variantDimensions",
    "tokensConsumed",
    "domAnatomy",
    "usageHints",
    "doNotInvent",
    "provenance",
}
VALID_CATEGORIES = {"action", "navigation", "feedback", "form", "display"}
VALID_STATUSES = {"draft", "stable", "optimizing", "deprecated"}
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
TOKEN_USE_RE = re.compile(r"^wg-[a-z0-9-]+$")
FORBIDDEN_CSS_VALUE_RE = re.compile(
    r"#(?:[0-9A-Fa-f]{3,8})\b"
    r"|rgba?\("
    r"|(?<![-\w])(?:white|black|transparent)(?![-\w])"
    r"|(?<![-\w])\d+(?:\.\d+)?(?:px|rem)\b"
)


@dataclass(frozen=True)
class CssBlock:
    path: Path
    text: str
    start_line: int


def load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"{path.relative_to(ROOT)} does not exist"]
    except json.JSONDecodeError as exc:
        return None, [f"{path.relative_to(ROOT)} is invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{path.relative_to(ROOT)} must contain a JSON object"]
    return data, []


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return path.name


def resolve_inside(base: Path, value: str) -> Path | None:
    path = (base / value).resolve()
    try:
        path.relative_to(base.resolve())
    except ValueError:
        return None
    return path


def extract_preview_css_blocks(preview_dir: Path = PREVIEW_DIR) -> tuple[list[CssBlock], list[str]]:
    errors: list[str] = []
    blocks: list[CssBlock] = []
    for path in sorted(preview_dir.glob("component-*.html")):
        text = path.read_text(encoding="utf-8")
        start = text.find(CSS_START_MARKER)
        end = text.find(CSS_END_MARKER)
        if start == -1:
            errors.append(f"{relative(path)} missing {CSS_START_MARKER}")
            continue
        if end == -1:
            errors.append(f"{relative(path)} missing {CSS_END_MARKER}")
            continue
        if end <= start:
            errors.append(f"{relative(path)} has CSS end marker before start marker")
            continue
        block_start = start + len(CSS_START_MARKER)
        blocks.append(
            CssBlock(
                path=path,
                text=text[block_start:end],
                start_line=text[:block_start].count("\n") + 1,
            )
        )
    return blocks, errors


def validate_preview_css_hardcoding(preview_dir: Path = PREVIEW_DIR) -> list[str]:
    blocks, errors = extract_preview_css_blocks(preview_dir)
    for block in blocks:
        previous_line_allows = False
        for offset, line in enumerate(block.text.splitlines()):
            if "token-lint: allow-hardcoded" in line:
                previous_line_allows = True
                continue
            if previous_line_allows:
                previous_line_allows = False
                continue
            for match in FORBIDDEN_CSS_VALUE_RE.finditer(line):
                errors.append(
                    f"{relative(block.path)}:{block.start_line + offset} "
                    f"contains hardcoded CSS value {match.group(0)}"
                )
    return errors


def validate_component_contracts() -> list[str]:
    errors: list[str] = []
    index, index_errors = load_json(INDEX)
    errors.extend(index_errors)
    if index is None:
        return errors

    components = index.get("components")
    if not isinstance(components, list) or not components:
        return ["design-library/components/index.json must contain a non-empty components array"]

    seen: set[str] = set()
    for component in components:
        if not isinstance(component, dict):
            errors.append("components/index.json contains a non-object component entry")
            continue

        missing = REQUIRED_INDEX_FIELDS - set(component)
        if missing:
            errors.append(
                "components/index.json component missing fields: "
                + ", ".join(sorted(missing))
            )
            continue

        slug = component["slug"]
        if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
            errors.append(f"invalid component slug: {slug}")
            continue
        if slug in seen:
            errors.append(f"duplicate component slug: {slug}")
        seen.add(slug)

        if component["category"] not in VALID_CATEGORIES:
            errors.append(f"{slug} has invalid category: {component['category']}")
        if component["status"] not in VALID_STATUSES:
            errors.append(f"{slug} has invalid status: {component['status']}")

        contract_path = resolve_inside(COMPONENT_DIR, component["contract"])
        if contract_path is None:
            errors.append(f"{slug} contract must stay inside design-library/components")
            continue
        contract, contract_errors = load_json(contract_path)
        errors.extend(contract_errors)
        if contract is None:
            continue

        missing_contract = REQUIRED_CONTRACT_FIELDS - set(contract)
        if missing_contract:
            errors.append(
                f"{slug} contract missing fields: {', '.join(sorted(missing_contract))}"
            )
        if contract.get("schemaVersion") != 2:
            errors.append(f"{slug} contract schemaVersion must be 2")
        if contract.get("slug") != slug:
            errors.append(f"{slug} contract slug mismatch: {contract.get('slug')}")
        if contract.get("name") != component["name"]:
            errors.append(f"{slug} contract name mismatch: {contract.get('name')}")
        if contract.get("category") != component["category"]:
            errors.append(f"{slug} contract category mismatch: {contract.get('category')}")

        tokens = contract.get("tokensConsumed")
        if not isinstance(tokens, list):
            errors.append(f"{slug} tokensConsumed must be a list")
        else:
            for token in tokens:
                if not isinstance(token, str) or not TOKEN_USE_RE.fullmatch(token):
                    errors.append(f"{slug} tokensConsumed has invalid token: {token}")

        preview_path = resolve_inside(DESIGN_LIBRARY, component["preview"])
        if preview_path is None:
            errors.append(f"{slug} preview must stay inside design-library")
        elif not preview_path.is_file():
            errors.append(f"{slug} preview does not exist: {component['preview']}")

        provenance = contract.get("provenance")
        if not isinstance(provenance, dict):
            errors.append(f"{slug} provenance must be an object")
            continue
        if provenance.get("preview") != component["preview"]:
            errors.append(f"{slug} provenance preview mismatch: {provenance.get('preview')}")
        css = provenance.get("css")
        if not isinstance(css, dict):
            errors.append(f"{slug} provenance.css must be an object")
            continue
        if css.get("file") != "components.css":
            errors.append(f"{slug} provenance.css.file must be components.css")
        marker = css.get("marker")
        if not isinstance(marker, str) or not marker:
            errors.append(f"{slug} provenance.css.marker must be a non-empty string")

    return errors


def main() -> int:
    errors = [
        *validate_component_contracts(),
        *validate_preview_css_hardcoding(),
    ]
    if errors:
        print("Component validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    print(f"Component validation passed: {len(index['components'])} components")
    return 0


if __name__ == "__main__":
    sys.exit(main())
