# 微购 Token 使用规则

具体名称、值和 CSS 变量以自动生成的 `token-reference.md` 为准。本文件只定义使用原则，不重复保存 Token 值。

## 总原则

- 优先使用 Semantic Token，其次使用 Pattern Token，最后使用 Base Token。
- HTML/CSS 只使用 `token-css-map.md` 中存在的 `var(--wg-*)`。
- 不直接写颜色、字号、间距、圆角、尺寸、阴影、动效或层级值。
- 不把组件结构或组件状态组合写进基础 Token。

## Color

- 文本使用 `wg.color.text.*`。
- 操作状态使用 `wg.color.action.*`。
- 成功、警示、危险和信息反馈使用对应的状态语义。
- Base Color 只用于缺少语义映射的底层定义，不作为默认选择。

### 页面背景色

| 背景 Token | 值 | 适用场景 |
|---|---|---|
| `wg.color.bg.page` | 灰色 | 多模块/多卡片页面，灰底充当卡片间的视觉分隔（列表页、设置页、管理页） |
| `wg.color.bg.surface` | 白色 | 聚焦型单任务页面，内容区域是一个整体不需要卡片分隔（登录、结果、详情、表单提交） |

选择规则：

- 页面包含多个独立卡片/模块 → 灰底（`bg-page`），卡片使用 `bg-surface`
- 页面内容是一个整体、不需要卡片分隔 → 白底（`bg-surface`）
- 不确定时优先选择白底；白底信息层级更清晰，灰底只在确实需要分隔时使用

### 容器背景色

| 背景 Token | 值 | 适用场景 |
|---|---|---|
| `wg.color.bg.surface` | 白色 | 卡片、表单容器、列表项等主要内容容器 |
| `wg.color.bg.subtle` | 极浅灰 | 需要与白色容器做微弱区分的次要容器 |
| `wg.color.bg.muted` | 浅灰 | 选中态、禁用态等弱化容器 |

## Typography

- 普通界面文本使用 `wg.font.size.*` 系列。
- 金额和关键数据使用 `wg.font.number.*` 系列，并配合装饰数字字体。
- 默认正文从 `wg.font.size.f14` 开始。
- 辅助说明优先使用 `wg.font.size.f12`。
- 字重只使用 `wg.font.weight.*`，行高与对应字号配套。

## Spacing、Radius 与 Size

- 所有间距从 `wg.spacing.*` 选择。
- 所有圆角从 `wg.radius.*` 选择，避免把大圆角作为默认风格。
- 图标、头像和通用尺寸从 `wg.size.*` 选择。
- 可点击区域不得小于 `wg.touch.min`。
- 不通过临时 padding 制造新的页面布局规则。

### 间距前提：浏览器默认间距必须清除

Token 间距生效的前提是浏览器默认间距已清除。未清除时，浏览器默认 margin/padding 会与 Token 间距叠加，导致实际渲染值偏离设计意图。

受影响的元素及默认行为：

| 元素 | 浏览器默认行为 | 对布局的影响 |
|---|---|---|
| `body` | margin: 8px | 页面整体偏移，M0-M3 的 margin 被叠加 |
| `h1`~`h6` | margin + 默认字号/字重 | 标题间距和排版层级不可控 |
| `p` | margin: 1em 0 | 文本间距不可控，与 Token spacing 冲突 |
| `ul`/`ol` | padding-left: 40px + margin | 列表缩进和间距不可控 |
| `dl` | margin | 定义列表间距不可控 |
| `figure` | margin: 1em 0 | 图片容器间距不可控 |
| `blockquote` | margin + padding-left | 引用块间距不可控 |
| `hr` | margin + border 样式 | 分割线样式与 Token divider 冲突 |
| `fieldset` | padding + border | 表单分组容器不可控 |
| `pre` | margin + font-family: monospace | 等宽字体干扰排版 |

`tokens.css` 已包含基础重置块，将上述元素的 margin 归零，`ul`/`ol` 的 padding 和 list-style 归零，`body` 设置默认字体和颜色。生成页面时必须引入包含基础重置的 `tokens.css`，不得在业务样式中自行修补浏览器默认间距。

## Layout

- 默认业务页面使用 M2。
- 高密度列表使用 M0。
- 通栏连续内容使用 M1。
- 低密度聚焦页面使用 M3。
- 紧密连续信息使用 G1，宽松模块信息使用 G2。
- 屏幕、内容宽度和模态高度只使用 `wg.layout.*` 中已有定义。

### 页面高度与滚动

- 页面容器默认占满一屏：`block-size: 100vh`（兼容环境使用 `100dvh`），不使用 `min-height`。
- 内容不超出一屏时禁止滚动：页面容器设置 `overflow: hidden`。
- 内容可能超出一屏时允许滚动：页面容器设置 `overflow-y: auto`。
- 判断依据：表单型、结果型、聚焦型页面内容通常不超出 → 禁止滚动；浏览型、列表型页面内容通常超出 → 允许滚动。

## Elevation、Stroke、Blur 与 Motion

- 默认无阴影；只有层级确实浮起时使用 `wg.shadow.*`。
- 描边宽度、颜色和样式分别使用 `wg.stroke.width.*`、`wg.stroke.color.*`、`wg.stroke.style.*`。
- Blur 只用于明确的毛玻璃或背景弱化场景。
- 动效持续时间和缓动分别使用 `wg.motion.duration.*` 与 `wg.motion.ease.*`。

## Z-Index

- 使用 `wg.zIndex.*` 表达固定层、下拉层、浮层、反馈、遮罩和弹层。
- 不使用任意大数字解决层级冲突。
- Modal 必须位于 Overlay 之上，Toast 不得被遮罩覆盖。

## Copywriting

- 高频操作、空状态、错误、反馈和表单文案优先使用 `wg.copy.*`。
- Copywriting Token 不生成 CSS 变量。
- 错误提示必须可理解并提供恢复方向。
- 危险操作必须说明对象和后果。

## 缺失处理

缺少 Token 时不直接创造设计值，输出：

```text
当前使用：
原因：
建议新增：
归属位置：02-tokens/tokens.json
```
