# Input 组件规范输出计划

## 总结

已完成 Input 组件规范的输出，文件位于 `/Users/dk/Documents/code/wego-design-system/wego-ux-design/03-components/input.md`。

## 当前状态

✅ **已完成**：Input 组件规范文档已创建

规范文档包含以下内容：
- 使用决策：明确何时使用/不使用 Input 组件
- 语义模型：定义 4 个决策维度（layout、type、state、error）
- 允许组合：规定布局、类型、错误状态和单位文本的组合规则
- Anatomy：定义 4 种输入框的 HTML 结构（通栏单行、卡片单行、卡片多行、卡片数字）
- 文案规则：placeholder、错误提示、单位文本的文案要求
- Canonical HTML：提供 7 个标准示例（通栏/卡片、正常/错误/禁用状态）
- Canonical CSS：完整的样式实现，包含所有状态和变体
- 状态：定义 5 种交互状态（default、filled、focused、disabled、error）
- 可访问性：原生元素、disabled 属性、inputmode、aria 关联等要求
- 生成约束：10 条强制规则，确保 AI 正确生成 Input 组件
- 自检：12 项自检清单
- 规范来源：Figma 设计稿和 Kuikly 组件文档的参考说明

## 关键设计决策

### 1. 布局模式
- **full（通栏）**：无边框，无内边距，高度 44px，用于表单页面
- **card（卡片）**：有背景、边框、圆角，高度 36px，用于卡片/弹窗内

### 2. 输入类型
- **text**：单行文本，默认类型
- **multiline**：多行文本，使用 textarea，默认高度 56px
- **number**：数字输入，自动过滤非数字字符，支持单位文本

### 3. 错误状态
- 红色边框 + 浅红背景
- 错误提示文字显示在输入框下方
- 用户重新输入或聚焦时自动清除错误（可禁用）

### 4. Token 使用
所有样式均使用 wego design tokens：
- 颜色：`wg.color.text.primary`、`wg.color.border.default`、`wg.color.status.danger.*` 等
- 尺寸：`wg.size.36`、`wg.size.56`、`wg.touch.default`
- 间距：`wg.spacing.4`、`wg.spacing.8`、`wg.spacing-12`
- 字体：`wg.font.size.16`、`wg.font.lineheight.16`、`wg.font.weight.medium`
- 圆角：`wg.radius.sm`
- 描边：`wg.stroke.width.default`、`wg.stroke.style.solid`

## 验证步骤

1. ✅ 文件已创建在正确位置
2. ⏳ 待验证：检查文件内容是否符合 wego-ux-design 规范模板
3. ⏳ 待验证：确认所有 Token 引用存在于 tokens.json
4. ⏳ 待验证：确认 HTML/CSS 示例可正确渲染

## 后续建议

如需进一步完善，可以：
1. 补充 Input 组件在表单中的使用示例
2. 添加 Input 与其他组件（如 Button、Dialog）的组合示例
3. 创建 Input 组件的 Figma 组件说明文档
4. 编写 Input 组件的测试用例
