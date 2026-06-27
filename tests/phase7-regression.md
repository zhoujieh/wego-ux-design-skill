# Phase 7 Regression Record

> This record captures the deterministic checks that back the Phase 7 prompt acceptance criteria. It does not replace a live AI session review, but it verifies that the runtime contracts required by those prompts are present and validated.

## Phase 1 Gate

Contract evidence:

```text
wego-ux-design/SKILL.md
wego-ux-design/rules/execution.md
wego-ux-design/rules/confirmation.md
生成类任务的首轮回复只能是《需求确认卡》
未获用户确认前，不得输出原型代码、项目目录、文件内容、组件方案、页面方案或在线链接
```

Verification:

```bash
python3 wego-ux-design/scripts/validate_skill.py
python3 -m unittest tests/test_phase6_validators.py
```

## Phase 4 Output Gate

Contract evidence:

```text
wego-ux-design/rules/execution.md
wego-ux-design/rules/checkout.md
wego-ux-design/rules/output.md
不得输出“没有额外做浏览器视觉回归或线上部署”“未做浏览器验证/部署”这类完成态免责声明
在线链接：阻断
验证结果：浏览器验证 / 静态代码审查降级
```

Verification:

```bash
python3 wego-ux-design/scripts/validate_skill.py
python3 -m unittest tests/test_phase6_validators.py
```

## Prompt: strong 主按钮

Acceptance target:

```text
生成一个 strong 主按钮
```

Contract evidence:

```text
design-library/library-consumption.json
design-library/components/index.json
design-library/components/button.json
design-library/preview/component-button.html
wg-button wg-button--page wg-button--strong
tests/fixtures/generated/主按钮
```

Verification:

```bash
python3 wego-ux-design/scripts/validate_components.py
python3 wego-ux-design/scripts/validate_library.py
python3 scripts/validate_generated_projects.py --require-fixtures
```

## Prompt: 带标题和操作的 dialog

Acceptance target:

```text
生成一个带标题和操作的 dialog
```

Contract evidence:

```text
design-library/library-consumption.json
design-library/components/index.json
design-library/components/dialog.json
design-library/preview/component-dialog.html
wg-dialog
wg-dialog__title
wg-dialog__buttons
tests/fixtures/generated/弹窗
```

Verification:

```bash
python3 wego-ux-design/scripts/validate_components.py
python3 wego-ux-design/scripts/validate_library.py
python3 scripts/validate_generated_projects.py --require-fixtures
```

## Prompt: 微购店铺设置页

Acceptance target:

```text
生成一个微购店铺设置页，包含导航栏、表单行、保存按钮
```

Contract evidence:

```text
design-library/library-consumption.json
design-library/components/index.json
design-library/components/navbar.json
design-library/components/form.json
design-library/components/button.json
rules/generation.md
rules/components.md
rules/tokens.md
rules/checkout.md
tests/fixtures/generated/店铺设置
```

Verification:

```bash
python3 wego-ux-design/scripts/validate_skill.py
python3 wego-ux-design/scripts/validate_tokens.py
python3 wego-ux-design/scripts/validate_components.py
python3 scripts/validate_generated_projects.py --require-fixtures
```

## Golden Prompts

Regression source:

```text
tests/golden-prompts/
```

Fixture gate:

```bash
python3 scripts/generate_phase7_fixtures.py
python3 scripts/validate_generated_projects.py --require-fixtures
python3 -m unittest tests/test_phase7_acceptance.py
```

Current fixture coverage:

```text
tests/fixtures/generated/主按钮
tests/fixtures/generated/弹窗
tests/fixtures/generated/店铺设置
tests/fixtures/generated/登录
tests/fixtures/generated/商品发布
tests/fixtures/generated/订单列表
tests/fixtures/generated/搜索空状态
tests/fixtures/generated/删除确认
tests/fixtures/generated/表单校验失败
tests/fixtures/generated/结果页
tests/fixtures/generated/多页导航
```
