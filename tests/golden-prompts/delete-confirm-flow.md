# 删除确认流程回归测试

## 测试目标
验证 Skill 能否生成符合微购规范的删除确认流程 Web 原型项目，包含危险操作确认、取消、成功反馈、列表更新等完整链路。

## 输入提示词
使用 $wego-ux-design 生成一个微购删除确认流程 Web 原型项目。用户是需要删除商品的商家，需要二次确认删除操作，业务目标是防止误删并给出明确的操作反馈。

## 期望页面类型
操作型

## 必须命中的组件
- Button
- Dialog（删除确认）
- Toast（操作反馈）

## 必须覆盖状态
- 初始状态（列表展示）
- 点击删除按钮
- 删除确认弹窗展示
- 确认删除
- 取消删除
- 删除中
- 删除成功
- 删除失败
- 失败后可重试
- 列表更新（删除项移除）

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
- 禁止跳过确认弹窗
- 禁止跳过失败恢复路径
- 禁止删除后不更新列表

## 验收清单
- 输出目录包含 index.html、styles/tokens.css、styles/components.css、styles/app.css、scripts/app.js
- app.css 只使用 var(--wg-*) 表达设计值
- app.js 中存在真实状态切换逻辑
- 点击删除按钮弹出确认弹窗
- 确认弹窗可取消
- 确认删除有加载状态
- 删除成功有 Toast 反馈
- 删除失败可重试
- 删除成功后列表项移除
