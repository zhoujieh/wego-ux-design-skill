# Tag

Tag 用于标记、分类和筛选。本规则首先判断标签在页面中的用途和交互需求，再映射尺寸与视觉样式。

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

使用 Tag：

- 标签作为主要任务，如为客户添加和移除身份标签、选择各类信息。
- 筛选、历史记录等可点击标签，如搜索推荐项、快捷筛选。
- 商品标签等可能集中出现的、次要信息的可点击标签，如商品信息流、商品详情页标签。
- 在列表内纯展示的不可点击标签，如客户标签、开单页余额标签。

不使用 Tag：

- 页面级主要操作：使用 Button。
- 页面间导航切换：使用 Tabs。
- 列表中的跳转入口：使用 Cell。
- 弹出操作菜单：使用 ActionSheet。

Tag 与 Button 的区别：

- Tag 用于标记、分类和筛选，视觉上弱于 Button，不承载页面级主要操作。
- Button 用于触发明确操作，视觉强调度高，承载页面级主要操作。

## 语义模型

Tag 有四个决策维度：

```text
size     标签尺寸，决定高度、交互能力和图标支持
color    颜色预设方案，决定背景、文字和边框
icon     图标配置，决定图标类型和位置
state    当前交互状态
```

### Size

| Size | 应用场景 | 视觉高度 | 可选中 | 可点击 | 支持图标 | 圆角 |
|---|---|---|---|---|---|---|
| `32` | 标签作为主要任务，支持移除、选中 | `wg.size.32` | 是 | 是 | 是 | `wg.radius.full` |
| `28` | 筛选、历史记录等可点击标签，支持移除、选中、点击跳转 | `wg.size.28` | 是 | 是 | 是 | `wg.radius.full` |
| `24` | 商品标签等次要信息的可点击标签，不支持选中 | `wg.size.24` | 否 | 是 | 否 | `wg.radius.full` |
| `20` | 列表内纯展示标签，不可点击、不可选中 | `wg.size.20` | 否 | 否 | 否 | `wg.radius.sm` |

禁止让 AI 直接根据"大、中、小"选择尺寸。必须先判断标签用途和交互需求：

```text
标签是否需要选中态？
├─ 是 → 是否作为主要任务？
│    ├─ 是 → size=32
│    └─ 否 → size=28
└─ 否 → 是否需要点击？
    ├─ 是 → size=24
    └─ 否 → size=20（纯展示）
```

### Color

| Color | 默认背景 | 选中背景 | 默认文字 | 选中文字 | 边框 |
|---|---|---|---|---|---|
| `grey` | `wg.color.bg.subtle` | `wg.color.bg.success` | `wg.color.text.primary` | `wg.color.text.success` | 无 |
| `white` | `wg.color.bg.surface` | `wg.color.bg.success` | `wg.color.text.primary` | `wg.color.text.success` | `wg.color.border.default` |
| `green` | `wg.color.bg.surface` | `wg.color.bg.success` | `wg.color.text.success` | `wg.color.text.success` | `wg.color.border.success` |

Color 选择规则：

- 默认使用 `grey`，灰底标签适用于大多数场景。
- 需要白底带边框的标签使用 `white`，常用于白底页面中需要与背景区分的标签。
- 需要绿色文字和绿色边框的标签使用 `green`，用于强调品牌色或成功状态。

### Icon

| Icon | 图标 | 位置 | 默认颜色 | 说明 |
|---|---|---|---|---|
| `none` | 无 | — | — | 无图标 |
| `close` | `icon-cha16` | 右侧 | `wg.color.text.tertiary` | 关闭，支持图标独立点击 |
| `add` | `icon-jia16` | 左侧 | `wg.color.text.primary` | 添加，用作"新建"标签 |
| `jump-to` | `icon-youjiantou16` | 右侧 | `wg.color.text.tertiary` | 跳转，支持点击跳转 |
| `edit` | `icon-bianji16` | 左侧 | `wg.color.text.primary` | 编辑 |

Icon 选择规则：

- 只有 `size=32` 和 `size=28` 支持图标。
- 用作"新建"标签时使用 `add`，图标在左侧。
- 需要移除标签时使用 `close`，图标在右侧，支持图标独立点击。
- 需要点击跳转时使用 `jump-to`，图标在右侧。
- 需要编辑时使用 `edit`，图标在左侧。
- 不需要图标时使用 `none`。

## 允许组合

| Size | Color | Icon | 可选中 | 说明 |
|---|---|---|---|---|
| `32` | `grey` / `white` / `green` | `none` / `close` / `add` / `jump-to` / `edit` | 是 | 标签作为主要任务 |
| `28` | `grey` / `white` / `green` | `none` / `close` / `add` / `jump-to` / `edit` | 是 | 筛选、历史记录等可点击标签 |
| `24` | `grey` / `white` / `green` | `none` | 否 | 次要信息的可点击标签 |
| `20` | `grey` / `green` | `none` | 否 | 纯展示标签 |

附加规则：

- `size=24` 和 `size=20` 不得使用图标。
- `size=24` 不可选中，但可点击。
- `size=20` 不可选中、不可点击，仅作信息展示。
- `size=20` 文字颜色固定为灰色（`wg.color.text.tertiary`），但 `color=green` 时文字为绿色（`wg.color.text.success`）。
- `close` 图标支持独立点击事件，不会触发标签本体的点击事件。
- 同一标签组内所有标签的 `size` 和 `color` 必须一致。

## Anatomy

基础标签（无图标）：

```text
span.wg-tag.wg-tag--{size}.wg-tag--{color}
└── span.wg-tag__text
```

左侧图标标签：

```text
span.wg-tag.wg-tag--{size}.wg-tag--{color}.wg-tag--icon-left
├── i.wg-tag__icon.wego-iconfont-s.icon-{font_class}
└── span.wg-tag__text
```

右侧图标标签：

```text
span.wg-tag.wg-tag--{size}.wg-tag--{color}.wg-tag--icon-right
├── span.wg-tag__text
└── i.wg-tag__icon.wego-iconfont-s.icon-{font_class}
```

选中态：

```text
span.wg-tag.wg-tag--{size}.wg-tag--{color}.wg-tag--selected
└── ...
```

V1 仅允许上述 Anatomy 中的元素。不得自行加入徽章、副标题、自定义内容插槽；这些作为 V1 能力缺失标注。

## 文案规则

- 使用简短名词或名词短语，如"标签""新增""已完成"。
- 单行展示，不换行，超长时截断显示省略号。
- 同一标签组内文案使用一致的语法结构。
- 标签文本最大宽度受限时自动省略。

## Canonical HTML

基础标签（灰底，可选中）：

```html
<span class="wg-tag wg-tag--32 wg-tag--grey" role="button" tabindex="0" aria-pressed="false">
  <span class="wg-tag__text">标签</span>
</span>
```

选中态标签：

```html
<span class="wg-tag wg-tag--32 wg-tag--grey wg-tag--selected" role="button" tabindex="0" aria-pressed="true">
  <span class="wg-tag__text">标签</span>
</span>
```

左侧添加图标标签：

```html
<span class="wg-tag wg-tag--32 wg-tag--grey wg-tag--icon-left" role="button" tabindex="0" aria-pressed="false">
  <i class="wg-tag__icon wego-iconfont-s icon-jia16"></i>
  <span class="wg-tag__text">添加标签</span>
</span>
```

右侧关闭图标标签：

```html
<span class="wg-tag wg-tag--32 wg-tag--grey wg-tag--icon-right" role="button" tabindex="0" aria-pressed="false">
  <span class="wg-tag__text">可关闭</span>
  <i class="wg-tag__icon wego-iconfont-s icon-cha16" role="button" tabindex="0" aria-label="移除"></i>
</span>
```

白底带边框标签：

```html
<span class="wg-tag wg-tag--28 wg-tag--white" role="button" tabindex="0" aria-pressed="false">
  <span class="wg-tag__text">White</span>
</span>
```

绿色标签：

```html
<span class="wg-tag wg-tag--28 wg-tag--green" role="button" tabindex="0" aria-pressed="false">
  <span class="wg-tag__text">Green</span>
</span>
```

小尺寸可点击标签（不可选中）：

```html
<span class="wg-tag wg-tag--24 wg-tag--grey" role="button" tabindex="0">
  <span class="wg-tag__text">小标签</span>
</span>
```

纯展示标签（不可点击）：

```html
<span class="wg-tag wg-tag--20 wg-tag--grey">
  <span class="wg-tag__text">展示</span>
</span>
```

纯展示绿色标签：

```html
<span class="wg-tag wg-tag--20 wg-tag--green">
  <span class="wg-tag__text">GREEN</span>
</span>
```

标签组：

```html
<div class="wg-tag-group">
  <span class="wg-tag wg-tag--32 wg-tag--grey" role="button" tabindex="0" aria-pressed="false">
    <span class="wg-tag__text">标签1</span>
  </span>
  <span class="wg-tag wg-tag--32 wg-tag--grey wg-tag--selected" role="button" tabindex="0" aria-pressed="true">
    <span class="wg-tag__text">标签2</span>
  </span>
  <span class="wg-tag wg-tag--32 wg-tag--grey" role="button" tabindex="0" aria-pressed="false">
    <span class="wg-tag__text">标签3</span>
  </span>
</div>
```

## Canonical CSS

```css
/* ===== Tag 容器 ===== */
.wg-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-solid) transparent;
  border-radius: var(--wg-radius-full);
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
  transition:
    background-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard),
    color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard),
    border-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

/* ===== 尺寸 ===== */
.wg-tag--32 {
  block-size: var(--wg-size-32);
  min-inline-size: 52px;
  padding-inline: var(--wg-spacing-12);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-regular);
}

.wg-tag--28 {
  block-size: var(--wg-size-28);
  min-inline-size: 48px;
  padding-inline: var(--wg-spacing-12);
  font-size: var(--wg-font-size-12);
  line-height: var(--wg-font-lineheight-12);
  font-weight: var(--wg-font-weight-regular);
}

.wg-tag--24 {
  block-size: var(--wg-size-24);
  min-inline-size: 40px;
  padding-inline: var(--wg-spacing-8);
  font-size: var(--wg-font-size-12);
  line-height: var(--wg-font-lineheight-12);
  font-weight: var(--wg-font-weight-regular);
  border-radius: var(--wg-radius-full);
}

.wg-tag--20 {
  block-size: var(--wg-size-20);
  min-inline-size: 36px;
  padding-inline: var(--wg-spacing-8);
  font-size: var(--wg-font-size-12);
  line-height: var(--wg-font-lineheight-12);
  font-weight: var(--wg-font-weight-regular);
  border-radius: var(--wg-radius-sm);
  cursor: default;
}

/* ===== 文字 ===== */
.wg-tag__text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ===== 图标 ===== */
.wg-tag__icon {
  font-size: var(--wg-size-16);
  flex-shrink: 0;
}

.wg-tag--icon-left .wg-tag__icon {
  margin-inline-end: var(--wg-spacing-4);
}

.wg-tag--icon-right .wg-tag__icon {
  margin-inline-start: var(--wg-spacing-4);
}

/* ===== GREY 颜色预设 ===== */
.wg-tag--grey {
  background-color: var(--wg-color-bg-subtle);
  color: var(--wg-color-text-primary);
}

.wg-tag--grey.wg-tag--selected {
  background-color: var(--wg-color-bg-success);
  color: var(--wg-color-text-success);
}

/* ===== WHITE 颜色预设 ===== */
.wg-tag--white {
  background-color: var(--wg-color-bg-surface);
  color: var(--wg-color-text-primary);
  border: var(--wg-stroke-width-default) var(--wg-stroke-style-solid) var(--wg-color-border-default);
}

.wg-tag--white.wg-tag--selected {
  background-color: var(--wg-color-bg-success);
  color: var(--wg-color-text-success);
  border-color: var(--wg-color-border-success);
}

/* ===== GREEN 颜色预设 ===== */
.wg-tag--green {
  background-color: var(--wg-color-bg-surface);
  color: var(--wg-color-text-success);
  border: var(--wg-stroke-width-default) var(--wg-stroke-style-solid) var(--wg-color-border-success);
}

.wg-tag--green.wg-tag--selected {
  background-color: var(--wg-color-bg-success);
  color: var(--wg-color-text-success);
}

/* ===== TAG_20 特殊文字颜色 ===== */
.wg-tag--20.wg-tag--grey {
  color: var(--wg-color-text-tertiary);
}

.wg-tag--20.wg-tag--grey.wg-tag--selected {
  color: var(--wg-color-text-tertiary);
}

/* ===== 按下态 ===== */
.wg-tag--grey:not(.wg-tag--20):active {
  background-color: var(--wg-color-state-pressed);
}

.wg-tag--grey.wg-tag--selected:not(.wg-tag--20):active {
  background-color: var(--wg-color-border-success);
}

.wg-tag--white:not(.wg-tag--20):active {
  background-color: var(--wg-color-state-hover);
}

.wg-tag--white.wg-tag--selected:not(.wg-tag--20):active {
  background-color: var(--wg-color-border-success);
}

.wg-tag--green:not(.wg-tag--20):active {
  background-color: var(--wg-color-state-hover);
}

.wg-tag--green.wg-tag--selected:not(.wg-tag--20):active {
  background-color: var(--wg-color-border-success);
}

/* ===== 焦点态 ===== */
.wg-tag:focus-visible {
  outline: none;
}

.wg-tag:not(.wg-tag--20):focus-visible {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}

/* ===== 图标颜色 ===== */
.wg-tag--grey .wg-tag__icon,
.wg-tag--white .wg-tag__icon {
  color: var(--wg-color-text-primary);
}

.wg-tag--grey.wg-tag--icon-right .wg-tag__icon,
.wg-tag--white.wg-tag--icon-right .wg-tag__icon {
  color: var(--wg-color-text-tertiary);
}

.wg-tag--green .wg-tag__icon {
  color: var(--wg-color-text-success);
}

.wg-tag--grey.wg-tag--selected .wg-tag__icon,
.wg-tag--white.wg-tag--selected .wg-tag__icon {
  color: var(--wg-color-text-success);
}

/* ===== 标签组 ===== */
.wg-tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: var(--wg-spacing-8);
}
```

## 状态

| State | HTML / CSS 表达 | 适用 Size | 规则 |
|---|---|---|---|
| `default` | 默认 class | 全部 | 正常可用（size=20 为纯展示） |
| `selected` | `.wg-tag--selected` + `aria-pressed="true"` | 32, 28 | 选中态，背景和文字变色 |
| `pressed` | `:active` | 32, 28, 24 | 按下时背景变深，不位移、不缩放 |
| `focus-visible` | `:focus-visible` | 32, 28, 24 | 必须显示清晰焦点描边 |

V1 未定义 `disabled`、`loading` 视觉变体。遇到这些需求不得自行向 Tag 加入禁用样式或加载图标；通过页面级样式实现，并标注组件能力缺失。

## 可访问性

- 可点击标签（size=32/28/24）必须使用 `role="button"` 和 `tabindex="0"`。
- 可选中标签必须使用 `aria-pressed` 表达选中状态。
- `close` 图标必须使用 `role="button"` 和 `aria-label="移除"`。
- 纯展示标签（size=20）不添加交互角色和 tabindex。
- 焦点顺序必须与视觉顺序一致。
- 禁止使用 `div` 模拟可交互标签。

## 生成约束

- 必须同时声明一个 `size` class（`wg-tag--32` / `wg-tag--28` / `wg-tag--24` / `wg-tag--20`）和一个 `color` class（`wg-tag--grey` / `wg-tag--white` / `wg-tag--green`）。
- 有图标时必须声明 `wg-tag--icon-left` 或 `wg-tag--icon-right`。
- 选中态必须添加 `wg-tag--selected` class 和 `aria-pressed="true"`。
- 不得覆盖标签高度、字号、字重、颜色、圆角和间距。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 页面布局只控制标签组的位置，不控制标签内部样式。
- 完整页面中出现 Tag 时，必须读取并遵守本文件。
- Canonical CSS 必须从本文件 `## Canonical CSS` 区块逐字复制到 `styles/components.css`，不得增删规则、修改选择器或添加属性。组件视觉行为只能通过规范中已声明的修饰符 class 调整。

## 自检

```text
□ 是否先判断标签用途和交互需求选择 size
□ size=24 和 size=20 是否没有使用图标
□ size=20 是否没有添加交互角色和 tabindex
□ size=20 文字颜色是否为灰色（green 预设除外）
□ 是否选择了正确的颜色预设（grey / white / green）
□ 选中态是否同时添加了 --selected class 和 aria-pressed
□ close 图标是否添加了 role="button" 和 aria-label
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 是否没有自创 disabled、loading 变体
□ 同一标签组内 size 和 color 是否一致
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `467:5002`（Tag_标签）。提取四个尺寸（Tag_32 / Tag_28 / Tag_24 / Tag_20）的使用场景规则、场景说明和应用实例。
- Kuikly `Tag`：参考四种尺寸（TAG_32 / TAG_28 / TAG_24 / TAG_20）的高度、最小宽度、padding、字号、圆角、选中态行为、图标支持、颜色预设（GREY / WHITE / GREEN）、图标预设（CLOSE / ADD / JUMP_TO / EDIT）、按下态颜色和 TAG_20 特殊行为；不继承 Kuikly DSL、自定义颜色配置（TagCustomColorConfig）、maxWidth 属性、additionalIconAttr、isClickable 覆盖或高级配置。
