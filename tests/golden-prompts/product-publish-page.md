# 商品发布页回归测试

## 测试目标
验证 Skill 能否生成符合微购规范的商品发布页 Web 原型项目，包含多字段表单、图片上传、草稿保存、发布成功等完整链路。

## 输入提示词
使用 $wego-ux-design 生成一个微购商品发布页 Web 原型项目。用户是需要上架新商品的商家，需要填写商品名称、价格、库存、描述并上传商品图片，业务目标是提高商品上架效率。

## 期望页面类型
表单型

## 必须命中的组件
- Input
- Button
- Toast
- Dialog（草稿保存确认）

## 必须覆盖状态
- 初始状态
- 字段为空校验
- 价格格式错误
- 图片上传中
- 图片上传成功
- 图片上传失败
- 草稿保存确认
- 草稿保存成功
- 发布中
- 发布成功
- 发布失败
- 失败后可重新发布

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
- 禁止省略图片上传反馈

## 验收清单
- 输出目录包含 index.html、styles/tokens.css、styles/components.css、styles/app.css、scripts/app.js
- app.css 只使用 var(--wg-*) 表达设计值
- app.js 中存在真实状态切换逻辑
- 表单字段能触发校验
- 图片上传有加载中和成功/失败状态
- 草稿保存有确认和成功反馈
- 发布按钮能触发提交流程
- 失败状态能恢复
- 成功状态有明确结果反馈
