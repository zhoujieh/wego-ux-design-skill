# Cell 组件规范创建计划

## 概述

基于 Figma 设计文档（`📙 wegoo 组件应用场景`，节点 `586:134408`）中的 Cell 使用场景规则，结合 Kuikly `Cell` 组件文档，创建符合 wego-ux-design 技能规范的 Cell 组件文件，并注册到 `registry.json`。

## 当前状态分析

### 已有组件
- `03-components/` 下已有 9 个组件：button、link、navbar、tabs、dialog、actionsheet、input、toast、result
- `registry.json` 中无 Cell 注册
- 无 `cell.md` 文件

### 从 Figma 提取的 Cell 使用场景

**命名表（3 个样式变体）：**
1. **Cell** — 基础列表单元格，标题+操作区
2. **Cell_Avatar** — 带头像的列表单元格
3. **Cell_Action** — 带选择操作的列表单元格

**使用场景说明：**
- **Cell**：跳转入口；开关项。Cell 用于导航与查看信息，没有保存的概念；Form 是为了提交保存而存在。Form 里也有跳转的分支，样式与 Cell 几乎一致，但前者是因为设置项比较复杂，需要跳转或拉起弹窗进行设置，其本身仍然需要提交保存。Switch 开关有及时生效的属性，所以开关本身不依赖于保存提交，故属于 Cell 的一类用法。在 Form，开关可用于控制设置项的显示与否，但不能用于设置值。
- **Cell_Avatar**：作为展示多条相关信息使用。标题后面支持带标签信息、标题二级信息作为用法解释、支持展示数据、支持自定义入口、表单右边支持附加操作、可显示附加信息。
- **Cell_Action**：作为列表切换成选择时使用。

### 从 Kuikly 文档提取的 API 参考

- **四区域布局**：选择区(36px) → 头像区(+12px间距) → 内容区(flex 1) → 操作区
- **操作区类型**：JUMP_TO（箭头跳转）、TEXT（纯文本）、SWITCH（开关）、BUTTON（按钮）、CUSTOM（自定义）
- **分割线**：true（右侧到头）、null（右侧保留16px间距）、false（不显示）
- **颜色预设**：WHITE（白色+bg_gray_06点击态）、GREY（bg_gray_03+bg_gray_10点击态）
- **高度**：56px（单行）、72px（双行/带副标题）
- **点击态**：isClickable = true 时整个 Cell 有按下变色效果
- **宽度优先级**：优先压缩操作区宽度以保证标题可读性

## 提议变更

### 1. 创建 `wego-ux-design/03-components/cell.md`

按照现有组件规范格式（参考 button.md、actionsheet.md、input.md），创建 Cell 组件规范文件，包含以下章节：

- **使用决策**：使用/不使用 Cell 的场景判断，与 Form 的区别说明
- **语义模型**：4 个决策维度
  - `variant`：Cell / Cell_Avatar / Cell_Action
  - `action`：jump / text / switch / button / custom（操作区类型）
  - `divider`：full / inset / none（分割线样式）
  - `state`：default / pressed / disabled
- **允许组合**：各变体与操作类型的合法组合
- **Anatomy**：四区域 HTML 结构
- **文案规则**：标题、副标题、操作区文本规则
- **Canonical HTML**：各变体的 HTML 示例
- **Canonical CSS**：完整的 CSS 规则（使用 var(--wg-*) Token）
- **状态**：交互状态表
- **可访问性**：ARIA 规则
- **生成约束**：组件使用约束
- **自检**：自查清单
- **规范来源**：Figma 节点 + Kuikly 参考说明

**关键设计决策：**
- V1 仅支持 3 个变体（Cell / Cell_Avatar / Cell_Action），与 Figma 命名表一致
- 操作区 5 种类型映射到 CSS 修饰符：`--jump`、`--text`、`--switch`、`--button`、`--custom`
- 分割线 3 种样式映射到：`--divider-full`、`--divider-inset`、无修饰符（不显示）
- 高度：单行 56px（`--wg-size-56`），双行 72px（`--wg-size-72`）
- 颜色预设：白色背景（默认）、灰色背景（`--grey` 修饰符）
- V1 不支持：退格区（showBackSpace）、标题图标（titleIcon）、标题自定义内容（titleCustomContent）、副标题自定义富文本（subtitleCustomContent）、操作区自定义内容（actionCustomContent）、徽章（Badge）

### 2. 修改 `wego-ux-design/03-components/registry.json`

在 `components` 数组末尾添加 Cell 组件注册：

```json
{
  "id": "cell",
  "name": "Cell",
  "category": "display",
  "status": "stable",
  "file": "cell.md",
  "keywords": [
    "列表",
    "cell",
    "单元格",
    "列表项",
    "设置项",
    "跳转",
    "开关",
    "头像列表",
    "选择列表"
  ],
  "decisionAxes": {
    "variant": ["default", "avatar", "action"],
    "action": ["jump", "text", "switch", "button", "custom"],
    "divider": ["full", "inset", "none"],
    "state": ["default", "pressed", "disabled"]
  },
  "interactionMode": "css+js"
}
```

**分类决策**：Cell 归入 `display` 类别（展示类组件），因为它主要用于导航和查看信息，而非触发操作（action）或收集输入（form）。

**交互模式决策**：`css+js`，因为 Switch 操作需要 JS 控制开关状态。

## 假设与决策

1. **V1 范围裁剪**：Figma 和 Kuikly 中有很多高级功能（退格区、标题图标、徽章、自定义内容插槽等），V1 仅实现 Figma 命名表中明确展示的样式变体和基础操作类型
2. **Cell 与 Form 的区分**：Cell 用于导航与查看（无保存概念），Form 用于提交保存。两者视觉相似但语义不同
3. **category 选择**：Cell 归入 `display` 而非 `form`，因为 Cell 本身不负责数据提交
4. **分割线命名**：使用 `full`（右侧到头）和 `inset`（右侧保留间距）与 Figma 的 `true`/`null`/`false` 三态对应
5. **Switch 交互**：V1 中 Switch 作为 Cell 操作区的一部分，需要 JS 控制状态切换

## 验证步骤

1. 运行 `cd wego-ux-design && python scripts/validate_tokens.py` 校验 Token 引用合规
2. 运行 `cd wego-ux-design && python scripts/validate_skill.py` 校验技能路由和项目契约
3. 检查 `cell.md` 中所有 `var(--wg-*)` 引用是否在 `tokens.json` 中存在
4. 检查 `registry.json` 格式是否正确（JSON 语法、必填字段完整）
5. 检查 `cell.md` 格式是否与现有组件规范一致（章节结构、Token 引用方式、CSS 编写规范）
