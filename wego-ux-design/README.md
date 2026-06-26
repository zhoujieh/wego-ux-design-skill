# 微购设计系统 Skill

> 维护者索引，不参与 AI 运行时决策。  
> AI 的任务分类、读取路由、阶段边界和输出要求以 `SKILL.md` 为唯一依据。

## 当前用途

该 Skill 面向产品设计阶段，用于生成完整可交互 Web 原型项目、审查界面和检查 Token 合规性。

当前阶段不生成 KuiklyUI 代码。运行时组件契约位于 `design-library/components/`，由 `SKILL.md` 先读取 `design-library/library-consumption.json` 再按推荐顺序消费。

## 目录职责

| 路径 | 作用 |
|---|---|
| `SKILL.md` | 唯一运行时入口和任务路由 |
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
| `resources/` | 字体、图片等原型资源 |

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

### 生成项目回归校验
```bash
# 在项目根目录运行
python scripts/validate_generated_projects.py
```
校验 `tests/fixtures/generated/` 中的生成项目：
- 项目结构完整性
- HTML/CSS/JS 分离
- CSS 无硬编码设计值
- JS 包含真实交互逻辑
- Token 文件与源文件一致

### CI 入口
GitHub Actions 在 push 到 main 和 pull_request 时自动运行所有校验：
- `.github/workflows/validate.yml`

## 维护原则

- 不在 README 中定义 AI 读取顺序、冲突优先级或输出格式。
- 不在详细规则中新增独立任务路由。
- 修改运行时行为时，只在 `SKILL.md` 中维护路由，再同步调整被引用规则的内容。
- 新增资料时明确其阶段和用途，避免产品设计资料与开发实现资料混用。
- 修改 Token 时只编辑 `design-library/tokens-source.json`，随后运行生成和校验脚本。
- 组件发现以 `design-library/components/index.json` 为唯一入口，不再维护旧组件注册表。
- 规则入口统一在 `rules/`，示例统一在 `examples/`，原则统一在 `principles/`。
