# 微购 Design Token Reference

<!-- GENERATED FILE. DO NOT EDIT. Run: python3 scripts/generate_tokens.py -->

> Version 3.2.0  
> 唯一数据源：`tokens.json`。本文件由脚本生成，禁止手工修改。

## 使用规则

- 设计说明使用 `wg.*` 名称。
- HTML/CSS 使用对应的 `--wg-*` 变量。
- Token 值和映射只能在 `tokens.json` 中修改。

## Color

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.color.action.danger.default` | `--wg-color-action-danger-default` | `wg.color.base.danger.500` | 危险操作默认态 |
| `wg.color.action.danger.hover` | `--wg-color-action-danger-hover` | `wg.color.base.danger.alpha.80` | 危险操作 hover |
| `wg.color.action.danger.pressed` | `--wg-color-action-danger-pressed` | `wg.color.base.danger.alpha.80` | 危险操作 pressed |
| `wg.color.action.link.default` | `--wg-color-action-link-default` | `wg.color.base.link.500` | 链接操作默认态 |
| `wg.color.action.link.disabled` | `--wg-color-action-link-disabled` | `wg.color.base.link.alpha.20` | 链接操作 disabled |
| `wg.color.action.link.hover` | `--wg-color-action-link-hover` | `wg.color.base.link.hover` | 链接操作 hover |
| `wg.color.action.link.pressed` | `--wg-color-action-link-pressed` | `wg.color.base.link.pressed` | 链接操作 pressed |
| `wg.color.action.primary.default` | `--wg-color-action-primary-default` | `wg.color.base.brand.500` | 主操作默认态 |
| `wg.color.action.primary.disabled` | `--wg-color-action-primary-disabled` | `wg.color.base.brand.alpha.60` | 主操作 disabled |
| `wg.color.action.primary.hover` | `--wg-color-action-primary-hover` | `wg.color.base.brand.alpha.80` | 主操作 hover |
| `wg.color.action.primary.pressed` | `--wg-color-action-primary-pressed` | `wg.color.base.brand.alpha.80` | 主操作 pressed |
| `wg.color.action.secondary.default` | `--wg-color-action-secondary-default` | `wg.color.base.neutral.alpha.03` | 次操作默认态 |
| `wg.color.action.secondary.hover` | `--wg-color-action-secondary-hover` | `wg.color.base.neutral.alpha.06` | 次操作 hover |
| `wg.color.action.secondary.pressed` | `--wg-color-action-secondary-pressed` | `wg.color.base.neutral.alpha.10` | 次操作 pressed |
| `wg.color.base.accent.gold.500` | `--wg-color-base-accent-gold-500` | `#C79A56` | 金色权益、等级、价值感表达 |
| `wg.color.base.accent.green.500` | `--wg-color-base-accent-green-500` | `#00C777` | 辅助绿色，不替代品牌绿 |
| `wg.color.base.accent.purple.500` | `--wg-color-base-accent-purple-500` | `#6367F0` | 会员、权益、特殊信息 |
| `wg.color.base.accent.yellow.500` | `--wg-color-base-accent-yellow-500` | `#FFC300` | 特殊强调、等级、权益类信息 |
| `wg.color.base.accent.yellow.alpha.10` | `--wg-color-base-accent-yellow-alpha-10` | `rgba(255, 195, 0, 0.10)` | 特殊强调极浅背景 |
| `wg.color.base.accent.yellow.alpha.20` | `--wg-color-base-accent-yellow-alpha-20` | `rgba(255, 195, 0, 0.20)` | 特殊强调浅背景 |
| `wg.color.base.accent.yellow.alpha.60` | `--wg-color-base-accent-yellow-alpha-60` | `rgba(255, 195, 0, 0.60)` | 特殊强调弱化态 |
| `wg.color.base.accent.yellow.alpha.80` | `--wg-color-base-accent-yellow-alpha-80` | `rgba(255, 195, 0, 0.80)` | 特殊强调 hover |
| `wg.color.base.brand.500` | `--wg-color-base-brand-500` | `#03C160` | 品牌主色、主操作 |
| `wg.color.base.brand.alpha.10` | `--wg-color-base-brand-alpha-10` | `rgba(3, 193, 96, 0.10)` | 极浅品牌背景 |
| `wg.color.base.brand.alpha.20` | `--wg-color-base-brand-alpha-20` | `rgba(3, 193, 96, 0.20)` | 品牌浅背景、轻提示 |
| `wg.color.base.brand.alpha.60` | `--wg-color-base-brand-alpha-60` | `rgba(3, 193, 96, 0.60)` | 主操作 disabled / 次级品牌强调 |
| `wg.color.base.brand.alpha.80` | `--wg-color-base-brand-alpha-80` | `rgba(3, 193, 96, 0.80)` | 主操作 hover / 弱化品牌色 |
| `wg.color.base.danger.500` | `--wg-color-base-danger-500` | `#FA5051` | 危险 / 错误主色 |
| `wg.color.base.danger.alpha.10` | `--wg-color-base-danger-alpha-10` | `rgba(250, 80, 81, 0.10)` | 危险极浅背景 |
| `wg.color.base.danger.alpha.20` | `--wg-color-base-danger-alpha-20` | `rgba(250, 80, 81, 0.20)` | 危险浅背景 |
| `wg.color.base.danger.alpha.60` | `--wg-color-base-danger-alpha-60` | `rgba(250, 80, 81, 0.60)` | 危险弱化态 |
| `wg.color.base.danger.alpha.80` | `--wg-color-base-danger-alpha-80` | `rgba(250, 80, 81, 0.80)` | 危险 hover / 弱化强调 |
| `wg.color.base.info.500` | `--wg-color-base-info-500` | `#208BF1` | 信息主色 |
| `wg.color.base.info.alpha.10` | `--wg-color-base-info-alpha-10` | `rgba(32, 139, 241, 0.10)` | 信息极浅背景 |
| `wg.color.base.info.alpha.20` | `--wg-color-base-info-alpha-20` | `rgba(32, 139, 241, 0.20)` | 信息浅背景 |
| `wg.color.base.info.alpha.60` | `--wg-color-base-info-alpha-60` | `rgba(32, 139, 241, 0.60)` | 信息弱化态 |
| `wg.color.base.info.alpha.80` | `--wg-color-base-info-alpha-80` | `rgba(32, 139, 241, 0.80)` | 信息 hover / 弱化强调 |
| `wg.color.base.link.500` | `--wg-color-base-link-500` | `#285B9A` | 文本链接 |
| `wg.color.base.link.alpha.20` | `--wg-color-base-link-alpha-20` | `rgba(40, 91, 154, 0.20)` | 链接禁用态 |
| `wg.color.base.link.hover` | `--wg-color-base-link-hover` | `#285B9A` | 链接 hover，当前保持同色 |
| `wg.color.base.link.pressed` | `--wg-color-base-link-pressed` | `#285B9A` | 链接 pressed，当前保持同色 |
| `wg.color.base.neutral.100` | `--wg-color-base-neutral-100` | `#F2F3F6` | 浅灰背景、点击态背景 |
| `wg.color.base.neutral.200` | `--wg-color-base-neutral-200` | `#E9EAEF` | 强一点的选中 / pressed 背景 |
| `wg.color.base.neutral.300` | `--wg-color-base-neutral-300` | `#EDEDED` | 页面灰色背景 |
| `wg.color.base.neutral.50` | `--wg-color-base-neutral-50` | `#F8F9FA` | 极浅灰背景、一级 hover 背景 |
| `wg.color.base.neutral.500` | `--wg-color-base-neutral-500` | `#B7BEC5` | 失效文字、占位文字 |
| `wg.color.base.neutral.600` | `--wg-color-base-neutral-600` | `#9097A3` | 三级文字、弱辅助说明 |
| `wg.color.base.neutral.700` | `--wg-color-base-neutral-700` | `#6E7382` | 二级文字 |
| `wg.color.base.neutral.800` | `--wg-color-base-neutral-800` | `#3F434C` | 强辅助文字、深色容器 |
| `wg.color.base.neutral.900` | `--wg-color-base-neutral-900` | `#1E2028` | 一级文字、主要文本 |
| `wg.color.base.neutral.alpha.03` | `--wg-color-base-neutral-alpha-03` | `rgba(32, 47, 100, 0.03)` | 一级 hover、二级 normal 背景 |
| `wg.color.base.neutral.alpha.06` | `--wg-color-base-neutral-alpha-06` | `rgba(32, 47, 100, 0.06)` | 一级 pressed、二级 hover 背景 |
| `wg.color.base.neutral.alpha.08` | `--wg-color-base-neutral-alpha-08` | `rgba(32, 47, 100, 0.08)` | 默认线条、分割线 |
| `wg.color.base.neutral.alpha.10` | `--wg-color-base-neutral-alpha-10` | `rgba(32, 47, 100, 0.10)` | 二级 pressed、选中背景 |
| `wg.color.base.neutral.alpha.30` | `--wg-color-base-neutral-alpha-30` | `rgba(30, 32, 40, 0.30)` | 轻遮罩 |
| `wg.color.base.neutral.alpha.60` | `--wg-color-base-neutral-alpha-60` | `rgba(30, 32, 40, 0.60)` | 默认弹窗遮罩 |
| `wg.color.base.neutral.alpha.80` | `--wg-color-base-neutral-alpha-80` | `rgba(30, 32, 40, 0.80)` | 强遮罩 |
| `wg.color.base.promotion.500` | `--wg-color-base-promotion-500` | `#FF6045` | 促销 / 营销主色 |
| `wg.color.base.promotion.alpha.10` | `--wg-color-base-promotion-alpha-10` | `rgba(255, 96, 69, 0.10)` | 促销极浅背景 |
| `wg.color.base.promotion.alpha.20` | `--wg-color-base-promotion-alpha-20` | `rgba(255, 96, 69, 0.20)` | 促销浅背景 |
| `wg.color.base.promotion.alpha.60` | `--wg-color-base-promotion-alpha-60` | `rgba(255, 96, 69, 0.60)` | 促销弱化态 |
| `wg.color.base.promotion.alpha.80` | `--wg-color-base-promotion-alpha-80` | `rgba(255, 96, 69, 0.80)` | 促销 hover / 弱化强调 |
| `wg.color.base.static.black` | `--wg-color-base-static-black` | `#000000` | 极少数纯黑场景，默认不建议直接使用 |
| `wg.color.base.static.white` | `--wg-color-base-static-white` | `#FFFFFF` | 纯白背景、反白文字 |
| `wg.color.base.success.500` | `--wg-color-base-success-500` | `#03C160` | 成功状态主色 |
| `wg.color.base.success.alpha.10` | `--wg-color-base-success-alpha-10` | `rgba(3, 193, 96, 0.10)` | 成功极浅背景 |
| `wg.color.base.success.alpha.20` | `--wg-color-base-success-alpha-20` | `rgba(3, 193, 96, 0.20)` | 成功浅背景 |
| `wg.color.base.success.alpha.60` | `--wg-color-base-success-alpha-60` | `rgba(3, 193, 96, 0.60)` | 成功弱化态 |
| `wg.color.base.success.alpha.80` | `--wg-color-base-success-alpha-80` | `rgba(3, 193, 96, 0.80)` | 成功强调 hover |
| `wg.color.base.warning.500` | `--wg-color-base-warning-500` | `#FA9D3B` | 警示主色 |
| `wg.color.base.warning.alpha.10` | `--wg-color-base-warning-alpha-10` | `rgba(250, 157, 59, 0.10)` | 警示极浅背景 |
| `wg.color.base.warning.alpha.20` | `--wg-color-base-warning-alpha-20` | `rgba(250, 157, 59, 0.20)` | 警示浅背景 |
| `wg.color.base.warning.alpha.60` | `--wg-color-base-warning-alpha-60` | `rgba(250, 157, 59, 0.60)` | 警示弱化态 |
| `wg.color.base.warning.alpha.80` | `--wg-color-base-warning-alpha-80` | `rgba(250, 157, 59, 0.80)` | 警示 hover / 弱化强调 |
| `wg.color.bg.active` | `--wg-color-bg-active` | `wg.color.base.neutral.200` | 选中 / pressed 背景 |
| `wg.color.bg.danger` | `--wg-color-bg-danger` | `wg.color.base.danger.alpha.10` | 危险浅背景 |
| `wg.color.bg.info` | `--wg-color-bg-info` | `wg.color.base.info.alpha.10` | 信息浅背景 |
| `wg.color.bg.inverse` | `--wg-color-bg-inverse` | `wg.color.base.neutral.900` | 深色背景 |
| `wg.color.bg.muted` | `--wg-color-bg-muted` | `wg.color.base.neutral.100` | 弱灰背景 |
| `wg.color.bg.page` | `--wg-color-bg-page` | `wg.color.base.neutral.300` | 页面默认背景 |
| `wg.color.bg.promotion` | `--wg-color-bg-promotion` | `wg.color.base.promotion.alpha.10` | 促销浅背景 |
| `wg.color.bg.subtle` | `--wg-color-bg-subtle` | `wg.color.base.neutral.50` | 极浅灰背景 |
| `wg.color.bg.success` | `--wg-color-bg-success` | `wg.color.base.success.alpha.10` | 成功浅背景 |
| `wg.color.bg.surface` | `--wg-color-bg-surface` | `wg.color.base.static.white` | 卡片、表单、列表等主要容器背景 |
| `wg.color.bg.warning` | `--wg-color-bg-warning` | `wg.color.base.warning.alpha.10` | 警示浅背景 |
| `wg.color.border.danger` | `--wg-color-border-danger` | `wg.color.base.danger.alpha.20` | 危险边框 |
| `wg.color.border.default` | `--wg-color-border-default` | `wg.color.base.neutral.alpha.08` | 默认边框 |
| `wg.color.border.focus` | `--wg-color-border-focus` | `wg.color.base.brand.500` | 聚焦边框 |
| `wg.color.border.info` | `--wg-color-border-info` | `wg.color.base.info.alpha.20` | 信息边框 |
| `wg.color.border.promotion` | `--wg-color-border-promotion` | `wg.color.base.promotion.alpha.20` | 促销边框 |
| `wg.color.border.strong` | `--wg-color-border-strong` | `wg.color.base.neutral.alpha.10` | 强边框 |
| `wg.color.border.subtle` | `--wg-color-border-subtle` | `wg.color.base.neutral.alpha.03` | 极弱边框 |
| `wg.color.border.success` | `--wg-color-border-success` | `wg.color.base.success.alpha.20` | 成功边框 |
| `wg.color.border.warning` | `--wg-color-border-warning` | `wg.color.base.warning.alpha.20` | 警示边框 |
| `wg.color.divider.default` | `--wg-color-divider-default` | `wg.color.base.neutral.alpha.08` | 默认分割线 |
| `wg.color.divider.strong` | `--wg-color-divider-strong` | `wg.color.base.neutral.alpha.10` | 强分割线 |
| `wg.color.divider.subtle` | `--wg-color-divider-subtle` | `wg.color.base.neutral.alpha.03` | 弱分割线 |
| `wg.color.feedback.toast.bg` | `--wg-color-feedback-toast-bg` | `rgba(63, 67, 71, 0.96)` | Toast 背景 |
| `wg.color.feedback.toast.text` | `--wg-color-feedback-toast-text` | `wg.color.base.static.white` | Toast 文字 |
| `wg.color.overlay.light` | `--wg-color-overlay-light` | `wg.color.base.neutral.alpha.30` | 轻遮罩 |
| `wg.color.overlay.modal` | `--wg-color-overlay-modal` | `wg.color.base.neutral.alpha.60` | 默认弹窗遮罩 |
| `wg.color.overlay.strong` | `--wg-color-overlay-strong` | `wg.color.base.neutral.alpha.80` | 强遮罩 |
| `wg.color.state.disabled.bg` | `--wg-color-state-disabled-bg` | `wg.color.base.neutral.100` | disabled 背景 |
| `wg.color.state.disabled.text` | `--wg-color-state-disabled-text` | `wg.color.base.neutral.500` | disabled 文本 |
| `wg.color.state.focus` | `--wg-color-state-focus` | `wg.color.base.brand.500` | focus 状态 |
| `wg.color.state.hover` | `--wg-color-state-hover` | `wg.color.base.neutral.alpha.03` | hover 状态 |
| `wg.color.state.pressed` | `--wg-color-state-pressed` | `wg.color.base.neutral.alpha.06` | pressed 状态 |
| `wg.color.state.selected` | `--wg-color-state-selected` | `wg.color.base.neutral.alpha.10` | selected 状态 |
| `wg.color.status.danger.bg` | `--wg-color-status-danger-bg` | `wg.color.base.danger.alpha.10` | 危险背景 |
| `wg.color.status.danger.border` | `--wg-color-status-danger-border` | `wg.color.base.danger.alpha.20` | 危险边框 |
| `wg.color.status.danger.default` | `--wg-color-status-danger-default` | `wg.color.base.danger.500` | 危险主色 |
| `wg.color.status.danger.text` | `--wg-color-status-danger-text` | `wg.color.base.danger.500` | 危险文字 |
| `wg.color.status.info.bg` | `--wg-color-status-info-bg` | `wg.color.base.info.alpha.10` | 信息背景 |
| `wg.color.status.info.border` | `--wg-color-status-info-border` | `wg.color.base.info.alpha.20` | 信息边框 |
| `wg.color.status.info.default` | `--wg-color-status-info-default` | `wg.color.base.info.500` | 信息主色 |
| `wg.color.status.info.text` | `--wg-color-status-info-text` | `wg.color.base.info.500` | 信息文字 |
| `wg.color.status.promotion.bg` | `--wg-color-status-promotion-bg` | `wg.color.base.promotion.alpha.10` | 促销背景 |
| `wg.color.status.promotion.border` | `--wg-color-status-promotion-border` | `wg.color.base.promotion.alpha.20` | 促销边框 |
| `wg.color.status.promotion.default` | `--wg-color-status-promotion-default` | `wg.color.base.promotion.500` | 促销主色 |
| `wg.color.status.promotion.text` | `--wg-color-status-promotion-text` | `wg.color.base.promotion.500` | 促销文字 |
| `wg.color.status.success.bg` | `--wg-color-status-success-bg` | `wg.color.base.success.alpha.10` | 成功背景 |
| `wg.color.status.success.border` | `--wg-color-status-success-border` | `wg.color.base.success.alpha.20` | 成功边框 |
| `wg.color.status.success.default` | `--wg-color-status-success-default` | `wg.color.base.success.500` | 成功主色 |
| `wg.color.status.success.text` | `--wg-color-status-success-text` | `wg.color.base.success.500` | 成功文字 |
| `wg.color.status.warning.bg` | `--wg-color-status-warning-bg` | `wg.color.base.warning.alpha.10` | 警示背景 |
| `wg.color.status.warning.border` | `--wg-color-status-warning-border` | `wg.color.base.warning.alpha.20` | 警示边框 |
| `wg.color.status.warning.default` | `--wg-color-status-warning-default` | `wg.color.base.warning.500` | 警示主色 |
| `wg.color.status.warning.text` | `--wg-color-status-warning-text` | `wg.color.base.warning.500` | 警示文字 |
| `wg.color.surface.active` | `--wg-color-surface-active` | `wg.color.base.neutral.200` | 选中容器 |
| `wg.color.surface.default` | `--wg-color-surface-default` | `wg.color.base.static.white` | 默认内容容器 |
| `wg.color.surface.inverse` | `--wg-color-surface-inverse` | `wg.color.base.neutral.900` | 深色容器 |
| `wg.color.surface.muted` | `--wg-color-surface-muted` | `wg.color.base.neutral.100` | 灰底容器 |
| `wg.color.surface.subtle` | `--wg-color-surface-subtle` | `wg.color.base.neutral.50` | 弱容器 |
| `wg.color.surface.toolbar.solid` | `--wg-color-surface-toolbar-solid` | `#F6F6F6` | 实底工具栏、输入法头部 |
| `wg.color.surface.toolbar.translucent` | `--wg-color-surface-toolbar-translucent` | `rgba(246, 246, 246, 0.80)` | 毛玻璃工具栏背景，必须配合 blur 使用 |
| `wg.color.text.danger` | `--wg-color-text-danger` | `wg.color.base.danger.500` | 危险 / 错误文字 |
| `wg.color.text.disabled` | `--wg-color-text-disabled` | `wg.color.base.neutral.500` | 不可用文字 |
| `wg.color.text.info` | `--wg-color-text-info` | `wg.color.base.info.500` | 信息文字 |
| `wg.color.text.inverse` | `--wg-color-text-inverse` | `wg.color.base.static.white` | 深色背景上的文字 |
| `wg.color.text.link` | `--wg-color-text-link` | `wg.color.base.link.500` | 文本链接 |
| `wg.color.text.placeholder` | `--wg-color-text-placeholder` | `wg.color.base.neutral.500` | 输入框占位文案 |
| `wg.color.text.primary` | `--wg-color-text-primary` | `wg.color.base.neutral.900` | 一级文字、主要内容、强标题 |
| `wg.color.text.promotion` | `--wg-color-text-promotion` | `wg.color.base.promotion.500` | 促销、价格、营销文字 |
| `wg.color.text.secondary` | `--wg-color-text-secondary` | `wg.color.base.neutral.700` | 二级文字、辅助信息 |
| `wg.color.text.success` | `--wg-color-text-success` | `wg.color.base.success.500` | 成功文字 |
| `wg.color.text.tertiary` | `--wg-color-text-tertiary` | `wg.color.base.neutral.600` | 三级文字、弱辅助说明 |
| `wg.color.text.warning` | `--wg-color-text-warning` | `wg.color.base.warning.500` | 警示文字 |

## Typography

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.font.family.number.decorative` | `--wg-font-family-number-decorative` | `"WegoKeyboard N9", "DIN Alternate", "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif` | 需要突出展示的数字，如金额、总价、数据指标 |
| `wg.font.family.number.fallback` | `--wg-font-family-number-fallback` | `"DIN Alternate", "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif` | 装饰数字字体不可用时的兜底字体 |
| `wg.font.family.system` | `--wg-font-family-system` | `-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Arial, sans-serif` | 系统兜底字体 |
| `wg.font.family.text` | `--wg-font-family-text` | `"PingFang SC", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif` | 中文、英文、普通数字、正文、标题、表单、列表 |
| `wg.font.lineHeight.f10` | `--wg-font-lineheight-10` | `14px` | 极弱信息、小型辅助文字 |
| `wg.font.lineHeight.f12` | `--wg-font-lineheight-12` | `18px` | 辅助说明、标签 |
| `wg.font.lineHeight.f14` | `--wg-font-lineheight-14` | `20px` | 默认正文 |
| `wg.font.lineHeight.f16` | `--wg-font-lineheight-16` | `24px` | 二级标题、重要正文 |
| `wg.font.lineHeight.f18` | `--wg-font-lineheight-18` | `26px` | 一级标题 |
| `wg.font.lineHeight.f22` | `--wg-font-lineheight-22` | `30px` | 页面级大标题 |
| `wg.font.number.nf12` | `--wg-font-number-nf12` | `12px` | 弱数字、小数部分、辅助数字 |
| `wg.font.number.nf14` | `--wg-font-number-nf14` | `14px` | 小金额、小数部分、普通数字强调 |
| `wg.font.number.nf16` | `--wg-font-number-nf16` | `16px` | 常规金额、常规数字强调 |
| `wg.font.number.nf20` | `--wg-font-number-nf20` | `20px` | 操作区金额、重要数字 |
| `wg.font.number.nf24` | `--wg-font-number-nf24` | `24px` | 数据看板、总价、强指标 |
| `wg.font.number.nf32` | `--wg-font-number-nf32` | `32px` | 超强金额、关键结果数字 |
| `wg.font.size.f10` | `--wg-font-size-10` | `10px` | 极弱信息、小型辅助文字 |
| `wg.font.size.f12` | `--wg-font-size-12` | `12px` | 辅助说明、提示、标签、弱信息 |
| `wg.font.size.f14` | `--wg-font-size-14` | `14px` | 默认正文、普通内容 |
| `wg.font.size.f16` | `--wg-font-size-16` | `16px` | 二级标题、重要正文、强信息 |
| `wg.font.size.f18` | `--wg-font-size-18` | `18px` | 一级标题、强标题 |
| `wg.font.size.f22` | `--wg-font-size-22` | `22px` | 页面级大标题、强引导标题、结果标题 |
| `wg.font.weight.medium` | `--wg-font-weight-medium` | `500` | 轻强调、重要文字 |
| `wg.font.weight.regular` | `--wg-font-weight-regular` | `400` | 正文、说明、普通信息 |
| `wg.font.weight.semibold` | `--wg-font-weight-semibold` | `600` | 标题、重要数字、关键层级 |

## Spacing

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.spacing.0` | `--wg-spacing-0` | `0px` | 无间距、紧密贴合 |
| `wg.spacing.12` | `--wg-spacing-12` | `12px` | 紧凑内容区、次级信息关系 |
| `wg.spacing.16` | `--wg-spacing-16` | `16px` | 默认内容间距、默认组间距 |
| `wg.spacing.2` | `--wg-spacing-2` | `2px` | 极小间距，仅限特殊紧密关系 |
| `wg.spacing.24` | `--wg-spacing-24` | `24px` | 清晰分隔、左右信息组间距 |
| `wg.spacing.32` | `--wg-spacing-32` | `32px` | 宽松分隔、模块间距 |
| `wg.spacing.4` | `--wg-spacing-4` | `4px` | 强关联内容、极小距离 |
| `wg.spacing.40` | `--wg-spacing-40` | `40px` | 大区块间距 |
| `wg.spacing.48` | `--wg-spacing-48` | `48px` | 页面级大分隔 |
| `wg.spacing.8` | `--wg-spacing-8` | `8px` | 同组内容、标题与内容 |

## Radius

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.radius.full` | `--wg-radius-full` | `999px` |  |
| `wg.radius.lg` | `--wg-radius-lg` | `12px` |  |
| `wg.radius.md` | `--wg-radius-md` | `8px` |  |
| `wg.radius.none` | `--wg-radius-none` | `0px` |  |
| `wg.radius.sm` | `--wg-radius-sm` | `6px` |  |
| `wg.radius.xl` | `--wg-radius-xl` | `16px` |  |
| `wg.radius.xs` | `--wg-radius-xs` | `4px` |  |

## Size & Touch

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.component.button.width.compact.max` | `--wg-component-button-width-compact-max` | `120px` | 横条容器或卡片内小按钮的最大宽度 |
| `wg.component.button.width.container.max` | `--wg-component-button-width-container-max` | `420px` | 局部容器按钮组的最大宽度 |
| `wg.component.button.width.page.paired` | `--wg-component-button-width-page-paired` | `120px` | 页面级按钮横向成对排列时的单按钮宽度 |
| `wg.component.button.width.page.single` | `--wg-component-button-width-page-single` | `180px` | 页面级单按钮或纵向按钮组的单按钮宽度 |
| `wg.size.10` | `--wg-size-10` | `10px` |  |
| `wg.size.12` | `--wg-size-12` | `12px` |  |
| `wg.size.16` | `--wg-size-16` | `16px` |  |
| `wg.size.20` | `--wg-size-20` | `20px` |  |
| `wg.size.24` | `--wg-size-24` | `24px` |  |
| `wg.size.28` | `--wg-size-28` | `28px` |  |
| `wg.size.32` | `--wg-size-32` | `32px` |  |
| `wg.size.40` | `--wg-size-40` | `40px` |  |
| `wg.size.48` | `--wg-size-48` | `48px` |  |
| `wg.size.56` | `--wg-size-56` | `56px` |  |
| `wg.size.72` | `--wg-size-72` | `72px` |  |
| `wg.touch.comfortable` | `--wg-touch-comfortable` | `48px` |  |
| `wg.touch.default` | `--wg-touch-default` | `44px` |  |
| `wg.touch.min` | `--wg-touch-min` | `40px` |  |

## Layout

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.layout.group.g1.inside` | `--wg-layout-group-g1-inside` | `0px` | 紧密分组组内间距 |
| `wg.layout.group.g1.outside` | `--wg-layout-group-g1-outside` | `16px` | 紧密分组组间间距 |
| `wg.layout.group.g2.inside` | `--wg-layout-group-g2-inside` | `8px` | 宽松分组组内间距 |
| `wg.layout.group.g2.outside` | `--wg-layout-group-g2-outside` | `32px` | 宽松分组组间间距 |
| `wg.layout.modal.height.375.full` | `--wg-layout-modal-height-375-full` | `812px` | 375 屏全屏高度 |
| `wg.layout.modal.height.375.standard` | `--wg-layout-modal-height-375-standard` | `594px` | 375 屏标准模态高度参考 |
| `wg.layout.modal.height.375.top44` | `--wg-layout-modal-height-375-top44` | `768px` | 375 屏距顶部 44px |
| `wg.layout.modal.height.375.top88` | `--wg-layout-modal-height-375-top88` | `724px` | 375 屏距顶部 88px |
| `wg.layout.modal.height.430.full` | `--wg-layout-modal-height-430-full` | `932px` | 430 屏全屏高度 |
| `wg.layout.modal.height.430.standard` | `--wg-layout-modal-height-430-standard` | `652px` | 430 屏标准模态高度参考 |
| `wg.layout.modal.height.430.top44` | `--wg-layout-modal-height-430-top44` | `888px` | 430 屏距顶部 44px |
| `wg.layout.modal.height.430.top88` | `--wg-layout-modal-height-430-top88` | `844px` | 430 屏距顶部 88px |
| `wg.layout.page.m0.margin` | `--wg-layout-page-m0-margin` | `8px` | 高密度列表、下拉列表、搜索建议、筛选面板 |
| `wg.layout.page.m1.margin` | `--wg-layout-page-m1-margin` | `0px` | 通栏页面、连续列表、沉浸式内容 |
| `wg.layout.page.m2.margin` | `--wg-layout-page-m2-margin` | `16px` | 默认业务页面、常规卡片页面 |
| `wg.layout.page.m3.margin` | `--wg-layout-page-m3-margin` | `32px` | 宽松页面、强聚焦页面、引导页 |
| `wg.layout.screen.375` | `--wg-layout-screen-375` | `375px` | 标准移动端设计参考宽度 |
| `wg.layout.screen.430` | `--wg-layout-screen-430` | `430px` | 大屏移动端设计参考宽度 |
| `wg.layout.width.375.m0` | `--wg-layout-width-375-m0` | `359px` | 8px |
| `wg.layout.width.375.m1` | `--wg-layout-width-375-m1` | `375px` | 0px |
| `wg.layout.width.375.m2` | `--wg-layout-width-375-m2` | `343px` | 16px |
| `wg.layout.width.375.m3` | `--wg-layout-width-375-m3` | `311px` | 32px |
| `wg.layout.width.430.m0` | `--wg-layout-width-430-m0` | `414px` | 8px |
| `wg.layout.width.430.m1` | `--wg-layout-width-430-m1` | `430px` | 0px |
| `wg.layout.width.430.m2` | `--wg-layout-width-430-m2` | `398px` | 16px |
| `wg.layout.width.430.m3` | `--wg-layout-width-430-m3` | `366px` | 32px |

## Elevation

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.shadow.lg` | `--wg-shadow-lg` | `0 8px 32px rgba(30, 32, 40, 0.12)` | 强浮起 |
| `wg.shadow.md` | `--wg-shadow-md` | `0 4px 16px rgba(30, 32, 40, 0.08)` | 中等浮起 |
| `wg.shadow.none` | `--wg-shadow-none` | `none` | 无阴影 |
| `wg.shadow.sm` | `--wg-shadow-sm` | `0 2px 8px rgba(30, 32, 40, 0.06)` | 轻量浮起 |
| `wg.shadow.xl` | `--wg-shadow-xl` | `0 12px 48px rgba(30, 32, 40, 0.16)` | 高层覆盖 |
| `wg.shadow.xs` | `--wg-shadow-xs` | `0 1px 4px rgba(30, 32, 40, 0.04)` | 极轻阴影 |

## Stroke

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.stroke.color.danger` | `--wg-stroke-color-danger` | `wg.color.base.danger.500` | 危险状态描边 |
| `wg.stroke.color.default` | `--wg-stroke-color-default` | `wg.color.base.neutral.alpha.08` | 默认描边、分割线 |
| `wg.stroke.color.focus` | `--wg-stroke-color-focus` | `wg.color.base.brand.500` | 聚焦描边 |
| `wg.stroke.color.strong` | `--wg-stroke-color-strong` | `wg.color.base.neutral.alpha.10` | 强描边 |
| `wg.stroke.color.subtle` | `--wg-stroke-color-subtle` | `wg.color.base.neutral.alpha.03` | 极弱描边 |
| `wg.stroke.color.success` | `--wg-stroke-color-success` | `wg.color.base.success.500` | 成功状态描边 |
| `wg.stroke.color.warning` | `--wg-stroke-color-warning` | `wg.color.base.warning.500` | 警示状态描边 |
| `wg.stroke.style.dashed` | `--wg-stroke-style-dashed` | `dashed` | 临时占位、上传、拖拽区域 |
| `wg.stroke.style.none` | `--wg-stroke-style-none` | `none` | 无描边 |
| `wg.stroke.style.solid` | `--wg-stroke-style-solid` | `solid` | 默认实线 |
| `wg.stroke.width.default` | `--wg-stroke-width-default` | `1px` | 默认描边 |
| `wg.stroke.width.hairline` | `--wg-stroke-width-hairline` | `0.5px` | 极细分割线 |
| `wg.stroke.width.icon` | `--wg-stroke-width-icon` | `1.5px` | 线性图标默认描边 |
| `wg.stroke.width.icon.strong` | `--wg-stroke-width-icon-strong` | `2.25px` | 加粗图标描边 |
| `wg.stroke.width.none` | `--wg-stroke-width-none` | `0px` | 无描边 |
| `wg.stroke.width.strong` | `--wg-stroke-width-strong` | `1.5px` | 强调描边 |

## Blur

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.blur.frosted` | `--wg-blur-frosted` | `20px` | 毛玻璃效果参考值 |
| `wg.blur.lg` | `--wg-blur-lg` | `24px` | 强模糊 |
| `wg.blur.md` | `--wg-blur-md` | `16px` | 默认模糊 |
| `wg.blur.none` | `--wg-blur-none` | `0px` | 无模糊 |
| `wg.blur.sm` | `--wg-blur-sm` | `8px` | 轻模糊 |
| `wg.blur.xl` | `--wg-blur-xl` | `32px` | 超强模糊 |
| `wg.blur.xs` | `--wg-blur-xs` | `4px` | 极轻模糊 |

## Motion

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.motion.duration.fast` | `--wg-motion-duration-fast` | `150ms` | 快速反馈 |
| `wg.motion.duration.instant` | `--wg-motion-duration-instant` | `0ms` | 无动画 |
| `wg.motion.duration.normal` | `--wg-motion-duration-normal` | `250ms` | 默认过渡 |
| `wg.motion.duration.slow` | `--wg-motion-duration-slow` | `350ms` | 较强层级变化 |
| `wg.motion.duration.xslow` | `--wg-motion-duration-xslow` | `500ms` | 特殊强调动效，谨慎使用 |
| `wg.motion.ease.emphasized` | `--wg-motion-ease-emphasized` | `cubic-bezier(0.2, 0, 0, 1)` | 强调动效 |
| `wg.motion.ease.enter` | `--wg-motion-ease-enter` | `cubic-bezier(0, 0, 0.2, 1)` | 进入动效 |
| `wg.motion.ease.exit` | `--wg-motion-ease-exit` | `cubic-bezier(0.4, 0, 1, 1)` | 退出动效 |
| `wg.motion.ease.linear` | `--wg-motion-ease-linear` | `linear` | 线性变化 |
| `wg.motion.ease.standard` | `--wg-motion-ease-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | 默认缓动 |

## Z-Index

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.zIndex.base` | `--wg-zindex-base` | `0` | 默认内容层 |
| `wg.zIndex.critical` | `--wg-zindex-critical` | `900` | 最高优先级临时层，谨慎使用 |
| `wg.zIndex.dropdown` | `--wg-zindex-dropdown` | `200` | 下拉 / 选择层 |
| `wg.zIndex.modal` | `--wg-zindex-modal` | `600` | 弹出层 |
| `wg.zIndex.overlay` | `--wg-zindex-overlay` | `500` | 遮罩层 |
| `wg.zIndex.popover` | `--wg-zindex-popover` | `300` | 浮层提示 |
| `wg.zIndex.raised` | `--wg-zindex-raised` | `10` | 轻浮起层 |
| `wg.zIndex.sticky` | `--wg-zindex-sticky` | `100` | 吸顶 / 固定层 |
| `wg.zIndex.toast` | `--wg-zindex-toast` | `400` | 全局反馈 |

## Copywriting

| Token | CSS Variable | Value / Reference | Description |
|---|---|---|---|
| `wg.copy.action.add` | — | `添加` | 添加 |
| `wg.copy.action.cancel` | — | `取消` | 取消 |
| `wg.copy.action.clear` | — | `清空` | 清空 |
| `wg.copy.action.close` | — | `关闭` | 关闭 |
| `wg.copy.action.confirm` | — | `确定` | 确认 |
| `wg.copy.action.delete` | — | `删除` | 删除 |
| `wg.copy.action.done` | — | `完成` | 完成 |
| `wg.copy.action.edit` | — | `编辑` | 编辑 |
| `wg.copy.action.refresh` | — | `刷新` | 刷新 |
| `wg.copy.action.retry` | — | `重试` | 重试 |
| `wg.copy.action.save` | — | `保存` | 保存 |
| `wg.copy.action.search` | — | `搜索` | 搜索 |
| `wg.copy.confirm.basic` | — | `确定{动作}{对象}吗？` | 基础二次确认 |
| `wg.copy.confirm.withResult` | — | `确定{动作}{对象}吗？{动作}后，将{发生结果}` | 带后果说明的二次确认 |
| `wg.copy.empty.content` | — | `暂无内容` | 通用无内容 |
| `wg.copy.empty.data` | — | `暂无数据` | 通用无数据 |
| `wg.copy.empty.list` | — | `暂无{对象}` | 列表为空 |
| `wg.copy.empty.search` | — | `无匹配的{对象}` | 搜索无结果 |
| `wg.copy.error.network` | — | `网络异常，请稍后重试` | 网络错误 |
| `wg.copy.error.permission` | — | `暂无权限` | 权限错误 |
| `wg.copy.error.server` | — | `服务异常，请稍后重试` | 服务错误 |
| `wg.copy.error.timeout` | — | `请求超时，请重试` | 请求超时 |
| `wg.copy.error.unknown` | — | `操作失败，请重试` | 未知错误 |
| `wg.copy.feedback.copied` | — | `已复制` | 复制成功 |
| `wg.copy.feedback.deleted` | — | `已删除` | 删除成功 |
| `wg.copy.feedback.failed` | — | `{对象}失败` | 通用失败反馈 |
| `wg.copy.feedback.loading` | — | `加载中` | 加载状态 |
| `wg.copy.feedback.saved` | — | `已保存` | 保存成功 |
| `wg.copy.feedback.saving` | — | `保存中` | 保存中 |
| `wg.copy.feedback.submitting` | — | `提交中` | 提交中 |
| `wg.copy.feedback.success` | — | `{对象}成功` | 通用成功反馈 |
| `wg.copy.form.invalid` | — | `{对象}格式不正确` | 格式错误 |
| `wg.copy.form.required` | — | `请输入{对象}` | 必填输入 |
| `wg.copy.form.selectRequired` | — | `请选择{对象}` | 必选选择 |
| `wg.copy.form.tooLong` | — | `{对象}过长` | 超出长度 |
| `wg.copy.form.tooShort` | — | `{对象}过短` | 长度不足 |
