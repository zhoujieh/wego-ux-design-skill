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



UI_KITS_DIR = DESIGN_LIBRARY / "ui_kits"
UI_KITS_INDEX = UI_KITS_DIR / "index.json"
CONSUMPTION_JSON = DESIGN_LIBRARY / "library-consumption.json"

REQUIRED_UIKIT_INDEX_FIELDS = {
    "type", "name", "path", "qualityReport",
    "appliesTo", "openMode", "layoutMode", "background",
    "keyFeatures", "copyPolicy",
}
ALLOWED_OPEN_MODES = {"push", "present-bottom", "fade"}
ALLOWED_LAYOUT_MODES = {"M0", "M1", "M2", "M3"}
ALLOWED_BACKGROUNDS = {"bg-page", "bg-surface"}
UIKIT_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
REQUIRED_QUALITY_FIELDS = {"layoutRulesCaptured"}

RESOURCE_ASSET_DIRS = [
    "assets/fonts",
    "assets/icons/app-center",
    "assets/media",
    "assets/video",
]
def resolve_inside(base: Path, value: str) -> Path | None:
    path = (base / value).resolve()
    try:
        path.relative_to(base.resolve())
    except ValueError:
        return None
    return path





def validate_ui_kits_index(root: Path = ROOT) -> list[str]:
    """A: ui_kits/index.json legality."""
    errors: list[str] = []
    index_path = root / "design-library" / "ui_kits" / "index.json"

    if not index_path.is_file():
        return ["design-library/ui_kits/index.json does not exist"]

    data, json_errors = load_json(index_path, root)
    errors.extend(json_errors)
    if data is None:
        return errors

    if data.get("schemaVersion") != 1:
        errors.append("ui_kits/index.json schemaVersion must be 1")

    patterns = data.get("patterns")
    if not isinstance(patterns, list):
        return errors + ["ui_kits/index.json must contain a patterns array"]
    if not patterns:
        return errors + ["ui_kits/index.json patterns array is empty"]

    seen_types: set[str] = set()
    for pattern in patterns:
        if not isinstance(pattern, dict):
            errors.append("ui_kits/index.json pattern entry is not an object")
            continue

        missing = REQUIRED_UIKIT_INDEX_FIELDS - set(pattern)
        if missing:
            errors.append(f"ui_kits/index.json pattern missing fields: {', '.join(sorted(missing))}")
            continue

        ptype = pattern["type"]
        if not isinstance(ptype, str) or not UIKIT_SLUG_RE.fullmatch(ptype):
            errors.append(f"invalid ui_kit type slug: {ptype}")
            continue
        if ptype in seen_types:
            errors.append(f"duplicate ui_kit type: {ptype}")
        seen_types.add(ptype)

        if pattern.get("openMode") not in ALLOWED_OPEN_MODES:
            errors.append(f"{ptype} has invalid openMode: {pattern.get('openMode')}")
        if pattern.get("layoutMode") not in ALLOWED_LAYOUT_MODES:
            errors.append(f"{ptype} has invalid layoutMode: {pattern.get('layoutMode')}")
        if pattern.get("background") not in ALLOWED_BACKGROUNDS:
            errors.append(f"{ptype} has invalid background: {pattern.get('background')}")
        if pattern.get("copyPolicy") != "structural-reference":
            errors.append(f"{ptype} copyPolicy must be 'structural-reference'")

        applies_to = pattern.get("appliesTo")
        if not isinstance(applies_to, list) or not applies_to:
            errors.append(f"{ptype} appliesTo must be a non-empty array")

        key_features = pattern.get("keyFeatures")
        if not isinstance(key_features, list) or not key_features:
            errors.append(f"{ptype} keyFeatures must be a non-empty array")

    return errors


def validate_ui_kits_directory_consistency(root: Path = ROOT) -> list[str]:
    """B: Directory <-> index.json bidirectional check."""
    errors: list[str] = []
    ui_kits_dir = root / "design-library" / "ui_kits"
    index_path = ui_kits_dir / "index.json"

    if not index_path.is_file():
        return ["design-library/ui_kits/index.json does not exist — cannot verify directory consistency"]

    data = json.loads(index_path.read_text(encoding="utf-8"))
    patterns = data.get("patterns", [])
    registered_types = {p["type"] for p in patterns if isinstance(p, dict) and "type" in p}

    # Check: every registered pattern has its files
    for pattern in patterns:
        if not isinstance(pattern, dict):
            continue
        ptype = pattern.get("type")
        html_path = ui_kits_dir / pattern.get("path", "")
        qr_path = ui_kits_dir / pattern.get("qualityReport", "")
        if ptype:
            if not html_path.is_file():
                errors.append(f"{ptype} index.html does not exist: {pattern.get('path')}")
            if not qr_path.is_file():
                errors.append(f"{ptype} quality-report.json does not exist: {pattern.get('qualityReport')}")

    # Check: every directory with index.html is registered
    for child in sorted(ui_kits_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if not (child / "index.html").is_file():
            continue  # empty dir, skip (only warn if dir has no content at all)
        if not any((child / f).is_file() for f in child.iterdir() if f.name != ".gitkeep"):
            continue  # truly empty
        if child.name not in registered_types:
            errors.append(f"ui_kits/{child.name} has index.html but is not registered in ui_kits/index.json")

    return errors


def validate_quality_reports(root: Path = ROOT) -> list[str]:
    """C: quality-report.json legality."""
    errors: list[str] = []
    ui_kits_dir = root / "design-library" / "ui_kits"
    index_path = ui_kits_dir / "index.json"

    if not index_path.is_file():
        return []

    data = json.loads(index_path.read_text(encoding="utf-8"))
    components_index_path = root / "design-library" / "components" / "index.json"
    valid_slugs: set[str] = set()
    if components_index_path.is_file():
        comp_data = json.loads(components_index_path.read_text(encoding="utf-8"))
        for c in comp_data.get("components", []):
            if isinstance(c, dict) and "slug" in c:
                valid_slugs.add(c["slug"])

    for pattern in data.get("patterns", []):
        if not isinstance(pattern, dict):
            continue
        qr_path = ui_kits_dir / pattern.get("qualityReport", "")
        if not qr_path.is_file():
            continue

        qr_data, qr_errors = load_json(qr_path, root)
        errors.extend(qr_errors)
        if qr_data is None:
            continue

        rules = qr_data.get("layoutRulesCaptured")
        if not isinstance(rules, list) or not rules:
            errors.append(f"{pattern.get('type')} quality-report.json layoutRulesCaptured must be a non-empty array")

        temp_structures = qr_data.get("temporaryStructures")
        if isinstance(temp_structures, list):
            for ts in temp_structures:
                if isinstance(ts, dict):
                    if "name" not in ts:
                        errors.append(f"{pattern.get('type')} temporaryStructure missing 'name'")
                    if "reason" not in ts:
                        errors.append(f"{pattern.get('type')} temporaryStructure missing 'reason'")

        components_used = qr_data.get("componentsUsed")
        if isinstance(components_used, list) and valid_slugs:
            for cu in components_used:
                if isinstance(cu, dict):
                    slug = cu.get("slug")
                    if slug and slug not in valid_slugs:
                        errors.append(f"{pattern.get('type')} quality-report references unregistered component: {slug}")

    return errors


def validate_library_consumption_cross_ref(root: Path = ROOT) -> list[str]:
    """D: library-consumption.json cross-reference with ui_kits/index.json."""
    errors: list[str] = []
    consumption_path = root / "design-library" / "library-consumption.json"
    index_path = root / "design-library" / "ui_kits" / "index.json"

    if not consumption_path.is_file():
        return ["design-library/library-consumption.json does not exist"]
    if not index_path.is_file():
        return []

    consumption = json.loads(consumption_path.read_text(encoding="utf-8"))
    index_data = json.loads(index_path.read_text(encoding="utf-8"))

    # uiKitsAvailable must match index types
    available = set(consumption.get("uiKitsAvailable", []))
    registered = {p["type"] for p in index_data.get("patterns", []) if isinstance(p, dict) and "type" in p}

    missing_in_available = registered - available
    extra_in_available = available - registered

    for t in sorted(missing_in_available):
        errors.append(f"ui_kit type '{t}' registered in ui_kits/index.json but missing from library-consumption.json uiKitsAvailable")
    for t in sorted(extra_in_available):
        errors.append(f"ui_kit type '{t}' in library-consumption.json uiKitsAvailable but not in ui_kits/index.json")

    # recommendedReadOrder must include ui_kits/index.json
    read_order = consumption.get("recommendedReadOrder", [])
    if "ui_kits/index.json" not in read_order:
        errors.append("library-consumption.json recommendedReadOrder must include ui_kits/index.json")

    # downstreamScenarios.buildFullPageCustomCanvas must reference ui_kits/index.json
    scenario = consumption.get("downstreamScenarios", {}).get("buildFullPageCustomCanvas", {})
    scenario_read = scenario.get("read", [])
    if "ui_kits/index.json" not in scenario_read:
        errors.append("library-consumption.json downstreamScenarios.buildFullPageCustomCanvas.read must include ui_kits/index.json")

    # consumptionLayers.uikit must reference ui_kits/index.json
    uikit_files = consumption.get("consumptionLayers", {}).get("uikit", {}).get("files", [])
    if "ui_kits/index.json" not in uikit_files:
        errors.append("library-consumption.json consumptionLayers.uikit.files must include ui_kits/index.json")

    return errors


def validate_resource_assets(root: Path = ROOT) -> list[str]:
    """E: Resource asset directory integrity."""
    errors: list[str] = []
    design_library = root / "design-library"

    for rel_dir in RESOURCE_ASSET_DIRS:
        path = design_library / rel_dir
        if not path.is_dir():
            errors.append(f"design-library/{rel_dir} directory is missing")
            continue

        has_content = any(
            f.is_file() and not f.name.startswith(".")
            for f in path.iterdir()
        ) or any(
            sub.is_dir() and not sub.name.startswith(".")
            for sub in path.iterdir()
        )
        if not has_content:
            errors.append(f"design-library/{rel_dir} exists but is empty — may need content or .gitkeep")

    # media/index.json must exist
    media_index = design_library / "assets" / "media" / "index.json"
    if not media_index.is_file():
        errors.append("design-library/assets/media/index.json is missing")

    # token font references
    tokens_css = design_library / "tokens.css"
    if tokens_css.is_file():
        css_text = tokens_css.read_text(encoding="utf-8")
        font_refs = re.findall(r'url\("\.\./assets/fonts/([^"]+)"\)', css_text)
        for ref in font_refs:
            font_path = design_library / "assets" / "fonts" / ref
            if not font_path.is_file():
                errors.append(f"tokens.css references missing font: assets/fonts/{ref}")

    return errors

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

    ui_kits_errors = validate_ui_kits_index(ROOT)
    errors.extend(ui_kits_errors)

    dir_errors = validate_ui_kits_directory_consistency(ROOT)
    errors.extend(dir_errors)

    qr_errors = validate_quality_reports(ROOT)
    errors.extend(qr_errors)

    cross_ref_errors = validate_library_consumption_cross_ref(ROOT)
    errors.extend(cross_ref_errors)

    resource_errors = validate_resource_assets(ROOT)
    errors.extend(resource_errors)

    if errors:
        print("Library validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    ui_kit_count = 0
    if UI_KITS_INDEX.is_file():
        ui_data = json.loads(UI_KITS_INDEX.read_text(encoding="utf-8"))
        ui_kit_count = len(ui_data.get("patterns", []))
    print(f"Library validation passed: {len(index['components'])} components, {ui_kit_count} ui_kits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
