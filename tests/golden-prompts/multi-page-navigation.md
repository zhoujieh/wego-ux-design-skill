# 多页导航回归测试

## 测试目标
验证 Skill 能否生成符合微购规范的多页导航 Web 原型项目，包含页面跳转、返回、NavBar 联动、背景色继承等完整链路。

## 输入提示词
使用 $wego-ux-design 生成一个微购多页导航 Web 原型项目。用户是需要浏览商品详情并返回的买家，需要流畅的页面切换体验，业务目标是提高浏览效率。

## 期望页面类型
浏览型

## 必须命中的组件
- NavBar
- Button

## 必须覆盖状态
- 首页展示
- 点击商品跳转详情页
- 详情页展示
- 详情页返回
- NavBar 背景色联动
- 返回动画

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
- 禁止 NavBar 背景色硬编码
- 禁止返回按钮无响应
- 禁止跳过页面过渡动画

## 验收清单
- 输出目录包含 index.html、styles/tokens.css、styles/components.css、styles/app.css、scripts/app.js
- app.css 只使用 var(--wg-*) 表达设计值
- app.js 中存在真实状态切换逻辑
- 首页可点击商品跳转详情页
- 详情页有 NavBar
- NavBar 背景色随页面背景动态变化
- 详情页有返回按钮
- 返回按钮点击后返回首页
- 页面切换有过渡动画
