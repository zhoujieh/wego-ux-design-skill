# 04 Token Usage Rules

> 微购 Design System Skill / 04-ai-rules

## 权威来源

- Token 定义：`02-tokens/tokens.json`
- 可读参考：`02-tokens/token-reference.md`
- CSS 映射：`token-css-map.md`
- 使用原则：`02-tokens/token-usage-guidelines.md`

`token-reference.md` 和 `token-css-map.md` 是生成文件，不能作为编辑入口。

## 合规检查

检查界面或代码时必须确认：

- 使用的 `wg.*` 名称存在于 Token Reference。
- 使用的 `var(--wg-*)` 存在于 CSS 映射。
- Token 定义层可以保存原始值；业务样式不存在硬编码颜色、字号、间距、圆角、尺寸、阴影、动效或 z-index。
- Semantic Token 可以表达时，没有退回 Base Token。
- Copywriting Token 没有被错误当作 CSS 变量。
- 缺失 Token 没有通过临时值绕过。

## 缺失处理

```text
当前使用：
原因：
建议新增：
归属位置：02-tokens/tokens.json
```

## 禁止事项

- 为单页面或单个临时变体新增 Token。
- 手工修改 `token-reference.md` 或 `token-css-map.md`。
- 使用未定义的 `wg.*` 或 `--wg-*`。
- 用魔法数字绕过 Token。
- 把组件结构写进 Token。
