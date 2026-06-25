# 微购设计系统 Skill 迭代计划地图

> **目标**：基于 TRAE 设计库架构，让 AI 稳定输出统一的微购设计页面。
>
> **核心策略**：把每个组件的 Canonical CSS 写进 preview HTML 标记块 → 脚本提取聚合到 components.css → AI 只读不改。
>
> **使用方式**：按编号顺序推进，每完成一条勾选 `[x]`，每个里程碑可独立验收。

---

## 整体架构：三层分离、单向依赖

```
wego-design-skill/
│
├── SKILL.md                           ← 唯一运行时入口
│
├── ── 控制层：告诉 AI 做什么、怎么做、什么不能做 ──
│   ├── rules/
│   │   ├── execution.md               ← 4 阶段执行总流程 + 门禁
│   │   ├── generation.md              ← UI 生成规则
│   │   ├── components.md              ← 组件选用规则
│   │   ├── tokens.md                  ← Token 使用规则
│   │   ├── forbidden.md               ← 禁止事项清单
│   │   ├── output.md                  ← 输出格式规范
│   │   ├── checkout.md                ← 最终检查清单
│   │   └── confirmation.md           ← 需求确认规则
│   ├── principles/
│   │   └── design-principles.md       ← 最高设计原则（兜底安全网，可选）
│   └── examples/
│       ├── good-ui.md                 ← 正面示例
│       ├── bad-ui.md                  ← 反例示例
│       └── output.md                  ← 标准输出示例
│
├── ── 产物层：给 AI 直接复制的可渲染产物 ──
│   └── design-library/
│       ├── tokens.css                 ← Token CSS 变量定义
│       ├── tokens.json                ← Token JSON 投影
│       ├── scaffold.css               ← 页面骨架
│       ├── components.css             ← 聚合组件样式（自动生成）
│       ├── library-consumption.json   ← AI 消费指令
│       ├── preview/                   ← 组件预览页（含 Canonical CSS）
│       │   └── component-*.html
│       ├── components/                ← 组件 JSON 契约
│       │   ├── index.json
│       │   └── *.json
│       ├── ui_kits/                   ← 页面级 Showcase
│       └── assets/                    ← 图标、字体
│
└── ── 工具层：维护 + 质量守护 ──
    └── scripts/
        ├── extract_components_css.py  ← preview HTML → components.css
        ├── validate_library.py        ← 包体完整性检查
        ├── validate_components.py     ← 硬编码检查
        └── validate_tokens.py         ← Token 一致性检查
```

## 架构原则

```
控制层（rules/）  →  定义边界：「什么能做、什么不能做」
产物层（design-library/）→  提供锚点：「可以直接复制的 CSS + markup」
工具层（scripts/） →  保证一致性：「自动生成 + 自动校验」

AI 的工作变成：按 rules 决策 → 从 design-library 复制产物 → 自己只写页面级布局胶水
```

### 关于最高设计原则

`principles/design-principles.md` 是兜底安全网：当组件 `doNotInvent` 和 `hardConstraints` 还没覆盖某个场景时，AI 至少有一个方向判断依据。当以下条件全部满足后可删除：

- ✅ 组件 `doNotInvent` 覆盖所有不该做的事
- ✅ `library-consumption.json` 的 `hardConstraints` 覆盖所有禁止项
- ✅ Canonical CSS 覆盖所有组件变体
- ✅ `rules/forbidden.md` 覆盖所有视觉禁忌
- ✅ `examples/` 中有正反例覆盖典型歧义场景

---

## 迭代总览

```
阶段 1（骨架）       阶段 2（组件试点）     阶段 3（批量Canonicalize）  阶段 4（契约+注册）
 7 个任务              4 个任务                6 个任务                  4 个任务
 ─────────────────────────────────────────────────────────────────────────────────

 阶段 5（消费契约）    阶段 6（校验闭环）      阶段 7（回归验收）
 3 个任务              3 个任务                3 个任务
 ─────────────────────────────────────────────────────────────────────────────────

 总计 30 个任务，预计 7 个验收节点
```

---

## 阶段 1：设计库包体骨架搭建

> **验收标准**：目录结构完整、Token 可被浏览器消费、有页面骨架样式、有 Token 机器可读投影。
>
> **验收方式**：在浏览器中打开 `scaffold.html`（新建的空页引用 scaffold.css + tokens.css），检查背景色、字体、标题类是否正确渲染。

### 1.1 创建设计库根目录

- [x] **1.1.1** 在 `wego-ux-design/` 下创建 `design-library/` 目录（作为设计库包体根）
  - 验收：目录存在且结构符合规划

### 1.2 Token 相关文件

- [x] **1.2.1** 创建 `design-library/tokens.css`，将现有 CSS 变量写入
  - 包含全部 `--wg-*` Token 定义（颜色、字号、间距、圆角、组件专属 Token）
  - 来源：现有 `02-tokens/tokens.css`（后续由 `generate_tokens.py` 生成）
  - 验收：文件存在，CSS 变量完整

- [x] **1.2.2** 创建 `design-library/tokens.json`，将 Token 按分组输出为机器可读投影
  - 输出格式：`{ "color": { "group": { "token-name": { "hex": "...", "opacity": "1" } } }, "font": {...}, "radius": {...}, "spacing": {...} }`
  - 来源：由 `scripts/generate_tokens.py` 生成（后续补齐脚本参数）
  - 验收：文件存在，JSON 结构正确

### 1.3 手写 scaffold.css

- [x] **1.3.1** 创建 `design-library/scaffold.css`，包含：
  - CSS Reset（清除所有浏览器默认 margin/padding/list-style）
  - html/body 基础样式（引用 `--wg-*` Token：背景色、字体、字号、字色）
  - 排版工具类：`.wg-h1`、`.wg-h2`、`.wg-h3`、`.wg-eyebrow`、`.wg-text-secondary`、`.wg-text-tertiary`
  - 布局工具类：`.wg-row`、`.wg-col`、`.wg-grid-{n}`、`.wg-stack-{n}`
  - 验收：文件存在，在浏览器中引用后页面基础样式正常

- [x] **1.3.2** 创建 `design-library/scaffold.html`（空 HTML 页面，仅引用 tokens.css + scaffold.css）
  - 页面内放置 h1/h2/h3/eyebrow/text-secondary 等测试元素
  - 验收：浏览器打开后样式正确渲染

### 1.4 空占位文件

- [x] **1.4.1** 创建空的 `design-library/components.css`（写注释 `/* 自动生成，禁止手改 — 运行 scripts/extract_components_css.py 重新生成 */`）
  - 验收：文件存在，内容仅为注释

- [x] **1.4.2** 创建空目录 `design-library/preview/`、`design-library/components/`、`design-library/ui_kits/`、`design-library/assets/icons/`
  - 验收：目录存在

---

## 阶段 2：第一个组件试点（button）

> **验收标准**：button 组件的 Canonical CSS 可通过标记块机制工作，AI 可以稳定生成 button。
>
> **验收方式**：在浏览器打开 `preview/component-button.html`，检查所有变体 × 状态是否正确渲染。

### 2.1 创建 button 的 preview HTML + Canonical CSS

- [x] **2.1.1** 创建 `design-library/preview/component-button.html`
  - 引用 `../tokens.css` + `../scaffold.css` + `../components.css`
  - 在 `<style>` 中用 `/* @component-css-start */` 和 `/* @component-css-end */` 包裹 button 的 Canonical CSS
  - CSS 中 **100% 使用 `var(--wg-*)` Token**，禁止硬编码
  - 覆盖全部变体：
    - emphasis: strong / medium / weak
    - scope: page / container / compact
    - state: default / hover / pressed / disabled / focus-visible
  - 页面 body 中渲染全部变体 × 状态的矩阵表格
  - 验收：浏览器打开后所有按钮正确渲染

- [x] **2.1.2** 按钮 Canonical CSS 自检清单
  - [x] CSS 中**零硬编码**颜色（无 `#xxx`、`rgb()`、`white`、`black` 等）
  - [x] CSS 中**零硬编码**尺寸（无裸 `px`/`rem`，全部用 `var(--wg-spacing-*)`）
  - [x] hover 状态有样式变化
  - [x] pressed（active）状态有样式变化
  - [x] disabled 状态有样式变化（`cursor: not-allowed` + 透明度降低）
  - [x] 验收：grep 搜索 `component-button.html`，无硬编码值

### 2.2 编写 CSS 提取脚本

- [x] **2.2.1** 创建 `scripts/extract_components_css.py`
  - 功能：扫描 `design-library/preview/component-*.html`
  - 提取每个文件的 `/* @component-css-start */` 到 `/* @component-css-end */` 之间的内容
  - 按文件名排序后聚合写入 `design-library/components.css`
  - 每个组件 CSS 块前加分隔注释：`/* ===== Button ===== */`
  - 验收：运行脚本后 `components.css` 内容正确

- [x] **2.2.2** 运行 `extract_components_css.py`，验证 `components.css` 输出正确
  - 验收：`components.css` 中 button 的 CSS 与 preview HTML 中标记块内容完全一致

---

## 阶段 3：批量 Canonicalize 所有组件

> **验收标准**：全部组件都有 Canonical CSS + preview HTML，components.css 可一次性聚合全部。
>
> **验收方式**：逐个打开 preview HTML，检查全部变体是否正确渲染。

按 registry.json 中已有组件顺序，逐一 Canonicalize：

### 第一批：action 类（2 个组件）

- [x] **3.1.1** `link` — 创建 `preview/component-link.html` + Canonical CSS
  - context: standalone / inline
  - behavior: navigation / command
  - state: default / hover / pressed / focus-visible / disabled

- [x] **3.1.2** `link` — 运行 extract 脚本，确认 components.css 更新

### 第二批：navigation 类（2 个组件）

- [x] **3.2.1** `navbar` — 创建 `preview/component-navbar.html` + Canonical CSS
  - mode: standard / title-only / search
  - leftButton: none / back / close / text
  - background: default / transparent / custom

- [x] **3.2.2** `tabs` — 创建 `preview/component-tabs.html` + Canonical CSS
  - size: standard / mini
  - layout: divide / scroll
  - state: default / pressed / focus-visible

### 第三批：feedback 类（4 个组件）

- [x] **3.3.1** `dialog` — 创建 `preview/component-dialog.html` + Canonical CSS
  - variant: text / title / status / custom
  - buttons: single / dual
  - state: open / closed

- [x] **3.3.2** `actionsheet` — 创建 `preview/component-actionsheet.html` + Canonical CSS
  - mode: action / select
  - header: none / simple / with-icon / with-link
  - itemType: single / multi

- [x] **3.3.3** `toast` — 创建 `preview/component-toast.html` + Canonical CSS
  - variant: default / action
  - action: none / weak / strong

- [x] **3.3.4** `loading` — 创建 `preview/component-loading.html` + Canonical CSS
  - variant: spinner / modal / skeleton / image
  - size: lg / sm

### 第四批：form 类（2 个组件）

- [x] **3.4.1** `input` — 创建 `preview/component-input.html` + Canonical CSS
  - layout: full / card
  - type: text / multiline / number
  - state: default / filled / focused / disabled
  - error: false / true

- [x] **3.4.2** `form` — 创建 `preview/component-form.html` + Canonical CSS
  - layout: horizontal / vertical
  - action: text / number / money / phone / select / custom
  - rightButton: none / link / button / icon-text
  - error: false / true

### 第五批：display 类（2 个组件）

- [x] **3.5.1** `tag` — 创建 `preview/component-tag.html` + Canonical CSS
  - size: 32 / 28 / 24 / 20
  - color: grey / white / green
  - icon: none / close / add / jump-to / edit
  - state: default / selected / pressed / focus-visible

- [x] **3.5.2** `cell` — 创建 `preview/component-cell.html` + Canonical CSS
  - variant: default / avatar / action
  - action: jump / text / switch / button / custom
  - divider: full / inset / none
  - state: default / pressed / disabled

### 第六批：结果页类（1 个组件）

- [x] **3.6.1** `result` — 创建 `preview/component-result.html` + Canonical CSS
  - layout: result-40 / result-60 / result-80
  - image: success / error / warning / not-found / search-not-found / no-permission / network-error 等
  - buttons: none / single / dual / with-links

### 最终提取

- [x] **3.7.0** 全部组件完成后，运行 `extract_components_css.py`，最终生成完整 `components.css`
  - 验收：`components.css` 包含全部 13 个组件的完整 CSS，无遗漏

---

## 阶段 4：组件 JSON 契约 + 注册表

> **验收标准**：每个组件有 JSON 契约文件，AI 可以通过读 JSON 知道组件支持哪些变体和 Token。
>
> **验收方式**：抽查任意组件的 JSON，检查 tokensConsumed 是否与实际 CSS 一致、variantDimensions 是否与 preview HTML 渲染的变体一致。

### 4.1 创建每个组件的 JSON 契约

- [ ] **4.1.1** 创建 `design-library/components/button.json`
- [ ] **4.1.2** 创建 `design-library/components/link.json`
- [ ] **4.1.3** 创建 `design-library/components/navbar.json`
- [ ] **4.1.4** 创建 `design-library/components/tabs.json`
- [ ] **4.1.5** 创建 `design-library/components/dialog.json`
- [ ] **4.1.6** 创建 `design-library/components/actionsheet.json`
- [ ] **4.1.7** 创建 `design-library/components/toast.json`
- [ ] **4.1.8** 创建 `design-library/components/loading.json`
- [ ] **4.1.9** 创建 `design-library/components/input.json`
- [ ] **4.1.10** 创建 `design-library/components/form.json`
- [ ] **4.1.11** 创建 `design-library/components/tag.json`
- [ ] **4.1.12** 创建 `design-library/components/cell.json`
- [ ] **4.1.13** 创建 `design-library/components/result.json`

每个 JSON 文件必须包含以下字段：
```json
{
  "schemaVersion": 2,
  "slug": "button",
  "name": "按钮",
  "category": "action",
  "variantDimensions": { ... },
  "tokensConsumed": [ ... ],
  "domAnatomy": { ... },
  "usageHints": [ ... ],
  "doNotInvent": [ ... ],
  "provenance": {
    "preview": "preview/component-button.html",
    "css": { "file": "components.css", "marker": "Button" }
  }
}
```

### 4.2 创建组件注册表

- [ ] **4.2.1** 创建 `design-library/components/index.json`
  - 列出全部组件的 slug、name、preview 路径
  - 参考格式：TRAE 的 `components/index.json`

---

## 阶段 5：消费契约（AI 使用指南）

> **验收标准**：一个新 AI session 按照 `library-consumption.json` 的读取顺序，能正确找到并使用设计库。
>
> **验收方式**：人工测试——给 AI 指令「生成一个微购登录页」，观察 AI 是否按照推荐顺序读取文件。

### 5.1 创建 library-consumption.json

- [ ] **5.1.1** 创建 `design-library/library-consumption.json`
  - 定义 `consumptionLayers`（tokens / components / icons / uikit 四层）
  - 定义每层的 `copyable` 标记和 `downstreamRule`
  - 定义 `recommendedReadOrder`（AI 读取顺序）
  - 定义 `downstreamScenarios`（三种场景：仅用 Token、生成单组件、生成整页）
  - 定义 `hardConstraints`（禁止事项）

### 5.2 更新 SKILL.md 和控制层

- [ ] **5.2.1** 在 `SKILL.md` 顶部增加「设计库路径」区块
  - 明确指出 `design-library/` 路径
  - 明确指出 AI 必须先读 `design-library/library-consumption.json`

- [ ] **5.2.2** 在 `rules/execution.md`（原 `04-ai-rules/01-ai-execution-rules.md`）中，阶段三实现阶段增加设计库消费子步骤：
  - 读取 `library-consumption.json`
  - 按 `recommendedReadOrder` 读取对应文件
  - 从 preview HTML 复制组件 markup
  - link `components.css` + `tokens.css`
  - 严禁自己手写组件 CSS

- [ ] **5.2.3** 移除旧的 `02-tokens/` 目录下的冗余 md 文件（Token 使用指南合并到 `rules/tokens.md`，架构说明不再需要）
  - 保留 `02-tokens/tokens.json` 作为 Token 定义的原始来源（供 `generate_tokens.py` 使用），其他的归档或删除
  - 保留 `02-tokens/tokens.css` 作为生成物引用

- [ ] **5.2.4** 移除旧的 `03-components/` 目录下的组件 md 文件（被 `design-library/components/*.json` + `preview/*.html` 替代）
  - 保留 `03-components/registry.json` 作为组件定义的原始来源（后续可作为 `design-library/components/index.json` 的生成来源）

---

## 阶段 6：校验闭环

> **验收标准**：所有校验脚本运行通过，设计库包体完整性自动化检查。
>
> **验收方式**：运行所有校验脚本，全部通过。

### 6.1 组件 CSS 硬编码检查

- [ ] **6.1.1** 在 `scripts/validate_components.py` 中增加检查项：
  - 扫描 `design-library/preview/component-*.html` 的 `@component-css-start` 块
  - 检查是否有裸 `#xxx`/`rgb()`/`white`/`black`/`transparent`（非 Token 引用）
  - 检查是否有裸 `px`/`rem` 值（非 `var(--wg-*)` 引用）
  - 输出违规文件和行号
  - 验收：运行脚本后定位到所有硬编码问题

### 6.2 设计库包体完整性检查

- [ ] **6.2.1** 创建 `scripts/validate_library.py`，检查项：
  - `design-library/` 下必需文件是否齐全
  - `components/index.json` 中列出的组件是否都有对应的 `.json` 和 `preview/*.html`
  - `components.css` 中是否包含所有组件的 CSS（检查分隔注释 `/* ===== xxx ===== */`）
  - 验收：运行脚本，全部通过

### 6.3 Token 一致性检查

- [ ] **6.3.1** 验证 `design-library/tokens.css` 中的 Token 定义与 `02-tokens/tokens.json` 数据源一致
  - 扩展 `scripts/validate_tokens.py`：确保 `tokens.css` 中的变量名与 `tokens.json` 中的 token 名一一对应
  - 验收：运行脚本通过

---

## 阶段 7：回归验收

> **验收标准**：AI 使用新的设计库机制后，能稳定生成符合微购规范的页面。
>
> **验收方式**：用标准 Prompt 测试 AI，检查输出质量。

### 7.1 AI 单组件生成测试

- [ ] **7.1.1** 测试 Prompt：「在微购设计系统中生成一个 strong 主按钮」
  - 预期 AI 行为：读 `library-consumption.json` → 读 `tokens.json` → 读 `components/button.json` → 读 `preview/component-button.html` → 复制 markup + link CSS
  - 验收：AI 输出中包含 `class="wg-btn wg-btn--strong wg-btn--page"` 且无硬编码样式

- [ ] **7.1.2** 测试 Prompt：「在微购设计系统中生成一个带标题和操作的 dialog」
  - 预期 AI 行为：类似上述流程，但针对 dialog 组件
  - 验收：AI 输出中包含 dialog 的 `.wg-dialog` class，结构正确

### 7.2 AI 整页生成测试

- [ ] **7.2.1** 测试 Prompt：「生成一个微购店铺设置页，包含导航栏、表单行、保存按钮」
  - 预期 AI 行为：按 `library-consumption.json` 顺序读取 → 组合 navbar + form + button 组件 → 自己写外层布局 grid
  - 验收：
    - [ ] 所有设计值使用 `var(--wg-*)`
    - [ ] 组件 class 名与 Canonical CSS 一致
    - [ ] 页面无硬编码颜色/间距
    - [ ] 交互状态完整（hover/active/disabled）

### 7.3 回归测试

- [ ] **7.3.1** 用 `tests/golden-prompts/` 中的已有黄金用例重新生成，对比新旧输出
  - 检查新输出是否有任何硬编码值
  - 检查新输出的组件 class 是否正确
  - 验收：新输出质量不低于旧输出，且无硬编码

---

## 附录 A：验收里程碑汇总

| 里程碑 | 对应阶段 | 验收方式 | 可独立验证 |
|--------|---------|---------|-----------|
| 🚩 M1 | 阶段 1（骨架） | 浏览器打开 scaffold.html，样式正常 | ✅ |
| 🚩 M2 | 阶段 2（button 试点） | 浏览器打开 component-button.html，全部变体 OK | ✅ |
| 🚩 M3 | 阶段 3（全部组件） | 逐个打开 13 个 preview HTML，全部正确 | ✅ |
| 🚩 M4 | 阶段 4（JSON 契约） | 抽查 JSON 与实际 CSS 一致性 | ✅ |
| 🚩 M5 | 阶段 5（消费契约） | 人工测试 AI 读取行为 | ✅ |
| 🚩 M6 | 阶段 6（校验闭环） | 全部脚本运行通过 | ✅ |
| 🚩 M7 | 阶段 7（回归验收） | AI 生成页面无硬编码、组件 class 正确 | ✅ |

## 附录 B：完整目录树与文件映射

```
wego-design-skill/
│
├── SKILL.md                              # 唯一运行时入口（修改：增加 design-library/ 引用）
├── README.md                             # 维护者索引（AI 不读）
│
├── rules/                                # 控制层：AI 行为规则（由旧 04-ai-rules/ 改名）
│   ├── execution.md                      # 4 阶段执行总流程 + 门禁
│   ├── generation.md                     # UI 生成规则
│   ├── components.md                     # 组件选用规则（由旧 shared-rules.md 合并）
│   ├── tokens.md                         # Token 使用规则（由旧 token-usage-guidelines.md 合并）
│   ├── forbidden.md                      # 禁止事项清单
│   ├── output.md                         # 输出格式规范
│   ├── checkout.md                       # 最终检查清单
│   └── confirmation.md                   # 需求确认规则
│
├── principles/                           # 控制层：设计原则（由旧 01-principles/ 改名）
│   └── design-principles.md              # 最高设计原则（兜底安全网，可选退役）
│
├── examples/                             # 控制层：示例参照（由旧 05-examples/ 改名）
│   ├── good-ui.md                        # 正面示例
│   ├── bad-ui.md                         # 反例示例
│   └── output.md                         # 标准输出示例
│
├── design-library/                       # 产物层：设计库包体（新建）
│   ├── tokens.css                        # Token CSS 变量（来源：由 generate_tokens.py 生成）
│   ├── tokens.json                       # Token JSON 投影（来源：由 generate_tokens.py 生成）
│   ├── scaffold.css                      # 页面骨架（手写）
│   ├── scaffold.html                     # 骨架测试页（手写）
│   ├── components.css                    # 聚合组件样式（自动生成）
│   ├── library-consumption.json          # AI 消费指令（手写）
│   ├── preview/                          # 组件预览页
│   │   ├── component-button.html         # 2.1.1
│   │   ├── component-link.html           # 3.1.1
│   │   ├── component-navbar.html         # 3.2.1
│   │   ├── component-tabs.html           # 3.2.2
│   │   ├── component-dialog.html         # 3.3.1
│   │   ├── component-actionsheet.html    # 3.3.2
│   │   ├── component-toast.html          # 3.3.3
│   │   ├── component-loading.html        # 3.3.4
│   │   ├── component-input.html          # 3.4.1
│   │   ├── component-form.html           # 3.4.2
│   │   ├── component-tag.html            # 3.5.1
│   │   ├── component-cell.html           # 3.5.2
│   │   └── component-result.html         # 3.6.1
│   ├── components/                       # 组件 JSON 契约
│   │   ├── index.json                    # 4.2.1 注册表
│   │   ├── button.json                   # 4.1.1
│   │   ├── link.json                     # 4.1.2
│   │   ├── navbar.json                   # 4.1.3
│   │   ├── tabs.json                     # 4.1.4
│   │   ├── dialog.json                   # 4.1.5
│   │   ├── actionsheet.json              # 4.1.6
│   │   ├── toast.json                    # 4.1.7
│   │   ├── loading.json                  # 4.1.8
│   │   ├── input.json                    # 4.1.9
│   │   ├── form.json                     # 4.1.10
│   │   ├── tag.json                      # 4.1.11
│   │   ├── cell.json                     # 4.1.12
│   │   └── result.json                   # 4.1.13
│   ├── ui_kits/                          # 页面级 Showcase（后续扩展）
│   │   └── shop-home/
│   │       ├── index.html
│   │       └── quality-report.json
│   └── assets/                           # 静态资源
│       ├── icons/                        # 图标 SVG
│       └── fonts/                        # 字体文件
│
├── scripts/                              # 工具层：脚本
│   ├── extract_components_css.py         # 2.2.1 新建：preview HTML → components.css
│   ├── validate_library.py               # 6.2.1 新建：包体完整性检查
│   ├── validate_components.py            # 6.1.1 修改：增加硬编码检查
│   ├── validate_tokens.py                # 6.3.1 修改：增加 design-library/ 一致性检查
│   └── generate_tokens.py                # 1.2.2 修改：增加 --output-css-json 输出 design-library/tokens.json
│
├── token-css-map.md                      # [保留] 自动生成的 Token→CSS 映射表
│
├── 02-tokens/                            # [旧目录，保留 tokens.json 作为数据源，其余归档]
│   ├── tokens.json                       # 唯一数据源（generate_tokens.py 从此读取）
│   └── tokens.css                        # 旧输出（后续 tokens.css 直接输出到 design-library/）
│
└── 03-components/                        # [旧目录，保留 registry.json 作为数据源，其余归档]
    └── registry.json                     # 原始组件注册表（后续可生成 design-library/components/index.json）
```

## 附录 C：新旧文件命名对照

| 旧路径 | 新路径 | 说明 |
|--------|--------|------|
| `01-principles/01-design-principles.md` | `principles/design-principles.md` | 去数字前缀 |
| `04-ai-rules/01-ai-execution-rules.md` | `rules/execution.md` | 去数字前缀，精简文件名 |
| `04-ai-rules/02-ui-generation-rules.md` | `rules/generation.md` | 同上 |
| `04-ai-rules/03-ui-review-rules.md` | — | 合并到 `rules/generation.md`、`rules/checkout.md` |
| `04-ai-rules/04-token-usage-rules.md` | `rules/tokens.md` | 合并了 `02-tokens/token-usage-guidelines.md` |
| `04-ai-rules/05-forbidden-rules.md` | `rules/forbidden.md` | 去数字前缀 |
| `04-ai-rules/06-output-format.md` | `rules/output.md` | 去数字前缀 |
| `04-ai-rules/07-final-checklist.md` | `rules/checkout.md` | 去数字前缀 |
| `04-ai-rules/08-requirement-confirmation-rules.md` | `rules/confirmation.md` | 去数字前缀 |
| `05-examples/01-good-ui-example.md` | `examples/good-ui.md` | 去数字前缀 |
| `05-examples/02-bad-ui-example.md` | `examples/bad-ui.md` | 去数字前缀 |
| `05-examples/03-token-usage-example.md` | — | 合并到 `rules/tokens.md` |
| `05-examples/04-ui-review-example.md` | — | 合并到 `examples/bad-ui.md` |
| `05-examples/05-output-example.md` | `examples/output.md` | 去数字前缀 |
| `02-tokens/tokens.css` | `design-library/tokens.css` | 归属产物层 |
| `02-tokens/tokens.json` | `02-tokens/tokens.json` | 保留为数据源，另生成 `design-library/tokens.json` |
| `03-components/*.md` | `design-library/components/*.json` | md 文字描述 → JSON 结构化契约 |
| `03-components/registry.json` | `design-library/components/index.json` | 旧 registry 保留为数据源，新 index.json 为产物 |

## 附录 D：关键设计决策

| 决策 | 说明 |
|------|------|
| 三层架构 | 控制层（rules/examples/principles）→ 产物层（design-library）→ 工具层（scripts），单向依赖 |
| CSS class 前缀 | 使用 `wg-` 前缀，与 Token 命名 `--wg-*` 一致 |
| 文件命名（preview） | `component-{slug}.html`，与 TRAE 一致 |
| 文件命名（去前缀） | 所有目录和文件名去掉 `01-`/`02-` 等数字前缀，文件名只留语义 |
| 标记块格式 | `/* @component-css-start */` / `/* @component-css-end */`，与 TRAE 一致 |
| Token 引用方式 | 组件 CSS 中直接使用 `var(--wg-*)`，不做别名映射 |
| 组件契约格式 | JSON（非 md），结构化 variantDimensions + tokensConsumed + doNotInvent |
| 硬编码禁止 | 不仅 CSS 禁止，HTML inline style 也禁止（用户偏好） |
| 移动端优先 | 设计基准 375px，组件 fluid 自适应，不用固定宽度 |
| 设计原则去留 | 现阶段保留为兜底安全网，当 doNotInvent + hardConstraints 覆盖 80% 场景后可删除 |

---

> **开始迭代的推荐顺序**：从阶段 1 开始 → 阶段 2 试点 → 验证机制可行 → 阶段 3 批量推进 → 阶段 4~7 顺次完成。
>
> 每完成一个 `[ ]`，改为 `[x]`，保持进度可见。
