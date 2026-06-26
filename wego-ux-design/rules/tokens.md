# 微购 Token 与消费规则

> 微购 Design System Skill / rules
> 本文档定义 Token 的权威来源、下游消费方式、合规检查和缺失处理。

## 权威来源

- 唯一源数据：`design-library/tokens-source.json`
- 机器可读投影：`design-library/tokens.json`
- 可复制 CSS：`design-library/tokens.css`
- 页面骨架：`design-library/scaffold.css`
- CSS 映射参考：`design-library/token-css-map.md`

`design-library/tokens.json` 和 `design-library/tokens.css` 是供 AI / 下游消费的产物；`design-library/tokens-source.json` 是维护入口。不得手工修改生成物去绕过源数据。

## 读取顺序

消费设计库时，Token 层的推荐顺序是：

```text
design-library/library-consumption.json
↓
design-library/tokens.json
↓
design-library/tokens.css
↓
design-library/scaffold.css（需要布局骨架时）
```

## 总原则

- 优先使用 Semantic Token，其次使用 Pattern Token，最后使用 Base Token。
- HTML/CSS 只使用 `design-library/token-css-map.md` 中存在的 `var(--wg-*)`。
- 业务样式不直接写颜色、字号、间距、圆角、尺寸、阴影、动效或层级值。
- 不把组件结构、组件状态或页面专属补丁写进 Token。
- 页面级辅助排版优先复用 `scaffold.css`，不要用临时样式重新定义同类基础规则。

## Color

- 文本使用 `wg.color.text.*`
- 操作状态使用 `wg.color.action.*`
- 成功、警示、危险和信息反馈使用对应状态语义
- Base Color 只用于缺少语义映射的底层定义，不作为默认选择

### 页面背景色

- 多模块 / 多卡片页面：`wg.color.bg.page`
- 聚焦型单任务页面：`wg.color.bg.surface`
- 不确定时优先选择白底 `bg-surface`

## Typography

- 普通界面文本使用 `wg.font.size.*`
- 金额和关键数据使用 `wg.font.number.*`
- 默认正文从 `wg.font.size.f14` 开始
- 辅助说明优先使用 `wg.font.size.f12`
- 字重只使用 `wg.font.weight.*`

## Spacing、Radius 与 Size

- 所有间距从 `wg.spacing.*` 选择
- 所有圆角从 `wg.radius.*` 选择
- 图标、头像和通用尺寸从 `wg.size.*` 选择
- 可点击区域不得小于 `wg.touch.min`
- 不通过临时 padding 制造新的页面布局规则

## Layout

- 默认业务页面使用 M2
- 高密度列表使用 M0
- 通栏连续内容使用 M1
- 低密度聚焦页面使用 M3
- 紧密连续信息使用 G1，宽松模块信息使用 G2
- 屏幕、内容宽度和模态高度只使用 `wg.layout.*` 中已有定义

### 布局工具类

M/G 模式通过 `design-library/scaffold.css` 的工具类在代码中表达：

- `.wg-page-m{0-3}`：页面级左右留白
- `.wg-group-g{1-2}`：分组内子元素间距

具体值、适用场景及使用示例参见 `rules/generation.md` 布局选择章节。


## Elevation、Stroke、Blur 与 Motion

- 默认无阴影；只有层级确实浮起时使用 `wg.shadow.*`
- 描边宽度、颜色和样式分别使用 `wg.stroke.width.*`、`wg.stroke.color.*`、`wg.stroke.style.*`
- Blur 只用于明确的毛玻璃或背景弱化场景
- 动效持续时间和缓动分别使用 `wg.motion.duration.*` 与 `wg.motion.ease.*`

## Z-Index

- 使用 `wg.zIndex.*` 表达固定层、下拉层、浮层、反馈、遮罩和弹层
- 不使用任意大数字解决层级冲突
- Modal 必须位于 Overlay 之上，Toast 不得被遮罩覆盖

## Copywriting

- 高频操作、空状态、错误、反馈和表单文案优先使用 `wg.copy.*`
- Copywriting Token 不生成 CSS 变量
- 错误提示必须可理解并提供恢复方向
- 危险操作必须说明对象和后果

## 合规检查

检查界面或代码时必须确认：

- 使用的 `wg.*` 名称存在于 `design-library/tokens.json` 或 `design-library/token-css-map.md`
- 使用的 `var(--wg-*)` 存在于 `design-library/tokens.css`
- 业务样式不存在硬编码颜色、字号、间距、圆角、尺寸、阴影、动效或 z-index
- Semantic Token 可以表达时，没有退回 Base Token
- Copywriting Token 没有被误用为 CSS 变量
- 缺失 Token 没有通过临时值绕过

## 图标关系

图标尺寸、颜色和 SVG 兜底规则仍以 `rules/icon-guidelines.md` 为准。图标资源的消费边界以 `design-library/library-consumption.json` 的 `icons` layer 为准。

## 缺失处理

缺少 Token 时不直接创造设计值，输出：

```text
当前使用：
原因：
建议新增：
归属位置：design-library/tokens-source.json
```

## 使用示例

正确示例：

```text
主标题：wg.font.size.f18 + wg.font.weight.semibold
正文：wg.font.size.f14 + wg.font.weight.regular
辅助说明：wg.font.size.f12 + wg.font.weight.regular

主文字：wg.color.text.primary
辅助文字：wg.color.text.secondary
页面背景：wg.color.bg.page
内容背景：wg.color.bg.surface
主操作：wg.color.action.primary.default
危险文字：wg.color.text.danger

强关联：wg.spacing.4
同组内容：wg.spacing.8 / wg.spacing.16
清晰分隔：wg.spacing.24
模块分隔：wg.spacing.32

默认圆角：wg.radius.md
大圆角：wg.radius.lg
胶囊圆角：wg.radius.full

默认业务页面：wg.layout.page.m2.margin
高密度列表：wg.layout.page.m0.margin
紧密分组：G1
宽松分组：G2
```

错误示例：

<!-- token-lint: allow-hardcoded reason=negative-example -->

```text
color: #03C160
font-size: 15px
margin: 10px
border-radius: 20px
z-index: 9999
box-shadow: 0 8px 40px rgba(...)
```

缺失 Token 示例：

```text
当前使用：wg.spacing.24
原因：缺少专用于「筛选区与结果列表之间」的间距 Token
建议新增：wg.spacing.xxx
归属位置：design-library/tokens-source.json
```

## 禁止事项

- 为单页面或单个临时变体新增 Token
- 手工修改 `design-library/tokens.json`、`design-library/tokens.css` 或 `design-library/token-css-map.md`
- 使用未定义的 `wg.*` 或 `--wg-*`
- 用魔法数字绕过 Token
- 把组件结构写进 Token
