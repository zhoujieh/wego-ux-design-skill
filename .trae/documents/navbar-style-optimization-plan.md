# NavBar 样式优化计划

## 摘要

针对 ITERATION_PLAN.md 4.1.3 已创建的 `navbar.json`，对其对应的 Canonical CSS（`component-navbar.html`）和 JSON 契约进行 6 项样式优化，使其对齐 kuikly 设计规范。

## 当前状态分析

### 涉及文件

| 文件 | 路径 | 职责 |
|------|------|------|
| 预览页 + Canonical CSS | `wego-ux-design/design-library/preview/component-navbar.html` | 组件预览 HTML，内含 `@component-css-start/end` 标记块包裹的 Canonical CSS |
| 聚合 CSS | `wego-ux-design/design-library/components.css` | 自动生成，运行 `extract_components_css.py` 后更新 |
| JSON 契约 | `wego-ux-design/design-library/components/navbar.json` | 组件的结构化定义（variantDimensions、usageHints、doNotInvent 等） |

### 当前问题诊断

#### 1. 导航内容未上下居中
```css
/* 当前：第 19 行 */
.wg-navbar {
  align-items: flex-end;   /* ❌ 内容靠底部对齐 */
  block-size: var(--wg-touch-default); /* 44px */
  padding-block: var(--wg-spacing-8);   /* 上下各 8px */
}
```
- 使用 `flex-end` 导致子元素（左侧、标题、右侧）贴在底部
- 加上 `padding-block: 8px`，在没有 `box-sizing: border-box` 情况下，总高度 = 44 + 16 = 60px

#### 2. 导航栏高度与 kuikly 规范不符
- kuikly 规范明确：**标准模式高度 44px**
- 当前因缺少 `box-sizing: border-box`，实际渲染高度 = content-box 44px + padding 16px = **60px**（偏差 +16px）

#### 3. 左侧图标热区导致图标视觉位置偏右
- `.wg-navbar` padding-inline: 16px
- `.wg-navbar__left-btn` min-inline-size: 40px（触摸热区），icon font-size: 24px
- 图标居中在 40px 按钮内 → 图标左边缘 = 16 + (40-24)/2 = **24px**，而非规范的 **16px**

#### 4. 关闭按钮使用 `icon-guanbi` 而非 `icon-cha`
- kuikly NavBar 规范中 `CLOSE` 类型对应 `cha` 图标
- 当前预览 HTML 和 usageHints 中写的是 `icon-guanbi`

#### 5. 左侧为「取消」时右侧未强制 button 样式
- kuikly 规范：「左侧文字按钮 + 右侧 Button 样式」是固定搭配
- 当前预览 HTML 中「取消+保存」示例的右侧使用的是 `--text` 样式，应改为 `--button`

#### 6. icon-text 场景间距和最小宽度不达标
- 每个 icon-text item 需要 min-width: 44px（当前无此约束）
- 右侧内容到屏幕边缘的 padding-right 在 icon-text 场景应动态调整为 4px（普通场景保持 16px）

---

## 修改方案

### 修改文件清单

1. **`wego-ux-design/design-library/preview/component-navbar.html`** — 核心修改
   - 修改 Canonical CSS（`@component-css-start/end` 标记块内）
   - 修改预览 HTML 示例
2. **`wego-ux-design/design-library/components/navbar.json`** — 契约同步
   - 更新 `usageHints`、`doNotInvent`、`domAnatomy.modifiers`
3. **`wego-ux-design/design-library/components.css`** — 自动生成
   - 运行 `extract_components_css.py` 重新生成

---

### 修改 1：导航内容上下居中

**文件**: `component-navbar.html` → Canonical CSS 块

**当前代码**（第 14-24 行）：
```css
.wg-navbar {
  position: sticky;
  top: 0;
  z-index: var(--wg-zindex-sticky);
  display: flex;
  align-items: flex-end;                          /* ❌ */
  block-size: var(--wg-touch-default);
  padding-block: var(--wg-spacing-8);             /* ❌ */
  padding-inline: var(--wg-spacing-16);
  background-color: var(--wg-color-bg-page);
}
```

**修改为**：
```css
.wg-navbar {
  position: sticky;
  top: 0;
  z-index: var(--wg-zindex-sticky);
  display: flex;
  align-items: center;                            /* ✅ 上下居中 */
  box-sizing: border-box;                         /* ✅ 确保高度精确 */
  block-size: var(--wg-touch-default);            /* 44px */
  padding-inline: var(--wg-spacing-16);           /* 仅保留水平方向 */
  background-color: var(--wg-color-bg-page);
}
```

**变更点**：
- `align-items: flex-end` → `align-items: center`
- 移除 `padding-block: var(--wg-spacing-8)` — 居中后无需垂直方向 padding
- 新增 `box-sizing: border-box` — 确保 44px = 总高度，不再出现 content-box 偏差

---

### 修改 2：导航栏高度对齐 kuikly 规范（44px）

此项已通过修改 1 解决：
- 移除 `padding-block` 后高度 = block-size 44px
- 新增 `box-sizing: border-box` 防止未来 padding 导致高度膨胀
- 子元素（按钮 min-block-size: 40px、标题 line-height: 26px）在 44px 容器内自然居中，上下各有约 2-9px 空隙

kuikly 规范参考：[NavBar.md](file:///Users/dk/Documents/code/wego-design-system/参考资料/kuikly_doc/basic_components/NavBar.md#L349-L351)：「标准模式默认高度 44px」

---

### 修改 3：左侧图标距离左边缘恰好 16px

**问题**：图标在 40px 宽按钮内居中，导致图标左边缘距屏幕边缘 = 16(padding) + (40-24)/2 = 24px

**解决**：给 `.wg-navbar__left-btn` 添加负 `margin-inline-start` 偏移

**修改**（`.wg-navbar__left-btn` 块，约第 127-141 行）：
```css
.wg-navbar__left-btn {
  appearance: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-block-size: var(--wg-touch-min);
  min-inline-size: var(--wg-touch-min);
  margin-inline-start: calc(-1 * (var(--wg-touch-min) - var(--wg-size-24)) / 2);  /* ✅ 新增 */
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  color: var(--wg-color-text-primary);
  cursor: pointer;
  transition: opacity var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}
```

**计算**：`margin-left = -(40 - 24) / 2 = -8px`，使得图标左边缘回退到 `16 - 8 + (40-24)/2 = 16px`（恰好等于 navbar 的 padding-inline）

---

### 修改 4：关闭按钮 iconfont 改为 `icon-cha`

**文件**: `component-navbar.html` 预览 HTML 部分

**需要修改的位置**：
- 第 446 行：`icon-guanbi` → `icon-cha`（standard + 关闭按钮 + 文字左侧 示例）
- 也可能有其他引用 `icon-guanbi` 的地方

**文件**: `navbar.json`

**修改**：
- 第 78 行 usageHints：「`icon-guanbi 关闭图标`」→「`icon-cha 关闭图标`」

---

### 修改 5：左侧为「取消」时，右侧强制 button 样式

**文件**: `navbar.json`

在 `usageHints` 中新增规则，在 `doNotInvent` 中新增禁止项：

```json
"usageHints": [
  // ... 现有项 ...
  "左侧按钮 text（取消）时，必须搭配右侧 button action，形成'取消+按钮'固定搭配"
]

"doNotInvent": [
  // ... 现有项 ...
  "左侧为取消文字按钮时，右侧不得使用 text 或 icon-text 样式"
]
```

**文件**: `component-navbar.html` 预览 HTML 示例

修改第 461-477 行的示例（standard + 文字左侧按钮 + 文字右侧）：
- 标题从「编辑资料」改为更贴合场景的名称
- 右侧从 `--text`（保存）改为 `--button`（保存）

```html
<h3>standard + 取消文字 + button 右侧</h3>
<div class="wg-navbar wg-navbar--standard wg-navbar--bg-default wg-navbar--divider">
  <div class="wg-navbar__left">
    <button class="wg-navbar__left-btn wg-navbar__left-btn--text" type="button">
      <span class="wg-navbar__left-text">取消</span>
    </button>
  </div>
  <div class="wg-navbar__center">
    <span class="wg-navbar__title">编辑资料</span>
  </div>
  <div class="wg-navbar__actions">
    <button class="wg-navbar__action wg-navbar__action--button" type="button">
      <span class="wg-navbar__action-label">保存</span>
    </button>
  </div>
</div>
```

---

### 修改 6：icon-text 场景间距优化

此修改涉及两个子项：

#### 6a. icon-text item 最小宽度 44px

**修改**（`.wg-navbar__action--icon-text` 块，约第 226-228 行）：
```css
.wg-navbar__action--icon-text {
  flex-direction: column;
  padding-inline: var(--wg-spacing-4);
  min-inline-size: var(--wg-touch-default);   /* ✅ 新增：44px */
}
```

#### 6b. icon-text 场景右侧 edge 间距动态调整为 4px

**策略**：新增导航栏修饰符 `.wg-navbar--actions-icon-text`，当右侧全部使用 icon-text 时应用。

**新增 CSS**：
```css
.wg-navbar--actions-icon-text {
  padding-inline-end: var(--wg-spacing-4);     /* 覆盖默认 16px → 4px */
}
```

**原因**：icon-text item 每个 44px 宽，3 个占 132px + gap 4px×2 = 140px。375px 屏幕中，左侧 padding 16px + 中间标题 + 右侧 140px + padding 4px 刚好能容纳。

#### 6c. 同步 contract

**navbar.json** 中：
- `domAnatomy.modifiers` 新增 `".wg-navbar--actions-icon-text"`
- `usageHints` 新增：「右侧全部为 icon-text action 时，给 `.wg-navbar` 添加 `--actions-icon-text` 修饰符」
- `tokensConsumed` 确认 `wg-touch-default`（44px）已在列表中

#### 6d. 预览示例

在 preview HTML 中添加一个使用 `--actions-icon-text` 修饰符的示例。

---

## 验证步骤

1. **浏览器验证**：在浏览器中打开 `component-navbar.html`，逐项检查：
   - 所有导航变体中，内容（标题、按钮）在导航栏中垂直居中
   - 导航栏总高度为 44px（开发者工具测量）
   - 左侧图标的左边缘距屏幕边缘为 16px
   - 关闭按钮使用 `icon-cha`
   - 「取消+保存」示例中保存按钮为绿色 button 样式
   - icon-text 场景中每个 item 宽度 ≥ 44px，右侧 padding 为 4px

2. **CSS 提取验证**：运行 `python scripts/extract_components_css.py`，确认 `components.css` 更新且 NavBar 部分与 preview HTML 一致

3. **零硬编码检查**：grep 检查 CSS 块中无裸 `#xxx`/`rgb()`/`px`（`var(--wg-*)` 之外的值）

4. **Token 自检**：确认新增 CSS 属性中非零值均通过 `var(--wg-*)` 引用

---

## 假设与决策

| 决策 | 说明 |
|------|------|
| `box-sizing: border-box` | 仅在 `.wg-navbar` 层添加，不修改全局 scaffold.css，避免影响其他组件 |
| margin-inline-start 负值 | 使用 `calc()` 动态计算，自动适配 Token 变化 |
| `--actions-icon-text` 修饰符 | 放在 `.wg-navbar` 根节点，用 padding-inline-end 覆盖右间距（仅覆盖 end，不影响左侧） |
| `icon-cha` vs `icon-cha16` | kuikly 规范中 `CLOSE` 类型使用 `cha` 图标（24px 尺寸），选用 `icon-cha` 而非 `icon-cha16` |
| 左侧按钮 margin-inline-start | 只对 `.wg-navbar__left-btn` 添加，不影响 `.wg-navbar__left-btn--text`（文字按钮不需要触控热区扩展） |

---

## 不修改的内容

- `scaffold.css` — 不添加全局 `box-sizing`，只影响 navbar 组件
- `tokens.css` — 现有 Token 已满足需求（`wg-touch-default: 44px`、`wg-touch-min: 40px`、`wg-size-24: 24px`）
- 其他组件预览页 — 本次修改仅限 navbar
