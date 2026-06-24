# Link

Link 用于低强调的跳转、入口或次要操作。本规则先判断链接所在语境，再根据行为语义选择原生 `<a>` 或 `<button>`。

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

使用 Link：

- 页面主流程之外的跳转、帮助、说明或补充入口。
- 主操作之后的次要操作，例如“编辑后邀请”“什么是粉丝”。
- 列表项、表单项或紧凑横条右侧的低强调操作。
- 一段正文或辅助说明中的上下文操作。

不使用 Link：

- 提交、保存、发布、确认、完成或推进流程：使用 Button。
- 整行内容都可点击并进入详情：使用可点击 Cell，不在行内重复放 Link。
- 标签页或视图切换：使用 Tabs 或 Segmented Control。
- 只有图标且没有文字标签：暂不生成，标注 Icon Button 规范缺失。
- 需要高强调、危险色、加载态或成功态的操作：当前 Link V1 不支持，不得自行创建变体。

## 语义模型

Link 有三个决策维度：

```text
context   链接所在语境
behavior  触发后是导航还是执行命令
state     当前交互状态
```

### Context

| Context | Figma 映射 | 应用场景 | 排版规则 |
|---|---|---|---|
| `standalone` | `Link_14` | 次要入口、流程外操作、列表或表单右侧操作 | 使用 `wg.font.size.f14`、`wg.font.lineHeight.f14`、`wg.font.weight.medium` |
| `inline` | `Link_intext` | 一段文本中，或紧接在文本后面的操作 | 继承所在文本的字号、行高和字重 |

禁止直接根据字号选择 Link。必须先判断链接是独立操作还是正文的一部分。

### Behavior

| Behavior | 语义 | 原生元素 |
|---|---|---|
| `navigation` | 打开页面、路由、资源或说明内容 | 带有效 `href` 的 `<a>` |
| `command` | 在当前页面执行删除、编辑、邀请等命令 | `type="button"` 的 `<button>` |

视觉样式不能决定原生元素。只要触发的是命令，即使看起来像文本链接，也必须使用 `<button>`。

## 允许组合

| Context | Navigation | Command | 同一区域数量 |
|---|---|---|---|
| `standalone` | 允许 | 允许 | 默认一个；列表或表单右侧最多三个 |
| `inline` | 允许 | 允许 | 同一段说明默认一个 |

附加规则：

- Link 只能表达低强调操作，不能替代当前作用范围内的 `strong` Button。
- 列表或表单右侧超过三个操作时，保留高频操作，其余进入更多菜单。
- 多个 `standalone` Link 使用 Link Group 横向排列，不用空格字符制造间距。
- `inline` Link 必须保持所在句子的自然阅读顺序，不得单独换行伪装成 Button。
- 同一操作不得同时出现 Button 和 Link 两个入口。

## Anatomy

导航链接：

```text
a.wg-link.wg-link--{context}
└── span.wg-link__surface
    └── span.wg-link__label
```

命令链接：

```text
button.wg-link.wg-link--{context}
└── span.wg-link__surface
    └── span.wg-link__label
```

V1 仅允许文字内容。不得自行加入图标、角标、副标题或外部链接图标。

## 文案规则

- 导航链接使用能说明目的地的名词或短语，例如“权限设置”“什么是粉丝”。
- 命令链接使用明确动词，例如“编辑”“删除”“去邀请”。
- 避免“点击这里”“查看更多”等脱离上下文后无法理解的文案。
- `standalone` Link 单行展示，不换行。
- `inline` Link 可以随正文自然换行，但链接文字本身应保持简短。
- 同组操作使用一致的语法结构和粒度。

## Canonical HTML

独立导航入口：

```html
<a class="wg-link wg-link--standalone" href="/help/fans">
  <span class="wg-link__surface">
    <span class="wg-link__label">什么是粉丝</span>
  </span>
</a>
```

列表右侧命令：

```html
<div class="wg-link-group" aria-label="岗位操作">
  <button class="wg-link wg-link--standalone" type="button">
    <span class="wg-link__surface">
      <span class="wg-link__label">删除</span>
    </span>
  </button>
  <button class="wg-link wg-link--standalone" type="button">
    <span class="wg-link__surface">
      <span class="wg-link__label">编辑</span>
    </span>
  </button>
  <button class="wg-link wg-link--standalone" type="button">
    <span class="wg-link__surface">
      <span class="wg-link__label">邀请</span>
    </span>
  </button>
</div>
```

正文内导航入口：

```html
<p class="wg-supporting-text">
  尚未邀请该客户，
  <a class="wg-link wg-link--inline" href="/customers/invite">
    <span class="wg-link__surface">
      <span class="wg-link__label">去邀请</span>
    </span>
  </a>
</p>
```

命令型 Link 禁用时使用原生 `disabled`。导航型 Link 禁用时必须移除 `href`，并同时设置 `aria-disabled="true"`；不得保留仍可访问的目标地址。

## Canonical CSS

```css
.wg-link-group {
  display: flex;
  align-items: center;
  gap: var(--wg-spacing-16);
}

.wg-link {
  appearance: none;
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  color: var(--wg-color-action-link-default);
  font-family: inherit;
  text-decoration: none;
  cursor: pointer;
  transition:
    color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-link__surface {
  border-radius: var(--wg-radius-none);
  transition:
    background-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard),
    outline-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-link--standalone {
  display: inline-flex;
  min-block-size: var(--wg-touch-min);
  align-items: center;
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-medium);
}

.wg-link--standalone .wg-link__surface {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.wg-link--standalone .wg-link__label {
  white-space: nowrap;
}

.wg-link--inline,
.wg-link--inline .wg-link__surface,
.wg-link--inline .wg-link__label {
  display: inline;
  font: inherit;
  line-height: inherit;
}

.wg-link:visited {
  color: var(--wg-color-action-link-default);
}

.wg-link:not(:disabled):not([aria-disabled="true"]):hover {
  color: var(--wg-color-action-link-hover);
}

.wg-link:not(:disabled):not([aria-disabled="true"]):hover .wg-link__surface,
.wg-link:not(:disabled):not([aria-disabled="true"]):active .wg-link__surface {
  background-color: var(--wg-color-state-pressed);
}

.wg-link:not(:disabled):not([aria-disabled="true"]):active {
  color: var(--wg-color-action-link-pressed);
}

.wg-link:focus-visible {
  outline: none;
}

.wg-link:focus-visible .wg-link__surface {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}

.wg-link:disabled,
.wg-link[aria-disabled="true"] {
  color: var(--wg-color-action-link-disabled);
  cursor: not-allowed;
}

a.wg-link[aria-disabled="true"] {
  pointer-events: none;
}
```

`standalone` 的文字视觉高度由 `wg.font.lineHeight.f14` 决定，外层点击区域通过 `wg.touch.min` 保证最小触控尺寸。`inline` 必须继承上下文排版，不得强制改成固定字号。

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 使用链接色，无背景 |
| `hover` | `:hover` | 桌面原型显示弱背景，不作为移动端必要状态 |
| `pressed` | `:active` | 使用弱背景，不位移、不缩放 |
| `focus-visible` | `:focus-visible` | 必须显示清晰焦点描边 |
| `disabled` | `disabled` 或 `aria-disabled="true"` | 使用链接禁用色，不响应操作 |

V1 未定义 `visited` 的差异化视觉，也未定义 `loading`、`selected`、`success`、`error`、`danger` 视觉变体。遇到这些需求不得修改 Link 变体；通过页面级状态和相邻反馈结构表达，并标注组件能力缺失。

## 可访问性

- 导航必须使用带有效 `href` 的 `<a>`，命令必须使用原生 `<button>`。
- 不得使用 `div`、`span` 或 `href="#"` 模拟 Link。
- Link 文案脱离周边文本后仍应能说明目的地或结果。
- `standalone` Link 的点击区域不得小于 `wg.touch.min`。
- `inline` Link 不得在一个短句中密集堆叠，避免产生难以准确点击的目标。
- 命令禁用使用 `disabled`；导航禁用必须移除 `href` 并设置 `aria-disabled="true"`。
- 焦点顺序必须与视觉顺序一致，焦点态不能只依赖颜色变化。
- 新窗口打开时必须在可访问名称中说明，当前 V1 不自动生成外部链接图标。

## 生成约束

- 必须同时声明一个 `context` class，并根据 `behavior` 选择正确原生元素。
- 必须使用 `wg-link__surface` 和 `wg-link__label`。
- 不得覆盖文字色、状态背景、字号、字重、行高和点击区域。
- `inline` 只能继承上下文排版，调用方不得另设 Link 专用字号。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`small`、`danger`、`icon` 等平行命名。
- 页面布局只控制 Link 或 Link Group 的位置，不控制 Link 内部样式。
- 完整页面中出现 Link 时，必须读取并遵守本文件。

## 自检

```text
□ 是否先判断 standalone / inline
□ 是否根据 navigation / command 选择 a 或 button
□ 是否没有用 Link 替代主流程 Button
□ 列表或表单右侧是否不超过三个 Link
□ inline 是否继承所在文本排版
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ disabled 是否使用正确原生语义
□ 是否没有自创 danger、loading、icon 变体
```

## 规范来源

- Figma：`📙 V1-组件应用场景-2024.12 - Copy`，节点 `493:38331`。提取 `Link_14`、`Link_intext`、默认态、弱背景交互态、禁用态及三类使用场景。
- HTML 语义与可访问性：在保持 Figma 视觉规范的基础上，根据导航与命令行为分别使用原生 `<a>` 和 `<button>`。
