# ActionSheet

ActionSheet 用于底部弹出一组操作或选项，底部带固定"取消"按钮。本规则首先判断交互模式（操作 / 选择），再选择头部布局和选项类型。

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

使用 ActionSheet：

- 底部弹出一组并列操作，如分享、复制、删除。
- 底部弹出单选列表，如排序方式、筛选条件。
- 需要明确取消入口的操作集合。

不使用 ActionSheet：

- 相对目标视图弹出的下拉菜单：使用 PopOver 或 PopViewSelect。
- 确认 / 警告 / 提示弹窗：使用 Dialog。
- 页面内嵌的选项列表：使用 List 或 Cell。

## 语义模型

ActionSheet 有四个决策维度：

```text
mode      交互模式
header    头部布局
itemType  选项类型
state     当前交互状态
```

### Mode

| Mode | 应用场景 | 文本对齐 | 选中指示 |
|---|---|---|---|
| `action` | 并列操作按钮组（分享 / 复制 / 删除） | 居中 | 无 |
| `select` | 单选切换（筛选 / 排序） | 左对齐 | 选中项右侧绿色对勾 |

禁止让 AI 直接根据"有没有勾选"选择模式。必须先判断交互目的：执行操作用 `action`，单选切换用 `select`。

### Header

| Header | 含义 | 布局 |
|---|---|---|
| `none` | 无头部描述 | 无 |
| `simple` | 纯描述文本 | 文本居中 |
| `with-icon` | 图标 + 描述文本 | 图标 + 文本整体居中 |
| `with-link` | 描述 + 右侧链接 | 左边（图标 + 文本）+ 右边（链接），两端对齐 |

### ItemType

| ItemType | 应用场景 | 行高 |
|---|---|---|
| `single` | 纯文本或图标 + 文本 | `wg.size.56` |
| `multi` | 主标题 + 副标题 | `wg.size.72` |

## 允许组合

| Mode | Header | ItemType | 说明 |
|---|---|---|---|
| `action` | `none` | `single` | 最简操作列表 |
| `action` | `simple` | `single` | 带描述的操作列表 |
| `action` | `with-icon` | `single` | 头部带图标的操作列表 |
| `action` | `with-link` | `single` | 头部带链接的操作列表 |
| `action` | `none` | `multi` | 带副标题的操作列表 |
| `select` | `none` | `single` | 最简选择列表 |
| `select` | `simple` | `single` | 带描述的选择列表 |

附加规则：

- `select` 模式下文本强制左对齐，不得使用居中。
- `select` 模式下必须有且仅有一个 `selected` 项。
- `action` 模式下不得出现选中指示（绿色对勾）。
- 同一 ActionSheet 内所有选项的 `itemType` 必须一致。
- 选项数量建议 2–6 个；超过 6 个时应考虑使用其他组件。

## Anatomy

操作模式 + 单行 + 无头部：

```text
div.wg-actionsheet
├── div.wg-actionsheet__overlay
└── div.wg-actionsheet__panel.wg-actionsheet__panel--action
    ├── div.wg-actionsheet__list
    │   ├── button.wg-actionsheet__item
    │   │   └── span.wg-actionsheet__item-title
    │   └── button.wg-actionsheet__item
    │       └── span.wg-actionsheet__item-title
    ├── div.wg-actionsheet__separator
    └── button.wg-actionsheet__cancel
        └── span.wg-actionsheet__cancel-text
```

操作模式 + 单行有 icon + 带头部：

```text
div.wg-actionsheet
├── div.wg-actionsheet__overlay
└── div.wg-actionsheet__panel.wg-actionsheet__panel--action
    ├── div.wg-actionsheet__header
    │   ├── i.wg-actionsheet__header-icon
    │   └── span.wg-actionsheet__header-text
    ├── div.wg-actionsheet__list
    │   └── button.wg-actionsheet__item
    │       ├── i.wg-actionsheet__item-icon
    │       └── span.wg-actionsheet__item-title
    ├── div.wg-actionsheet__separator
    └── button.wg-actionsheet__cancel
        └── span.wg-actionsheet__cancel-text
```

选择模式 + 单行：

```text
div.wg-actionsheet
├── div.wg-actionsheet__overlay
└── div.wg-actionsheet__panel.wg-actionsheet__panel--select
    ├── div.wg-actionsheet__header
    │   └── span.wg-actionsheet__header-text
    ├── div.wg-actionsheet__list
    │   ├── button.wg-actionsheet__item[aria-selected="true"]
    │   │   ├── span.wg-actionsheet__item-title
    │   │   └── i.wg-actionsheet__item-check
    │   └── button.wg-actionsheet__item[aria-selected="false"]
    │       ├── span.wg-actionsheet__item-title
    │       └── i.wg-actionsheet__item-check
    ├── div.wg-actionsheet__separator
    └── button.wg-actionsheet__cancel
        └── span.wg-actionsheet__cancel-text
```

V1 仅允许文字选项或图标 + 文字选项。不得自行加入徽章、推荐标签、副标题或自定义 slot 内容；这些作为 V1 能力缺失标注。

## 文案规则

- 选项文本使用动词或动宾短语，如"拍照""从相册选择""分享给好友"。
- 取消按钮固定文案为"取消"，不得修改。
- 头部描述简短说明操作目的，如"请选择图片来源""排序方式"。
- 头部链接使用简短动词，如"查看帮助""了解更多"。
- 所有文本单行展示，不换行。
- 同一 ActionSheet 内选项文案使用一致的语法结构。

## Canonical HTML

操作模式 + 单行 + 无头部：

```html
<div class="wg-actionsheet" role="dialog" aria-modal="true" aria-label="操作选项">
  <div class="wg-actionsheet__overlay"></div>
  <div class="wg-actionsheet__panel wg-actionsheet__panel--action">
    <div class="wg-actionsheet__list">
      <button class="wg-actionsheet__item" type="button">
        <span class="wg-actionsheet__item-title">拍照</span>
      </button>
      <button class="wg-actionsheet__item" type="button">
        <span class="wg-actionsheet__item-title">从相册选择</span>
      </button>
    </div>
    <div class="wg-actionsheet__separator"></div>
    <button class="wg-actionsheet__cancel" type="button">
      <span class="wg-actionsheet__cancel-text">取消</span>
    </button>
  </div>
</div>
```

操作模式 + 单行有 icon + 带头部：

```html
<div class="wg-actionsheet" role="dialog" aria-modal="true" aria-label="更多操作">
  <div class="wg-actionsheet__overlay"></div>
  <div class="wg-actionsheet__panel wg-actionsheet__panel--action">
    <div class="wg-actionsheet__header">
      <i class="wg-actionsheet__header-icon wego-iconfont-s icon-xiangji"></i>
      <span class="wg-actionsheet__header-text">请选择图片来源</span>
    </div>
    <div class="wg-actionsheet__list">
      <button class="wg-actionsheet__item" type="button">
        <i class="wg-actionsheet__item-icon wego-iconfont-s icon-fenxiang"></i>
        <span class="wg-actionsheet__item-title">分享给好友</span>
      </button>
      <button class="wg-actionsheet__item" type="button">
        <i class="wg-actionsheet__item-icon wego-iconfont-s icon-fuzhi"></i>
        <span class="wg-actionsheet__item-title">复制链接</span>
      </button>
      <button class="wg-actionsheet__item" type="button">
        <i class="wg-actionsheet__item-icon wego-iconfont-s icon-shoucang"></i>
        <span class="wg-actionsheet__item-title">收藏</span>
      </button>
    </div>
    <div class="wg-actionsheet__separator"></div>
    <button class="wg-actionsheet__cancel" type="button">
      <span class="wg-actionsheet__cancel-text">取消</span>
    </button>
  </div>
</div>
```

选择模式 + 单行：

```html
<div class="wg-actionsheet" role="dialog" aria-modal="true" aria-label="排序方式">
  <div class="wg-actionsheet__overlay"></div>
  <div class="wg-actionsheet__panel wg-actionsheet__panel--select">
    <div class="wg-actionsheet__header">
      <span class="wg-actionsheet__header-text">排序方式</span>
    </div>
    <div class="wg-actionsheet__list">
      <button class="wg-actionsheet__item" type="button" aria-selected="true">
        <span class="wg-actionsheet__item-title">按时间排序</span>
        <i class="wg-actionsheet__item-check"></i>
      </button>
      <button class="wg-actionsheet__item" type="button" aria-selected="false">
        <span class="wg-actionsheet__item-title">按热度排序</span>
        <i class="wg-actionsheet__item-check"></i>
      </button>
      <button class="wg-actionsheet__item" type="button" aria-selected="false">
        <span class="wg-actionsheet__item-title">按点赞数排序</span>
        <i class="wg-actionsheet__item-check"></i>
      </button>
    </div>
    <div class="wg-actionsheet__separator"></div>
    <button class="wg-actionsheet__cancel" type="button">
      <span class="wg-actionsheet__cancel-text">取消</span>
    </button>
  </div>
</div>
```

头部带链接：

```html
<div class="wg-actionsheet__header wg-actionsheet__header--with-link">
  <span class="wg-actionsheet__header-text">请选择一项</span>
  <button class="wg-actionsheet__header-link" type="button">查看帮助</button>
</div>
```

## Canonical CSS

```css
/* ===== 遮罩层 ===== */
.wg-actionsheet {
  position: fixed;
  inset: 0;
  z-index: var(--wg-zindex-modal);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.wg-actionsheet__overlay {
  position: absolute;
  inset: 0;
  background-color: var(--wg-color-overlay-modal);
}

/* ===== 面板 ===== */
.wg-actionsheet__panel {
  position: relative;
  display: flex;
  flex-direction: column;
  background-color: var(--wg-color-bg-surface);
  border-radius: var(--wg-radius-xl) var(--wg-radius-xl) 0 0;
  padding-top: var(--wg-spacing-4);
  max-block-size: 70vh;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

/* ===== 头部描述区 ===== */
.wg-actionsheet__header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--wg-spacing-8);
  padding: var(--wg-spacing-12) var(--wg-spacing-16);
}

.wg-actionsheet__header-icon {
  font-size: var(--wg-size-20);
  color: var(--wg-color-text-secondary);
}

.wg-actionsheet__header-text {
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-secondary);
  white-space: nowrap;
}

.wg-actionsheet__header--with-link {
  justify-content: space-between;
}

.wg-actionsheet__header-link {
  appearance: none;
  border: none;
  background: transparent;
  padding: 0;
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-link);
  cursor: pointer;
  white-space: nowrap;
}

/* ===== 选项列表 ===== */
.wg-actionsheet__list {
  display: flex;
  flex-direction: column;
  padding: var(--wg-spacing-8) var(--wg-spacing-12);
}

/* ===== 选项项 ===== */
.wg-actionsheet__item {
  appearance: none;
  display: flex;
  align-items: center;
  gap: var(--wg-spacing-8);
  block-size: var(--wg-size-56);
  padding-inline: var(--wg-spacing-12);
  border: none;
  background-color: var(--wg-color-bg-surface);
  border-radius: var(--wg-radius-md);
  cursor: pointer;
  position: relative;
  transition:
    background-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

/* 操作模式：文本居中 */
.wg-actionsheet__panel--action .wg-actionsheet__item {
  justify-content: center;
}

/* 选择模式：文本左对齐 */
.wg-actionsheet__panel--select .wg-actionsheet__item {
  justify-content: flex-start;
}

/* 选项图标 */
.wg-actionsheet__item-icon {
  font-size: var(--wg-size-24);
  color: var(--wg-color-text-primary);
  flex-shrink: 0;
}

/* 选项标题 */
.wg-actionsheet__item-title {
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 选择模式选中项标题加粗 */
.wg-actionsheet__panel--select .wg-actionsheet__item[aria-selected="true"] .wg-actionsheet__item-title {
  font-weight: var(--wg-font-weight-medium);
}

/* 选项分割线 */
.wg-actionsheet__item + .wg-actionsheet__item::after {
  content: "";
  position: absolute;
  top: 0;
  left: var(--wg-spacing-12);
  right: var(--wg-spacing-12);
  block-size: var(--wg-stroke-width-hairline);
  background-color: var(--wg-color-divider-default);
}

/* 选中指示（绿色对勾） */
.wg-actionsheet__item-check {
  display: none;
  margin-inline-start: auto;
  flex-shrink: 0;
}

.wg-actionsheet__panel--select .wg-actionsheet__item-check {
  display: block;
  inline-size: var(--wg-size-20);
  block-size: var(--wg-size-20);
}

.wg-actionsheet__panel--select .wg-actionsheet__item[aria-selected="true"] .wg-actionsheet__item-check {
  background-color: var(--wg-color-base-accent-green-500);
  -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
}

.wg-actionsheet__panel--select .wg-actionsheet__item[aria-selected="false"] .wg-actionsheet__item-check {
  background-color: transparent;
}

/* ===== 分割区 ===== */
.wg-actionsheet__separator {
  block-size: var(--wg-spacing-8);
  background-color: var(--wg-color-bg-page);
}

/* ===== 取消按钮 ===== */
.wg-actionsheet__cancel {
  appearance: none;
  display: flex;
  align-items: center;
  justify-content: center;
  block-size: var(--wg-size-56);
  padding-inline: var(--wg-spacing-12);
  border: none;
  background-color: var(--wg-color-bg-surface);
  cursor: pointer;
  transition:
    background-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-actionsheet__cancel-text {
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-primary);
  text-align: center;
  inline-size: 100%;
}

/* ===== 安全区 ===== */
.wg-actionsheet__safe-area {
  /* Token 缺失：--wg-size-34 不存在，使用硬编码值 */
  block-size: 34px;
  background-color: var(--wg-color-bg-surface);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-block-end: var(--wg-spacing-8);
}

.wg-actionsheet__safe-area::after {
  content: "";
  display: block;
  inline-size: 134px;
  block-size: 5px;
  background-color: var(--wg-color-text-primary);
  border-radius: var(--wg-radius-full);
}

/* ===== 状态 ===== */

/* 按下态 */
.wg-actionsheet__item:not(:disabled):active {
  background-color: var(--wg-color-state-pressed);
}

.wg-actionsheet__cancel:active {
  background-color: var(--wg-color-state-pressed);
}

/* 禁用态 */
.wg-actionsheet__item:disabled {
  cursor: not-allowed;
}

.wg-actionsheet__item:disabled .wg-actionsheet__item-title {
  color: var(--wg-color-text-disabled);
}

.wg-actionsheet__item:disabled .wg-actionsheet__item-icon {
  color: var(--wg-color-text-disabled);
}

/* 焦点态 */
.wg-actionsheet__item:focus-visible {
  outline: none;
}

.wg-actionsheet__item:focus-visible .wg-actionsheet__item-title {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}

.wg-actionsheet__cancel:focus-visible {
  outline: none;
}

.wg-actionsheet__cancel:focus-visible .wg-actionsheet__cancel-text {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}

.wg-actionsheet__header-link:focus-visible {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}
```

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 正常可用 |
| `pressed` | `:active` | 选项和取消按钮按下时背景变色，不位移、不缩放 |
| `disabled` | `disabled` | 选项禁用：文本变浅，不响应点击 |
| `selected` | `aria-selected="true"` | 仅 `select` 模式：选中项文字加粗 + 右侧绿色对勾 |

V1 未定义 `loading`、`badge`、`recommendation`、`subtitle` 视觉变体。遇到这些需求不得自行向 ActionSheet 加入徽章、推荐标签或副标题；通过页面级样式实现，并标注组件能力缺失。

## 可访问性

- 必须使用 `role="dialog"` 和 `aria-modal="true"` 作为弹窗容器。
- 必须提供 `aria-label` 描述弹窗用途。
- 选项必须使用原生 `<button>`。
- 选择模式下选中项必须设置 `aria-selected="true"`，未选中设置为 `aria-selected="false"`。
- 禁用状态必须使用 `disabled` 属性，不能只降低透明度。
- 取消按钮必须使用原生 `<button>`。
- 焦点顺序：从上到下，最后到取消按钮。
- 禁止使用 `div`、`span` 模拟可点击选项。

## 生成约束

- 必须同时声明一个 `mode` class（`wg-actionsheet__panel--action` 或 `wg-actionsheet__panel--select`）。
- `select` 模式下必须有且仅有一个 `aria-selected="true"` 的选项。
- `action` 模式下不得出现 `wg-actionsheet__item-check`。
- 不得覆盖选项高度、字号、字重、圆角、分割线颜色和间距。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 页面布局只控制 ActionSheet 的显示/隐藏，不控制面板内部样式。
- 完整页面中出现 ActionSheet 时，必须读取并遵守本文件。

## 自检

```text
□ 是否先判断操作 / 选择 → action / select
□ action 模式下选项文本是否居中
□ select 模式下选项文本是否左对齐
□ select 模式下是否有且仅有一个 aria-selected="true"
□ action 模式下是否没有选中指示
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 每个选项是否使用原生 button
□ disabled 是否使用原生属性
□ 取消按钮文案是否为"取消"
□ 是否没有自创 badge、recommendation、subtitle 变体
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `522:51546`（Actionsheet _ 选择面板）。提取操作模式和选择模式的选项高度、字号、颜色、分割线、取消按钮和头部布局。
- Kuikly `ActionSheet`：参考两种调用方式（showActionSheet / showActionSheetSelect）、头部描述区三种布局、选项数据结构（图标 / 副标题 / 徽章 / 推荐标签 / 禁用态）、自动关闭行为和底部安全区适配；不继承 Kuikly DSL、DialogContainer 依赖、自定义前景/背景 View 或高级配置。
