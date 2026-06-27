# 回归测试体系

## 概述

本目录包含 `wego-ux-design` Skill 的回归测试体系，用于验证 Skill 生成结果是否符合运行时契约。

## 目录结构

```text
tests/
├── golden-prompts/          # 标准测试用例（输入提示词 + 验收清单）
│   ├── login-page.md
│   ├── product-publish-page.md
│   ├── order-list-page.md
│   ├── search-empty-state.md
│   ├── delete-confirm-flow.md
│   ├── form-validation-failure.md
│   ├── result-page.md
│   └── multi-page-navigation.md
├── fixtures/
│   └── generated/           # AI 实际生成的项目样本（待填充）
└── README.md                # 本文档
```

## 核心概念

### Golden Prompts（标准测试用例）

`golden-prompts/` 中的每个 `.md` 文件定义一个标准测试用例，包含：

- **输入提示词**：喂给 Skill 的完整 prompt
- **期望页面类型**：浏览/操作/表单/结果/异常/空 六类之一
- **必须命中的组件**：从 `wego-ux-design/design-library/components/index.json` 中选取
- **必须覆盖的交互状态**：初始、输入、校验、处理中、成功、失败、恢复等
- **必须使用的 Token 类别**：color、typography、spacing 等
- **禁止问题**：单文件 HTML、内联样式、硬编码设计值等
- **验收清单**：可逐项检查的通过条件

### Generated Fixtures（生成结果样本）

`fixtures/generated/` 用于存放 AI 实际生成的项目样本。每个子目录是一个完整的可运行原型项目。

**CI 不直接调用 LLM 生成结果**，原因：

1. 测试结果不稳定 — 同一 prompt 不同次生成结果不同
2. 依赖外部模型和 API — CI 环境不可控
3. 成本高 — 每次 CI 运行都消耗 LLM token
4. 速度慢 — LLM 生成需要数秒到数分钟

CI 只校验已放入 `fixtures/generated/` 的生成结果。

## 标准流程

### 如何手动生成一个新 fixture

```text
1. 从 tests/golden-prompts/ 选择一个用例
2. 使用 Skill（$wego-ux-design）生成项目
3. 将生成结果放入 tests/fixtures/generated/，目录名使用中文（如 "登录"、"商品发布"）
4. 运行 python scripts/validate_generated_projects.py
5. 修复所有失败项
6. 提交
```

阶段 7 的标准验收与 golden prompt fixtures 可用确定性脚本刷新：

```bash
python scripts/generate_phase7_fixtures.py
python scripts/validate_generated_projects.py --require-fixtures
python -m unittest tests/test_phase7_acceptance.py
```

### 如何运行校验

```bash
# 在项目根目录运行
python scripts/validate_generated_projects.py
```

### 新增测试用例的流程

1. 在 `tests/golden-prompts/` 中创建新的 `.md` 文件
2. 按照现有用例的格式填写所有必填章节
3. 确保测试用例覆盖不同的页面类型和交互模式
4. 提交后用 Skill 生成对应项目，放入 `fixtures/generated/`
5. 运行校验脚本确认通过

## CI 检查内容

CI（`.github/workflows/validate.yml`）在 push 到 main 和 pull_request 时运行：

| 脚本 | 检查内容 |
|------|---------|
| `generate_tokens.py --check` | Token 生成文件是否最新 |
| `validate_tokens.py` | Token 引用、映射、漂移校验 |
| `validate_skill.py` | Skill 路由和项目契约校验 |
| `validate_generated_projects.py` | 生成项目结构、CSS、JS、Token 一致性校验 |

CI 不依赖 Node、不依赖外部 API、不调用 LLM。

## 校验规则说明

### 项目结构校验

- 必须包含 `index.html`、`styles/tokens.css`、`styles/components.css`、`styles/app.css`、`scripts/app.js`
- 禁止 `<style>` 内联 CSS、`<script>` 内联 JS
- 禁止通用英文占位名（`prototype`、`demo`、`page1`、`test`、`example`）

### HTML 校验

- CSS 通过 `<link>` 引入，顺序：`tokens.css` → `iconfont.css`（如有）→ `components.css` → `app.css`
- JS 通过 `<script src>` 引入

### CSS 校验（扫描 `app.css` 和 `components.css`）

禁止硬编码设计值：HEX、rgb/rgba、未通过 Token 的 px 值、z-index 数字、box-shadow、border-radius、transition duration。

允许例外：`0`、`100%`、`100vh`、`100dvh`、`auto`、`none`、`transparent`、`currentColor`、CSS 变量定义、transform 中的百分比、opacity 数值、flex/grid 数字、line-clamp。

### JS 校验

- 必须存在 `addEventListener`
- 必须存在状态切换信号（`classList`/`dataset`/`setAttribute`/`removeAttribute`）
- 表单类项目必须有校验逻辑
- 涉及提交的项目必须有处理中状态
- 涉及失败的项目必须有恢复/重试逻辑

### Token 文件校验

每个生成项目的 `styles/tokens.css` 必须与仓库 `wego-ux-design/design-library/tokens.css` 内容一致。
