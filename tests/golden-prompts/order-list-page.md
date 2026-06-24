# 订单列表页回归测试

## 测试目标
验证 Skill 能否生成符合微购规范的订单列表页 Web 原型项目，包含列表加载、空状态、下拉刷新、分页等完整链路。

## 输入提示词
使用 $wego-ux-design 生成一个微购订单列表页 Web 原型项目。用户是需要查看和管理订单的商家，需要浏览订单列表、筛选订单状态、查看详情，业务目标是提高订单管理效率。

## 期望页面类型
浏览型

## 必须命中的组件
- NavBar
- Tabs（订单状态筛选）
- Button

## 必须覆盖状态
- 初始加载中
- 列表加载成功
- 列表为空（空状态）
- 下拉刷新中
- 下拉刷新成功
- 分页加载中
- 分页加载成功
- 分页加载失败
- 网络错误

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
- 禁止省略加载中和空状态
- 禁止跳过错误处理

## 验收清单
- 输出目录包含 index.html、styles/tokens.css、styles/components.css、styles/app.css、scripts/app.js
- app.css 只使用 var(--wg-*) 表达设计值
- app.js 中存在真实状态切换逻辑
- 列表有加载中状态
- 列表为空时有空状态反馈
- 下拉刷新有视觉反馈
- 分页加载有加载指示器
- 网络错误有重试机制
