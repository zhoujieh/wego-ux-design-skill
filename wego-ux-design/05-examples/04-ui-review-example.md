# 04 UI Review Example

> 微购 Design System Skill / 05-examples  
> Version 1.0  
> 本文档提供界面审查输出示例。

---

# 示例：审查一个商品列表页

## 结论

当前界面主要问题是信息密度不足、主次层级不清、Token 使用不统一。

---

## P0 问题

问题：

```text
商品列表中主操作和次操作视觉权重相同，用户难以判断下一步。
```

原因：

```text
同一区域存在多个强焦点。
```

修改建议：

```text
只保留一个主操作，其余操作降级为文本操作或次操作。
```

---

## P1 问题

问题：

```text
列表间距过大，影响高密度商品浏览效率。
```

原因：

```text
高密度列表没有使用 M0 / G1。
```

修改建议：

```text
页面布局改为 M0，连续商品信息使用 G1。
```

---

## P1 问题

问题：

```text
价格、标签、状态同时使用高饱和色。
```

原因：

```text
颜色语义混乱。
```

修改建议：

```text
价格使用 wg.color.text.promotion
状态使用对应的 `wg.color.state.*` Token
普通标签降级为中性色
```

---

## P2 问题

问题：

```text
辅助说明字号过大。
```

原因：

```text
辅助信息使用了正文层级。
```

修改建议：

```text
辅助说明改为 F12。
```

---

## Token 检查

合规：

```text
使用了 wg.color.text.primary
使用了 wg.radius.md
```

不合规：

<!-- token-lint: allow-hardcoded reason=review-input -->

```text
margin: 10px
font-size: 15px
border-radius: 20px
```

---

## 交互链路检查

已覆盖：

```text
商品点击进入详情
加载失败后可以重试
```

缺失或断链：

```text
批量操作提交后没有处理中状态
删除失败后没有恢复路径
```

---

## 最终建议

优先修改：

```text
1. 降低次操作权重
2. 商品列表改为高密度布局
3. 修正颜色语义
4. 替换所有未定义 Token
5. 补齐批量操作和删除失败的状态闭环
```
