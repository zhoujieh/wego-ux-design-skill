# Toast

Toast 页面底部浮层轻量反馈，用于展示操作结果或简短提示，自动消失、不打断用户流程。本规则首先判断反馈类型（成功 / 失败 / 引导），再映射视觉样式。

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

使用 Toast：

- 操作后的轻量反馈，如保存成功、提交失败。
- 无需用户决策的简短提示信息。
- 页面内操作后的即时状态确认。
- 带引导操作的提示，如"已加入清单，去查看"。

不使用 Toast：

- 需要用户确认或决策的关键操作：使用 Dialog。
- 底部多选项列表：使用 ActionSheet。
- 页面内轻量反馈但不自动消失：使用页面内 Alert 或 Banner。
- 顶部消息推送：使用 Push。
- 加载中状态：使用 Loading。

## 语义模型

Toast 有三个决策维度：

```text
variant   反馈类型
action    引导操作
state     当前交互状态
```

### Variant

| Variant | 含义 | 结构 | 场景说明 | 规则 | 应用实例 |
|---|---|---|---|---|---|
| `default` | 基础 Toast | 图标（可选）+ 文案 | 操作后轻反馈 | 文本尽量不超过 8 个字，严格限制在 1 行以内；轻型操作的反馈，不强调结果；默认不使用图标，若需强调结果成功失败则带上【勾】【叉】【感叹号】 | 刷新图文位置 |
| `action` | 带操作的 Toast | 图标（可选）+ 文案 + 引导按钮 | 操作后有额外引导操作、重要反馈 | 根据与当前反馈内容相关性强弱，强的用高亮文字按钮，弱的用跳转；伴随页面级跳转时，反馈信息需足够明显可见，即使不带操作也使用长条形 toast | 下载图片；小程序引导批量下载 |

禁止让 AI 直接根据"有图标/无图标"选择变体。必须先判断反馈目的。

### Action

| Action | 含义 | 规则 |
|---|---|---|
| `none` | 无引导操作 | 仅展示反馈文案，自动消失 |
| `weak` | 弱引导操作 | 引导按钮使用次要样式，可点击跳转 |
| `strong` | 强引导操作 | 引导按钮使用主要样式，可点击跳转 |

仅 `action` 变体支持引导操作。`default` 变体不得添加引导按钮。

### State

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `visible` | `data-state="visible"` | Toast 可见，从底部滑入 |
| `hidden` | `data-state="hidden"` | Toast 隐藏，淡出动画 |

## 允许组合

| Variant | none | weak | strong |
|---|---|---|---|
| `default` | 允许 | 不允许 | 不允许 |
| `action` | 不允许 | 允许 | 允许 |

附加规则：

- 同一时刻只允许显示一个 Toast（单例模式）。
- 新 Toast 出现时，旧 Toast 必须立即消失。
- Toast 必须自动消失，默认时长 4000ms。
- 引导按钮文案不超过 4 个字符。

## Anatomy

通用结构：

```text
div.wg-toast-container[data-state]
└── div.wg-toast.wg-toast--{variant}
    ├── i.wg-toast__icon.wg-toast__icon--{success|error|info}（可选）
    ├── span.wg-toast__message
    └── button.wg-toast__action.wg-toast__action--{weak|strong}（仅 action 变体）
```

各变体差异：

- `default`：有 `span.wg-toast__message`，可选 `i.wg-toast__icon`，无 `button.wg-toast__action`
- `action`：有 `span.wg-toast__message` + `button.wg-toast__action`，可选 `i.wg-toast__icon`

## 文案规则

- 文案使用简短明确的短语，如"保存成功""提交失败""已加入清单"。
- 文案单行展示，不换行；超长时截断显示省略号。
- 成功文案不超过 6 个字符。
- 失败文案不超过 8 个字符。
- 引导文案不超过 10 个字符。
- 引导按钮文案使用动词，如"查看""去使用""立即查看"。
- 引导按钮文案不超过 4 个字符。
- 同一 Toast 内文案使用一致的语气。

## Canonical HTML

`default` 变体 — 无图标：

```html
<div class="wg-toast-container" data-state="visible">
  <div class="wg-toast wg-toast--default" role="status" aria-live="polite">
    <span class="wg-toast__message">刷新图文位置</span>
  </div>
</div>
```

`default` 变体 — 带图标（强调结果）：

```html
<div class="wg-toast-container" data-state="visible">
  <div class="wg-toast wg-toast--default" role="status" aria-live="polite">
    <i class="wg-toast__icon wg-toast__icon--success"></i>
    <span class="wg-toast__message">保存成功</span>
  </div>
</div>
```

`action` 变体 — 弱引导操作：

```html
<div class="wg-toast-container" data-state="visible">
  <div class="wg-toast wg-toast--action" role="status" aria-live="polite">
    <span class="wg-toast__message">已加入清单</span>
    <button class="wg-toast__action wg-toast__action--weak" type="button">查看</button>
  </div>
</div>
```

`action` 变体 — 强引导操作：

```html
<div class="wg-toast-container" data-state="visible">
  <div class="wg-toast wg-toast--action" role="status" aria-live="polite">
    <span class="wg-toast__message">下载图片成功</span>
    <button class="wg-toast__action wg-toast__action--strong" type="button">去查看</button>
  </div>
</div>
```

## Canonical CSS

```css
/* ── Container ── */
.wg-toast-container {
  position: fixed;
  inset-inline: 0;
  block-end: calc(var(--wg-spacing-72) + env(safe-area-inset-bottom));
  z-index: var(--wg-zindex-toast);
  display: flex;
  justify-content: center;
  pointer-events: none;
  transition:
    opacity var(--wg-motion-duration-normal) var(--wg-motion-ease-standard),
    transform var(--wg-motion-duration-normal) var(--wg-motion-ease-emphasized);
}

.wg-toast-container[data-state="hidden"] {
  opacity: 0;
  transform: translateY(var(--wg-spacing-16));
}

/* ── Toast Card ── */
.wg-toast {
  display: inline-flex;
  align-items: center;
  gap: var(--wg-spacing-8);
  padding: var(--wg-spacing-12) var(--wg-spacing-16);
  background-color: var(--wg-color-bg-toast);
  border-radius: var(--wg-radius-lg);
  box-shadow: var(--wg-shadow-md);
  pointer-events: auto;
  max-inline-size: min(320px, 90vw);
}

/* ── Icon ── */
.wg-toast__icon {
  display: inline-block;
  inline-size: var(--wg-size-20);
  block-size: var(--wg-size-20);
  flex-shrink: 0;
  border-radius: var(--wg-radius-full);
}

.wg-toast__icon--success {
  background-color: var(--wg-color-status-success-default);
}

.wg-toast__icon--error {
  background-color: var(--wg-color-status-danger-default);
}

.wg-toast__icon--info {
  background-color: var(--wg-color-status-info-default);
}

/* ── Message ── */
.wg-toast__message {
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-inverse);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 100%;
}

/* ── Action Button ── */
.wg-toast__action {
  appearance: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--wg-spacing-4) var(--wg-spacing-8);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  cursor: pointer;
  font-family: var(--wg-font-family-text);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-medium);
  white-space: nowrap;
  flex-shrink: 0;
  transition:
    opacity var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-toast__action--weak {
  color: var(--wg-color-text-inverse-secondary);
}

.wg-toast__action--strong {
  color: var(--wg-color-action-primary-default);
}

.wg-toast__action:not(:disabled):active {
  opacity: 0.6;
}

.wg-toast__action:focus-visible {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: calc(-1 * var(--wg-spacing-2));
}

.wg-toast__action:disabled {
  cursor: not-allowed;
  color: var(--wg-color-text-disabled);
}
```

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `visible` | `data-state="visible"` | Toast 可见，从底部滑入 |
| `hidden` | `data-state="hidden"` | Toast 隐藏，淡出动画 |
| `pressed` | `:active`（引导按钮） | 按下时透明度 0.6，不位移、不缩放 |
| `focus-visible` | `:focus-visible`（引导按钮） | 必须显示清晰焦点描边 |
| `disabled` | `disabled`（引导按钮） | 统一使用禁用文字色，不响应操作 |

V1 未定义 `loading`、`stacking` 视觉变体。多 Toast 时采用单例模式，新 Toast 替换旧 Toast。文案超长时截断显示省略号，不得自行添加滚动区域；标注组件能力缺失。

## 可访问性

- 必须使用 `role="status"` 和 `aria-live="polite"`。
- 引导按钮必须使用原生 `<button>`。
- 禁用状态必须使用 `disabled` 属性，不能只降低透明度。
- Toast 不得抢夺焦点，不得影响键盘导航。
- 禁止使用 `div`、`span` 模拟可点击按钮。

## 生成约束

- 必须同时声明一个 `variant` class。
- 必须使用 `wg-toast-container`、`wg-toast`、`wg-toast__icon`、`wg-toast__message`。
- 不得覆盖 Toast 位置、内边距、圆角和阴影。
- 不得覆盖图标尺寸、字号和颜色。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 不得新增 `warning`、`info` 等未定义的变体。
- 页面脚本可以控制 Toast 的显示/隐藏和引导按钮回调，但不得绕过组件规定的 Anatomy、状态语义和可访问性约束。
- 完整页面中出现 Toast 时，必须读取并遵守本文件。

## 自检

```text
□ 是否先判断反馈目的 → default / action
□ 是否只存在一个 variant
□ 是否遵守 none / weak / strong 引导操作组合
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 是否使用原生 button 和正确 type（引导按钮）
□ 是否设置 role="status" 和 aria-live="polite"
□ disabled 是否使用原生属性
□ 是否没有自创 loading、warning 变体
□ 是否保证单例模式（同时只有一个 Toast）
□ 是否设置自动消失时长
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `75:55812`。提取 Toast（基础反馈）和 Toast_Action（带操作反馈）两种变体的结构、尺寸、间距和引导按钮规则。
- Kuikly `Toast`：参考 BaseVisuals 的 showSimpleSuccessToast、showFailedToast、showGuideToast 方法设计（变体类型、自动关闭时长、冲突控制、引导按钮样式）；不继承 Kuikly DSL、DialogUtil 管理方式、ActionButtonStyle 枚举、IconPresets 机制。
