#!/usr/bin/env python3
"""Validate Wego skill routing and design-library consumption contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"

REQUIRED_FILES = {
    "principles/design-principles.md",
    "02-tokens/icon-guidelines.md",
    "02-tokens/tokens.css",
    "agents/openai.yaml",
    "design-library/library-consumption.json",
    "design-library/tokens.json",
    "design-library/tokens.css",
    "design-library/scaffold.css",
    "design-library/components.css",
    "design-library/components/index.json",
    "rules/execution.md",
    "rules/generation.md",
    "rules/tokens.md",
    "rules/components.md",
    "rules/review.md",
    "rules/output.md",
    "rules/checkout.md",
    "rules/confirmation.md",
    "examples/good-ui.md",
    "examples/bad-ui.md",
    "examples/output.md",
    "resources/README.md",
    "token-css-map.md",
}

RUNTIME_FILES = [
    SKILL,
    ROOT / "rules" / "execution.md",
    ROOT / "rules" / "generation.md",
    ROOT / "rules" / "tokens.md",
    ROOT / "rules" / "components.md",
    ROOT / "rules" / "review.md",
    ROOT / "rules" / "output.md",
    ROOT / "rules" / "checkout.md",
    ROOT / "rules" / "confirmation.md",
]

LEGACY_CONSTRAINTS = {
    "完整独立 HTML",
    "仍禁止写 JavaScript",
    "禁止写 JS",
    "`<style>` 内联",
    "默认只交付完整独立 HTML",
}

PROJECT_CONTRACT_MARKERS = {
    "design-library/library-consumption.json",
    "design-library/tokens.css",
    "design-library/components.css",
    "design-library/components/index.json",
    "index.html",
    "styles/tokens.css",
    "styles/components.css",
    "styles/app.css",
    "scripts/app.js",
    "完整项目目录",
    "关键交互",
}


def validate_frontmatter(text: str) -> list[str]:
    errors: list[str] = []
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return ["SKILL.md must start with YAML frontmatter"]
    frontmatter = match.group(1)
    keys = re.findall(r"^([a-zA-Z0-9_-]+):", frontmatter, re.MULTILINE)
    if keys != ["name", "description"]:
        errors.append("SKILL.md frontmatter must contain only name and description")
    if not re.search(r"^name:\s*wego-ux-design\s*$", frontmatter, re.MULTILINE):
        errors.append("SKILL.md name must be wego-ux-design")
    if "可交互" not in frontmatter or "Web 原型项目" not in frontmatter:
        errors.append("SKILL.md description must advertise interactive Web prototype projects")
    return errors


def validate_files() -> list[str]:
    return [
        f"Missing required file: {relative}"
        for relative in sorted(REQUIRED_FILES)
        if not (ROOT / relative).is_file()
    ]


def validate_runtime_contract() -> list[str]:
    errors: list[str] = []
    combined = "\n".join(path.read_text(encoding="utf-8") for path in RUNTIME_FILES)
    for phrase in sorted(LEGACY_CONSTRAINTS):
        if phrase in combined:
            errors.append(f"Legacy runtime constraint remains: {phrase}")
    skill_text = SKILL.read_text(encoding="utf-8")
    for marker in sorted(PROJECT_CONTRACT_MARKERS):
        if marker not in skill_text:
            errors.append(f"SKILL.md missing project contract marker: {marker}")
    if "页面级临时结构" not in skill_text or "组件候选" not in skill_text:
        errors.append("SKILL.md must define the incomplete-component fallback")
    if "严禁自己手写组件 CSS" not in skill_text:
        errors.append("SKILL.md must forbid handwritten component CSS")
    return errors


def validate_library_consumption() -> list[str]:
    errors: list[str] = []
    path = ROOT / "design-library" / "library-consumption.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    required_keys = {
        "tokenSource",
        "tokenCss",
        "scaffoldCss",
        "componentsCss",
        "componentsIndex",
        "componentContractDir",
        "previewDir",
        "iconsDir",
        "uiKitsDir",
        "consumptionLayers",
        "downstreamScenarios",
        "recommendedReadOrder",
        "hardConstraints",
    }
    missing = required_keys - set(data)
    if missing:
        errors.append(
            f"library-consumption.json missing keys: {', '.join(sorted(missing))}"
        )
    read_order = data.get("recommendedReadOrder", [])
    if not read_order or read_order[0] != "library-consumption.json":
        errors.append("library-consumption.json must be first in recommendedReadOrder")

    for key in ("tokenSource", "tokenCss", "scaffoldCss", "componentsCss", "componentsIndex"):
        value = data.get(key)
        if isinstance(value, str) and not (ROOT / "design-library" / value).exists():
            errors.append(f"library-consumption.json points to missing path: {value}")

    for key in ("componentContractDir", "previewDir", "iconsDir", "uiKitsDir"):
        value = data.get(key)
        if isinstance(value, str) and not (ROOT / "design-library" / value).exists():
            errors.append(f"library-consumption.json points to missing directory: {value}")

    layers = data.get("consumptionLayers", {})
    if "resourceAssets" not in layers:
        errors.append("library-consumption.json must declare consumptionLayers.resourceAssets")
    scenarios = data.get("downstreamScenarios", {})
    if "useResourceAssets" not in scenarios:
        errors.append("library-consumption.json must declare downstreamScenarios.useResourceAssets")

    for resource_path in (
        ROOT / "resources" / "README.md",
        ROOT / "resources" / "images",
        ROOT / "resources" / "fonts",
        ROOT / "design-library" / "assets" / "icons",
        ROOT / "design-library" / "assets" / "video",
    ):
        if not resource_path.exists():
            errors.append(f"resource asset path is missing: {resource_path.relative_to(ROOT)}")
    return errors


def validate_components_index() -> list[str]:
    errors: list[str] = []
    path = ROOT / "design-library" / "components" / "index.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    components = data.get("components", [])
    if not components:
        return ["design-library/components/index.json must contain a non-empty components array"]
    for component in components:
        contract = ROOT / "design-library" / "components" / component.get("contract", "")
        preview = ROOT / "design-library" / component.get("preview", "")
        if not contract.is_file():
            errors.append(f"Component contract does not exist: {component.get('contract')}")
        if not preview.is_file():
            errors.append(f"Component preview does not exist: {component.get('preview')}")
    return errors


def validate_project_css_assets() -> list[str]:
    errors: list[str] = []
    project_css = (ROOT / "design-library" / "tokens.css").read_text(encoding="utf-8")
    font_names = re.findall(r'url\("\.\./assets/fonts/([^"]+)"\)', project_css)
    if not font_names:
        errors.append("design-library/tokens.css must reference project-local fonts under ../assets/fonts/")
    for name in font_names:
        if not (ROOT / "resources" / "fonts" / name).is_file():
            errors.append(f"tokens.css references missing source font: {name}")
    return errors


def main() -> int:
    skill_text = SKILL.read_text(encoding="utf-8")
    errors = [
        *validate_frontmatter(skill_text),
        *validate_files(),
        *validate_runtime_contract(),
        *validate_library_consumption(),
        *validate_components_index(),
        *validate_project_css_assets(),
    ]
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill validation passed: routing and design-library contracts are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
