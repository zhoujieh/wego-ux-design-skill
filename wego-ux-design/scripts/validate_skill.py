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
    "rules/design-principles.md",
    "agents/openai.yaml",
    "design-library/library-consumption.json",
    "design-library/page-layout.json",
    "design-library/tokens.json",
    "design-library/tokens.css",
    "design-library/scaffold.css",
    "design-library/components.css",
    "design-library/components/index.json",
    "rules/execution.md",
    "rules/tokens.md",
    "rules/components.md",
    "rules/review.md",
    "rules/output.md",
    "rules/checkout.md",
    "rules/confirmation.md",
}

RUNTIME_FILES = [
    SKILL,
    ROOT / "rules" / "execution.md",
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

PHASE1_GATE_MARKERS = {
    "SKILL.md": [
        "生成类任务的首轮回复只能是《需求确认卡》",
        "未获用户确认前，不得输出原型代码、项目目录、文件内容、组件方案、页面方案或在线链接",
    ],
    "rules/execution.md": [
        "生成类任务的首轮回复只能输出《需求确认卡》",
        "未获用户确认前，不得输出原型代码、项目目录、文件内容、组件方案、页面方案、交互实现或在线链接",
    ],
    "rules/confirmation.md": [
        "生成类任务的首轮回复只能输出《需求确认卡》",
        "未获用户确认前，不得输出原型代码、项目目录、文件内容、组件方案、页面方案、交互实现或在线链接",
    ],
}

PHASE4_OUTPUT_MARKERS = {
    "rules/execution.md": [
        "已完成交付时，不得输出",
        "阶段四降级为静态代码审查",
        "交付被部署门禁阻断",
    ],
    "rules/checkout.md": [
        "不得跳过后在最终回复中补一句",
        "在线链接：阻断",
        "不得用",
    ],
    "rules/output.md": [
        "浏览器验证",
        "在线链接",
        "不得使用",
    ],
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
    if not re.search(r'^name:\s*"?wego-ux-design"?\s*$', frontmatter, re.MULTILINE):
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
        ROOT / "design-library" / "assets" / "fonts",
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
        if not (ROOT / "design-library" / "assets" / "fonts" / name).is_file():
            errors.append(f"tokens.css references missing source font: {name}")
    return errors


def validate_confirmation_card_contract() -> list[str]:
    errors: list[str] = []
    for relative, markers in PHASE1_GATE_MARKERS.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative} missing phase1 gate marker: {marker}")
    confirmation_text = (ROOT / "rules" / "confirmation.md").read_text(encoding="utf-8")
    required_confirmation_markers = (
        "唯一权威描述",
        "- 用户角色：[",
        "- 使用场景：[",
        "- 用户任务：[",
        "- 业务目标：[",
        "- 页面范围：[",
        "- 不做范围：[",
        "- 业务规则：[",
        "- 待确认：[",
    )
    for marker in required_confirmation_markers:
        if marker not in confirmation_text:
            errors.append(f"rules/confirmation.md missing confirmation card contract marker: {marker}")

    forbidden_legacy_labels = (
        "- 我理解的用户角色：[",
        "- 我理解的使用场景：[",
        "- 我理解的用户任务：[",
        "- 我理解的业务目标：[",
        "- 本次页面范围：[",
        "- 本次不做范围：[",
        "- 已知业务规则：[",
        "- 缺失信息与设计假设：[",
        "- 需要用户确认的问题：[",
        "- 设计假设：[",
    )
    for marker in forbidden_legacy_labels:
        if marker in confirmation_text:
            errors.append(f"rules/confirmation.md contains legacy confirmation card label: {marker}")
    return errors


def validate_phase4_output_contract() -> list[str]:
    errors: list[str] = []
    for relative, markers in PHASE4_OUTPUT_MARKERS.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative} missing phase4 output marker: {marker}")
    return errors



def validate_ui_kits_in_rules() -> list[str]:
    """F/G/H: Check ui_kits integration in rules files."""
    errors: list[str] = []
    root = ROOT

    # Skill runtime entry is authoritative and must expose the consumption plan.
    skill_path = root / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8") if skill_path.is_file() else ""
    skill_markers = ("设计库消费计划", "ui_kits/index.json", "quality-report.json", "page-layout.json")
    if any(marker not in skill_text for marker in skill_markers):
        errors.append("SKILL.md must mention design-library consumption plan, page-layout.json and ui_kits matching")

    # F: page-layout.json must reference the 6 broad types
    layout_path = root / "design-library" / "page-layout.json"
    if layout_path.is_file():
        layout_text = layout_path.read_text(encoding="utf-8")
        required_types = ["浏览型", "操作型", "表单型", "结果型", "异常型", "空状态"]
        for t in required_types:
            if t not in layout_text:
                errors.append(f"page-layout.json must preserve broad type: {t}")

    # G: execution.md must contain the design-library consumption plan and ui_kits matching
    exec_path = root / "rules" / "execution.md"
    exec_text = exec_path.read_text(encoding="utf-8") if exec_path.is_file() else ""
    if "设计库消费计划" not in exec_text or "ui_kits/index.json" not in exec_text:
        errors.append("execution.md must contain design-library consumption plan and ui_kits matching")

    # G: execution.md must contain missing annotation template
    if "未命中已有页面模式" not in exec_text:
        errors.append("execution.md §5 must contain ui_kits missing annotation template")

    # H: ui_kits/index.json must exist
    ui_index = root / "design-library" / "ui_kits" / "index.json"
    if not ui_index.is_file():
        errors.append("design-library/ui_kits/index.json does not exist")
    else:
        import json
        data = json.loads(ui_index.read_text(encoding="utf-8"))
        patterns = data.get("patterns", [])
        # Only require non-empty if there are ui_kit dirs with index.html
        ui_kits_dir = root / "design-library" / "ui_kits"
        has_content = False
        if ui_kits_dir.is_dir():
            for child in ui_kits_dir.iterdir():
                if child.is_dir() and not child.name.startswith("."):
                    if (child / "index.html").is_file():
                        has_content = True
                        break
        if has_content and not patterns:
            errors.append("design-library/ui_kits/index.json patterns is empty but ui_kits/ has content directories")

    return errors

def main() -> int:
    skill_text = SKILL.read_text(encoding="utf-8")
    errors = [
        *validate_ui_kits_in_rules(),
        *validate_frontmatter(skill_text),
        *validate_files(),
        *validate_runtime_contract(),
        *validate_confirmation_card_contract(),
        *validate_phase4_output_contract(),
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
