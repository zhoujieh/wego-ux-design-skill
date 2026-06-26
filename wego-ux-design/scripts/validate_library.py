#!/usr/bin/env python3
"""Validate design-library package integrity."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DESIGN_LIBRARY = ROOT / "design-library"
COMPONENT_DIR = DESIGN_LIBRARY / "components"
PREVIEW_DIR = DESIGN_LIBRARY / "preview"
INDEX = COMPONENT_DIR / "index.json"
COMPONENTS_CSS = DESIGN_LIBRARY / "components.css"

REQUIRED_FILES = [
    "tokens.css",
    "tokens.json",
    "scaffold.css",
    "components.css",
    "library-consumption.json",
    "components/index.json",
]
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
REQUIRED_INDEX_FIELDS = {
    "slug",
    "name",
    "category",
    "status",
    "preview",
    "contract",
}
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
CSS_START_MARKER = "/* @component-css-start */"
CSS_END_MARKER = "/* @component-css-end */"


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_json(path: Path, root: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"{rel(path, root)} does not exist"]
    except json.JSONDecodeError as exc:
        return None, [f"{rel(path, root)} is invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{rel(path, root)} must contain a JSON object"]
    return data, []


def resolve_inside(base: Path, value: str) -> Path | None:
    path = (base / value).resolve()
    try:
        path.relative_to(base.resolve())
    except ValueError:
        return None
    return path


def validate_library_package(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    library = root / "design-library"
    component_dir = library / "components"
    index_path = component_dir / "index.json"
    components_css = library / "components.css"
    errors: list[str] = []

    if not library.is_dir():
        return ["design-library directory does not exist"]

    for required in REQUIRED_FILES:
        path = library / required
        if not path.is_file():
            errors.append(f"design-library/{required} is missing")

    if not (library / "preview").is_dir():
        errors.append("design-library/preview directory is missing")
    if not component_dir.is_dir():
        errors.append("design-library/components directory is missing")

    index, index_errors = load_json(index_path, root)
    errors.extend(index_errors)
    if index is None:
        return errors

    components = index.get("components")
    if not isinstance(components, list) or not components:
        errors.append("design-library/components/index.json must contain a non-empty components array")
        return errors

    css_text = components_css.read_text(encoding="utf-8") if components_css.is_file() else ""
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

        contract_path = resolve_inside(component_dir, component["contract"])
        if contract_path is None:
            errors.append(f"{slug} contract must stay inside design-library/components")
            continue
        contract, contract_errors = load_json(contract_path, root)
        errors.extend(contract_errors)
        if contract is None:
            continue

        missing_contract = REQUIRED_CONTRACT_FIELDS - set(contract)
        if missing_contract:
            errors.append(
                f"{rel(contract_path, root)} missing fields: "
                + ", ".join(sorted(missing_contract))
            )
        if contract.get("schemaVersion") != 2:
            errors.append(f"{rel(contract_path, root)} schemaVersion must be 2")
        if contract.get("slug") != slug:
            errors.append(f"{rel(contract_path, root)} slug must match index entry {slug}")

        preview_value = component["preview"]
        preview_path = resolve_inside(library, preview_value)
        if preview_path is None:
            errors.append(f"{slug} preview must stay inside design-library")
        elif not preview_path.is_file():
            errors.append(f"{slug} preview does not exist: {preview_value}")
        else:
            preview_text = preview_path.read_text(encoding="utf-8")
            if CSS_START_MARKER not in preview_text:
                errors.append(f"{rel(preview_path, root)} missing {CSS_START_MARKER}")
            if CSS_END_MARKER not in preview_text:
                errors.append(f"{rel(preview_path, root)} missing {CSS_END_MARKER}")

        provenance = contract.get("provenance")
        if not isinstance(provenance, dict):
            errors.append(f"{rel(contract_path, root)} provenance must be an object")
            continue
        if provenance.get("preview") != preview_value:
            errors.append(f"{rel(contract_path, root)} provenance preview mismatch")
        css = provenance.get("css")
        if not isinstance(css, dict):
            errors.append(f"{rel(contract_path, root)} provenance.css must be an object")
            continue
        if css.get("file") != "components.css":
            errors.append(f"{rel(contract_path, root)} provenance.css.file must be components.css")
        marker = css.get("marker")
        if not isinstance(marker, str) or not marker:
            errors.append(f"{rel(contract_path, root)} provenance.css.marker is required")
            marker = slug.title()
        if f"/* ===== {marker} ===== */" not in css_text:
            errors.append(f"components.css missing marker: /* ===== {marker} ===== */")

    return errors


def main() -> int:
    errors = validate_library_package(ROOT)
    if errors:
        print("Library validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    print(f"Library validation passed: {len(index['components'])} components")
    return 0


if __name__ == "__main__":
    sys.exit(main())
