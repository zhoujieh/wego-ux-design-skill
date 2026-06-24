# HTML 组件公共规则

本目录定义 AI 生成 Web 原型时使用的正式组件契约，不是 React、Vue、Web Component 或 KuiklyUI 代码库。

## 使用流程

1. 先读取 `registry.json`，根据用户目标识别组件。
2. 只读取被选中组件的规则文件。
3. 先确定组件的语义维度，再选择视觉变体。
4. 复制已注册组件规定的 Anatomy 和 class，不临时改造其内部结构。
5. 只使用组件声明的组合、状态和 Token。

## 规则优先级

```text
组件使用决策
↓
允许组合
↓
Canonical HTML
↓
Canonical CSS
↓
页面布局规则
```

页面布局可以决定组件放在哪里，但不能改变组件内部结构、变体含义和状态行为。

## NavBar 使用场景补充

### 不使用 NavBar 的页面类型

以下页面类型不应使用 NavBar 组件：

| 页面类型 | 原因 | 替代方案 |
|---|---|---|
| 应用入口页面（登录、注册首页、启动页） | 没有"返回"或"关闭"的概念，用户尚未进入应用 | 使用自定义头部区域（Logo + 标题 + 副标题） |
| 沉浸式全屏页面 | 需要完整展示内容，导航栏会干扰 | 使用浮动按钮或手势操作 |
| 弹窗内的标题区域 | 弹窗已有独立的关闭机制 | 使用 Dialog 组件的内置标题结构 |

判断规则：
- 如果页面是用户进入应用的第一个页面，且没有"返回上一级"的概念，则不使用 NavBar
- 如果页面是应用内的二级或更深层级页面，则必须使用 NavBar

## 图标使用

组件内使用图标时遵守 `02-tokens/icon-guidelines.md`：

- 优先使用 iconfont 字体库：`<i class="wego-iconfont-s icon-{font_class}"></i>`
- 图标尺寸由组件规范决定，使用 `wg.size.*` Token
- 图标颜色继承父元素 `color` 属性，或使用 `wg.color.text.*` Token
- iconfont 中不存在所需图标时，按绘制规则输出 SVG 内联图标，并标注缺失
- 不得硬编码图标尺寸和颜色

## 命名约定

```text
组件：       .wg-{component}
组件元素：   .wg-{component}__{element}
组件修饰符： .wg-{component}--{modifier}
组件组：     .wg-{component}-group
```

状态优先使用原生属性和 ARIA：

```text
disabled
aria-expanded
aria-selected
aria-pressed
data-state
```

不得使用只表达颜色或尺寸、不表达语义的临时 class。

## 生成边界

- 不读取 KuiklyUI API 补充 HTML 规则。
- 不允许调用方覆盖颜色、间距、圆角和任意宽高。
- 不允许生成规则未声明的变体和组合。
- 组件 CSS 只能引用 `token-css-map.md` 中存在的变量。
- 组件未定义的状态不得擅自补齐；应标注规范缺失。
- `interactionMode` 描述组件自身的交互实现需求，不限制页面使用 JavaScript 编排业务流程。
- 页面脚本可以监听已注册组件事件、更新原生属性并驱动流程，但不得绕过组件规定的 Anatomy、状态语义和可访问性约束。

## 缺失处理

当 registry 中不存在所需组件时，使用语义化 HTML、页面级 class 和 JavaScript 完成当前原型，不阻塞交互链路。页面级实现：

- 不使用 `.wg-{component}` 命名。
- 不写入 registry，不宣称为正式组件。
- 仍使用 Token，并满足语义、状态和可访问性要求。
- 具有复用价值时标记为“组件候选”。

当已注册组件无法表达所需变体时，保持正式组件不变，在页面层组合反馈结构，并输出：

```text
当前使用：
缺失内容：
建议补充：
归属位置：03-components/
```

页面级临时结构不得被描述为正式组件规范。
