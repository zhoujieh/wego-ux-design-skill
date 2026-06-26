#!/usr/bin/env python3
"""Generate CSS and Markdown token references from tokens.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from token_utils import (
    CATEGORY_TITLES,
    DESIGN_TOKENS_CSS,
    TOKENS_JSON,
    SOURCE,
    css_enabled,
    css_name,
    css_value,
    grouped_tokens,
    load_source,
    markdown_value,
)


GENERATED_NOTICE = "<!-- GENERATED FILE. DO NOT EDIT. Run: python3 scripts/generate_tokens.py -->"
def render_design_tokens_css(data: dict) -> str:
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



def render_projection(data: dict) -> str:
    """Generate hierarchical tokens.json projection for AI consumption."""
    import json
    from token_utils import css_name
    tokens = data["tokens"]
    root: dict = {}
    for name, entry in tokens.items():
        parts = name.split(".")[1:]
        node = root
        for part in parts[:-1]:
            existing = node.get(part)
            if isinstance(existing, str):
                node[part] = {"__value": existing}
            node = node.setdefault(part, {})
        leaf = parts[-1]
        if isinstance(node, str):
            continue
        if entry["category"] == "copywriting":
            node[leaf] = str(entry["value"])
        else:
            node[leaf] = "var(" + css_name(name) + ")"
    result = {
        "name": "Wego Design Tokens (AI消费投影)",
        "description": "设计库产物层 Token 投影。由 generate_tokens.py 从 tokens-source.json 自动生成，供 AI 消费。",
        "source": "tokens-source.json",
    }
    result.update(root)
    return json.dumps(result, ensure_ascii=False, indent=2) + "\n"


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
    DESIGN_TOKENS_CSS,
    ok &= write_or_check(TOKENS_JSON, render_projection(data), args.check)
    ok &= write_or_check(DESIGN_TOKENS_CSS, render_design_tokens_css(data), args.check)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
