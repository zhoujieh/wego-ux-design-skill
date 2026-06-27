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

AI 执行任何界面任务时，按 4 阶段闭环执行。每阶段有明确入口、出口和门禁，未通过门禁不得进入下一阶段。

## 2.1 阶段一：需求理解与确认（唯一用户门禁）

执行 `rules/confirmation.md`，确认六个维度：

- **用户角色**：这个页面主要给谁用，用户能力水平、操作习惯、痛点是什么
- **使用场景**：用户从哪里进入，在什么情况下使用，完成后去哪里
- **用户任务**：用户要完成什么，完成标准是什么
- **业务目标**：页面最重要的成功标准是什么，只允许一个最高优先级目标
- **页面范围**：本页面包含什么，不包含什么
- **关键业务规则**：字段、权限、校验、状态、数量限制、风险操作等规则

**门禁：** AI 输出《需求确认卡》，用户确认通过后才允许进入阶段二。格式如下：

```text
📋 需求确认卡
- 我理解的用户角色：[谁，能力水平，操作习惯，痛点]
- 我理解的使用场景：[从哪来，什么情况下用，完成后去哪]
- 我理解的用户任务：[要完成什么，完成标准]
- 我理解的业务目标：[最高优先级的成功标准]
- 本次页面范围：[本页面包含什么]
- 本次不做范围：[本页面不包含什么]
- 已知业务规则：[字段/权限/校验/状态/数量限制/风险操作]
- 缺失信息与设计假设：[缺失但可假设的，标注「设计假设」]
- 需要用户确认的问题：[影响页面方向的缺失信息]
```

**门禁规则：**
- 用户确认《需求确认卡》后，才允许进入阶段二
- 缺失信息影响页面方向 → 必须先向用户确认，不得进入阶段二
- 缺失信息只影响局部细节 → 可列为"设计假设"，但必须在确认卡中显式标注，并请求用户确认

**简短模式：** 用户要求"直接输出""不要解释""给我文件"时：
- 仍然必须输出精简版《需求确认卡》
- 如果存在影响设计方向的缺失信息，最多提出 1 个关键问题
- 不得在页面方向不清晰时直接进入阶段二

**阶段一完成标准：** AI 必须能明确回答以下问题，才允许进入阶段二：
- 这是给谁用的？
- 用户为什么进入这个页面？
- 用户要完成什么？
- 页面成功标准是什么？
- 本页面负责什么？
- 本页面不负责什么？
- 哪些业务规则会影响设计？


## 2.2 阶段二：设计决策（内部门禁，AI 自主，产物驱动）

10 个步骤形成依赖链，每步产出内部产物，下一步依赖上一步产物。全部内部完成，不展示给用户。核心变化：先判断页面如何组合、操作如何分级、滚动如何拆分，再选择组件——禁止从组件开始拼页面。

| 步骤 | 输入 | 产物 | 门禁条件 |
|------|------|------|---------|
| 2.1 页面目标判断 | 已确认需求 | `目标=[一句话] \| 类型=[6类之一]` | 类型必须是浏览/操作/表单/结果/异常/空之一 |
| 2.2 信息结构判断 | 页面目标 | `一级=[...] / 二级=[...] / 三级=[...] / 四级=[...]` | 一级只有一个核心视觉重心 |
| 2.3 页面组合判断 | 信息结构 | `分组=[组列表] / 组间关系=[递进\|并列\|补充\|警示] / 视觉节奏=[紧凑\|留白] / 操作位置=[顶部\|局部\|底部固定\|跟随内容] / 反馈位置=[靠近对象] / 滚动结构=[导航区\|内容区\|操作区]` | 禁止未完成页面组合判断直接选择组件；禁止把所有字段平铺成连续列表 |
| 2.4 操作层级判断 | 页面组合 | `核心动作=[1个] / 辅助动作=[...] / 重复入口降级=[text\|weak\|secondary]` | 同一业务动作只能有一个 primary/strong 表达；其它重复入口必须降级 |
| 2.5 布局与滚动结构判断 | 页面组合 + 操作层级 | `M[x] / G[x] / 背景=[bg-page\|bg-surface] / 滚动=[导航区独立\|内容区滚动\|操作区固定] / 导航区z-index=[值]` | M 和 G 必须从定义选项中选；导航区承载页面级动作时滚动不得带走；普通业务页面最大宽度必须受 --wg-layout-page-max-width 限制 |
| 2.5.1 ui_kits 模式匹配 | §3 粗类型 + 布局 | 读取 `ui_kits/index.json` → 按 `appliesTo`+`keyFeatures` 匹配 → `命中=[ui_kit type]` 或 `未命中=[]` | 命中时自动应用该模式的 `openMode` / `layoutMode` / `background` 并读取 `quality-report.json` 逐条遵守 `layoutRulesCaptured`；NavBar 左侧为取消/关闭时 openMode 必须为 present-bottom；未命中时走 generation.md §6.8 通用规则并产出缺失标注（格式见本文件 §5） |
| 2.6 表单组织判断 | 页面组合 + 操作层级（仅表单型页面） | `分组=[表单组列表] / 每组主交互模式=[输入\|选择\|混合] / 对齐规则=[统一规则]` | 同一 form group 内对齐方式必须统一；禁止左对齐和右对齐混用；表单组是视觉单元不是 cell 堆叠 |
| 2.7 状态反馈判断 | 操作层级 + 表单组织 | `错误恢复=[路径] / loading语义=[任务说明] / loading类型=[skeleton\|局部spinner\|modal\|按钮loading]` | 可修正的错误必须有恢复路径；loading 必须表达任务语义；禁止空 spinner 长时间占位 |
| 2.8 组件匹配 | 信息结构 + 页面组合 + 操作层级 + 布局 + 表单 + 状态 | `命中=[组件列表] / 缺失=[...]` | 命中组件的规则文件已读取；缺失已标注；禁止从组件开始拼页面 |
| 2.9 Token 应用 | 组件 + 布局 | `类别=[color, spacing, ...]` | 只选实际需要的类别，不为清单强加 |
| 2.10 交互链路验证 | 页面类型 + 组件 + 状态反馈 | `状态链=[初始→...→恢复]` | 适用状态全覆盖，不可逆操作有确认+后果+取消+恢复；错误修正后必须清除 error 状态 |

依赖链：2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.5.1 → 2.6（仅表单型）→ 2.7 → 2.8 → 2.9/2.10。跳过任一步，下一步缺少输入无法执行。2.5.1 在所有页面类型中执行；2.6 仅在页面类型为表单型时执行，非表单型页面跳过 2.6 直接进入 2.7。

具体设计规则见 `rules/generation.md`，本表只定义步骤顺序、产物和门禁。


## 2.3 阶段三：实现

**前置准备：**

1. 读取 `design-library/library-consumption.json`
2. 按 `recommendedReadOrder` 读取 `design-library/tokens.json`、`design-library/tokens.css`、`design-library/scaffold.css`、`design-library/components/index.json`
3. 针对阶段二 2.8 命中的每个组件，继续读取对应的 `design-library/components/{slug}.json` 与 `design-library/preview/component-{slug}.html`
4. 复制 `design-library/tokens.css` → 项目 `styles/tokens.css`
5. 需要基础排版和布局工具时，按需复用 `design-library/scaffold.css` 中的通用骨架规则
6. 复制 `design-library/components.css` → 项目 `styles/components.css`
7. 使用图标时，复制 `design-library/assets/fonts/iconfont/` 整个目录 → `assets/fonts/iconfont/`，并按 `rules/icon-guidelines.md` 处理 iconfont 缺失场景
8. 从 `preview/component-{slug}.html` 复制组件 markup；只复制组件本体，不复制演示壳、矩阵或说明文案

**主体实现：**

- HTML：语义结构 + 资源引用。样式加载顺序：`tokens.css` → `iconfont.css`（如有）→ `components.css` → `app.css`
- app.css：只写页面级业务样式和布局胶水，全部通过 `var(--wg-*)` 使用 Token
- app.js：交互逻辑，驱动阶段二设计的状态链

**硬性规则：**

- 必须先读 `library-consumption.json`
- 必须按 `components/index.json` → `components/{slug}.json` → `preview/component-{slug}.html` 的顺序消费组件
- 严禁自己手写组件 CSS
- 严禁改写组件内部 class、modifier、DOM anatomy 或未声明状态

**门禁：** 项目结构完整、资源路径有效、样式加载顺序正确；组件 markup 来自 preview，组件 CSS 来自 `components.css`，未自行增删修改。


## 2.4 阶段四：验证与输出

执行 `rules/checkout.md`，对照阶段二设计产物逐项验证：

- Step 1：浏览器验证（关键交互、控制台、资源、响应式）
  - **降级：** 当环境不支持本地服务器或浏览器时，改为静态代码审查
    （资源路径有效性、CSS 变量引用合规性、JavaScript 交互逻辑完整性）
- Step 2：设计产物落地验证（对照 2.1-2.10 产物编号检查是否落地）
- Step 3：合规验证（无硬编码、无自创变体、无装饰性视觉、不内联）


**自动部署：**

验证通过后，自动部署到 Vercel 获取公网链接：

1. 检查授权：`npx vercel whoami`
   - 已授权 → 进入第 2 步
   - 未授权 → 提示用户执行一次 `npx vercel login`（浏览器授权，仅首次），完成后继续
2. 部署：项目目录下执行 `npx vercel --prod --yes`
3. 提取返回的 `https://xxx.vercel.app` 链接，写入最终输出

**CLI 故障处理：**

若遇到 `Detected linked project does not have "id"` 错误（Vercel CLI 已知 bug），改用以下方式：

```text
npx vercel projects add <项目名>      # 先通过 CLI 创建项目
npx vercel link --project <项目名> --scope <team> --yes   # 链接本地目录
npx vercel deploy --prod --yes       # 正常部署
```

**门禁：** 自查清单逐项通过。未通过项必须修复后重新验证。

**输出：** 项目目录 + 简短运行说明（入口、启动方式、关键交互、验证结果 + 在线链接）。默认不输出设计简报和推理过程。


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

## 4.6 未注册组件的临时实现

当 `design-library/components/index.json` 注册表中尚未覆盖所需界面元素时：

- 可使用语义化 HTML、页面级 class 和 JavaScript 完成交互
- 临时结构不得使用 `.wg-{component}` 命名
- 临时结构不得写入 `design-library/components/` 注册表
- 不得将临时结构宣称为正式设计系统组件
- 页面级临时结构可完整实现 loading、empty、error、success、校验和导航等状态
- 如果临时结构具有跨页面复用价值，在交付说明中标记为"组件候选"，但不阻塞当前原型实现

---

# 5. 缺失内容处理

当 Token 不够用时，**不直接写硬编码值**。当已注册组件规范不够用时，**不修改正式组件契约**。可在页面层组合或补充反馈结构，并按以下格式标注缺失：

缺失 Token 时：

```text
当前使用：<最接近的已有 Token 或页面层实现>
原因：<为什么不够用>
建议新增：<建议的 Token 名称>
归属位置：<应添加到 design-library/tokens-source.json 的哪个位置>
```

缺失组件规范时：

```text
当前使用：<页面层实现方式>
缺失内容：<缺少什么组件能力或变体>
建议补充：<建议的组件能力>
归属位置：<应添加到 design-library/components/{slug}.json 的哪个文件>
```

缺失页面信息时：

```text
当前假设：
影响范围：
建议确认：
```

ui_kits 模式未命中时：

```text
⚠️ 未命中已有页面模式
- 建议新增 ui_kit type: [slug]
- 页面粗类型: [§3 六类之一]
- 关键特征: [keyFeatures 列表，AI 从当前页面观察提取]
- 实际应用的通用规则: [openMode / layoutMode / background 来源]
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
