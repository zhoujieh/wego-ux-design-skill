# 05 Output Example

> 微购 Design System Skill / 05-examples  
> Version 1.0  
> 本文档提供 AI 输出界面方案的标准示例。

---

# 用户需求

```text
帮我设计一个客户搜索结果为空的页面。
```

---

# 设计说明示例

> 仅当用户明确要求设计说明时参考。页面生成任务的默认交付是完整可运行的项目目录。

## 页面目标

告诉用户当前没有匹配客户，并引导用户调整搜索或新增客户。

---

## 页面类型

```text
空状态
```

---

## 信息层级

一级信息：

```text
无匹配的客户
```

二级信息：

```text
请检查关键词，或尝试新增客户
```

三级信息：

```text
新增客户操作
```

---

## 布局模式

页面布局：

```text
M2
```

分组方式：

```text
G2
```

---

## 组件选择

使用：

```text
空状态图形
主标题
辅助说明
主按钮
```

组件规范缺失时：

```text
当前使用：页面级 Empty 结构
缺失内容：Empty 组件图形、标题、说明、操作区规则
建议补充：HTML 原型 Empty 组件规范
归属位置：03-components/（组件候选，不阻塞当前原型）
```

---

## Token 使用

Color：

```text
标题：wg.color.text.primary
说明：wg.color.text.secondary
页面背景：wg.color.bg.page
主按钮：wg.color.action.primary.default
```

Typography：

```text
标题：wg.font.size.f16 + wg.font.weight.semibold
说明：wg.font.size.f14
```

Spacing：

```text
页面边距：wg.layout.page.m2.margin
标题与说明：wg.spacing.8
说明与按钮：wg.spacing.24
```

Radius：

```text
按钮圆角按组件规范；组件缺失时不自创
```

Copywriting：

```text
标题：wg.copy.empty.search → 无匹配的客户
```

---

## 状态设计

```text
loading：搜索中
empty：无匹配的客户
error：搜索失败，请重试
success：展示搜索结果
```

---

## 自查结果

```text
页面目标清晰
信息层级清晰
使用了空状态文案 Token
未使用硬编码颜色
未创建组件级 Token
组件规范缺失处已标注
```
