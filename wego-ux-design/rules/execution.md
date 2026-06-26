# Execution Rules

> 微购 Design System Skill / rules
> Version 3.0
> 本文档定义 AI 执行微购设计任务的总流程，以及设计库消费阶段的强制子步骤。

---

# 1. 执行目标

AI 的目标不是自由创作界面，而是基于微购设计系统与 `design-library/` 输出稳定、可执行、符合规范的结果。

AI 必须保证：

- 不偏离微购设计原则
- 不绕过 Token 体系
- 不自创组件规范
- 不跳过设计库消费顺序
- 不输出空泛建议
- 不制造视觉噪音

---

# 2. 标准执行流程

AI 执行任何界面任务时，按 4 阶段闭环执行。每阶段有明确门禁，未通过不得进入下一阶段。

```text
阶段一：需求确认（唯一用户门禁）
  执行 rules/confirmation.md
  确认用户任务 / 业务目标 / 使用场景
  ↓ 门禁：用户确认“对吗？”
↓
阶段二：设计决策（内部门禁，AI 自主，产物驱动）
  页面目标 → 信息层级 → 页面组合 → 操作层级
  → 布局与滚动 → 表单组织（如适用） → 状态反馈 → 组件匹配 → Token 应用 / 交互链路
  ↓ 门禁：阶段二产物链完整
↓
阶段三：实现（设计库消费阶段）
  先读 design-library/library-consumption.json
  → 按 recommendedReadOrder 读取 tokens / components / icons / uikit 层
  → 从 preview 复制组件 markup
  → 复制并链接 tokens.css / components.css / iconfont 资源
  → 只补页面级布局胶水与业务交互
  ↓ 门禁：项目结构完整、资源路径有效、组件 CSS 未手写
↓
阶段四：验证与输出
  执行 rules/checkout.md
  浏览器验证 + 设计产物落地验证 + 合规验证
  ↓ 门禁：自查清单逐项通过
  输出项目目录 + 简短运行说明
```

阶段和门禁的详细定义以 `SKILL.md` 为准。本文档不重复具体设计规则，只说明执行流程的总体结构。

---

# 3. 输入判断

任务类型和读取路由以 `SKILL.md` 为准。本文档只说明进入对应任务后的处理方式：

| 用户需求 | 执行方式 |
|---|---|
| 生成完整页面或单个组件 | 执行 `rules/generation.md` |
| 审查已有界面 | 执行审查路由和 `rules/checkout.md` |
| 优化已有界面 | 先审查，再执行对应的生成规则 |
| 检查 Token 合规性 | 执行 `rules/tokens.md` |
| 询问规范 | 直接回答当前路由选中的规则 |

“直接输出”“不要解释”等要求只影响表达方式，不产生新的任务路由。

---

# 4. 阶段三：设计库消费子步骤

阶段三不是“自己写一套组件”，而是消费设计库：

## 4.1 先读消费契约

必须先读取：

```text
design-library/library-consumption.json
```

从中获取：

- `recommendedReadOrder`
- `consumptionLayers`
- `downstreamScenarios`
- `hardConstraints`

未读取消费契约，不得直接读组件预览或开始写代码。

## 4.2 按推荐顺序读取

生成单组件或整页时，必须按以下方向推进：

```text
library-consumption.json
↓
tokens.json / tokens.css / scaffold.css
↓
components/index.json
↓
components/{slug}.json
↓
preview/component-{slug}.html
↓
components.css
↓
iconfont 资源（组件需要图标时）
```

不得先扫 preview 再回头猜 slug，也不得跳过组件契约直接复制结构。

## 4.3 复制边界

- `tokens.css`、`scaffold.css`、`components.css`：允许复制到项目内再引用
- `preview/component-{slug}.html`：只复制组件 markup，不复制整页演示壳
- `components/{slug}.json`、`components/index.json`：只用于理解契约，不是可直接输出给用户的页面
- `assets/fonts/iconfont/`：使用图标时复制整个目录

## 4.4 禁止事项

- 严禁自己手写组件 CSS
- 严禁改写预览组件的 class、modifier、DOM anatomy
- 严禁新增未在契约中声明的交互状态、尺寸或颜色变体
- 严禁用业务样式覆盖组件内部 Token

## 4.5 主体实现

- HTML：语义结构 + 资源引用
- app.css：只写页面级布局胶水和业务态样式，全部通过 `var(--wg-*)`
- app.js：驱动状态链和业务交互，不定义新的设计系统组件状态

---

# 5. 缺失内容处理

缺失 Token 时：

```text
当前使用：
原因：
建议新增：
归属位置：
```

缺失组件规范时：

```text
当前使用：
缺失内容：
建议补充：
归属位置：
```

缺失页面信息时：

```text
当前假设：
影响范围：
建议确认：
```

---

# 6. 输出要求

AI 输出必须满足：

- 结论明确
- 层级清晰
- 规则可追溯
- 建议可执行
- 代码可落地
- 文档可直接保存

不允许输出：

```text
可以更高级
视觉更现代
建议更美观
可以更有设计感
```

必须说明：

```text
哪里有问题
为什么有问题
怎么修改
依据什么规则
```

---

# 7. 简短模式

当用户要求“直接输出”“不要解释”“给我文件”时：

只输出最终结果。

不输出过程分析。

---

# 8. 最终原则

AI 始终按微购设计系统工作，而不是按通用 UI 审美自由发挥。
