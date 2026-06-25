# Loading

Loading 加载指示组件，用于在数据加载、内容刷新、操作等待等场景中向用户反馈当前状态。本规则首先判断加载场景（下拉刷新 / 页面加载 / 模态加载 / 局部加载 / 骨架屏 / 图片占位），再映射视觉变体。

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

使用 Loading：

- 用户通过手势下拉列表触发的刷新操作，用于更新当前页面内容：使用 `spinner` 变体（`lg` 尺寸）。
- 整个页面的内容加载过程中展示的全屏加载状态，用户无法交互：使用 `spinner` 变体（`sm` 尺寸）居中展示。
- 等待判断以决定后续表现，判断过程中不许新增操作（模态加载）：使用 `modal` 变体。
- 页面中某个区域的内容加载或刷新状态：使用 `spinner` 变体（`sm` 尺寸）。
- 加载时间较长，且结构复杂但重复的页面：使用 `skeleton` 变体。
- 在图片加载过程中展示的默认占位状态，防止页面出现空白区域：使用 `image` 变体。

不使用 Loading：

- 操作后的轻量反馈（成功/失败）：使用 Toast。
- 需要用户确认或决策的关键操作：使用 Dialog。
- 底部多选项列表：使用 ActionSheet。
- 非加载状态的空页面：使用 Result。

### 场景与变体映射

| 场景 | 变体 | 尺寸 | 说明 |
|---|---|---|---|
| 下拉刷新 | `spinner` | `lg`（48px） | 列表型内容、消息流、商品推荐页等需要实时刷新内容的场景 |
| 页面加载 | `spinner` | `sm`（24px） | 页面首次进入、内容切换、全局网络请求等场景；加载完成前不可交互 |
| 模态加载 | `modal` | — | 需要先准备好数据后再进行跳转或变更状态的场景；加载完成前不可操作 |
| 局部加载 | `spinner` | `sm`（24px） | 表单提交后的状态刷新、列表筛选后的内容加载等 |
| 骨架屏加载 | `skeleton` | — | 加载时间较长，且结构复杂但重复的页面，如店铺、商品详情页 |
| 图片占位加载 | `image` | — | 图片较多或加载延迟明显的页面，如商品缩略图、用户头像等 |

### 模态加载补充规则

- 模态加载期间，用户不可操作页面内容。
- 如果能明确等待进度，应使用带进度样式（V1 未定义进度变体，标注组件能力缺失）。
- 若加载是为了等待结果，则还需要在加载完成时进行结果反馈，切换内容或跳转到结果页。
- 模态加载不会自动关闭，需要由业务逻辑手动控制关闭时机。

### 骨架屏加载补充规则

- 结构不复杂的页面，骨架色块大且不美观，不宜使用骨架屏。
- 使用骨架加载目的在于给人更高效的感觉，且对页面内容能有预知。
- 骨架屏的色块形状应与实际内容布局一致。

## 语义模型

Loading 有三个决策维度：

```text
variant   加载类型
size      旋转指示器尺寸（仅 spinner 变体）
state     当前交互状态
```

### Variant

| Variant | 含义 | 结构 | 场景说明 | 规则 |
|---|---|---|---|---|
| `spinner` | 旋转指示器 | 旋转圆环 | 下拉刷新、页面加载、局部加载 | 根据场景选择尺寸：下拉刷新用 `lg`（48px），页面/局部加载用 `sm`（24px）；居中放置于加载区域 |
| `modal` | 模态加载浮层 | 深色半透明容器 + 旋转图标 + 可选文案 | 模态加载 | 居中浮层，加载完成前不可操作；不会自动关闭，需业务逻辑控制 |
| `skeleton` | 骨架屏占位 | 灰色色块组合 | 骨架屏加载 | 色块形状与实际内容布局一致；仅用于结构复杂且重复的页面 |
| `image` | 图片占位 | 默认图片图标 | 图片占位加载 | 防止图片加载期间出现空白区域；图片加载完成后替换为实际图片 |

禁止让 AI 直接根据"有动画/无动画"选择变体。必须先判断加载场景。

### Size

| Size | 含义 | 规则 |
|---|---|---|
| `lg` | 大尺寸（48px） | 仅用于下拉刷新场景 |
| `sm` | 小尺寸（24px） | 用于页面加载、局部加载场景 |

仅 `spinner` 变体支持 `size` 维度。其他变体不得添加 `size` 修饰符。

### State

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `visible` | `data-state="visible"` | 加载指示器可见 |
| `hidden` | `data-state="hidden"` | 加载指示器隐藏，淡出动画 |

## 允许组合

| Variant | lg | sm | 无 size |
|---|---|---|---|
| `spinner` | 允许 | 允许 | 不允许 |
| `modal` | 不允许 | 不允许 | 允许 |
| `skeleton` | 不允许 | 不允许 | 允许 |
| `image` | 不允许 | 不允许 | 允许 |

附加规则：

- 同一区域同一时刻只允许显示一个 Loading 指示器。
- `modal` 变体与 Toast 会互相冲突——显示 Toast 会关闭先前的 modal Loading，反之亦然。
- `spinner` 变体不得与 `modal` 变体在同一区域同时使用。
- `skeleton` 变体应覆盖整个待加载区域，不得只覆盖部分内容。
- `image` 变体仅在图片加载期间显示，图片加载完成后必须移除。

## Anatomy

通用结构：

```text
div.wg-loading.wg-loading--{variant}[data-state]
├──（spinner 变体）div.wg-loading__spinner.wg-loading__spinner--{size}
├──（modal 变体）div.wg-loading__overlay
│   └── div.wg-loading__toast
│       ├── div.wg-loading__spinner.wg-loading__spinner--sm
│       └── span.wg-loading__text（可选）
├──（skeleton 变体）div.wg-loading__skeleton
│   ├── div.wg-loading__skeleton-block（可重复）
│   └── ...
└──（image 变体）div.wg-loading__image
    └── i.wg-loading__image-icon
```

各变体差异：

- `spinner`：仅有 `div.wg-loading__spinner`，无文案，无遮罩
- `modal`：有 `div.wg-loading__overlay` 遮罩 + `div.wg-loading__toast` 容器 + 旋转图标 + 可选文案
- `skeleton`：有 `div.wg-loading__skeleton`，内含多个 `div.wg-loading__skeleton-block`，色块形状由页面布局决定
- `image`：有 `div.wg-loading__image`，内含 `i.wg-loading__image-icon` 占位图标

## 文案规则

- 仅 `modal` 变体支持文案，其他变体不得添加文案。
- 文案使用简短明确的短语，如"加载中...""提交中...""处理中..."。
- 文案单行展示，不换行；超长时截断显示省略号。
- 文案不超过 8 个字符。
- 文案使用省略号结尾表示进行中状态，如"加载中..."。

## Canonical HTML

`spinner` 变体 — `lg` 尺寸（下拉刷新）：

```html
<div class="wg-loading wg-loading--spinner wg-loading--lg" data-state="visible" role="status" aria-live="polite">
  <div class="wg-loading__spinner wg-loading__spinner--lg"></div>
</div>
```

`spinner` 变体 — `sm` 尺寸（页面加载/局部加载）：

```html
<div class="wg-loading wg-loading--spinner wg-loading--sm" data-state="visible" role="status" aria-live="polite">
  <div class="wg-loading__spinner wg-loading__spinner--sm"></div>
</div>
```

`modal` 变体 — 无文案：

```html
<div class="wg-loading wg-loading--modal" data-state="visible" role="status" aria-live="polite">
  <div class="wg-loading__overlay">
    <div class="wg-loading__toast">
      <div class="wg-loading__spinner wg-loading__spinner--sm"></div>
    </div>
  </div>
</div>
```

`modal` 变体 — 带文案：

```html
<div class="wg-loading wg-loading--modal" data-state="visible" role="status" aria-live="polite">
  <div class="wg-loading__overlay">
    <div class="wg-loading__toast">
      <div class="wg-loading__spinner wg-loading__spinner--sm"></div>
      <span class="wg-loading__text">加载中...</span>
    </div>
  </div>
</div>
```

`skeleton` 变体：

```html
<div class="wg-loading wg-loading--skeleton" data-state="visible" role="status" aria-live="polite">
  <div class="wg-loading__skeleton">
    <div class="wg-loading__skeleton-block wg-loading__skeleton-block--rect"></div>
    <div class="wg-loading__skeleton-block wg-loading__skeleton-block--circle"></div>
    <div class="wg-loading__skeleton-block wg-loading__skeleton-block--line"></div>
  </div>
</div>
```

`image` 变体：

```html
<div class="wg-loading wg-loading--image" data-state="visible" role="status" aria-live="polite">
  <div class="wg-loading__image">
    <i class="wg-loading__image-icon"></i>
  </div>
</div>
```

## Canonical CSS

```css
/* ── Base ── */
.wg-loading {
  display: flex;
  align-items: center;
  justify-content: center;
}

.wg-loading[data-state="hidden"] {
  display: none;
}

/* ── Spinner ── */
.wg-loading__spinner {
  border-radius: var(--wg-radius-full);
  border: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-border-loading-track);
  border-block-start-color: var(--wg-color-border-loading-indicator);
  animation: wg-spin var(--wg-motion-duration-slow) linear infinite;
}

.wg-loading__spinner--lg {
  inline-size: var(--wg-size-48);
  block-size: var(--wg-size-48);
  border-width: calc(var(--wg-stroke-width-strong) * 2);
}

.wg-loading__spinner--sm {
  inline-size: var(--wg-size-24);
  block-size: var(--wg-size-24);
}

@keyframes wg-spin {
  to {
    transform: rotate(360deg);
  }
}

/* ── Modal Overlay ── */
.wg-loading__overlay {
  position: fixed;
  inset: 0;
  z-index: var(--wg-zindex-modal);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: auto;
}

/* ── Modal Toast Card ── */
.wg-loading__toast {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--wg-spacing-12);
  inline-size: var(--wg-size-104);
  block-size: var(--wg-size-104);
  background-color: var(--wg-color-bg-toast);
  border-radius: var(--wg-radius-lg);
  box-shadow: var(--wg-shadow-md);
}

/* ── Modal Text ── */
.wg-loading__text {
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-inverse);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: calc(var(--wg-size-104) - var(--wg-spacing-16) * 2);
}

/* ── Skeleton ── */
.wg-loading__skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-12);
  inline-size: 100%;
}

.wg-loading__skeleton-block {
  background-color: var(--wg-color-bg-skeleton);
  border-radius: var(--wg-radius-sm);
  animation: wg-pulse var(--wg-motion-duration-slow) var(--wg-motion-ease-standard) infinite;
}

.wg-loading__skeleton-block--rect {
  block-size: var(--wg-size-48);
  inline-size: 100%;
}

.wg-loading__skeleton-block--circle {
  block-size: var(--wg-size-48);
  inline-size: var(--wg-size-48);
  border-radius: var(--wg-radius-full);
}

.wg-loading__skeleton-block--line {
  block-size: var(--wg-size-16);
  inline-size: 60%;
}

@keyframes wg-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
}

/* ── Image Placeholder ── */
.wg-loading__image {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--wg-color-bg-skeleton);
  border-radius: var(--wg-radius-sm);
  inline-size: var(--wg-size-72);
  block-size: var(--wg-size-72);
}

.wg-loading__image-icon {
  display: inline-block;
  inline-size: var(--wg-size-24);
  block-size: var(--wg-size-24);
  background-color: var(--wg-color-border-loading-track);
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z'/%3E%3C/svg%3E");
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
}
```

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `visible` | `data-state="visible"` | 加载指示器可见 |
| `hidden` | `data-state="hidden"` | 加载指示器隐藏 |

V1 未定义 `progress`（带进度条）视觉变体。模态加载需要进度展示时，标注组件能力缺失。

## 可访问性

- 必须使用 `role="status"` 和 `aria-live="polite"`。
- `modal` 变体加载期间，屏幕阅读器应播报加载状态。
- `skeleton` 变体应使用 `aria-busy="true"` 标记加载区域。
- `image` 变体加载完成后应移除占位元素并替换为 `<img>` 元素。
- 不得使用 `display: none` 隐藏正在加载的 `modal` 变体遮罩层，应使用 `data-state` 控制可见性。

## 生成约束

- 必须同时声明一个 `variant` class。
- `spinner` 变体必须同时声明一个 `size` class（`lg` 或 `sm`）。
- 必须使用 `wg-loading`、`wg-loading__spinner`、`wg-loading__overlay`、`wg-loading__toast`、`wg-loading__skeleton`、`wg-loading__image`。
- 不得覆盖 Loading 位置、内边距、圆角和阴影。
- 不得覆盖旋转指示器尺寸、字号和颜色。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 不得新增 `progress`、`bar` 等未定义的变体。
- `skeleton` 变体的色块形状由页面布局决定，但必须使用 `wg-loading__skeleton-block` 命名。
- 页面脚本可以控制 Loading 的显示/隐藏，但不得绕过组件规定的 Anatomy、状态语义和可访问性约束。
- 完整页面中出现 Loading 时，必须读取并遵守本文件。

## 自检

```text
□ 是否先判断加载场景 → spinner / modal / skeleton / image
□ spinner 变体是否选择了正确的 size（lg / sm）
□ 是否只存在一个 variant
□ modal 变体是否设置了遮罩层
□ modal 变体文案是否不超过 8 个字符
□ skeleton 变体色块是否与实际内容布局一致
□ image 变体是否在图片加载完成后移除
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 是否设置 role="status" 和 aria-live="polite"
□ 是否没有自创 progress、bar 变体
□ modal 变体是否由业务逻辑控制关闭时机
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `469:39880`。提取下拉刷新（48px 旋转指示器）、页面加载（24px 旋转指示器）、模态加载（104px 深色浮层 + 旋转图标 + 可选文案）、局部加载（24px 旋转指示器）、骨架屏加载（灰色色块组合）、图片占位加载（72px 默认图片占位）六种场景的结构、尺寸、间距和使用规则。
- Kuikly `Loading`：参考 BaseVisuals 的 showLoadingToast 方法设计（变体类型、不自动关闭、冲突控制、遮罩样式、容器尺寸 96pt、图标区域 24x24、文案 14pt 白字）；不继承 Kuikly DSL、DialogUtil 管理方式、LoadingToastType 枚举、PAG 帧动画机制。
