# NavBar

NavBar 用于页面顶部导航，承载标题、返回/关闭按钮和右侧操作区。本规则先判断导航栏布局模式，再选择左侧按钮类型和右侧操作样式。

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

使用 NavBar：

- 几乎每个页面都需要顶部导航栏。
- 需要返回、关闭或取消操作的页面顶部。
- 主 Tab 页面顶部仅显示标题的导航。
- 需要搜索入口的页面顶部。

不使用 NavBar：

- 沉浸式全屏页面（如视频播放、图片预览）：不需要固定导航栏。
- 弹窗内的标题栏：弹窗有自己的标题机制，不使用 NavBar 组件。
- 应用入口页面（登录页、启动页等）：用户尚未进入应用，没有"返回"的概念。

### NavBar 固定与滚动规则

NavBar 如果承载页面级返回、关闭、保存、发布、提交等动作，必须在长内容页面滚动时保持可见。

要求：

- NavBar 必须位于滚动内容外层，或使用可靠 sticky / fixed 方案
- sticky 必须设置 `top: 0`
- 必须设置合理 z-index（使用 `wg.zIndex.sticky` Token）
- 内容滚动不得带走 NavBar
- 生成后必须验证滚动状态

### NavBar 操作强度规则

NavBar 右侧操作不能默认使用 strong。

要求：

- 如果页面已有底部核心操作，NavBar 右侧同业务操作必须降级为 text / weak
- 如果 NavBar 是唯一核心操作入口，才允许使用较强表达（button 类型）
- NavBar 和底部操作栏不能同时承载同一个 strong 操作

判断流程：

```text
NavBar 右侧是否有核心操作？
├─ 是 → 页面底部是否已有同业务核心操作？
│   ├─ 是 → NavBar 右侧操作降级为 text / weak
│   └─ 否 → NavBar 允许使用 button 类型
└─ 否 → 无需判断
```

### NavBar 滚动时背景与层级

滚动时 NavBar 必须保持：

- 背景不透明或具备清晰毛玻璃规则
- 文本可读
- 分隔线或阴影符合滚动状态
- 不被页面内容覆盖

## 语义模型

NavBar 有四个决策维度：

```text
mode        导航栏布局模式
leftButton  左侧按钮类型
background  导航栏背景风格
state       当前交互状态
```

### Mode

| Mode | 应用场景 | 布局规则 |
|---|---|---|
| `standard` | 普通页面，有左侧按钮 + 居中标题 + 右侧操作区 | 左侧按钮区 + 标题区（自动居中）+ 右侧操作区 |
| `title-only` | 主 Tab 页面，仅标题，无返回按钮 | 标题区左对齐 + 可选右侧操作区 |
| `search` | 需要搜索入口的页面 | 左侧按钮区 + 搜索框 + 可选右侧操作区 |

禁止直接根据"有没有返回按钮"选择模式。必须先判断页面是否为主 Tab 页面或搜索页面。

### LeftButton

| LeftButton | 含义 | 样式 |
|---|---|---|
| `none` | 无左侧按钮 | 不渲染左侧区域 |
| `back` | 返回上一页 | 返回箭头图标 |
| `close` | 关闭当前页面 | 叉号图标 |
| `text` | 文字按钮（如"取消"） | 纯文字，一级文字色 |

`back` 是最常用的左侧按钮。`close` 用于需要关闭而非返回的页面。`text` 用于需要"取消"等文字操作的表单页。弹窗内的标题区域（含圆形关闭按钮、下拉关闭按钮等）不使用 NavBar，后续单独定义。

### Background

| Background | 应用场景 | 样式 |
|---|---|---|
| `default` | 页面背景为灰色或白色 | 跟随页面背景色，通过 `wg-navbar--bg-default` 修饰符 + 页面级 CSS 变量覆盖实现（见下方联动规则） |
| `transparent` | 页面背景为图片或深色底 | 透明背景 + 内容反白（文字和图标使用 `wg.color.text.inverse`） |
| `custom` | 极其特殊的场景 | 完全自定义背景和内容颜色，不得修改导航栏高度、内边距和布局结构 |

背景选择规则：

- 默认使用 `default`，导航栏背景跟随页面背景色。
- 页面顶部为全屏图片、深色背景或沉浸式内容时使用 `transparent`。
- `custom` 仅在 `default` 和 `transparent` 均无法满足时使用，必须在交付说明中标注自定义原因。
- `transparent` 模式下，`button` 类型操作按钮保持品牌色背景 + 反白文字不变。

### NavBar 背景色与页面背景色联动规则

`wg-navbar--bg-default` 的默认背景色跟随页面背景色。灰底页面使用 `wg.color.bg.page`（#EDEDED），白底页面使用 `wg.color.bg.surface`（#FFFFFF）。

`wg.color.surface.toolbar.solid`（#F6F6F6）仅适用于页面底部操作栏，不得用于顶部 NavBar。

实现方式：

```css
/* 灰底页面中，NavBar 背景色 */
.wg-navbar--bg-default {
  background-color: var(--wg-color-bg-page);
}

/* 白底页面中，覆盖 NavBar 背景色 */
.page-surface .wg-navbar--bg-default {
  background-color: var(--wg-color-bg-surface);
}
```

判断流程：

```text
页面背景色是什么？
├─ bg-page（灰色 #EDEDED）→ NavBar 使用 bg-page（#EDEDED）
├─ bg-surface（白色 #FFFFFF）→ NavBar 使用 bg-surface（#FFFFFF）
└─ 其他 → 使用 transparent 或 custom
```

页面类型与 NavBar 背景对照：

| 页面类型 | 页面背景 | NavBar 背景 |
|---|---|---|
| 多卡片/多模块列表页 | `bg-page`（灰 #EDEDED） | `bg-page`（#EDEDED） |
| 聚焦型单任务页（登录、注册、重置密码、绑定手机号等） | `bg-surface`（白 #FFFFFF） | `bg-surface`（#FFFFFF） |
| 结果页 | `bg-surface`（白 #FFFFFF） | `bg-surface`（#FFFFFF） |
| 沉浸式/图片背景页 | 自定义 | `transparent` |

## 允许组合

| Mode | LeftButton | 右侧操作 | 操作数量 |
|---|---|---|---|
| `standard` | `back` / `close` / `text` | 允许 | 0–3 个 |
| `title-only` | `none` | 允许 | 0–3 个 |
| `search` | `back` / `close` / `none` | 允许 | 0–2 个 |

附加规则：

- 右侧操作最多 3 个，超过时保留高频操作，其余进入更多菜单。
- `search` 模式右侧操作最多 2 个，搜索框需要足够空间。
- 同一导航栏不得同时出现 `back` 和 `close`。
- `title-only` 模式标题左对齐，不居中。
- `standard` 模式标题自动居中，通过左右区域等宽补偿实现。

### 右侧操作按钮类型

| 类型 | 语义 | 说明 |
|---|---|---|
| `text` | 纯文字操作 | 最多 4 字，如"发布""保存""管理" |
| `icon-text` | 上图标下文字 | 图标 20px + 文字 10px，如分享图标+"分享" |
| `button` | 填充按钮 | 复用 Button compact strong 样式，如"确认收货" |

右侧操作按钮类型选择规则：

- 页面级主要操作使用 `button`，如"发布""确认收货"。
- 次要操作使用 `text`，如"管理""编辑"。
- 需要图标辅助说明的操作使用 `icon-text`。
- 同一导航栏右侧最多出现一个 `text`，最多出现一个 `button`。
- `icon-text` 和 `text` 不得混搭。同一导航栏右侧要么全部使用 `icon-text`，要么使用 `text`（或单个 `text` + 单个 `button`）。

## Anatomy

标准模式：

```text
header.wg-navbar.wg-navbar--standard.wg-navbar--bg-{background}
├── div.wg-navbar__left
│   └── button.wg-navbar__left-btn.wg-navbar__left-btn--{type}
├── div.wg-navbar__center
│   └── h1.wg-navbar__title
└── div.wg-navbar__actions
    └── button.wg-navbar__action.wg-navbar__action--{type}
```

仅标题模式：

```text
header.wg-navbar.wg-navbar--title-only.wg-navbar--bg-{background}
├── div.wg-navbar__center
│   └── h1.wg-navbar__title
└── div.wg-navbar__actions
    └── button.wg-navbar__action.wg-navbar__action--{type}
```

搜索模式：

```text
header.wg-navbar.wg-navbar--search.wg-navbar--bg-{background}
├── div.wg-navbar__left
│   └── button.wg-navbar__left-btn.wg-navbar__left-btn--back
├── div.wg-navbar__center
│   └── div.wg-navbar__search-box
│       └── input.wg-navbar__search-input
└── div.wg-navbar__actions
    └── button.wg-navbar__action.wg-navbar__action--{type}
```

V1 左侧按钮图标使用 SVG 内联实现。不得自行加入角标、副标题或加载图标。

搜索框为页面级临时结构，不使用 `.wg-input` 命名。Input 组件注册后应替换为正式组件。

## 文案规则

- 标题使用页面名称，如"商品管理""订单详情""设置"。
- 标题最多 10 个字符，超出截断显示省略号。
- 标题单行展示，不换行。
- 右侧 `text` 操作使用明确动词，如"发布""保存""管理"，避免"操作""更多"等模糊词。
- 右侧 `text` 操作最多 4 个字符，超出截断。
- `leftButton` 为 `text` 时，使用"取消"等明确动作词。
- 同一导航栏的操作文案使用一致的语法结构。

## Canonical HTML

标准模式 — 返回 + 标题 + 文字操作（默认背景）：

```html
<header class="wg-navbar wg-navbar--standard wg-navbar--bg-default">
  <div class="wg-navbar__left">
    <button class="wg-navbar__left-btn wg-navbar__left-btn--back" type="button" aria-label="返回">
      <svg class="wg-navbar__left-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M15.5 19L9 12.5L15.5 6" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
  <div class="wg-navbar__center">
    <h1 class="wg-navbar__title">商品管理</h1>
  </div>
  <div class="wg-navbar__actions">
    <button class="wg-navbar__action wg-navbar__action--text" type="button">
      <span class="wg-navbar__action-label">管理</span>
    </button>
  </div>
</header>
```

仅标题模式 — 主 Tab 导航：

```html
<header class="wg-navbar wg-navbar--title-only wg-navbar--bg-default">
  <div class="wg-navbar__center">
    <h1 class="wg-navbar__title">微购</h1>
  </div>
  <div class="wg-navbar__actions">
    <button class="wg-navbar__action wg-navbar__action--icon-text" type="button">
      <svg class="wg-navbar__action-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
        <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <span class="wg-navbar__action-label">添加</span>
    </button>
  </div>
</header>
```

搜索模式：

```html
<header class="wg-navbar wg-navbar--search wg-navbar--bg-default">
  <div class="wg-navbar__left">
    <button class="wg-navbar__left-btn wg-navbar__left-btn--back" type="button" aria-label="返回">
      <svg class="wg-navbar__left-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M15.5 19L9 12.5L15.5 6" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
  <div class="wg-navbar__center">
    <div class="wg-navbar__search-box">
      <input class="wg-navbar__search-input" type="search" placeholder="搜索商品" />
    </div>
  </div>
</header>
```

关闭按钮 + 填充按钮操作：

```html
<header class="wg-navbar wg-navbar--standard wg-navbar--bg-default">
  <div class="wg-navbar__left">
    <button class="wg-navbar__left-btn wg-navbar__left-btn--close" type="button" aria-label="关闭">
      <svg class="wg-navbar__left-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.25" stroke-linecap="round"/>
      </svg>
    </button>
  </div>
  <div class="wg-navbar__center">
    <h1 class="wg-navbar__title">商品详情</h1>
  </div>
  <div class="wg-navbar__actions">
    <button class="wg-navbar__action wg-navbar__action--button" type="button">
      <span class="wg-navbar__action-label">确认收货</span>
    </button>
  </div>
</header>
```

文字左侧按钮：

```html
<header class="wg-navbar wg-navbar--standard wg-navbar--bg-default">
  <div class="wg-navbar__left">
    <button class="wg-navbar__left-btn wg-navbar__left-btn--text" type="button">
      <span class="wg-navbar__left-text">取消</span>
    </button>
  </div>
  <div class="wg-navbar__center">
    <h1 class="wg-navbar__title">编辑商品</h1>
  </div>
  <div class="wg-navbar__actions">
    <button class="wg-navbar__action wg-navbar__action--text" type="button">
      <span class="wg-navbar__action-label">保存</span>
    </button>
  </div>
</header>
```

透明背景 — 图片/深色底页面：

```html
<header class="wg-navbar wg-navbar--standard wg-navbar--bg-transparent">
  <div class="wg-navbar__left">
    <button class="wg-navbar__left-btn wg-navbar__left-btn--back" type="button" aria-label="返回">
      <svg class="wg-navbar__left-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M15.5 19L9 12.5L15.5 6" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
  <div class="wg-navbar__center">
    <h1 class="wg-navbar__title">活动详情</h1>
  </div>
  <div class="wg-navbar__actions">
    <button class="wg-navbar__action wg-navbar__action--text" type="button">
      <span class="wg-navbar__action-label">分享</span>
    </button>
  </div>
</header>
```

## Canonical CSS

```css
.wg-navbar {
  position: sticky;
  top: 0;
  z-index: var(--wg-zindex-sticky);
  display: flex;
  align-items: flex-end;
  block-size: var(--wg-touch-default);
  padding-block: var(--wg-spacing-8);
  padding-inline: var(--wg-spacing-16);
  background-color: var(--wg-color-bg-page);
}

/* 背景风格 */
.wg-navbar--bg-default {
  background-color: var(--wg-color-bg-page);
  /* 灰底页面使用 bg-page；白底页面需通过页面级选择器覆盖为 var(--wg-color-bg-surface) */
  /* toolbar.solid 仅适用于底部操作栏，不得用于顶部 NavBar */
}

.wg-navbar--bg-transparent {
  background-color: transparent;
  color: var(--wg-color-text-inverse);
}

.wg-navbar--bg-transparent .wg-navbar__title {
  color: var(--wg-color-text-inverse);
}

.wg-navbar--bg-transparent .wg-navbar__left-btn {
  color: var(--wg-color-text-inverse);
}

.wg-navbar--bg-transparent .wg-navbar__action--text .wg-navbar__action-label {
  color: var(--wg-color-text-inverse);
}

.wg-navbar--bg-transparent .wg-navbar__action--icon-text .wg-navbar__action-label {
  color: var(--wg-color-text-inverse);
}

.wg-navbar--bg-transparent .wg-navbar__action--icon-text .wg-navbar__action-icon {
  color: var(--wg-color-text-inverse);
}

.wg-navbar--bg-transparent .wg-navbar__search-box {
  background-color: var(--wg-color-bg-inverse-subtle);
}

.wg-navbar--bg-transparent .wg-navbar__search-input {
  color: var(--wg-color-text-inverse);
}

.wg-navbar--bg-transparent .wg-navbar__search-input::placeholder {
  color: var(--wg-color-text-inverse-weak);
}

.wg-navbar--bg-custom {
  /* 自定义背景色由页面级样式覆盖 background-color */
}

.wg-navbar--standard .wg-navbar__left,
.wg-navbar--standard .wg-navbar__actions {
  flex: 1 1 0;
  min-inline-size: 0;
}

.wg-navbar--standard .wg-navbar__left {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.wg-navbar--standard .wg-navbar__center {
  flex: 0 0 auto;
}

.wg-navbar--title-only .wg-navbar__center {
  flex: 1 1 0;
  min-inline-size: 0;
}

.wg-navbar--title-only .wg-navbar__actions {
  flex: 0 0 auto;
}

.wg-navbar--search .wg-navbar__left {
  flex: 0 0 auto;
}

.wg-navbar--search .wg-navbar__center {
  flex: 1 1 0;
  min-inline-size: 0;
}

.wg-navbar--search .wg-navbar__actions {
  flex: 0 0 auto;
}

/* 标题 */
.wg-navbar__title {
  font-size: var(--wg-font-size-18);
  line-height: var(--wg-font-lineheight-18);
  font-weight: var(--wg-font-weight-semibold);
  color: var(--wg-color-text-primary);
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.wg-navbar--title-only .wg-navbar__title {
  text-align: left;
}

/* 左侧按钮 */
.wg-navbar__left-btn {
  appearance: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-block-size: var(--wg-touch-min);
  min-inline-size: var(--wg-touch-min);
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  color: var(--wg-color-text-primary);
  cursor: pointer;
  transition:
    opacity var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-navbar__left-icon {
  inline-size: var(--wg-size-24);
  block-size: var(--wg-size-24);
}

.wg-navbar__left-btn--text {
  min-inline-size: auto;
}

.wg-navbar__left-text {
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
  color: var(--wg-color-text-primary);
  white-space: nowrap;
}

.wg-navbar__left-btn:not(:disabled):active {
  opacity: 0.6;
}

.wg-navbar__left-btn:focus-visible {
  outline: none;
}

.wg-navbar__left-btn:focus-visible .wg-navbar__left-icon,
.wg-navbar__left-btn:focus-visible .wg-navbar__left-text {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}

/* 右侧操作区 */
.wg-navbar__actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--wg-spacing-4);
}

/* 右侧操作按钮 — 公共 */
.wg-navbar__action {
  appearance: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-block-size: var(--wg-touch-min);
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  color: var(--wg-color-text-primary);
  cursor: pointer;
  transition:
    opacity var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-navbar__action:not(:disabled):active {
  opacity: 0.6;
}

.wg-navbar__action:focus-visible {
  outline: none;
}

.wg-navbar__action:focus-visible .wg-navbar__action-label {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: var(--wg-spacing-2);
}

/* 右侧操作按钮 — text */
.wg-navbar__action--text {
  padding-inline: var(--wg-spacing-8);
}

.wg-navbar__action--text .wg-navbar__action-label {
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
  color: var(--wg-color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 4em;
}

/* 右侧操作按钮 — icon-text */
.wg-navbar__action--icon-text {
  flex-direction: column;
  padding-inline: var(--wg-spacing-4);
}

.wg-navbar__action-icon {
  inline-size: var(--wg-size-20);
  block-size: var(--wg-size-20);
}

.wg-navbar__action--icon-text .wg-navbar__action-label {
  font-size: var(--wg-font-size-10);
  line-height: var(--wg-font-lineheight-10);
  font-weight: var(--wg-font-weight-medium);
  color: var(--wg-color-text-primary);
  white-space: nowrap;
}

/* 右侧操作按钮 — button */
.wg-navbar__action--button .wg-navbar__action-label {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  block-size: var(--wg-size-32);
  padding-inline: var(--wg-spacing-12);
  border-radius: var(--wg-radius-sm);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-medium);
  background-color: var(--wg-color-action-primary-default);
  color: var(--wg-color-text-inverse);
  white-space: nowrap;
}

.wg-navbar__action--button:not(:disabled):hover .wg-navbar__action-label {
  background-color: var(--wg-color-action-primary-hover);
}

.wg-navbar__action--button:not(:disabled):active .wg-navbar__action-label {
  background-color: var(--wg-color-action-primary-pressed);
  opacity: 1;
}

/* 搜索框 */
.wg-navbar__search-box {
  display: flex;
  align-items: center;
  block-size: var(--wg-size-32);
  padding-inline: var(--wg-spacing-8);
  border-radius: var(--wg-radius-md);
  background-color: var(--wg-color-bg-subtle);
}

.wg-navbar__search-input {
  appearance: none;
  flex: 1 1 0;
  min-inline-size: 0;
  block-size: 100%;
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  color: var(--wg-color-text-primary);
  outline: none;
}

.wg-navbar__search-input::placeholder {
  color: var(--wg-color-text-placeholder);
}

/* 底部分割线 */
.wg-navbar--divider::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  block-size: var(--wg-stroke-width-hairline);
  background-color: var(--wg-stroke-color-default);
}
```

导航栏高度使用 `wg.touch.default`（44px），与 Kuikly 和 Figma 设计一致。左侧按钮和操作按钮的可见尺寸可能小于触控区域，外层通过 `wg.touch.min` 保证最小触控尺寸。

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 正常可用 |
| `pressed` | `:active` | 左侧按钮和操作按钮按下时透明度 0.6，不位移、不缩放 |
| `focus-visible` | `:focus-visible` | 必须显示清晰焦点描边 |

V1 未定义 `loading`、`scrolling`（毛玻璃吸顶态）视觉变体。遇到这些需求不得自行向 NavBar 加入 Spinner、毛玻璃背景或滚动监听；通过页面级脚本和样式实现，并标注组件能力缺失。

NavBar 滚动状态要求：

- NavBar 使用 `position: sticky; top: 0` 实现吸顶
- z-index 必须使用 `wg.zIndex.sticky` Token
- 滚动时 NavBar 不得被内容区覆盖
- 如果 NavBar 承载页面级动作（返回、保存、发布），滚动时必须保持可见

## 可访问性

- 必须使用原生 `<header>` 作为导航栏容器。
- 标题必须使用 `<h1>`。
- 左侧按钮必须使用原生 `<button>`，图标按钮必须提供 `aria-label`。
- 右侧操作按钮必须使用原生 `<button>`。
- 搜索输入框必须使用 `<input type="search">`。
- 焦点顺序必须与视觉顺序一致：左侧按钮 → 标题 → 右侧操作。
- 禁止使用 `div`、`span` 模拟可点击按钮。

## 生成约束

- 必须同时声明一个 `mode` class 和一个 `background` class（`wg-navbar--bg-{background}`）。
- `standard` 模式必须声明一个 `leftButton` class。
- 不得覆盖导航栏高度、标题字号、标题字重、标题颜色和内边距。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- `transparent` 和 `custom` 是通过 `wg-navbar--bg-*` 修饰符实现的，不是独立 mode。
- 搜索框使用 `.wg-navbar__search-box` 和 `.wg-navbar__search-input`，不使用 `.wg-input` 命名。
- 页面布局只控制 NavBar 的位置，不控制 NavBar 内部样式。
- `wg-navbar--bg-custom` 仅允许覆盖 `background-color` 和内容颜色，不得修改高度、内边距和布局结构。
- 完整页面中出现 NavBar 时，必须读取并遵守本文件。

## 自检

```text
□ 是否先判断 standard / title-only / search
□ standard 模式是否选择了正确的 leftButton 类型
□ 是否声明了 background 修饰符（bg-default / bg-transparent / bg-custom）
□ 右侧操作是否不超过 3 个
□ 是否只存在一个 text 和一个 button 类型操作
□ icon-text 和 text 是否未混搭
□ 标题是否不超过 10 个字符
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 左侧图标按钮是否提供 aria-label
□ 是否使用原生 header、h1、button
□ 搜索框是否未使用 .wg-input 命名
□ 是否没有自创 loading、scrolling 变体
□ NavBar 是否使用 sticky 定位
□ NavBar z-index 是否使用 wg.zIndex.sticky Token
□ 滚动时 NavBar 是否保持可见
□ NavBar 右侧操作是否与底部操作去重
□ 同一业务动作是否不在 NavBar 和底部同时使用 strong
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `166:2630`。提取导航栏标准模式、仅标题模式和搜索模式的布局、间距、字号和颜色。
- Kuikly `WGNavBar`：参考三种布局模式、左侧按钮类型枚举、右侧操作区数量限制、标题自动居中和标题截断规则；不继承 Kuikly DSL、ModalFrame 联动、自定义主题或高级配置。
- Kuikly `NavBarActionButton`：参考右侧操作按钮的三种类型（text / icon-text / button）、文字截断规则和按下态透明度；不继承 ICON、PICTURE、CUSTOM 类型和自定义颜色配置。
