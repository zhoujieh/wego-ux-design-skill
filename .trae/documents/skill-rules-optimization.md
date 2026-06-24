# Skill 规则优化计划 — 基于登录注册原型案例的问题分析

## 摘要

基于「微购相册」登录注册原型案例中暴露的 5 个设计问题，优化 wego-ux-design skill 规则文件，使 AI 在后续生成原型时能自动遵循正确的设计决策。

---

## 当前状态分析

### 问题 1：按钮宽度规则不够明确

**现状：** `button.md` 的 Scope 表格中，`page` 级按钮宽度规则为：
- 单个或纵向排列使用 `wg.component.button.width.page.single`（180px）
- 横向成对使用 `wg.component.button.width.page.paired`（120px）

**问题：** 登录场景中，page 级单按钮 180px 固定宽度在表单型页面中显得过窄，实际需要自适应容器宽度（M2 布局下 343px）。当前规则缺少「自适应宽度」的适用场景说明，AI 无法判断何时使用固定宽度、何时使用自适应宽度。

**根因：** 规则只定义了固定宽度的 Token 值，缺少宽度策略的决策逻辑——即何时用固定宽度、何时用自适应宽度。

### 问题 2：滚动条未隐藏

**现状：** `02-ui-generation-rules.md` 第 5 节「页面高度」只规定了何时允许滚动（`overflow-y: auto`）和禁止滚动（`overflow: hidden`），未提及滚动条的视觉处理。

**问题：** 原型中 `overflow-y: auto` 会显示浏览器默认滚动条，破坏移动端视觉体验。移动端 App 中滚动条通常是隐藏的或半透明悬浮样式。

**根因：** 规则缺少滚动条隐藏的明确要求。

### 问题 3：NavBar 背景色与页面背景色联动规则不明确

**现状：** `navbar.md` 的 Background 规则写的是：
- `default`：跟随页面背景色——灰底页面用 `wg.color.surface.toolbar.solid`（#F6F6F6），白底页面用 `wg.color.bg.surface`（#FFFFFF）

**问题：** 规则文字描述了联动逻辑，但 Canonical CSS 中 `.wg-navbar--bg-default` 只有一个值 `var(--wg-color-surface-toolbar-solid)`（#F6F6F6），没有提供白色背景的变体。AI 生成时直接复制 Canonical CSS，导致白底页面的导航栏也是灰色（#F6F6F6），与白色页面背景不协调。

**根因：** `bg-default` 修饰符内部缺少对页面背景色的区分机制。规则文字描述了联动，但 CSS 实现没有对应的结构支撑。

### 问题 4：页面导航缺少转场动画规则

**现状：** `02-ui-generation-rules.md` 和 `SKILL.md` 均未定义页面间的转场动画规则。视图切换只有 `display: none/flex` 的硬切。

**问题：** 原型中页面切换是瞬间出现/消失，不像真实 App 的导航体验。App 中二级页面从右侧滑入，全屏模态从底部滑入，退出反方向执行。

**根因：** 规则完全缺失页面转场动画的定义，包括转场类型、方向、时长和缓动。

### 问题 5：iconfont 本地资源引用路径错误

**现状：** `icon-guidelines.md` 和 `SKILL.md` 规定：
- 将 `resources/fonts/iconfont/iconfont.css` 和字体文件复制到 `assets/fonts/`
- HTML 中引入 `<link rel="stylesheet" href="assets/fonts/iconfont.css">`

**问题：** `iconfont.css` 内部通过 `@font-face` 引用字体文件时使用了相对路径（如 `url('./iconfont.woff2')`）。当 CSS 文件被复制到 `assets/fonts/iconfont/iconfont.css` 时，字体文件也在同目录下，但 `iconfont.css` 中的路径可能指向 `url('iconfont.woff2')` 而非 `url('./iconfont.woff2')`，或者原始 CSS 中嵌入了 base64 编码的 woff2 数据但仍有外部引用的 woff/ttf 路径不匹配。

**根因：** 规则只说了「复制文件」和「引入 CSS」，没有验证 `iconfont.css` 内部的字体文件引用路径在目标目录结构下是否有效。

---

## 修改方案

### 修改 1：`03-components/button.md` — 补充宽度策略决策规则

**文件：** `/Users/dk/.trae-cn/skills/wego-ux-design/03-components/button.md`

**修改位置：** Scope 表格之后，添加「宽度策略」小节

**修改内容：**

在 Scope 表格的「宽度规则」列和「允许组合」章节之间，新增一个「宽度策略」小节：

```markdown
### 宽度策略

`page` 级按钮的宽度需要根据页面类型选择策略：

| 页面类型 | 宽度策略 | 说明 |
|---|---|---|
| 表单型页面（登录、注册、设置、重置等） | 自适应容器宽度 | 按钮宽度跟随 M0–M3 布局的内容区宽度，`inline-size: 100%`，不使用固定宽度 Token |
| 结果型页面（操作成功、操作失败等） | 固定宽度 `wg.component.button.width.page.single` | 居中展示，不需要撑满 |
| 浏览型页面底部的固定操作栏 | 自适应容器宽度 | 跟随操作栏宽度 |

判断流程：

```text
页面是否为表单型？
├─ 是 → 按钮自适应容器宽度
└─ 否 → 页面是否为结果型？
    ├─ 是 → 使用 page.single 固定宽度
    └─ 否 → 使用 page.single 固定宽度
```

`container` 和 `compact` 级按钮始终使用自适应宽度或跟随内容，不受此策略影响。
```

**同时修改 Scope 表格的宽度规则列：**

将 `page` 行的宽度规则从：
```
单个或纵向排列使用 `wg.component.button.width.page.single`；横向成对使用 `wg.component.button.width.page.paired`
```
改为：
```
单个或纵向排列使用 `wg.component.button.width.page.single`；横向成对使用 `wg.component.button.width.page.paired`；表单型页面使用自适应容器宽度（见下方宽度策略）
```

### 修改 2：`04-ai-rules/02-ui-generation-rules.md` — 添加滚动条隐藏规则

**文件：** `/Users/dk/.trae-cn/skills/wego-ux-design/04-ai-rules/02-ui-generation-rules.md`

**修改位置：** 第 5 节「布局选择」的「页面高度」小节

**修改内容：**

在「页面高度」规则之后，新增「滚动条」规则：

```markdown
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
```

### 修改 3：`03-components/navbar.md` — 明确 NavBar 背景色与页面背景色的联动规则

**文件：** `/Users/dk/.trae-cn/skills/wego-ux-design/03-components/navbar.md`

**修改位置：** Background 章节

**修改内容：**

将 Background 表格的 `default` 行从：

```markdown
| `default` | 页面背景为灰色或白色 | 跟随页面背景色：灰底页面用 `wg.color.surface.toolbar.solid`，白底页面用 `wg.color.bg.surface` |
```

改为：

```markdown
| `default` | 页面背景为灰色或白色 | 跟随页面背景色，通过 `wg-navbar--bg-default` 修饰符 + 页面级 CSS 变量覆盖实现（见下方联动规则） |
```

在「背景选择规则」之后，新增「NavBar 背景色与页面背景色联动规则」小节：

```markdown
### NavBar 背景色与页面背景色联动规则

`wg-navbar--bg-default` 的默认背景色为 `wg.color.surface.toolbar.solid`（#F6F6F6，灰色），适用于灰底页面。

当页面背景为白色（`bg-surface`）时，NavBar 背景必须同步使用白色。实现方式：

```css
/* 白底页面中，覆盖 NavBar 背景色 */
.page-surface .wg-navbar--bg-default {
  background-color: var(--wg-color-bg-surface);
}
```

判断流程：

```text
页面背景色是什么？
├─ bg-page（灰色 #EDEDED）→ NavBar 使用 toolbar.solid（#F6F6F6）
├─ bg-surface（白色 #FFFFFF）→ NavBar 使用 bg-surface（#FFFFFF）
└─ 其他 → 使用 transparent 或 custom
```

页面类型与 NavBar 背景对照：

| 页面类型 | 页面背景 | NavBar 背景 |
|---|---|---|
| 多卡片/多模块列表页 | `bg-page`（灰） | `toolbar.solid`（#F6F6F6） |
| 聚焦型单任务页（登录、注册、重置密码、绑定手机号等） | `bg-surface`（白） | `bg-surface`（#FFFFFF） |
| 结果页 | `bg-surface`（白） | `bg-surface`（#FFFFFF） |
| 沉浸式/图片背景页 | 自定义 | `transparent` |
```

**同时修改 Canonical CSS：**

在 `.wg-navbar--bg-default` 规则后添加注释说明：

```css
.wg-navbar--bg-default {
  background-color: var(--wg-color-surface-toolbar-solid);
  /* 白底页面需通过页面级选择器覆盖为 var(--wg-color-bg-surface) */
}
```

### 修改 4：`04-ai-rules/02-ui-generation-rules.md` — 添加页面转场动画规则

**文件：** `/Users/dk/.trae-cn/skills/wego-ux-design/04-ai-rules/02-ui-generation-rules.md`

**修改位置：** 第 9 节「交互实现」之前，新增第 9 节「页面转场」，原第 9–12 节顺延

**修改内容：**

```markdown
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
```

### 修改 5：`02-tokens/icon-guidelines.md` + `SKILL.md` — 修正 iconfont 本地资源引用规则

**文件 1：** `/Users/dk/.trae-cn/skills/wego-ux-design/02-tokens/icon-guidelines.md`

**修改位置：** 第 2 节「使用方式」的「Web 原型」部分

**修改内容：**

将现有的引入方式说明从：

```markdown
## Web 原型

引入 iconfont 样式：

```html
<link rel="stylesheet" href="assets/fonts/iconfont.css">
```
```

改为：

```markdown
## Web 原型

引入 iconfont 样式：

```html
<link rel="stylesheet" href="assets/fonts/iconfont/iconfont.css">
```

注意：iconfont.css 和字体文件必须保持在同一目录下。复制资源时，需将整个 `iconfont/` 目录复制到 `assets/fonts/` 下，保持目录结构完整：

```text
assets/fonts/iconfont/
├── iconfont.css
├── iconfont.woff2
├── iconfont.woff
└── iconfont.ttf
```

不得将 `iconfont.css` 单独复制到 `assets/fonts/` 根目录，否则 CSS 内部的字体文件引用路径将失效。
```

**文件 2：** `/Users/dk/.trae-cn/skills/wego-ux-design/SKILL.md`

**修改位置：** 「Token → CSS 映射」章节中的资源复制说明

**修改内容：**

将现有的：

```markdown
- 将 `resources/fonts/iconfont/iconfont.css` 和对应字体文件（woff2 / woff / ttf）复制到 `assets/fonts/`。
```

改为：

```markdown
- 将 `resources/fonts/iconfont/` 整个目录复制到 `assets/fonts/iconfont/`，保持 `iconfont.css` 与字体文件（woff2 / woff / ttf）在同一目录下。不得将 `iconfont.css` 单独复制到 `assets/fonts/` 根目录。
```

将现有的样式引入顺序说明：

```markdown
- 在 HTML 中按以下顺序引入样式：`tokens.css` → `iconfont.css`（如有）→ `components.css` → `app.css`。
```

改为：

```markdown
- 在 HTML 中按以下顺序引入样式：`tokens.css` → `iconfont/iconfont.css`（如有）→ `components.css` → `app.css`。`iconfont.css` 的引入路径必须与实际目录结构一致。
```

### 修改 6：`04-ai-rules/07-final-checklist.md` — 补充检查项

**文件：** `/Users/dk/.trae-cn/skills/wego-ux-design/04-ai-rules/07-final-checklist.md`

**修改位置：** 在对应检查章节中追加新检查项

**修改内容：**

在「3. 布局检查」中追加：

```text
□ 滚动区域是否隐藏浏览器默认滚动条
□ 页面转场是否使用 Push/Present/Fade 动画而非硬切
```

在「5. 组件检查」中追加：

```text
□ page 级按钮宽度是否符合宽度策略（表单型自适应 / 结果型固定）
□ NavBar 背景色是否与页面背景色联动（白底页面 NavBar 白色）
```

在「9. 最终交付检查」中追加：

```text
□ iconfont 资源目录结构是否完整（iconfont.css 与字体文件在同一目录）
```

---

## 修改文件清单

| 序号 | 文件路径 | 修改类型 | 修改内容摘要 |
|---|---|---|---|
| 1 | `03-components/button.md` | 新增+修改 | Scope 表格宽度规则列补充表单型场景；新增「宽度策略」小节 |
| 2 | `04-ai-rules/02-ui-generation-rules.md` | 新增 | 第 5 节添加「滚动条」规则；新增第 9 节「页面转场」 |
| 3 | `03-components/navbar.md` | 修改+新增 | Background 表格 `default` 行修改；新增「NavBar 背景色与页面背景色联动规则」小节；Canonical CSS 添加注释 |
| 4 | `02-tokens/icon-guidelines.md` | 修改 | 第 2 节「Web 原型」引入路径修正为 `assets/fonts/iconfont/iconfont.css`；补充目录结构说明 |
| 5 | `SKILL.md` | 修改 | 资源复制说明改为整个目录复制；样式引入路径修正 |
| 6 | `04-ai-rules/07-final-checklist.md` | 追加 | 布局检查、组件检查、最终交付检查中追加新检查项 |

---

## 假设与决策

1. **按钮宽度策略**：假设 Figma 中 weigoo-组件应用场景 的按钮宽度规则与上述分析一致——表单型页面按钮自适应，结果型页面按钮固定宽度。如 Figma 中有更细粒度的规则，需进一步对齐。

2. **NavBar 背景色联动**：选择通过页面级 CSS 选择器覆盖（`.page-surface .wg-navbar--bg-default`），而非新增 `wg-navbar--bg-surface` 修饰符。原因是避免为每种背景色都新增修饰符，保持 `bg-default` 的语义——「跟随页面背景」。

3. **页面转场**：选择 CSS `transform` + `transition` 方案而非 JavaScript 动画库，保持原型零依赖。转场参数使用已有 Token，不新增 Token。

4. **iconfont 路径**：选择保持目录结构完整（`assets/fonts/iconfont/`），而非修改 `iconfont.css` 内部路径。原因是修改生成文件的内容容易出错，保持原始目录结构更可靠。

5. **不修改 demo 代码**：按用户要求，只修改 skill 规则文件，不修改已生成的登录注册原型代码。

---

## 验证步骤

1. 修改完成后，运行 `python3 scripts/validate_skill.py` 验证 skill 结构完整性
2. 重新使用 skill 生成一个简单的表单型页面，验证：
   - 按钮宽度是否自适应
   - 滚动条是否隐藏
   - NavBar 背景色是否与页面背景联动
   - 页面切换是否有转场动画
   - iconfont 资源路径是否正确
3. 对照 `07-final-checklist.md` 新增检查项，确认每项都有对应规则支撑
