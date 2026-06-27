# 组件消费规则

> 微购 Design System Skill / rules
> Version 3.0
> 本文档定义跨组件的语义规则。单组件的契约、变体、anatomy 和禁止事项以 `design-library/components/{slug}.json` 和 `design-library/library-consumption.json` 为准。

## 权威来源

- 组件发现入口：`design-library/components/index.json`
- 组件契约：`design-library/components/{slug}.json`
- Canonical markup 来源：`design-library/preview/component-{slug}.html`（通过 `@component-markup-start` / `@component-markup-end` 标记定位）
- 聚合样式：`design-library/components.css`
- 图标资源：`design-library/assets/fonts/iconfont/`
- 消费入口与硬约束：`design-library/library-consumption.json`

组件消费前必须先读取 `design-library/library-consumption.json`。

## 组件发现顺序

```text
library-consumption.json → components/index.json → components/{slug}.json → preview/component-{slug}.html → components.css
```

不得扫描整个 `preview/` 或 `components/` 目录自行猜组件，不得跳过契约直接按视觉拼结构。

## 标记定位

每个 `design-library/preview/component-{slug}.html` 中，组件本体由以下标记包裹：

```
<!-- @component-markup-start -->
<!-- @component-markup-end -->
```

AI 复制组件 markup 时，**必须通过这两个标记定位**，只复制标记之间的 HTML 片段。标记之间已是组件本体的完整展示（包含各 variant 示例），可直接按需裁剪使用。不得依赖语义推断或 class 名猜测边界。

## 页面级可写范围

允许自己写的只有：

- 页面容器布局
- 组件之间的排列关系
- 页面级业务态（如局部显隐、流程切换）
- 组件外层的辅助说明区、空态编排、列表分组

不允许自己写的包括：

- 组件内部字号、颜色、圆角、边框、状态色
- 组件内部节点的结构改写
- 契约中不存在的 modifier
- 自定义"看起来差不多"的替代 class

## 选择控件语义

- 多项独立授权、多选列表、批量选择使用 Checkbox。
- 互斥选项、单选列表、二选一/多选一设置使用 Radio。
- Cell 左侧选择槽位只承载对应语义的 `checkbox` / `radio` 组件，不得用 radio 表达多项权限，也不得用 checkbox 表达互斥选择。
- Checkbox、Radio、Switch 在可交互页面和 UI Kit showcase 中都必须可点击，并同步 `aria-checked` 与对应 checked/on class。
- 静态并列展示只允许出现在组件 preview 的状态矩阵；页面和 showcase 不得把关键状态做成不可操作截图。

## 文字链语义

- 所有可点击文字链必须使用 Link 组件 `.wg-link`，包括设置页右侧操作、帮助入口、切换岗位、查看设置等。
- Cell 右侧动作区可以承载 Link 组件，但不得用页面级 class 自定义链接颜色、字号或 pressed 态。
- 只有不可点击的纯文本值才使用 `.wg-cell__action-text`。

## 未命中组件时

如果 `components/index.json` 中不存在所需组件：

```text
当前使用：
缺失内容：
建议补充：
归属位置：design-library/components/
```

此时可以使用页面级语义结构完成当前原型，但不得宣称为正式设计系统组件，也不得使用 `.wg-{component}` 这类正式命名。
