---
name: wego-ux-design
description: 微购(WeGo)设计系统 — 生成符合微购规范的完整可交互 Web 原型项目，并支持界面审查、Token 合规检查和规范问答。当用户需要设计微购/wego/WeGo 页面、生成可交互 UI 原型、做界面 demo、审查设计合规性、检查 Token、或询问微购设计规范时自动触发。触发词包括但不限于："设计一个页面""做个原型""生成一个按钮""帮我看看这个UI""设计一个微购的XX页""生成微购风格""WeGo design""wego页面""微购组件"。覆盖设计原则、Token 体系、布局模式、组件契约、交互实现、UI 生成与审查。支持安装到 Codex / Claude Code / Trae，详见 install.sh。

# 微购设计系统 Skill

## 权威边界

`SKILL.md` 是本 Skill 唯一的运行时控制入口。只有本文件可以定义：

- 任务类型
- 必读文件
- 禁止读取的目录
- 执行阶段
- 输出形式

其他 Markdown 文件只提供被选中任务的详细规则，不得自行增加必读文件、改变输出形式或覆盖本文件的阶段边界。

发生冲突时按以下顺序处理：

```text
用户明确需求
↓
SKILL.md
↓
本文件为当前任务指定的详细规则
```

`README.md` 仅供维护者查看，不参与 AI 执行。`examples/` 仅作示例，不是规范来源。

## 设计库路径

运行时设计库根目录固定为：

```text
design-library/
```

生成页面、单组件、组件组合或设计库消费相关任务时，AI **必须先读取**：

```text
design-library/library-consumption.json
```

之后再按其中的 `recommendedReadOrder` 决定继续读取哪些文件。未读取该文件前，不得直接扫描 `design-library/preview/`、`design-library/components/` 或自行猜测组件路径。

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
执行 `rules/confirmation.md` 确认六个维度，输出《需求确认卡》。用户确认后进入阶段二。详见 `rules/execution.md#2.1`。

### 阶段二：设计决策（内部门禁，AI 自主，产物驱动）
10 步依赖链，产物驱动，禁止从组件拼页面。详见 `rules/execution.md#2.2`。

### 阶段三：实现
按 `design-library/library-consumption.json` 消费设计库，禁止手写组件 CSS。详见 `rules/execution.md#2.3`。

### 阶段四：验证与输出
执行 `rules/checkout.md` 逐项验证后输出项目。详见 `rules/execution.md#2.4`。
## 任务路由

只读取下表明确列出的文件。禁止扫描或通读整个目录。

| 任务类型 | 必读文件 |
|---------|---------|
| 生成完整页面 | `design-library/library-consumption.json`、`principles/design-principles.md`、`rules/execution.md`、`rules/generation.md`、`rules/tokens.md`、`rules/components.md`、`rules/output.md`、`rules/checkout.md`、`rules/icon-guidelines.md`、`design-library/tokens.css`；再按 `recommendedReadOrder` 读取 `design-library/tokens.json`、`design-library/tokens.css`、`design-library/scaffold.css`、`design-library/components/index.json`，并针对命中组件读取对应 JSON 契约与 preview 文件 |
| 生成单个组件或按钮 | `design-library/library-consumption.json`、`rules/execution.md`、`rules/generation.md`、`rules/tokens.md`、`rules/components.md`、`rules/output.md`、`rules/checkout.md`、`rules/icon-guidelines.md`、`design-library/tokens.css`；再按 `recommendedReadOrder` 读取目标组件的 JSON 契约与 preview 文件 |
| 审查已有界面 | `design-library/library-consumption.json`、`principles/design-principles.md`、`rules/tokens.md`、`rules/components.md`、`rules/review.md`、`rules/checkout.md`；识别到已注册组件时读取 `design-library/components/index.json`、对应组件 JSON 契约与 preview 文件；涉及代码时再读 `design-library/tokens.css` |
| 优化已有界面 | 先按“审查已有界面”读取，再按对应生成任务补充读取 |
| 检查 Token 合规性 | `design-library/library-consumption.json`、`rules/tokens.md`、`design-library/tokens.json`、`design-library/tokens.css`、`design-library/tokens.css` |
| 询问规范、不生成 | 只读用户指定或与问题直接对应的单个规则文件 |

补充限制：

- 不默认读取 `README.md`。
- 不扫描或通读 `design-library/components/`、`design-library/preview/`；只读取 `library-consumption.json`、`components/index.json` 和当前任务命中的组件文件。
- 不默认读取 `examples/`；只有用户明确要求参考示例时才读取对应单个文件。
- 不因为某个详细规则提到其他目录，就扩大本表定义的读取范围。

## Token → CSS 映射

`design-library/tokens-source.json` 是唯一 Token 源数据；`design-library/tokens.json` 和 `design-library/tokens.css` 是运行时消费产物；`design-library/tokens.css` 是查阅映射。除 `design-library/tokens-source.json` 外，相关生成物禁止手工修改。

所有设计值通过 CSS 自定义属性使用，完整映射表见 **`design-library/tokens.css`**。

生成项目时：

- 将 `design-library/tokens.css` 复制为项目内的 `styles/tokens.css`。
- 将 `design-library/assets/fonts/iconfont/` 整个目录复制到 `assets/fonts/iconfont/`，保持 `iconfont.css` 与字体文件（woff2 / woff / ttf）在同一目录下。不得将 `iconfont.css` 单独复制到 `assets/fonts/` 根目录。
- 将 `design-library/components.css` 复制为项目内的 `styles/components.css`。
- 在 HTML 中按以下顺序引入样式：`tokens.css` → `iconfont/iconfont.css`（如有）→ `components.css` → `app.css`。`iconfont.css` 的引入路径必须与实际目录结构一致。
- Token 定义层允许保存 HEX、RGBA、px 等原始值；业务 CSS 只能通过 `var(--wg-*)` 使用设计值。

核心用法：

- 颜色：`color: var(--wg-color-text-primary)`
- 间距：`gap: var(--wg-spacing-16)`
- 字号：`font-size: var(--wg-font-size-14)`
- 圆角：`border-radius: var(--wg-radius-md)`

## 原型项目输出规范

详见 `rules/output.md#2`。核心要点：
- 项目根目录名必须使用中文（如 `商品发布`、`登录`、`订单列表`）
- 必须交付完整项目目录，至少包含 `index.html`、`styles/tokens.css`、`styles/components.css`、`styles/app.css`、`scripts/app.js`
- 页面最大宽度 768px（由 `--wg-layout-page-max-width` 控制），同时保持移动端响应式适配
- 输出完整项目目录，不合并为单文件
- 所有关键交互必须可实际操作
- 已注册组件的视觉样式只能复制到 `styles/components.css`，严禁自己手写组件 CSS；页面级业务样式只写入 `styles/app.css`
- 组件库尚未覆盖的结构只能作为页面级临时结构实现；若具备复用价值，在交付说明中标记为组件候选，不得声明为正式组件规则

## 扩展与约束

**组件完善期处理**：未注册组件的临时实现规则详见 `rules/execution.md#4.6`。

**缺失处理**：Token 或组件不够用时，不写硬编码值、不修改正式契约，按 `rules/execution.md#5` 标注缺失。

**硬性禁令**：详见 `rules/forbidden.md`。核心底线：
- 业务样式禁用硬编码设计值
- 禁止自创正式组件变体
- 禁止为单页面新增 Token
- 禁止装饰性视觉元素
- 禁止牺牲交互闭环
- 输出前必须运行验证
- 禁止输出空泛建议

## 上下文保护

当 AI context window 不足时，本文件的保底读取优先级：

1. **必须保留**：`任务路由` 表（决定哪些规则文件要读）、`设计库路径`（`design-library/` 根目录位置）
2. **可从 rules/ 按需读取**：执行流程细节、Token→CSS 映射详情、原型项目输出规范
3. **其他 rules/ 文件本身即按需读取**：`execution.md`、`generation.md`、`tokens.md`、`components.md`、`checkout.md` 等

截断时 AI 只需记住：去 `design-library/library-consumption.json` → 按路由表读对应规则文件 → 执行，不会丢失核心能力。

