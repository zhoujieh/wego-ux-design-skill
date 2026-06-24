# Result

Result 结果页组件，用于操作完成后的反馈页面，如成功、失败、搜索无结果、空状态等场景。本规则首先判断布局类型，再确定图片、文案和按钮组合。

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

使用 Result：

- 操作完成后的全屏反馈，如提交成功、支付成功、操作失败。
- 列表或页面为空时的缺省状态，如无数据、无内容。
- 搜索无结果时的提示页面。
- 需要引导用户进行下一步操作的中间结果页。

不使用 Result：

- 操作过程中的轻量反馈：使用 Toast。
- 需要用户确认的弹窗信息：使用 Dialog。
- 页面内局部区域的加载状态：使用 Loading / Skeleton。
- 表单校验错误提示：使用内联错误文案。

## 语义模型

Result 有三个决策维度：

```text
layout    布局类型，决定消息区与操作区的高度分配
image     图片类型，决定状态图标或插图
buttons   按钮组合，决定操作区的交互方式
```

### Layout

| Layout | 含义 | 结构 | 应用场景 |
|---|---|---|---|
| `result-40` | 固定间距，内容包裹 | 消息区 + 操作区，上下各 40dp padding | 嵌入式结果展示，如卡片内、列表内 |
| `result-60` | 消息区 6 : 操作区 4 的 flex 比例 | 消息区 flex(6) + 操作区 flex(4)，各自垂直居中 | 全屏成功页，如提交成功、支付完成 |
| `result-80` | 底部留白 20%，内容居中对齐 | 消息区动态定位至 40% 高度处，操作区固定底部 | 全屏失败/空状态页 |

### Image

| Image | 含义 | 尺寸 | 应用场景 |
|---|---|---|---|
| `success` | 成功打勾图标 | 72×72 | 操作成功 |
| `error` | 失败叉号图标 | 72×72 | 操作失败 |
| `warning` | 警告叹号图标 | 72×72 | 异常提示 |
| `waiting` | 等待图标 | 72×72 | 处理中、审核中 |
| `celebrate` | 嗨起来勾图标 | 72×72 | 庆祝类成功 |
| `not-found` | 通用无结果插图 | 120×120 | 空数据、无内容 |
| `search-not-found` | 搜索无结果插图 | 120×120 | 搜索无结果 |
| `no-permission` | 无权限插图 | 120×120 | 权限不足 |
| `time-expired` | 时间已过插图 | 120×120 | 链接过期、活动结束 |
| `network-error` | 网络异常插图 | 120×120 | 网络错误 |
| `custom` | 自定义图片 | 72×72 或 120×120 | 业务自定义场景 |

图片尺寸规则：

- 状态图标类（success / error / warning / waiting / celebrate）：72×72
- 插图归档类（not-found / search-not-found / no-permission / time-expired / network-error）：120×120
- 自定义图片支持 72×72 或 120×120 两种尺寸，通过 `--wg-component-result-image-size` 控制

### Buttons

| Buttons | 含义 | 规则 |
|---|---|---|
| `none` | 无按钮 | 纯信息告知，无操作引导 |
| `single` | 单按钮：确认 | 主要操作，如"完成""返回首页" |
| `dual` | 双按钮：取消 + 确认 | 两个操作，如"查看详情" + "完成" |
| `with-links` | 按钮 + 底部链接 | 主按钮 + 底部最多 2 个文字链接 |

底部链接规则：

- 最多 2 个文字链接，中间用分隔线分开
- 链接文字使用次要色，支持点击态
- 链接位于按钮下方，间距 24dp

## 允许组合

| Layout | none | single | dual | with-links |
|---|---|---|---|---|
| `result-40` | 允许 | 允许 | 允许 | 允许 |
| `result-60` | 允许 | 允许 | 允许 | 允许 |
| `result-80` | 允许 | 允许 | 允许 | 允许 |

附加规则：

- 搜索类结果（search-not-found）通常使用 `result-40` 或 `result-80` 布局，且通常无按钮或仅单按钮。
- 双按钮时，取消按钮在左，确认按钮在右，间距 16dp。
- 底部链接最多 2 个，超过时合并为"更多"入口。

## Anatomy

通用结构：

```text
div.wg-result.wg-result--{layout}
├── div.wg-result__message
│   ├── div.wg-result__image
│   │   └── i.wg-result__icon.wg-result__icon--{image}
│   ├── h2.wg-result__title
│   ├── p.wg-result__description
│   │   ├── span.wg-result__text-start
│   │   ├── a.wg-result__link（可选）
│   │   └── span.wg-result__text-end（可选）
│   └── div.wg-result__custom（可选）
├── div.wg-result__operate
│   ├── div.wg-result__buttons.wg-result__buttons--{single|dual}
│   │   ├── button.wg-result__button.wg-result__button--cancel（dual 时）
│   │   └── button.wg-result__button.wg-result__button--confirm
│   └── div.wg-result__links（可选）
│       ├── a.wg-result__link-btn
│       ├── span.wg-result__link-divider（2 个链接时）
│       └── a.wg-result__link-btn（第 2 个，可选）
```

各布局差异：

- `result-40`：外层不设 flex，上下各 40dp padding，内容自然高度排列
- `result-60`：外层 flex(1)，消息区 flex(6) 居中，操作区 flex(4) 居中
- `result-80`：外层 flex(1)，消息区动态定位至 40% 高度处，操作区固定底部

## 文案规则

- 标题使用简短明确的短语，如"操作成功""暂无数据""搜索无结果"。
- 标题单行展示，超长时截断显示省略号。
- 说明文本使用完整句子说明情况，如"你的申请已提交，预计 3 个工作日内审核完成"。
- 说明文本最多 3 行，超出截断显示省略号。
- 说明文本支持「普通文字 + 链接文字 + 普通文字」的混排格式。
- 链接文字使用蓝色高亮色，支持点击。
- 确认按钮文案不超过 5 个字符，如"完成""返回首页""刷新"。
- 取消按钮文案不超过 5 个字符，如"查看详情""取消"。
- 底部链接文案不超过 6 个字符，如"查看订单""联系客服"。

## Canonical HTML

`result-60` 布局 — 成功页，双按钮：

```html
<div class="wg-result wg-result--result-60">
  <div class="wg-result__message">
    <div class="wg-result__image">
      <i class="wg-result__icon wg-result__icon--success"></i>
    </div>
    <h2 class="wg-result__title">提交成功</h2>
    <p class="wg-result__description">
      <span class="wg-result__text-start">你的申请已提交，预计 </span>
      <a class="wg-result__link" href="javascript:void(0)">3个工作日</a>
      <span class="wg-result__text-end"> 内审核完成</span>
    </p>
  </div>
  <div class="wg-result__operate">
    <div class="wg-result__buttons wg-result__buttons--dual">
      <button class="wg-result__button wg-result__button--cancel" type="button">查看详情</button>
      <button class="wg-result__button wg-result__button--confirm" type="button">完成</button>
    </div>
  </div>
</div>
```

`result-80` 布局 — 空状态页，单按钮：

```html
<div class="wg-result wg-result--result-80">
  <div class="wg-result__message">
    <div class="wg-result__image">
      <i class="wg-result__icon wg-result__icon--not-found"></i>
    </div>
    <h2 class="wg-result__title">暂无数据</h2>
    <p class="wg-result__description">
      <span class="wg-result__text-start">当前没有可展示的内容</span>
    </p>
  </div>
  <div class="wg-result__operate">
    <div class="wg-result__buttons wg-result__buttons--single">
      <button class="wg-result__button wg-result__button--confirm" type="button">刷新</button>
    </div>
  </div>
</div>
```

`result-40` 布局 — 搜索无结果，无按钮：

```html
<div class="wg-result wg-result--result-40">
  <div class="wg-result__message">
    <div class="wg-result__image">
      <i class="wg-result__icon wg-result__icon--search-not-found"></i>
    </div>
    <h2 class="wg-result__title">未找到相关结果</h2>
    <p class="wg-result__description">
      <span class="wg-result__text-start">试试 </span>
      <a class="wg-result__link" href="javascript:void(0)">换个关键词</a>
    </p>
  </div>
</div>
```

带底部链接 — 单按钮 + 底部链接：

```html
<div class="wg-result wg-result--result-60">
  <div class="wg-result__message">
    <div class="wg-result__image">
      <i class="wg-result__icon wg-result__icon--error"></i>
    </div>
    <h2 class="wg-result__title">提交失败</h2>
    <p class="wg-result__description">
      <span class="wg-result__text-start">网络异常，请重新提交</span>
    </p>
  </div>
  <div class="wg-result__operate">
    <div class="wg-result__buttons wg-result__buttons--single">
      <button class="wg-result__button wg-result__button--confirm" type="button">重新提交</button>
    </div>
    <div class="wg-result__links">
      <a class="wg-result__link-btn" href="javascript:void(0)">查看帮助</a>
      <span class="wg-result__link-divider"></span>
      <a class="wg-result__link-btn" href="javascript:void(0)">联系客服</a>
    </div>
  </div>
</div>
```

带自定义区域：

```html
<div class="wg-result wg-result--result-60">
  <div class="wg-result__message">
    <div class="wg-result__image">
      <i class="wg-result__icon wg-result__icon--success"></i>
    </div>
    <h2 class="wg-result__title">支付成功</h2>
    <p class="wg-result__description">
      <span class="wg-result__text-start">订单号：20250410001</span>
    </p>
    <div class="wg-result__custom">
      <!-- 页面级自定义内容，使用 wego Token -->
      <div class="custom-amount">金额：¥128.00</div>
    </div>
  </div>
  <div class="wg-result__operate">
    <div class="wg-result__buttons wg-result__buttons--single">
      <button class="wg-result__button wg-result__button--confirm" type="button">完成</button>
    </div>
  </div>
</div>
```

## Canonical CSS

```css
/* ── Result Container ── */
.wg-result {
  display: flex;
  flex-direction: column;
  inline-size: 100%;
}

/* ── Layout Variants ── */
.wg-result--result-40 {
  padding: var(--wg-spacing-40) 0;
}

.wg-result--result-60 {
  flex: 1;
}

.wg-result--result-80 {
  flex: 1;
}

/* ── Message Area ── */
.wg-result__message {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding-inline: var(--wg-spacing-32);
}

.wg-result--result-60 .wg-result__message {
  flex: 6;
  justify-content: center;
}

.wg-result--result-80 .wg-result__message {
  padding-block-start: 40%;
}

.wg-result--result-40 .wg-result__message {
  align-items: center;
}

/* ── Image Area ── */
.wg-result__image {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-block-end: var(--wg-spacing-24);
}

.wg-result__icon {
  display: block;
  flex-shrink: 0;
}

.wg-result__icon--success,
.wg-result__icon--error,
.wg-result__icon--warning,
.wg-result__icon--waiting,
.wg-result__icon--celebrate {
  inline-size: var(--wg-size-72);
  block-size: var(--wg-size-72);
  border-radius: var(--wg-radius-full);
}

.wg-result__icon--success {
  background-color: var(--wg-color-status-success-default);
}

.wg-result__icon--error {
  background-color: var(--wg-color-status-danger-default);
}

.wg-result__icon--warning {
  background-color: var(--wg-color-status-warning-default);
}

.wg-result__icon--waiting {
  background-color: var(--wg-color-status-info-default);
}

.wg-result__icon--celebrate {
  background-color: var(--wg-color-status-success-default);
}

.wg-result__icon--not-found,
.wg-result__icon--search-not-found,
.wg-result__icon--no-permission,
.wg-result__icon--time-expired,
.wg-result__icon--network-error,
.wg-result__icon--custom {
  inline-size: 120px;
  block-size: 120px;
}

/* ── Title ── */
.wg-result__title {
  font-size: var(--wg-font-size-18);
  line-height: var(--wg-font-lineheight-18);
  font-weight: var(--wg-font-weight-medium);
  color: var(--wg-color-text-primary);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 100%;
}

/* ── Description ── */
.wg-result__description {
  margin-block-start: var(--wg-spacing-8);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  font-weight: var(--wg-font-weight-regular);
  color: var(--wg-color-text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  max-inline-size: 100%;
}

.wg-result__link {
  color: var(--wg-color-action-primary-default);
  text-decoration: none;
  cursor: pointer;
}

.wg-result__link:active {
  opacity: 0.6;
}

/* ── Custom Slot ── */
.wg-result__custom {
  margin-block-start: var(--wg-spacing-16);
  inline-size: 100%;
}

/* ── Operate Area ── */
.wg-result__operate {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-inline: var(--wg-spacing-32);
}

.wg-result--result-60 .wg-result__operate {
  flex: 4;
  justify-content: center;
}

.wg-result--result-80 .wg-result__operate {
  margin-block-start: var(--wg-spacing-40);
}

/* ── Buttons ── */
.wg-result__buttons {
  display: flex;
  align-items: center;
  justify-content: center;
  inline-size: 100%;
}

.wg-result__buttons--dual {
  gap: var(--wg-spacing-16);
}

.wg-result__buttons--single {
  justify-content: center;
}

.wg-result__button {
  appearance: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  block-size: var(--wg-size-48);
  inline-size: 100%;
  padding: 0;
  border: none;
  border-radius: var(--wg-radius-lg);
  cursor: pointer;
  font-family: var(--wg-font-family-text);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
  transition:
    opacity var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-result__button--confirm {
  background-color: var(--wg-color-action-primary-default);
  color: var(--wg-color-text-inverse);
}

.wg-result__button--cancel {
  background-color: var(--wg-color-bg-secondary);
  color: var(--wg-color-text-primary);
}

.wg-result__button:not(:disabled):active {
  opacity: 0.6;
}

.wg-result__button:focus-visible {
  outline: var(--wg-stroke-width-strong) var(--wg-stroke-style-solid) var(--wg-color-state-focus);
  outline-offset: calc(-1 * var(--wg-spacing-2));
}

.wg-result__button:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}

/* ── Bottom Links ── */
.wg-result__links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--wg-spacing-12);
  margin-block-start: var(--wg-spacing-24);
}

.wg-result__link-btn {
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  color: var(--wg-color-text-secondary);
  text-decoration: none;
  cursor: pointer;
}

.wg-result__link-btn:active {
  opacity: 0.6;
}

.wg-result__link-divider {
  inline-size: var(--wg-stroke-width-hairline);
  block-size: var(--wg-spacing-12);
  background-color: var(--wg-color-divider-default);
}
```

## 状态

| State | HTML / CSS 表达 | 规则 |
|---|---|---|
| `default` | 默认渲染 | 正常展示所有元素 |
| `pressed` | `:active`（按钮/链接） | 按下时透明度 0.6，不位移、不缩放 |
| `focus-visible` | `:focus-visible`（按钮） | 必须显示清晰焦点描边 |
| `disabled` | `disabled`（按钮） | 统一使用禁用透明度 0.4，不响应操作 |

V1 未定义 `loading`、`scrolling` 视觉变体。说明文本超长时截断显示省略号，不得自行添加滚动区域；标注组件能力缺失。

## 可访问性

- 标题必须使用 `<h2>` 标签，确保语义正确。
- 按钮必须使用原生 `<button>`。
- 禁用状态必须使用 `disabled` 属性，不能只降低透明度。
- 链接必须使用原生 `<a>` 标签。
- 图片区域如为纯装饰，使用 `aria-hidden="true"`；如承载语义，使用 `role="img"` + `aria-label`。
- 禁止使用 `div`、`span` 模拟可点击按钮或链接。

## 生成约束

- 必须同时声明一个 `layout` class。
- 必须使用 `wg-result__message`、`wg-result__operate`、`wg-result__buttons`。
- 不得覆盖 Result 内边距、图片尺寸和按钮高度。
- 不得覆盖按钮颜色、字号和圆角。
- 不得使用内联 style 修改组件。
- 不得新增 `primary`、`secondary`、`large`、`small` 等平行命名。
- 自定义区内容不得使用 `.wg-result` 命名空间内的子元素 class。
- 页面脚本可以控制按钮回调和链接跳转，但不得绕过组件规定的 Anatomy、状态语义和可访问性约束。
- 完整页面中出现 Result 时，必须读取并遵守本文件。

## 自检

```text
□ 是否先判断布局类型 → result-40 / result-60 / result-80
□ 是否只存在一个 layout
□ 是否遵守 none / single / dual / with-links 按钮组合
□ 是否使用规定的 HTML Anatomy
□ 是否只引用已有 Token
□ 是否使用原生 button 和正确 type
□ 图片类型是否匹配场景（成功/失败/空状态/搜索无结果）
□ 说明文本是否控制在 3 行以内
□ 底部链接是否不超过 2 个
□ disabled 是否使用原生属性
□ 是否没有自创 loading、scrollable 变体
□ 自定义区是否没有额外按钮或操作入口
```

## 规范来源

- Figma：`📙 wegoo 组件库`，节点 `9192:1529`。提取 Result_40、Result_60、Result_80 三种布局的结构、尺寸、间距和按钮规则；提取状态图标（72×72）和插图归档（120×120）的分类与使用场景。
- Kuikly `Result`：参考 ResultType 的布局策略（6:4 比例、80% 居中、40% 固定间距）、ResultImgPreset 的图片预设、ResultMessageConfig 的消息区域配置（标题、说明文本富文本混排、自定义区域）、ResultOperateConfig 的操作区域配置（确认/取消按钮、底部链接）；不继承 Kuikly DSL、flex 布局计算逻辑、响应式高度调整机制。
