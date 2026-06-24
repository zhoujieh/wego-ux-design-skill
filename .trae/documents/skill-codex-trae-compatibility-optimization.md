# 微购设计 Skill 双平台兼容性优化方案

## 总结

当前 skill 的核心设计(4 阶段流程、任务路由、Token 体系、组件契约)质量良好且平台无关。问题集中在**入口配置**和**平台适配**两个层面。

**核心发现:**
- Trae 读取 SKILL.md + 目录结构作为 skill 入口
- Codex 读取 AGENTS.md 作为执行指令入口
- 当前项目缺少 AGENTS.md,Codex 无法正确加载 skill
- 阶段四浏览器验证和 Figma MCP 集成假设了特定工具能力,需要降级策略

---

## 当前状态分析

### 平台配置格式差异

| 平台 | 配置格式 | 当前状态 | 说明 |
|------|---------|---------|------|
| **Trae** | SKILL.md frontmatter + 目录结构 | ✅ 已完整 | Trae 通过 SKILL.md 的 YAML frontmatter 识别 skill |
| **Codex** | AGENTS.md (Markdown 指令文件) | ❌ 缺失 | Codex 通过 AGENTS.md 获取执行指令 |
| **openai.yaml** | UI 元数据 | ⚠️ 仅 Trae 使用 | 提供显示名称和默认提示词,Codex 不读取 |

**AGENTS.md 规范要点:**
- 控制在 100 行以内(硬上限 300 行)
- 只放 Codex 可能忽略的项目特定规则
- 必须指向完整执行指令文件(SKILL.md)
- 包含:入口文件、执行流程摘要、核心约束、平台适配说明

### 已做好的部分(不需要改动)

| 层面 | 说明 |
|------|------|
| SKILL.md 权威边界 | 唯一定义任务类型、必读文件、阶段边界、输出形式 |
| 4 阶段闭环 | 需求确认 → 设计决策 → 实现 → 验证,逻辑清晰,平台无关 |
| 任务路由表 | 精确的文件读取控制,两个平台都能按表执行 |
| 产物驱动门禁 | 不依赖特定工具,纯逻辑判断 |
| Token/组件规则 | 纯设计规则,平台无关 |
| 输出格式 | 纯文本结构,平台无关 |
| 规则文件体系 | 01~08 规则文件职责清晰,被 SKILL.md 按需选择 |

### 存在的问题

#### 问题 1:缺少 AGENTS.md 入口(Codex 无法加载 skill)

**现状:**
- 项目根目录没有 AGENTS.md
- 只有 `agents/openai.yaml`(UI 元数据)
- Codex 无法找到执行指令入口

**影响:**
- Codex 环境下 skill 完全不可用
- 用户需要手动告诉 Codex "读取 SKILL.md",体验差

#### 问题 2:阶段四浏览器验证假设了特定工具

**现状:**
`07-final-checklist.md` Step 1 要求:
- 关键交互链路可操作
- 控制台无阻断错误
- 资源加载成功
- 响应式表现合理

**问题:**
- 这些需要启动本地服务器 + 浏览器验证
- Trae 有 RunCommand + OpenPreview
- Codex 能执行命令,但浏览器控制能力可能受限
- 没有降级策略时,Codex 环境可能无法完成验证

#### 问题 3:Figma MCP 集成无降级策略

**现状:**
`08-requirement-confirmation-rules.md` 第 4 节定义了 Figma 链接处理流程,假设 Figma MCP 可用。

**问题:**
- Codex 环境不一定有 Figma MCP
- 没有降级策略时,流程会卡住

#### 问题 4:阶段一用户确认方式未做平台适配

**现状:**
SKILL.md 定义确认语句必须输出。

**问题:**
- Trae 可通过 AskUserQuestion 实现交互式确认
- Codex 通过文本交互
- 确认语句本身是平台无关的,但交互方式可能不同
- **这个问题实际上不严重**:确认语句是文本输出,两个平台都能输出

---

## 优化方案

### 改动 1:新增 AGENTS.md(Codex 入口)

**文件:** 项目根目录 `AGENTS.md`

**目标:** 让 Codex 知道读什么、怎么执行、有什么约束。

**内容:**

```markdown
# 微购设计系统 Skill

## 入口文件

**SKILL.md** 是本 skill 唯一的运行时控制入口。

执行任何任务前,必须先读取 SKILL.md,它定义:
- 任务类型和必读文件路由
- 4 阶段执行流程和门禁
- 输出形式和约束

## 执行流程

按 SKILL.md 定义的 4 阶段闭环执行:

1. **阶段一:需求确认** — 确认用户任务/业务目标/使用场景,输出确认语句
2. **阶段二:设计决策** — 6 步依赖链(2.1→2.2→2.3→2.4→2.5/2.6),全部内部完成
3. **阶段三:实现** — 前置准备(tokens/字体/组件 CSS)+ 主体实现(HTML/app.css/app.js)
4. **阶段四:验证与输出** — 验证 + 输出项目目录

每阶段有门禁,未通过不得进入下一阶段。

## 核心约束

- 业务 CSS 不写硬编码设计值,只通过 `var(--wg-*)` 使用 Token
- 不自创正式组件变体
- HTML 不内联业务 CSS 和 JavaScript
- 不扫描或通读整个组件目录,只读取任务路由指定的文件
- 阶段四验证:环境支持浏览器时做浏览器验证,不支持时降级为静态代码审查

## 平台适配

- **浏览器验证:** 当环境不支持本地服务器或浏览器时,降级为静态代码审查(资源路径有效性、CSS 变量引用合规性、JavaScript 交互逻辑完整性)
- **Figma MCP:** 不可用时,提示用户提供截图或文字描述替代
- **用户交互:** 通过文本交互完成需求确认,不依赖特定交互组件

## 文件结构

```
wego-ux-design/
├── SKILL.md                    # 唯一运行时入口
├── 01-principles/              # 设计原则
├── 02-tokens/                  # Token 体系
├── 03-components/              # 组件契约
├── 04-ai-rules/                # 详细规则(被 SKILL.md 按需选择)
├── 05-examples/                # 示例(非规范)
├── agents/openai.yaml          # Trae UI 元数据
└── scripts/validate_skill.py   # 验证脚本
```
```

**理由:**
- AGENTS.md 简洁(约 60 行),符合 Codex 规范
- 明确指向 SKILL.md 作为完整执行指令
- 提供流程摘要和核心约束,Codex 不需要读完所有文件就能理解整体结构
- 明确平台适配策略,解决工具能力差异
- 保留 openai.yaml(Trae 特定配置),不影响 Trae 兼容性

### 改动 2:阶段四增加平台降级策略

**文件:** `SKILL.md`(阶段四部分)+ `04-ai-rules/07-final-checklist.md`

**SKILL.md 改动:** 在阶段四"门禁"前增加降级说明:

```markdown
### 阶段四:验证与输出

执行 `04-ai-rules/07-final-checklist.md`,对照阶段二设计产物逐项验证:

- Step 1:浏览器验证(关键交互、控制台、资源、响应式)
  - **降级:** 当环境不支持本地服务器或浏览器时,改为静态代码审查
    (资源路径有效性、CSS 变量引用合规性、JavaScript 交互逻辑完整性)
- Step 2:设计产物落地验证(对照 2.1-2.6 产物编号检查是否落地)
- Step 3:合规验证(无硬编码、无自创变体、无装饰性视觉、不内联)

**门禁:** 自查清单逐项通过。未通过项必须修复后重新验证。
```

**07-final-checklist.md 改动:** Step 1 增加降级选项:

```markdown
# 1. Step 1:验证

**方式 A:浏览器验证(环境支持时)**

□ 关键交互链路可操作(对照阶段二 2.6 状态链)
□ 控制台无阻断错误
□ 资源加载成功(字体、图标、图片)
□ 响应式表现合理(375px 基准 + 宽屏验证)

**方式 B:静态代码审查(环境不支持浏览器时)**

□ 资源路径在交付目录内可解析(字体、图标、图片文件存在)
□ CSS 中所有颜色、间距、字号、圆角通过 var(--wg-*) 引用
□ JavaScript 中状态转换逻辑完整覆盖阶段二 2.6 状态链
□ HTML 语义结构正确,无内联业务 CSS 和 JavaScript
□ 样式加载顺序正确:tokens.css → iconfont.css → components.css → app.css
```

**理由:** 
- 不降低验证标准,只是提供等价的替代验证方式
- 静态审查能覆盖大部分合规问题
- 两个平台都能执行

### 改动 3:Figma MCP 条件判断

**文件:** `04-ai-rules/08-requirement-confirmation-rules.md`

**改动:** 第 4 节增加降级:

```markdown
# 4. Figma 集成

当用户输入中包含 Figma 链接时:

1. 检查 Figma MCP 是否可用
2. 可用 → 调用 Figma MCP 读取设计稿,提取布局结构、组件层级、交互标注,作为草图型输入处理
3. 不可用 → 提示用户:"Figma MCP 未连接,请提供设计稿截图或文字描述"
4. 没有链接时跳过,不影响流程
```

**理由:** 
- 简单条件判断,不改变流程逻辑
- 需求确认是必要步骤,不能完全跳过

### 改动 4:validate_skill.py 同步更新

**文件:** `scripts/validate_skill.py`

**改动:** 增加对 AGENTS.md 的校验:

```python
def validate_agents_md() -> list[str]:
    errors: list[str] = []
    path = ROOT / "AGENTS.md"
    if not path.is_file():
        errors.append("Missing AGENTS.md (required for Codex compatibility)")
        return errors
    
    content = path.read_text(encoding="utf-8")
    if "SKILL.md" not in content:
        errors.append("AGENTS.md must reference SKILL.md as entry point")
    if "阶段一" not in content or "阶段四" not in content:
        errors.append("AGENTS.md must summarize the 4-phase execution flow")
    if "平台适配" not in content and "降级" not in content:
        errors.append("AGENTS.md must include platform adaptation notes")
    
    # Check line count (should be under 100 lines)
    lines = content.split("\n")
    if len(lines) > 100:
        errors.append(f"AGENTS.md should be under 100 lines (current: {len(lines)})")
    
    return errors
```

并在 `main()` 中加入调用。

**理由:**
- 确保 AGENTS.md 存在且包含关键信息
- 防止 AGENTS.md 过长(违反 Codex 规范)

---

## 不改动的部分

| 文件 | 理由 |
|------|------|
| agents/openai.yaml | 保留给 Trae 使用,不影响 Trae 兼容性 |
| 01~06 规则文件 | 内容平台无关,不需要改动 |
| 03-components/ | 组件契约平台无关 |
| 02-tokens/ | Token 体系平台无关 |
| token-css-map.md | 纯数据映射 |
| 05-examples/ | 示例文件不参与执行 |
| SKILL.md frontmatter | Trae 已经能正确识别,不需要改动 |

---

## 假设与决策

| 决策 | 理由 |
|------|------|
| **新增 AGENTS.md,保留 openai.yaml** | 两个平台使用不同的入口文件,互不影响 |
| **AGENTS.md 指向 SKILL.md** | 保持 SKILL.md 唯一入口原则,避免维护两套规则 |
| **降级策略写在 SKILL.md 和 checklist 中** | 平台适配是执行层面的问题,应该在执行规则中处理 |
| **Figma 降级为提示用户提供截图** | 需求确认是必要步骤,不能完全跳过 |
| **静态审查作为浏览器验证的等价替代** | 覆盖资源路径、CSS 合规性、JS 逻辑完整性 |
| **AGENTS.md 控制在 60 行左右** | 符合 Codex 规范(100 行以内) |

---

## 实施步骤

### Step 1: 创建 AGENTS.md
- 在项目根目录创建 AGENTS.md
- 内容指向 SKILL.md,包含流程摘要、核心约束、平台适配说明
- 控制在 100 行以内

### Step 2: 更新 SKILL.md 阶段四
- 在阶段四"门禁"前增加降级说明
- 明确浏览器验证和静态代码审查两种方式

### Step 3: 更新 07-final-checklist.md
- Step 1 拆分为方式 A(浏览器验证)和方式 B(静态代码审查)
- 两种方式覆盖相同的验证维度

### Step 4: 更新 08-requirement-confirmation-rules.md
- 第 4 节增加 Figma MCP 不可用时的降级处理

### Step 5: 更新 validate_skill.py
- 新增 validate_agents_md() 函数
- 校验 AGENTS.md 存在性、关键内容、行数限制
- 在 main() 中加入调用

### Step 6: 验证
- 运行 `python scripts/validate_skill.py`,确认所有校验通过
- 检查 AGENTS.md 内容完整性
- 检查 SKILL.md 和 checklist 的降级说明

---

## 验证清单

- [ ] AGENTS.md 存在且控制在 100 行以内
- [ ] AGENTS.md 包含 SKILL.md 引用
- [ ] AGENTS.md 包含 4 阶段流程摘要
- [ ] AGENTS.md 包含核心约束
- [ ] AGENTS.md 包含平台适配说明
- [ ] SKILL.md 阶段四包含降级说明
- [ ] 07-final-checklist.md Step 1 包含方式 A 和方式 B
- [ ] 08-requirement-confirmation-rules.md 第 4 节包含 MCP 不可用处理
- [ ] validate_skill.py 校验通过
- [ ] openai.yaml 保持不变(Trae 兼容性)
