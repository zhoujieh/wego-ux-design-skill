#!/usr/bin/env python3
"""Generate CSS and Markdown token references from tokens.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from token_utils import (
    CATEGORY_TITLES,
    CSS_MAP,
    PROJECT_CSS,
    REFERENCE,
    SOURCE,
    css_enabled,
    css_name,
    css_value,
    grouped_tokens,
    load_source,
    markdown_value,
)


GENERATED_NOTICE = "<!-- GENERATED FILE. DO NOT EDIT. Run: python3 scripts/generate_tokens.py -->"


def render_reference(data: dict) -> str:
    lines = [
        "# 微购 Design Token Reference",
        "",
        GENERATED_NOTICE,
        "",
        f"> Version {data['version']}  ",
        "> 唯一数据源：`tokens.json`。本文件由脚本生成，禁止手工修改。",
        "",
        "## 使用规则",
        "",
        "- 设计说明使用 `wg.*` 名称。",
        "- HTML/CSS 使用对应的 `--wg-*` 变量。",
        "- Token 值和映射只能在 `tokens.json` 中修改。",
        "",
    ]
    for category, tokens in grouped_tokens(data):
        if not tokens:
            continue
        lines.extend(
            [
                f"## {CATEGORY_TITLES[category]}",
                "",
                "| Token | CSS Variable | Value / Reference | Description |",
                "|---|---|---|---|",
            ]
        )
        for name, entry in tokens:
            css = f"`{css_name(name)}`" if css_enabled(entry) else "—"
            value = markdown_value(entry["value"]).replace("|", "\\|")
            description = entry["description"].replace("|", "\\|")
            lines.append(f"| `{name}` | {css} | `{value}` | {description} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_css_map(data: dict) -> str:
    lines = [
        "# Token → CSS 映射表",
        "",
        GENERATED_NOTICE,
        "",
        f"> Version {data['version']}  ",
        "> 唯一数据源：`02-tokens/tokens.json`。本文件由脚本生成，禁止手工修改。",
        "",
        "## 使用方式",
        "",
        "原型项目直接复制 `design-library/tokens.css` 为 `styles/tokens.css`，并通过 `<link>` 引入。下面内容仅用于查阅映射。",
        "",
        "```css",
    ]
    for font in data.get("fontFaces", []):
        lines.extend(
            [
                "@font-face {",
                f'  font-family: "{font["family"]}";',
                f'  src: url("{font["source"]}") format("opentype");',
                f'  font-weight: {font["weight"]};',
                "  font-style: normal;",
                "}",
                "",
            ]
        )
    lines.append(":root {")
    for category, tokens in grouped_tokens(data):
        css_tokens = [(name, entry) for name, entry in tokens if css_enabled(entry)]
        if not css_tokens:
            continue
        lines.append(f"  /* {CATEGORY_TITLES[category]} */")
        for name, entry in css_tokens:
            lines.append(f"  {css_name(name)}: {css_value(entry['value'])};")
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    lines.extend(
        [
            "}",
        ]
    )

    # Base reset in css-map
    reset = data.get("baseReset")
    if reset:
        lines.append("")
        margin_elements = reset.get("marginZero", [])
        if margin_elements:
            selector = ",\n".join(margin_elements)
            lines.append(f"{selector} {{")
            lines.append("  margin: var(--wg-spacing-0);")
            lines.append("}")
            lines.append("")
        list_elements = reset.get("listReset", [])
        if list_elements:
            selector = ", ".join(list_elements)
            lines.append(f"{selector} {{")
            lines.append("  padding: var(--wg-spacing-0);")
            lines.append("  list-style: none;")
            lines.append("}")
            lines.append("")
        body_defaults = reset.get("bodyDefaults", {})
        if body_defaults:
            lines.append("body {")
            if "fontFamily" in body_defaults:
                lines.append(f"  font-family: var({css_name(body_defaults['fontFamily'])});")
            if "fontSize" in body_defaults:
                lines.append(f"  font-size: var({css_name(body_defaults['fontSize'])});")
            if "lineHeight" in body_defaults:
                lines.append(f"  line-height: var({css_name(body_defaults['lineHeight'])});")
            if "color" in body_defaults:
                lines.append(f"  color: var({css_name(body_defaults['color'])});")
            lines.append("  -webkit-font-smoothing: antialiased;")
            lines.append("  -moz-osx-font-smoothing: grayscale;")
            lines.append("}")

    lines.extend(
        [
            "```",
            "",
            "## 引用示例",
            "",
            "```css",
            ".example {",
            "  color: var(--wg-color-text-primary);",
            "  background: var(--wg-color-bg-surface);",
            "  padding: var(--wg-spacing-16);",
            "  border-radius: var(--wg-radius-md);",
            "  font-size: var(--wg-font-size-14);",
            "}",
            "```",
            "",
            "Copywriting Token 不生成 CSS 变量，请从 `02-tokens/token-reference.md` 读取对应文案。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_project_css(data: dict) -> str:
    lines = [
        "/* GENERATED FILE. DO NOT EDIT. Run: python3 scripts/generate_tokens.py */",
        "/* Copy to <prototype>/styles/tokens.css and copy fonts to <prototype>/assets/fonts/. */",
        "",
    ]
    for font in data.get("fontFaces", []):
        filename = Path(font["source"]).name
        lines.extend(
            [
                "@font-face {",
                f'  font-family: "{font["family"]}";',
                f'  src: url("../assets/fonts/{filename}") format("opentype");',
                f'  font-weight: {font["weight"]};',
                "  font-style: normal;",
                "}",
                "",
            ]
        )
    lines.append(":root {")
    for category, tokens in grouped_tokens(data):
        css_tokens = [(name, entry) for name, entry in tokens if css_enabled(entry)]
        if not css_tokens:
            continue
        lines.append(f"  /* {CATEGORY_TITLES[category]} */")
        for name, entry in css_tokens:
            lines.append(f"  {css_name(name)}: {css_value(entry['value'])};")
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    lines.append("}")

    # Base reset
    reset = data.get("baseReset")
    if reset:
        lines.append("")
        lines.append("/* ============================================")
        lines.append("   基础重置")
        lines.append(f"   {reset.get('description', '')}")
        lines.append("   ============================================ */")
        lines.append("")
        margin_elements = reset.get("marginZero", [])
        if margin_elements:
            selector = ",\n".join(margin_elements)
            lines.append(f"{selector} {{")
            lines.append("  margin: var(--wg-spacing-0);")
            lines.append("}")
            lines.append("")
        list_elements = reset.get("listReset", [])
        if list_elements:
            selector = ", ".join(list_elements)
            lines.append(f"{selector} {{")
            lines.append("  padding: var(--wg-spacing-0);")
            lines.append("  list-style: none;")
            lines.append("}")
            lines.append("")
        body_defaults = reset.get("bodyDefaults", {})
        if body_defaults:
            lines.append("body {")
            if "fontFamily" in body_defaults:
                lines.append(f"  font-family: var({css_name(body_defaults['fontFamily'])});")
            if "fontSize" in body_defaults:
                lines.append(f"  font-size: var({css_name(body_defaults['fontSize'])});")
            if "lineHeight" in body_defaults:
                lines.append(f"  line-height: var({css_name(body_defaults['lineHeight'])});")
            if "color" in body_defaults:
                lines.append(f"  color: var({css_name(body_defaults['color'])});")
            lines.append("  -webkit-font-smoothing: antialiased;")
            lines.append("  -moz-osx-font-smoothing: grayscale;")
            lines.append("}")

    return "\n".join(lines).rstrip() + "\n"


def write_or_check(path: Path, expected: str, check: bool) -> bool:
    if check:
        actual = path.read_text(encoding="utf-8") if path.exists() else ""
        if actual != expected:
            print(f"OUT OF DATE: {path.relative_to(SOURCE.parents[1])}")
            return False
        return True
    path.write_text(expected, encoding="utf-8")
    print(f"Wrote {path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail when generated files are stale.")
    args = parser.parse_args()

    data = load_source()
    ok = True
    ok &= write_or_check(REFERENCE, render_reference(data), args.check)
    ok &= write_or_check(CSS_MAP, render_css_map(data), args.check)
    ok &= write_or_check(PROJECT_CSS, render_project_css(data), args.check)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
