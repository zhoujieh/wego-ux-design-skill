#!/usr/bin/env python3
"""Validate the HTML component registry and component rule files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENT_ROOT = ROOT / "03-components"
REGISTRY = COMPONENT_ROOT / "registry.json"

REQUIRED_FIELDS = {
    "id",
    "name",
    "category",
    "status",
    "file",
    "keywords",
    "decisionAxes",
    "interactionMode",
}
REQUIRED_SECTIONS = {
    "## 使用决策",
    "## 语义模型",
    "## 允许组合",
    "## Anatomy",
    "## Canonical HTML",
    "## Canonical CSS",
    "## 状态",
    "## 可访问性",
    "## 生成约束",
    "## 自检",
}
VALID_STATUSES = {"draft", "stable", "deprecated"}
VALID_INTERACTION_MODES = {"static", "css", "js-required"}
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
CSS_FENCE_RE = re.compile(r"```css\n(.*?)```", re.DOTALL)
HARDCODED_CSS_RE = re.compile(
    r"(?:#[0-9A-Fa-f]{3,8}|rgba?\(|(?<![-\w])\d+(?:\.\d+)?px|!important)"
)


def main() -> int:
    errors: list[str] = []
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    components = data.get("components")
    if not isinstance(components, list) or not components:
        errors.append("registry.json must contain a non-empty components array")
        components = []

    seen: set[str] = set()
    for component in components:
        missing = REQUIRED_FIELDS - set(component)
        if missing:
            errors.append(
                f"component entry missing fields: {', '.join(sorted(missing))}"
            )
            continue

        component_id = component["id"]
        if not ID_RE.fullmatch(component_id):
            errors.append(f"invalid component id: {component_id}")
        if component_id in seen:
            errors.append(f"duplicate component id: {component_id}")
        seen.add(component_id)

        if component["status"] not in VALID_STATUSES:
            errors.append(f"{component_id} has invalid status: {component['status']}")
        if component["interactionMode"] not in VALID_INTERACTION_MODES:
            errors.append(
                f"{component_id} has invalid interactionMode: "
                f"{component['interactionMode']}"
            )
        if not isinstance(component["keywords"], list) or not component["keywords"]:
            errors.append(f"{component_id} must define non-empty keywords")
        if not isinstance(component["decisionAxes"], dict):
            errors.append(f"{component_id} decisionAxes must be an object")

        path = (COMPONENT_ROOT / component["file"]).resolve()
        if path.parent != COMPONENT_ROOT.resolve():
            errors.append(f"{component_id} file must stay inside 03-components")
            continue
        if not path.is_file():
            errors.append(f"{component_id} file does not exist: {component['file']}")
            continue

        text = path.read_text(encoding="utf-8")
        if not text.startswith(f"# {component['name']}\n"):
            errors.append(
                f"{component_id} file must start with '# {component['name']}'"
            )
        for section in sorted(REQUIRED_SECTIONS):
            if section not in text:
                errors.append(f"{component_id} missing section: {section}")
        for css_block in CSS_FENCE_RE.findall(text):
            violation = HARDCODED_CSS_RE.search(css_block)
            if violation:
                errors.append(
                    f"{component_id} Canonical CSS contains forbidden value: "
                    f"{violation.group(0)}"
                )

    if errors:
        print("Component validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Component validation passed: {len(components)} components")
    return 0


if __name__ == "__main__":
    sys.exit(main())
