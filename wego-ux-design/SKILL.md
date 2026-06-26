---
name: wego-ux-design
description: 微购设计系统 — 生成符合微购规范、具备完整交互链路的 Web 原型项目，并支持界面审查、Token 合规检查和规范问答。当用户需要设计微购/wego页面、生成可交互UI原型、做界面demo、审查设计合规性、检查 Token、或询问微购设计规范时自动触发。即使只说"设计一个页面""做个原型""帮我看看这个UI""生成一个按钮样式"，只要在微购项目上下文中都应使用本Skill。覆盖设计原则、Token体系、布局模式、组件契约、交互实现、UI生成与审查。
---

# 微购设计系统 Skill

## 权威边界

`SKILL.md` 是本 Skill 唯一的运行时控制入口。只有本文件可以定义：

- 任务类型
- 必读文件
- 禁止读取的目录
- 执行阶段
- 输出形式

其他 Markdown 文件只提供被选中任务的详细规则，不得自行增加必读文件、改变输出形式或覆盖本文件的阶段边界。

发生冲突时按以下顺序处理：

```text
用户明确需求
↓
SKILL.md
↓
本文件为当前任务指定的详细规则
```

`README.md` 仅供维护者查看，不参与 AI 执行。`examples/` 仅作示例，不是规范来源。

## 设计库路径

运行时设计库根目录固定为：

```text
design-library/
```

生成页面、单组件、组件组合或设计库消费相关任务时，AI **必须先读取**：

```text
design-library/library-consumption.json
```

之后再按其中的 `recommendedReadOrder` 决定继续读取哪些文件。未读取该文件前，不得直接扫描 `design-library/preview/`、`design-library/components/` 或自行猜测组件路径。

## 当前阶段：产品设计（可交互 Web 原型）

**目标：** 通过可运行项目验证页面目标、信息层级、完整交互流程、状态闭环和组件选用。

**阶段边界：**

- 生成页面或组件原型时，输出完整可运行的项目结构目录。
- HTML、CSS、JavaScript 和资源文件分离组织。
- 根据任务需要实现页面跳转、表单校验、状态切换、数据模拟和错误恢复等完整链路。
- 审查界面时，输出带优先级的问题报告。
- 检查 Token 时，输出合规检查结果。
- 询问规范时，直接回答对应规则。
- 当前阶段不涉及 KuiklyUI 代码。
- 正式组件契约只来自 `design-library/components/*.json`，不包含或映射 KuiklyUI API。

## 角色

你是微购设计系统的执行者，不是自由发挥的视觉设计师。

职责链：需求理解与确认 → 设计决策（产物驱动） → 实现 → 验证与输出。每阶段未通过门禁不得进入下一阶段。

## 核心原则

```text
清晰 > 一致 > 效率 > 美观 > 创新
```

微购风格：简洁 · 干净 · 淡雅 · 克制 · 高信息密度 · 微信生态一致。

当不确定时，选择更克制、更清晰、更接近微信生态的方案。

## 执行流程

生成界面时按以下 4 阶段闭环执行。每阶段有明确入口、出口和门禁，未通过门禁不得进入下一阶段。

### 阶段一：需求理解与确认（唯一用户门禁）

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

### 阶段二：设计决策（内部门禁，AI 自主，产物驱动）

10 个步骤形成依赖链，每步产出内部产物，下一步依赖上一步产物。全部内部完成，不展示给用户。核心变化：先判断页面如何组合、操作如何分级、滚动如何拆分，再选择组件——禁止从组件开始拼页面。

| 步骤 | 输入 | 产物 | 门禁条件 |
|------|------|------|---------|
| 2.1 页面目标判断 | 已确认需求 | `目标=[一句话] \| 类型=[6类之一]` | 类型必须是浏览/操作/表单/结果/异常/空之一 |
| 2.2 信息结构判断 | 页面目标 | `一级=[...] / 二级=[...] / 三级=[...] / 四级=[...]` | 一级只有一个核心视觉重心 |
| 2.3 页面组合判断 | 信息结构 | `分组=[组列表] / 组间关系=[递进\|并列\|补充\|警示] / 视觉节奏=[紧凑\|留白] / 操作位置=[顶部\|局部\|底部固定\|跟随内容] / 反馈位置=[靠近对象] / 滚动结构=[导航区\|内容区\|操作区]` | 禁止未完成页面组合判断直接选择组件；禁止把所有字段平铺成连续列表 |
| 2.4 操作层级判断 | 页面组合 | `核心动作=[1个] / 辅助动作=[...] / 重复入口降级=[text\|weak\|secondary]` | 同一业务动作只能有一个 primary/strong 表达；其它重复入口必须降级 |
| 2.5 布局与滚动结构判断 | 页面组合 + 操作层级 | `M[x] / G[x] / 背景=[bg-page\|bg-surface] / 滚动=[导航区独立\|内容区滚动\|操作区固定] / 导航区z-index=[值]` | M 和 G 必须从定义选项中选；导航区承载页面级动作时滚动不得带走；普通业务页面最大宽度必须受 --wg-layout-page-max-width 限制 |
| 2.6 表单组织判断 | 页面组合 + 操作层级（仅表单型页面） | `分组=[表单组列表] / 每组主交互模式=[输入\|选择\|混合] / 对齐规则=[统一规则]` | 同一 form group 内对齐方式必须统一；禁止左对齐和右对齐混用；表单组是视觉单元不是 cell 堆叠 |
| 2.7 状态反馈判断 | 操作层级 + 表单组织 | `错误恢复=[路径] / loading语义=[任务说明] / loading类型=[skeleton\|局部spinner\|modal\|按钮loading]` | 可修正的错误必须有恢复路径；loading 必须表达任务语义；禁止空 spinner 长时间占位 |
| 2.8 组件匹配 | 信息结构 + 页面组合 + 操作层级 + 布局 + 表单 + 状态 | `命中=[组件列表] / 缺失=[...]` | 命中组件的规则文件已读取；缺失已标注；禁止从组件开始拼页面 |
| 2.9 Token 应用 | 组件 + 布局 | `类别=[color, spacing, ...]` | 只选实际需要的类别，不为清单强加 |
| 2.10 交互链路验证 | 页面类型 + 组件 + 状态反馈 | `状态链=[初始→...→恢复]` | 适用状态全覆盖，不可逆操作有确认+后果+取消+恢复；错误修正后必须清除 error 状态 |

依赖链：2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6（仅表单型）→ 2.7 → 2.8 → 2.9/2.10。跳过任一步，下一步缺少输入无法执行。2.6 仅在页面类型为表单型时执行，非表单型页面跳过 2.6 直接进入 2.7。

具体设计规则见 `rules/generation.md`，本表只定义步骤顺序、产物和门禁。

### 阶段三：实现

**前置准备：**

1. 读取 `design-library/library-consumption.json`
2. 按 `recommendedReadOrder` 读取 `design-library/tokens.json`、`design-library/tokens.css`、`design-library/scaffold.css`、`design-library/components/index.json`
3. 针对阶段二 2.8 命中的每个组件，继续读取对应的 `design-library/components/{slug}.json` 与 `design-library/preview/component-{slug}.html`
4. 复制 `design-library/tokens.css` → 项目 `styles/tokens.css`
5. 需要基础排版和布局工具时，按需复用 `design-library/scaffold.css` 中的通用骨架规则
6. 复制 `design-library/components.css` → 项目 `styles/components.css`
7. 使用图标时，复制 `design-library/assets/fonts/iconfont/` 整个目录 → `assets/fonts/iconfont/`，并按 `02-tokens/icon-guidelines.md` 处理 iconfont 缺失场景
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

### 阶段四：验证与输出

执行 `rules/checkout.md`，对照阶段二设计产物逐项验证：

- Step 1：浏览器验证（关键交互、控制台、资源、响应式）
  - **降级：** 当环境不支持本地服务器或浏览器时，改为静态代码审查
    （资源路径有效性、CSS 变量引用合规性、JavaScript 交互逻辑完整性）
- Step 2：设计产物落地验证（对照 2.1-2.10 产物编号检查是否落地）
- Step 3：合规验证（无硬编码、无自创变体、无装饰性视觉、不内联）

**门禁：** 自查清单逐项通过。未通过项必须修复后重新验证。

**输出：** 项目目录 + 简短运行说明（入口、启动方式、关键交互、验证结果）。默认不输出设计简报和推理过程。

## 任务路由

只读取下表明确列出的文件。禁止扫描或通读整个目录。

| 任务类型 | 必读文件 |
|---------|---------|
| 生成完整页面 | `design-library/library-consumption.json`、`principles/design-principles.md`、`rules/execution.md`、`rules/generation.md`、`rules/tokens.md`、`rules/components.md`、`rules/output.md`、`rules/checkout.md`、`02-tokens/icon-guidelines.md`、`token-css-map.md`；再按 `recommendedReadOrder` 读取 `design-library/tokens.json`、`design-library/tokens.css`、`design-library/scaffold.css`、`design-library/components/index.json`，并针对命中组件读取对应 JSON 契约与 preview 文件 |
| 生成单个组件或按钮 | `design-library/library-consumption.json`、`rules/execution.md`、`rules/generation.md`、`rules/tokens.md`、`rules/components.md`、`rules/output.md`、`rules/checkout.md`、`02-tokens/icon-guidelines.md`、`token-css-map.md`；再按 `recommendedReadOrder` 读取目标组件的 JSON 契约与 preview 文件 |
| 审查已有界面 | `design-library/library-consumption.json`、`principles/design-principles.md`、`rules/tokens.md`、`rules/components.md`、`rules/review.md`、`rules/checkout.md`；识别到已注册组件时读取 `design-library/components/index.json`、对应组件 JSON 契约与 preview 文件；涉及代码时再读 `token-css-map.md` |
| 优化已有界面 | 先按“审查已有界面”读取，再按对应生成任务补充读取 |
| 检查 Token 合规性 | `design-library/library-consumption.json`、`rules/tokens.md`、`design-library/tokens.json`、`design-library/tokens.css`、`token-css-map.md` |
| 询问规范、不生成 | 只读用户指定或与问题直接对应的单个规则文件 |

补充限制：

- 不默认读取 `README.md`。
- 不扫描或通读 `design-library/components/`、`design-library/preview/`；只读取 `library-consumption.json`、`components/index.json` 和当前任务命中的组件文件。
- 不默认读取 `examples/`；只有用户明确要求参考示例时才读取对应单个文件。
- 不因为某个详细规则提到其他目录，就扩大本表定义的读取范围。

## Token → CSS 映射

`02-tokens/tokens.json` 是唯一 Token 源数据；`design-library/tokens.json` 和 `design-library/tokens.css` 是运行时消费产物；`token-css-map.md` 是查阅映射。除 `02-tokens/tokens.json` 外，相关生成物禁止手工修改。

所有设计值通过 CSS 自定义属性使用，完整映射表见 **`token-css-map.md`**。

生成项目时：

- 将 `design-library/tokens.css` 复制为项目内的 `styles/tokens.css`。
- 将 `design-library/assets/fonts/iconfont/` 整个目录复制到 `assets/fonts/iconfont/`，保持 `iconfont.css` 与字体文件（woff2 / woff / ttf）在同一目录下。不得将 `iconfont.css` 单独复制到 `assets/fonts/` 根目录。
- 将 `design-library/components.css` 复制为项目内的 `styles/components.css`。
- 在 HTML 中按以下顺序引入样式：`tokens.css` → `iconfont/iconfont.css`（如有）→ `components.css` → `app.css`。`iconfont.css` 的引入路径必须与实际目录结构一致。
- Token 定义层允许保存 HEX、RGBA、px 等原始值；业务 CSS 只能通过 `var(--wg-*)` 使用设计值。

核心用法：

- 颜色：`color: var(--wg-color-text-primary)`
- 间距：`gap: var(--wg-spacing-16)`
- 字号：`font-size: var(--wg-font-size-14)`
- 圆角：`border-radius: var(--wg-radius-md)`

## 原型项目输出规范

- 项目根目录名必须使用中文，精简直接表达页面或组件的主要内容（如 `商品发布`、`登录`、`订单列表`），不使用英文、拼音或通用占位名（如 `prototype`、`demo`、`page1`）。
- 输出完整项目目录，不把 HTML、CSS 和 JavaScript 合并为单文件。
- 最小结构包含 `index.html`、`styles/tokens.css`、`styles/components.css`、`styles/app.css`、`scripts/app.js` 和实际使用的 `assets/`。
- 多页面、多模块或使用构建工具时，可按技术方案扩展目录，并提供明确启动入口。
- 样式通过 `<link>` 引入；行为脚本通过 `<script src>` 或模块入口引入。
- 可使用原生 Web 技术、框架、包管理器、Mock 数据或本地服务；选择以完整实现交互链路和可运行性为准。
- 使用依赖时必须声明依赖和启动命令，不依赖未说明的全局环境。
- 布局使用 CSS Grid / Flexbox，对应 M/G 布局模式。
- 移动端优先，默认设计基准为 375px，同时验证合理的响应式表现。
- 所有关键交互必须可实际操作，不能只展示静态状态截图。

推荐的最小目录：

```text
商品发布/
├── index.html
├── styles/
│   ├── tokens.css
│   ├── components.css
│   └── app.css
├── scripts/
│   └── app.js
└── assets/
    ├── fonts/
    ├── images/
    └── data/
```

只创建任务实际需要的资源子目录，不生成空占位文件。

## 组件完善期处理

- `design-library/components/index.json` 中已注册的组件必须遵守对应 JSON 契约与 preview anatomy。
- 注册表中尚未覆盖的界面元素，可以使用语义化 HTML、页面级 class 和 JavaScript 完成交互。
- 未注册结构属于当前原型的页面实现，不得使用 `.wg-{component}` 命名、写入组件注册表，或宣称为正式设计系统组件。
- 页面级临时结构可以完整实现 loading、empty、error、success、校验和导航等状态。
- 如果临时结构具有跨页面复用价值，在交付说明中标记为“组件候选”，但不阻塞当前原型实现。

## Token / 已注册组件缺失处理

当 Token 不够用时，不直接写硬编码值。已注册组件规范不够用时，不修改正式组件契约，可在页面层组合或补充反馈结构，并标注缺失：

```text
当前使用：<最接近的已有 Token 或页面层实现>
原因：<为什么不够用>
建议新增：<建议的 Token 名称或组件能力>
归属位置：<应添加到 `02-tokens/tokens.json` 或 `design-library/components/*.json` 的哪个文件>
```

## 关键约束

- **业务样式不写硬编码设计值** — Token 定义层保存原始值，业务 CSS 通过变量使用
- **不自创正式组件变体** — 页面级临时结构不能改变已注册组件契约
- **不为单页面新增 Token** — Token 至少需要 3 个场景复用才允许新增，否则 Token 体系会碎片化
- **不加装饰性视觉** — 复杂渐变、重阴影、多层卡片会干扰用户对信息层级的判断，违背微购克制风格
- **不牺牲交互闭环** — 组件尚未注册不能成为省略关键流程、状态或恢复路径的理由
- **输出前必须运行验证** — 验证关键交互、资源路径和控制台错误
- **不输出空泛建议** — 每条建议必须说明：问题在哪 → 为什么是问题 → 怎么改 → 依据什么规则
