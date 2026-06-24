# 微购 Design Token 架构

## 唯一数据源

`tokens.json` 是 Token 名称、值、类型、引用关系和分类的唯一事实源。

以下文件均为派生产物：

- `token-reference.md`
- `tokens.css`
- `../token-css-map.md`

派生文件包含生成标记，禁止手工修改。任何 Token 变更必须先修改 `tokens.json`。

## 文件职责

| 文件 | 职责 |
|---|---|
| `tokens.json` | 机器可读的 Token 定义 |
| `tokens.schema.json` | 数据结构约束 |
| `token-reference.md` | 供设计说明和规范查询使用的完整参考 |
| `tokens.css` | 复制到原型项目 `styles/tokens.css` 的 CSS 变量文件 |
| `token-usage-guidelines.md` | 不包含具体值的人工使用规则 |
| `../token-css-map.md` | Web 原型使用的 CSS 自定义属性映射参考 |
| `../scripts/generate_tokens.py` | 生成三个派生产物 |
| `../scripts/validate_tokens.py` | 校验定义、引用、生成漂移和示例 |

## 分层

使用优先级：

```text
Semantic Token
↓
Pattern Token
↓
Base Token
```

优先使用表达意图的语义 Token。只有语义层无法表达时才使用基础 Token。

## 引用格式

`tokens.json` 中引用其他 Token 时使用：

```json
{
  "value": "{wg.color.base.brand.500}"
}
```

生成器会将该引用转换为对应的 CSS `var(...)`。

## 变更流程

1. 修改 `tokens.json`。
2. 运行 `python3 scripts/generate_tokens.py`。
3. 运行 `python3 scripts/validate_tokens.py`。
4. 生成或校验失败时不得交付。

## 扩展规则

- 新 Token 至少服务三个可复用场景。
- 不为单页面或单个临时变体创建 Token。
- 优先新增语义 Token，最后才新增基础 Token。
- 不直接修改生成后的 CSS 名称。
- Token 引用必须存在且不得形成循环。
