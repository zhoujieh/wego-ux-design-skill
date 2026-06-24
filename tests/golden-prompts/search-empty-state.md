# 搜索空状态回归测试

## 测试目标
验证 Skill 能否生成符合微购规范的搜索空状态 Web 原型项目，包含搜索输入、空结果反馈、推荐引导等完整链路。

## 输入提示词
使用 $wego-ux-design 生成一个微购搜索空状态 Web 原型项目。用户是在微购后台搜索商品但未找到结果的商家，需要清晰的空状态反馈和后续操作引导，业务目标是降低用户搜索失败后的挫败感。

## 期望页面类型
空状态型

## 必须命中的组件
- Input（搜索框）
- Button（推荐操作）
- Result（空状态反馈）

## 必须覆盖状态
- 初始状态（搜索框聚焦）
- 输入中
- 搜索中
- 搜索完成有结果
- 搜索完成无结果（空状态）
- 空状态下推荐操作
- 点击推荐操作后跳转

## 必须使用 Token 类别
- color
- typography
- spacing
- radius
- size
- layout
- motion

## 禁止问题
- 禁止输出单文件 HTML
- 禁止内联 style
- 禁止内联 script
- 禁止业务 CSS 硬编码 HEX / px / rgba
- 禁止只静态展示多个状态
- 禁止省略空状态反馈
- 禁止省略推荐引导

## 验收清单
- 输出目录包含 index.html、styles/tokens.css、styles/components.css、styles/app.css、scripts/app.js
- app.css 只使用 var(--wg-*) 表达设计值
- app.js 中存在真实状态切换逻辑
- 搜索框能触发搜索
- 搜索中有加载状态
- 无结果时有清晰的空状态反馈
- 空状态下有推荐操作引导
- 推荐操作可点击并跳转
