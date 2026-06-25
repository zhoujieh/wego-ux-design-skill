# 完善回归测试体系计划

## 概要
对 3 个文件进行定向更新，使回归测试同时承担"工程合规回归"和"页面设计质量 benchmark"。

---

## 修改清单

### 1. 更新 `tests/golden-prompts/product-publish-page.md`

保留现有全部内容，在末尾追加 4 个新章节：

- **信息层级要求** — 明确商品发布页的视觉层级规则（标题 > 表单分组 > 字段 > 辅助文字）
- **布局节奏要求** — 明确间距节奏（分组间距 G2、字段间距 G1、页面边距 M0-M2）
- **常见失败** — 列出历史回归中高频出现的设计问题（如层级扁平化、间距不一致、状态遗漏等）
- **设计评分** — 100 分制，6 维度：
  - 目标清晰度 20
  - 信息层级 20
  - 布局节奏 20
  - 组件正确性 15
  - 状态完整性 15
  - 微购风格 10

### 2. 更新 `scripts/validate_generated_projects.py`

- 导入 `argparse`，解析命令行参数
- 新增 `--require-fixtures` 可选参数
- **默认行为不变**：无 fixture 目录或目录为空时返回 0（通过）
- **启用 `--require-fixtures` 时**：fixture 目录不存在或为空则返回 1（失败），并输出明确错误信息
- 现有校验逻辑完全不变

### 3. 更新 `.github/workflows/validate.yml`

- Validate generated projects 步骤的命令改为：
  ```
  python scripts/validate_generated_projects.py --require-fixtures
  ```
- 其余步骤不变

---

## 不做的事

- 不修改 Token 定义或生成脚本
- 不修改组件契约
- 不修改 SKILL.md 任务路由
- 不新增 06-benchmarks 目录
- 不修改其他 golden-prompts 文件

---

## 验证步骤

1. `python scripts/validate_generated_projects.py` — 无 fixture 时仍通过（返回 0）
2. `python scripts/validate_generated_projects.py --require-fixtures` — 无 fixture 时失败（返回 1）
3. `python scripts/validate_generated_projects.py --require-fixtures` — 有 fixture 时正常校验
4. 检查 `product-publish-page.md` 新增章节格式与现有内容一致
