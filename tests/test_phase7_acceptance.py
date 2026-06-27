from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "generated"


def load_generated_validator():
    path = ROOT / "scripts" / "validate_generated_projects.py"
    spec = importlib.util.spec_from_file_location("validate_generated_projects_phase7", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_generated_projects_phase7"] = module
    spec.loader.exec_module(module)
    return module


class Phase7AcceptanceTests(unittest.TestCase):
    standard_prompt_fixtures = {
        "主按钮": "wg-button wg-button--page wg-button--strong",
        "弹窗": "wg-dialog",
        "店铺设置": "wg-navbar",
    }

    golden_prompt_fixtures = {
        "登录",
        "商品发布",
        "订单列表",
        "搜索空状态",
        "删除确认",
        "表单校验失败",
        "结果页",
        "多页导航",
    }

    def test_phase7_plan_items_are_marked_complete(self) -> None:
        plan = (ROOT / "ITERATION_PLAN.md").read_text(encoding="utf-8")
        match = re.search(r"## 阶段 7：回归验收(?P<body>.*?)## 附录 A", plan, re.DOTALL)
        self.assertIsNotNone(match)
        phase7 = match.group("body")
        self.assertNotIn("- [ ]", phase7)
        for item in ("7.1.1", "7.1.2", "7.2.1", "7.3.1"):
            self.assertIn(f"- [x] **{item}**", phase7)

    def test_standard_prompt_fixtures_exist_and_use_canonical_classes(self) -> None:
        for dirname, required_class in self.standard_prompt_fixtures.items():
            project = FIXTURES / dirname
            self.assertTrue(project.is_dir(), f"missing fixture directory: {dirname}")
            html = (project / "index.html").read_text(encoding="utf-8")
            self.assertIn(required_class, html)

        shop_html = (FIXTURES / "店铺设置" / "index.html").read_text(encoding="utf-8")
        self.assertIn("wg-form", shop_html)
        self.assertIn("wg-button wg-button--page wg-button--strong", shop_html)

        dialog_html = (FIXTURES / "弹窗" / "index.html").read_text(encoding="utf-8")
        self.assertIn("wg-dialog__title", dialog_html)
        self.assertIn("wg-dialog__buttons", dialog_html)

    def test_all_golden_prompts_have_generated_fixtures(self) -> None:
        missing = sorted(
            dirname for dirname in self.golden_prompt_fixtures if not (FIXTURES / dirname).is_dir()
        )
        self.assertEqual([], missing)

    def test_generated_fixtures_pass_regression_gate(self) -> None:
        module = load_generated_validator()
        projects = sorted(d for d in FIXTURES.iterdir() if d.is_dir() and not d.name.startswith("."))
        self.assertGreaterEqual(len(projects), 11)

        failures = {
            project.name: module.validate_project(project)
            for project in projects
        }
        failures = {name: errors for name, errors in failures.items() if errors}
        self.assertEqual({}, failures)


if __name__ == "__main__":
    unittest.main()
