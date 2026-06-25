# Cell

Cell 用于列表中的导航与信息查看。本规则首先判断 Cell 变体（基础 / 头像 / 选择），再选择操作区类型和分割线样式。

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

使用 Cell：

- 列表中的跳转入口，如设置页、个人中心等导航项。
- 列表中的开关项，开关即时生效、不需要保存提交。
- 展示多条相关信息的列表，如好友列表、消息列表。
- 列表切换成选择模式，如多选商品、选择联系人。

不使用 Cell：

- 需要提交保存的表单项：使用 Input 或 Form 组件。
- 弹出操作菜单：使用 ActionSheet。
- 确认/警告弹窗：使用 Dialog。
- 纯展示无交互的信息行：使用文本布局，不使用 Cell。

Cell 与 Form 的区别：

- Cell 用于导航与查看信息，看到啥事实就是啥，没有保存的概念。
- Form 是为了提交保存而存在。Form 里也有跳转的分支，样式与 Cell 几乎一致，但前者是因为设置项比较复杂，需要跳转或拉起弹窗进行设置，其本身仍然需要提交保存。
- Switch 开关有即时生效的属性，所以开关本身不依赖于保存提交，故属于 Cell 的一类用法。在 Form，开关可用于控制设置项的显示与否，但不能用于设置值。

### Cell 与 Form 的边界

- Cell 适合展示型、跳转型、轻操作型信息
- Form 适合输入、选择、校验、提交相关信息
- 如果内容需要校验、错误提示、恢复状态，应优先使用 Form，而不是普通 Cell
- 不允许用 Cell 伪装复杂表单字段

### Cell 对齐一致性

同一个 Cell Group 内必须保持：

- label 对齐一致
- value / action 对齐一致
- icon 位置一致
- 分隔线规则一致
- 高度和 padding 节奏一致

禁止：

- 同组内一部分左对齐，一部分右对齐
- 同组内一部分像展示项，一部分像表单项，但没有明确分组
- 用 Cell 堆出复杂页面

## 语义模型

Cell 有四个决策维度：

```text
variant   列表变体
action    操作区类型
divider   分割线样式
state     当前交互状态
```

### Variant

| Variant | 应用场景 | 左侧区域 | 行高 |
|---|---|---|---|
| `default` | 跳转入口、开关项 | 无选择区、无头像 | `wg.size.56`（单行）/ `wg.size.72`（双行） |
| `avatar` | 展示多条相关信息的列表 | 有头像区（44px + 12px 间距） | `wg.size.56`（单行）/ `wg.size.72`（双行） |
| `action` | 列表切换成选择时使用 | 有选择区（40px） | `wg.size.56` |

禁止让 AI 直接根据"有没有头像"选择变体。必须先判断列表用途：导航与查看用 `default`，展示相关信息用 `avatar`，切换选择用 `action`。

### Action

| Action | 含义 | 右侧内容 |
|---|---|---|
| `jump` | 箭头跳转 | 可选文本 + 右箭头图标 |
| `text` | 纯文本 | 只读文本信息 |
| `switch` | 开关 | Switch 开关控件 |
| `button` | 按钮 | WGButton SCALE_32 |
| `custom` | 无操作区 / 自定义 | 不显示操作区 |

Action 选择规则：

- 跳转到新页面用 `jump`。
- 展示只读信息（如"上次选择"）用 `text`。
- 即时生效的开关用 `switch`。
- 需要触发操作（如"编辑""关注"）用 `button`。
- 无操作区用 `custom`。

### Divider

| Divider | 含义 | 视觉规则 |
|---|---|---|
| `full` | 分割线右侧到头 | 分割线从左侧内容起始位置延伸到右边缘 |
| `inset` | 分割线右侧保留间距 | 分割线从左侧内容起始位置延伸，右侧保留 `wg.spacing.16` 间距 |
| `none` | 不显示分割线 | 无分割线 |

## 允许组合

| Variant | Action | 单行/双行 | 说明 |
|---|---|---|---|
| `default` | `jump` | 单行 | 最简跳转项 |
| `default` | `jump` | 双行 | 带副标题的跳转项 |
| `default` | `switch` | 单行 | 开关项 |
| `default` | `switch` | 双行 | 带副标题的开关项 |
| `default` | `text` | 单行 | 展示只读信息 |
| `default` | `button` | 单行 | 带操作按钮 |
| `default` | `custom` | 单行 | 无操作区 |
| `avatar` | `jump` | 单行 | 头像 + 跳转 |
| `avatar` | `jump` | 双行 | 头像 + 副标题 + 跳转 |
| `avatar` | `text` | 单行 | 头像 + 只读信息 |
| `avatar` | `custom` | 双行 | 头像 + 副标题 + 自定义操作区 |
| `action` | `jump` | 单行 | 选择区 + 跳转 |
| `action` | `custom` | 单行 | 选择区 + 无操作区 |

附加规则：

- `avatar` 变体下不得使用 `switch` 操作区（头像列表不适合放开关）。
- `action` 变体下不得使用 `switch` 操作区（选择列表与开关互斥）。
- `switch` 操作区不得同时出现文本和箭头。
- 同一列表中所有 Cell 的 `variant` 必须一致。
- 同一列表中所有 Cell 的 `divider` 必须一致（最后一项可用 `none`）。
- 双行 Cell 必须提供副标题文本，不得留空。

## Anatomy

基础变体 + 跳转操作 + 单行：

```text
div.wg-cell.wg-cell--default.wg-cell--jump
├── div.wg-cell__body
│   └── div.wg-cell__content
│       └── span.wg-cell__title
└── div.wg-cell__action
    ├── span.wg-cell__action-text（可选）
    └── i.wg-cell__arrow
```

基础变体 + 开关操作 + 双行：

```text
div.wg-cell.wg-cell--default.wg-cell--switch.wg-cell--two-line
├── div.wg-cell__body
│   └── div.wg-cell__content
│       ├── span.wg-cell__title
│       └── span.wg-cell__subtitle
└── div.wg-cell__action
    └── label.wg-cell__switch
        ├── input[type="checkbox"]
        └── span.wg-cell__switch-track
```

头像变体 + 跳转操作 + 双行：

```text
div.wg-cell.wg-cell--avatar.wg-cell--jump.wg-cell--two-line
├── div.wg-cell__body
│   ├── div.wg-cell__avatar
│   │   └── img.wg-cell__avatar-img 或 div.wg-cell__avatar-placeholder
│   └── div.wg-cell__content
│       ├── span.wg-cell__title
│       └── span.wg-cell__subtitle
└── div.wg-cell__action
    └── i.wg-cell__arrow
```

选择变体 + 跳转操作：

```text
div.wg-cell.wg-cell--action.wg-cell--jump
├── div.wg-cell__body
│   ├── div.wg-cell__select
│   │   └── input[type="checkbox"].wg-cell__checkbox
│   └── div.wg-cell__content
│       └── span.wg-cell__title
└── div.wg-cell__action
    └── i.wg-cell__arrow
```

V1 仅允许上述 Anatomy 中的元素。不得自行加入徽章、标签、标题图标、退格区、自定义内容插槽；这些作为 V1 能力缺失标注。

## 文案规则

- 标题使用简短名词或名词短语，如"用户名""消息通知""推送设置"。
- 副标题作为标题的补充说明，如"开启后将接收推送通知""管理你的好友列表"。
- 操作区文本使用简短描述，如"查看详情""上次选择""3 条新消息"。
- 所有文本单行展示，不换行，超长时截断显示省略号。
- 同一列表内标题文案使用一致的语法结构。

## Canonical HTML

基础变体 + 跳转操作 + 单行：

```html
<div class="wg-cell wg-cell--default wg-cell--jump wg-cell--divider-full">
  <div class="wg-cell__body">
    <div class="wg-cell__content">
      <span class="wg-cell__title">消息通知</span>
    </div>
  </div>
  <div class="wg-cell__action">
    <span class="wg-cell__action-text">查看详情</span>
    <i class="wg-cell__arrow"></i>
  </div>
</div>
```

基础变体 + 跳转操作 + 双行：

```html
<div class="wg-cell wg-cell--default wg-cell--jump wg-cell--two-line wg-cell--divider-full">
  <div class="wg-cell__body">
    <div class="wg-cell__content">
      <span class="wg-cell__title">推送通知</span>
      <span class="wg-cell__subtitle">开启后将接收推送通知</span>
    </div>
  </div>
  <div class="wg-cell__action">
    <i class="wg-cell__arrow"></i>
  </div>
</div>
```

基础变体 + 开关操作：

```html
<div class="wg-cell wg-cell--default wg-cell--switch wg-cell--divider-inset">
  <div class="wg-cell__body">
    <div class="wg-cell__content">
      <span class="wg-cell__title">推送通知</span>
      <span class="wg-cell__subtitle">开启后将接收推送通知</span>
    </div>
  </div>
  <div class="wg-cell__action">
    <label class="wg-cell__switch">
      <input class="wg-cell__switch-input" type="checkbox" />
      <span class="wg-cell__switch-track"></span>
    </label>
  </div>
</div>
```

基础变体 + 纯文本操作：

```html
<div class="wg-cell wg-cell--default wg-cell--text wg-cell--divider-full">
  <div class="wg-cell__body">
    <div class="wg-cell__content">
      <span class="wg-cell__title">上次选择</span>
    </div>
  </div>
  <div class="wg-cell__action">
    <span class="wg-cell__action-text">选项 A</span>
  </div>
</div>
```

基础变体 + 按钮操作：

```html
<div class="wg-cell wg-cell--default wg-cell--button wg-cell--divider-full">
  <div class="wg-cell__body">
    <div class="wg-cell__content">
      <span class="wg-cell__title">操作按钮</span>
    </div>
  </div>
  <div class="wg-cell__action">
    <button class="wg-button wg-button--compact wg-button--strong" type="button">
      <span class="wg-button__surface">
        <span class="wg-button__label">编辑</span>
      </span>
    </button>
  </div>
</div>
```

头像变体 + 跳转操作 + 双行：

```html
<div class="wg-cell wg-cell--avatar wg-cell--jump wg-cell--two-line wg-cell--divider-inset">
  <div class="wg-cell__body">
    <div class="wg-cell__avatar">
      <div class="wg-cell__avatar-placeholder">头</div>
    </div>
    <div class="wg-cell__content">
      <span class="wg-cell__title">用户名</span>
      <span class="wg-cell__subtitle">作为用法解释</span>
    </div>
  </div>
  <div class="wg-cell__action">
    <i class="wg-cell__arrow"></i>
  </div>
</div>
```

选择变体 + 跳转操作：

```html
<div class="wg-cell wg-cell--action wg-cell--jump wg-cell--divider-full">
  <div class="wg-cell__body">
    <div class="wg-cell__select">
      <input class="wg-cell__checkbox" type="checkbox" aria-label="选择" />
    </div>
    <div class="wg-cell__content">
      <span class="wg-cell__title">用户名</span>
    </div>
  </div>
  <div class="wg-cell__action">
    <i class="wg-cell__arrow"></i>
  </div>
</div>
```

灰色背景：

```html
<div class="wg-cell wg-cell--default wg-cell--jump wg-cell--grey wg-cell--divider-full">
  <div class="wg-cell__body">
    <div class="wg-cell__content">
      <span class="wg-cell__title">灰色背景</span>
    </div>
  </div>
  <div class="wg-cell__action">
    <i class="wg-cell__arrow"></i>
  </div>
</div>
```

## Canonical CSS

```css
/* ===== Cell 容器 ===== */
.wg-cell {
  display: flex;
  align-items: center;
  min-block-size: var(--wg-size-56);
  padding-inline: var(--wg-spacing-16);
  background-color: var(--wg-color-bg-surface);
  position: relative;
  transition:
    background-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

/* 双行高度 */
.wg-cell--two-line {
  min-block-size: var(--wg-size-72);
}

/* 灰色背景 */
.wg-cell--grey {
  background-color: var(--wg-color-bg-page);
}

/* ===== 主体区域 ===== */
.wg-cell__body {
  display: flex;
  align-items: center;
  flex: 1 1 0;
  min-inline-size: 0;
  gap: var(--wg-spacing-12);
}

/* ===== 选择区 ===== */
.wg-cell__select {
  flex: 0 0 var(--wg-size-40);
  display: flex;
  align-items: center;
  justify-content: center;
}

.wg-cell__checkbox {
  appearance: none;
  inline-size: var(--wg-size-20);
  block-size: var(--wg-size-20);
  border: var(--wg-stroke-width-default) var(--wg-stroke-style-solid) var(--wg-color-border-default);
  border-radius: var(--wg-radius-sm);
  cursor: pointer;
  position: relative;
  flex-shrink: 0;
}

.wg-cell__checkbox:checked {
  background-color: var(--wg-color-action-primary-default);
  border-color: var(--wg-color-action-primary-default);
}

.wg-cell__checkbox:checked::after {
  content: "";
  position: absolute;
  inset: 0;
  background-color: var(--wg-color-text-inverse);
  -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
}

/* ===== 头像区 ===== */
.wg-cell__avatar {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wg-cell__avatar-img {
  inline-size: var(--wg-size-40);
  block-size: var(--wg-size-40);
  border-radius: var(--wg-radius-full);
  object-fit: cover;
}

.wg-cell__avatar-placeholder {
  inline-size: var(--wg-size-40);
  block-size: var(--wg-size-40);
  border-radius: var(--wg-radius-full);
  background-color: var(--wg-color-bg-page);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
  color: var(--wg-color-text-secondary);
}

/* ===== 内容区 ===== */
.wg-cell__content {
  display: flex;
  flex-direction: column;
  min-inline-size: 0;
  gap: var(--wg-spacing-4);
  flex: 1 1 0;
}

.wg-cell__title {
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.wg-cell__subtitle {
  font-size: var(--wg-font-size-12);
  line-height: var(--wg-font-lineheight-12);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ===== 操作区 ===== */
.wg-cell__action {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: var(--wg-spacing-4);
  margin-inline-start: var(--wg-spacing-12);
}

.wg-cell__action-text {
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-tertiary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 120px;
}

/* ===== 箭头图标 ===== */
.wg-cell__arrow {
  display: inline-block;
  inline-size: var(--wg-size-16);
  block-size: var(--wg-size-16);
  flex-shrink: 0;
  background-color: var(--wg-color-text-tertiary);
  -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z'/%3E%3C/svg%3E");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
}

/* ===== Switch 开关 ===== */
.wg-cell__switch {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.wg-cell__switch-input {
  position: absolute;
  opacity: 0;
  inline-size: 0;
  block-size: 0;
}

.wg-cell__switch-track {
  display: inline-block;
  inline-size: var(--wg-size-40);
  block-size: var(--wg-size-24);
  border-radius: var(--wg-radius-full);
  background-color: var(--wg-color-border-default);
  position: relative;
  transition:
    background-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-cell__switch-track::after {
  content: "";
  position: absolute;
  top: var(--wg-spacing-2);
  inset-inline-start: var(--wg-spacing-2);
  inline-size: var(--wg-size-20);
  block-size: var(--wg-size-20);
  border-radius: var(--wg-radius-full);
  background-color: var(--wg-color-bg-surface);
  transition:
    transform var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-cell__switch-input:checked + .wg-cell__switch-track {
  background-color: var(--wg-color-action-primary-default);
}

.wg-cell__switch-input:checked + .wg-cell__switch-track::after {
  transform: translateX(16px);
}

/* ===== 分割线 ===== */
.wg-cell--divider-full::after,
.wg-cell--divider-inset::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: var(--wg-spacing-16);
  block-size: var(--wg-stroke-width-hairline);
  background-color: var(--wg-color-divider-default);
}

.wg-cell--divider-full::after {
  right: 0;
}

.wg-cell--divider-inset::after {
  right: var(--wg-spacing-16);
}

/* ===== 按下态 ===== */
.wg-cell:not(.wg-cell--disabled):active {
  background-color: var(--wg-color-state-pressed);
}

.wg-cell--grey:not(.wg-cell--disabled):active {
  background-color: var(--wg-color-bg-page);
}

/* ===== 禁用态 ===== */
.wg-cell--disabled {
  cursor: not-allowed;
}

.wg-cell--disabled .wg-cell__title {
  color: var(--wg-color-text-disabled);
}

.wg-cell--disabled .wg-cell__subtitle {
  color: var(--wg-color-text-disabled);
}

.wg-cell--disabled .wg-cell__action-text {
  color: var(--wg-color-text-disabled);
}

.wg-cell--disabled .wg-cell__arrow {
  background-color: var(--wg-color-text-disabled);
}

/* ===== 焦点态 ===== */
.wg-cell:focus-visible {
  outline: none;
}

.wg-cell:focus-visible .wg-cell__body {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}
```

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 正常可用 |
| `pressed` | `:active` | 按下时背景变色，不位移、不缩放 |
| `disabled` | `.wg-cell--disabled` | 文字变浅，不响应点击 |

V1 未定义 `loading`、`badge`、`tag`、`icon-title` 视觉变体。遇到这些需求不得自行向 Cell 加入徽章、标签或标题图标；通过页面级样式实现，并标注组件能力缺失。

Cell 可点击时的状态要求：

- `default`：正常可用
- `hover`：仅桌面原型预览
- `active / pressed`：按下时背景变色，不位移、不缩放
- `disabled`：文字变浅，不响应点击

如果 Cell 承载错误提示，必须明确错误恢复规则；否则应改用 Form。

## 可访问性

- 跳转类 Cell 必须使用可交互元素（`<button>` 或 `<a>`）或添加 `role="button"` 和 `tabindex="0"`。
- Switch 必须使用原生 `<input type="checkbox">`，并通过 `<label>` 关联。
- 选择区复选框必须使用原生 `<input type="checkbox">`。
- 禁用状态必须使用 `.wg-cell--disabled` class，不能只降低透明度。
- 焦点顺序必须与视觉顺序一致。
- 禁止使用 `div`、`span` 模拟可交互元素。

## 生成约束

- 必须同时声明一个 `variant` class（`wg-cell--default` / `wg-cell--avatar` / `wg-cell--action`）和一个 `action` class（`wg-cell--jump` / `wg-cell--text` / `wg-cell--switch` / `wg-cell--button` / `wg-cell--custom`）。
- 必须声明一个 `divider` class（`wg-cell--divider-full` / `wg-cell--divider-inset`），不显示分割线时不添加 divider class。
- 双行 Cell 必须添加 `wg-cell--two-line` class。
- 不得覆盖 Cell 高度、字号、字重、颜色、圆角和间距。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 页面布局只控制 Cell 的位置和宽度，不控制 Cell 内部样式。
- 完整页面中出现 Cell 时，必须读取并遵守本文件。
- Canonical CSS 必须从本文件 `## Canonical CSS` 区块逐字复制到 `styles/components.css`，不得增删规则、修改选择器或添加属性。组件视觉行为只能通过规范中已声明的修饰符 class 调整。
- 同一个 Cell Group 内对齐方式必须一致，禁止左对齐和右对齐混用。
- 不允许用 Cell 伪装需要校验、错误提示、恢复状态的表单字段——应使用 Form。

## 自检

```text
□ 是否先判断 default / avatar / action 变体
□ 是否选择了正确的操作区类型（jump / text / switch / button / custom）
□ 是否选择了正确的分割线样式（full / inset / none）
□ 双行 Cell 是否添加了 --two-line class
□ 双行 Cell 是否提供了副标题
□ avatar 变体是否没有使用 switch 操作区
□ action 变体是否没有使用 switch 操作区
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ switch 是否使用原生 input[type="checkbox"]
□ disabled 是否使用 --disabled class
□ 是否没有自创 badge、tag、icon-title 变体
□ 同一 Cell Group 内对齐方式是否一致
□ 是否没有用 Cell 伪装复杂表单字段
□ 可点击 Cell 是否覆盖 default / pressed / disabled 状态
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `586:134408`（Cell _ 列表）。提取三个变体（Cell / Cell_Avatar / Cell_Action）的使用场景规则、命名表和布局结构。
- Kuikly `Cell`：参考四区域布局（选择区 36px → 头像区 + 12px 间距 → 内容区 flex 1 → 操作区）、五种操作区类型（JUMP_TO / TEXT / SWITCH / BUTTON / CUSTOM）、分割线三态、颜色预设（WHITE / GREY）、点击态行为和宽度优先级规则；不继承 Kuikly DSL、退格区（showBackSpace）、标题图标（titleIcon）、标题自定义内容（titleCustomContent）、副标题自定义富文本（subtitleCustomContent）、操作区自定义内容（actionCustomContent）、徽章（Badge）、ViewBuilder 插槽或高级配置。
