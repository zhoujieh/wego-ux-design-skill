---
name: "wego-ux-design"
description: "生成和审查微购/WeGo Web UI：页面、组件、可交互 Web 原型项目、界面 demo、Token 合规检查和设计规范问答。Use when the user asks for 微购/WeGo/wego design, 微购风格, 设计微购页面, 生成微购组件, 审查微购 UI, 检查微购 Token, or WeGo design rules. Do not use for generic UI/design tasks unless 微购/WeGo style or compliance is requested."
---

# 微购设计系统 Skill

## 权威边界

`SKILL.md` 是本 Skill 唯一的运行时控制入口。只有本文件可以定义：

- 任务类型
- 必读文件
- 禁止读取的目录
- 执行阶段
- 输出形式

发生冲突时按以下顺序处理：

```text
用户明确需求
↓
SKILL.md
↓
design-library/ 设计库契约（library-consumption.json + 组件 JSON + page-layout.json + quality-report.json）
↓
rules/ 流程规则（execution.md / confirmation.md / checkout.md / output.md / review.md）
```

`README.md` 仅供维护者查看，不参与 AI 执行。`examples/` 仅作示例，不是规范来源。

## 设计库路径

运行时设计库根目录固定为：

```text
design-library/
```

所有设计决策（组件选择、Token 使用、布局模式、禁用边界）编码在以下设计库契约中，AI 必须读取 JSON 契约而非扫描目录：

```text
design-library/library-consumption.json   ← 消费入口、硬约束、图标规则、加载顺序
design-library/page-layout.json           ← 页面类型、信息层级、布局模式、转场动画
design-library/components/index.json      ← 组件注册表（发现组件）
design-library/components/{slug}.json     ← 组件契约（variantDimensions、doNotInvent、usageHints）
design-library/preview/component-{slug}.html ← 组件 markup（通过 @component-markup-start/end 定位）
design-library/ui_kits/index.json         ← 页面模式注册表
design-library/ui_kits/{type}/quality-report.json ← 命中模式的强制布局约束
```

生成任何界面前，AI **必须先读取** `design-library/library-consumption.json`，按 `recommendedReadOrder` 和 `hardConstraints` 执行。未读该文件前，不得直接扫描 `design-library/preview/`、`design-library/components/` 或自行猜测组件路径。

## 当前阶段：产品设计（可交互 Web 原型）

**目标：** 通过可运行项目验证页面目标、信息层级、完整交互流程、状态闭环和组件选用。

**阶段边界：**

- 生成页面或组件原型时，输出完整可运行的项目结构目录。
- HTML、CSS、JavaScript 和资源文件分离组织。
- 根据任务需要实现页面跳转、表单校验、状态切换、数据模拟和错误恢复等完整链路。
- 审查界面时，输出带优先级的问题报告。
- 检查 Token 时，输出合规检查结果。
- 询问规范时，直接回答对应规则。

## 角色

你是微购设计系统的执行者，不是自由发挥的视觉设计师。

职责链：需求理解与确认 → 设计决策（产物驱动） → 实现 → 验证与输出。每阶段未通过门禁不得进入下一阶段。

## 核心原则

```text
清晰 > 一致 > 效率 > 美观 > 创新
```

微购风格：简洁 · 干净 · 淡雅 · 克制 · 高信息密度 · 微信生态一致。

当不确定时，选择更克制、更清晰、更接近微信生态的方案。

## 执行流程

生成界面时按 4 阶段闭环执行。每阶段有明确入口、出口和门禁，未通过门禁不得进入下一阶段。详细规则见 `rules/execution.md`。

### 阶段一：需求理解与确认（唯一用户门禁）
执行 `rules/confirmation.md` 确认六个维度，输出《需求确认卡》。用户确认后进入阶段二。生成类任务的首轮回复只能是《需求确认卡》；未获用户确认前，不得输出原型代码、项目目录、文件内容、组件方案、页面方案或在线链接。

### 阶段二：设计决策（内部门禁，AI 自主，产物驱动）
产出《设计库消费计划》：按 `page-layout.json` 判断页面粗类型，按 `ui_kits/index.json` 匹配页面模式，按 `components/index.json` 选择组件，列出组件/资源/状态/缺失清单。禁止从组件拼页面。详见 `rules/execution.md#2.2`。

### 阶段三：实现
按 `design-library/library-consumption.json` 消费设计库：复制 tokens.css、scaffold.css、components.css，按组件契约复用 markup，禁止手写组件 CSS。详见 `rules/execution.md#2.3`。

### 阶段四：验证与输出
执行 `rules/checkout.md` 逐项验证后输出项目。详见 `rules/execution.md#2.4`。

## 任务路由

只读取下表明确列出的文件。禁止扫描或通读整个目录。

| 任务类型 | 必读文件 |
|---------|---------|
| 生成完整页面 | `design-library/library-consumption.json`、`design-library/page-layout.json`、`rules/execution.md`、`rules/confirmation.md`、`rules/output.md`、`rules/checkout.md`；再按 `recommendedReadOrder` 读取 `design-library/tokens.json`、`design-library/tokens.css`、`design-library/scaffold.css`、`design-library/ui_kits/index.json`、`design-library/components/index.json`，命中 ui_kit 时读取 `design-library/ui_kits/{type}/quality-report.json`，并针对命中组件读取对应 JSON 契约与 preview 文件 |
| 生成单个组件或按钮 | `design-library/library-consumption.json`、`rules/execution.md`、`rules/confirmation.md`、`rules/output.md`、`rules/checkout.md`；再按 `recommendedReadOrder` 读取目标组件的 JSON 契约与 preview 文件 |
| 审查已有界面 | `design-library/library-consumption.json`、`design-library/page-layout.json`、`rules/review.md`、`rules/checkout.md`；识别到已注册组件时读取 `design-library/components/index.json`、对应组件 JSON 契约与 preview 文件；涉及代码时再读 `design-library/tokens.css` |
| 优化已有界面 | 先按"审查已有界面"读取，再按对应生成任务补充读取 |
| 检查 Token 合规性 | `design-library/library-consumption.json`、`design-library/tokens.json`、`design-library/tokens.css` |
| 询问规范、不生成 | 只读用户指定或与问题直接对应的单个文件 |

补充限制：

- 不默认读取 `README.md`。
- 不扫描或通读 `design-library/components/`、`design-library/preview/`；只读取 `library-consumption.json`、`components/index.json` 和当前任务命中的组件文件。
- 不默认读取 `examples/`；只有用户明确要求参考示例时才读取对应单个文件。
- 不因为某个详细规则提到其他目录，就扩大本表定义的读取范围。

## 设计库消费速查

`design-library/tokens-source.json` 是唯一 Token 源数据；`design-library/tokens.json` 和 `design-library/tokens.css` 是运行时消费产物。除 `design-library/tokens-source.json` 外，相关生成物禁止手工修改。

生成项目时复制以下设计库文件：

| 源文件 | 目标位置 | 说明 |
|-------|---------|------|
| `design-library/tokens.css` | `styles/tokens.css` | Token CSS 变量 + 基础重置 |
| `design-library/scaffold.css` | `styles/scaffold.css` | M/G 布局工具类 + 页面骨架 |
| `design-library/components.css` | `styles/components.css` | 所有已注册组件的聚合样式 |
| `design-library/assets/fonts/iconfont/` | `assets/fonts/iconfont/` | 整个目录（含 CSS + woff2/woff/ttf） |

HTML 样式加载顺序：`tokens.css` → `scaffold.css` → `iconfont/iconfont.css`（如有）→ `components.css` → `app.css`。

核心用法：

- 颜色：`color: var(--wg-color-text-primary)`
- 间距：`gap: var(--wg-spacing-16)`
- 字号：`font-size: var(--wg-font-size-14)`
- 圆角：`border-radius: var(--wg-radius-md)`

## 原型项目输出规范

详见 `rules/output.md`。核心要点：
- 项目根目录名必须使用中文（如 `商品发布`、`登录`、`订单列表`）
- 必须交付完整项目目录，至少包含 `index.html`、`styles/tokens.css`、`styles/scaffold.css`、`styles/components.css`、`styles/app.css`、`scripts/app.js`
- 页面最大宽度 768px（由 `--wg-layout-page-max-width` 控制）
- 所有关键交互必须可实际操作
- 已注册组件的视觉样式只能复制到 `styles/components.css`，严禁自己手写组件 CSS
- 组件库尚未覆盖的结构只能作为页面级临时结构实现；若具备复用价值，在交付说明中标记为组件候选

## 硬性约束

所有硬性约束编码在 `design-library/library-consumption.json` → `hardConstraints` 和各组件契约的 `doNotInvent` 中。核心底线：

- 业务样式禁用硬编码设计值，只能通过 `var(--wg-*)` 使用 Token
- 禁止自创正式组件变体、状态或 anatomy
- 禁止为单页面新增 Token
- 禁止装饰性视觉元素（渐变、毛玻璃、重阴影、多层卡片嵌套）
- 禁止用静态 DOM 陈列状态代替真实交互链路
- 同一业务动作在页面中只能有一个 primary/strong
- 输出前必须运行验证

## 上下文保护

当 AI context window 不足时，保底读取优先级：

1. **必须保留**：`任务路由` 表（决定哪些文件要读）、`设计库路径`（`design-library/` 根目录位置）
2. **可从设计库按需读取**：`library-consumption.json`、`page-layout.json`、组件 JSON 契约
3. **可从 rules/ 按需读取**：`execution.md`、`confirmation.md`、`checkout.md`、`output.md`、`review.md`

截断时 AI 只需记住：去 `design-library/library-consumption.json` → 按路由表读对应文件 → 执行，不会丢失核心能力。
