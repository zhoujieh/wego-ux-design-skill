# Phase 7 Regression Record

> This record captures the deterministic checks that back the Phase 7 prompt acceptance criteria. It does not replace a live AI session review, but it verifies that the runtime contracts required by those prompts are present and validated.

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
```

Verification:

```bash
python3 wego-ux-design/scripts/validate_components.py
python3 wego-ux-design/scripts/validate_library.py
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
```

Verification:

```bash
python3 wego-ux-design/scripts/validate_components.py
python3 wego-ux-design/scripts/validate_library.py
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
```

Verification:

```bash
python3 wego-ux-design/scripts/validate_skill.py
python3 wego-ux-design/scripts/validate_tokens.py
python3 wego-ux-design/scripts/validate_components.py
```

## Golden Prompts

Regression source:

```text
tests/golden-prompts/
```

Fixture gate:

```bash
python3 scripts/validate_generated_projects.py --require-fixtures
```

Current fixture coverage:

```text
tests/fixtures/generated/登录
```
