# 结果页回归测试

## 测试目标
验证 Skill 能否生成符合微购规范的结果页 Web 原型项目，包含成功/失败结果、后续操作引导等完整链路。

## 输入提示词
使用 $wego-ux-design 生成一个微购结果页 Web 原型项目。用户是完成支付后的买家，需要明确知道支付结果并了解后续操作，业务目标是降低用户支付后的焦虑感。

## 期望页面类型
结果型

## 必须命中的组件
- Result（成功/失败反馈）
- Button（后续操作）

## 必须覆盖状态
- 支付成功状态
- 支付失败状态
- 查看订单
- 继续购物
- 重试支付（失败时）

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
- 禁止省略后续操作引导
- 禁止失败状态无重试入口

## 验收清单
- 输出目录包含 index.html、styles/tokens.css、styles/components.css、styles/app.css、scripts/app.js
- app.css 只使用 var(--wg-*) 表达设计值
- app.js 中存在真实状态切换逻辑
- 成功状态有明确的结果反馈
- 失败状态有明确的结果反馈
- 成功状态有后续操作按钮
- 失败状态有重试按钮
- 后续操作按钮可点击并跳转
