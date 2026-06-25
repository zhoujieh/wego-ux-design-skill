# Dialog

Dialog 居中弹出的模态对话框，用于确认关键操作、提示重要信息或展示带自定义内容的说明。本规则首先判断内容变体和按钮组合，再映射视觉样式。

## 目录

- [使用决策](#使用决策)
- [语义模型](#语义模型)
- [允许组合](#允许组合)
- [Anatomy](#anatomy)
- [文案规则](#文案规则)
- [Canonical HTML](#canonical-html)
- [Canonical CSS](#canonical-css)
- [状态](#状态)
- [可访问性](#可访问性)
- [生成约束](#生成约束)
- [自检](#自检)
- [规范来源](#规范来源)

## 使用决策

使用 Dialog：

- 需要用户确认或决策的关键操作，如删除、扣费、发布。
- 向用户强调操作结果，如成功、失败、余额不足。
- 需要用户阅读的简短说明或提示信息。
- 需要在弹窗内展示一个额外操作构件（如输入框），且该构件与确认流程直接相关。

不使用 Dialog：

- 页面内轻量反馈：使用 Toast。
- 底部多选项列表：使用 ActionSheet。
- 底部半屏内容面板：使用 ModalFrame。
- 顶部消息推送：使用 Push。
- 非模态信息展示：使用页面内 Alert 或 Banner。

## 语义模型

Dialog 有三个决策维度：

```text
variant   内容变体
buttons   按钮组合
state     当前交互状态
```

### Variant

| Variant | 含义 | 结构 | 应用场景 |
|---|---|---|---|
| `text` | 标题 + 正文 | 标题 + 多行正文 + 按钮行 | 描述 1 个以上信息；介绍说明。如「二次确认 + 影响」「现状 + 解决办法」「设置结果 + 影响」 |
| `title` | 仅标题 | 标题 + 按钮行 | 仅描述 1 个信息。如一般疑问句、一组「主语 + 谓语 + 宾语」 |
| `status` | 状态图标 + 标题 + 正文 | 图标 + 标题 + 正文 + 按钮行 | 强调结果。如退款失败、操作成功 |
| `custom` | 标题 + 正文 + 自定义区 | 标题 + 正文 + 自定义区 + 按钮行 | 有额外元素或操作。仅支持 1 个操作构件如输入框 |

禁止让 AI 直接根据"有图标/无图标"选择变体。必须先判断内容目的。

### Buttons

| Buttons | 含义 | 规则 |
|---|---|---|
| `dual` | 双按钮：取消 + 确认 | 两个操作必须是一正一反的关系，要么更进一步，要么放弃 |
| `single` | 单按钮：确认/知道了 | 等效于关闭弹窗，用于纯信息告知 |

双按钮时，确认按钮可使用危险色（`--danger` 修饰符）：风险性不可逆操作，主要操作用红色以示警告。

### State

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `open` | `data-state="open"` | 弹窗可见，遮罩层显示，背景不可交互 |
| `closed` | `data-state="closed"` | 弹窗隐藏，遮罩层隐藏 |

## 允许组合

| Variant | single | dual |
|---|---|---|
| `text` | 允许 | 允许 |
| `title` | 允许 | 允许 |
| `status` | 允许 | 允许 |
| `custom` | 允许 | 允许 |

附加规则：

- 同一 Dialog 内只允许一个自定义区。
- 自定义区内只允许 1 个操作构件（如输入框），不得包含额外的按钮或操作入口。
- 操作统一由按钮行承载，自定义区不得替代按钮行。
- `dual` 双按钮时，确认按钮位于右侧，取消按钮位于左侧。
- `dual` 双按钮的确认按钮可附加 `--danger` 修饰符，取消按钮不得使用 `--danger`。

## Anatomy

通用结构：

```text
div.wg-dialog-overlay[data-state]
└── div.wg-dialog.wg-dialog--{variant}[role="dialog"][aria-modal="true"]
    ├── div.wg-dialog__content
    │   ├── div.wg-dialog__header
    │   │   ├── i.wg-dialog__icon.wg-dialog__icon--{status}（仅 status 变体）
    │   │   └── h2.wg-dialog__title
    │   ├── p.wg-dialog__description（text / status / custom 变体）
    │   └── div.wg-dialog__custom（仅 custom 变体）
    └── div.wg-dialog__action
        └── div.wg-dialog__buttons.wg-dialog__buttons--{single|dual}
            ├── button.wg-dialog__button.wg-dialog__button--dismiss（dual 时）
            └── button.wg-dialog__button.wg-dialog__button--confirm[--danger]
```

各变体差异：

- `text`：有 `h2.wg-dialog__title` + `p.wg-dialog__description`，无 `i.wg-dialog__icon`，无 `div.wg-dialog__custom`
- `title`：仅有 `h2.wg-dialog__title`，无 `p.wg-dialog__description`，无 `i.wg-dialog__icon`，无 `div.wg-dialog__custom`
- `status`：有 `i.wg-dialog__icon` + `h2.wg-dialog__title` + `p.wg-dialog__description`，无 `div.wg-dialog__custom`
- `custom`：有 `h2.wg-dialog__title` + `p.wg-dialog__description` + `div.wg-dialog__custom`，无 `i.wg-dialog__icon`

自定义区规则：

- `div.wg-dialog__custom` 是可选插槽，位于正文之后、按钮行之前。
- 自定义区内容不使用 `.wg-dialog` 命名空间内的子元素 class，由页面级样式控制。
- 自定义区仍须使用 wego Token，满足语义和可访问性要求。
- 典型场景：费用展示卡片、输入框、预览图、详情列表等。
- 自定义区不得包含额外的按钮或操作入口，操作统一由 footer 按钮行承载。

## 文案规则

- 标题使用简短明确的短语，如"确认删除""操作成功""退款失败"。
- `title` 变体的标题严格控制在 1 行，不可太长。
- 正文使用完整句子说明情况，如"删除后无法恢复，请谨慎操作"。
- 正文单行展示，不换行；超长时截断显示省略号。
- 取消按钮使用"取消"；确认按钮使用能说明结果的动词，如"删除""确认扣费""知道了"。
- 确认按钮文案不超过 5 个字符。
- 同一 Dialog 内标题和正文使用一致的语气。
- 危险操作必须写明对象和后果；确认按钮使用 `--danger` 修饰符。
- 标题限制最大 2 行，超出截断。
- 描述限制最大 3 行或具备滚动策略；超长内容必须进入内容滚动区。
- 按钮区不得被长内容挤压。

## Canonical HTML

`text` 变体 — 双按钮：

```html
<div class="wg-dialog-overlay" data-state="open">
  <div class="wg-dialog wg-dialog--text" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
    <div class="wg-dialog__content">
      <div class="wg-dialog__header">
        <h2 class="wg-dialog__title" id="dialog-title">确认删除</h2>
      </div>
      <p class="wg-dialog__description">删除后无法恢复，请谨慎操作</p>
    </div>
    <div class="wg-dialog__action">
      <div class="wg-dialog__buttons wg-dialog__buttons--dual">
        <button class="wg-dialog__button wg-dialog__button--dismiss" type="button">取消</button>
        <button class="wg-dialog__button wg-dialog__button--confirm wg-dialog__button--danger" type="button">删除</button>
      </div>
    </div>
  </div>
</div>
```

`title` 变体 — 双按钮：

```html
<div class="wg-dialog-overlay" data-state="open">
  <div class="wg-dialog wg-dialog--title" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
    <div class="wg-dialog__content">
      <div class="wg-dialog__header">
        <h2 class="wg-dialog__title" id="dialog-title">开启手动跟图</h2>
      </div>
    </div>
    <div class="wg-dialog__action">
      <div class="wg-dialog__buttons wg-dialog__buttons--dual">
        <button class="wg-dialog__button wg-dialog__button--dismiss" type="button">取消</button>
        <button class="wg-dialog__button wg-dialog__button--confirm" type="button">确认</button>
      </div>
    </div>
  </div>
</div>
```

`status` 变体 — 单按钮（成功）：

```html
<div class="wg-dialog-overlay" data-state="open">
  <div class="wg-dialog wg-dialog--status" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
    <div class="wg-dialog__content">
      <div class="wg-dialog__header">
        <i class="wg-dialog__icon wg-dialog__icon--success"></i>
        <h2 class="wg-dialog__title" id="dialog-title">操作成功</h2>
      </div>
      <p class="wg-dialog__description">可前往个人相册查看</p>
    </div>
    <div class="wg-dialog__action">
      <div class="wg-dialog__buttons wg-dialog__buttons--single">
        <button class="wg-dialog__button wg-dialog__button--confirm" type="button">知道了</button>
      </div>
    </div>
  </div>
</div>
```

`status` 变体 — 单按钮（失败）：

```html
<div class="wg-dialog-overlay" data-state="open">
  <div class="wg-dialog wg-dialog--status" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
    <div class="wg-dialog__content">
      <div class="wg-dialog__header">
        <i class="wg-dialog__icon wg-dialog__icon--danger"></i>
        <h2 class="wg-dialog__title" id="dialog-title">退款失败</h2>
      </div>
      <p class="wg-dialog__description">账户余额不足，请先充值</p>
    </div>
    <div class="wg-dialog__action">
      <div class="wg-dialog__buttons wg-dialog__buttons--single">
        <button class="wg-dialog__button wg-dialog__button--confirm" type="button">知道了</button>
      </div>
    </div>
  </div>
</div>
```

`custom` 变体 — 双按钮：

```html
<div class="wg-dialog-overlay" data-state="open">
  <div class="wg-dialog wg-dialog--custom" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
    <div class="wg-dialog__content">
      <div class="wg-dialog__header">
        <h2 class="wg-dialog__title" id="dialog-title">快捷新建标签</h2>
      </div>
      <p class="wg-dialog__description">请输入标签名称</p>
      <div class="wg-dialog__custom">
        <!-- 页面级自定义内容，使用 wego Token -->
        <div class="custom-input-area">
          <input type="text" placeholder="请输入标签名" />
        </div>
      </div>
    </div>
    <div class="wg-dialog__action">
      <div class="wg-dialog__buttons wg-dialog__buttons--dual">
        <button class="wg-dialog__button wg-dialog__button--dismiss" type="button">取消</button>
        <button class="wg-dialog__button wg-dialog__button--confirm" type="button">创建</button>
      </div>
    </div>
  </div>
</div>
```

## Canonical CSS

```css
/* ── Overlay ── */
.wg-dialog-overlay {
  position: fixed;
  inset: 0;
  z-index: var(--wg-zindex-modal);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--wg-color-overlay-modal);
  transition:
    opacity var(--wg-motion-duration-normal) var(--wg-motion-ease-standard);
}

.wg-dialog-overlay[data-state="closed"] {
  opacity: 0;
  pointer-events: none;
}

/* ── Dialog Card ── */
.wg-dialog {
  inline-size: min(300px, 90vw);
  max-block-size: 80vh;
  display: flex;
  flex-direction: column;
  background-color: var(--wg-color-bg-surface);
  border-radius: var(--wg-radius-xl);
  box-shadow: var(--wg-shadow-xl);
  overflow: hidden;
  transform: scale(1);
  transition:
    transform var(--wg-motion-duration-normal) var(--wg-motion-ease-emphasized),
    opacity var(--wg-motion-duration-normal) var(--wg-motion-ease-standard);
}

.wg-dialog-overlay[data-state="closed"] .wg-dialog {
  transform: scale(0.95);
  opacity: 0;
}

/* ── Content Area ── */
.wg-dialog__content {
  padding: var(--wg-spacing-24) var(--wg-spacing-20);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

/* ── Header (Title Row) ── */
.wg-dialog__header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--wg-spacing-4);
}

.wg-dialog__title {
  font-size: var(--wg-font-size-18);
  line-height: var(--wg-font-lineheight-18);
  font-weight: var(--wg-font-weight-medium);
  color: var(--wg-color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 100%;
}

/* ── Status Icon ── */
.wg-dialog__icon {
  display: inline-block;
  inline-size: var(--wg-size-24);
  block-size: var(--wg-size-24);
  flex-shrink: 0;
  border-radius: var(--wg-radius-full);
}

.wg-dialog__icon--success {
  background-color: var(--wg-color-status-success-default);
}

.wg-dialog__icon--danger {
  background-color: var(--wg-color-status-danger-default);
}

.wg-dialog__icon--warning {
  background-color: var(--wg-color-status-warning-default);
}

/* ── Description ── */
.wg-dialog__description {
  margin-block-start: var(--wg-spacing-12);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 100%;
}

/* ── Custom Slot ── */
.wg-dialog__custom {
  margin-block-start: var(--wg-spacing-12);
  inline-size: 100%;
}

/* ── Action Area ── */
.wg-dialog__action {
  border-block-start: var(--wg-stroke-width-hairline) var(--wg-stroke-style-solid) var(--wg-color-divider-default);
}

/* ── Buttons ── */
.wg-dialog__buttons {
  display: flex;
  align-items: center;
  justify-content: center;
}

.wg-dialog__buttons--dual {
  gap: var(--wg-spacing-16);
}

.wg-dialog__buttons--single {
  justify-content: center;
}

.wg-dialog__button {
  appearance: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  block-size: var(--wg-size-48);
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  cursor: pointer;
  font-family: var(--wg-font-family-text);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
  transition:
    opacity var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-dialog__buttons--dual .wg-dialog__button {
  flex: 1 1 0;
  min-inline-size: 0;
}

.wg-dialog__buttons--single .wg-dialog__button {
  inline-size: 100%;
}

.wg-dialog__button--dismiss {
  color: var(--wg-color-text-primary);
}

.wg-dialog__button--confirm {
  color: var(--wg-color-action-primary-default);
}

.wg-dialog__button--confirm.wg-dialog__button--danger {
  color: var(--wg-color-action-danger-default);
}

.wg-dialog__button:not(:disabled):active {
  opacity: 0.6;
}

.wg-dialog__button:focus-visible {
  outline: none;
}

.wg-dialog__button:focus-visible {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: calc(-1 * var(--wg-spacing-2));
}

.wg-dialog__button:disabled {
  cursor: not-allowed;
  color: var(--wg-color-text-disabled);
}
```

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `open` | `data-state="open"` | 弹窗可见，遮罩层显示，背景不可交互 |
| `closed` | `data-state="closed"` | 弹窗隐藏，遮罩层隐藏，动画退出 |
| `pressed` | `:active`（按钮） | 按下时透明度 0.6，不位移、不缩放 |
| `focus-visible` | `:focus-visible`（按钮） | 必须显示清晰焦点描边 |
| `disabled` | `disabled`（按钮） | 统一使用禁用文字色，不响应操作 |

V1 未定义 `loading`、`scrolling` 视觉变体。正文超长时截断显示省略号，不得自行添加滚动区域；标注组件能力缺失。

Dialog 按钮状态完整性要求：

- `default`：正常可用
- `hover`：仅桌面原型预览
- `active / pressed`：按下时透明度 0.6，必须可见
- `disabled`：统一使用禁用文字色，不响应操作
- `loading`：V1 未定义视觉变体，但提交类操作必须防止重复提交——通过 `disabled` + `aria-busy="true"` 实现

destructive 操作必须有明确视觉区分（使用 `--danger` 修饰符）。

Dialog 内容结构要求：

- 标题：说明问题或动作
- 描述：解释原因
- 限制条件：独立成组，不得混在长段落中
- 操作区：主次明确

Dialog 间距规则：

- title 与 description 之间必须有明确间距（wg.spacing.12）
- description 与限制条件之间必须有明确间距
- 多条限制条件必须用列表或独立块呈现
- 内容与按钮之间必须有明确间距
- 文本不能贴边、拥挤或压缩

## 可访问性

- 必须使用 `role="dialog"` 和 `aria-modal="true"`。
- 必须使用 `aria-labelledby` 指向标题元素。
- 打开时焦点必须移入 Dialog 内第一个可交互元素。
- 关闭时焦点必须返回触发元素。
- 遮罩层打开时，Tab 键不得离开 Dialog（焦点陷阱）。
- 按钮必须使用原生 `<button>`。
- 禁用状态必须使用 `disabled` 属性，不能只降低透明度。
- Escape 键应关闭 Dialog。
- 禁止使用 `div`、`span` 模拟可点击按钮。

## 生成约束

- 必须同时声明一个 `variant` class 和一个 `buttons` class。
- 必须使用 `wg-dialog__content`、`wg-dialog__action`、`wg-dialog__buttons`。
- 不得覆盖 Dialog 宽度、内边距、圆角和阴影。
- 不得覆盖按钮高度、字号和颜色。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 自定义区内容不得使用 `.wg-dialog` 命名空间内的子元素 class。
- 页面脚本可以控制 Dialog 的打开/关闭状态和按钮回调，但不得绕过组件规定的 Anatomy、状态语义和可访问性约束。
- 完整页面中出现 Dialog 时，必须读取并遵守本文件。
- Dialog 内容必须形成结构（标题 + 描述 + 限制条件 + 操作），不得只是文本和按钮堆叠。
- 限制条件必须独立成组，不得混在长段落中。
- 标题限制最大 2 行，描述限制最大 3 行。
- 按钮区不得被长内容挤压。

## 自检

```text
□ 是否先判断内容目的 → text / title / status / custom
□ 是否只存在一个 variant
□ 是否遵守 single / dual 按钮组合
□ 危险操作确认按钮是否使用 --danger
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 是否使用原生 button 和正确 type
□ 是否设置 role="dialog" 和 aria-modal="true"
□ 是否设置 aria-labelledby 指向标题
□ disabled 是否使用原生属性
□ 是否没有自创 loading、scrollable 变体
□ 自定义区是否没有额外按钮或操作入口
□ Dialog 内容是否形成结构（标题+描述+限制条件+操作）
□ 限制条件是否独立成组
□ 按钮是否覆盖 default / pressed / disabled 状态
□ 标题是否限制最大行数
□ 描述是否限制最大行数或具备滚动策略
□ 按钮区是否未被长内容挤压
□ destructive 操作是否使用 --danger 修饰符
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `8:60797`。提取 Dialog_Text、Dialog_Title、Dialog_Status、Dialog_X 四种内容变体的结构、尺寸、间距和按钮规则。
- Kuikly `Dialog`：参考 showTextDialog 的参数设计（标题图标、双/单按钮、关闭行为、遮罩样式、customContent 插槽机制）；不继承 Kuikly DSL、DialogUtil 管理方式、contentLink 拼接机制、DialogTextColor 枚举、conflicting 单例逻辑。
