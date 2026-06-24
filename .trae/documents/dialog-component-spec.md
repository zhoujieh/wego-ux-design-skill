# Dialog 组件规范输出计划

## 摘要

为 wego-design-system 项目新增 Dialog（对话框）组件规范文档，遵循已有的组件契约模板（button.md、tabs.md 等），通过 Figma MCP 读取设计源文件，参考 Kuikly Dialog 文档，输出完整的 `dialog.md` 规范文件并更新 `registry.json`。

## 当前状态分析

### 已有资源
- **组件规范模板**：`wego-ux-design/03-components/button.md`、`tabs.md` 等已建立完整的规范结构（使用决策 → 语义模型 → 允许组合 → Anatomy → 文案规则 → Canonical HTML/CSS → 状态 → 可访问性 → 生成约束 → 自检 → 规范来源）
- **公共规则**：`wego-ux-design/03-components/shared-rules.md` 定义了命名约定、生成边界、缺失处理等
- **Kuikly Dialog 文档**：
  - `参考资料/kuikly_doc/basic_components/Dialog.md` — Dialog 组件 API（showTextDialog 参数、DialogTitleIcon、DialogTextColor、关闭行为等）
  - `参考资料/kuikly_doc/API/components/alert-dialog.md` — AlertDialog API
  - `参考资料/kuikly_doc/basic_components/DialogContainer.md` — DialogContainer & DialogUtil 弹窗系统
- **Figma 设计源**：URL 中 node-id 为 `8:60797`，对应 `📙 wegoo 组件应用场景` 文件中的 Dialog 设计

### 缺失项
- `wego-ux-design/03-components/dialog.md` 不存在，需要新建
- `registry.json` 中未注册 Dialog 组件

## 实施步骤

### 步骤 1：通过 Figma MCP 读取设计数据

使用 `get_design_context` 工具读取 Figma 节点 `8:60797` 的设计上下文：
- nodeId: `8:60797`
- artifactType: `COMPONENT_WITHIN_A_WEB_PAGE_OR_APP_SCREEN`
- clientLanguages: `html,css`
- clientFrameworks: `unknown`

同时使用 `get_screenshot` 获取节点截图，用于确认设计细节。

### 步骤 2：使用 `get_variable_defs` 获取设计变量

读取节点 `8:60797` 的设计变量定义（颜色、间距、字号等），用于映射到 wego Token。

### 步骤 3：分析 Figma 设计 + Kuikly 文档，提取规范要素

基于 Figma 设计数据和 Kuikly Dialog 文档，提取以下关键信息：

| 规范要素 | 数据来源 |
|---|---|
| 使用决策（何时用/何时不用） | Figma 应用场景 + Kuikly Dialog 概览 |
| 语义模型（决策维度） | Figma 变体 + Kuikly API 参数分类 |
| 允许组合 | Figma 组件实例 + Kuikly 按钮组合规则 |
| Anatomy（HTML 结构） | Figma 图层结构 + Kuikly 组件结构 |
| 文案规则 | Kuikly 按钮文字限制 + 项目文案规则 |
| Canonical HTML/CSS | Figma 布局数据 + 项目 Token 映射 |
| 状态 | Figma 组件状态 + Kuikly 关闭行为 |
| 可访问性 | 项目公共规则 + ARIA dialog 规范 |

### 步骤 4：编写 `dialog.md` 规范文件

按照已有模板结构编写 `wego-ux-design/03-components/dialog.md`，关键设计决策：

**语义模型初步设计**（待 Figma 数据确认后调整）：

```text
intent    对话框意图
buttons   按钮组合
state     当前交互状态
```

- **intent** 维度：
  - `confirm` — 确认操作（如删除确认、扣费确认）
  - `inform` — 信息告知（如操作成功、温馨提示）
  - `alert` — 警告提示（如无法操作、异常提醒）

- **buttons** 维度：
  - `dual` — 双按钮（取消 + 确认），用于需要用户决策的场景
  - `single` — 单按钮（仅确认/知道了），用于纯信息告知

- **state** 维度：
  - `open` / `closed` — 由 `data-state` 或 `aria-modal` 控制

**Anatomy 初步设计**：

```text
div.wg-dialog-overlay
└── div.wg-dialog[role="dialog"][aria-modal="true"]
    ├── div.wg-dialog__header
    │   ├── i.wg-dialog__icon（可选状态图标）
    │   └── h2.wg-dialog__title
    ├── div.wg-dialog__body
    │   ├── p.wg-dialog__content（文本内容，可选）
    │   │   └── a.wg-dialog__link（可选链接）
    │   └── div.wg-dialog__custom（可选自定义内容区，位于正文下方）
    └── div.wg-dialog__footer
        ├── button.wg-dialog__button.wg-dialog__button--dismiss（左侧/取消按钮）
        └── button.wg-dialog__button.wg-dialog__button--confirm（右侧/确认按钮）
```

**自定义内容区规则**：
- `div.wg-dialog__custom` 是可选插槽，位于正文 `p.wg-dialog__content` 之后、按钮行之前
- 自定义区内容不使用 `.wg-dialog` 命名空间内的子元素 class，由页面级样式控制
- 自定义区仍须使用 wego Token，满足语义和可访问性要求
- 典型场景：费用展示卡片、输入框、预览图、详情列表等
- 自定义区不得包含额外的按钮或操作入口，操作统一由 footer 按钮行承载

**从 Kuikly 参考但不继承的内容**：
- 不继承 Kuikly DSL 语法、DialogUtil 管理方式、conflicting 单例逻辑
- 不继承 contentLink 拼接机制（V1 简化为纯文本 + 可选链接）
- 不继承 DialogTextColor 枚举（使用 wego Token 体系中的颜色）
- 参考：三档意图、双/单按钮组合、标题图标、关闭行为、遮罩样式、customContent 插槽机制

### 步骤 5：更新 `registry.json`

在 `wego-ux-design/03-components/registry.json` 的 `components` 数组中新增 Dialog 注册项：

```json
{
  "id": "dialog",
  "name": "Dialog",
  "category": "feedback",
  "status": "stable",
  "file": "dialog.md",
  "keywords": ["对话框", "dialog", "弹窗", "确认", "提示", "警告", "modal", "alert"],
  "decisionAxes": {
    "intent": ["confirm", "inform", "alert"],
    "buttons": ["dual", "single"],
    "state": ["open", "closed"]
  },
  "interactionMode": "js"
}
```

注意 `interactionMode` 为 `js`，因为 Dialog 需要脚本来控制打开/关闭状态和遮罩交互，不同于纯 CSS 组件。

## 假设与决策

1. **Dialog 属于 `feedback` 类别**：与 Button（action）、Tabs（navigation）不同，Dialog 用于信息反馈和操作确认
2. **V1 支持自定义内容区**：`div.wg-dialog__custom` 作为可选插槽，位于正文和按钮行之间，内容由页面级样式控制，仍须使用 wego Token
3. **V1 不定义链接拼接机制**：Kuikly 的 contentLink/contentLinkEnd 拼接较复杂，V1 简化为纯文本内容
4. **interactionMode 为 `js`**：Dialog 的打开/关闭、遮罩点击、焦点陷阱等需要 JavaScript
5. **参考但不继承 Kuikly DSL**：规范是 HTML 原型契约，不是 KuiklyUI 代码库

## 验证步骤

1. 确认 `dialog.md` 遵循与 `button.md`、`tabs.md` 一致的文档结构
2. 确认所有 CSS 变量引用的 Token 在 `token-css-map.md` 中存在
3. 确认 `registry.json` 格式正确且 Dialog 注册项完整
4. 确认 Anatomy 中的 class 命名遵循 `shared-rules.md` 的命名约定
5. 确认规范来源中正确记录 Figma 节点 ID 和 Kuikly 参考文档
