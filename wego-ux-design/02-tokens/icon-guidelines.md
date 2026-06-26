# 图标使用规范

> 微购 Design System Skill / 02-tokens
> 本文档定义微购设计系统中图标的使用方式、尺寸规范、颜色规则、绘制规则和 SVG 兜底方案。

---

# 1. 图标资源

微购图标统一使用 iconfont 字体库：

- **项目名称**：微购单色图标库
- **font-family**：`wego-iconfont-s`
- **CSS 前缀**：`icon-`
- **权威来源**：`resources/fonts/iconfont/iconfont.json`
- **字体文件**：`resources/fonts/iconfont/iconfont.css` + 对应字体文件（woff2 / woff / ttf）

当 iconfont 中不存在所需图标时，按第 7 节绘制规则输出 SVG 内联图标作为兜底。

---

# 2. 使用方式

## Web 原型

引入 iconfont 样式：

```html
<link rel="stylesheet" href="assets/fonts/iconfont/iconfont.css">
```

使用图标：

```html
<i class="wego-iconfont-s icon-{font_class}"></i>
```

其中 `{font_class}` 来自 `iconfont.json` 中 `glyphs` 数组的 `font_class` 字段。

示例：

```html
<i class="wego-iconfont-s icon-sousuo"></i>
<i class="wego-iconfont-s icon-fanhui"></i>
<i class="wego-iconfont-s icon-gou"></i>
```

不得使用 `<span>` 或 `<div>` 替代 `<i>` 标签渲染 iconfont 图标。

注意：iconfont.css 和字体文件必须保持在同一目录下。复制资源时，需将整个 `iconfont/` 目录复制到 `assets/fonts/` 下，保持目录结构完整：

```text
assets/fonts/iconfont/
├── iconfont.css
├── iconfont.woff2
├── iconfont.woff
└── iconfont.ttf
```

不得将 `iconfont.css` 单独复制到 `assets/fonts/` 根目录，否则 CSS 内部的字体文件引用路径将失效。

## 图标查询

生成界面时，必须先读取 `resources/fonts/iconfont/iconfont.json`，在 `glyphs` 数组中查找所需图标的 `font_class`。只有确认 iconfont 中不存在所需图标时，才使用 SVG 兜底方案。

---

# 3. 尺寸规范

## 支持尺寸

图标以 24px 为基准绘制，以 4px 为梯度缩放。

| 尺寸 | Token | 推荐程度 | 典型场景 |
|---|---|---|---|
| 16px | `wg.size.16` | 推荐 | 紧凑行内图标、列表前缀图标、12pt 字体搭配 |
| 20px | `wg.size.20` | 可用 | 14pt 字体搭配 |
| 24px | `wg.size.24` | 推荐 | 标准图标、16pt 字体搭配 |
| 28px | `wg.size.28` | 可用 | 较大图标 |
| 32px | `wg.size.32` | 推荐 | 大图标、空状态图标 |
| 48px | `wg.size.48` | 可用 | 超大状态图标 |

## 图标-字号搭配

| 字号 | 图标尺寸 | 说明 |
|---|---|---|
| 12pt（`wg.font.size.f12`） | 16px（`wg.size.16`） | 辅助说明旁图标 |
| 14pt（`wg.font.size.f14`） | 20px（`wg.size.20`） | 正文旁图标 |
| 16pt（`wg.font.size.f16`） | 24px（`wg.size.24`） | 标题旁图标 |

## 尺寸设置

通过 `font-size` 控制图标尺寸，iconfont 默认 `font-size: 16px`。修改尺寸时使用 Token：

```css
.wg-icon--16 { font-size: var(--wg-size-16); line-height: 1; }
.wg-icon--20 { font-size: var(--wg-size-20); line-height: 1; }
.wg-icon--24 { font-size: var(--wg-size-24); line-height: 1; }
.wg-icon--28 { font-size: var(--wg-size-28); line-height: 1; }
.wg-icon--32 { font-size: var(--wg-size-32); line-height: 1; }
.wg-icon--48 { font-size: var(--wg-size-48); line-height: 1; }
```

不得硬编码 `font-size` 像素值。

## 行高设置

iconfont 图标元素必须设置 `line-height: 1`，确保行高等于字号，防止继承父元素行高导致图标垂直偏移或出现额外上下间距。

`.wego-iconfont-s` 基类中应包含：

```css
.wego-iconfont-s {
  line-height: 1;
}
```

所有以 `font-size` 控制图标尺寸的 CSS 类，必须同步设置 `line-height: 1`。不得通过 `line-height` 硬编码像素值。

---

# 4. 颜色规则

图标颜色通过 `color` 属性控制，继承父元素或使用 Token：

| 场景 | Token | 说明 |
|---|---|---|
| 一级图标 | `wg.color.text.primary` | 主要操作图标、导航图标 |
| 二级图标 | `wg.color.text.secondary` | 辅助功能图标 |
| 三级图标 | `wg.color.text.tertiary` | 弱化图标、占位图标 |
| 禁用图标 | `wg.color.text.disabled` | 不可操作图标 |
| 品牌图标 | `wg.color.action.primary.default` | 品牌色图标 |
| 危险图标 | `wg.color.status.danger.default` | 错误/删除图标 |
| 成功图标 | `wg.color.status.success.default` | 完成图标 |
| 反白图标 | `wg.color.text.inverse` | 深色背景上的图标 |

示例：

```html
<i class="wego-iconfont-s icon-sousuo" style="color: var(--wg-color-text-tertiary)"></i>
```

不得硬编码图标颜色值。

---

# 5. 边距规则

图标以 24px 为基准绘制时的边距建议：

- **方形图标**：内容区 24 - 3 = 21px（边距指不含线条的留白格子数）
- **最大圆图标**：内容区 24 - 2 = 22px

特殊情况下为保证图标识别度和视觉空间，图标左右留白可以不一致，但差值不超过 1。

---

# 6. 命名规则

Figma 中图标命名格式：`icon/名称_分类识别符`

分类识别符由两位组成：

**第一位 — 颜色**：

| 标识 | 颜色 |
|---|---|
| b | 黑色 |
| w | 白色 |
| h | 灰色 |
| g | 绿色 |
| s | 蓝色 |
| r | 红色 |
| o | 橙色 |
| c | 彩色 |

**第二位 — 属性**：

| 标识 | 属性 |
|---|---|
| 不追加 | 线性 |
| cell | 面性 |
| c | 线面结合 |

示例：

- 白色线性图标：`icon/star_w`
- 黑色面性图标：`icon/star_bcell`
- 黑色线面结合：`icon/star_bc`

iconfont 中的 `font_class` 采用中文拼音命名，与 Figma 命名不同。使用时以 `iconfont.json` 中的 `font_class` 为准。

---

# 7. 绘制规则

当 iconfont 中不存在所需图标时，按以下规则绘制 SVG 内联图标。

## 基础参数

| 参数 | 值 | 说明 |
|---|---|---|
| 线粗 | 1.5px | 对应 Token `wg.stroke.width.icon` |
| 线对齐 | 居中（center） | stroke-align: center |
| 端点 | 方（butt） | stroke-linecap: butt |
| 角点 | 圆（round） | stroke-linejoin: round |
| 圆角大小 | 0 | 图标路径自身不添加圆角 |

## 加粗版图标

部分场景 1.5px 线粗过细，使用加粗版：

| 场景 | 线粗 | Token |
|---|---|---|
| 列表前的勾 | 2px | — |
| 需要强调整体识别度的图标 | 2.25px | `wg.stroke.width.icon.strong` |

## 填充图标

面性图标添加 1.5px 描边，目的是让图标转角圆润。

## SVG 输出模板

```html
<svg class="wg-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="..." stroke="currentColor" stroke-width="1.5" stroke-linecap="butt" stroke-linejoin="round"/>
</svg>
```

关键属性：

- `fill="none"`：线性图标不填充
- `stroke="currentColor"`：颜色继承父元素
- `stroke-width="1.5"`：默认线粗
- `stroke-linecap="butt"`：方端点
- `stroke-linejoin="round"`：圆角点

面性图标：

```html
<svg class="wg-icon" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
  <path d="..." stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
</svg>
```

## 缺失标注

使用 SVG 兜底时，必须在交付说明中标注：

```text
当前使用：SVG 内联图标（{图标名称}）
原因：iconfont 字体库中不存在该图标
建议补充：将 {图标名称} 添加至 iconfont 项目
归属位置：resources/fonts/iconfont/
```

---

# 8. 特殊图标

## 16×16 独立尺寸图标

右箭头和小型加减号等图标缩小使用会极细，此时选用 16×16 的独立尺寸图标。16×16 的特殊图标绘制时使用 1.5px 线粗。

iconfont 中已有部分 16px 图标，`font_class` 以 `16` 结尾，如 `icon-youjiantou16`、`icon-zuojiantou16`、`icon-gou16`、`icon-cha16`、`icon-jia16`、`icon-jian16` 等。

## 大状态图标

用于结果页、空状态等场景的大尺寸图标（48px+），使用面性图标：

| 图标 | font_class | 语义 |
|---|---|---|
| 圆勾-面 | `yuangou-mian` | 操作成功 |
| 叹号-面 | `tanhao-mian` | 操作将引起后果 |
| 圆叉-面 | `yuancha-mian` | 不可挽回的严重后果 |
| 时间-面 | `shijian-mian` | 等待中 |

---

# 9. 禁止事项

- 禁止在 iconfont 中存在所需图标时使用 SVG 内联或图片替代
- 禁止硬编码图标尺寸（必须使用 `wg.size.*` Token）
- 禁止硬编码图标颜色（必须使用 `wg.color.*` Token 或继承父元素）
- 禁止自行创造 iconfont 中不存在的图标样式
- 禁止使用 emoji 或图片替代功能图标
- 禁止滥用图标（参见 `04-ai-rules/05-forbidden-rules.md`）
