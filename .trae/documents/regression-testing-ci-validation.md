# 回归测试与 CI 校验实施计划

## Summary

为 `wego-ux-design-skill` 仓库补齐"真实生成结果回归测试 + CI 校验"体系，证明 Skill 能稳定约束 AI 生成高质量、可交互、Token 合规的 Web 原型项目。

## Current State Analysis

**现有基础设施**：
- `SKILL.md`：定义了完整的任务路由、执行阶段、输出规范
- `02-tokens/tokens.css`：Token CSS 变量定义文件
- `03-components/`：组件注册表和组件契约
- `04-ai-rules/`：AI 执行规则、UI 生成规则、输出格式、最终检查清单
- **现有脚本**：`validate_tokens.py`、`validate_skill.py`、`validate_components.py`、`generate_tokens.py`（纯 Python，无 Node 依赖）

**缺失部分**：
- 无 `tests/` 目录
- 无 golden prompts 测试集
- 无生成结果校验脚本
- 无 CI workflow

## Proposed Changes

### 1. 新增 `tests/golden-prompts/` 目录（8 个测试用例）

每个 `.md` 文件包含：测试目标、输入提示词、期望页面类型、必须命中的组件、必须覆盖的交互状态、必须使用的 Token 类别、禁止问题、验收清单。

| 文件 | 页面类型 | 核心验证点 |
|---|---|---|
| `login-page.md` | 表单型 | 表单校验、提交中、成功/失败、失败恢复 |
| `product-publish-page.md` | 表单型 | 多字段表单、图片上传、草稿保存、发布成功 |
| `order-list-page.md` | 浏览型 | 列表加载、空状态、下拉刷新、分页 |
| `search-empty-state.md` | 空状态型 | 搜索输入、空结果反馈、推荐引导 |
| `delete-confirm-flow.md` | 操作型 | 危险操作确认、取消、成功反馈、列表更新 |
| `form-validation-failure.md` | 表单型 | 字段级校验、错误提示、提交失败、恢复 |
| `result-page.md` | 结果型 | 成功/失败结果、后续操作引导 |
| `multi-page-navigation.md` | 浏览型 | 页面跳转、返回、NavBar 联动、背景色继承 |

### 2. 新增 `tests/fixtures/generated/` 目录

空目录结构，放置 `.gitkeep` 保持目录。CI 只校验已放入的生成结果，不调用 LLM。

### 3. 新增 `scripts/validate_generated_projects.py`

扫描 `tests/fixtures/generated/` 下每个子目录，校验：

**项目结构校验**：
- 必须包含 `index.html`、`styles/tokens.css`、`styles/components.css`、`styles/app.css`、`scripts/app.js`
- 禁止 `<style>` 内联 CSS、`<script>` 内联 JS
- 禁止通用英文占位名（`prototype`、`demo`、`page1`、`test`、`example`）

**HTML 校验**：
- CSS 通过 `<link>` 引入，顺序：`tokens.css` → `iconfont.css`（如有）→ `components.css` → `app.css`
- JS 通过 `<script src>` 引入

**CSS 校验**（扫描 `app.css` 和 `components.css`）：
- 禁止硬编码：HEX、rgb/rgba、未通过 Token 的 px 值、z-index 数字、box-shadow、border-radius、transition duration
- 允许例外：`0`、`100%`、`100vh`、`100dvh`、`auto`、`none`、`transparent`、`currentColor`、CSS 变量定义、transform 中的百分比、opacity 数值、flex/grid 数字、line-clamp

**JS 校验**：
- 必须存在 `addEventListener`
- 必须存在状态切换信号：`classList`/`dataset`/`setAttribute`/`removeAttribute` 至少一种
- 表单类项目必须有校验逻辑（`required`/`validity`/`checkValidity`/自定义校验函数）
- 涉及提交的项目必须有处理中状态
- 涉及失败的项目必须有恢复/重试逻辑

**Token 文件校验**：
- `styles/tokens.css` 必须与仓库 `02-tokens/tokens.css` 内容一致

### 4. 新增 `tests/README.md`

说明 golden prompts、generated fixtures、CI 策略、手动生成流程、运行校验命令、新增测试用例流程。

### 5. 新增 `.github/workflows/validate.yml`

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python scripts/generate_tokens.py --check
      - run: python scripts/validate_tokens.py
      - run: python scripts/validate_skill.py
      - run: python scripts/validate_generated_projects.py
```

### 6. 修改 `wego-ux-design/README.md`

新增"质量验证"章节，索引 Token 校验、Skill 路由校验、生成项目回归校验、CI 入口。

## Assumptions & Decisions

1. **CI 不调用 LLM**：测试稳定性优先，fixture 由人工生成后提交
2. **CSS 校验白名单**：通过正则 + 白名单减少误伤，只抓硬编码设计值
3. **JS 校验基于信号检测**：不要求完整 AST 分析，只检测关键模式存在性
4. **Token 一致性校验**：直接文件内容比对，确保生成项目使用最新 Token
5. **所有脚本纯 Python**：无外部依赖，本地和 CI 均可直接运行

## Verification

1. 本地运行：
   ```bash
   cd wego-ux-design
   python scripts/validate_generated_projects.py
   ```
2. 放入测试 fixture 后验证校验脚本能正确通过/报错
3. CI 在 push/PR 时自动运行全部 4 个校验脚本

## 当前未覆盖的风险点

1. **组件契约合规校验**：未校验生成项目中组件是否使用了正确的 class 名和结构
2. **布局规则校验（M/G）**：未校验 CSS Grid/Flexbox 是否符合 M0/M1/M2/M3、G1/G2 定义
3. **交互链路完整性**：只检测信号存在性，不验证状态链是否完整覆盖 golden prompt 要求的所有状态
4. **资源路径有效性**：未校验 HTML 中引用的图片/字体路径是否实际存在

## 下一步建议

1. 后续可增加 `validate_components.py` 的扩展，校验生成项目中组件结构合规性
2. 可增加基于 Playwright 的截图回归测试（但会引入 Node 依赖，需权衡）
3. 可增加 Token 覆盖率报告，统计生成项目中实际使用了哪些 Token 类别

---

**新增/修改文件清单**：

| 文件 | 作用 |
|---|---|
| `tests/golden-prompts/login-page.md` | 登录页回归测试用例 |
| `tests/golden-prompts/product-publish-page.md` | 商品发布页回归测试用例 |
| `tests/golden-prompts/order-list-page.md` | 订单列表页回归测试用例 |
| `tests/golden-prompts/search-empty-state.md` | 搜索空状态回归测试用例 |
| `tests/golden-prompts/delete-confirm-flow.md` | 删除确认流程回归测试用例 |
| `tests/golden-prompts/form-validation-failure.md` | 表单校验失败回归测试用例 |
| `tests/golden-prompts/result-page.md` | 结果页回归测试用例 |
| `tests/golden-prompts/multi-page-navigation.md` | 多页导航回归测试用例 |
| `tests/fixtures/generated/.gitkeep` | 保持生成结果目录 |
| `tests/README.md` | 回归测试说明文档 |
| `scripts/validate_generated_projects.py` | 生成项目校验脚本 |
| `.github/workflows/validate.yml` | GitHub Actions CI 配置 |
| `wego-ux-design/README.md` | 新增质量验证章节 |

**本地运行命令**：
```bash
cd wego-ux-design
python scripts/validate_generated_projects.py
```

**CI 检查内容**：
- `generate_tokens.py --check`：Token 生成文件是否最新
- `validate_tokens.py`：Token 引用、映射、漂移校验
- `validate_skill.py`：Skill 路由和项目契约校验
- `validate_generated_projects.py`：生成项目结构、CSS、JS、Token 一致性校验
