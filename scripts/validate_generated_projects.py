#!/usr/bin/env python3
"""Validate generated prototype projects under tests/fixtures/generated/.

Checks:
- Project structure (index.html, styles/*, scripts/app.js)
- HTML (no inline style/script, CSS load order, external JS)
- CSS (no hardcoded design values in app.css and components.css)
- JS (addEventListener, state toggling, form validation, loading, error recovery)
- Token file matches the source tokens.css
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "wego-ux-design"
FIXTURES_DIR = ROOT / "tests" / "fixtures" / "generated"
SOURCE_TOKENS = SKILL_DIR / "design-library" / "tokens.css"

REQUIRED_FILES = [
    "index.html",
    "styles/tokens.css",
    "styles/components.css",
    "styles/app.css",
    "scripts/app.js",
]

FORBIDDEN_DIR_NAMES = {"prototype", "demo", "page1", "test", "example", "page", "pages"}

# Allowed CSS values that are not design tokens
ALLOWED_CSS_VALUES = {
    "0",
    "100%",
    "100vh",
    "100dvh",
    "auto",
    "none",
    "transparent",
    "currentColor",
    "inherit",
    "initial",
    "unset",
}

# CSS properties that legitimately take numeric values
NUMERIC_CSS_PROPERTIES = {
    "opacity",
    "z-index",  # only when using var(--wg-z-*)
    "flex",
    "flex-grow",
    "flex-shrink",
    "order",
    "grid-column",
    "grid-row",
    "line-clamp",
    "-webkit-line-clamp",
    "font-weight",
}


def validate_project_structure(project_dir: Path) -> list[str]:
    """Validate project structure."""
    errors: list[str] = []

    # Check forbidden directory names
    if project_dir.name.lower() in FORBIDDEN_DIR_NAMES:
        errors.append(f"项目目录名 '{project_dir.name}' 是禁止的通用占位名")

    # Check required files
    for required_file in REQUIRED_FILES:
        file_path = project_dir / required_file
        if not file_path.exists():
            errors.append(f"缺少必需文件: {required_file}")

    return errors


def validate_html(html_path: Path) -> list[str]:
    """Validate HTML file."""
    errors: list[str] = []
    content = html_path.read_text(encoding="utf-8")

    # Check for inline <style> with business CSS
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
    for block in style_blocks:
        # Allow empty or minimal reset styles
        if block.strip() and len(block.strip()) > 50:
            errors.append("HTML 中包含内联 <style> 块（业务样式应放在 styles/app.css）")
            break

    # Check for inline <script> with business logic
    script_blocks = re.findall(r"<script[^>]*>(.*?)</script>", content, re.DOTALL)
    for block in script_blocks:
        # Allow empty or minimal scripts
        if block.strip() and len(block.strip()) > 50:
            errors.append("HTML 中包含内联 <script> 块（业务逻辑应放在 scripts/app.js）")
            break

    # Check CSS link order
    link_tags = re.findall(r'<link[^>]+href="([^"]+)"[^>]*>', content)
    css_links = [link for link in link_tags if link.endswith(".css")]

    if css_links:
        expected_order = ["tokens.css", "iconfont.css", "components.css", "app.css"]
        actual_order = []
        for link in css_links:
            for expected in expected_order:
                if expected in link:
                    actual_order.append(expected)
                    break

        # Check if order matches
        if actual_order != expected_order:
            # Allow iconfont.css to be missing
            filtered_actual = [x for x in actual_order if x != "iconfont.css"]
            filtered_expected = [x for x in expected_order if x != "iconfont.css"]
            if filtered_actual != filtered_expected:
                errors.append(f"CSS 引入顺序不正确。期望: {' → '.join(filtered_expected)}, 实际: {' → '.join(filtered_actual)}")

    # Check for external JS
    if '<script src=' not in content and '<script type="module" src=' not in content:
        errors.append("HTML 中未通过 <script src> 引入外部 JS 文件")

    return errors


def validate_css_hardcoded_values(css_path: Path) -> list[str]:
    """Validate CSS file for hardcoded design values."""
    errors: list[str] = []
    content = css_path.read_text(encoding="utf-8")

    # Remove comments
    content_no_comments = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # Remove CSS variable definitions (--wg-*: ...)
    content_no_vars = re.sub(r"--wg-[a-z0-9-]+\s*:[^;]+;", "", content_no_comments)

    lines = content_no_vars.split("\n")

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("//"):
            continue

        # Skip CSS variable definitions
        if line.startswith("--wg-"):
            continue

        # Check for hardcoded HEX colors
        if re.search(r"#[0-9a-fA-F]{3,8}\b", line):
            # Allow in comments or variable names
            if not re.search(r"/\*.*#[0-9a-fA-F].*\*/", line):
                errors.append(f"{css_path.name}:{line_num} 包含硬编码 HEX 颜色: {line[:80]}")

        # Check for hardcoded rgb/rgba
        if re.search(r"rgba?\s*\(", line):
            errors.append(f"{css_path.name}:{line_num} 包含硬编码 rgb/rgba: {line[:80]}")

        # Check for hardcoded px values (except allowed ones)
        px_matches = re.finditer(r"(?<![-\w])(\d+(?:\.\d+)?)px", line)
        for match in px_matches:
            value = match.group(1)
            # Check if it's an allowed value
            if value not in ALLOWED_CSS_VALUES:
                # Check if it's in a transform
                if "transform" not in line and "translate" not in line:
                    errors.append(f"{css_path.name}:{line_num} 包含硬编码 px 值: {match.group(0)}")

        # Check for hardcoded z-index (should use var(--wg-z-*))
        if re.search(r"z-index\s*:\s*\d+", line) and "var(--wg-" not in line:
            errors.append(f"{css_path.name}:{line_num} 包含硬编码 z-index: {line[:80]}")

        # Check for hardcoded box-shadow (should use var(--wg-shadow-*))
        if re.search(r"box-shadow\s*:", line) and "var(--wg-" not in line:
            errors.append(f"{css_path.name}:{line_num} 包含硬编码 box-shadow: {line[:80]}")

        # Check for hardcoded border-radius (should use var(--wg-radius-*))
        if re.search(r"border-radius\s*:\s*\d+", line) and "var(--wg-" not in line:
            errors.append(f"{css_path.name}:{line_num} 包含硬编码 border-radius: {line[:80]}")

        # Check for hardcoded transition duration (should use var(--wg-duration-*))
        if re.search(r"transition.*\d+s", line) and "var(--wg-" not in line:
            errors.append(f"{css_path.name}:{line_num} 包含硬编码 transition duration: {line[:80]}")

    return errors


def validate_js(js_path: Path) -> list[str]:
    """Validate JS file for interaction signals."""
    errors: list[str] = []
    content = js_path.read_text(encoding="utf-8")

    # Check for addEventListener
    if "addEventListener" not in content:
        errors.append("app.js 中未找到 addEventListener（缺少事件监听）")

    # Check for state toggling signals
    state_signals = ["classList", "dataset", "setAttribute", "removeAttribute"]
    if not any(signal in content for signal in state_signals):
        errors.append("app.js 中未找到状态切换逻辑（classList/dataset/setAttribute/removeAttribute）")

    # Check for form validation (if form elements exist)
    form_keywords = ["input", "form", "submit", "validate", "checkValidity", "required"]
    has_form = any(keyword in content.lower() for keyword in form_keywords)
    if has_form:
        validation_keywords = ["validate", "check", "valid", "invalid", "error", "required"]
        if not any(keyword in content.lower() for keyword in validation_keywords):
            errors.append("app.js 包含表单但未找到校验逻辑")

    # Check for loading state (if submit exists)
    if "submit" in content.lower():
        loading_keywords = ["loading", "disabled", "pending", "processing"]
        if not any(keyword in content.lower() for keyword in loading_keywords):
            errors.append("app.js 包含提交逻辑但未找到处理中状态")

    # Check for error recovery (if error exists)
    if "error" in content.lower() or "fail" in content.lower():
        recovery_keywords = ["retry", "reset", "recover", "again", "重新"]
        if not any(keyword in content.lower() for keyword in recovery_keywords):
            errors.append("app.js 包含错误状态但未找到恢复/重试逻辑")

    return errors


def validate_tokens_file(project_dir: Path) -> list[str]:
    """Validate that tokens.css matches the source."""
    errors: list[str] = []

    project_tokens = project_dir / "styles" / "tokens.css"
    if not project_tokens.exists():
        return []  # Already caught by structure validation

    if not SOURCE_TOKENS.exists():
        errors.append(f"源 Token 文件不存在: {SOURCE_TOKENS}")
        return errors

    source_content = SOURCE_TOKENS.read_text(encoding="utf-8")
    project_content = project_tokens.read_text(encoding="utf-8")

    if source_content != project_content:
        errors.append(f"styles/tokens.css 与源文件不一致（使用了过期 Token 文件）")

    return errors


def validate_project(project_dir: Path) -> list[str]:
    """Validate a single generated project."""
    errors: list[str] = []

    # Structure validation
    errors.extend(validate_project_structure(project_dir))

    # HTML validation
    html_path = project_dir / "index.html"
    if html_path.exists():
        errors.extend(validate_html(html_path))

    # CSS validation (app.css and components.css)
    for css_file in ["styles/app.css", "styles/components.css"]:
        css_path = project_dir / css_file
        if css_path.exists():
            errors.extend(validate_css_hardcoded_values(css_path))

    # JS validation
    js_path = project_dir / "scripts" / "app.js"
    if js_path.exists():
        errors.extend(validate_js(js_path))

    # Token file validation
    errors.extend(validate_tokens_file(project_dir))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate generated prototype projects under tests/fixtures/generated/."
    )
    parser.add_argument(
        "--require-fixtures",
        action="store_true",
        help="Fail if no generated projects are found (for CI gate).",
    )
    args = parser.parse_args()

    if not FIXTURES_DIR.exists():
        if args.require_fixtures:
            print(f"Error: Fixtures directory not found: {FIXTURES_DIR}")
            print("No generated projects to validate (--require-fixtures enabled).")
            return 1
        print(f"Fixtures directory not found: {FIXTURES_DIR}")
        print("No projects to validate.")
        return 0

    # Find all project directories
    project_dirs = [
        d for d in FIXTURES_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ]

    if not project_dirs:
        if args.require_fixtures:
            print("Error: No generated projects found in tests/fixtures/generated/")
            print("At least one fixture is required (--require-fixtures enabled).")
            return 1
        print("No generated projects found in tests/fixtures/generated/")
        print("Skipping validation.")
        return 0

    all_errors: dict[str, list[str]] = {}

    for project_dir in sorted(project_dirs):
        errors = validate_project(project_dir)
        if errors:
            all_errors[project_dir.name] = errors

    if all_errors:
        print("Generated projects validation failed:")
        for project_name, errors in all_errors.items():
            print(f"\n[{project_name}]")
            for error in errors:
                print(f"  - {error}")
        return 1

    print(f"Generated projects validation passed: {len(project_dirs)} project(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
