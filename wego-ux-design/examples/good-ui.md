# Good UI Example

> 微购 Design System Skill / examples
> Version 1.0  
> 本文档提供符合微购风格的界面输出示例。

---

# 示例：订单提交页

## 页面目标

帮助用户确认订单金额、核对商品信息，并完成提交。

---

## 页面类型

```text
操作型 + 表单确认型
```

---

## 信息层级

一级信息：

```text
应付金额
提交订单按钮
```

二级信息：

```text
商品列表
客户信息
配送信息
```

三级信息：

```text
优惠、备注、辅助说明
```

弱信息：

```text
时间、编号、次要状态
```

---

## 布局模式

页面布局：

```text
M2
```

分组方式：

```text
G2 用于模块组
G1 用于连续信息行
```

---

## Token 使用

Color：

```text
主文字：wg.color.text.primary
辅助文字：wg.color.text.secondary
页面背景：wg.color.bg.page
内容表面：wg.color.bg.surface
主操作：wg.color.action.primary.default
价格：wg.color.text.promotion
```

Typography：

```text
金额：wg.font.number.nf24
正文：wg.font.size.f14
辅助说明：wg.font.size.f12
```

Spacing：

```text
页面边距：wg.layout.page.m2.margin
模块间距：wg.layout.group.g2.outside
同组间距：wg.spacing.8
```

Radius：

```text
容器圆角：wg.radius.md
```

---

## 状态补充

```text
loading：提交中
disabled：信息未完整时禁用提交
error：提交失败，请重试
success：订单提交成功
```

---

# 为什么这是好界面

它符合：

- 页面目标清晰
- 主操作明确
- 信息层级稳定
- Token 使用合规
- 没有额外装饰
- 状态完整
