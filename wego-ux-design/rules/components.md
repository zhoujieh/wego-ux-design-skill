# 组件消费规则

> 微购 Design System Skill / rules
> 本文档定义设计库组件的发现、读取、复制和禁用边界。

## 权威来源

- 组件发现入口：`design-library/components/index.json`
- 组件契约：`design-library/components/{slug}.json`
- Canonical markup 与 Canonical CSS 来源：`design-library/preview/component-{slug}.html`
- 聚合样式：`design-library/components.css`
- 图标资源：`design-library/assets/fonts/iconfont/`

组件消费前必须先读取 `design-library/library-consumption.json`。

## 组件发现顺序

```text
library-consumption.json
↓
components/index.json
↓
components/{slug}.json
↓
preview/component-{slug}.html
↓
components.css
```

不得扫描整个 `preview/` 或 `components/` 目录自行猜组件，不得跳过契约直接按视觉拼结构。

## 必读字段

读取组件契约时，至少确认：

- `variantDimensions`
- `tokensConsumed`
- `domAnatomy`
- `usageHints`
- `doNotInvent`
- `provenance`

其中：

- `variantDimensions` 决定能用哪些尺寸、强调级、布局和状态
- `domAnatomy` 决定根节点、子节点和 modifier class
- `doNotInvent` 是硬限制，不能突破
- `provenance.preview` 指向要复制 markup 的预览文件
- `knownIssues` 仅供维护者查阅，AI 照搬不修改，不得自行修补

## 复制规则


### 标记定位

每个 `design-library/preview/component-{slug}.html` 中，组件本体由以下标记包裹：

```
<!-- @component-markup-start -->
<!-- @component-markup-end -->
```

AI 复制组件 markup 时，**必须通过这两个标记定位**，只复制标记之间的 HTML 片段，不得依赖语义推断或 class 名猜测边界。
标记之间的内容已是组件本体的完整展示（包含各 variant 示例），可直接按需裁剪使用。
- 组件 markup 只能从 `preview/component-{slug}.html` 复制
- 复制时保留 class 名、修饰符、DOM 层级和辅助节点
- 只复制组件本体，不复制 preview 页面的演示壳、矩阵、标题或说明文案
- 页面中使用到的组件统一依赖 `components.css`，不要把组件样式拆散回写到 `app.css`

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
- 自定义“看起来差不多”的替代 class

## 图标规则

- 组件需要图标时，复制整个 `design-library/assets/fonts/iconfont/` 目录
- HTML 中使用 `<i class="wego-iconfont-s icon-{font_class}"></i>`
- `font_class` 必须来自图标字体资源或项目既有契约，不得臆造
- 只有在 iconfont 明确缺失目标图标时，才按 `rules/icon-guidelines.md` 使用 SVG 兜底

## 未命中组件时

如果 `components/index.json` 中不存在所需组件：

```text
当前使用：
缺失内容：
建议补充：
归属位置：design-library/components/
```

此时可以使用页面级语义结构完成当前原型，但不得宣称为正式设计系统组件，也不得使用 `.wg-{component}` 这类正式命名。
