# ActionSheet 组件规范输出计划

## 摘要

根据 Figma 设计稿和 Kuikly 组件文档，输出 ActionSheet 组件的 HTML 原型规范文件，遵循项目已有的组件规范格式（如 button.md、tabs.md）。

## 当前状态分析

### 已有资料
1. **Figma 设计稿**（节点 `522:51546`，"Actionsheet _ 选择面板"）：
   - 普通_单行_无标题（582:23730）：纯文本选项列表，居中对齐，56px 行高，16px 字号
   - 普通_单行有icon_无标题（582:23990）：带左侧图标的选项列表，图标 24px，图标与文字间距 8px
   - 普通_多行_有主副标题（582:27986）：slot 型多行选项，72px 行高
   - 取消按钮区：8px 灰色分割线 + 取消文字（居中，16px）
   - 安全区：34px 高度，含 5px Home Indicator
   - 顶部圆角 16px，选项圆角 8px
   - 选项内边距 12px 水平 / 16px 垂直
   - 分割线颜色 rgba(32,47,100,0.08)
   - 头部描述区：支持图标 + 描述文本 + 右侧链接

2. **Kuikly 文档**（`参考资料/kuikly_doc/basic_components/ActionSheet.md` + `API/components/action-sheet.md`）：
   - 两种模式：操作模式（showActionSheet）和选择模式（showActionSheetSelect）
   - 操作模式：文本居中，无选中状态
   - 选择模式：文本左对齐，选中项右侧绿色对勾，文字加粗
   - 头部描述区三种布局：无图标无链接→居中；有图标无链接→图标+文本居中；有链接→两端对齐
   - 选项支持：图标、标题、副标题、徽章（红点/数字）、推荐标签、禁用态
   - 点击选项后默认关闭（closeAfterClick），可手动关闭
   - 底部安全区自适应

3. **已有组件规范**（`wego-ux-design/03-components/`）：
   - button.md、tabs.md、link.md、navbar.md 提供格式参考
   - registry.json 提供注册格式
   - shared-rules.md 提供公共规则
   - token-css-map.md 提供可用 Token

### 设计 Token 映射（Figma → CSS 变量）
| Figma 值 | Token |
|---|---|
| #1E2028 (text_100) | `--wg-color-text-primary` |
| rgba(32,47,100,0.08) (bg_line_08) | `--wg-color-divider-default` |
| rgba(32,47,100,0.03) (bg_gray_03) | `--wg-color-state-hover` |
| rgba(32,47,100,0.06) | `--wg-color-state-pressed` |
| #FFFFFF (bg_white_100) | `--wg-color-bg-surface` |
| #00C777 (绿色对勾) | `--wg-color-base-accent-green-500` |
| PingFang SC 16px Regular | `--wg-font-size-16` / `--wg-font-weight-regular` |
| 56px 行高 | `--wg-size-56` |
| 72px 行高 | `--wg-size-72` |
| 24px 图标 | `--wg-size-24` |
| 8px 分割 | `--wg-spacing-8` |
| 12px 内边距 | `--wg-spacing-12` |
| 16px 圆角 | `--wg-radius-xl` |
| 8px 圆角 | `--wg-radius-md` |
| 0.5px 分割线 | `--wg-stroke-width-hairline` |
| 遮罩 rgba(30,32,40,0.60) | `--wg-color-overlay-modal` |

## 实施步骤

### 步骤 1：创建 `actionsheet.md` 规范文件

**文件路径**：`/Users/dk/Documents/code/wego-design-system/wego-ux-design/03-components/actionsheet.md`

**内容结构**（对齐已有规范格式）：

1. **使用决策**
   - 使用 ActionSheet：底部弹出一组操作或选项，底部带固定"取消"按钮
   - 不使用 ActionSheet：相对目标视图弹出的下拉菜单→用 PopOver/PopViewSelect；确认/警告弹窗→用 Dialog

2. **语义模型**
   - `mode`：`action`（操作模式）| `select`（选择模式）
   - `header`：`none`（无头部）| `simple`（纯描述）| `with-icon`（图标+描述）| `with-link`（带链接）
   - `itemType`：`single`（单行）| `multi`（多行主副标题）
   - `state`：`default` | `pressed` | `disabled` | `selected`

3. **允许组合**
   - action + 单行 + 无头部 / 简单头部 / 带图标头部 / 带链接头部
   - select + 单行 + 无头部 / 简单头部
   - action + 多行（slot 型）

4. **Anatomy**
   ```
   div.wg-actionsheet
   ├── div.wg-actionsheet__overlay
   ├── div.wg-actionsheet__panel
   │   ├── div.wg-actionsheet__header (可选)
   │   │   ├── i.wg-actionsheet__header-icon (可选)
   │   │   ├── span.wg-actionsheet__header-text
   │   │   └── button.wg-actionsheet__header-link (可选)
   │   ├── div.wg-actionsheet__list
   │   │   └── button.wg-actionsheet__item
   │   │       ├── i.wg-actionsheet__item-icon (可选)
   │   │       ├── span.wg-actionsheet__item-content
   │   │       │   ├── span.wg-actionsheet__item-title
   │   │       │   └── span.wg-actionsheet__item-subtitle (可选)
   │   │       ├── span.wg-actionsheet__item-badge (可选)
   │   │       ├── span.wg-actionsheet__item-recommendation (可选)
   │   │       └── i.wg-actionsheet__item-check (选择模式)
   │   ├── div.wg-actionsheet__separator
   │   └── button.wg-actionsheet__cancel
   └── div.wg-actionsheet__safe-area
   ```

5. **文案规则**
   - 选项文本使用动词或动宾短语
   - 取消按钮固定为"取消"
   - 单行展示，不换行
   - 头部描述简短说明操作目的

6. **Canonical HTML** — 提供 3 种典型场景的 HTML：
   - 操作模式 + 单行 + 无头部
   - 操作模式 + 单行有icon + 带头部
   - 选择模式 + 单行

7. **Canonical CSS** — 完整样式，仅使用 token-css-map.md 中的 Token

8. **状态**
   - default / pressed / disabled / selected

9. **可访问性**
   - 使用 `role="dialog"` + `aria-modal="true"`
   - 选项使用原生 `<button>`
   - 选中项使用 `aria-selected`

10. **生成约束**

11. **自检**

12. **规范来源**
    - Figma 节点 `522:51546`
    - Kuikly `ActionSheet` / `showActionSheet` / `showActionSheetSelect`

### 步骤 2：更新 `registry.json`

在 `components` 数组中添加 ActionSheet 条目：

```json
{
  "id": "actionsheet",
  "name": "ActionSheet",
  "category": "feedback",
  "status": "stable",
  "file": "actionsheet.md",
  "keywords": ["操作表", "actionsheet", "底部弹窗", "选择", "操作", "取消"],
  "decisionAxes": {
    "mode": ["action", "select"],
    "header": ["none", "simple", "with-icon", "with-link"],
    "itemType": ["single", "multi"],
    "state": ["default", "pressed", "disabled", "selected"]
  },
  "interactionMode": "css+js"
}
```

## 假设与决策

1. **V1 范围**：仅定义操作模式和选择模式的基础变体。徽章、推荐标签、副标题作为可选 slot 保留在 Anatomy 中但不生成独立 CSS 变体。
2. **交互模式**：`css+js` — 弹窗的显示/隐藏需要 JS 控制，但视觉状态通过 CSS 表达。
3. **头部描述区**：V1 仅定义三种布局（无头部、纯描述、带链接），不单独定义"带图标+无链接"为独立变体，图标作为可选元素出现在头部中。
4. **多行 slot**：V1 在 Anatomy 中保留 slot 结构，但不定义 slot 内部具体样式（类似 Kuikly 的 customContentView）。
5. **安全区**：HTML 原型中通过固定高度模拟，不依赖 JS 动态计算。

## 验证步骤

1. 确认 `actionsheet.md` 格式与 button.md / tabs.md 一致
2. 确认所有 CSS 变量均来自 `token-css-map.md`
3. 确认 HTML Anatomy 遵循 `shared-rules.md` 命名约定
4. 确认 `registry.json` 格式正确且可被解析
5. 确认 Figma 设计中的关键尺寸和颜色均已映射到 Token
