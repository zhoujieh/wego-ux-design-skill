# 微购 Skill 架构对齐计划

> 基于 TRAE（Nimbus Core）设计系统架构，逐项比对微购 skill 产物层的漂移和冗余，
> 输出统一的清理方案与命名对齐决策。

---

## 一、产物层对比

### TRAE 产物层（6 个根文件）

```
nimbus-core/
├── colors_and_type.css        ← 权威 Token 源头（手写 CSS，既读又复制）
├── css.json                   ← 机器可读 Token 投影（自动生成）
├── scaffold.css               ← 页面骨架（手写）
├── components.css             ← 聚合组件样式（自动生成，从 preview 提取）
├── library-consumption.json   ← AI 消费指令（手写）
└── uikit-plan.json            ← 组件白名单 + 槽位分配 + 屏幕蓝图
```

### 微购产物层（9 个根文件，3 个冗余）

```
design-library/
├── tokens-source.json         ← 唯一 Token 数据源（手写 JSON）       🟢 保留
├── tokens.json                ← Token JSON 投影（自动生成）         🟢 保留（对应 TRAE css.json）
├── tokens.css                 ← Token CSS 变量（自动生成）          🟢 保留（对应 TRAE colors_and_type.css）
├── tokens.schema.json         ← JSON Schema                        🟡 讨论
├── scaffold.css               ← 页面骨架                            🟢 保留（命名一致）
├── scaffold.html              ← 骨架测试页                          🔴 多余
├── components.css             ← 聚合组件样式（自动生成）              🟢 保留（命名一致）
├── library-consumption.json   ← AI 消费指令                         🟢 保留（命名一致）
├── token-css-map.md           ← Token→CSS 查阅映射（自动生成）       🔴 冗余
└── token-reference.md         ← Token 参考文档（自动生成）           🔴 冗余
```

---

## 二、冗余文件（直接删除）

### 2.1 `token-css-map.md`（423 行）—— 与 `tokens.css` 内容重复

**是什么**：将 `tokens.css` 的完整内容包裹在 Markdown ` ```css ` 代码块中，加上一段"使用方式"说明文字。

**谁用它**：SKILL.md 在任务路由表中指引 AI 读取它作为"查阅映射"。

**为什么冗余**：AI 可以直接读取 `tokens.css` 文件（纯 CSS 文本，完全可解析），不需要将同一段 CSS 包裹在 Markdown 里。TRAE 没有此文件——AI 读 `colors_and_type.css` 直接获取 CSS 变量。

**处理**：
- [ ] 删除 `design-library/token-css-map.md`
- [ ] 从 `token_utils.py` 移除 `CSS_MAP` 路径
- [ ] 从 `generate_tokens.py` 移除 `render_css_map()` 和对应 `write_or_check`
- [ ] 从 `validate_tokens.py` 移除 `CSS_MAP` 的引用扫描
- [ ] 从 `validate_skill.py` 的 `REQUIRED_FILES` 移除
- [ ] 在 SKILL.md 中，将所有 `design-library/token-css-map.md` 替换为 `design-library/tokens.css`（读取路径已在 `recommendedReadOrder` 中包含）

### 2.2 `token-reference.md`（427 行）—— 与 `tokens.json` + `tokens.css` 内容重复

**是什么**：以 Markdown 表格格式列出全部 355 个 Token（Token 名 | CSS 变量 | 值 | 描述），给人查阅用。

**谁用它**：仅 `validate_tokens.py` 扫描其中的 CSS 变量引用。SKILL.md 从未指引 AI 读取。

**为什么冗余**：同样的数据已存在于 `tokens.json`（JSON 结构，AI 已读）和 `tokens.css`（CSS 格式，AI 已读+复制）。TRAE 没有此文件。

**处理**：
- [ ] 删除 `design-library/token-reference.md`
- [ ] 从 `token_utils.py` 移除 `REFERENCE` 路径
- [ ] 从 `generate_tokens.py` 移除 `render_reference()` 和对应 `write_or_check`
- [ ] 从 `validate_tokens.py` 移除 `REFERENCE` 的引用扫描
- [ ] 更新 `token-css-map.md` 底部对它的引用（如果 token-css-map.md 已被删除，此条自动消除）

---

## 三、多余文件说明与处理

### 3.1 `scaffold.html` —— 骨架测试页

**是什么**：空 HTML 页面，仅引用 `tokens.css` + `scaffold.css`，用于 ITERATION_PLAN 阶段 1 验收——"在浏览器中打开检查基础样式是否正确渲染"。

**现在还有用吗**：已完成阶段 1 验收，不再需要。TRAE 没有此文件。

**处理**：
- [ ] 删除 `design-library/scaffold.html`
- 或移到 `tests/fixtures/` 作为回归测试参考。推荐直接删除——它是临时验收工具，不是设计库的一部分。

### 3.2 `tokens.schema.json` —— JSON Schema

**是什么**：`tokens-source.json` 的 JSON Schema 校验文件。

**现在还有用吗**：有用但可选。如果 `validate_tokens.py` 不依赖它进行 schema 校验，则可以删除。TRAE 没有对应文件（因为 TRAE 的源头是 CSS 文件，不需要 JSON Schema）。

**处理**：
- [ ] 检查 `validate_tokens.py` 是否调用此文件进行校验
- 如果未使用 → 删除
- 如果使用 → 保留，属工具层依赖

### 3.3 `design-library/assets/video/` —— 业务视频

**是什么**：6 个 `.mp4` 视频文件，来自微购业务场景。

**现在还有用吗**：作为原型项目的素材资源，有用。TRAE 的 `assets/` 下只有 `icons/`。

**处理**：
- [ ] 保留。属产物层的资源素材，不参与 AI 行为规则。

### 3.4 `design-library/assets/icons/app-center/` —— 业务图标

**是什么**：约 80 个微购业务 SVG 图标（ERP、企业微信、商品管理 等）。

**现在还有用吗**：有用，是微购专属的业务图标集。TRAE 的 `assets/icons/` 是通用图标。

**处理**：
- [ ] 保留，但建议整理目录名。`app-center` 是业务域名称，放在 `assets/icons/` 下合理。

---

## 四、命名对齐 TRAE

### 4.1 当前对齐状态

| TRAE | 微购 | 是否一致 | 说明 |
|------|------|:---:|------|
| `scaffold.css` | `scaffold.css` | ✅ | 完全一致 |
| `components.css` | `components.css` | ✅ | 完全一致 |
| `library-consumption.json` | `library-consumption.json` | ✅ | 完全一致 |
| `components/` | `components/` | ✅ | 完全一致 |
| `preview/` | `preview/` | ✅ | 完全一致 |
| `ui_kits/` | `ui_kits/` | ✅ | 完全一致 |
| `assets/` | `assets/` | ✅ | 完全一致 |
| `colors_and_type.css` | `tokens.css` | ⚠️ | 角色相同（CSS 变量文件），但 Wego 的 Token 不止 color + type，还包含 spacing / radius / shadow / motion 等，`tokens.css` 更准确 |
| `css.json` | `tokens.json` | ⚠️ | 角色相同（机器可读投影），但 Wego 的 `tokens.json` 已广泛引用在 SKILL.md / library-consumption.json 中 |
| `uikit-plan.json` | — | ❌ | Wego 没有，见第五节 |
| `icons.js` | — | ❌ | Wego 使用 iconfont 方案，不需要此文件 |

### 4.2 决策：保持现有命名

`tokens.css` 和 `tokens.json` 保持现有命名。原因：

- **语义更准确**：Wego 的 Token 体系远超 TRAE 的 `colors_and_type`（含 spacing、radius、shadow、motion、z-index、copywriting 等 12 个类别）
- **引用成本过高**：改名需同步更新 SKILL.md（6 处）、library-consumption.json、5 个脚本、README.md，风险远大于收益
- **TRAE 本身允许重命名**：其 SKILL.md 明确写道 "The deployed location is consumer-defined"，说明命名不是规范，角色才是

---

## 五、缺失项

### 5.1 `ui_kits/` 为空

TRAE 有 2 个 UI Kit：`dashboard`（KPI 统计 + 表格）和 `dev-explorer`（IDE 框架）。

Wego 的 `ui_kits/` 目录存在但为空（计划中的 `shop-home/` 未实现）。

**处理**：
- [ ] 后续迭代补充至少 1 个页面级 Showcase（如店铺首页、商品管理），含 `index.html` + `quality-report.json`

### 5.2 无 `uikit-plan.json`

TRAE 的 `uikit-plan.json` 定义了组件白名单、槽位分配和屏幕蓝图，是 UI Kit 生成的输入。

**是否需要**：如果后续要自动化生成 UI Kit，需要。当前阶段不阻塞。

### 5.3 无 `icons.js`

TRAE 用 `icons.js` 作为 SVG 图标的运行时精灵渲染器。

Wego 使用 **iconfont** 方案（`assets/fonts/iconfont/`），不需要此文件。不留。

---

## 六、超出计划的 4 个组件

计划中列出 13 个组件，实际有 17 个 preview HTML + JSON 契约。多出的 4 个：

| 组件 | 状态 | 处理建议 |
|------|------|---------|
| `checkbox` | 有 JSON 契约 + preview HTML | 确认 Canonical CSS 是否通过标记块机制工作，如在则保留并注册 |
| `radio` | 同上 | 同上 |
| `stacks` | 同上 | 同上 |
| `switch` | 同上 | 同上 |

**处理**：
- [ ] 逐个打开 `preview/component-{checkbox/radio/stacks/switch}.html` 确认 Canonical CSS 完整
- [ ] 确认已在 `design-library/components/index.json` 注册
- [ ] 如已完整注册 → 无需操作，视为计划外完成
- [ ] 如未注册 → 补充注册

---

## 七、执行计划汇总

### 第一阶段：立即清理（本次完成）

| # | 动作 | 文件 | 影响范围 |
|---|------|------|---------|
| 1 | 删除 | `design-library/token-css-map.md` | token_utils.py / generate_tokens.py / validate_tokens.py / validate_skill.py / SKILL.md |
| 2 | 删除 | `design-library/token-reference.md` | token_utils.py / generate_tokens.py / validate_tokens.py |
| 3 | 删除 | `design-library/scaffold.html` | 无依赖 |
| 4 | 检查后决定 | `design-library/tokens.schema.json` | validate_tokens.py |

### 第二阶段：补充完善（后续迭代）

| # | 动作 | 文件 |
|---|------|------|
| 5 | 补充 | `ui_kits/shop-home/index.html` + `quality-report.json` |
| 6 | 确认 | 4 个额外组件（checkbox/radio/stacks/switch）的注册与 CSS 完整性 |

### 清理后产物层预期（6 个根文件，对齐 TRAE）

```
design-library/
├── tokens-source.json         ← 唯一 Token 源头（手写 JSON）
├── tokens.json                ← 机器可读投影（自动生成，对应 TRAE css.json）
├── tokens.css                 ← CSS 变量（自动生成，对应 TRAE colors_and_type.css）
├── scaffold.css               ← 页面骨架（手写）
├── components.css             ← 聚合组件样式（自动生成）
├── library-consumption.json   ← AI 消费指令（手写）
├── tokens.schema.json         ← [待确认] JSON Schema
├── assets/                    ← 图标、字体、视频等资源
├── components/                ← 17 个 JSON 契约
├── preview/                   ← 17 个组件预览 HTML
└── ui_kits/                   ← 页面级 Showcase（待补充）
```

---

## 八、验证标准

- [ ] `validate_tokens.py` 通过
- [ ] `validate_skill.py` 通过
- [ ] `generate_tokens.py --check` 通过
- [ ] 全局搜索 `token-css-map` 和 `token-reference` 无残留引用
- [ ] 产物层根文件数量 ≤ 7（6 个核心 + 1 个 schema）
