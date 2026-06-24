# 计划：补充图标使用规则

## 摘要

将图标使用规则补充到微购设计系统中，包括：iconfont 图标库的使用规范、图标绘制规则（从 Figma 提取）、SVG 图标兜底方案，以及相关 AI 规则的更新。

## 当前状态分析

### 已有资源

1. **iconfont 字体库**：`wego-ux-design/resources/fonts/iconfont/` 目录下有完整的 iconfont 资源
   - `iconfont.json`：项目 ID 3553753，名称"微购单色图标库"，font-family `wego-iconfont-s`，css_prefix `icon-`
   - 包含约 300+ 个图标，涵盖业务图标、导航图标、状态图标等
   - `iconfont.css`：定义了 `.wego-iconfont-s` 基础类和所有 `.icon-{font_class}` 类

2. **Token 中的图标相关定义**：
   - `wg.stroke.width.icon` = 1.5px（线性图标默认描边）
   - `wg.stroke.width.icon.strong` = 2.25px（加粗图标描边）

3. **Kuikly Icon 组件参考**：`参考资料/kuikly_doc/basic_components/Icon.md`
   - 使用 `iconName`、`iconSize`、`iconColor` 三个属性
   - iconName 对应 iconfont 的 font_class 字符串

4. **NavBar 中的图标使用**：当前 NavBar 使用 SVG 内联图标，未使用 iconfont

5. **Figma 图标绘制规则**（从节点 1634:25705 提取）：
   - 线粗：1.5
   - 线对齐样式：居中
   - 端点：方（None）
   - 角点：圆
   - 圆角大小：0
   - 尺寸：16/20/24/28/32/48，推荐 16/24/32/48
   - 方形图标边距：24-3；最大圆图标边距：24-2
   - 填充图标添加 1.5 线粗描边（让转角圆润）
   - 命名规则：icon/名称_分类识别符
     - 第一位颜色：黑-b、白-w、灰-h、绿-g、蓝-s、红-r、橙-o、彩色-c
     - 第二位属性：线性-不追加、面性-cell、线面结合-c
   - 图标以 24 为基准绘制，以 4 为梯度缩放
   - 字体-图标搭配：12pt 配 16pt、14pt 配 20pt、16pt 配 24pt
   - 特殊图标：16×16 独立尺寸图标使用 1.5 线粗；勾在列表前使用 2.0 线粗加粗版

### 缺失内容

1. **无图标使用规范文档**：`02-tokens/` 和 `04-ai-rules/` 中均无图标使用规则
2. **Web 原型中图标使用方式未定义**：当前 NavBar 使用 SVG 内联，但 iconfont 字体库已就绪
3. **图标 Token 不完整**：缺少图标尺寸、颜色映射等 Token
4. **AI 生成规则中无图标指引**：生成界面时不知道如何正确使用图标

## 计划变更

### 变更 1：新建图标使用规范文档

**文件**：`wego-ux-design/02-tokens/icon-guidelines.md`

**内容**：
- 图标资源说明（iconfont 字体库 + SVG 兜底）
- 图标使用方式（Web 原型中通过 iconfont class 使用）
- 图标尺寸规范（16/20/24/28/32/48，推荐 16/24/32/48）
- 图标-字号搭配规则
- 图标颜色规则（通过 color 属性 + Token 控制）
- 图标绘制规则（从 Figma 提取的完整规则）
- SVG 兜底方案（当 iconfont 中无所需图标时）
- 命名规则说明

**为什么**：当前设计系统缺少图标使用规范，AI 生成界面时无法正确使用图标。

### 变更 2：更新 AI 规则 — 禁止事项

**文件**：`wego-ux-design/04-ai-rules/05-forbidden-rules.md`

**变更**：在"视觉禁止事项"或新增"图标禁止事项"部分补充：
- 禁止使用非 iconfont 图标（当 iconfont 中存在所需图标时）
- 禁止硬编码图标尺寸（必须使用 Token 或规范尺寸）
- 禁止使用图片替代图标
- 禁止自行创造 iconfont 中不存在的图标样式

**为什么**：确保图标使用的一致性。

### 变更 3：更新 AI 规则 — UI 生成规则

**文件**：`wego-ux-design/04-ai-rules/02-ui-generation-rules.md`

**变更**：在"Token 应用"部分补充图标使用流程：
- 优先从 iconfont 字体库查找图标
- iconfont 中无所需图标时，按绘制规则输出 SVG
- 图标尺寸必须使用规范尺寸
- 图标颜色必须通过 Token 控制

**为什么**：AI 生成界面时需要明确的图标使用流程。

### 变更 4：更新 SKILL.md 任务路由

**文件**：`wego-ux-design/SKILL.md`

**变更**：在生成页面的必读文件中增加 `02-tokens/icon-guidelines.md`。

**为什么**：图标是界面生成的高频需求，必须作为必读文件。

### 变更 5：更新 shared-rules.md

**文件**：`wego-ux-design/03-components/shared-rules.md`

**变更**：补充图标在组件中的使用规则：
- 组件内图标使用 iconfont class
- 图标尺寸由组件规范决定
- 图标颜色继承父元素或使用 Token

**为什么**：组件中经常使用图标，需要统一规则。

## 假设与决策

1. **Web 原型中图标使用 iconfont class 方式**：`<i class="wego-iconfont-s icon-{font_class}"></i>`，而非 SVG 内联。NavBar 中的 SVG 内联图标应逐步迁移为 iconfont 方式。
2. **SVG 兜底方案**：当 iconfont 中不存在所需图标时，按 Figma 绘制规则输出 SVG 内联图标，并标注 iconfont 缺失。
3. **图标尺寸不新增 Token**：图标尺寸使用已有的 `wg.size.*` Token（16/20/24/28/32/48），不单独创建图标尺寸 Token。
4. **图标颜色不新增 Token**：图标颜色继承父元素 `color` 属性，使用已有的 `wg.color.text.*` Token。
5. **iconfont.json 作为图标查询的权威来源**：生成界面时通过读取 iconfont.json 确认图标是否存在。

## 验证步骤

1. 确认 `icon-guidelines.md` 内容完整，覆盖使用方式、尺寸、颜色、绘制规则、SVG 兜底
2. 确认 AI 规则更新后，生成界面时能正确引用图标规范
3. 确认 SKILL.md 任务路由包含图标规范文件
4. 确认 shared-rules.md 补充了组件内图标使用规则
5. 确认所有变更不与现有规则冲突
