#!/usr/bin/env python3
"""从 preview HTML 提取 Canonical CSS，聚合写入 design-library/components.css。

扫描 design-library/preview/component-*.html，
提取 @component-css-start / @component-css-end 之间的 CSS，
按组件 slug 排序后聚合输出。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_DIR = ROOT / "design-library" / "preview"
COMPONENTS_CSS = ROOT / "design-library" / "components.css"

CSS_START_MARKER = "/* @component-css-start */"
CSS_END_MARKER = "/* @component-css-end */"
HEADER = "/* 自动生成，禁止手改 — 运行 scripts/extract_components_css.py 重新生成 */"


def extract_css(html_path: Path) -> str:
    content = html_path.read_text(encoding="utf-8")
    start_idx = content.find(CSS_START_MARKER)
    end_idx = content.find(CSS_END_MARKER)

    if start_idx == -1:
        print(f"SKIP {html_path.name}: missing start marker")
        return ""
    if end_idx == -1:
        print(f"SKIP {html_path.name}: missing end marker")
        return ""

    start_pos = start_idx + len(CSS_START_MARKER)
    css_block = content[start_pos:end_idx]

    css_block = css_block.strip()
    return css_block


def slug_from_filename(filename: str) -> str:
    match = re.match(r"component-(.+)\.html$", filename)
    return match.group(1) if match else filename


def main() -> int:
    if not PREVIEW_DIR.exists():
        print("ERROR: design-library/preview/ directory not found")
        return 1

    html_files = sorted(PREVIEW_DIR.glob("component-*.html"))
    if not html_files:
        print("No component-*.html files found in preview/")
        COMPONENTS_CSS.write_text(HEADER + "\n", encoding="utf-8")
        return 0

    blocks: list[tuple[str, str]] = []
    for html_file in html_files:
        css = extract_css(html_file)
        if css:
            slug = slug_from_filename(html_file.name)
            component_name = slug.title()
            blocks.append((component_name, css))
            print(f"EXTRACT {html_file.name} → {len(css)} chars")

    blocks.sort(key=lambda x: x[0])

    lines = [HEADER, ""]
    for name, css in blocks:
        lines.append(f"/* ===== {name} ===== */")
        lines.append("")
        lines.append(css)
        lines.append("")

    output = "\n".join(lines).rstrip() + "\n"
    COMPONENTS_CSS.write_text(output, encoding="utf-8")
    print(f"\nWrote {COMPONENTS_CSS} ({len(blocks)} components)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
