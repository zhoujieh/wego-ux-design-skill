# Button

Button 用于触发明确操作。本规则首先判断按钮影响范围和操作优先级，再映射尺寸与视觉样式。

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

使用 Button：

- 提交、保存、发布、完成、确认等会执行动作的操作。
- 推进流程的下一步操作。
- 局部容器内最重要的功能操作。
- 卡片、列表项或横条区域中的紧凑操作。

不使用 Button：

- 页面跳转但不执行动作：使用 Link 或可点击 Cell。
- 标签切换：使用 Tabs 或 Segmented Control。
- 只有图标且没有稳定图标规范：暂不生成，标注 Icon Button 规范缺失。
- 三个及以上并列操作：保留主要操作，其余进入更多菜单；不得平铺按钮。

## 语义模型

Button 只有三个决策维度：

```text
scope     按钮影响范围
emphasis  操作优先级
state     当前交互状态
```

### Scope

| Scope | 应用场景 | 视觉高度 | 宽度规则 |
|---|---|---|---|
| `page` | 页面级主要操作、流程推进、结果页操作 | `wg.size.48` | 单个或纵向排列使用 `wg.component.button.width.page.single`；横向成对使用 `wg.component.button.width.page.paired`；表单型页面使用自适应容器宽度（见下方宽度策略） |
| `container` | 卡片、模块、局部区域内的核心操作 | `wg.size.40` | 自适应容器，按钮组最大宽度为 `wg.component.button.width.container.max` |
| `compact` | 列表、导航栏、底部操作栏、横幅、卡片行内操作 | `wg.size.32` | 跟随内容，最大宽度为 `wg.component.button.width.compact.max` |

禁止让 AI 直接根据"大、中、小"选择尺寸。必须先判断 `scope`。

### 宽度策略

`page` 级按钮的宽度需要根据页面类型选择策略：

| 页面类型 | 宽度策略 | 说明 |
|---|---|---|
| 表单型页面（登录、注册、设置、重置等） | 自适应容器宽度 | 按钮宽度跟随 M0–M3 布局的内容区宽度，`inline-size: 100%`，不使用固定宽度 Token |
| 结果型页面（操作成功、操作失败等） | 固定宽度 `wg.component.button.width.page.single` | 居中展示，不需要撑满 |
| 浏览型页面底部的固定操作栏 | 自适应容器宽度 | 跟随操作栏宽度 |

判断流程：

```text
页面是否为表单型？
├─ 是 → 按钮自适应容器宽度
└─ 否 → 页面是否为结果型？
    ├─ 是 → 使用 page.single 固定宽度
    └─ 否 → 使用 page.single 固定宽度
```

`container` 和 `compact` 级按钮始终使用自适应宽度或跟随内容，不受此策略影响。

### Emphasis

| Emphasis | 含义 | 样式映射 |
|---|---|---|
| `strong` | 最重要、推荐或推进流程的操作 | 品牌色背景 + 反色文字 |
| `medium` | 有明确功能且较重要，但不需要重点引导 | 弱背景 + 品牌色文字 |
| `weak` | 次要、取消、关闭或不需要强调的操作 | 弱背景 + 一级文字 |

`medium` 只用于单按钮。按钮组合只允许 `strong + weak` 或 `weak + weak`。

## 允许组合

| Scope | 单按钮 | 双按钮 | 三个及以上操作 |
|---|---|---|---|
| `page` | `strong` / `medium` / `weak` | 只允许 `strong + weak` | 禁止 |
| `container` | `strong` / `medium` / `weak` | `strong + weak` 或 `weak + weak` | 禁止 |
| `compact` | `strong` / `medium` / `weak` | `strong + weak` 或 `weak + weak` | 保留最多两个，其他操作进入更多菜单 |

附加规则：

- 同一作用范围内只能有一个 `strong`。
- 不得出现 `strong + strong`、`medium + medium`、`medium + weak`。
- `page` 双按钮默认纵向排列；只有明确要求紧凑并列时才使用横向排列。
- `container` 和 `compact` 双按钮横向排列。
- 横向排列时，主要操作位于右侧，次要操作位于左侧。

## Anatomy

```text
button.wg-button
└── span.wg-button__surface
    └── span.wg-button__label
```

V1 仅允许文字按钮。不得自行加入图标、角标、副标题或加载图标。

## 文案规则

- 使用能说明结果的动词或动宾短语，例如“保存”“发布商品”“确认退款”。
- 避免只有“确定”，能够说明具体结果时必须写清结果。
- 单行展示，不换行。
- 同组按钮文案使用一致的语法结构。
- 危险操作必须写明对象和后果；当前 V1 不定义危险色 Button 变体。

## Canonical HTML

页面级单按钮：

```html
<div class="wg-button-group wg-button-group--page wg-button-group--single">
  <button class="wg-button wg-button--page wg-button--strong" type="button">
    <span class="wg-button__surface">
      <span class="wg-button__label">完成</span>
    </span>
  </button>
</div>
```

局部容器双按钮：

```html
<div class="wg-button-group wg-button-group--container wg-button-group--inline">
  <button class="wg-button wg-button--container wg-button--weak" type="button">
    <span class="wg-button__surface">
      <span class="wg-button__label">取消</span>
    </span>
  </button>
  <button class="wg-button wg-button--container wg-button--strong" type="button">
    <span class="wg-button__surface">
      <span class="wg-button__label">确认</span>
    </span>
  </button>
</div>
```

紧凑双按钮：

```html
<div class="wg-button-group wg-button-group--compact wg-button-group--inline">
  <button class="wg-button wg-button--compact wg-button--weak" type="button">
    <span class="wg-button__surface">
      <span class="wg-button__label">删除</span>
    </span>
  </button>
  <button class="wg-button wg-button--compact wg-button--strong" type="button">
    <span class="wg-button__surface">
      <span class="wg-button__label">再来一次</span>
    </span>
  </button>
</div>
```

表单真实提交操作才使用 `type="submit"`，其余按钮必须使用 `type="button"`。

## Canonical CSS

```css
.wg-button-group {
  display: flex;
  gap: var(--wg-spacing-8);
}

.wg-button-group--single,
.wg-button-group--page {
  justify-content: center;
}

.wg-button-group--page:not(.wg-button-group--inline) {
  flex-direction: column;
  align-items: center;
}

.wg-button-group--inline {
  flex-direction: row;
  align-items: center;
}

.wg-button-group--container {
  inline-size: 100%;
  max-inline-size: var(--wg-component-button-width-container-max);
}

.wg-button-group--compact {
  inline-size: fit-content;
}

.wg-button {
  --button-visual-height: var(--wg-size-40);
  appearance: none;
  display: inline-flex;
  min-inline-size: 0;
  min-block-size: max(var(--wg-touch-min), var(--button-visual-height));
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  color: inherit;
  cursor: pointer;
}

.wg-button__surface {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  inline-size: 100%;
  block-size: var(--button-visual-height);
  padding-inline: var(--wg-spacing-16);
  overflow: hidden;
  border-radius: var(--wg-radius-sm);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
  transition:
    color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard),
    background-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard),
    outline-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-button__label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.wg-button--page {
  --button-visual-height: var(--wg-size-48);
  inline-size: var(--wg-component-button-width-page-single);
}

.wg-button-group--page.wg-button-group--inline .wg-button {
  inline-size: var(--wg-component-button-width-page-paired);
}

.wg-button--container {
  --button-visual-height: var(--wg-size-40);
  flex: 1 1 0;
  inline-size: 100%;
}

.wg-button--compact {
  --button-visual-height: var(--wg-size-32);
  inline-size: fit-content;
  max-inline-size: var(--wg-component-button-width-compact-max);
}

.wg-button--compact .wg-button__surface {
  padding-inline: var(--wg-spacing-12);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
}

.wg-button--strong .wg-button__surface {
  background-color: var(--wg-color-action-primary-default);
  color: var(--wg-color-text-inverse);
}

.wg-button--medium .wg-button__surface {
  background-color: var(--wg-color-action-secondary-default);
  color: var(--wg-color-action-primary-default);
}

.wg-button--weak .wg-button__surface {
  background-color: var(--wg-color-action-secondary-default);
  color: var(--wg-color-text-primary);
}

.wg-button--strong:not(:disabled):hover .wg-button__surface {
  background-color: var(--wg-color-action-primary-hover);
}

.wg-button--medium:not(:disabled):hover .wg-button__surface,
.wg-button--weak:not(:disabled):hover .wg-button__surface {
  background-color: var(--wg-color-action-secondary-hover);
}

.wg-button--strong:not(:disabled):active .wg-button__surface {
  background-color: var(--wg-color-action-primary-pressed);
}

.wg-button--medium:not(:disabled):active .wg-button__surface,
.wg-button--weak:not(:disabled):active .wg-button__surface {
  background-color: var(--wg-color-action-secondary-pressed);
}

.wg-button:focus-visible {
  outline: none;
}

.wg-button:focus-visible .wg-button__surface {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}

.wg-button:disabled {
  cursor: not-allowed;
}

.wg-button:disabled .wg-button__surface {
  background-color: var(--wg-color-state-disabled-bg);
  color: var(--wg-color-state-disabled-text);
}
```

`compact` 的可见按钮高度使用 `wg.size.32`，外层点击区域通过 `wg.touch.min` 保证最小触控尺寸。

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 正常可用 |
| `hover` | `:hover` | 仅用于桌面原型预览，不作为移动端必要状态 |
| `pressed` | `:active` | 只改变操作背景，不位移、不缩放 |
| `focus-visible` | `:focus-visible` | 必须显示清晰焦点描边 |
| `disabled` | `disabled` | 统一使用禁用背景和文字，不响应操作 |

V1 未定义 `loading`、`success`、`error` 视觉变体。遇到这些需求不得自行向 Button 加入 Spinner、图标或颜色；通过 `disabled`、`aria-busy` 和页面级相邻反馈区域实现业务状态，并标注组件能力缺失。

## 可访问性

- 必须使用原生 `<button>`。
- 禁用状态必须使用 `disabled`，不能只降低透明度。
- 按钮必须有可理解的文字标签。
- 可见高度小于最小触控尺寸时，外层点击区域仍必须满足 `wg.touch.min`。
- 焦点顺序必须与视觉顺序一致。
- 禁止使用 `div`、`span` 模拟可点击按钮。

## 生成约束

- 必须同时声明一个 `scope` 和一个 `emphasis` class。
- 必须使用 `wg-button__surface` 和 `wg-button__label`。
- 不得覆盖背景色、文字色、圆角、宽度、高度和 padding。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 页面布局只控制 Button Group 的位置，不控制 Button 内部样式。
- 完整页面中出现 Button 时，必须读取并遵守本文件。

## 自检

```text
□ 是否先判断 page / container / compact
□ 是否只存在一个 strong
□ 是否遵守单按钮和双按钮组合
□ 是否把三个及以上操作收纳到更多菜单
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 是否使用原生 button 和正确 type
□ disabled 是否使用原生属性
□ 是否没有自创 loading、danger、icon-only 变体
```

## 规范来源

- Figma：`📙 V1-组件应用场景(2024.12) (Copy)`，节点 `141:36071`。提取页面级、局部容器和横条/卡片按钮的应用规则。
- Kuikly `WGButton`：仅参考三档高度、文字字号、禁用态和基础颜色方案；不继承 Kuikly DSL、自定义颜色、渐变或高级配置。
