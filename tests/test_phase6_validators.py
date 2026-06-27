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

    def test_uikit_quality_reports_are_in_page_consumption_path(self) -> None:
        data = json.loads(
            (SKILL_ROOT / "design-library" / "library-consumption.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertIn(
            "ui_kits/{type}/quality-report.json",
            data["downstreamScenarios"]["buildFullPageCustomCanvas"]["read"],
        )
        self.assertIn(
            "ui_kits/{type}/quality-report.json",
            data["recommendedReadOrder"],
        )

    def test_skill_runtime_entry_declares_uikit_matching_step(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("设计库消费计划", text)
        self.assertIn("ui_kits/index.json", text)
        self.assertIn("quality-report.json", text)

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

    def test_phase1_confirmation_card_rules_require_compact_output(self) -> None:
        module = load_module(
            "validate_skill_confirmation_contract",
            SKILL_ROOT / "scripts" / "validate_skill.py",
        )

        self.assertTrue(hasattr(module, "validate_confirmation_card_contract"))
        self.assertEqual([], module.validate_confirmation_card_contract())
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        execution_text = (SKILL_ROOT / "rules" / "execution.md").read_text(encoding="utf-8")
        confirmation_text = (SKILL_ROOT / "rules" / "confirmation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("生成类任务的首轮回复只能是《需求确认卡》", skill_text)
        self.assertIn(
            "未获用户确认前，不得输出原型代码、项目目录、文件内容、组件方案、页面方案或在线链接",
            skill_text,
        )
        self.assertIn("生成类任务的首轮回复只能输出《需求确认卡》", execution_text)
        self.assertIn(
            "未获用户确认前，不得输出原型代码、项目目录、文件内容、组件方案、页面方案、交互实现或在线链接",
            execution_text,
        )
        self.assertIn("生成类任务的首轮回复只能输出《需求确认卡》", confirmation_text)
        self.assertIn("即使用户要求“直接输出”“给我文件”“先做出来”，首轮回复仍只能是确认卡", confirmation_text)

    def test_phase4_output_contract_blocks_completion_disclaimers(self) -> None:
        module = load_module(
            "validate_skill_phase4_output_contract",
            SKILL_ROOT / "scripts" / "validate_skill.py",
        )

        self.assertTrue(hasattr(module, "validate_phase4_output_contract"))
        self.assertEqual([], module.validate_phase4_output_contract())

        execution_text = (SKILL_ROOT / "rules" / "execution.md").read_text(encoding="utf-8")
        checkout_text = (SKILL_ROOT / "rules" / "checkout.md").read_text(encoding="utf-8")
        output_text = (SKILL_ROOT / "rules" / "output.md").read_text(encoding="utf-8")

        self.assertIn(
            "不得输出“没有额外做浏览器视觉回归或线上部署”“未做浏览器验证/部署”这类完成态免责声明",
            execution_text,
        )
        self.assertIn("阶段四降级为静态代码审查", execution_text)
        self.assertIn("交付被部署门禁阻断", execution_text)
        self.assertIn("不得跳过后在最终回复中补一句“没有额外做浏览器视觉回归”", checkout_text)
        self.assertIn("在线链接：阻断", checkout_text)
        self.assertIn(
            "不得用“没有额外做浏览器视觉回归或线上部署”之类免责声明替代验证结果或阻断说明",
            checkout_text,
        )
        self.assertIn("`验证结果` 必须明确写明本次执行的是“浏览器验证”还是“静态代码审查降级”", output_text)
        self.assertIn("`在线链接` 必须填写真实公网链接；若因部署门禁未完成，写 `阻断：原因`", output_text)

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

    def test_validate_library_cross_ref_requires_quality_report_consumption(self) -> None:
        module = load_module(
            "validate_library_uikit_quality_report",
            SKILL_ROOT / "scripts" / "validate_library.py",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            library = root / "design-library"
            (library / "ui_kits").mkdir(parents=True)
            (library / "library-consumption.json").write_text(
                json.dumps(
                    {
                        "uiKitsAvailable": ["business-settings"],
                        "recommendedReadOrder": [
                            "library-consumption.json",
                            "ui_kits/index.json",
                            "ui_kits/{type}/index.html",
                        ],
                        "downstreamScenarios": {
                            "buildFullPageCustomCanvas": {
                                "read": [
                                    "ui_kits/index.json",
                                    "ui_kits/{type}/index.html",
                                ]
                            }
                        },
                        "consumptionLayers": {
                            "uikit": {
                                "files": [
                                    "ui_kits/index.json",
                                    "ui_kits/{type}/quality-report.json",
                                    "ui_kits/{type}/index.html",
                                ]
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            (library / "ui_kits" / "index.json").write_text(
                json.dumps(
                    {
                        "schemaVersion": 1,
                        "patterns": [{"type": "business-settings"}],
                    }
                ),
                encoding="utf-8",
            )

            errors = module.validate_library_consumption_cross_ref(root)

        joined = "\n".join(errors)
        self.assertIn(
            "recommendedReadOrder must include ui_kits/{type}/quality-report.json",
            joined,
        )
        self.assertIn(
            "buildFullPageCustomCanvas.read must include ui_kits/{type}/quality-report.json",
            joined,
        )

    def test_validate_library_uikit_helpers_report_bad_json(self) -> None:
        module = load_module(
            "validate_library_bad_uikit_json",
            SKILL_ROOT / "scripts" / "validate_library.py",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            library = root / "design-library"
            (library / "ui_kits").mkdir(parents=True)
            (library / "ui_kits" / "index.json").write_text("{bad json", encoding="utf-8")
            (library / "library-consumption.json").write_text("{}", encoding="utf-8")

            directory_errors = module.validate_ui_kits_directory_consistency(root)
            quality_errors = module.validate_quality_reports(root)
            cross_ref_errors = module.validate_library_consumption_cross_ref(root)

        joined = "\n".join([*directory_errors, *quality_errors, *cross_ref_errors])
        self.assertIn("design-library/ui_kits/index.json is invalid JSON", joined)

    def test_validate_skill_requires_uikit_matching_in_runtime_entry(self) -> None:
        module = load_module(
            "validate_skill_uikit_runtime_entry",
            SKILL_ROOT / "scripts" / "validate_skill.py",
        )
        original_root = module.ROOT
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "rules").mkdir(parents=True)
                (root / "design-library" / "ui_kits").mkdir(parents=True)
                (root / "SKILL.md").write_text(
                    "---\nname: wego-ux-design\ndescription: test\n---\n",
                    encoding="utf-8",
                )
                (root / "rules" / "generation.md").write_text(
                    "ui_kits/index.json\n浏览型 操作型 表单型 结果型 异常型 空状态\n",
                    encoding="utf-8",
                )
                (root / "rules" / "execution.md").write_text(
                    "设计库消费计划\nui_kits/index.json\n未命中已有页面模式\n",
                    encoding="utf-8",
                )
                (root / "design-library" / "ui_kits" / "index.json").write_text(
                    json.dumps({"schemaVersion": 1, "patterns": []}),
                    encoding="utf-8",
                )
                module.ROOT = root

                errors = module.validate_ui_kits_in_rules()
        finally:
            module.ROOT = original_root

        self.assertIn("SKILL.md must mention design-library consumption plan and ui_kits matching", errors)

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
