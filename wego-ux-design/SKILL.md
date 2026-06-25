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

`README.md` 仅供维护者查看，不参与 AI 执行。`05-examples/` 仅作示例，不是规范来源。

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
- `03-components/` 只定义 Web 原型中的正式组件契约，不包含或映射 KuiklyUI API。

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

执行 `04-ai-rules/08-requirement-confirmation-rules.md`，确认六个维度：

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

6 个步骤形成依赖链，每步产出内部产物，下一步依赖上一步产物。全部内部完成，不展示给用户。

| 步骤 | 输入 | 产物 | 门禁条件 |
|------|------|------|---------|
| 2.1 页面目标与类型 | 已确认需求 | `目标=[一句话] \| 类型=[6类之一]` | 类型必须是浏览/操作/表单/结果/异常/空之一 |
| 2.2 信息层级 | 页面目标与类型 | `一级=[...] / 二级=[...] / 三级=[...]` | 一级只有一个核心视觉重心 |
| 2.3 布局模式 | 信息层级 | `M[x] / G[x] / 背景=[bg-page\|bg-surface]` | M 和 G 必须从定义选项中选 |
| 2.4 组件匹配 | 信息层级 + 布局 | `命中=[组件列表] / 缺失=[...]` | 命中组件的规则文件已读取；缺失已标注 |
| 2.5 Token 类别 | 组件 + 布局 | `类别=[color, spacing, ...]` | 只选实际需要的类别，不为清单强加 |
| 2.6 交互链路 | 页面类型 + 组件 | `状态链=[初始→...→恢复]` | 适用状态全覆盖，不可逆操作有确认+后果+取消+恢复 |

依赖链：2.1 → 2.2 → 2.3 → 2.4 → 2.5/2.6。跳过任一步，下一步缺少输入无法执行。

具体设计规则见 `04-ai-rules/02-ui-generation-rules.md`，本表只定义步骤顺序、产物和门禁。

### 阶段三：实现

**前置准备：**

1. 复制 `02-tokens/tokens.css` → 项目 `styles/tokens.css`
2. 复制 `resources/fonts/WegoKeyboardN9-*.otf` → `assets/fonts/`
3. 复制 `resources/fonts/iconfont/` 整个目录 → `assets/fonts/iconfont/`
4. **读取 `resources/fonts/iconfont/iconfont.json`，提取 `glyphs` 数组中所有 `font_class`，建立可用图标清单。实现时只从清单中选取图标；需要清单中不存在的图标时，按 `02-tokens/icon-guidelines.md` 第 7 节输出 SVG 内联图标并标注缺失。**
5. 将阶段二 2.4 命中列表中每个组件的 Canonical CSS **逐字复制**写入 `styles/components.css`（未命中不写入）。**复制规则**：从组件 `.md` 文件的 `## Canonical CSS` 区块原样搬运，不得增删规则、修改选择器、添加属性或调整 Token 引用。组件视觉行为只能通过规范中已声明的修饰符 class 实现，禁止在复制时进行"合理优化"或自行补充未定义的交互状态。

**主体实现：**

- HTML：语义结构 + 资源引用。样式加载顺序：`tokens.css` → `iconfont.css`（如有）→ `components.css` → `app.css`
- app.css：页面级业务样式，全部通过 `var(--wg-*)` 使用 Token
- app.js：交互逻辑，驱动阶段二 2.6 设计的状态链

**门禁：** 项目结构完整、资源路径有效、样式加载顺序正确；组件 Canonical CSS 已逐字复制，未增删修改。

### 阶段四：验证与输出

执行 `04-ai-rules/07-final-checklist.md`，对照阶段二设计产物逐项验证：

- Step 1：浏览器验证（关键交互、控制台、资源、响应式）
  - **降级：** 当环境不支持本地服务器或浏览器时，改为静态代码审查
    （资源路径有效性、CSS 变量引用合规性、JavaScript 交互逻辑完整性）
- Step 2：设计产物落地验证（对照 2.1-2.6 产物编号检查是否落地）
- Step 3：合规验证（无硬编码、无自创变体、无装饰性视觉、不内联）

**门禁：** 自查清单逐项通过。未通过项必须修复后重新验证。

**输出：** 项目目录 + 简短运行说明（入口、启动方式、关键交互、验证结果）。默认不输出设计简报和推理过程。

## 任务路由

只读取下表明确列出的文件。禁止扫描或通读整个目录。

| 任务类型 | 必读文件 |
|---------|---------|
| 生成完整页面 | `01-principles/01-design-principles.md`、`02-tokens/token-usage-guidelines.md`、`02-tokens/token-reference.md`、`02-tokens/icon-guidelines.md`、`02-tokens/tokens.css`、`token-css-map.md`、`resources/fonts/iconfont/iconfont.json`、`03-components/registry.json`、`03-components/shared-rules.md`、`04-ai-rules/08-requirement-confirmation-rules.md`、`04-ai-rules/02-ui-generation-rules.md`、`04-ai-rules/06-output-format.md`、`04-ai-rules/07-final-checklist.md`；匹配到组件后再读 registry 指向的对应文件 |
| 生成单个组件或按钮 | `02-tokens/token-usage-guidelines.md`、`02-tokens/token-reference.md`、`02-tokens/icon-guidelines.md`、`02-tokens/tokens.css`、`token-css-map.md`、`resources/fonts/iconfont/iconfont.json`、`03-components/registry.json`、`03-components/shared-rules.md`、`04-ai-rules/08-requirement-confirmation-rules.md`、`04-ai-rules/02-ui-generation-rules.md`、`04-ai-rules/06-output-format.md`、`04-ai-rules/07-final-checklist.md`；再读 registry 指向的目标组件文件 |
| 审查已有界面 | `01-principles/01-design-principles.md`、`02-tokens/token-usage-guidelines.md`、`02-tokens/token-reference.md`、`03-components/registry.json`、`04-ai-rules/03-ui-review-rules.md`、`04-ai-rules/07-final-checklist.md`；识别到已注册组件时读取 `03-components/shared-rules.md` 和对应组件文件；涉及代码时再读 `token-css-map.md` |
| 优化已有界面 | 先按“审查已有界面”读取，再按对应生成任务补充读取 |
| 检查 Token 合规性 | `04-ai-rules/04-token-usage-rules.md`、`02-tokens/token-usage-guidelines.md`、`02-tokens/token-reference.md`、`token-css-map.md` |
| 询问规范、不生成 | 只读用户指定或与问题直接对应的单个规则文件 |

补充限制：

- 不默认读取 `README.md`。
- 不扫描或通读 `03-components/`；只读取 registry、公共规则和当前任务命中的组件文件。
- 不默认读取 `05-examples/`；只有用户明确要求参考示例时才读取对应单个文件。
- 不因为某个详细规则提到其他目录，就扩大本表定义的读取范围。

## Token → CSS 映射

`02-tokens/tokens.json` 是唯一 Token 数据源。`token-css-map.md`、`02-tokens/token-reference.md` 和 `02-tokens/tokens.css` 均由脚本生成，禁止手工修改。

所有设计值通过 CSS 自定义属性使用，完整映射表见 **`token-css-map.md`**。

生成项目时：

- 将 `02-tokens/tokens.css` 复制为项目内的 `styles/tokens.css`。
- 将 `tokens.css` 引用的 `resources/fonts/WegoKeyboardN9-*.otf` 复制到 `assets/fonts/`。
- 将 `resources/fonts/iconfont/` 整个目录复制到 `assets/fonts/iconfont/`，保持 `iconfont.css` 与字体文件（woff2 / woff / ttf）在同一目录下。不得将 `iconfont.css` 单独复制到 `assets/fonts/` 根目录。
- 将页面中使用的每个已注册组件的 Canonical CSS 写入 `styles/components.css`；页面未使用到的组件不写入。
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

- registry 中已注册的组件必须遵守对应组件契约。
- registry 中尚未注册的界面元素，可以使用语义化 HTML、页面级 class 和 JavaScript 完成交互。
- 未注册结构属于当前原型的页面实现，不得使用 `.wg-{component}` 命名、写入 registry，或宣称为正式设计系统组件。
- 页面级临时结构可以完整实现 loading、empty、error、success、校验和导航等状态。
- 如果临时结构具有跨页面复用价值，在交付说明中标记为“组件候选”，但不阻塞当前原型实现。

## Token / 已注册组件缺失处理

当 Token 不够用时，不直接写硬编码值。已注册组件规范不够用时，不修改正式组件契约，可在页面层组合或补充反馈结构，并标注缺失：

```text
当前使用：<最接近的已有 Token 或页面层实现>
原因：<为什么不够用>
建议新增：<建议的 Token 名称或组件能力>
归属位置：<应添加到哪个文件>
```

## 关键约束

- **业务样式不写硬编码设计值** — Token 定义层保存原始值，业务 CSS 通过变量使用
- **不自创正式组件变体** — 页面级临时结构不能改变已注册组件契约
- **不为单页面新增 Token** — Token 至少需要 3 个场景复用才允许新增，否则 Token 体系会碎片化
- **不加装饰性视觉** — 复杂渐变、重阴影、多层卡片会干扰用户对信息层级的判断，违背微购克制风格
- **不牺牲交互闭环** — 组件尚未注册不能成为省略关键流程、状态或恢复路径的理由
- **输出前必须运行验证** — 验证关键交互、资源路径和控制台错误
- **不输出空泛建议** — 每条建议必须说明：问题在哪 → 为什么是问题 → 怎么改 → 依据什么规则
