# Tabs

Tabs 用于在同一区域切换并列内容。本规则首先判断标签栏的导航范围和尺寸，再选择布局模式。

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

使用 Tabs：

- 页面级导航：统领整个页面内容切换，如数据中心切换访客、商品。
- 局部导航：在某个局部区域（卡片）内切换内容，如设置多价格-颜色 tab。

不使用 Tabs：

- 页面底部导航栏：使用 Bottom Tab Bar，不使用 Tabs。
- 筛选/分类标签：使用 Tag 或 Chip，不使用 Tabs。
- 单一内容展示：无需切换时不使用 Tabs。

## 语义模型

Tabs 有三个决策维度：

```text
size    标签栏尺寸
layout  布局模式
state   当前交互状态
```

### Size

| Size | 应用场景 | 视觉高度 | 字号 |
|---|---|---|---|
| `standard` | 页面级导航，统领整个页面内容切换 | `wg.size.56` | `wg.font.size.16` |
| `mini` | 局部导航，在某个局部区域（卡片）内切换内容 | `wg.size.48` | `wg.font.size.14` |

禁止直接根据"大、小"选择尺寸。必须先判断导航范围：页面级用 `standard`，局部区域用 `mini`。

### Layout

| Layout | 含义 | 触发条件 |
|---|---|---|
| `divide` | 等分型：各 Tab 等宽平分整行宽度 | Tab 数量 ≤ `maxSize`（默认 5） |
| `scroll` | 滑动型：Tab 按内容宽度排列，可水平滚动 | Tab 数量 > `maxSize`，或 `mini` 尺寸 |

布局模式选择规则：

- `standard` 尺寸下，Tab 数量 ≤ 5 时使用 `divide`，> 5 时自动切换为 `scroll`。
- `mini` 尺寸始终使用 `scroll`，第一个 Tab 左侧 padding 为 16px，其余为 8px。
- 无论哪种布局模式，组件都会占整个屏幕的宽度。

## 允许组合

| Size | Layout | 说明 |
|---|---|---|
| `standard` | `divide` | 页面级，Tab 数量 ≤ 5 |
| `standard` | `scroll` | 页面级，Tab 数量 > 5 |
| `mini` | `scroll` | 局部导航，始终滚动 |

附加规则：

- `standard` + `divide` 下，每个 Tab 宽度 = 页面宽度 / Tab 数量。
- `standard` + `scroll` 下，Tab 按内容宽度排列，可水平滚动。
- `mini` 始终为 `scroll`，不得使用 `divide`。
- 同一 Tabs 组件内所有 Tab 项的文字样式必须一致。

## Anatomy

标准等分型：

```text
div.wg-tabs.wg-tabs--standard.wg-tabs--divide
├── div.wg-tabs__scroll
│   └── button.wg-tabs__item
│       ├── span.wg-tabs__label
│       └── span.wg-tabs__indicator
```

标准滑动型：

```text
div.wg-tabs.wg-tabs--standard.wg-tabs--scroll
├── div.wg-tabs__scroll
│   └── button.wg-tabs__item
│       ├── span.wg-tabs__label
│       └── span.wg-tabs__indicator
```

迷你滑动型：

```text
div.wg-tabs.wg-tabs--mini.wg-tabs--scroll
├── div.wg-tabs__scroll
│   └── button.wg-tabs__item.wg-tabs__item--first
│       ├── span.wg-tabs__label
│       └── span.wg-tabs__indicator
```

V1 仅允许文字 Tab。不得自行加入图标、角标、副标题或徽章。

## 文案规则

- Tab 文字使用简短名词或短语，如"推荐""商品""访客""设置"。
- 每个 Tab 文字最多 4 个字符，超出截断显示省略号。
- Tab 文字单行展示，不换行。
- 同一 Tabs 内所有 Tab 文字使用一致的语法结构。
- 选中与未选中 Tab 文字内容相同，仅颜色和字重变化。

## Canonical HTML

标准等分型 — 3 个 Tab：

```html
<div class="wg-tabs wg-tabs--standard wg-tabs--divide" role="tablist">
  <div class="wg-tabs__scroll">
    <button class="wg-tabs__item" role="tab" aria-selected="true" type="button">
      <span class="wg-tabs__label">推荐</span>
      <span class="wg-tabs__indicator"></span>
    </button>
    <button class="wg-tabs__item" role="tab" aria-selected="false" type="button">
      <span class="wg-tabs__label">商品</span>
      <span class="wg-tabs__indicator"></span>
    </button>
    <button class="wg-tabs__item" role="tab" aria-selected="false" type="button">
      <span class="wg-tabs__label">访客</span>
      <span class="wg-tabs__indicator"></span>
    </button>
  </div>
</div>
```

标准滑动型 — 多个 Tab：

```html
<div class="wg-tabs wg-tabs--standard wg-tabs--scroll" role="tablist">
  <div class="wg-tabs__scroll">
    <button class="wg-tabs__item" role="tab" aria-selected="true" type="button">
      <span class="wg-tabs__label">推荐</span>
      <span class="wg-tabs__indicator"></span>
    </button>
    <button class="wg-tabs__item" role="tab" aria-selected="false" type="button">
      <span class="wg-tabs__label">商品</span>
      <span class="wg-tabs__indicator"></span>
    </button>
    <button class="wg-tabs__item" role="tab" aria-selected="false" type="button">
      <span class="wg-tabs__label">访客</span>
      <span class="wg-tabs__indicator"></span>
    </button>
    <button class="wg-tabs__item" role="tab" aria-selected="false" type="button">
      <span class="wg-tabs__label">订单</span>
      <span class="wg-tabs__indicator"></span>
    </button>
    <button class="wg-tabs__item" role="tab" aria-selected="false" type="button">
      <span class="wg-tabs__label">设置</span>
      <span class="wg-tabs__indicator"></span>
    </button>
    <button class="wg-tabs__item" role="tab" aria-selected="false" type="button">
      <span class="wg-tabs__label">更多</span>
      <span class="wg-tabs__indicator"></span>
    </button>
  </div>
</div>
```

迷你滑动型：

```html
<div class="wg-tabs wg-tabs--mini wg-tabs--scroll" role="tablist">
  <div class="wg-tabs__scroll">
    <button class="wg-tabs__item wg-tabs__item--first" role="tab" aria-selected="true" type="button">
      <span class="wg-tabs__label">白色</span>
      <span class="wg-tabs__indicator"></span>
    </button>
    <button class="wg-tabs__item" role="tab" aria-selected="false" type="button">
      <span class="wg-tabs__label">黑色</span>
      <span class="wg-tabs__indicator"></span>
    </button>
    <button class="wg-tabs__item" role="tab" aria-selected="false" type="button">
      <span class="wg-tabs__label">金色</span>
      <span class="wg-tabs__indicator"></span>
    </button>
  </div>
</div>
```

## Canonical CSS

```css
.wg-tabs {
  display: flex;
  inline-size: 100%;
  background-color: var(--wg-color-bg-surface);
}

.wg-tabs__scroll {
  display: flex;
  inline-size: 100%;
}

/* 等分型：所有 Tab 等宽 */
.wg-tabs--divide .wg-tabs__scroll {
  flex-wrap: nowrap;
}

.wg-tabs--divide .wg-tabs__item {
  flex: 1 1 0;
  min-inline-size: 0;
}

/* 滑动型：Tab 按内容宽度排列，可水平滚动 */
.wg-tabs--scroll .wg-tabs__scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  flex-wrap: nowrap;
}

.wg-tabs--scroll .wg-tabs__scroll::-webkit-scrollbar {
  display: none;
}

.wg-tabs--scroll .wg-tabs__item {
  flex: 0 0 auto;
}

/* Tab 项 */
.wg-tabs__item {
  appearance: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  cursor: pointer;
  position: relative;
  transition:
    opacity var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

/* standard 尺寸 */
.wg-tabs--standard .wg-tabs__item {
  block-size: var(--wg-size-56);
  padding-inline: var(--wg-spacing-16);
}

.wg-tabs--standard .wg-tabs__label {
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
  color: var(--wg-color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 4em;
}

.wg-tabs--standard .wg-tabs__item[aria-selected="true"] .wg-tabs__label {
  color: var(--wg-color-text-primary);
}

/* mini 尺寸 */
.wg-tabs--mini .wg-tabs__item {
  block-size: var(--wg-size-48);
  padding-inline: var(--wg-spacing-8);
}

.wg-tabs--mini .wg-tabs__item--first {
  padding-left: var(--wg-spacing-16);
}

.wg-tabs--mini .wg-tabs__label {
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-medium);
  color: var(--wg-color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 4em;
}

.wg-tabs--mini .wg-tabs__item[aria-selected="true"] .wg-tabs__label {
  color: var(--wg-color-text-primary);
}

/* 指示器 */
.wg-tabs__indicator {
  display: none;
  block-size: var(--wg-stroke-width-none);
  background-color: var(--wg-color-action-primary-default);
  border-radius: var(--wg-radius-full);
  margin-inline: var(--wg-spacing-2);
}

.wg-tabs__item[aria-selected="true"] .wg-tabs__indicator {
  display: block;
}

/* standard 指示器 3px */
.wg-tabs--standard .wg-tabs__indicator {
  block-size: 3px;
  inline-size: 100%;
}

/* mini 指示器 2px */
.wg-tabs--mini .wg-tabs__indicator {
  block-size: 2px;
  flex: 1 1 0;
  min-inline-size: 0;
}

/* 按下态 */
.wg-tabs__item:not(:disabled):active {
  opacity: 0.6;
}

/* 焦点态 */
.wg-tabs__item:focus-visible {
  outline: none;
}

.wg-tabs__item:focus-visible .wg-tabs__label {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}
```

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 未选中 Tab 使用二级文字色，选中 Tab 使用一级文字色 + 指示器 |
| `pressed` | `:active` | 按下时透明度 0.6，不位移、不缩放 |
| `focus-visible` | `:focus-visible` | 必须显示清晰焦点描边 |

V1 未定义 `disabled`、`loading`、`badge` 视觉变体。遇到这些需求不得自行向 Tabs 加入禁用样式、徽章或加载图标；通过页面级样式实现，并标注组件能力缺失。

## 可访问性

- 必须使用 `role="tablist"` 作为标签栏容器。
- 每个 Tab 必须使用原生 `<button>` 并设置 `role="tab"`。
- 选中 Tab 必须设置 `aria-selected="true"`，未选中设置为 `aria-selected="false"`。
- Tab 面板应使用 `role="tabpanel"` 并通过 `aria-labelledby` 关联对应 Tab。
- 焦点顺序必须与视觉顺序一致：从左到右。
- 禁止使用 `div`、`span` 模拟可点击 Tab。
- 滑动型 Tabs 的滚动区域不得阻止键盘导航。

## 生成约束

- 必须同时声明一个 `size` class 和一个 `layout` class。
- `mini` 必须搭配 `scroll`，不得搭配 `divide`。
- 不得覆盖标签栏高度、字号、字重、指示器高度和指示器颜色。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 页面布局只控制 Tabs 的位置，不控制 Tabs 内部样式。
- 完整页面中出现 Tabs 时，必须读取并遵守本文件。

## 自检

```text
□ 是否先判断页面级 / 局部导航 → standard / mini
□ standard 下 Tab 数量 ≤ 5 是否使用 divide
□ standard 下 Tab 数量 > 5 是否使用 scroll
□ mini 是否始终使用 scroll
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 每个 Tab 是否使用原生 button + role="tab"
□ 选中 Tab 是否设置 aria-selected="true"
□ 是否没有自创 disabled、badge、icon 变体
□ Tab 文字是否不超过 4 个字符
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `559:42238`。提取 TabBar（standard）和 TabBar_mini（mini）的高度、字号、颜色、指示器和间距。
- Kuikly `TabBar`：参考两种尺寸（STANDARD / MINI）、两种布局模式（等分型 / 滑动型）、maxSize 默认 5、指示器样式和联动机制；不继承 Kuikly DSL、PageList 联动、自定义主题或高级配置。
- Kuikly `tabs`：参考 scrollParams、defaultInitIndex、indicatorInTabItem 和 indicatorAlignCenter / indicatorAlignAspectRatio 的底层能力；V1 不实现联动逻辑。
