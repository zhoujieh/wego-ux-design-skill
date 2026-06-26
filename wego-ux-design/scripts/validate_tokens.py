#!/usr/bin/env python3
"""Validate Wego token source, generated artifacts, and prototype examples."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from token_utils import (
    CSS_MAP,
    PROJECT_CSS,
    REFERENCE,
    ROOT,
    TOKEN_NAME_RE,
    css_enabled,
    css_name,
    load_source,
    token_reference,
)


CSS_VAR_USE_RE = re.compile(r"var\((--wg-[a-z0-9-]+)\)")
CSS_VAR_DEF_RE = re.compile(r"(?m)^\s*(--wg-[a-z0-9-]+)\s*:")
TOKEN_USE_RE = re.compile(r"(?<![A-Za-z0-9_-])(wg\.[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)+)")
FENCE_RE = re.compile(r"```(?:css|html|text)?\n(.*?)```", re.DOTALL)
HARDCODED_STYLE_RE = re.compile(
    r"(?m)^\s*(?!-{2})[a-z-]+\s*:\s*[^;\n]*(?:#[0-9A-Fa-f]{3,8}|rgba?\(|(?<![-\w])\d+(?:\.\d+)?px)"
)

SCAN_FILES = [
    ROOT / "SKILL.md",
    ROOT / "README.md",
    ROOT / "design-library" / "library-consumption.json",
    ROOT / "design-library" / "tokens.json",
    ROOT / "design-library" / "tokens.css",
    ROOT / "design-library" / "scaffold.css",
    ROOT / "design-library" / "components.css",
    *sorted((ROOT / "design-library" / "preview").glob("component-*.html")),
    *sorted((ROOT / "principles").glob("*.md")),
    ROOT / "02-tokens" / "icon-guidelines.md",
    *sorted((ROOT / "rules").glob("*.md")),
    *sorted((ROOT / "examples").glob("*.md")),
    ROOT / "resources" / "README.md",
]
DESIGN_LIBRARY_TOKENS_CSS = ROOT / "design-library" / "tokens.css"

IGNORED_TOKEN_SUFFIXES = (
    ".xxx",
    ".custom",
    ".random",
    ".pageSpecial",
)

ALLOWED_TYPES = {
    "color",
    "fontFamily",
    "dimension",
    "shadow",
    "duration",
    "cubicBezier",
    "number",
    "string",
}

ALLOWED_CATEGORIES = {
    "color",
    "typography",
    "spacing",
    "radius",
    "size",
    "layout",
    "elevation",
    "stroke",
    "blur",
    "motion",
    "z-index",
    "copywriting",
}


def validate_source(data: dict) -> list[str]:
    errors: list[str] = []
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(data.get("version", ""))):
        errors.append("tokens.json version must use semantic version format")
    tokens = data.get("tokens")
    if not isinstance(tokens, dict) or not tokens:
        return ["tokens.json must contain a non-empty tokens object"]

    css_names: dict[str, str] = {}
    for name, entry in tokens.items():
        if not TOKEN_NAME_RE.fullmatch(name):
            errors.append(f"Invalid token name: {name}")
            continue
        required = {"value", "type", "category", "description"}
        missing = required - set(entry)
        if missing:
            errors.append(f"{name} missing fields: {', '.join(sorted(missing))}")
        extra = set(entry) - required
        if extra:
            errors.append(f"{name} contains unsupported fields: {', '.join(sorted(extra))}")
        if entry.get("type") not in ALLOWED_TYPES:
            errors.append(f"{name} has unsupported type: {entry.get('type')}")
        if entry.get("category") not in ALLOWED_CATEGORIES:
            errors.append(f"{name} has unsupported category: {entry.get('category')}")
        if not isinstance(entry.get("value"), (str, int, float)):
            errors.append(f"{name} value must be a string or number")
        if not isinstance(entry.get("description"), str):
            errors.append(f"{name} description must be a string")
        reference = token_reference(entry.get("value"))
        if reference and reference not in tokens:
            errors.append(f"{name} references undefined token: {reference}")
        if css_enabled(entry):
            variable = css_name(name)
            previous = css_names.get(variable)
            if previous:
                errors.append(f"CSS variable collision: {previous} and {name} -> {variable}")
            css_names[variable] = name

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        if name in visiting:
            errors.append(f"Token reference cycle detected at {name}")
            return
        visiting.add(name)
        reference = token_reference(tokens[name]["value"])
        if reference in tokens:
            visit(reference)
        visiting.remove(name)
        visited.add(name)

    for name in tokens:
        visit(name)

    for font in data.get("fontFaces", []):
        required = {"family", "source", "weight"}
        if set(font) != required:
            errors.append("Each fontFaces entry must contain only family, source, and weight")
            continue
        if not (ROOT / font["source"]).is_file():
            errors.append(f"Font source does not exist: {font['source']}")
    return errors


def validate_references(data: dict) -> list[str]:
    errors: list[str] = []
    tokens = data["tokens"]
    css_variables = {css_name(name) for name, entry in tokens.items() if css_enabled(entry)}

    for path in [CSS_MAP, PROJECT_CSS, REFERENCE, *SCAN_FILES]:
        text = path.read_text(encoding="utf-8")
        for variable in CSS_VAR_USE_RE.findall(text):
            if variable not in css_variables:
                errors.append(f"{path.relative_to(ROOT)} uses undefined CSS variable {variable}")
        for match in TOKEN_USE_RE.finditer(text):
            token = match.group(1)
            if text[match.end() :].startswith(".*"):
                continue
            if token in tokens or token.endswith(IGNORED_TOKEN_SUFFIXES):
                continue
            errors.append(f"{path.relative_to(ROOT)} references undefined token {token}")
    return sorted(set(errors))


def validate_design_library_token_names(
    data: dict,
    css_path: Path = DESIGN_LIBRARY_TOKENS_CSS,
) -> list[str]:
    expected = {
        css_name(name)
        for name, entry in data["tokens"].items()
        if css_enabled(entry)
    }
    text = css_path.read_text(encoding="utf-8")
    actual = set(CSS_VAR_DEF_RE.findall(text))

    errors: list[str] = []
    for variable in sorted(expected - actual):
        errors.append(f"design-library/tokens.css missing CSS variable {variable}")
    for variable in sorted(actual - expected):
        errors.append(f"design-library/tokens.css defines unknown CSS variable {variable}")
    return errors


def validate_examples() -> list[str]:
    errors: list[str] = []
    for path in sorted((ROOT / "examples").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        allow_next = False
        position = 0
        for match in FENCE_RE.finditer(text):
            prefix = text[position : match.start()]
            if "token-lint: allow-hardcoded" in prefix:
                allow_next = True
            block = match.group(1)
            if not allow_next:
                violation = HARDCODED_STYLE_RE.search(block)
                if violation:
                    line = text[: match.start(1) + violation.start()].count("\n") + 1
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line} contains hardcoded design value: "
                        f"{violation.group(0).strip()}"
                    )
            allow_next = False
            position = match.end()
    return errors


def validate_generated_files() -> list[str]:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_tokens.py"), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()] or ["Generated token files are stale"]


def main() -> int:
    data = load_source()
    errors = [
        *validate_source(data),
        *validate_generated_files(),
        *validate_design_library_token_names(data),
        *validate_references(data),
        *validate_examples(),
    ]
    if errors:
        print("Token validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Token validation passed: {len(data['tokens'])} tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
