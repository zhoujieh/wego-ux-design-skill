# 微购设计系统 Skill

> 维护者索引，不参与 AI 运行时决策。  
> AI 的任务分类、读取路由、阶段门禁和输出要求以 `SKILL.md` 为唯一依据。

## 当前用途

`wego-ux-design` 当前用于生成和审查微购/WeGo Web UI，主要覆盖：

- 生成完整可交互 Web 原型项目
- 生成单个页面或组件 demo
- 审查现有界面的设计合规性
- 检查 Token 使用是否符合微购设计系统
- 回答微购设计规范相关问题

当前阶段聚焦产品设计与原型验证。运行时消费入口固定从 `design-library/library-consumption.json` 开始。

## 安装

只保留通过 AI 自然语言安装 / 更新的方式，下面的提示词可直接一键复制使用。

### Codex

```text
从 GitHub 仓库 zhoujieh/wego-ux-design-skill 的 wego-ux-design 目录安装或更新本地 Codex skill 到 ~/.codex/skills/wego-ux-design；如果已存在就直接覆盖，不要做备份；如果不能直接覆盖，就先删除已安装目录再重新克隆安装
```

### Claude Code

```text
从 GitHub 仓库 zhoujieh/wego-ux-design-skill 的 wego-ux-design 目录安装或更新本地 Claude Code skill 到 ~/.claude/skills/wego-ux-design；如果已存在就直接覆盖，不要做备份；如果不能直接覆盖，就先删除已安装目录再重新克隆安装
```

### Trae

```text
从 GitHub 仓库 zhoujieh/wego-ux-design-skill 的 wego-ux-design 目录安装或更新本地 Trae skill 到 ~/.trae-cn/skills/wego-ux-design；如果已存在就直接覆盖，不要做备份；如果不能直接覆盖，就先删除已安装目录再重新克隆安装
```

## 设计库概览

当前设计库主要由以下内容构成：

- Token 源与运行时投影：`tokens-source.json`、`tokens.json`、`tokens.css`
- 页面骨架与布局工具：`scaffold.css`、`page-layout.json`
- 组件注册表、组件契约、预览标记和聚合样式
- 页面级模式库：`ui_kits/`
- 图标字体、业务图标、商品媒体、视频和字体资源

截至当前版本：

- 已注册稳定组件：17 个，入口为 `design-library/components/index.json`
- 已收录页面模式：`business-settings`，入口为 `design-library/ui_kits/index.json`
- 已提供 OpenAI Agent 展示配置：`agents/openai.yaml`

## 目录职责

下面按“先找入口，再找细节”的方式整理，方便后续查阅。

### 顶层目录与入口文件

| 路径 | 职责 |
|---|---|
| `SKILL.md` | Skill 唯一运行时入口，定义任务路由、必读文件、阶段门禁和输出边界 |
| `README.md` | 维护者说明和查阅索引，不参与 AI 运行时决策 |
| `install.sh` | 安装、覆盖更新、卸载脚本，兼容 Codex / Claude Code / Trae |
| `agents/openai.yaml` | OpenAI Agent 展示配置，定义名称、简介和默认触发提示 |
| `rules/` | 运行时规则层，细化执行、确认、审查、输出和验收规则 |
| `design-library/` | 设计库主目录，承载 Token、组件契约、页面模式和可复制资源 |
| `scripts/` | 设计库和 Skill 的生成、提取、校验脚本 |

### `rules/` 目录

| 路径 | 职责 |
|---|---|
| `rules/execution.md` | 生成任务的 4 阶段执行闭环，约束何时确认、何时消费设计库、何时验证输出 |
| `rules/confirmation.md` | 生成类任务首轮《需求确认卡》的固定格式与门禁 |
| `rules/checkout.md` | 阶段四验收清单，约束浏览器验证、静态检查与交付门禁 |
| `rules/output.md` | 原型项目输出格式、目录结构和交付说明要求 |
| `rules/review.md` | 界面审查流程、问题优先级和审查输出格式 |
| `rules/components.md` | 组件消费规则补充，约束组件发现、组合和禁止事项 |
| `rules/tokens.md` | Token 使用与合规约束补充，约束变量引用方式和禁用写法 |
| `rules/design-principles.md` | 微购设计原则说明，统一判断基线 |

### `design-library/` 目录

| 路径 | 职责 |
|---|---|
| `design-library/library-consumption.json` | 设计库消费总入口，定义 `recommendedReadOrder`、消费层、复制边界和硬约束 |
| `design-library/page-layout.json` | 页面类型、信息层级、布局模式、固定区和页面转场契约 |
| `design-library/tokens-source.json` | Token 唯一源数据，所有 Token 修改都应从这里开始 |
| `design-library/tokens.json` | 面向运行时消费的 Token 投影结果，由脚本生成 |
| `design-library/tokens.css` | Token CSS 变量和基础重置，供原型项目直接复制 |
| `design-library/scaffold.css` | 页面骨架与 M/G 布局工具类，供原型项目直接复制 |
| `design-library/components.css` | 从 preview 中提取并聚合得到的组件样式文件，供原型项目直接复制 |
| `design-library/components/` | 组件契约目录，保存每个组件的 JSON 契约和组件注册表 |
| `design-library/preview/` | 组件 Canonical preview，内含 `@component-markup-start/end` 和 CSS 提取标记 |
| `design-library/ui_kits/` | 页面模式库，保存页面模式注册表、质量报告和结构参考页 |
| `design-library/assets/` | 设计库资源目录，存放图标字体、业务图标、媒体、视频和字体资源 |

### `design-library/components/`

| 路径 | 职责 |
|---|---|
| `design-library/components/index.json` | 组件注册表，是发现组件的唯一入口 |
| `design-library/components/*.json` | 单个组件契约，定义 `variantDimensions`、`domAnatomy`、`usageHints`、`doNotInvent` 等 |

当前已注册组件包括：`actionsheet`、`button`、`cell`、`checkbox`、`dialog`、`form`、`input`、`link`、`loading`、`navbar`、`radio`、`result`、`stacks`、`switch`、`tabs`、`tag`、`toast`。

### `design-library/preview/`

| 路径 | 职责 |
|---|---|
| `design-library/preview/component-*.html` | 每个组件的标准预览页，提供可复制 markup 和可提取 CSS |

这些文件既是组件结构来源，也是 `components.css` 的样式提取来源。

### `design-library/ui_kits/`

| 路径 | 职责 |
|---|---|
| `design-library/ui_kits/index.json` | 页面模式注册表，按 `appliesTo` 和 `keyFeatures` 匹配页面模式 |
| `design-library/ui_kits/{type}/quality-report.json` | 命中页面模式后的强制布局约束来源 |
| `design-library/ui_kits/{type}/index.html` | 页面结构参考样例，只作结构参考，不直接复制 |

当前已收录页面模式：

- `business-settings`：业务设置页

### `design-library/assets/`

| 路径 | 职责 |
|---|---|
| `design-library/assets/fonts/` | 字体资源目录，含微购字体和 iconfont |
| `design-library/assets/fonts/iconfont/` | 图标字体目录，原型项目使用图标时需要整目录复制 |
| `design-library/assets/icons/app-center/` | 应用中心业务图标 SVG 资源 |
| `design-library/assets/media/index.json` | 商品媒体索引，建立“品类 -> 产品 ID -> 标题”的映射 |
| `design-library/assets/media/` | 商品图片等业务媒体资源 |
| `design-library/assets/video/` | 非产品类视频资源，例如宣传或演示视频 |

### `scripts/` 目录

| 路径 | 职责 |
|---|---|
| `scripts/generate_tokens.py` | 从 `tokens-source.json` 生成 `tokens.json` 和 `tokens.css` |
| `scripts/token_utils.py` | Token 生成与校验共享工具函数 |
| `scripts/extract_components_css.py` | 从 `preview/component-*.html` 提取组件 CSS 并聚合生成 `components.css` |
| `scripts/validate_tokens.py` | 校验 Token 源数据、生成物、引用关系和硬编码设计值 |
| `scripts/validate_components.py` | 校验组件注册表、组件契约、preview 标记和组件 CSS 规则 |
| `scripts/validate_library.py` | 校验设计库整体完整性，包括 ui_kits、资源目录和组件映射 |
| `scripts/validate_skill.py` | 校验 Skill 路由、所需文件和阶段门禁相关约束 |

## 常用维护命令

### 设计库校验

```bash
cd wego-ux-design
python3 scripts/validate_tokens.py
python3 scripts/validate_components.py
python3 scripts/validate_library.py
python3 scripts/validate_skill.py
```

### Token / 组件样式生成

```bash
cd wego-ux-design
python3 scripts/generate_tokens.py
python3 scripts/extract_components_css.py
```

## 维护原则

- 不在 `README.md` 中定义运行时读取顺序、冲突优先级或输出格式。
- 修改运行时行为时，只在 `SKILL.md` 维护任务路由和阶段边界，再同步被引用规则。
- 生成页面或组件时，必须先从 `design-library/library-consumption.json` 开始消费设计库。
- 修改 Token 时，只编辑 `design-library/tokens-source.json`，再运行生成与校验脚本。
- 组件发现以 `design-library/components/index.json` 为唯一入口，不扫描整个组件目录。
- `preview/` 是组件结构和组件 CSS 的事实来源，修改组件时要同步考虑 preview 与聚合样式。
- `ui_kits/` 只提供页面模式参考和质量约束，不直接作为可复制源码。
- README 只做维护索引，不能替代 `SKILL.md` 的权威边界。
