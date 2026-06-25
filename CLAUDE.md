# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 沟通语言

**始终使用中文与用户沟通**，包括解释、确认、错误报告和所有对话。代码、命令、文件路径和变量名保持原样不变。

## 仓库用途

这是 **微购 (wego) 设计系统** — 一个 Claude Code 技能，用于生成符合微购规范、具备完整交互链路的 Web 原型项目，并支持设计 Token 合规检查、组件契约校验、布局规则约束和交互状态覆盖。

## 技能架构

技能位于 `wego-ux-design/`。**`SKILL.md` 是唯一运行时入口** — 所有 AI 行为（任务路由、必读文件、执行阶段、输出格式）均在此定义，其他文件不可覆盖。

```
SKILL.md（运行时控制）
├── 01-principles/     — 设计判断原则
├── 02-tokens/         — tokens.json 是唯一数据源；tokens.css 和文档由脚本自动生成
├── 03-components/     — registry.json 按关键词路由到组件文件；每个组件有 Canonical HTML/CSS
├── 04-ai-rules/       — SKILL.md 按任务类型挑选的详细规则（不会全部加载）
├── 05-examples/       — 非规范示例，默认不读取
├── scripts/           — 纯 Python 校验/生成脚本（无 Node 依赖）
└── resources/         — 字体、iconfont、图片等资源
```

**关键架构约束：**
- `tokens.json` → `generate_tokens.py` → `tokens.css`、`token-css-map.md`、`token-reference.md`（自动生成文件，禁止手改）
- 业务 CSS 中所有设计值必须通过 `var(--wg-*)` 使用，禁止硬编码 HEX/rgb/px
- 组件通过 `registry.json` 关键词匹配发现，不得扫描整个目录
- 布局使用 CSS Grid / Flexbox，对应 M0-M3（margin）和 G1-G2（gap）模式
- 移动端优先，设计基准 375px

## 执行流水线（4 阶段）

1. **需求确认** — 用户门禁；必须输出确认语句
2. **设计决策** — 内部 6 步依赖链（页面类型 → 信息层级 → 布局 → 组件 → Token → 交互状态）
3. **实现** — 复制 tokens.css / 资源，为命中组件写入 Canonical CSS，实现 HTML / app.css / app.js
4. **验证与输出** — 自查清单驱动：浏览器/静态验证 → 设计产物落地验证 → 合规验证

## 命令

所有脚本为纯 Python 3（无外部依赖）。从指定目录运行。

### Token 管理
```bash
# 从 tokens.json 生成 Token 文档、CSS 和 CSS 映射，仅修改 Token 定义时运行
cd wego-ux-design && python scripts/generate_tokens.py

# 检查生成文件是否最新（CI 门禁）
cd wego-ux-design && python scripts/generate_tokens.py --check
```

### 本地校验
```bash
# 校验 Token 引用、映射、漂移和示例硬编码
cd wego-ux-design && python scripts/validate_tokens.py

# 校验 Skill 任务路由、项目契约和旧约束回归
cd wego-ux-design && python scripts/validate_skill.py

# 校验 tests/fixtures/generated/ 中的生成项目
python scripts/validate_generated_projects.py
```

### 回归测试流程
1. 从 `tests/golden-prompts/` 中选取一个黄金测试用例
2. 将用例中的提示词喂给 wego-ux-design 技能 → 得到生成项目
3. 将生成项目放入 `tests/fixtures/generated/`（用中文目录名，如 `登录/`）
4. 运行 `python scripts/validate_generated_projects.py`
5. 修复失败项，重新校验，提交

### CI
`.github/workflows/validate.yml` 在 push 到 main 和 pull_request 时自动运行全部校验。CI 不调用 LLM — 仅校验已提交的 fixture。

## 修改技能时的注意事项

- **修改 AI 行为** → 编辑 `SKILL.md` 路由，同步调整被引用规则文件
- **修改 Token** → 编辑 `tokens.json`，然后运行 `generate_tokens.py`
- **新增组件** → 添加到 `registry.json` + 在 `03-components/` 中创建组件 `.md` 文件
- **新增校验规则** → 编辑 `scripts/` 中对应脚本
- `README.md` 仅供维护者查看，不作为 AI 上下文加载
- 新增详细规则放入 `04-ai-rules/`，并在 `SKILL.md` 任务路由表中注册
- 新增 Token 需要至少 3 个场景复用才允许（防止碎片化）

## 关键模式

- CSS 设计值：`color: var(--wg-color-text-primary)` / `gap: var(--wg-spacing-16)` / `border-radius: var(--wg-radius-md)`
- 页面转场：`transform` + `opacity` 配合 CSS transition，禁用 `display: none`
- 组件选择：读 registry → 匹配关键词 → 读命中组件文件 + shared-rules
- 原型输出：`index.html` + `styles/(tokens|components|app).css` + `scripts/app.js` + `assets/` — 禁止单文件
- CSS 加载顺序：`tokens.css` → `iconfont.css`（如使用）→ `components.css` → `app.css`
