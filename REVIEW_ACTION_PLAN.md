<!-- 
  wego-ux-design 审查行动清单
  生成日期：2026-06-27
  目标：基于 TRAE 设计库架构，让 AI 稳定输出统一的微购设计页面
  使用方式：按优先级顺序推进，每完成一条勾选 [x]
-->

# 审查行动清单

> **审查结论**：架构和规则设计扎实，但稳定统一输出的核心瓶颈有三个——测试覆盖不够、组件状态不统一、路径引用不一致。
>
> **路线**：P0（3 条）→ P1（3 条）→ P2（2 条），共 8 项。每项独立可验证。

---

## P0：阻碍稳定输出的结构性问题

> 这 3 条不改，AI 的输出行为本质上不可控。优先解决。

### P0-1 补齐 golden fixture 生成样本

- [ ] **P0-1.1** 用 `$wego-ux-design` 生成「商品发布」页面，放入 `tests/fixtures/generated/商品发布/`
  - golden prompt：`tests/golden-prompts/product-publish-page.md`
  - 验收：`python scripts/validate_generated_projects.py` 通过

- [ ] **P0-1.2** 用 `$wego-ux-design` 生成「订单列表」页面，放入 `tests/fixtures/generated/订单列表/`
  - golden prompt：`tests/golden-prompts/order-list-page.md`
  - 验收：`python scripts/validate_generated_projects.py` 通过

- [ ] **P0-1.3** 用 `$wego-ux-design` 生成「搜索空状态」页面，放入 `tests/fixtures/generated/搜索空状态/`
  - golden prompt：`tests/golden-prompts/search-empty-state.md`
  - 验收：`python scripts/validate_generated_projects.py` 通过

- [ ] **P0-1.4** 用 `$wego-ux-design` 生成「删除确认流程」页面，放入 `tests/fixtures/generated/删除确认流程/`
  - golden prompt：`tests/golden-prompts/delete-confirm-flow.md`
  - 验收：`python scripts/validate_generated_projects.py` 通过

- [ ] **P0-1.5** 用 `$wego-ux-design` 生成「表单校验失败」页面，放入 `tests/fixtures/generated/表单校验失败/`
  - golden prompt：`tests/golden-prompts/form-validation-failure.md`
  - 验收：`python scripts/validate_generated_projects.py` 通过

- [ ] **P0-1.6** 用 `$wego-ux-design` 生成「结果页」页面，放入 `tests/fixtures/generated/结果页/`
  - golden prompt：`tests/golden-prompts/result-page.md`
  - 验收：`python scripts/validate_generated_projects.py` 通过

- [ ] **P0-1.7** 用 `$wego-ux-design` 生成「多页导航」项目，放入 `tests/fixtures/generated/多页导航/`
  - golden prompt：`tests/golden-prompts/multi-page-navigation.md`
  - 验收：`python scripts/validate_generated_projects.py` 通过

- [ ] **P0-1.8** 全部 8 个 golden prompt 对应的 fixture 生成完毕，运行 `python scripts/validate_generated_projects.py` 全量通过
  - 验收：8 个项目全部通过，覆盖 6 种页面类型（表单 / 浏览 / 空 / 操作 / 结果 / 多页）

### P0-2 修复 icon 路径引用分裂

- [x] **P0-2.1** 在 `rules/icon-guidelines.md` 中，将所有 `resources/fonts/iconfont/iconfont.json` 路径统一改为 `design-library/assets/fonts/iconfont/iconfont.json`
  - 影响章节：第 1 节"图标资源"、第 2 节"图标查询"、第 7 节"缺失标注"
  - 验收：`rg "resources/fonts" rules/icon-guidelines.md` 无结果

- [x] **P0-2.2** 扫描其他 rules/ 文件，确认没有残留的 `resources/fonts/iconfont` 旧路径
  - 搜索范围：`rules/*.md`、`principles/*.md`
  - 验收：`rg "resources/fonts/iconfont" rules/ principles/` 无结果（icon-guidelines.md 除外，已在上一步修正）

- [x] **P0-2.3** 在 `rules/icon-guidelines.md` 中补充说明：`design-library/assets/fonts/iconfont/iconfont.json` 是运行时查询源，`website/assets/fonts/iconfont/iconfont.json` 是 website 本地副本，两者内容一致
  - 验收：AI 不会再在运行时去读 `website/assets/fonts/` 或 `resources/` 下的 iconfont 文件

### P0-3 统一组件状态，消除 AI 行为不确定性

- [x] **P0-3.1** 逐个审查 8 个 `optimizing` 组件的 `knownIssues`，判断每个 knownIssue 的处置方式
  - 处置选项：
    - A）修复 → 修改 preview HTML 中的 Canonical CSS，运行 `extract_components_css.py`，从 `knownIssues` 中移除
    - B）降级为约束 → 从 `knownIssues` 移除，改写为 `usageHints` 或 `doNotInvent` 中的一条
    - C）转为 P1 待办 → 记录到本文档 P1 区，从 `knownIssues` 移除
  - 8 个 optimizing 组件：`dialog`、`toast`、`loading`、`input`、`form`、`tag`、`cell`、`result`
  - 验收：每个组件的 `knownIssues` 数组为空或已清空

- [x] **P0-3.2** 将所有组件 `status` 统一为 `stable`
  - 修改 `design-library/components/index.json`，8 个 optimizing → stable
  - 验收：`rg '"status": "optimizing"' design-library/components/index.json` 无结果

- [x] **P0-3.3** 在 `SKILL.md` 或 `rules/components.md` 中补充规则：AI 遇到 `knownIssues` 字段时，应照搬契约不修改，不得自行修补；`knownIssues` 仅供维护者查阅
  - 验收：规则文字明确，AI 的行为可预期

---

## P1：影响输出质量的设计完善

### P1-1 scaffold.css 增加 M/G 布局工具类

- [ ] **P1-1.1** 在 `design-library/scaffold.css` 中增加 `.wg-page-m0` ~ `.wg-page-m3` 工具类，封装对应的 `padding-inline` 规则
  - m0 = 0、m1 = `var(--wg-spacing-12)`、m2 = `var(--wg-spacing-24)`、m3 = `var(--wg-spacing-48)`
  - 验收：浏览器中引用 scaffold.css 后，`.wg-page-m2` 左右 padding 为 24px

- [ ] **P1-1.2** 在 `design-library/scaffold.css` 中增加 `.wg-group-g1` / `.wg-group-g2` 工具类，封装对应的 `gap` 规则
  - g1 = `var(--wg-spacing-16)`、g2 = `var(--wg-spacing-24)`
  - 验收：`.wg-group-g1` 内部 children 间距为 16px

- [ ] **P1-1.3** 更新 `rules/generation.md` 的布局章节和 `rules/tokens.md`，明确 AI 可以引用这些工具类代替手写 inline-size padding
  - 验收：规则中描述了 `.wg-page-m{0-3}` 和 `.wg-group-g{1-2}` 的用法

- [ ] **P1-1.4** 在 `rules/checkout.md` 中增加检查项：M/G 模式是否通过 scaffold 工具类表达、而非 app.css 手写 padding
  - 验收：checkout 检查清单中新增此项

### P1-2 preview HTML 加 markup 标记注释，让 AI 精确复制

- [x] **P1-2.1** 在每个 `design-library/preview/component-*.html` 中，用 `<!-- @component-markup-start -->` / `<!-- @component-markup-end -->` 包裹组件本体的 HTML 结构（不含演示壳、矩阵、说明文案）
  - 17 个文件逐个修改
  - 验收：每个 preview HTML 中能精确定位到带标记的组件本体

- [x] **P1-2.2** 更新 `rules/components.md` 的"复制规则"章节，明确 AI 应通过标记注释定位并复制，而不是靠语义判断
  - 验收：规则文字指定了 `<!-- @component-markup-start -->` 和 `<!-- @component-markup-end -->` 标记

- [x] **P1-2.3** 在 `scripts/validate_components.py` 中增加检查项：所有 preview HTML 文件必须包含 `@component-markup-start` 和 `@component-markup-end` 标记
  - 验收：运行 `python scripts/validate_components.py`，缺失标记的文件被检出

### P1-3 削减 SKILL.md 内容密度

- [ ] **P1-3.1** 将 SKILL.md 中"阶段一"～"阶段四"的详细执行描述（约 120 行）移至 `rules/execution.md` 中
  - SKILL.md 中只保留阶段名称、门禁条件和 `rules/execution.md` 的引用链接
  - 验收：SKILL.md 总行数减少约 30%，execution.md 增加相应内容

- [ ] **P1-3.2** 将 SKILL.md 中"组件完善期处理""缺失处理""关键约束"章节合并精简，保留硬性规则，具体示例移至对应 rules 文件
  - 验收：SKILL.md 中"关键约束"部分不超过 10 条核心禁令

- [ ] **P1-3.3** 在 SKILL.md 末尾增加"上下文保护"说明：当 AI context window 不足时，优先保留"任务路由表"和"design-library 路径"区块，其余部分可从 rules/ 按需读取
  - 验收：说明文字清晰，AI 知道截断时的保底行为


### P1-4 统一组件硬编码值为设计 Token（来自 P0-3 knownIssues 转化）

- [ ] **P1-4.1** toast: active opacity 0.6 收敛为组件 Token（`--wg-component-toast-active-opacity`）
  - 验收：toast 的 active 透明度通过 CSS 变量引用而非硬编码

- [ ] **P1-4.2** loading: Skeleton pulse 中间帧透明度 0.4 收敛为 Token
  - 验收：skeleton pulse 动画关键帧透明度通过 CSS 变量引用

- [ ] **P1-4.3** loading: wg-loading__image-icon 内联 SVG mask-image 替换为统一图标资产
  - 验收：image-icon 不再内联 SVG，改用 iconfont 或独立图标引用

- [ ] **P1-4.4** input: number 模式宽度评估是否沉淀为专用组件 Token（`--wg-component-input-number-width` 等）
  - 验收：number 宽度通过单一 Token 表达，不再用 wg-size-64 / wg-size-40 组合推导

- [ ] **P1-4.5** form: focused 态抽取为显式 `.wg-form--focused` 视觉修饰（当前依赖原生焦点反馈）
  - 验收：form 的 focused 态有独立且可预览的 CSS 规则

- [ ] **P1-4.6** cell: active 态统一使用单一表面 Token（`wg-color-state-pressed` 与 `wg-color-surface-active` 二选一）
  - 验收：cell active 态只引用一个表面颜色 Token

- [ ] **P1-4.7** result: result-80 主内容起始位置的固定百分比偏移 Token 化
  - 验收：偏移值通过 CSS 变量表达

- [ ] **P1-4.8** result + toast: active / disabled 透明度 0.6、0.4 收敛为组件级 Token
  - 验收：所有组件透明度通过 CSS 变量引用，无硬编码 0.6 / 0.4 值
---

## P2：细节优化

### P2-1 网站完善或清理

- [ ] **P2-1.1** 决定 website 的去留
  - 选项 A）充实：搭建组件 showcase 页面，展示全部 17 个组件的预览效果，供人工审查
  - 选项 B）移除：删除 `website/` 目录，减少仓库体积和维护负担
  - 验收：要么 website 有完整的组件展示，要么目录不存在

- [ ] **P2-1.2** 如果选择充实，至少完成：
  - 在 `website/scripts/app.js` 中实现侧边栏组件导航
  - 每个组件一个展示页面，引用 `design-library/tokens.css` + `components.css`
  - 启动 `npm run dev` 后可在浏览器中浏览全部组件
  - 验收：本地 dev server 启动后，所有组件可预览

### P2-2 清理冗余文件

- [ ] **P2-2.1** 评估 `参考资料/kuikly_doc/` 目录是否仍需要
  - 当前阶段为"Web 原型"，不涉及 KuiklyUI 代码，这些文档约 50MB
  - 如果后续阶段需要，保留并加 README 说明用途；如果不需要，移除
  - 验收：目录有明确的存留理由和 README，或已移除

- [ ] **P2-2.2** 清理 `.DS_Store` 文件（当前散落在多个子目录中）
  - 执行 `find . -name ".DS_Store" -delete`
  - 在 `.gitignore` 中确认 `.DS_Store` 已忽略
  - 验收：`find . -name ".DS_Store"` 无结果

- [ ] **P2-2.3** 评估 `rules/design-principles.md` 的退役条件是否满足
  - 条件：doNotInvent 覆盖所有不该做的事、hardConstraints 覆盖所有禁止项、Canonical CSS 覆盖所有变体、forbidden.md 覆盖所有视觉禁忌
  - 如果满足，可标记为"兜底安全网，可选读"；如果不满足，标注剩余缺口
  - 验收：principles 文件中有明确的留/退役判断说明

---

## 附录 A：验收里程碑汇总

| 里程碑 | 阶段 | 验收方式 | 预计工作量 |
|--------|------|---------|-----------|
| 🚩 M0 | P0-1 fixture 补齐 | 8/8 golden prompt 通过 validate_generated_projects.py | 中（需逐个 AI 生成） |
| 🚩 M1 | P0-2 路径统一 + P0-3 状态统一 | rg 搜索无旧路径、无 optimizing 状态 | 小（查找替换） |
| 🚩 M2 | P1-1 scaffold 工具类 | 浏览器验证 + 规则更新 | 中（手写 CSS + 改规则） |
| 🚩 M3 | P1-2 markup 标记 | 验证脚本 + 规则更新 | 中（17 个文件 + 脚本） |
| 🚩 M4 | P1-3 SKILL.md 精简 | 行数减少约 30% | 小（文本重组） |
| 🚩 M5 | P2 细节清理 | 目录整洁、无垃圾文件 | 小 |

每个里程碑可独立验收，不必等全部完成。

---

## 附录 B：与 ITERATION_PLAN.md 的关系

| ITERATION_PLAN 任务 | 本次审查对应的行动 | 说明 |
|---------------------|-------------------|------|
| 7.1.1 AI 单组件生成测试 | P0-1 fixture 补齐 | 通过 fixture 生成间接验证单组件 |
| 7.1.2 同上 | P0-1 | 同上 |
| 7.2.1 AI 整页生成测试 | P0-1 fixture 补齐 | 8 个 golden prompt 覆盖 6 种页面类型 |
| 7.3.1 回归测试 | P0-1 fixture 补齐 | 所有 fixture 通过 validate_generated_projects.py |

本次审查的 P0-1 实际上就是 ITERATION_PLAN 阶段 7 的落实方案。P0-2 / P0-3 / P1 / P2 是 ITERATION_PLAN 未覆盖的新发现。

---

> **建议推进顺序**：P0-2（路径统一）→ P0-3（状态统一）→ P0-1（生成 fixture）→ P1-1（scaffold 工具类）→ P1-2（markup 标记）→ P1-3（SKILL.md 精简）→ P2（清理）。
>
> P0-2 和 P0-3 改动小、见效快，先做可以降低 P0-1 生成 fixture 时的 AI 行为不确定性。
