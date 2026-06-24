# 03 Token Usage Example

> 微购 Design System Skill / 05-examples  
> Version 1.0  
> 本文档提供 Token 使用示例。

---

# 1. 正确示例

## 文本

```text
主标题：wg.font.size.f18 + wg.font.weight.semibold
正文：wg.font.size.f14 + wg.font.weight.regular
辅助说明：wg.font.size.f12 + wg.font.weight.regular
```

## 颜色

```text
主文字：wg.color.text.primary
辅助文字：wg.color.text.secondary
页面背景：wg.color.bg.page
内容背景：wg.color.bg.surface
主操作：wg.color.action.primary.default
危险文字：wg.color.text.danger
```

## 间距

```text
强关联：wg.spacing.4
同组内容：wg.spacing.8 / wg.spacing.16
清晰分隔：wg.spacing.24
模块分隔：wg.spacing.32
```

## 圆角

```text
默认圆角：wg.radius.md
大圆角：wg.radius.lg
胶囊圆角：wg.radius.full
```

## 布局

```text
默认业务页面：wg.layout.page.m2.margin
高密度列表：wg.layout.page.m0.margin
紧密分组：G1
宽松分组：G2
```

---

# 2. 错误示例

禁止：

<!-- token-lint: allow-hardcoded reason=negative-example -->

```text
color: #03C160
font-size: 15px
margin: 10px
border-radius: 20px
z-index: 9999
box-shadow: 0 8px 40px rgba(...)
```

---

# 3. 缺失 Token 示例

当缺少 Token 时，不直接新增。

正确输出：

```text
当前使用：wg.spacing.24
原因：缺少专用于「筛选区与结果列表之间」的间距 Token
建议新增：wg.spacing.xxx
归属位置：02-tokens/tokens.json
```
