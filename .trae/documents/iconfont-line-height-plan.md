# iconfont 行高规范化计划

## 摘要

所有 iconfont 图标元素需要设置 `line-height: 1`（使其等于 `font-size`），防止从父元素继承 `line-height` 导致图标垂直偏移或多余上下间距。

修改分为三层：
1. **规范层** — 将规则写入 AI 运行时必读文档
2. **基类层** — 修复 `iconfont.css` 中 `.wego-iconfont-s` 基类
3. **组件层** — 修复所有组件预览页和 scaffold 中的 icon 类

---

## 当前状态分析

### 缺失 line-height 的位置

| 文件 | CSS 选择器 | 当前 line-height | 问题 |
|------|-----------|-----------------|------|
| `resources/fonts/iconfont/iconfont.css` | `.wego-iconfont-s` | **无** | 基类缺失，所有图标继承父元素行高 |
| `design-library/assets/fonts/iconfont/iconfont.css` | `.wego-iconfont-s` | **无** | 同上（交付副本） |
| `design-library/scaffold.css` | `.wg-icon--16` ~ `.wg-icon--48` | **无** | 6 个图标尺寸工具类缺失 |
| `preview/component-navbar.html` | `.wg-navbar__left-icon` | **无** | font-size: 24px, 无 line-height |
| `preview/component-navbar.html` | `.wg-navbar__action-icon` | **无** | font-size: 20px, 无 line-height |
| `preview/component-navbar.html` | `.wg-navbar__search-icon` | **无** | font-size: 20px, 无 line-height |
| `preview/component-tag.html` | `.wg-tag__icon` | **无** | font-size: 16px, 无 line-height |
| `preview/component-cell.html` | `.wg-cell__arrow` | **无** | font-size: 16px, 无 line-height |
| `preview/component-dialog.html` | `.wg-dialog__icon` | **无** | font-size: 24px, 无 line-height |
| `preview/component-toast.html` | `.wg-toast__icon` | **无** | font-size: 20px, 无 line-height |
| `preview/component-result.html` | `.wg-result__icon` | **无** | font-size: 72px/120px, 无 line-height |

### 已有但需修正的位置

| 文件 | CSS 选择器 | 当前 line-height | 问题 |
|------|-----------|-----------------|------|
| `preview/component-actionsheet.html` | `.wg-actionsheet__item-icon` | `line-height: 24px` | 应改为 `line-height: 1`（硬编码 24px） |
| `preview/component-button.html` | `.wg-button__icon` | `line-height: 1` ✅ | 但**位于 `@component-css-end` 标记之外**，需移入标记块 |

### 规范文档现状

| 文件 | 状态 |
|------|------|
| `02-tokens/icon-guidelines.md` 第 3 节 | 仅含尺寸设置规则（`font-size`），**缺少行高规则** |
| `04-ai-rules/05-forbidden-rules.md` 第 3 节 | 有颜色/尺寸禁止项，**缺少行高禁止项** |

---

## 修改方案

### 修改文件清单

共涉及 **3 类 12 个文件**，按类型分组：

**类型 A — 规范文档（2 个文件）：**
1. `02-tokens/icon-guidelines.md`
2. `04-ai-rules/05-forbidden-rules.md`

**类型 B — iconfont 字体 CSS（2 个文件）：**
3. `resources/fonts/iconfont/iconfont.css`
4. `design-library/assets/fonts/iconfont/iconfont.css`

**类型 C — 组件 CSS（8 个文件）：**
5. `design-library/scaffold.css`
6. `design-library/preview/component-navbar.html`
7. `design-library/preview/component-tag.html`
8. `design-library/preview/component-cell.html`
9. `design-library/preview/component-dialog.html`
10. `design-library/preview/component-toast.html`
11. `design-library/preview/component-result.html`
12. `design-library/preview/component-actionsheet.html`

**类型 D — 自动生成：**
13. `design-library/components.css` — 运行 extract 脚本重新生成

---

### 修改 A1：`02-tokens/icon-guidelines.md` — 新增行高规则

**位置**：第 3 节「尺寸规范」末尾，第 104 行（「不得硬编码…」之后）

**新增内容**：

```markdown
## 行高设置

iconfont 图标元素必须设置 `line-height: 1`，确保行高等于字号，防止继承父元素行高导致图标垂直偏移或出现额外上下间距。

```css
.wego-iconfont-s {
  line-height: 1;
}
```

所有以 `font-size` 控制图标尺寸的 CSS 类，必须同步设置 `line-height: 1`：

```css
.wg-icon--16 { font-size: var(--wg-size-16); line-height: 1; }
.wg-icon--20 { font-size: var(--wg-size-20); line-height: 1; }
.wg-icon--24 { font-size: var(--wg-size-24); line-height: 1; }
/* ... 以此类推 */
```
```

**同时，修改第 3 节现有的尺寸设置示例**（第 93-102 行），给每个 `.wg-icon--*` 添加 `line-height: 1`：

```css
.wg-icon--16 { font-size: var(--wg-size-16); line-height: 1; }
.wg-icon--20 { font-size: var(--wg-size-20); line-height: 1; }
.wg-icon--24 { font-size: var(--wg-size-24); line-height: 1; }
.wg-icon--28 { font-size: var(--wg-size-28); line-height: 1; }
.wg-icon--32 { font-size: var(--wg-size-32); line-height: 1; }
.wg-icon--48 { font-size: var(--wg-size-48); line-height: 1; }
```

---

### 修改 A2：`04-ai-rules/05-forbidden-rules.md` — 新增禁止项

**位置**：第 3 节「图标禁止事项」第 49 行之后

**新增内容**：

```markdown
- iconfont 图标元素未设置 `line-height: 1` 导致垂直偏移
```

---

### 修改 B1 & B2：`iconfont.css`（两个副本）

**修改内容**：在 `.wego-iconfont-s` 基类中添加 `line-height: 1`

**修改前**：
```css
.wego-iconfont-s {
  font-family: "wego-iconfont-s" !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

**修改后**：
```css
.wego-iconfont-s {
  font-family: "wego-iconfont-s" !important;
  font-size: 16px;
  font-style: normal;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

**涉及文件**：
- `wego-ux-design/resources/fonts/iconfont/iconfont.css` — 源副本
- `wego-ux-design/design-library/assets/fonts/iconfont/iconfont.css` — 交付副本

---

### 修改 C1：`design-library/scaffold.css` — 图标尺寸工具类

**修改前**（第 215-220 行）：
```css
.wg-icon--16 { font-size: var(--wg-size-16); }
.wg-icon--20 { font-size: var(--wg-size-20); }
.wg-icon--24 { font-size: var(--wg-size-24); }
.wg-icon--28 { font-size: var(--wg-size-28); }
.wg-icon--32 { font-size: var(--wg-size-32); }
.wg-icon--48 { font-size: var(--wg-size-48); }
```

**修改后**：
```css
.wg-icon--16 { font-size: var(--wg-size-16); line-height: 1; }
.wg-icon--20 { font-size: var(--wg-size-20); line-height: 1; }
.wg-icon--24 { font-size: var(--wg-size-24); line-height: 1; }
.wg-icon--28 { font-size: var(--wg-size-28); line-height: 1; }
.wg-icon--32 { font-size: var(--wg-size-32); line-height: 1; }
.wg-icon--48 { font-size: var(--wg-size-48); line-height: 1; }
```

---

### 修改 C2：`component-navbar.html` — 3 个 icon 类

**`.wg-navbar__left-icon`**（第 144-149 行）添加 `line-height: 1`：
```css
.wg-navbar__left-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: var(--wg-size-24);
  line-height: 1;
}
```

**`.wg-navbar__action-icon`**（第 233-238 行）添加 `line-height: 1`：
```css
.wg-navbar__action-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: var(--wg-size-20);
  line-height: 1;
}
```

**`.wg-navbar__search-icon`**（第 299-304 行）添加 `line-height: 1`：
```css
.wg-navbar__search-icon {
  flex-shrink: 0;
  margin-inline-end: var(--wg-spacing-4);
  color: var(--wg-color-text-placeholder);
  font-size: var(--wg-size-20);
  line-height: 1;
}
```

---

### 修改 C3：`component-tag.html` — `.wg-tag__icon`

**当前**（第 74-77 行）：
```css
.wg-tag__icon {
  font-size: var(--wg-size-16);
  flex-shrink: 0;
}
```

**修改后**：
```css
.wg-tag__icon {
  font-size: var(--wg-size-16);
  flex-shrink: 0;
  line-height: 1;
}
```

---

### 修改 C4：`component-cell.html` — `.wg-cell__arrow`

**当前**（第 152-159 行）：
```css
.wg-cell__arrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: var(--wg-size-16);
  flex-shrink: 0;
  color: var(--wg-color-text-tertiary);
}
```

**修改后**：添加 `line-height: 1`

---

### 修改 C5：`component-dialog.html` — `.wg-dialog__icon`

**当前**（第 77-83 行）：
```css
.wg-dialog__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: var(--wg-size-24);
  flex-shrink: 0;
}
```

**修改后**：添加 `line-height: 1`

---

### 修改 C6：`component-toast.html` — `.wg-toast__icon`

**当前**（第 50-57 行）：
```css
.wg-toast__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: var(--wg-size-20);
  flex-shrink: 0;
  color: var(--wg-color-text-inverse);
}
```

**修改后**：添加 `line-height: 1`

---

### 修改 C7：`component-result.html` — `.wg-result__icon` 及变体

**`.wg-result__icon` 基础**（第 60-65 行）：添加 `line-height: 1`

```css
.wg-result__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 1;
}
```

**状态图标变体**（第 67-73 行）`font-size: var(--wg-size-72)` — 继承基础 `line-height: 1`，无需额外修改。

**场景图标变体**（第 95-102 行）`font-size: 120px` — 继承基础 `line-height: 1`，无需额外修改。

---

### 修改 C8：`component-actionsheet.html` — 修正硬编码 line-height

**`.wg-actionsheet__item-icon`**（第 113-118 行）：

**修改前**：
```css
.wg-actionsheet__item-icon {
  font-size: var(--wg-size-20);
  line-height: 24px;
  color: var(--wg-color-text-primary);
  flex-shrink: 0;
}
```

**修改后**：
```css
.wg-actionsheet__item-icon {
  font-size: var(--wg-size-20);
  line-height: 1;
  color: var(--wg-color-text-primary);
  flex-shrink: 0;
}
```

---

### 修改 D：重新生成 `components.css`

运行 `python3 scripts/extract_components_css.py` 将修改同步到聚合 CSS。

---

## 不修改的内容

- `component-button.html` 中 `.wg-button__icon` 已有 `line-height: 1`，但位于 `@component-css-end` 之外（属于布局 bug），**本次不处理**（超出 scope）
- `component-actionsheet.html` 中 `.wg-actionsheet__item-check` 已有 `line-height: 1`，无需修改
- `component-form.html`、`component-input.html`、`component-loading.html`、`component-link.html`、`component-tabs.html` — 不使用 iconfont，无需修改

---

## 验证步骤

1. **规范文档验证**：确认 `02-tokens/icon-guidelines.md` 和 `04-ai-rules/05-forbidden-rules.md` 中包含行高规则
2. **CSS 提取验证**：运行 `python3 scripts/extract_components_css.py`，确认无报错
3. **零硬编码检查**：grep 检查 iconfont 相关 CSS 中无裸 `px`/`rem`/`#xxx`/`rgb()`
4. **规则一致性**：确认所有 icon 类的 `line-height: 1` 风格统一（无 `line-height: 24px` 等硬编码）
5. **浏览器验证**：打开各组件预览页，检查图标垂直对齐无异常
