# 02 UI Generation Rules

> 微购 Design System Skill / 04-ai-rules  
> Version 2.0  
> 本文档定义 AI 生成微购界面时的流程和规则。

---

# 1. 生成目标

AI 生成界面时，必须优先保证：

1. 任务目标清晰
2. 信息层级明确
3. 布局节奏稳定
4. 组件选择正确
5. Token 使用合规
6. 状态完整
7. 微购风格一致

---

# 2. 页面目标

生成前必须回答：

```text
这个页面帮助用户完成什么？
用户进入页面后第一眼应该看到什么？
用户下一步应该做什么？
```

如果页面目标不清晰，不得直接堆组件。

---

# 3. 页面类型

必须判断页面类型：

```text
浏览型
操作型
表单型
结果型
异常型
空状态
```

不同页面类型决定不同的信息密度和布局方式。

---

# 4. 信息层级

默认层级：

```text
一级：页面核心目标 / 关键结果 / 主标题
二级：主要内容 / 主要表单 / 主要列表
三级：辅助说明 / 状态解释 / 次要信息
四级：弱提示 / 时间 / 标签 / 占位内容
```

规则：

- 一个页面只允许一个核心视觉重心
- 主操作必须清晰
- 辅助信息必须弱化
- 状态信息必须靠近对应对象

---

# 5. 布局选择

页面布局按 `02-tokens/token-usage-guidelines.md` 选择，具体 Token 以 `02-tokens/token-reference.md` 为准。

默认规则：

```text
普通业务页面：M2
高密度列表：M0
通栏连续列表：M1
低密度聚焦页面：M3
```

分组规则：

```text
连续紧密信息：G1
宽松模块信息：G2
```

禁止随意新增 M / G 模式。

### 页面背景色

按页面内容结构选择：

- 多卡片/多模块页面 → 页面背景 `bg-page`（灰色），卡片背景 `bg-surface`（白色）
- 聚焦型单任务页面 → 页面背景 `bg-surface`（白色），不使用卡片容器

#### 页面层级与背景色

二级及以下页面的背景色选择规则：

| 场景 | 背景色规则 | 示例 |
|---|---|---|
| 一级页面是白底（聚焦型） | 二级页面继承白底，保持视觉连续性 | 登录（白底）→ 注册（白底） |
| 一级页面是灰底（多模块型） | 二级页面根据内容结构独立选择 | 首页（灰底）→ 详情（白底） |
| 跨层级跳转 | 目标页面按自身内容结构选择背景色 | 任意页面 → 设置页（灰底） |

实现规则：
- 二级页面通过 `.page` 容器的 `background-color` 声明背景色
- 如果继承一级页面背景色，使用相同的 Token（`bg-surface` 或 `bg-page`）
- 如果独立选择，按"页面背景色"章节的规则判断

### 页面宽度约束

页面容器必须设置最大宽度，防止在大屏设备上内容过度拉伸：

| 页面类型 | 最大宽度 | 适用场景 |
|---|---|---|
| 默认业务页面 | 670px | 大多数表单、详情、列表页面 |
| 沉浸式页面 | 无限制 | 视频播放、图片预览等全屏内容 |
| 特殊指定 | 按需求定义 | 需在阶段二明确标注 |

实现方式：
- 页面容器设置 `max-inline-size: var(--wg-layout-page-max-width)` 和 `margin-inline: auto`
- 内容区域在最大宽度内居中显示

### 页面高度

- 页面容器默认 `block-size: 100vh`（兼容环境使用 `100dvh`），占满一屏，不使用 `min-height`。
- 内容不超出时不滚动（`overflow: hidden`）；内容超出时允许滚动（`overflow-y: auto`）。
- 表单型、结果型、聚焦型页面通常不超出 → 禁止滚动；浏览型、列表型页面通常超出 → 允许滚动。

### 滚动条

所有可滚动区域必须隐藏浏览器默认滚动条，保持移动端 App 的视觉一致性。

```css
/* 全局滚动条隐藏 — 写入 app.css */
* {
  scrollbar-width: none;          /* Firefox */
  -ms-overflow-style: none;       /* IE / Edge */
}

*::-webkit-scrollbar {
  display: none;                  /* Chrome / Safari / 新版 Edge */
}
```

禁止出现浏览器默认滚动条。滚动能力通过 `overflow-y: auto` 保留，但视觉上不可见。

---

# 6. Token 应用

生成界面时按场景应用：

```text
Color
Typography
Spacing
Radius
Size
Layout
Elevation
Stroke
Blur
Motion
Z-Index
Copywriting
```

只使用当前界面实际需要的类别，不为满足清单而强行添加阴影、模糊、动效或层级。

不得直接写硬编码设计值。

### 图标使用

生成界面时涉及图标的流程：

```text
读取 iconfont.json 确认图标是否存在
↓
存在 → 使用 iconfont class 渲染
↓
不存在 → 按绘制规则输出 SVG 内联图标，并标注缺失
```

规则：

- 所有图标优先使用 iconfont 字体库（`wego-iconfont-s`）
- 图标尺寸使用 `wg.size.*` Token，不得硬编码
- 图标颜色通过 `color` 属性 + `wg.color.*` Token 控制，不得硬编码
- 图标与文字搭配时遵循字号-图标尺寸对应关系（详见 `02-tokens/icon-guidelines.md`）
- SVG 兜底图标必须遵守绘制规则：线粗 1.5、端点方、角点圆
- 使用 SVG 兜底时必须标注 iconfont 缺失

### 基础重置

Token 间距生效的前提是浏览器默认间距已清除。`tokens.css` 已包含基础重置块，覆盖 `body`、`h1`~`h6`、`p`、`ul`/`ol`、`dl`、`figure`、`blockquote`、`hr`、`fieldset`、`pre` 等元素的默认 margin/padding。

生成页面时必须：

1. 引入包含基础重置的 `tokens.css`，不得使用缺少重置块的版本
2. 不在业务样式中自行修补浏览器默认间距（如对 `p` 单独写 `margin: 0`）
3. 所有间距由 Token 控制，浏览器默认值不得参与布局计算

---

# 7. 组件选择

当前阶段生成可交互 Web 原型项目。`03-components/` 中只允许存在 Web 原型组件契约，不得放入或引用 KuiklyUI API。

组件选择流程：

```text
读取 registry
↓
根据用户目标匹配主流程组件
↓
扫描页面中是否存在辅助交互元素（链接、提示、空状态等）
↓
将辅助元素匹配到 registry 中对应组件（如 <a> → Link、空态提示 → Result）
↓
读取 shared-rules 和所有被选中组件文件
↓
先确定每个组件的语义维度
↓
使用 Canonical HTML / CSS 生成
```

辅助元素扫描规则：
- 页面中存在 `href` 不为空的 `<a>` 标签时，必须检查 Link 组件并匹配 `standalone` 或 `inline` context
- 页面中存在可点击的文字按钮（非 `<button>` 标签）时，必须检查 Link 组件的 `command` behavior
- 辅助元素匹配到的组件与其他命中组件同等对待 — 必须读取规范文件、使用 Canonical HTML/CSS

不得扫描整个组件目录，也不得根据视觉相似度自行选择尺寸或变体。

如果 HTML 组件规范缺失：

```text
当前使用：
缺失内容：
建议补充：
归属位置：
```

不得把临时设计声明为正式组件规范，也不得使用 KuiklyUI 实现细节替代 Web 原型规则。组件尚未注册时，使用页面级语义结构继续实现完整交互，并标记为组件候选。

已注册组件必须遵守：

- 使用决策和禁用场景
- 语义维度
- 允许组合
- Anatomy
- Canonical HTML / CSS
- 适用状态
- 可访问性约束

---

# 8. 状态补全

已注册组件只使用对应组件规则声明的视觉状态。业务流程状态由页面层完整实现。

例如 Button V1 只定义：

```text
default
hover
pressed
focus-visible
disabled
```

组件未声明的 `loading`、`error`、`success` 等状态不得作为该组件的新变体；应通过页面级反馈、原生属性、相邻状态区域或未注册的临时结构表达。

涉及不可逆操作时必须补齐：

```text
确认文案
后果说明
取消路径
失败恢复
```

---

# 9. 页面转场

原型中的页面切换必须模拟 App 原生导航体验，不得使用 `display: none/flex` 硬切。

### 转场类型

| 导航类型 | 进入方向 | 退出方向 | 适用场景 |
|---|---|---|---|
| 推入（Push） | 从右侧滑入 | 向右侧滑出 | 二级页面进入：从一级页面进入详情、表单、设置等子页面 |
| 弹出（Present） | 从底部滑入 | 向底部滑出 | 全屏模态：绑定手机号、独立流程、需要关闭而非返回的页面 |
| 淡入（Fade） | 渐显 | 渐隐 | 同级切换：Tab 切换、登录方式切换等不涉及层级变化的场景 |

### 转场参数

| 参数 | 推入（Push） | 弹出（Present） | 淡入（Fade） |
|---|---|---|---|
| 时长 | `wg.motion.duration.normal`（250ms） | `wg.motion.duration.normal`（250ms） | `wg.motion.duration.fast`（150ms） |
| 缓动 | `wg.motion.ease.emphasized` | `wg.motion.ease.emphasized` | `wg.motion.ease.standard` |
| 进入起始 | `translateX(100%)` | `translateY(100%)` | `opacity: 0` |
| 进入终态 | `translateX(0)` | `translateY(0)` | `opacity: 1` |
| 退出起始 | `translateX(0)` | `translateY(0)` | `opacity: 1` |
| 退出终态 | `translateX(100%)` | `translateY(100%)` | `opacity: 0` |

### 实现方式

视图容器使用绝对定位堆叠，通过 CSS `transform` + `transition` 实现转场动画：

```css
.view {
  position: absolute;
  inset: 0;
  transition:
    transform var(--wg-motion-duration-normal) var(--wg-motion-ease-emphasized),
    opacity var(--wg-motion-duration-normal) var(--wg-motion-ease-standard);
}

/* 推入型视图 — 默认隐藏在右侧 */
.view[data-position="right"] {
  transform: translateX(100%);
  opacity: 0;
  pointer-events: none;
}

/* 弹出型视图 — 默认隐藏在底部 */
.view[data-position="bottom"] {
  transform: translateY(100%);
  opacity: 0;
  pointer-events: none;
}

/* 激活态 */
.view[data-active="true"] {
  transform: translateX(0);
  opacity: 1;
  pointer-events: auto;
}
```

### 判断流程

```text
新页面与当前页面是什么关系？
├─ 层级深入（详情、表单、子页面）→ 推入（Push）
├─ 独立流程（绑定、授权、全屏操作）→ 弹出（Present）
└─ 同级切换（Tab、模式切换）→ 淡入（Fade）
```

### 约束

- 不得使用 `display: none` 切换视图，必须使用 `transform` + `opacity` 实现连续动画。
- 推入时，底层页面保持不动（不跟随滑动），与 iOS 原生行为一致。
- 弹出时，底层页面可添加轻微缩放效果（`scale(0.95)`）增强层次感，但不强制。
- 转场期间，退出页面的交互必须禁用（`pointer-events: none`）。

### 返回按钮交互规则

返回按钮的交互逻辑必须与页面进入的转场类型匹配：

| 进入转场类型 | 返回按钮行为 | 退出动画 |
|---|---|---|
| 推入（Push） | 点击返回，当前页面向右滑出，底层页面恢复交互 | `translateX(100%)` |
| 弹出（Present） | 点击返回/关闭，当前页面向下滑出，底层页面恢复交互 | `translateY(100%)` |
| 淡入（Fade） | 点击返回，当前页面淡出，底层页面恢复交互 | `opacity: 0` |

实现规则：
- 返回按钮必须绑定 `click` 事件，调用视图切换函数
- 视图切换函数必须根据当前视图的 `data-position` 属性决定退出动画方向
- 退出完成后，底层页面必须恢复 `pointer-events: auto`
- 禁止返回按钮无响应或响应后无动画效果

---

# 10. 交互实现

原型必须覆盖用户任务的完整链路，包括适用的：

```text
初始状态
输入与校验
触发操作
处理中
成功结果
失败反馈与重试
取消、返回或撤销
空状态与数据恢复
页面或步骤跳转
```

可使用原生 JavaScript、模块化脚本、框架、Mock 数据、本地存储或本地服务。实现方式不设统一限制，以可运行、可验证和符合用户任务为准。

不能只用静态 DOM 同时陈列所有状态来代替真实状态转换。

---

# 11. 项目组织

生成任务交付完整项目目录：

```text
index.html
styles/tokens.css
styles/components.css
styles/app.css
scripts/app.js
assets/（按需）
```

HTML 只承载语义结构和资源引用；已注册组件的 Canonical CSS 写入 `styles/components.css`；页面级业务样式写入 `styles/app.css`；交互逻辑放在独立 JavaScript 或框架模块中。样式加载顺序：`tokens.css` → `components.css` → `app.css`，确保组件样式不被业务样式意外覆盖。使用构建工具时，保留等价的职责分离，并声明启动命令。

---

# 12. 生成输出格式

输出形式由 `SKILL.md` 决定。

页面或组件原型生成任务默认交付完整可运行项目目录。页面目标、信息层级、组件选择、Token 使用和自查属于生成过程，不默认作为说明文字输出。

最终说明至少提供项目入口、启动方式和已验证的关键交互；用户明确要求设计说明时，再补充简短设计说明。

---

# 13. 禁止事项

禁止：

- 未判断页面目标直接生成界面
- 未建立信息层级直接写视觉
- 使用随机间距
- 使用随机圆角
- 使用随机颜色
- 将页面级临时结构声明为正式组件
- 大量使用装饰性视觉
- 用阴影和颜色替代信息结构
- 只展示静态状态而不实现关键交互
- 将业务 CSS 或交互脚本内联到 HTML
