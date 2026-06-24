# 计划：输出 Tabs 组件规范

## 摘要

为 wego-ux-design 组件库新增 Tabs（标签栏）组件规范文档，遵循已有的 button.md / navbar.md 格式，基于 Figma 设计稿和 Kuikly TabBar.md 参考文档提取设计规则。

## 当前状态分析

### 已有资源
- **Figma 设计稿**：`📙 wegoo 组件应用场景`，节点 `559:42238`，包含 TabBar（标准/全局）和 TabBar_mini（迷你/局部）两种样式及使用场景
- **Kuikly TabBar.md**：`参考资料/kuikly_doc/basic_components/TabBar.md`，完整的 Kotlin DSL API 文档
- **Kuikly tabs.md**：`参考资料/kuikly_doc/API/components/tabs.md`，底层 Tabs API
- **已有组件规范**：button.md、navbar.md、link.md，格式统一（使用决策→语义模型→允许组合→Anatomy→文案规则→Canonical HTML→Canonical CSS→状态→可访问性→生成约束→自检→规范来源）

### Figma 提取的关键设计数据

| 属性 | TabBar（标准/全局） | TabBar_mini（迷你/局部） |
|---|---|---|
| 高度 | 56px | 48px |
| 字号 | 16px Medium | 14px Medium |
| 选中文字色 | text_100 (#1e2028) | text_100 (#1e2028) |
| 未选中文字色 | text_80 (#6e7382) | text_80 (#6e7382) |
| 指示器高度 | 3px | 2px |
| 指示器颜色 | green_1_100 (#03c160) | green_1_100 (#03c160) |
| 布局模式 | 等分型（≤5 个） | 始终滑动型 |
| Tab 内边距 | px 15px | 首 tab pl 16px pr 8px，其余 pl 8px pr 8px |
| 最大等分数量 | 5 | N/A（始终滚动） |

Kuikly 规定 maxSize 默认 5，Tab 数量 ≤5 时等分，>5 时滚动。Figma 组件描述"最多4个选项"仅为 Figma 组件实例的展示限制，规范以 Kuikly 的 5 为准。

### Token 映射

| Figma 变量 | Token |
|---|---|
| text_100（一级） | `--wg-color-text-primary` |
| text_80（二级） | `--wg-color-text-secondary` |
| green_1_100（品牌） | `--wg-color-action-primary-default` |
| 16/中文 加粗 | `--wg-font-size-16` / `--wg-font-weight-medium` |
| 14/中文 加粗 | `--wg-font-size-14` / `--wg-font-weight-medium` |
| 表单高度/间隙_3 (16px) | `--wg-spacing-16` |
| 表单高度/间隙_1 (8px) | `--wg-spacing-8` |

## 实施步骤

### 步骤 1：创建 `wego-ux-design/03-components/tabs.md`

按照已有组件规范格式，编写 Tabs 组件规范文档，包含以下章节：

1. **使用决策**：何时使用/不使用 Tabs
2. **语义模型**：两个决策维度 — `size`（standard / mini）和 `layout`（divide / scroll）+ `state`
3. **允许组合**：standard+divide、standard+scroll、mini+scroll
4. **Anatomy**：HTML 结构树
5. **文案规则**：Tab 文字长度、截断规则
6. **Canonical HTML**：各组合的 HTML 示例
7. **Canonical CSS**：使用 Token 的完整 CSS
8. **状态**：default / pressed / focus-visible
9. **可访问性**：role="tablist"、aria-selected 等
10. **生成约束**：禁止事项
11. **自检**：检查清单
12. **规范来源**：Figma 节点 + Kuikly 参考

### 步骤 2：更新 `wego-ux-design/03-components/registry.json`

在 registry.json 的 components 数组中新增 tabs 组件条目：

```json
{
  "id": "tabs",
  "name": "Tabs",
  "category": "navigation",
  "status": "stable",
  "file": "tabs.md",
  "keywords": ["标签栏", "tabs", "tabbar", "页签", "切换", "选项卡"],
  "decisionAxes": {
    "size": ["standard", "mini"],
    "layout": ["divide", "scroll"],
    "state": ["default", "pressed", "focus-visible"]
  },
  "interactionMode": "css"
}
```

## 关键设计决策

1. **组件命名**：使用 `Tabs` 而非 `TabBar`，与 HTML 语义（tablist/tab/tabpanel）一致，且与 Kuikly API `tabs.md` 呼应
2. **CSS 命名**：`wg-tabs`（而非 wg-tabbar），与组件名一致
3. **standard 最多 5 个等分**：以 Kuikly TabBar.md 的 maxSize=5 为准，Figma 组件描述"最多4个"仅为展示限制
4. **V1 不含图标 Tab**：与 Button V1 不含图标一致，简化首版规范
5. **V1 不含 PageList 联动**：联动逻辑需要 JS，HTML 原型仅定义视觉和结构
6. **指示器宽度**：等分型下指示器跟随文字宽度居中（与 Kuikly 一致）；滑动型下指示器贴合 Tab 项两侧内边距
7. **mini 指示器高度 2px**：来自 Figma 实际测量，与 Kuikly 一致

## 验证步骤

1. 确认 tabs.md 格式与 button.md / navbar.md 一致
2. 确认所有 CSS Token 引用均存在于 tokens.css 中
3. 确认 registry.json 格式正确且 tabs 条目可被解析
4. 确认 Figma 设计数据与规范一致（高度、字号、颜色、间距）
5. 确认 Kuikly TabBar 关键规则已被纳入（布局模式、指示器、事件语义）
