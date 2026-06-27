# Execution Rules

> 微购 Design System Skill / rules
> Version 4.0
> 定义 AI 执行微购设计任务的阶段门禁、设计库消费计划、验证与输出要求。

---

# 1. 执行目标

AI 必须基于微购设计系统与 `design-library/` 输出稳定、可执行、符合规范的结果，不得自由创作界面。

必须保证：

- 不偏离微购设计原则
- 不绕过 Token 体系
- 不自创组件规范
- 不跳过设计库消费顺序
- 不输出空泛建议
- 不制造视觉噪音

---

# 2. 标准执行流程

界面生成任务按 4 阶段闭环执行。每阶段有入口、出口和门禁；门禁未通过不得进入下一阶段。

设计知识（页面类型、布局模式、组件契约、禁止事项）均编码在 `design-library/` JSON 契约中，阶段二/三/四消费这些契约而非 prose 规则。本文档只定义流程门禁和产物格式。

## 2.1 阶段一：需求理解与确认（唯一用户门禁）

入口：执行 `rules/confirmation.md`，确认六个维度：

- **用户角色**：主要用户、能力水平、操作习惯、痛点
- **使用场景**：从哪里进入、什么情况下使用、完成后去哪里
- **用户任务**：要完成什么、完成标准是什么
- **业务目标**：页面唯一最高优先级成功标准
- **页面范围**：本页面包含什么、不包含什么
- **关键业务规则**：字段、权限、校验、状态、数量限制、风险操作等

输出：只输出紧凑《需求确认卡》。卡片模板、字段名和空字段规则以 `rules/confirmation.md#3-需求确认卡` 为唯一权威来源，本文件不再重复定义。

门禁规则：

- 生成类任务的首轮回复只能输出《需求确认卡》。
- 用户确认《需求确认卡》后，才允许进入阶段二。
- 未获用户确认前，不得输出原型代码、项目目录、文件内容、组件方案、页面方案、交互实现或在线链接。
- 缺失信息影响页面方向时，必须先向用户确认，不得进入阶段二。
- 不得输出"我理解的用户角色"这类长标签；必须使用上面的短标签。
- 每个字段默认单行表达；`业务规则` 最多 3 条，超过时合并为一句高密度总结，不展开二级列表。
- 不额外输出"按阶段门禁""你回复确认后我继续"这类前后置话术，卡片本身就是阶段一输出。

阶段一完成标准：AI 能明确回答"给谁用、为何进入、完成什么、成功标准、负责范围、不做范围、影响设计的业务规则"后，才允许进入阶段二。

## 2.2 阶段二：设计决策（内部门禁，AI 自主，消费计划驱动）

阶段二只产出阶段三消费设计库必须的信息。全部内部完成，不展示给用户。

先读取 `design-library/page-layout.json` 理解页面类型和布局约束，再通过 `design-library/components/index.json` 匹配组件；禁止从组件开始拼页面。

内部产物固定为《设计库消费计划》：

```text
设计库消费计划
- 页面粗类型：[浏览 / 操作 / 表单 / 结果 / 异常 / 空]（来自 page-layout.json）
- 布局模式：[M0 / M1 / M2 / M3 + G1 / G2]（来自 page-layout.json）
- ui_kit：[命中 type 或 未命中]；约束来源：[quality-report.json 路径或 page-layout.json 通用规则]
- 页面壳约束：[openMode / background / maxWidth / 固定区]
- 转场类型：[push / present / fade]（来自 page-layout.json transitions）
- 组件消费：[slug / variant / state / contract 路径 / preview 路径]
- 资源消费：[iconfont / app icon / media / video / 无]
- 状态覆盖：[loading / empty / error / success / disabled / selected / 其他实际状态]
- 临时结构：[页面级结构与原因 / 无]
- 缺失标注：[缺 Token / 缺组件能力 / 未命中 ui_kit / 缺页面信息 / 无]
```

门禁规则：

- 生成完整页面时，必须读取 `design-library/ui_kits/index.json`，按 `appliesTo` + `keyFeatures` 匹配页面模式。
- 命中 `ui_kit` 时，必须读取对应 `quality-report.json`，将 `layoutRulesCaptured` 写入计划并逐条遵守。
- 未命中 `ui_kit` 时，按 `page-layout.json` 通用规则处理，并按 §4 标注缺失。
- NavBar 左侧为取消或关闭时，`openMode` 必须为 `present-bottom`，不得被页面粗类型推理覆盖。
- 组件消费必须从 `components/index.json` 选择 slug；不得扫描 `preview/` 或凭视觉相似猜组件。
- 每个命中组件必须写明契约文件和 preview 文件；状态和变体只能来自组件契约的 `variantDimensions` 和 `doNotInvent`。
- 未注册结构只能作为页面级临时结构，不得使用 `.wg-{component}` 命名，不得宣称为正式组件。
- 资源消费只列当前页面实际使用的图标、图片、视频或应用图标。
- 计划必须足以推出阶段三要读取、复制和禁止改写的设计库文件；否则不得进入实现。

## 2.3 阶段三：实现（设计库消费）

入口：阶段二《设计库消费计划》已完成，且已明确命中组件、资源、状态覆盖与缺失项。

必须按 `design-library/library-consumption.json` → `recommendedReadOrder` 消费设计库。

读取与复制规则：

- 必须先读 `design-library/library-consumption.json`，获取 `recommendedReadOrder`、`consumptionLayers`、`hardConstraints`。
- 不得未读消费契约就直接读组件预览或开始写代码。
- 不得先扫 `preview/` 再回头猜 slug；不得跳过组件契约直接复制结构。
- 复制 `design-library/tokens.css` → 项目 `styles/tokens.css`。
- 复制 `design-library/scaffold.css` → 项目 `styles/scaffold.css`（M/G 布局工具类来源）。
- 复制 `design-library/components.css` → 项目 `styles/components.css`。
- 使用图标时，复制 `design-library/assets/fonts/iconfont/` 整个目录 → `assets/fonts/iconfont/`。
- 从 `preview/component-{slug}.html` 通过 `@component-markup-start` / `@component-markup-end` 标记定位，只复制标记之间的组件 markup，不复制演示壳、矩阵或说明文案。
- `components/{slug}.json`、`components/index.json` 只用于理解契约，不是可直接输出给用户的页面。

主体实现规则：

- HTML：语义结构 + 资源引用；样式加载顺序为 `tokens.css` → `scaffold.css` → `iconfont.css`（如有）→ `components.css` → `app.css`。
- app.css：只写页面级业务样式和布局胶水，全部通过 `var(--wg-*)` 使用 Token。M/G 布局使用 scaffold.css 工具类，禁止在 app.css 中手写 `padding-inline`/`gap` 伪造效果。
- app.js：驱动阶段二《设计库消费计划》中的状态覆盖和业务交互，不定义新的设计系统组件状态。
- 页面转场按 `page-layout.json` → `transitions` 实现，使用 `data-position` + `data-active` 属性模式，禁止 `display:none` 硬切。

禁止事项（详见 `library-consumption.json` → `hardConstraints`）：

- 严禁自己手写组件 CSS。
- 严禁改写组件内部 class、modifier、DOM anatomy。
- 严禁新增未在契约中声明的交互状态、尺寸或颜色变体。
- 严禁用业务样式覆盖组件内部 Token。

未注册组件临时实现：

- 当 `design-library/components/index.json` 注册表尚未覆盖所需界面元素时，可使用语义化 HTML、页面级 class 和 JavaScript 完成交互。
- 临时结构不得使用 `.wg-{component}` 命名。
- 临时结构不得写入 `design-library/components/` 注册表。
- 不得将临时结构宣称为正式设计系统组件。
- 页面级临时结构可完整实现 loading、empty、error、success、校验和导航等状态。
- 临时结构具备跨页面复用价值时，在交付说明中标记为"组件候选"，但不阻塞当前原型实现。

门禁：项目结构完整、资源路径有效、样式加载顺序正确；组件 markup 来自 preview（通过标记定位），组件 CSS 来自 `components.css`，未自行增删修改。

## 2.4 阶段四：验证与输出

入口：执行 `rules/checkout.md`，对照阶段二《设计库消费计划》逐项验证。

验证要求：

- Step 1：浏览器验证关键交互、控制台、资源、响应式。
- Step 1 降级：环境不支持本地服务器或浏览器时，改为静态代码审查，检查资源路径、CSS 变量引用、JavaScript 交互逻辑完整性。
- Step 2：设计库消费计划落地验证，对照页面壳约束、组件消费、资源消费、状态覆盖和缺失标注检查是否落地。
- Step 3：合规验证，对照 `library-consumption.json` → `hardConstraints` 逐项检查。

部署要求：

- 验证通过后，自动部署到 Vercel 获取公网链接。
- 先执行 `npx vercel whoami` 检查授权；未授权时提示用户执行一次 `npx vercel login`，完成后继续。
- 已授权时，在项目目录执行 `npx vercel --prod --yes`，提取 `https://xxx.vercel.app` 链接写入最终输出。
- 若遇到 `Detected linked project does not have "id"`，改用 `npx vercel projects add <项目名>` → `npx vercel link --project <项目名> --scope <team> --yes` → `npx vercel deploy --prod --yes`。

输出约束：

- 已完成交付时，不得输出"没有额外做浏览器视觉回归或线上部署""未做浏览器验证/部署"这类完成态免责声明。
- 浏览器验证未执行，只能因为环境确实不支持本地服务器或浏览器；此时必须明确标注"阶段四降级为静态代码审查"。
- Vercel 部署未执行，只能因为授权缺失或 CLI 故障阻断；此时必须明确标注"交付被部署门禁阻断"，不得伪装成已完成交付。
- 只要浏览器验证或部署属于本次交付要求且未完成，最终输出就必须报告阻断原因，不得写成普通补充说明。

输出：项目目录 + 简短运行说明（入口、启动方式、关键交互、验证结果 + 在线链接）。默认不输出设计简报和推理过程。

---

# 3. 输入判断

任务类型和读取路由以 `SKILL.md` 为准。本文档只说明进入对应任务后的处理方式。

| 用户需求 | 执行方式 |
|---|---|
| 生成完整页面或单个组件 | 按 §2 四阶段流程执行 |
| 审查已有界面 | 执行 `rules/review.md` + `rules/checkout.md` |
| 优化已有界面 | 先审查，再执行对应生成流程 |
| 检查 Token 合规性 | 读取 `design-library/tokens.json` + `design-library/tokens.css` |
| 询问规范 | 直接回答当前路由选中的规则 |

---

# 4. 缺失内容处理

Token 不够用时，不直接写硬编码值。已注册组件规范不够用时，不修改正式组件契约。可在页面层组合或补充反馈结构，并按以下格式标注缺失。

缺失 Token：

```text
当前使用：<最接近的已有 Token 或页面层实现>
原因：<为什么不够用>
建议新增：<建议的 Token 名称>
归属位置：<应添加到 design-library/tokens-source.json 的哪个位置>
```

缺失组件规范：

```text
当前使用：<页面层实现方式>
缺失内容：<缺少什么组件能力或变体>
建议补充：<建议的组件能力>
归属位置：<应添加到 design-library/components/{slug}.json 的哪个文件>
```

缺失页面信息：

```text
缺失信息：
影响范围：
需要用户确认：
```

ui_kits 模式未命中：

```text
⚠️ 未命中已有页面模式
- 建议新增 ui_kit type: [slug]
- 页面粗类型: [浏览/操作/表单/结果/异常/空之一]
- 关键特征: [keyFeatures 列表，AI 从当前页面观察提取]
- 实际应用的通用规则: [openMode / background 来源 — page-layout.json]
```

以上缺失标注在最终输出中必须各自放在单个 `text` 代码块中展示，不得改写为普通段落、普通列表或表格。

---

# 5. 输出要求

AI 输出必须结论明确、层级清晰、规则可追溯、建议可执行、代码可落地、文档可直接保存。

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

# 6. 最终原则

AI 始终按微购设计系统工作，而不是按通用 UI 审美自由发挥。
