# Form

Form 用于表单中需要提交保存的数据录入。本规则首先判断表单行的布局模式（水平/垂直），再选择操作区类型（文本输入/数字输入/金额输入/手机号输入/选择/自定义），最后确定右侧按钮和交互状态。

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

使用 Form：

- 需要用户填写并提交保存的数据录入场景，如绑定银行卡、编辑供应商信息、修改结算账号等。
- 表单中包含文本输入、数字输入、金额输入、手机号输入等操作区。
- 表单中包含选择类操作（如选择银行卡类型），选择后仍需提交保存。
- 需要输入校验和错误提示的场景。
- 需要统一取值和批量校验的表单容器。

不使用 Form：

- 即时生效的开关项：使用 Cell 的 switch 操作区。
- 纯导航跳转列表：使用 Cell 的 jump 操作区。
- 只读展示信息：使用 Cell 的 text 操作区或纯文本布局。
- 搜索框输入：使用 NavBar 的 search 模式。
- 长文本富文本编辑：使用独立的 TextArea 或富文本编辑器。

Form 与 Cell 的区别：

- Form 是为了提交保存而存在，所有操作最终都需要用户确认提交。
- Cell 用于导航与查看信息，看到啥事实就是啥，没有保存的概念。
- Form 里也有跳转的分支（如选择银行卡），样式与 Cell 几乎一致，但前者是因为设置项比较复杂，需要跳转或拉起弹窗进行设置，其本身仍然需要提交保存。
- Switch 开关有即时生效的属性，所以开关本身不依赖于保存提交，故属于 Cell 的一类用法。在 Form 中，开关可用于控制设置项的显示与否，但不能用于设置值。

### Form Group 一致性规则

同一个 form group 内必须保持统一视觉规则：

- label 对齐方式统一
- value 对齐方式统一
- action 对齐方式统一
- 错误提示位置统一
- 辅助说明位置统一
- 行高、padding、分隔线规则统一

如果同一组内同时包含输入、选择、开关、跳转、数值字段：

- 必须先确定该组的主交互模式
- 再统一所有行的 action 对齐
- 禁止逐字段单独决定对齐方式

判断原则：

- 表单组是一个视觉单元，不是一堆 cell 的集合
- 同组内字段复杂度不同，也必须保持统一秩序
- 同一个 form group 内禁止左对齐和右对齐混用

### 表单不是 Cell 堆叠

- 表单字段必须按业务含义分组
- Form Group 是视觉单元，不是 cell 列表
- 复杂表单必须有分组节奏和留白
- 不允许把所有字段连续堆叠成一组

Form 与 Input 的区别：

- Form 是表单行组件，包含标签 + 操作区 + 可选右侧按钮，是一个完整的表单行。
- Input 是纯输入框组件，只负责文本输入，不包含标签和右侧按钮。
- Form 的操作区内部使用 Input 作为底层输入控件。

## 语义模型

Form 有五个决策维度：

```text
layout      布局模式（水平/垂直）
action      操作区类型
rightButton 右侧按钮类型
state       当前交互状态
error       是否处于错误状态
```

### Layout

| Layout | 应用场景 | 视觉规则 |
|---|---|---|
| `horizontal` | 标签在左、操作区在右的水平排列 | 标签区固定宽度 96px，操作区自适应剩余宽度 |
| `vertical` | 标签在上、操作区在下的垂直排列 | 标签区占满宽度，操作区占满宽度 |

布局选择规则：

- 默认使用 `horizontal` 水平布局，适用于大多数表单场景（姓名、金额、选择等）。
- 多行文本输入（备注、描述等）使用 `vertical` 垂直布局。
- 标签文字较长（超过 4 个字）且操作区为文本输入时，优先使用 `horizontal`，标签区宽度可通过 `labelWidth` 覆盖。
- 禁止让 AI 直接根据"标签长短"选择布局。必须先判断操作区类型：多行输入必用 `vertical`，其余默认 `horizontal`。

### Action

| Action | 含义 | 结构 | 应用场景 |
|---|---|---|---|
| `text` | 纯文本输入 | 输入框 + 可选 placeholder | 姓名、地址、备注等文本 |
| `number` | 数字输入 | 输入框 + 数字过滤 | 数量、年龄等整数 |
| `money` | 金额输入 | ¥ 前缀 + 输入框 + 小数过滤 | 金额、价格等货币值 |
| `phone` | 手机号输入 | 区号输入 + 分隔线 + 手机号输入 | 手机号、联系电话 |
| `select` | 右箭头选择 | 文本 + 右箭头图标 | 银行卡类型、日期选择等 |
| `custom` | 完全自定义 | 自定义内容区 | 计数器、特殊控件等 |

Action 选择规则：

- 需要用户手动输入文本时使用 `text`。
- 只允许输入整数时使用 `number`，自动过滤非数字字符。
- 输入金额时使用 `money`，自动显示 ¥ 前缀并限制小数位数。
- 输入手机号时使用 `phone`，自带区号和 11 位限制。
- 需要跳转或弹窗选择时使用 `select`，选择后通过程序回写显示文本。
- 以上都不满足时使用 `custom`。

### RightButton

| RightButton | 含义 | 结构 | 应用场景 |
|---|---|---|---|
| `none` | 无右侧按钮 | 无 | 默认，大多数表单行 |
| `link` | 文字链接 | 链接文本 | "全部""查看""获取验证码"等辅助操作 |
| `button` | 按钮 | WGButton SCALE_32 | "新增""校验""发送"等操作按钮 |
| `icon-text` | 上图标下文字 | 图标 + 文字 | "扫码""拍照"等图标操作 |

RightButton 选择规则：

- 默认不使用右侧按钮（`none`）。
- 需要提供辅助链接操作（如"全部"填充金额）时使用 `link`。
- 需要触发操作（如"新增""校验"）时使用 `button`。
- 需要图标 + 文字的快捷操作（如扫码）时使用 `icon-text`。

### State

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 正常可用，显示 placeholder |
| `focused` | `:focus-within` | 操作区获得焦点，显示焦点态 |
| `disabled` | `.wg-form--disabled` | 整行禁用，标签和操作区均不可交互 |

### Error

| Error | 含义 | 视觉规则 |
|---|---|---|
| `false` | 正常状态 | 默认样式 |
| `true` | 错误状态 | 操作区显示错误态 + 错误提示文字 |

错误状态规则：

- 输入校验失败时进入错误状态。
- 错误提示文字显示在表单行底部，与操作区左对齐。
- 错误提示文字使用红色（`wg.color.status.danger.text`），字号 12px。
- 用户重新输入时，自动清除错误状态。
- 错误信息优先级高于计数文本：有错误时不显示计数。
- 错误恢复规则：用户修正内容后，必须自动恢复默认状态——清除 error class、清除错误文案、恢复默认边框/背景/文字颜色、恢复 aria-invalid 状态
- 具体恢复触发：input 触发有效输入后清除错误；select / picker 重新选择后清除错误；switch 重新切换后清除错误；upload 成功后清除错误

## 允许组合

| Layout | Action | RightButton | 错误状态 | 计数文本 |
|---|---|---|---|---|
| `horizontal` | `text` | `none` / `link` / `button` / `icon-text` | 允许 | 允许 |
| `horizontal` | `number` | `none` / `link` / `button` | 允许 | 不支持 |
| `horizontal` | `money` | `none` / `link` | 允许 | 不支持 |
| `horizontal` | `phone` | `none` | 允许 | 不支持 |
| `horizontal` | `select` | `none` | 不支持 | 不支持 |
| `horizontal` | `custom` | `none` / `link` / `button` / `icon-text` | 允许 | 不支持 |
| `vertical` | `text` | `none` / `link` / `button` / `icon-text` | 允许 | 允许 |
| `vertical` | `custom` | `none` / `link` / `button` / `icon-text` | 允许 | 不支持 |

附加规则：

- `select` 操作区只读展示，不做校验，不支持错误状态。
- `phone` 操作区不支持右侧按钮（手机号输入场景无需辅助操作）。
- `text` 操作区的 `multiline` 变体必须使用 `vertical` 布局。
- 同一表单容器内所有表单行之间默认显示分隔线，可通过 `showDivider` 控制。
- 计数文本仅在 `text` 操作区且设置了 `maxLength` 时显示，格式为"当前/最大"。
- 输入字符数 ≥ `showCountThreshold` 时才显示计数文本（默认 35），多行输入始终显示计数。

## 使用场景

### Form_Input（纯输入表单）

不与其他操作表单混用。当表单中所有行都是纯文本输入时使用。

- 案例1：绑定银行卡 — 纯文本输入（姓名、卡号等）
- 案例2：编辑供应商 — 备注（多行文本输入）

### Form_Input_L（输入表单_右对齐）

与其他操作表单混用。当表单中包含选择、金额等非纯文本操作时，文本输入行使用右对齐样式。

- 案例1：绑定银行卡 — 混合输入和选择（姓名输入 + 银行卡选择 + 金额输入）
- 案例2：修改结算账号信息 — 混合输入和选择

选择规则：

- 表单中所有行都是纯文本输入 → 使用 Form_Input 样式（输入区左对齐）
- 表单中混合了选择、金额等操作 → 文本输入行使用 Form_Input_L 样式（输入区右对齐），与其他操作区视觉对齐

## Anatomy

水平布局 + 文本输入 + 无右侧按钮：

```text
div.wg-form.wg-form--horizontal
├── div.wg-form__body
│   ├── label.wg-form__label
│   ├── div.wg-form__action
│   │   └── input.wg-form__input[placeholder="请输入"]
│   └── p.wg-form__hint（错误/计数文本，可选）
```

水平布局 + 金额输入 + 右侧链接按钮：

```text
div.wg-form.wg-form--horizontal
├── div.wg-form__body
│   ├── label.wg-form__label
│   ├── div.wg-form__action
│   │   ├── span.wg-form__currency（¥ 符号）
│   │   └── input.wg-form__input[placeholder="0.00"]
│   ├── div.wg-form__right
│   │   └── a.wg-form__link
│   └── p.wg-form__hint（错误/计数文本，可选）
```

水平布局 + 选择操作：

```text
div.wg-form.wg-form--horizontal
├── div.wg-form__body
│   ├── label.wg-form__label
│   ├── div.wg-form__action.wg-form__action--select
│   │   ├── span.wg-form__display（选中值或 placeholder）
│   │   └── i.wg-form__arrow
```

垂直布局 + 多行文本输入：

```text
div.wg-form.wg-form--vertical
├── div.wg-form__body
│   ├── label.wg-form__label
│   ├── div.wg-form__action
│   │   └── textarea.wg-form__input[placeholder="请输入"]
│   └── p.wg-form__hint（错误/计数文本，可选）
```

水平布局 + 手机号输入：

```text
div.wg-form.wg-form--horizontal
├── div.wg-form__body
│   ├── label.wg-form__label
│   ├── div.wg-form__action
│   │   ├── input.wg-form__region[placeholder="+86"]
│   │   ├── span.wg-form__separator
│   │   └── input.wg-form__input[placeholder="请输入手机号"]
```

水平布局 + 右侧按钮：

```text
div.wg-form.wg-form--horizontal
├── div.wg-form__body
│   ├── label.wg-form__label
│   ├── div.wg-form__action
│   │   └── input.wg-form__input[placeholder="请输入"]
│   ├── div.wg-form__right
│   │   └── button.wg-form__btn（WGButton SCALE_32）
```

V1 不支持标签区自定义富文本、操作区自定义 ViewBuilder 插槽、右侧图标文字按钮的上图标下文字样式。不得自行加入标签图标、退格区、徽章等元素；这些作为 V1 能力缺失标注。

## 文案规则

- 标签使用简短名词，如"姓名""金额""手机号""备注"，最多 2 行，超出省略。
- placeholder 使用简短提示，如"请输入姓名""请输入金额""请选择"。
- placeholder 单行展示，不换行。
- 选择操作区的 placeholder 默认为"请选择"。
- 错误提示使用明确的问题描述，如"姓名不能为空""请输入 11 位手机号""金额不能超过 50,000 元"。
- 错误提示单行展示，不换行，超长时截断显示省略号。
- 右侧链接文本使用简短操作词，如"全部""查看""获取验证码"。
- 右侧按钮文本使用简短动词，如"新增""校验""发送"。
- 金额输入的 ¥ 符号与数字之间无间距。
- 同一表单内的标签和 placeholder 使用一致的语法结构。

## Canonical HTML

水平布局 + 文本输入：

```html
<div class="wg-form wg-form--horizontal">
  <div class="wg-form__body">
    <label class="wg-form__label">姓名</label>
    <div class="wg-form__action">
      <input class="wg-form__input" type="text" placeholder="请输入姓名" />
    </div>
  </div>
</div>
```

水平布局 + 文本输入 + 错误状态：

```html
<div class="wg-form wg-form--horizontal wg-form--error">
  <div class="wg-form__body">
    <label class="wg-form__label">姓名</label>
    <div class="wg-form__action">
      <input class="wg-form__input" type="text" value="" placeholder="请输入姓名" />
    </div>
  </div>
  <p class="wg-form__hint">姓名不能为空</p>
</div>
```

水平布局 + 金额输入 + 右侧链接：

```html
<div class="wg-form wg-form--horizontal">
  <div class="wg-form__body">
    <label class="wg-form__label">金额</label>
    <div class="wg-form__action">
      <span class="wg-form__currency">¥</span>
      <input class="wg-form__input" type="text" inputmode="decimal" placeholder="0.00" />
    </div>
    <div class="wg-form__right">
      <a class="wg-form__link" href="javascript:void(0)">全部</a>
    </div>
  </div>
</div>
```

水平布局 + 数字输入 + 右侧按钮：

```html
<div class="wg-form wg-form--horizontal">
  <div class="wg-form__body">
    <label class="wg-form__label">数量</label>
    <div class="wg-form__action">
      <input class="wg-form__input" type="text" inputmode="numeric" placeholder="0" />
    </div>
    <div class="wg-form__right">
      <button class="wg-button wg-button--compact wg-button--strong" type="button">
        <span class="wg-button__surface">
          <span class="wg-button__label">校验</span>
        </span>
      </button>
    </div>
  </div>
</div>
```

水平布局 + 手机号输入：

```html
<div class="wg-form wg-form--horizontal">
  <div class="wg-form__body">
    <label class="wg-form__label">手机号</label>
    <div class="wg-form__action">
      <input class="wg-form__region" type="text" value="+86" placeholder="+86" />
      <span class="wg-form__separator"></span>
      <input class="wg-form__input" type="tel" placeholder="请输入手机号" maxlength="11" />
    </div>
  </div>
</div>
```

水平布局 + 选择操作：

```html
<div class="wg-form wg-form--horizontal">
  <div class="wg-form__body">
    <label class="wg-form__label">银行卡</label>
    <div class="wg-form__action wg-form__action--select">
      <span class="wg-form__display">招商银行</span>
      <i class="wg-form__arrow"></i>
    </div>
  </div>
</div>
```

水平布局 + 选择操作（未选择）：

```html
<div class="wg-form wg-form--horizontal">
  <div class="wg-form__body">
    <label class="wg-form__label">银行卡</label>
    <div class="wg-form__action wg-form__action--select">
      <span class="wg-form__display wg-form__display--placeholder">请选择</span>
      <i class="wg-form__arrow"></i>
    </div>
  </div>
</div>
```

垂直布局 + 多行文本输入 + 计数：

```html
<div class="wg-form wg-form--vertical">
  <div class="wg-form__body">
    <label class="wg-form__label">备注</label>
    <div class="wg-form__action">
      <textarea class="wg-form__input" placeholder="选填，最多 500 字" rows="3"></textarea>
    </div>
  </div>
  <p class="wg-form__hint wg-form__hint--count">0/500</p>
</div>
```

禁用状态：

```html
<div class="wg-form wg-form--horizontal wg-form--disabled">
  <div class="wg-form__body">
    <label class="wg-form__label">姓名</label>
    <div class="wg-form__action">
      <input class="wg-form__input" type="text" value="张三" disabled />
    </div>
  </div>
</div>
```

表单容器（多行组合）：

```html
<div class="wg-form-group">
  <div class="wg-form wg-form--horizontal wg-form--divider">
    <div class="wg-form__body">
      <label class="wg-form__label">收款人</label>
      <div class="wg-form__action">
        <input class="wg-form__input" type="text" placeholder="请输入收款人姓名" />
      </div>
    </div>
  </div>
  <div class="wg-form wg-form--horizontal wg-form--divider">
    <div class="wg-form__body">
      <label class="wg-form__label">金额</label>
      <div class="wg-form__action">
        <span class="wg-form__currency">¥</span>
        <input class="wg-form__input" type="text" inputmode="decimal" placeholder="0.00" />
      </div>
      <div class="wg-form__right">
        <a class="wg-form__link" href="javascript:void(0)">全部</a>
      </div>
    </div>
  </div>
  <div class="wg-form wg-form--horizontal">
    <div class="wg-form__body">
      <label class="wg-form__label">类型</label>
      <div class="wg-form__action wg-form__action--select">
        <span class="wg-form__display wg-form__display--placeholder">请选择</span>
        <i class="wg-form__arrow"></i>
      </div>
    </div>
  </div>
</div>
```

## Canonical CSS

```css
/* ===== Form 容器 ===== */
.wg-form {
  display: flex;
  flex-direction: column;
  padding-inline: var(--wg-spacing-16);
  background-color: var(--wg-color-bg-surface);
  position: relative;
}

/* ===== 表单行主体 ===== */
.wg-form__body {
  display: flex;
  align-items: center;
  padding-block: var(--wg-spacing-16);
}

/* ===== 水平布局 ===== */
.wg-form--horizontal .wg-form__body {
  flex-direction: row;
}

.wg-form--horizontal .wg-form__label {
  flex: 0 0 calc(var(--wg-size-48) * 2);
  margin-inline-end: var(--wg-spacing-24);
}

.wg-form--horizontal .wg-form__action {
  flex: 1 1 0;
  min-inline-size: 0;
}

/* ===== 垂直布局 ===== */
.wg-form--vertical .wg-form__body {
  flex-direction: column;
  align-items: stretch;
}

.wg-form--vertical .wg-form__label {
  margin-block-end: var(--wg-spacing-4);
}

.wg-form--vertical .wg-form__action {
  width: 100%;
}

/* ===== 标签 ===== */
.wg-form__label {
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-all;
}

/* ===== 操作区 ===== */
.wg-form__action {
  display: flex;
  align-items: center;
  gap: var(--wg-spacing-4);
}

/* ===== 输入框 ===== */
.wg-form__input {
  appearance: none;
  flex: 1 1 0;
  min-inline-size: 0;
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  font-family: var(--wg-font-family-text);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-primary);
  outline: none;
  padding: var(--wg-spacing-0);
  block-size: var(--wg-font-lineheight-16);
}

.wg-form__input::placeholder {
  color: var(--wg-color-text-placeholder);
}

/* 多行输入 */
.wg-form--vertical .wg-form__input {
  resize: none;
  block-size: auto;
  min-block-size: var(--wg-size-40);
}

/* 数字输入居中加粗 */
.wg-form__input--number {
  text-align: right;
  font-weight: var(--wg-font-weight-medium);
}

/* ===== 金额 ¥ 符号 ===== */
.wg-form__currency {
  flex: 0 0 auto;
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-placeholder);
  transition:
    color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-form__currency--filled {
  color: var(--wg-color-text-primary);
}

/* ===== 手机号区号 ===== */
.wg-form__region {
  appearance: none;
  flex: 0 0 var(--wg-size-48);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: transparent;
  font-family: var(--wg-font-family-text);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-primary);
  outline: none;
  padding: var(--wg-spacing-0);
}

.wg-form__region::placeholder {
  color: var(--wg-color-text-placeholder);
}

.wg-form__separator {
  flex: 0 0 var(--wg-stroke-width-default);
  block-size: var(--wg-size-16);
  background-color: var(--wg-color-border-default);
  margin-inline: var(--wg-spacing-4);
}

/* ===== 选择操作区 ===== */
.wg-form__action--select {
  cursor: pointer;
  justify-content: flex-end;
}

.wg-form__display {
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-primary);
  text-align: right;
  flex: 1 1 0;
  min-inline-size: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.wg-form__display--placeholder {
  color: var(--wg-color-text-placeholder);
}

/* ===== 箭头图标 ===== */
.wg-form__arrow {
  display: inline-block;
  inline-size: var(--wg-size-16);
  block-size: var(--wg-size-16);
  flex-shrink: 0;
  background-color: var(--wg-color-text-tertiary);
  -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z'/%3E%3C/svg%3E");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
}

/* ===== 右侧按钮区 ===== */
.wg-form__right {
  flex: 0 0 auto;
  margin-inline-start: var(--wg-spacing-24);
  display: flex;
  align-items: center;
}

/* ===== 右侧链接 ===== */
.wg-form__link {
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-action-primary-default);
  text-decoration: none;
  white-space: nowrap;
  cursor: pointer;
}

.wg-form__link:active {
  color: var(--wg-color-action-link-pressed);
}

/* ===== 提示文本（错误/计数） ===== */
.wg-form__hint {
  padding-block-end: var(--wg-spacing-4);
  padding-inline-start: calc(var(--wg-size-48) * 2 + var(--wg-spacing-24));
  font-size: var(--wg-font-size-12);
  line-height: var(--wg-font-lineheight-12);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-status-danger-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 100%;
}

.wg-form--vertical .wg-form__hint {
  padding-inline-start: var(--wg-spacing-0);
}

.wg-form__hint--count {
  color: var(--wg-color-text-tertiary);
}

/* ===== 分隔线 ===== */
.wg-form--divider::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: var(--wg-spacing-16);
  right: var(--wg-spacing-16);
  block-size: var(--wg-stroke-width-hairline);
  background-color: var(--wg-color-divider-default);
}

.wg-form--divider-inset::after {
  right: 0;
}

/* ===== 禁用状态 ===== */
.wg-form--disabled .wg-form__label {
  color: var(--wg-color-text-disabled);
}

.wg-form--disabled .wg-form__input {
  color: var(--wg-color-text-disabled);
  cursor: not-allowed;
}

.wg-form--disabled .wg-form__display {
  color: var(--wg-color-text-disabled);
}

.wg-form--disabled .wg-form__arrow {
  background-color: var(--wg-color-text-disabled);
}

.wg-form--disabled .wg-form__link {
  color: var(--wg-color-text-disabled);
  pointer-events: none;
}

/* ===== 错误状态 ===== */
.wg-form--error .wg-form__input {
  color: var(--wg-color-status-danger-text);
}

.wg-form--error .wg-form__currency {
  color: var(--wg-color-status-danger-text);
}

/* ===== 表单容器 ===== */
.wg-form-group {
  display: flex;
  flex-direction: column;
  background-color: var(--wg-color-bg-surface);
}
```

水平布局表单行高度自适应（上下 padding 16px），标签区默认宽度 96px，操作区与标签区间距 24px，右侧按钮区间距 24px。分隔线为 0.5pt 细线。

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认 class | 正常可用，显示 placeholder |
| `focused` | `:focus-within` | 操作区输入框获得焦点 |
| `disabled` | `.wg-form--disabled` | 整行禁用，标签和操作区均不可交互 |
| `error` | `.wg-form--error` | 操作区错误态 + 底部错误提示文字 |

V1 未定义 `loading`、`success`、`readonly` 视觉变体。遇到这些需求不得自行向 Form 加入 Spinner、图标或颜色；通过页面级反馈区域实现业务状态，并标注组件能力缺失。

## 可访问性

- 文本输入必须使用原生 `<input>` 或 `<textarea>`。
- 标签必须使用 `<label>` 元素，并通过 `for` 属性关联到输入框。
- 禁用状态必须使用 `disabled` 属性，不能只降低透明度。
- 数字输入框必须使用 `inputmode="numeric"` 以唤起数字键盘。
- 金额输入框必须使用 `inputmode="decimal"` 以唤起数字键盘。
- 手机号输入框必须使用 `type="tel"` 以唤起电话键盘。
- 多行输入必须使用 `<textarea>`，不得使用 `<input>`。
- 选择操作区必须使用可交互元素或添加 `role="button"` 和 `tabindex="0"`。
- 错误提示必须使用 `<p>` 标签，并通过 `aria-describedby` 关联到输入框（可选）。
- 焦点顺序必须与视觉顺序一致。
- 禁止使用 `div`、`span` 模拟可输入框。

## 生成约束

- 必须声明一个 `layout` class（`wg-form--horizontal` 或 `wg-form--vertical`）。
- 操作区必须声明对应的 action 样式（`wg-form__action--select` 用于选择操作区）。
- 不得覆盖表单行高度、标签宽度、字号、颜色、间距和分隔线。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 错误提示必须使用 `wg-form__hint`，不得自定义样式。
- 计数文本必须使用 `wg-form__hint--count`，不得自定义样式。
- 金额 ¥ 符号必须使用 `wg-form__currency`，输入后需添加 `wg-form__currency--filled` class。
- 手机号区号必须使用 `wg-form__region`，分隔线必须使用 `wg-form__separator`。
- 选择操作区必须使用 `wg-form__action--select`，箭头必须使用 `wg-form__arrow`。
- 右侧链接必须使用 `wg-form__link`，右侧按钮必须使用 `wg-form__right` 容器。
- 分隔线必须使用 `wg-form--divider` class，不得自定义分割线样式。
- 页面布局只控制 Form 的位置和宽度，不控制 Form 内部样式。
- 完整页面中出现 Form 时，必须读取并遵守本文件。
- Canonical CSS 必须从本文件 `## Canonical CSS` 区块逐字复制到 `styles/components.css`，不得增删规则、修改选择器或添加属性。组件视觉行为只能通过规范中已声明的修饰符 class 调整。
- 同一个 form group 内对齐方式必须统一，禁止左对齐和右对齐混用。
- 表单字段必须按业务含义分组，不允许把所有字段连续堆叠成一组。
- 错误修正后必须清除 error 状态（error class、error 文案、aria-invalid）。

## 自检

```text
□ 是否先判断 horizontal / vertical 布局模式
□ 是否选择了正确的操作区类型（text / number / money / phone / select / custom）
□ 多行文本输入是否使用了 vertical 布局
□ 是否选择了正确的右侧按钮类型（none / link / button / icon-text）
□ 是否遵守了错误状态的视觉规则（操作区错误态 + 错误提示文字）
□ 金额输入是否使用了 ¥ 前缀和 inputmode="decimal"
□ 手机号输入是否使用了区号输入框和 type="tel"
□ 数字输入是否使用了 inputmode="numeric"
□ 选择操作区是否使用了 wg-form__action--select
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 是否使用原生 input 或 textarea
□ disabled 是否使用 --disabled class
□ 是否没有自创 loading、success、readonly 变体
□ 错误提示和计数文本是否使用了 wg-form__hint
□ 分隔线是否使用了 wg-form--divider class
□ 同一 form group 内对齐方式是否统一
□ 表单字段是否按业务含义分组
□ 错误修正后是否清除 error 状态
□ 是否没有把所有字段连续堆叠成一组
```

## 规范来源

- Figma：`📙 wegoo 组件应用场景`，节点 `251:4342`（Form 命名表）和节点 `596:23880`（Form_Input 使用场景）。提取水平/垂直两种布局模式的结构、尺寸、间距和颜色；提取 Form_Input（纯输入表单，不与其他操作混用）和 Form_Input_L（输入表单右对齐，与其他操作混用）的使用场景规则。
- Kuikly `Form`：参考两层结构（Form 容器 + FormBody 单元格）、六种操作区类型（Text / Number / Money / Phone / Select / Custom）、三种右侧按钮（Link / Button / IconText）、两种布局模式（HORIZONTAL / VERTICAL）、校验系统（validateAll / getValues）、分隔线控制（showDivider）、标签区宽度（默认 96pt）、间距规格（左右 padding 16pt、标签与操作区间距 24pt、右侧按钮左间距 24pt）、计数/错误文本定位规则；不继承 Kuikly DSL、FormCellConfig 数据类、FormActionConfig sealed class、FormRightButton sealed class、FormValidationResult 数据类、ViewRef 命令式 API、observable 响应式属性、ViewBuilder 自定义插槽。
