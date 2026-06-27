# Wego Design System

微购 (WeGo) 设计系统的文档网站、Codex Skill 和回归测试仓库。

## 常用命令

**文档网站 (website/):**

```bash
cd website && npm run dev      # 启动 Vite 开发服务器 (port 3000)
npm run build                   # 生产构建
```

**Skill 校验:**

```bash
python3 wego-ux-design/scripts/validate_components.py
python3 wego-ux-design/scripts/validate_library.py
```

**回归测试:**

```bash
python3 scripts/validate_generated_projects.py
python3 scripts/validate_generated_projects.py --require-fixtures
python3 -m unittest tests/test_phase7_acceptance.py
```

**Fixture 生成与刷新:**

```bash
python3 scripts/generate_phase7_fixtures.py
```

## 项目结构

```text
wego-design-system/
├── website/                  # 微购设计系统文档网站 (Vite + vanilla HTML/CSS/JS)
│   ├── index.html
│   ├── styles/               # tokens.css, components.css, app.css
│   ├── scripts/app.js        # 客户端路由与页面渲染
│   └── assets/               # 字体、图标等静态资源
├── wego-ux-design/           # Codex / Claude Code / Trae Skill
│   ├── SKILL.md              # Skill 运行时控制入口
│   ├── design-library/       # 设计库 (组件契约、Token、预览)
│   ├── rules/                # Skill 执行规则
│   ├── principles/           # 设计原则
│   └── scripts/              # Skill 内置校验脚本
├── tests/                    # 回归测试体系
│   ├── golden-prompts/       # 标准测试用例 (输入提示词 + 验收清单)
│   └── fixtures/generated/   # AI 生成结果样本
└── scripts/                  # 项目级脚本
    ├── validate_generated_projects.py
    └── generate_phase7_fixtures.py
```

## 关键约束

- **Skill 权威边界**: `wego-ux-design/SKILL.md` 是 Skill 唯一的运行时控制入口。不要绕过它直接修改或扩展 Skill 行为。
- **设计库消费**: 生成页面或组件时，必须先读取 `wego-ux-design/design-library/library-consumption.json`，按 `recommendedReadOrder` 引导加载后续文件。
- **测试 fixture 管理**: 新增 golden prompt 用例后，需手动生成对应的 fixture 并放入 `tests/fixtures/generated/`，然后运行校验脚本确认通过。
- **设计原则优先级**: 清晰 > 一致 > 效率 > 美观 > 创新。微购风格：简洁 · 干净 · 淡雅 · 克制 · 高信息密度 · 微信生态一致。
- **Skill 安装**: Skill 通过 `wego-ux-design/install.sh` 安装到 Codex、Claude Code 或 Trae。`.claude/` 目录已预配置该 Skill。
