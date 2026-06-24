# 登录页回归测试

## 测试目标
验证 Skill 能否生成符合微购规范的登录页 Web 原型项目，包含完整的表单校验、提交、成功/失败状态闭环。

## 输入提示词
使用 $wego-ux-design 生成一个微购登录页 Web 原型项目。用户是首次进入微购后台的商家，需要输入手机号和验证码完成登录，业务目标是降低首次登录成本。

## 期望页面类型
表单型

## 必须命中的组件
- Input
- Button
- Toast
- Result 或页面级成功反馈

## 必须覆盖状态
- 初始状态
- 手机号为空
- 手机号格式错误
- 验证码为空
- 提交中
- 登录成功
- 登录失败
- 失败后可重新提交

## 必须使用 Token 类别
- color
- typography
- spacing
- radius
- size
- layout
- motion
- z-index

## 禁止问题
- 禁止输出单文件 HTML
- 禁止内联 style
- 禁止内联 script
- 禁止业务 CSS 硬编码 HEX / px / rgba
- 禁止只静态展示多个状态
- 禁止跳过失败恢复路径

## 验收清单
- 输出目录包含 index.html、styles/tokens.css、styles/components.css、styles/app.css、scripts/app.js
- app.css 只使用 var(--wg-*) 表达设计值
- app.js 中存在真实状态切换逻辑
- 提交按钮能触发表单校验
- 失败状态能恢复
- 成功状态有明确结果反馈
