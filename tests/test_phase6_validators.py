from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "wego-ux-design"


def load_module(name: str, path: Path):
    scripts_dir = str(SKILL_ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Phase6ValidatorTests(unittest.TestCase):
    def test_validate_skill_uses_final_architecture_paths(self) -> None:
        module = load_module(
            "validate_skill_architecture",
            SKILL_ROOT / "scripts" / "validate_skill.py",
        )

        required_files = set(module.REQUIRED_FILES)

        self.assertIn("principles/design-principles.md", required_files)
        self.assertIn("rules/review.md", required_files)
        self.assertIn("examples/good-ui.md", required_files)
        self.assertIn("examples/bad-ui.md", required_files)
        self.assertIn("examples/output.md", required_files)
        self.assertNotIn("01-principles/01-design-principles.md", required_files)
        self.assertNotIn("03-components/registry.json", required_files)
        self.assertFalse(
            any(path.startswith("04-ai-rules/") for path in required_files)
        )
        self.assertFalse(
            any(path.startswith("05-examples/") for path in required_files)
        )

    def test_library_consumption_declares_resource_assets_layer(self) -> None:
        data = json.loads(
            (SKILL_ROOT / "design-library" / "library-consumption.json").read_text(
                encoding="utf-8"
            )
        )

        layers = data["consumptionLayers"]
        self.assertIn("resourceAssets", layers)
        self.assertIn("assets/media", layers["resourceAssets"]["files"])
        self.assertIn("assets/icons/app-center", layers["resourceAssets"]["files"])
        self.assertIn("assets/video", layers["resourceAssets"]["files"])
        self.assertIn("assets/fonts", layers["resourceAssets"]["files"])
        self.assertIn("useResourceAssets", data["downstreamScenarios"])

    def test_business_settings_uikit_is_registered_as_structural_showcase(self) -> None:
        library = SKILL_ROOT / "design-library"
        data = json.loads((library / "library-consumption.json").read_text(encoding="utf-8"))
        available = data.get("uiKitsAvailable", [])

        self.assertIn("business-settings", available)
        self.assertTrue((library / "ui_kits" / "business-settings" / "index.html").is_file())
        self.assertTrue(
            (library / "ui_kits" / "business-settings" / "quality-report.json").is_file()
        )

        report = json.loads(
            (library / "ui_kits" / "business-settings" / "quality-report.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("business-settings", report["type"])
        self.assertEqual("structural-reference", report["copyPolicy"])
        self.assertIn("5464:4685", report["figmaSource"]["nodeId"])

    def test_business_settings_uikit_encodes_settings_layout_rules(self) -> None:
        library = SKILL_ROOT / "design-library"
        html = (
            library
            / "ui_kits"
            / "business-settings"
            / "index.html"
        ).read_text(encoding="utf-8")
        tokens = json.loads((library / "tokens-source.json").read_text(encoding="utf-8"))

        self.assertEqual("0px", tokens["tokens"]["wg.layout.page.m0.margin"]["value"])
        self.assertEqual("768px", tokens["tokens"]["wg.layout.page.max.width"]["value"])
        self.assertFalse(
            any(name.startswith("wg.layout.screen.") for name in tokens["tokens"])
        )
        self.assertFalse(
            any(name.startswith("wg.layout.width.") for name in tokens["tokens"])
        )
        self.assertIn("max-inline-size: var(--wg-layout-page-max-width)", html)
        self.assertIn("business-page wg-page-m0", html)
        self.assertIn('data-open-mode="present-bottom"', html)
        self.assertIn("nav-safe-placeholder", html)
        self.assertNotIn("statusbar__battery", html)
        self.assertNotIn("section-gap", html)
        self.assertNotIn("business-card", html)
        self.assertIn("html,\n    body {\n      block-size: 100%;\n      background: var(--wg-color-bg-surface);", html)
        self.assertIn("wg-checkbox wg-checkbox--mark-check", html)
        self.assertIn("js-permission-checkbox", html)
        self.assertIn("js-switch", html)
        self.assertIn("wg-link wg-link--standalone", html)
        self.assertIn('aria-label="业绩归属"', html)

    def test_page_width_tokens_are_consolidated_to_single_max_width(self) -> None:
        root_text_paths = [
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "rules" / "generation.md",
            SKILL_ROOT / "rules" / "output.md",
            SKILL_ROOT / "design-library" / "tokens-source.json",
            SKILL_ROOT / "design-library" / "tokens.css",
            ROOT / "website" / "styles" / "tokens.css",
        ]
        fixture_token_paths = sorted((ROOT / "tests" / "fixtures" / "generated").glob("*/styles/tokens.css"))
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [*root_text_paths, *fixture_token_paths]
            if path.exists()
        )

        self.assertIn("--wg-layout-page-max-width: 768px", combined)
        self.assertNotIn("--wg-layout-screen-", combined)
        self.assertNotIn("--wg-layout-width-", combined)
        self.assertNotIn("--wg-layout-page-max-width: 430px", combined)
        self.assertNotIn("页面最大宽度 670px", combined)

    def test_phase7_regression_record_covers_planned_prompts(self) -> None:
        record = ROOT / "tests" / "phase7-regression.md"
        text = record.read_text(encoding="utf-8")

        self.assertIn("strong 主按钮", text)
        self.assertIn("wg-button wg-button--page wg-button--strong", text)
        self.assertIn("带标题和操作的 dialog", text)
        self.assertIn("wg-dialog", text)
        self.assertIn("微购店铺设置页", text)
        self.assertIn("design-library/library-consumption.json", text)
        self.assertIn("tests/golden-prompts/", text)
        self.assertIn("scripts/validate_generated_projects.py --require-fixtures", text)

    def test_component_css_hardcoding_reports_file_and_line(self) -> None:
        module = load_module(
            "validate_components_phase6",
            SKILL_ROOT / "scripts" / "validate_components.py",
        )
        with tempfile.TemporaryDirectory() as tmp:
            preview_dir = Path(tmp)
            (preview_dir / "component-demo.html").write_text(
                "\n".join(
                    [
                        "<style>",
                        "/* @component-css-start */",
                        ".demo {",
                        "  color: white;",
                        "  background: var(--wg-color-bg-page);",
                        "  border-color: rgba(0, 0, 0, 0.12);",
                        "  padding: 12px;",
                        "  font-size: 1rem;",
                        "  opacity: 0.6;",
                        "}",
                        "/* @component-css-end */",
                        "</style>",
                    ]
                ),
                encoding="utf-8",
            )

            errors = module.validate_preview_css_hardcoding(preview_dir)

        joined = "\n".join(errors)
        self.assertIn("component-demo.html:4", joined)
        self.assertIn("component-demo.html:6", joined)
        self.assertIn("component-demo.html:7", joined)
        self.assertIn("component-demo.html:8", joined)
        self.assertIn("white", joined)
        self.assertIn("rgba(", joined)
        self.assertIn("12px", joined)
        self.assertIn("1rem", joined)
        self.assertNotIn("opacity", joined)

    def test_validate_library_package_accepts_registered_component(self) -> None:
        module = load_module(
            "validate_library_phase6",
            SKILL_ROOT / "scripts" / "validate_library.py",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            library = root / "design-library"
            (library / "components").mkdir(parents=True)
            (library / "preview").mkdir()
            for name in [
                "tokens.css",
                "tokens.json",
                "scaffold.css",
                "components.css",
                "library-consumption.json",
            ]:
                (library / name).write_text("{}", encoding="utf-8")
            (library / "components" / "index.json").write_text(
                json.dumps(
                    {
                        "schemaVersion": 2,
                        "components": [
                            {
                                "slug": "demo",
                                "name": "Demo",
                                "category": "display",
                                "status": "stable",
                                "preview": "preview/component-demo.html",
                                "contract": "demo.json",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (library / "components" / "demo.json").write_text(
                json.dumps(
                    {
                        "schemaVersion": 2,
                        "slug": "demo",
                        "name": "Demo",
                        "category": "display",
                        "variantDimensions": {},
                        "tokensConsumed": [],
                        "domAnatomy": {},
                        "usageHints": [],
                        "doNotInvent": [],
                        "provenance": {
                            "preview": "preview/component-demo.html",
                            "css": {"file": "components.css", "marker": "Demo"},
                        },
                    }
                ),
                encoding="utf-8",
            )
            (library / "preview" / "component-demo.html").write_text(
                "/* @component-css-start */\n.demo {}\n/* @component-css-end */\n",
                encoding="utf-8",
            )
            (library / "components.css").write_text(
                "/* ===== Demo ===== */\n.demo {}\n",
                encoding="utf-8",
            )

            errors = module.validate_library_package(root)

        self.assertEqual([], errors)

    def test_validate_design_library_token_names_detects_extra_css_variable(self) -> None:
        module = load_module(
            "validate_tokens_phase6",
            SKILL_ROOT / "scripts" / "validate_tokens.py",
        )
        data = {
            "tokens": {
                "wg.color.text.primary": {
                    "value": "#111111",
                    "type": "color",
                    "category": "color",
                    "description": "Primary text",
                },
                "wg.spacing.12": {
                    "value": "12px",
                    "type": "dimension",
                    "category": "spacing",
                    "description": "Spacing",
                },
                "wg.copy.button.ok": {
                    "value": "OK",
                    "type": "string",
                    "category": "copywriting",
                    "description": "Label",
                },
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            css_path = Path(tmp) / "tokens.css"
            css_path.write_text(
                ":root {\n"
                "  --wg-color-text-primary: #111111;\n"
                "  --wg-spacing-12: 12px;\n"
                "  --wg-color-unknown: #ffffff;\n"
                "}\n",
                encoding="utf-8",
            )

            errors = module.validate_design_library_token_names(data, css_path)

        self.assertEqual(
            ["design-library/tokens.css defines unknown CSS variable --wg-color-unknown"],
            errors,
        )


if __name__ == "__main__":
    unittest.main()
