# Input

Input 用于表单中的文本输入。本规则首先判断输入框的布局模式（通栏/卡片），再选择输入类型（单行/多行/数字），最后确定状态和交互行为。

## 目录

- [使用决策](#使用决策)
- [语义模型](#语义模型)
- [允许组合](#允许组合)
- [Anatomy](#anatomy)
- [文案规则](#文案规则)
- [Canonical HTML](#canonical-html)
- [Canonical CSS](#canonical-css)
- [状态](#状态)
- [可访问性](#可访问性)
- [生成约束](#生成约束)
- [自检](#自检)
- [规范来源](#规范来源)

## 使用决策

使用 Input：

- 需要用户输入文本、数字或短文本内容。
- 表单中的姓名、手机号、金额、描述等字段。
- 搜索框内的文本输入（页面级搜索使用 NavBar 搜索模式，不使用本组件）。
- 需要输入校验和错误提示的场景。

不使用 Input：

- 长文本编辑（超过 5 行）：使用 TextArea 或富文本编辑器。
- 选择类操作（日期、时间、地址等）：使用对应的 Picker 组件。
- 只读展示：使用 Text 组件，不使用 Input。
- 页面顶部搜索入口：使用 NavBar 的 search 模式。

## 语义模型

Input 有四个决策维度：

```text
layout      布局模式（通栏/卡片）
type        输入类型（单行/多行/数字）
state       当前交互状态
error       是否处于错误状态
```

### Layout

| Layout | 应用场景 | 视觉规则 |
|---|---|---|
| `full` | 通栏输入框，占满容器宽度 | 无边框，左右无内边距，宽度 100% |
| `card` | 卡片内输入框，有明确边界 | 有背景色 + 细边框 + 圆角，左右有内边距 |

布局选择规则：

- 表单页面（登录、注册、设置等）通常使用 `full` 通栏模式，输入框占满容器宽度。
- 卡片、弹窗、局部模块内的输入使用 `card` 卡片模式，有明确的视觉边界。
- 禁止让 AI 直接根据"有没有边框"选择布局。必须先判断输入框所在的容器类型。

### Type

| Type | 含义 | 结构 | 应用场景 |
|---|---|---|---|
| `text` | 单行文本输入 | 单行输入框 + 可选 placeholder | 姓名、手机号、标题等短文本 |
| `multiline` | 多行文本输入 | 多行输入框（TextArea）+ 可选 placeholder | 描述、备注、地址等长文本 |
| `number` | 数字输入 | 单行输入框 + 数字过滤 + 可选单位 | 金额、数量、年龄等数值 |

类型选择规则：

- 默认使用 `text` 单行输入。
- 需要输入多行内容时使用 `multiline`。
- 只允许输入数字时使用 `number`，自动过滤非数字字符。
- `number` 类型支持最大值限制，超出时自动截断并报错。

### State

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 正常可用，显示 placeholder |
| `filled` | 有值状态 | 显示用户输入内容，隐藏 placeholder |
| `focused` | `:focus` | 显示焦点描边，光标闪烁 |
| `disabled` | `disabled` | 禁用状态，不可编辑，使用禁用色 |

### Error

| Error | 含义 | 视觉规则 |
|---|---|---|
| `false` | 正常状态 | 默认边框和背景 |
| `true` | 错误状态 | 红色边框 + 浅红背景 + 错误提示文字 |

错误状态规则：

- 输入校验失败时（如格式错误、超出最大值）进入错误状态。
- 错误状态下，输入框边框变为红色（`wg.color.status.danger.border`），背景变为浅红色（`wg.color.status.danger.bg`）。
- 错误提示文字显示在输入框下方，使用红色（`wg.color.status.danger.text`），字号 12px。
- 用户重新输入或聚焦时，自动清除错误状态（除非显式禁用此行为）。

## 允许组合

| Layout | Type | 错误状态 | 单位文本 |
|---|---|---|---|
| `full` | `text` / `multiline` / `number` | 允许 | 仅 `number` 允许 |
| `card` | `text` / `multiline` / `number` | 允许 | 仅 `number` 允许 |

附加规则：

- `number` 类型支持右侧单位文本（如"元""kg"），其他类型不支持。
- `multiline` 类型默认高度 58px，可通过自定义高度覆盖。
- `text` 和 `number` 类型默认高度 36px（卡片模式）或 44px（通栏模式）。
- 同一输入框不得同时显示单位文本和右侧图标（如清除按钮）。
- 错误提示文字不得超过 20 个字符，单行展示，超出截断。

## Anatomy

通栏单行输入框：

```text
div.wg-input.wg-input--full.wg-input--text
├── input.wg-input__field[placeholder="请输入"]
└── p.wg-input__error（错误状态时）
```

卡片单行输入框：

```text
div.wg-input.wg-input--card.wg-input--text
├── div.wg-input__container
│   └── input.wg-input__field[placeholder="请输入"]
└── p.wg-input__error（错误状态时）
```

卡片多行输入框：

```text
div.wg-input.wg-input--card.wg-input--multiline
├── div.wg-input__container
│   └── textarea.wg-input__field[placeholder="请输入"]
└── p.wg-input__error（错误状态时）
```

卡片数字输入框（带单位）：

```text
div.wg-input.wg-input--card.wg-input--number
├── div.wg-input__container
│   ├── input.wg-input__field[placeholder="0"]
│   └── span.wg-input__unit（单位文本）
└── p.wg-input__error（错误状态时）
```

V1 不支持前缀图标、后缀图标、清除按钮。不得自行加入图标或额外元素。

## 文案规则

- placeholder 使用简短提示，如"请输入姓名""请输入金额""请输入描述"。
- placeholder 单行展示，不换行。
- 错误提示使用明确的问题描述，如"格式不正确""不能超过 20 字""金额不能超过 100"。
- 错误提示单行展示，不换行，超长时截断显示省略号。
- 单位文本使用简短名词，如"元""kg""件"，不得超过 2 个字符。
- 同一表单内的 placeholder 使用一致的语法结构。

## Canonical HTML

通栏单行输入框（正常状态）：

```html
<div class="wg-input wg-input--full wg-input--text">
  <input class="wg-input__field" type="text" placeholder="请输入姓名" />
</div>
```

通栏单行输入框（错误状态）：

```html
<div class="wg-input wg-input--full wg-input--text wg-input--error">
  <input class="wg-input__field" type="text" value="123" placeholder="请输入姓名" />
  <p class="wg-input__error">格式不正确</p>
</div>
```

卡片单行输入框（正常状态）：

```html
<div class="wg-input wg-input--card wg-input--text">
  <div class="wg-input__container">
    <input class="wg-input__field" type="text" placeholder="请输入手机号" />
  </div>
</div>
```

卡片多行输入框：

```html
<div class="wg-input wg-input--card wg-input--multiline">
  <div class="wg-input__container">
    <textarea class="wg-input__field" placeholder="请输入描述" rows="3"></textarea>
  </div>
</div>
```

卡片数字输入框（带单位）：

```html
<div class="wg-input wg-input--card wg-input--number">
  <div class="wg-input__container">
    <input class="wg-input__field" type="text" inputmode="numeric" placeholder="0" />
    <span class="wg-input__unit">元</span>
  </div>
</div>
```

卡片数字输入框（错误状态，超出最大值）：

```html
<div class="wg-input wg-input--card wg-input--number wg-input--error">
  <div class="wg-input__container">
    <input class="wg-input__field" type="text" inputmode="numeric" value="150" placeholder="0" />
    <span class="wg-input__unit">元</span>
  </div>
  <p class="wg-input__error">金额不能超过 100</p>
</div>
```

禁用状态：

```html
<div class="wg-input wg-input--card wg-input--text wg-input--disabled">
  <div class="wg-input__container">
    <input class="wg-input__field" type="text" value="只读内容" disabled />
  </div>
</div>
```

## Canonical CSS

```css
/* ── 基础容器 ── */
.wg-input {
  display: flex;
  flex-direction: column;
  inline-size: 100%;
}

/* ── 布局模式 ── */
.wg-input--full {
  /* 通栏模式：无边框，无内边距 */
}

.wg-input--card {
  /* 卡片模式：有背景、边框、圆角 */
}

/* ── 输入容器（卡片模式） ── */
.wg-input__container {
  display: flex;
  align-items: center;
  block-size: var(--wg-size-36);
  padding-inline: var(--wg-spacing-12);
  background-color: var(--wg-color-bg-surface);
  border: var(--wg-stroke-width-default) var(--wg-stroke-style-solid) var(--wg-color-border-default);
  border-radius: var(--wg-radius-sm);
  transition:
    border-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard),
    background-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-input--full .wg-input__field {
  block-size: var(--wg-touch-default);
  padding-inline: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
}

/* ── 输入框 ── */
.wg-input__field {
  appearance: none;
  flex: 1 1 0;
  min-inline-size: 0;
  block-size: 100%;
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  font-family: var(--wg-font-family-text);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-primary);
  outline: none;
}

.wg-input__field::placeholder {
  color: var(--wg-color-text-placeholder);
}

/* ── 多行输入框 ── */
.wg-input--multiline .wg-input__container {
  block-size: auto;
  min-block-size: var(--wg-size-56);
  align-items: flex-start;
  padding-block: var(--wg-spacing-8);
}

.wg-input--multiline .wg-input__field {
  resize: none;
  block-size: auto;
  min-block-size: var(--wg-size-40);
}

/* ── 数字输入框 ── */
.wg-input--number .wg-input__field {
  text-align: center;
  font-weight: var(--wg-font-weight-medium);
}

.wg-input__unit {
  flex: 0 0 auto;
  margin-inline-start: var(--wg-spacing-8);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-secondary);
  white-space: nowrap;
}

/* ── 焦点状态 ── */
.wg-input--card .wg-input__container:focus-within {
  border-color: var(--wg-color-border-focus);
}

.wg-input--full .wg-input__field:focus {
  border-block-end: var(--wg-stroke-width-default) var(--wg-stroke-style-solid) var(--wg-color-border-focus);
}

/* ── 错误状态 ── */
.wg-input--error .wg-input__container {
  background-color: var(--wg-color-status-danger-bg);
  border-color: var(--wg-color-status-danger-border);
}

.wg-input--error .wg-input__field {
  color: var(--wg-color-text-primary);
}

.wg-input__error {
  margin-block-start: var(--wg-spacing-4);
  font-size: var(--wg-font-size-12);
  line-height: var(--wg-font-lineheight-12);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-status-danger-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 100%;
}

/* ── 禁用状态 ── */
.wg-input--disabled .wg-input__container {
  background-color: var(--wg-color-state-disabled-bg);
  border-color: var(--wg-color-border-subtle);
  cursor: not-allowed;
}

.wg-input--disabled .wg-input__field {
  color: var(--wg-color-text-disabled);
  cursor: not-allowed;
}

.wg-input--disabled .wg-input__unit {
  color: var(--wg-color-text-disabled);
}
```

通栏模式输入框高度使用 `wg.touch.default`（44px），卡片模式使用 `wg.size.36`（36px）。多行输入框默认高度使用 `wg.size.56`（56px），可通过自定义高度覆盖。

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 正常可用，显示 placeholder |
| `filled` | 有值状态 | 显示用户输入内容，隐藏 placeholder |
| `focused` | `:focus-within` | 显示焦点描边（品牌色边框） |
| `disabled` | `disabled` + `.wg-input--disabled` | 禁用背景 + 禁用文字色，不可编辑 |
| `error` | `.wg-input--error` | 红色边框 + 浅红背景 + 错误提示文字 |

V1 未定义 `loading`、`success` 视觉变体。遇到这些需求不得自行向 Input 加入 Spinner、图标或颜色；通过页面级反馈区域实现业务状态，并标注组件能力缺失。

## 可访问性

- 必须使用原生 `<input>` 或 `<textarea>`。
- 禁用状态必须使用 `disabled` 属性，不能只降低透明度。
- 数字输入框必须使用 `inputmode="numeric"` 以唤起数字键盘。
- 多行输入框必须使用 `<textarea>`，不得使用 `<input>`。
- 错误提示必须使用 `<p>` 标签，并通过 `aria-describedby` 关联到输入框（可选）。
- 焦点顺序必须与视觉顺序一致。
- 禁止使用 `div`、`span` 模拟可输入框。

## 生成约束

- 必须同时声明一个 `layout` class（`wg-input--full` 或 `wg-input--card`）和一个 `type` class（`wg-input--text` / `wg-input--multiline` / `wg-input--number`）。
- 必须使用 `wg-input__container`（卡片模式）或 `wg-input__field`（通栏模式）。
- 不得覆盖输入框高度、字号、颜色、边框和圆角。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 数字输入框的单位文本必须使用 `wg-input__unit`，不得自定义。
- 错误提示必须使用 `wg-input__error`，不得自定义样式。
- 页面布局只控制 Input 的位置和宽度，不控制 Input 内部样式。
- 完整页面中出现 Input 时，必须读取并遵守本文件。
- Canonical CSS 必须从本文件 `## Canonical CSS` 区块逐字复制到 `styles/components.css`，不得增删规则、修改选择器或添加属性。组件视觉行为只能通过规范中已声明的修饰符 class 调整。

## 自检

```text
□ 是否先判断 full / card 布局模式
□ 是否选择了正确的输入类型（text / multiline / number）
□ 是否遵守了错误状态的视觉规则（红色边框 + 浅红背景 + 错误提示）
□ 数字输入框是否使用了 inputmode="numeric"
□ 多行输入是否使用了 textarea
□ 是否使用了规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 是否使用原生 input 或 textarea
□ disabled 是否使用原生属性
□ 是否没有自创 loading、success、icon 变体
□ 错误提示是否不超过 20 个字符
□ 单位文本是否不超过 2 个字符
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `4:221`。提取通栏和卡片两种布局模式的结构、尺寸、间距和颜色。
- Kuikly `InputSimple`：参考高度预设（H_32 / H_36 / MULTI_LINE）、输入过滤规则、焦点/失焦行为；不继承 Kuikly DSL、InputPreset 枚举、自定义过滤规则函数。
- Kuikly `InputText`：参考错误状态行为（自动清错、外部控制报错）、单行/多行切换、响应式文本注入；不继承 Kuikly DSL、observableText 响应式属性、preventDefaultErrorBehavior 配置。
- Kuikly `InputNumber`：参考数字过滤、最大值限制、单位文本、居中加粗样式；不继承 Kuikly DSL、maxNumber 自动校验、errorGuard 机制、customFilter 自定义过滤。
