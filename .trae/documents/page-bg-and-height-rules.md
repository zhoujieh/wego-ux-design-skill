# 优化计划：页面背景色规则 + 页面高度与滚动规则

## 问题分析

### 问题 1：页面背景色全部输出灰色，缺少白/灰选择规则

**现状**：`token-usage-guidelines.md` 只写了"页面和容器背景使用 `wg.color.bg.*` 或 `wg.color.surface.*`"，没有定义什么场景用 `bg-page`（灰色 #EDEDED）、什么场景用 `bg-surface`（白色 #FFFFFF）。AI 生成时一律使用 `bg-page`，导致登录页等聚焦型页面也是灰色底。

**Token 现状**：
- `wg.color.bg.page` → `#EDEDED`（灰色）— 描述为"页面默认背景"
- `wg.color.bg.surface` → `#FFFFFF`（白色）— 描述为"卡片、表单、列表等主要容器背景"

**微信生态惯例**：
- 灰底：有多个白色卡片/模块的列表页、设置页，灰底充当卡片间距的视觉分隔
- 白底：聚焦型单任务页面（登录、结果、详情），内容区域是一个整体不需要卡片分隔

### 问题 2：页面高度默认 100%，内容不超出不滚动

**现状**：所有 `.page` 都用 `min-height: 100vh`，这会导致内容不足一屏时页面仍可滚动（因为 min-height 允许超出），且没有明确规则约束何时允许滚动、何时禁止滚动。

**期望**：
- 页面默认占满一屏（`height: 100vh` / `100dvh`），内容不超出时不滚动
- 内容超出时才允许滚动

## 修改方案

### 修改 1：`02-tokens/token-usage-guidelines.md` — 增加页面背景色选择规则

在 Color 段落中，将"页面和容器背景使用 `wg.color.bg.*` 或 `wg.color.surface.*`"替换为具体的背景色选择规则表：

```markdown
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
```

### 修改 2：`02-tokens/token-usage-guidelines.md` — 增加页面高度与滚动规则

在 Layout 段落末尾增加页面高度规则：

```markdown
### 页面高度与滚动

- 页面容器默认占满一屏：`block-size: 100vh`（兼容环境使用 `100dvh`），不使用 `min-height`。
- 内容不超出一屏时禁止滚动：页面容器设置 `overflow: hidden`。
- 内容可能超出一屏时允许滚动：页面容器设置 `overflow-y: auto`。
- 判断依据：表单型、结果型、聚焦型页面内容通常不超出 → 禁止滚动；浏览型、列表型页面内容通常超出 → 允许滚动。
```

### 修改 3：`04-ai-rules/02-ui-generation-rules.md` — 布局选择段落补充背景色和高度规则

在"5. 布局选择"段落末尾增加：

```markdown
### 页面背景色

按页面内容结构选择：

- 多卡片/多模块页面 → 页面背景 `bg-page`（灰色），卡片背景 `bg-surface`（白色）
- 聚焦型单任务页面 → 页面背景 `bg-surface`（白色），不使用卡片容器

### 页面高度

- 页面容器默认 `block-size: 100vh`，占满一屏。
- 内容不超出时不滚动（`overflow: hidden`）；内容超出时允许滚动（`overflow-y: auto`）。
```

## 涉及文件

| 文件 | 变更内容 |
|------|---------|
| `wego-ux-design/02-tokens/token-usage-guidelines.md` | Color 段落：增加页面背景色选择规则表 + 容器背景色规则表；Layout 段落：增加页面高度与滚动规则 |
| `wego-ux-design/04-ai-rules/02-ui-generation-rules.md` | 布局选择段落：增加页面背景色和页面高度规则 |

## 验证步骤

1. 修改完成后，用 Skill 重新生成相册登录页，验证：
   - 页面背景色应为 `bg-surface`（白色）而非 `bg-page`（灰色）
   - 页面高度应为 `block-size: 100dvh` + `overflow: hidden`，不出现滚动条
2. 用 Skill 生成一个列表页（如商品列表），验证：
   - 页面背景色应为 `bg-page`（灰色）
   - 页面高度应为 `block-size: 100dvh` + `overflow-y: auto`，允许滚动
