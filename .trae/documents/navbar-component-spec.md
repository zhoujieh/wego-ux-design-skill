# 导航栏（NavBar）组件规范编写计划

## 摘要

基于 Figma 设计文件和 Kuikly 参考文档，按照 Button/Link 组件规范的最佳实践，编写微购导航栏（NavBar）组件规范，并注册到 registry.json。

## 当前状态分析

### 已有组件规范
- [button.md](file:///Users/dk/Documents/code/wego-design-system/wego-ux-design/03-components/button.md)：完整的组件规范模板，包含使用决策、语义模型、允许组合、Anatomy、文案规则、Canonical HTML/CSS、状态、可访问性、生成约束、自检、规范来源
- [link.md](file:///Users/dk/Documents/code/wego-design-system/wego-ux-design/03-components/link.md)：同结构模板
- [shared-rules.md](file:///Users/dk/Documents/code/wego-design-system/wego-ux-design/03-components/shared-rules.md)：公共规则（命名约定、生成边界、缺失处理）
- [registry.json](file:///Users/dk/Documents/code/wego-design-system/wego-ux-design/03-components/registry.json)：组件注册表，当前仅有 button 和 link

### Figma 设计数据（已获取）
- 来源文件：`📙 wegoo 组件应用场景`，节点 `166:2630`
- 导航栏整体：375×88px（含状态栏 44px + 导航栏内容 44px）
- 导航栏内容区（166:3523）：白底，`px-16 py-8`，flex 布局，`items-end justify-between`
- 左侧区域（166:3524）：28px 高，含返回图标
- 标题文字（166:3527）：18px，PingFang SC Semibold，颜色 #1d1d1d，不换行
- 设计变量：`常用/text_100（一级黑）: #1E2028`

### Kuikly 参考文档（已获取）
- [NavBar.md](file:///Users/dk/Documents/code/wego-design-system/参考资料/kuikly_doc/basic_components/NavBar.md)：三种布局模式、左侧按钮类型枚举、右侧操作区、搜索模式、ModalFrame 联动
- [NavBarActionButton.md](file:///Users/dk/Documents/code/wego-design-system/参考资料/kuikly_doc/basic_components/NavBarActionButton.md)：六种操作按钮类型（TEXT/ICON/ICON_TEXT/BUTTON/PICTURE/CUSTOM）

### 用户确认的 V1 范围
1. **三种模式全部覆盖**：标准模式、无按钮模式（主 Tab 导航）、搜索模式
2. **右侧操作按钮三种类型**：上图标下文字（ICON_TEXT）、纯文字（TEXT）、纯按钮（BUTTON）
3. **无按钮模式 = 主 Tab 页面的导航栏**（仅标题，无返回按钮）

## 提议变更

### 1. 新建 `wego-ux-design/03-components/navbar.md`

按照 Button/Link 的文档结构，编写导航栏组件规范：

#### 文档结构（对齐 Button 模板）

```
# NavBar

NavBar 用于页面顶部导航，承载标题、返回/关闭按钮和右侧操作区。

## 目录
## 使用决策
## 语义模型
## 允许组合
## Anatomy
## 文案规则
## Canonical HTML
## Canonical CSS
## 状态
## 可访问性
## 生成约束
## 自检
## 规范来源
```

#### 核心设计决策

**语义模型（3 个决策维度）：**

| 维度 | 含义 | 选项 |
|------|------|------|
| `mode` | 导航栏布局模式 | `standard`（标准：左侧按钮+标题+右侧操作）、`title-only`（仅标题，主Tab导航）、`search`（搜索模式） |
| `leftButton` | 左侧按钮类型 | `none`、`back`（返回箭头）、`close`（叉号）、`close-round`（圆形叉号）、`drop`（下拉箭头）、`text`（文字按钮如"取消"） |
| `state` | 当前交互状态 | `default`、`pressed`（左侧按钮按下）、`focus-visible` |

**右侧操作按钮（NavBarAction）类型：**

| 类型 | 语义 | 说明 |
|------|------|------|
| `text` | 纯文字操作 | 最多4字，如"发布""保存" |
| `icon-text` | 上图标下文字 | 图标20px + 文字10px |
| `button` | 填充按钮 | 复用 Button compact strong 样式 |

**Anatomy：**

```
标准模式：
header.wg-navbar.wg-navbar--standard
├── div.wg-navbar__left
│   └── button.wg-navbar__back (或 .wg-navbar__close / .wg-navbar__close-round / .wg-navbar__drop / .wg-navbar__left-text)
├── div.wg-navbar__title
│   └── h1.wg-navbar__title-text
└── div.wg-navbar__actions
    └── button.wg-navbar__action.wg-navbar__action--{type}

仅标题模式：
header.wg-navbar.wg-navbar--title-only
├── div.wg-navbar__title
│   └── h1.wg-navbar__title-text
└── div.wg-navbar__actions (可选)

搜索模式：
header.wg-navbar.wg-navbar--search
├── div.wg-navbar__left
│   └── button.wg-navbar__back
├── div.wg-navbar__search
│   └── div.wg-navbar__search-input (页面级临时结构，标注 Input 组件缺失)
└── div.wg-navbar__actions (可选)
```

**Token 映射（从 Figma 提取 + 现有 Token 体系）：**

| 设计属性 | Token | 值 |
|---------|-------|-----|
| 导航栏高度 | `--wg-size-44`（需新增）或使用 `--wg-size-48` | 44px |
| 标题字号 | `--wg-font-size-18`（需新增） | 18px |
| 标题字重 | `--wg-font-weight-semibold` | 600 |
| 标题颜色 | `--wg-color-text-primary` | #1E2028 |
| 标题行高 | `--wg-font-lineheight-18` | 26px |
| 导航栏背景 | `--wg-color-surface-toolbar-solid` | #F6F6F6 |
| 导航栏内边距 | `--wg-spacing-16`（水平）、`--wg-spacing-8`（垂直） | 16px / 8px |
| 操作文字字号 | `--wg-font-size-16` | 16px |
| 操作文字字重 | `--wg-font-weight-medium` | 500 |
| 底部分割线 | `--wg-stroke-color-default` + `--wg-stroke-width-hairline` | 0.5px |
| 按下态透明度 | 0.6 | — |
| 左侧图标尺寸 | `--wg-size-24` | 24px |
| 触控区域 | `--wg-touch-min` | 40px |

**需要新增的 Token（标注在规范中）：**

| Token 名称 | 值 | 理由 |
|-----------|-----|------|
| `wg.size.44` | 44px | 导航栏标准高度，Kuikly 和 Figma 均为 44px |
| `wg.font.size.f18` | 18px | 导航栏标题字号，Figma 确认为 18px |
| `wg.font.lineHeight.f18` | 26px | 18px 对应行高 |
| `wg.component.navbar.height` | 44px | 导航栏组件高度语义 Token |

> 注意：如果 `wg.size.44` 和 `wg.font.size.f18` 不满足"3个场景复用"规则，则在 navbar.md 中标注为 Token 缺失，使用页面级临时值。

**Canonical CSS 要点：**
- 导航栏使用 `position: sticky; top: 0; z-index: var(--wg-zindex-sticky)` 固定在顶部
- 标题自动居中：通过 flex 布局 + 左右区域等宽补偿实现
- 搜索模式中搜索框为页面级临时结构（Input 组件尚未注册）
- 右侧操作按钮最多 3 个
- 底部分割线可选显示

**状态：**

| State | HTML/CSS 表达 | 规则 |
|-------|-------------|------|
| `default` | 默认 class | 正常可用 |
| `pressed` | `:active` | 左侧按钮和操作按钮按下时透明度 0.6 |
| `focus-visible` | `:focus-visible` | 清晰焦点描边 |

**搜索模式处理：**
- 搜索框为页面级临时结构，使用语义化 HTML + 页面级 class
- 不使用 `.wg-input` 命名（Input 组件未注册）
- 标注 Input 组件规范缺失

### 2. 更新 `wego-ux-design/03-components/registry.json`

新增 navbar 组件注册：

```json
{
  "id": "navbar",
  "name": "NavBar",
  "category": "navigation",
  "status": "stable",
  "file": "navbar.md",
  "keywords": [
    "导航栏",
    "navbar",
    "导航",
    "标题栏",
    "顶部栏",
    "返回",
    "关闭",
    "搜索"
  ],
  "decisionAxes": {
    "mode": ["standard", "title-only", "search"],
    "leftButton": ["none", "back", "close", "close-round", "drop", "text"],
    "state": ["default", "pressed", "focus-visible"]
  },
  "interactionMode": "css"
}
```

### 3. 可能需要更新 `wego-ux-design/02-tokens/tokens.json`

如果 `wg.size.44`、`wg.font.size.f18`、`wg.font.lineHeight.f18` 满足 3 场景复用规则，则新增到 tokens.json 并重新生成派生文件。否则在 navbar.md 中标注 Token 缺失。

## 假设与决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 导航栏是否包含状态栏 | 不包含 | 与 Kuikly 一致，状态栏由页面层处理 |
| 导航栏高度 | 44px | Figma + Kuikly 均为 44px |
| 标题是否自动居中 | 是 | Kuikly 已实现，通过左右等宽补偿 |
| 搜索框是否作为正式组件 | 否，页面级临时结构 | Input 组件尚未注册，遵循"不为单页面新增组件"规则 |
| 右侧操作按钮是否独立组件 | 否，作为 NavBar 子元素 | 与 Kuikly 的 NavBarActionButton 不同，Web 原型中操作按钮是 NavBar 的内部元素 |
| 导航栏背景色 | 使用 `--wg-color-surface-toolbar-solid` | Token 体系中已有此值 |
| 左侧图标如何实现 | 使用 SVG 内联或 CSS background | V1 不定义 Icon 组件，使用页面级 SVG |

## 验证步骤

1. **规范完整性**：navbar.md 包含与 button.md 一致的所有章节
2. **Token 合规**：所有 CSS 值通过 `var(--wg-*)` 引用，无硬编码
3. **命名合规**：遵循 `.wg-navbar`、`.wg-navbar__{element}`、`.wg-navbar--{modifier}` 命名
4. **registry 注册**：registry.json 包含 navbar 条目，decisionAxes 正确
5. **搜索模式标注**：搜索框标注为页面级临时结构 + Input 组件缺失
6. **端到端验证**：用 navbar + button 生成一个带导航栏的页面原型，验证渲染和交互
