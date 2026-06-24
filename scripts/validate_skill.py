#!/usr/bin/env python3
"""Validate Wego skill routing and interactive prototype output contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"

REQUIRED_FILES = {
    "01-principles/01-design-principles.md",
    "02-tokens/token-usage-guidelines.md",
    "02-tokens/token-reference.md",
    "02-tokens/tokens.css",
    "token-css-map.md",
    "03-components/registry.json",
    "03-components/shared-rules.md",
    "04-ai-rules/02-ui-generation-rules.md",
    "04-ai-rules/03-ui-review-rules.md",
    "04-ai-rules/04-token-usage-rules.md",
    "04-ai-rules/06-output-format.md",
    "04-ai-rules/07-final-checklist.md",
    "agents/openai.yaml",
}

RUNTIME_FILES = [
    SKILL,
    ROOT / "03-components" / "shared-rules.md",
    ROOT / "04-ai-rules" / "01-ai-execution-rules.md",
    ROOT / "04-ai-rules" / "02-ui-generation-rules.md",
    ROOT / "04-ai-rules" / "06-output-format.md",
    ROOT / "04-ai-rules" / "07-final-checklist.md",
]

LEGACY_CONSTRAINTS = {
    "完整独立 HTML",
    "仍禁止写 JavaScript",
    "禁止写 JS",
    "`<style>` 内联",
    "默认只交付完整独立 HTML",
    "当前产品设计阶段不得读取 `03-components/`",
}

PROJECT_CONTRACT_MARKERS = {
    "02-tokens/tokens.css",
    "index.html",
    "styles/tokens.css",
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
    return errors


def validate_registry() -> list[str]:
    errors: list[str] = []
    path = ROOT / "03-components" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for component in data.get("components", []):
        component_file = ROOT / "03-components" / component.get("file", "")
        if not component_file.is_file():
            errors.append(f"Registry target does not exist: {component.get('file')}")
    return errors


def validate_project_css_assets() -> list[str]:
    errors: list[str] = []
    project_css = (ROOT / "02-tokens" / "tokens.css").read_text(encoding="utf-8")
    font_names = re.findall(r'url\("\.\./assets/fonts/([^"]+)"\)', project_css)
    if not font_names:
        errors.append("tokens.css must reference project-local fonts under ../assets/fonts/")
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
        *validate_registry(),
        *validate_project_css_assets(),
    ]
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill validation passed: routing and interactive project contract are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
