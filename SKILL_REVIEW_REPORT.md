# wego-ux-design Skill 审查报告

> **审查日期**: 2026-06-27  
> **审查范围**: wego-ux-design 技能全量文件 × .trae/ 架构文档 × Trae 内置设计库 × 项目迭代计划  
> **审查原则**: 只审查，不改代码

---

## 一、审查概览

### 1.1 审查方法

通过 3 个并行 Explore Agent 分别深入探查：

| Agent | 探查范围 | 产出 |
|-------|---------|------|
| Agent 1 | wego-ux-design 全量文件（SKILL.md + 10 规则文件 + 设计库 + 脚本） | 规则交叉分析、冲突检测、缺口识别 |
| Agent 2 | .trae/documents/ 全部规划文档 + ITERATION_PLAN + REVIEW_ACTION_PLAN | 待办状态矩阵、过期路径映射、优先级冲突分析 |
| Agent 3 | wego 设计库 vs trae 内置设计库（Nimbus Core）结构对比 | 冗余判定、命名空间对比、依赖关系分析 |

### 1.2 总体结论

| 维度 | 结论 |
|------|------|
| **与 Trae 的冗余** | wego 与 trae/Nimbus Core 是**完全独立的两套设计系统**，无冗余可清理 |
| **逻辑冲突** | 发现 **8 项**不一致/冲突，其中 1 项为编号错误（bug），其余为歧义或过期引用 |
| **规则冗余** | **13 条**核心规则在 3 个以上文件中重复定义，forbidden.md 与各规则文件存在大量重叠 |
| **覆盖缺口** | 发现 **6 项**关键缺口：AGENTS.md 缺失、Golden Fixtures 空白、无障碍规则缺失等 |
| **待办进度** | ITERATION_PLAN 阶段 1-6 已完成，阶段 7（测试）**零进度**；REVIEW_ACTION_PLAN 8 项中仅完成 3 项 |

---

## 二、与 Trae 架构的冗余分析

### 2.1 设计库层面：wego vs Nimbus Core — 无冗余

| 对比维度 | wego design-library | trae dl_builtin_trae (Nimbus Core) |
|---------|--------------------|------------------------------------|
| **定位** | 移动端电商设计系统（微购） | IDE/桌面产品设计系统（暗色主题） |
| **组件数** | 17（actionsheet, button, cell, navbar 等移动组件） | 23（activity-rail, editor-tabs, file-tree 等 IDE 组件） |
| **Token 命名空间** | `--wg-*` | `--bg-*`, `--text-*`（扁平无前缀） |
| **字体** | WegoKeyboard N9（定制字体） | SF Pro + JetBrains Mono |
| **图标方案** | iconfont CSS class（`wego-iconfont-s icon-*`） | 115 个独立 SVG + `icons.js` 运行时渲染 |
| **色彩方案** | 浅色为主 | 纯暗色（`@dark-only`） |
| **UI Kit** | 无 | 2 个 React 18 展示页 |

**结论**: 两套设计库服务于**完全不同的产品和用户群**，使用**不同的命名空间、视觉语言和技术方案**。wego-ux-design 不引用也不依赖 trae 设计库。`参考资料/dl_builtin_trae/` 是独立参考物，**不存在需要清理的冗余**。

### 2.2 配置层面：双平台配置 — 各司其职

| 文件 | 平台 | 作用 |
|------|------|------|
| `wego-ux-design/agents/openai.yaml` | Trae | UI 元数据（display_name, default_prompt），设置 `allow_implicit_invocation: true` |
| `.claude/settings.json` | Claude Code | 启用 skill：`{"skills": ["wego-ux-design"]}` |
| `.claude/skills/wego-ux-design` → 符号链接 | Claude Code | 指向 `wego-ux-design/` |

**结论**: 两个平台的配置互不冲突，各自独立生效。**但缺少 AGENTS.md**，详见第五章缺口分析。

### 2.3 文档层面：.trae/documents/ 中的规划文档

`.trae/documents/` 包含 15 个 Markdown 文件，分为两类：

**组件规格文档（7 个）**: tabs、navbar、dialog、input、cell、actionsheet 等组件的 Figma→代码规格计划。这些是**开发过程的中间产物**，组件已完成 canonical 化，对应的 JSON 契约和 preview HTML 已落地。这些文档是历史记录，**与现有规则文件无冲突**。

**优化方案文档（8 个）**: skill-rules-optimization、skill-codex-trae-compatibility-optimization、merge-page-structure-rules、supplement-icon-rules、iconfont-line-height-plan、navbar-style-optimization-plan、page-bg-and-height-rules、regression-testing-ci-validation、regression-test-benchmark。

**关键发现**: 这些优化方案中引用的文件路径**已过期**（详见第三章 3.2 节），但方案本身提出的问题仍然有效。它们与 `rules/` 目录中的现有规则**不存在内容冲突**，只是尚未落地。

---

## 三、逻辑冲突与不一致

### 3.1 🔴 严重：checkout.md 编号引用错误

- **文件**: `wego-ux-design/rules/checkout.md`
- **位置**: Section 2.6
- **问题**: 写的是「对照阶段二 **2.6 状态链**」，但 execution.md 阶段二中 2.6 是「表单组织判断」，**状态链验证实际上是 2.10**
- **影响**: AI 按图索骥会找不到正确的验证目标，导致 Phase 4 验证流程跳过错位
- **修复**: 将 `2.6 状态链` 改为 `2.10 交互链路验证`

### 3.2 🟡 重要：.trae/documents/ 中的过期文件路径

`skill-rules-optimization.md` 全文引用旧文件路径，与 ITERATION_PLAN 附录 C 重命名后的实际路径不匹配：

| 优化文档引用的旧路径 | 实际路径（已重命名） |
|-------------------|-------------------|
| `03-components/button.md` | 规则已迁移至 `design-library/components/button.json`（契约）+ `design-library/preview/component-button.html`（CSS） |
| `03-components/navbar.md` | 同上 → `design-library/components/navbar.json` + preview |
| `04-ai-rules/02-ui-generation-rules.md` | `rules/generation.md` |
| `04-ai-rules/07-final-checklist.md` | `rules/checkout.md` |
| `02-tokens/icon-guidelines.md` | `rules/icon-guidelines.md` |

- **影响**: 直接按优化文档执行会写到错误路径或找不到目标文件
- **处理**: 执行这些优化前必须先做路径翻译

### 3.3 🟡 重要：confirmation.md 未纳入任务路由表

- **问题**: `SKILL.md` 任务路由表中，无一任务类型列出 `rules/confirmation.md` 为必读文件
- **但是**: `rules/execution.md` Section 2.1 明确要求 Phase 1 执行 `rules/confirmation.md`
- **影响**: 上下文截断场景下（SKILL.md 明确说路由表是最小保留集），AI 会丢失 Phase 1 的确认协议
- **修复**: 在路由表中「生成完整页面」和「优化已有界面」任务类型的必读文件列表中加入 `rules/confirmation.md`

### 3.4 🟡 重要：@component-markup 标记机制存在文件间缺口

- **问题**: `@component-markup-start` / `@component-markup-end` 标记机制**仅在** `rules/components.md` 中记录
- **但是**: `rules/execution.md` Section 4.3 描述了同样的复制边界（「只复制组件 markup」），却**从未提及标记机制**
- **影响**: 如果 AI 只读 execution.md（任务路由表指示如此），会不知道标记定位的存在，可能复制整页演示壳
- **修复**: 在 `rules/execution.md` Section 4.3 中补充标记机制的引用

### 3.5 🟡 重要：scaffold.css 引入方式未明确

- **问题**: 三个文件对 scaffold.css 的使用方式描述不一致：
  - `execution.md` 4.5: 「按需复用」
  - `generation.md` Section 5: 「M/G 模式必须使用 scaffold 工具类，**禁止**手写 padding-inline/gap」
  - `checkout.md` 2.3: 「检查是否使用了 scaffold 类」
- **缺失**: 没有任何文件说明**如何**引入 scaffold.css（复制整个文件？选择性复制类？在 HTML 中 link 引用？）
- **修复**: 在 `rules/generation.md` 或 `rules/output.md` 中明确 scaffold.css 的引入方式（建议：完整复制到 `styles/scaffold.css`，在 tokens.css 之后、components.css 之前加载）

### 3.6 🟢 轻微：SKILL.md Token 映射参考文件不一致

- **SKILL.md** 第 112-126 行: 「完整映射表见 **`design-library/tokens.css`**」，将 tokens.css 本身作为映射参考
- **tokens.md** 和 **generation.md**: 引用 `design-library/token-css-map.md` 作为映射参考
- **影响**: 轻微混淆，不影响功能（两个文件都包含 token 信息）
- **修复**: 统一引用为 `tokens.css`（因为 token-css-map.md 可能不存在于当前结构中）

### 3.7 🟢 轻微：SKILL.md 任务路由表重复条目

- **位置**: SKILL.md 任务路由表「检查 Token 合规性」行
- **问题**: `design-library/tokens.css` 被列出了**两次**
- **修复**: 删除重复条目

### 3.8 🟢 轻微：短模式边界模糊

- **问题**: 三个文件对「短模式」的定义不一致：
  - `execution.md` Section 7: 「只输出最终结果，不输出过程分析」
  - `confirmation.md` Section 8: 「仍需要精简版确认卡，最多 1 个关键问题」
  - `output.md` Section 7: 「生成任务只输出项目链接和运行信息」
- **歧义**: 如果用户在 Phase 1 之前要求短模式，confirmation.md 要求出确认卡，execution.md 暗示跳过过程（可能包括确认卡？）
- **影响**: 轻微，实际使用中 AI 通常能正确理解意图
- **修复**: 在 `rules/confirmation.md` 中明确：短模式下确认卡仍需输出，但其他阶段的分析过程省略

---

## 四、规则冗余分析

### 4.1 跨文件重复规则统计

以下 **13 条**核心规则在 3 个以上文件中重复出现：

| # | 规则 | 出现文件 | 重复次数 |
|---|------|---------|---------|
| 1 | 禁止硬编码设计值（HEX/RGBA/px） | SKILL.md, forbidden.md, generation.md, output.md, checkout.md, tokens.md | 6 |
| 2 | 禁止自创组件变体 | SKILL.md, execution.md, forbidden.md, generation.md, checkout.md, components.md, review.md | 7 |
| 3 | 单一主操作按钮 | execution.md, forbidden.md, generation.md, checkout.md, review.md | 5 |
| 4 | 完整交互链路（含加载/空/错误/确认） | SKILL.md, execution.md, forbidden.md, generation.md, checkout.md, review.md | 6 |
| 5 | 表单组对齐一致性 | forbidden.md, generation.md, checkout.md | 3 |
| 6 | 错误恢复路径 | execution.md, forbidden.md, generation.md, checkout.md, review.md | 5 |
| 7 | 加载必须有语义 | forbidden.md, generation.md, checkout.md | 3 |
| 8 | 禁止组件目录扫描 | SKILL.md, execution.md, tokens.md, components.md, review.md | 5 |
| 9 | 组件发现顺序 | SKILL.md, execution.md, generation.md, tokens.md, components.md, review.md | 6 |
| 10 | 页面最大宽度 670px | SKILL.md, generation.md, output.md, checkout.md | 4 |
| 11 | M/G 布局模式 | SKILL.md, generation.md, checkout.md, tokens.md, review.md | 5 |
| 12 | 禁止模糊输出 | execution.md, forbidden.md, review.md | 3 |
| 13 | CSS 加载顺序 | SKILL.md, generation.md, checkout.md | 3 |

### 4.2 冗余分析结论

- **forbidden.md 与各规则文件的重叠最严重**：forbidden.md 作为「禁止事项总集」，与 generation.md 的 Section 13（20 条禁令）、icon-guidelines.md 的 Section 9（6 条禁令）、review.md 的 Section 13（6 条禁令）大量重复
- **是否需要消除冗余？** 分两层看：
  - **forbidden.md 作为单一禁止清单**有其价值——AI 可以一次性加载所有禁区。但需要确保它是**权威源**，其他文件应引用它而非复制
  - **执行流程类规则**（如组件发现顺序）在多处重复是合理的——不同阶段、不同任务类型都需要知道这个规则
- **建议**: 不急于消除冗余（可能引入新问题），但在后续迭代中可考虑：各规则文件中的禁令改为引用 forbidden.md，减少维护负担

---

## 五、覆盖缺口

### 5.1 🔴 严重：Golden Fixtures 完全空白（无测试验证）

- **现状**: `tests/golden-prompts/` 有 8 个标准测试用例，`tests/fixtures/generated/` 仅有 1 个登录页 fixture
- **缺口**: 其余 7 个 golden prompt 无对应 fixture。整个 skill 的 4 阶段生成流程**从未被端到端 AI 生成验证过**
- **对应计划**: ITERATION_PLAN Phase 7 / REVIEW_ACTION_PLAN P0-1（均未启动）

### 5.2 🔴 严重：AGENTS.md 缺失（阻塞 Claude Code 平台）

- **现状**: 项目根目录无 `CLAUDE.md`、`AGENTS.md` 或任何 AI 入口指令文件
- **影响**: Claude Code（Codex）无法自动发现和加载该 skill。当前 skill **仅在 Trae 平台可用**
- **对应计划**: `skill-codex-trae-compatibility-optimization.md` 第 1 步（未启动）

### 5.3 🟡 重要：原型测试发现的 5 个设计 Bug 未修复

从 `skill-rules-optimization.md`（基于登录/注册原型测试）识别的 5 个问题全部未修复：

| # | 问题 | 影响 |
|---|------|------|
| 1 | 按钮宽度缺少决策策略（页面级 180px vs 表单自适应 343px） | 按钮宽度不一致 |
| 2 | 滚动条未隐藏（`overflow-y: auto` 显示浏览器默认滚动条） | 破坏移动端视觉 |
| 3 | NavBar 背景色未联动页面背景（canonical CSS 只有一个值） | 白页灰导航栏 |
| 4 | 无页面过渡动画（`display: none/flex` 硬切） | 交互生硬 |
| 5 | iconfont 资源路径断裂（文件分离后 @font-face 相对路径失效） | 图标不显示 |

### 5.4 🟡 重要：无障碍规则缺失

- **现状**: 仅在 `components.md`（usageHints）、`checkout.md`（ARIA 检查）、`review.md`（状态审查）中零散提及
- **缺失**: 无独立的无障碍规则文件、无 WCAG 合规清单、无色彩对比度要求、无焦点管理规则、无屏幕阅读器测试要求

### 5.5 🟡 重要：Vercel 部署容错不足

- **现状**: `execution.md` Section 2.4 仅处理一个特定 Vercel CLI bug
- **缺失**: 无网络超时、API 限流、项目创建失败、构建错误等其他部署失败场景的降级策略

### 5.6 🟢 轻微：组件组合任务类型未纳入路由表

- **SKILL.md** 第 40 行提到「组件组合」是任务类型之一
- **但**任务路由表（第 95-110 行）中无对应行。「生成单个组件或按钮」可能是最接近的匹配，但不覆盖多组件组合场景

---

## 六、待办状态总览

### 6.1 ITERATION_PLAN 各阶段状态

| 阶段 | 内容 | 状态 |
|------|------|------|
| 1: 包骨架 | 7 任务（1.1-1.4） | ✅ 全部完成 |
| 2: Button 试点 | 4 任务（2.1-2.2） | ✅ 全部完成 |
| 3: 批量 Canonical 化 | 13 组件，6 批次 | ✅ 全部完成 |
| 4: JSON 契约 + 注册表 | 3 任务（4.1-4.2） | ✅ 全部完成 |
| 5: 消费契约 | 4 任务（5.1-5.2） | ✅ 全部完成 |
| 6: 验证脚本 | 3 任务（6.1-6.3） | ✅ 全部完成 |
| **7: 回归测试** | **4 任务（7.1-7.3）** | **❌ 零进度** |

### 6.2 REVIEW_ACTION_PLAN 各条目状态

| ID | 条目 | 状态 |
|----|------|------|
| P0-1 | 生成 8 个 Golden Fixture | ❌ 未开始 |
| P0-2 | 修复 icon 路径引用分裂 | ✅ 已完成 |
| P0-3 | 统一组件状态 | ✅ 已完成 |
| P1-1 | scaffold.css M/G 布局工具类 | ❌ 未开始 |
| P1-2 | preview HTML 标记注释 | ✅ 已完成 |
| P1-3 | SKILL.md 内容减负（~30% 行数缩减） | ❌ 未开始 |
| P1-4 | 硬编码值 Token 化（8 子项） | ❌ 未开始 |
| P2-1 | website/ 清理/决策 | ❌ 未开始 |
| P2-2 | 冗余文件清理 | ❌ 未开始 |

### 6.3 .trae/documents/ 优化方案落地状态

| 文档 | 提出方案 | 落地状态 |
|------|---------|---------|
| skill-rules-optimization.md | 6 项修改（按钮/滚动条/NavBar/过渡/iconfont） | ❌ 全部未落地 |
| skill-codex-trae-compatibility-optimization.md | 6 步兼容方案（AGENTS.md/降级策略/验证扩展） | ❌ 全部未落地 |
| merge-page-structure-rules.md | 合并页面结构规则到主规则文件 | ⚠️ 不确定 |
| supplement-icon-rules.md | 补充图标使用规则 | ✅ 已体现为 icon-guidelines.md |
| iconfont-line-height-plan.md | iconfont line-height: 1 规范化 | ⚠️ 不确定 |
| navbar-style-optimization-plan.md | NavBar 样式 6 项优化 | ⚠️ 不确定 |
| page-bg-and-height-rules.md | 页面背景/高度规则 | ✅ 已融入 generation.md |
| regression-testing-ci-validation.md | 回归测试 CI 体系 | ✅ 已落地（CI workflow） |
| regression-test-benchmark.md | 测试基准扩展 | ❌ 未开始 |

---

## 七、必须做的 3 个事项

---

### 事项 1: 生成 Golden Fixtures 并跑通回归测试

**为什么必须做**

整个 wego-ux-design skill 经历了 6 个阶段的架构建设（设计库、组件契约、消费契约、验证脚本），但**从未端到端验证过 AI 使用该 skill 能否产出正确结果**。`tests/golden-prompts/` 下有 8 个标准测试用例，`tests/fixtures/generated/` 下只有 1 个登录页样本。没有完整的回归测试基线，任何后续规则修改都无法判断是改进还是退步。这是**所有后续工作的前置条件**。

**具体行动步骤**

| 步骤 | 行动 | 说明 |
|------|------|------|
| 1.1 | 用 8 个 golden prompts 分别驱动 AI 生成原型项目 | 在 Trae 或 Claude Code 中逐个执行，每个 prompt 产出一个项目目录 |
| 1.2 | 将生成的项目放入 `tests/fixtures/generated/` | 按页面类型命名（如 `登录/`, `商品发布/`, `订单列表/` 等） |
| 1.3 | 运行 `scripts/validate_generated_projects.py --require-fixtures` | 检查结构完整性、CSS 纯度、JS 行为、Token 一致性 |
| 1.4 | 记录每个 fixture 的验证结果 | 分类：通过 / 部分失败（列出失败项）/ 完全失败 |
| 1.5 | 修复导致验证失败的 skill 规则问题 | 可能是规则表述不清、设计库缺失、或 token 映射错误 |
| 1.6 | 重新生成 → 重新验证，直到 8/8 通过 | 迭代至全部绿灯 |
| 1.7 | 将 fixture 提交到仓库，确认 CI 通过 | 确保 GitHub Actions validate.yml 在 PR 时能通过 |

**涉及文件**

- `tests/golden-prompts/*.md`（8 个）
- `tests/fixtures/generated/`（目标目录）
- `scripts/validate_generated_projects.py`
- `.github/workflows/validate.yml`
- 可能需修改的 skill 文件：`rules/generation.md`, `rules/output.md`, `rules/checkout.md`, `design-library/tokens.css`

**验收标准**

- [ ] 8 个 golden prompts 全部有对应的 fixture 目录
- [ ] `validate_generated_projects.py --require-fixtures` 全部通过
- [ ] CI（`validate.yml`）在包含所有 fixture 的分支上绿色通过

---

### 事项 2: 创建 AGENTS.md 实现跨平台兼容

**为什么必须做**

当前 skill 仅在 Trae 平台可用。Claude Code 需要 `AGENTS.md` 或 `CLAUDE.md` 作为指令入口文件——项目根目录**完全没有**。这意味着在 Claude Code 环境中，即使 `.claude/settings.json` 启用了 skill，AI 也无法获取到 skill 的核心指令（skill 触发条件、执行流程、任务路由）。`.trae/documents/skill-codex-trae-compatibility-optimization.md` 已将此项列为第 1 步，但至今未执行。这个问题的修复**工作量小（~60 行 Markdown）、影响大（解锁整个第二平台）**。

**具体行动步骤**

| 步骤 | 行动 | 说明 |
|------|------|------|
| 2.1 | 在项目根目录创建 `AGENTS.md` | 约 60 行，作为 Claude Code 的指令入口 |
| 2.2 | 内容结构：指向 SKILL.md、摘要 4 阶段流程、核心约束、平台适配说明 | 不重复 SKILL.md 内容，而是做路由和摘要 |
| 2.3 | 补充平台降级说明 | 浏览器验证不可用 → 静态代码审查；Figma MCP 不可用 → 文本描述替代 |
| 2.4 | 在 `wego-ux-design/scripts/validate_skill.py` 中增加 `validate_agents_md()` 函数 | 检查 AGENTS.md 存在性、指向 SKILL.md 的正确性 |
| 2.5 | 运行验证，确认通过 | `python3 wego-ux-design/scripts/validate_skill.py` |

**涉及文件**

- `AGENTS.md`（新建，项目根目录）
- `wego-ux-design/SKILL.md`（补充平台降级说明，在 Stage 4 加入 Mode A/B 分支）
- `wego-ux-design/rules/checkout.md`（如尚未包含静态审查模式，补充 Mode B 检查项）
- `wego-ux-design/scripts/validate_skill.py`（扩展验证函数）
- `.trae/documents/skill-codex-trae-compatibility-optimization.md`（参考方案）

**验收标准**

- [ ] 项目根目录存在 `AGENTS.md`，内容覆盖：skill 入口指向、4 阶段摘要、核心约束、平台降级策略
- [ ] `AGENTS.md` 不重复 SKILL.md 的完整内容（仅做路由和摘要）
- [ ] `validate_skill.py` 包含 `validate_agents_md()` 检查并通过

---

### 事项 3: 修复原型测试中发现的 5 个设计 Bug

**为什么必须做**

`skill-rules-optimization.md` 记录了从**真实登录/注册原型测试**中发现的 5 个具体问题。这不是理论推演，而是 AI 按照当前规则实际生成的界面中出现的 bug——按钮宽度不一致、滚动条未隐藏、NavBar 背景色错误、页面切换无动画、iconfont 路径断裂。这些问题**直接影响产出的 UI 质量和视觉还原度**。修复它们需要的改动精准且范围可控（5 个明确的修改点），适合在事项 1（回归测试）之前或并行进行——修复后的规则产出更正确的 fixture。

**具体行动步骤**

| 步骤 | 行动 | 涉及文件 | 说明 |
|------|------|---------|------|
| 3.1 | **按钮宽度决策策略** | `rules/generation.md` 或 `design-library/components/button.json` | 新增 Width Strategy 段落：表单页按钮 → 自适应容器宽度（M2 布局下 343px），结果/异常页按钮 → 固定 180px |
| 3.2 | **滚动条隐藏规则** | `rules/generation.md` Section 5（页面高度与滚动） | 增加 `::-webkit-scrollbar { display: none; }` 规则，ScrollView 容器添加 `scrollbar-width: none`（Firefox） |
| 3.3 | **NavBar 背景-页面背景联动** | `rules/generation.md` Section 5 + `design-library/preview/component-navbar.html` | 规则中明确：灰底页（bg-page）→ NavBar `toolbar.solid`，白底页（bg-surface）→ NavBar `bg-surface`。canonical CSS 需补 `.page-surface .wg-navbar--bg-default` 选择器 |
| 3.4 | **页面过渡动画规则** | `rules/generation.md` Section 9 | 已有 Push/Present/Fade 定义，检查是否完整。补充禁止 `display: none/flex` 硬切，强制使用 `transform` + `transition`，定义默认参数（duration: 300ms, easing: cubic-bezier(0.4, 0, 0.2, 1)） |
| 3.5 | **iconfont 路径修复** | `rules/icon-guidelines.md` + `rules/output.md` + `SKILL.md` | 明确要求：复制整个 `iconfont/` 目录（不只是 CSS），HTML 中 link 路径为 `assets/fonts/iconfont/iconfont.css`，验证 @font-face 相对路径在复制后仍有效 |

**注意**: 步骤 3.3 中 `skill-rules-optimization.md` 引用的旧路径（`03-components/navbar.md`）需替换为实际路径（`design-library/components/navbar.json` + `design-library/preview/component-navbar.html`）。所有 5 个修改点都需对照 ITERATION_PLAN 附录 C 的路径重命名表做翻译。

**涉及文件**

- `rules/generation.md`（步骤 3.1, 3.2, 3.3, 3.4）
- `rules/icon-guidelines.md`（步骤 3.5）
- `rules/output.md`（步骤 3.5）
- `SKILL.md`（步骤 3.5）
- `design-library/preview/component-navbar.html`（步骤 3.3，可能需要补 CSS）
- `design-library/preview/component-button.html`（步骤 3.1，检查是否需要补宽度变体 CSS）

**验收标准**

- [ ] 生成一个表单页面原型，按钮宽度自适应容器（非固定 180px）
- [ ] 生成一个列表页面原型，滚动条在 WebKit 和 Firefox 中均不可见
- [ ] 生成一个白底页面 + NavBar 原型，NavBar 背景为白色（非灰色）
- [ ] 生成一个多页面原型，页面切换有 Push/Present/Fade 动画（非 display 硬切）
- [ ] 生成任意原型，iconfont 图标正常显示（@font-face 加载成功，路径不 404）

---

## 八、审查总结

### 优势

1. **三层架构清晰**: 控制层（规则）→ 产物层（设计库）→ 工具层（脚本），职责分明
2. **权威链明确**: User > SKILL.md > 任务规则，冲突时有明确裁决顺序
3. **4 阶段门禁流程**: 需求确认 → 设计决策 → 实现 → 验证，每阶段有 gate，质量有保障
4. **禁止体系全面**: forbidden.md 覆盖视觉/Token/图标/组件/布局/文案/AI 行为/状态 8 大类
5. **CI 自动化到位**: GitHub Actions 在每次 push/PR 时运行 4 个验证脚本，纯 Python 无外部依赖

### 待改进

1. **测试缺失是最紧迫的问题** — 6 个阶段的建设投入后，从未验证过 AI 使用效果
2. **跨平台是隐形天花板** — 缺少 AGENTS.md 意味着 skill 只能服务 Trae 用户，Claude Code 用户被排除
3. **5 个已发现的设计 Bug 未修复** — 知道问题在哪，但未排入执行
4. **规则冗余增加维护负担** — 13 条规则在 3+ 文件中重复，修改时需多处同步
5. **规划文档与代码脱节** — .trae/documents/ 中的路径已过期，降低了优化方案的可用性

### 建议执行顺序

```
事项 2（AGENTS.md，解锁平台）
   ↓
事项 3（5 个设计 Bug 修复，提升输出质量）
   ↓
事项 1（Golden Fixtures 回归测试，验证全链路）
   ↓
P1 事项（SKILL.md 减负、scaffold 工具类、硬编码 Token 化）
   ↓
P2 事项（website 清理、冗余文件清理）
```

> **注**: 事项 2 优先于事项 1 是因为 AGENTS.md 是低成本高回报的基建项，创建后即可在 Claude Code 中进行事项 3 和事项 1 的 AI 生成测试，避免单平台依赖。

---

*本报告由 3 个并行 Explore Agent 深度探查后综合生成，覆盖 wego-ux-design 技能全量文件 × .trae/ 架构文档 × Trae 内置设计库 × 项目迭代计划，共识别 8 项逻辑冲突、13 条跨文件冗余、6 个覆盖缺口、3 个必须事项。*
