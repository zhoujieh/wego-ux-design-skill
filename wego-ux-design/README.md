# 微购设计系统 Skill

> 维护者索引，不参与 AI 运行时决策。  
> AI 的任务分类、读取路由、阶段边界和输出要求以 `SKILL.md` 为唯一依据。

## 安装

### 一键终端安装

```bash
# 克隆仓库并安装到所有检测到的 AI 编码平台
git clone https://github.com/zhoujieh/wego-ux-design-skill.git /tmp/wego-ux-design-skill && \
  bash /tmp/wego-ux-design-skill/wego-ux-design/install.sh --all && \
  rm -rf /tmp/wego-ux-design-skill
```

或直接从 GitHub 下载（无 git 依赖）：

```bash
curl -fsSL https://raw.githubusercontent.com/zhoujieh/wego-ux-design-skill/main/wego-ux-design/install.sh | bash
```

**安装位置：**

| 平台 | 安装位置 | 方式 |
|------|---------|------|
| Codex | `~/.codex/skills/wego-ux-design/` | Skill（自动识别） |
| Claude Code | `~/.claude/skills/wego-ux-design/` | Skill |
| Trae | `~/.trae-cn/skills/wego-ux-design/` | Skill |

### 安装选项

| 命令 | 说明 |
|------|------|
| `bash install.sh` | 安装到所有检测到的平台 |
| `bash install.sh --codex` | 仅安装到 Codex |
| `bash install.sh --claude` | 仅安装到 Claude Code |
| `bash install.sh --trae` | 仅安装到 Trae |
| `bash install.sh --update` | 删除目标目录后覆盖更新已安装的 skill |
| `bash install.sh --codex --update` | 覆盖更新 Codex skill |
| `bash install.sh --uninstall` | 卸载所有平台（含旧位置清理） |

### 更新 Skill

更新策略固定为二选一：直接 `--update` 覆盖，或先 `--uninstall` 再重装；不需要、也不建议先做本地备份。

```bash
git clone https://github.com/zhoujieh/wego-ux-design-skill.git /tmp/wego-ux-design-skill && \
  bash /tmp/wego-ux-design-skill/wego-ux-design/install.sh --all --update && \
  rm -rf /tmp/wego-ux-design-skill
```

或一行：

```bash
curl -fsSL https://raw.githubusercontent.com/zhoujieh/wego-ux-design-skill/main/wego-ux-design/install.sh | bash -s -- --update
```

### 通过 AI 自然语言安装

将以下提示词复制发送给对应的 AI 编码工具即可自动安装。

**Codex：**

```
从 GitHub 仓库 zhoujieh/wego-ux-design-skill 路径 wego-ux-design 更新本地 skill；如果已存在就直接覆盖，不要做备份；如不能覆盖，就先删除已安装目录再重新克隆安装
```

**Claude Code：**

```
从 GitHub 仓库 zhoujieh/wego-ux-design-skill 的 wego-ux-design 目录更新本地 ~/.claude/skills/ 下的 skill；如果已存在就直接覆盖，不要做备份；如不能覆盖，就先删除已安装目录再重新克隆安装
```

**Trae：**

```
从 GitHub 仓库 zhoujieh/wego-ux-design-skill 路径 wego-ux-design 更新 ~/.trae-cn/skills/ 下的 skill；如果已存在就直接覆盖，不要做备份；如不能覆盖，就先删除已安装目录再重新克隆安装
```

### 安装后

**务必完全退出并重启**对应的 AI 编码工具，然后在任意项目中用自然语言触发：

> 「帮我设计一个微购的商品列表页」  
> 「生成一个微购风格的登录页面」  
> 「审查这个页面的设计合规性」

---

## 当前用途

该 Skill 面向产品设计阶段，用于生成完整可交互 Web 原型项目、审查界面和检查 Token 合规性。

当前阶段不生成 KuiklyUI 代码。运行时组件契约位于 `design-library/components/`，由 `SKILL.md` 先读取 `design-library/library-consumption.json` 再按推荐顺序消费。

## 目录职责

| 路径 | 作用 |
|---|---|
| `SKILL.md` | 唯一运行时入口和任务路由 |
| `install.sh` | 一键安装/更新/卸载脚本 |
| `principles/` | 微购设计判断原则 |
| `rules/` | 运行时控制层规则（execution / generation / tokens / components / review / output / checkout / confirmation） |
| `design-library/tokens-source.json` | 唯一 Token 数据源 |
| `design-library/token-reference.md` | 自动生成的 Token 名称、值和 CSS 映射参考 |
| `design-library/token-css-map.md` | 从 `tokens.json` 自动生成的 CSS 变量 |
| `scripts/generate_tokens.py` | 生成 Token 参考文档、CSS 映射和项目 Token 样式 |
| `scripts/validate_tokens.py` | 校验引用、映射、漂移和示例硬编码 |
| `scripts/validate_skill.py` | 校验任务路由、交互项目契约和旧约束回归 |
| `design-library/` | 设计库消费产物（tokens / scaffold / components / preview / assets / library-consumption） |
| `examples/` | 非规范示例，仅供人工参考或显式调用 |

## 质量验证

### Token 校验
```bash
cd wego-ux-design
python scripts/validate_tokens.py
```
校验 Token 引用、映射、漂移和示例硬编码。

### Skill 路由校验
```bash
python scripts/validate_skill.py
```
校验任务路由、交互项目契约和旧约束回归。

## 维护原则

- 不在 README 中定义 AI 读取顺序、冲突优先级或输出格式。
- 不在详细规则中新增独立任务路由。
- 修改运行时行为时，只在 `SKILL.md` 中维护路由，再同步调整被引用规则的内容。
- 新增资料时明确其阶段和用途，避免产品设计资料与开发实现资料混用。
- 修改 Token 时只编辑 `design-library/tokens-source.json`，随后运行生成和校验脚本。
- 组件发现以 `design-library/components/index.json` 为唯一入口，不再维护旧组件注册表。
- 规则入口统一在 `rules/`，示例统一在 `examples/`，原则统一在 `principles/`。
