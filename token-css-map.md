# Token → CSS 映射表

<!-- GENERATED FILE. DO NOT EDIT. Run: python3 scripts/generate_tokens.py -->

> Version 3.2.0  
> 唯一数据源：`02-tokens/tokens.json`。本文件由脚本生成，禁止手工修改。

## 使用方式

原型项目直接复制 `02-tokens/tokens.css` 为 `styles/tokens.css`，并通过 `<link>` 引入。下面内容仅用于查阅映射。

```css
@font-face {
  font-family: "WegoKeyboard N9";
  src: url("resources/fonts/WegoKeyboardN9-Regular.otf") format("opentype");
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: "WegoKeyboard N9";
  src: url("resources/fonts/WegoKeyboardN9-Medium.otf") format("opentype");
  font-weight: 500;
  font-style: normal;
}

@font-face {
  font-family: "WegoKeyboard N9";
  src: url("resources/fonts/WegoKeyboardN9-Bold.otf") format("opentype");
  font-weight: 600;
  font-style: normal;
}

:root {
  /* Color */
  --wg-color-action-danger-default: var(--wg-color-base-danger-500);
  --wg-color-action-danger-hover: var(--wg-color-base-danger-alpha-80);
  --wg-color-action-danger-pressed: var(--wg-color-base-danger-alpha-80);
  --wg-color-action-link-default: var(--wg-color-base-link-500);
  --wg-color-action-link-disabled: var(--wg-color-base-link-alpha-20);
  --wg-color-action-link-hover: var(--wg-color-base-link-hover);
  --wg-color-action-link-pressed: var(--wg-color-base-link-pressed);
  --wg-color-action-primary-default: var(--wg-color-base-brand-500);
  --wg-color-action-primary-disabled: var(--wg-color-base-brand-alpha-60);
  --wg-color-action-primary-hover: var(--wg-color-base-brand-alpha-80);
  --wg-color-action-primary-pressed: var(--wg-color-base-brand-alpha-80);
  --wg-color-action-secondary-default: var(--wg-color-base-neutral-alpha-03);
  --wg-color-action-secondary-hover: var(--wg-color-base-neutral-alpha-06);
  --wg-color-action-secondary-pressed: var(--wg-color-base-neutral-alpha-10);
  --wg-color-base-accent-gold-500: #C79A56;
  --wg-color-base-accent-green-500: #00C777;
  --wg-color-base-accent-purple-500: #6367F0;
  --wg-color-base-accent-yellow-500: #FFC300;
  --wg-color-base-accent-yellow-alpha-10: rgba(255, 195, 0, 0.10);
  --wg-color-base-accent-yellow-alpha-20: rgba(255, 195, 0, 0.20);
  --wg-color-base-accent-yellow-alpha-60: rgba(255, 195, 0, 0.60);
  --wg-color-base-accent-yellow-alpha-80: rgba(255, 195, 0, 0.80);
  --wg-color-base-brand-500: #03C160;
  --wg-color-base-brand-alpha-10: rgba(3, 193, 96, 0.10);
  --wg-color-base-brand-alpha-20: rgba(3, 193, 96, 0.20);
  --wg-color-base-brand-alpha-60: rgba(3, 193, 96, 0.60);
  --wg-color-base-brand-alpha-80: rgba(3, 193, 96, 0.80);
  --wg-color-base-danger-500: #FA5051;
  --wg-color-base-danger-alpha-10: rgba(250, 80, 81, 0.10);
  --wg-color-base-danger-alpha-20: rgba(250, 80, 81, 0.20);
  --wg-color-base-danger-alpha-60: rgba(250, 80, 81, 0.60);
  --wg-color-base-danger-alpha-80: rgba(250, 80, 81, 0.80);
  --wg-color-base-info-500: #208BF1;
  --wg-color-base-info-alpha-10: rgba(32, 139, 241, 0.10);
  --wg-color-base-info-alpha-20: rgba(32, 139, 241, 0.20);
  --wg-color-base-info-alpha-60: rgba(32, 139, 241, 0.60);
  --wg-color-base-info-alpha-80: rgba(32, 139, 241, 0.80);
  --wg-color-base-link-500: #285B9A;
  --wg-color-base-link-alpha-20: rgba(40, 91, 154, 0.20);
  --wg-color-base-link-hover: #285B9A;
  --wg-color-base-link-pressed: #285B9A;
  --wg-color-base-neutral-100: #F2F3F6;
  --wg-color-base-neutral-200: #E9EAEF;
  --wg-color-base-neutral-300: #EDEDED;
  --wg-color-base-neutral-50: #F8F9FA;
  --wg-color-base-neutral-500: #B7BEC5;
  --wg-color-base-neutral-600: #9097A3;
  --wg-color-base-neutral-700: #6E7382;
  --wg-color-base-neutral-800: #3F434C;
  --wg-color-base-neutral-900: #1E2028;
  --wg-color-base-neutral-alpha-03: rgba(32, 47, 100, 0.03);
  --wg-color-base-neutral-alpha-06: rgba(32, 47, 100, 0.06);
  --wg-color-base-neutral-alpha-08: rgba(32, 47, 100, 0.08);
  --wg-color-base-neutral-alpha-10: rgba(32, 47, 100, 0.10);
  --wg-color-base-neutral-alpha-30: rgba(30, 32, 40, 0.30);
  --wg-color-base-neutral-alpha-60: rgba(30, 32, 40, 0.60);
  --wg-color-base-neutral-alpha-80: rgba(30, 32, 40, 0.80);
  --wg-color-base-promotion-500: #FF6045;
  --wg-color-base-promotion-alpha-10: rgba(255, 96, 69, 0.10);
  --wg-color-base-promotion-alpha-20: rgba(255, 96, 69, 0.20);
  --wg-color-base-promotion-alpha-60: rgba(255, 96, 69, 0.60);
  --wg-color-base-promotion-alpha-80: rgba(255, 96, 69, 0.80);
  --wg-color-base-static-black: #000000;
  --wg-color-base-static-white: #FFFFFF;
  --wg-color-base-success-500: #03C160;
  --wg-color-base-success-alpha-10: rgba(3, 193, 96, 0.10);
  --wg-color-base-success-alpha-20: rgba(3, 193, 96, 0.20);
  --wg-color-base-success-alpha-60: rgba(3, 193, 96, 0.60);
  --wg-color-base-success-alpha-80: rgba(3, 193, 96, 0.80);
  --wg-color-base-warning-500: #FA9D3B;
  --wg-color-base-warning-alpha-10: rgba(250, 157, 59, 0.10);
  --wg-color-base-warning-alpha-20: rgba(250, 157, 59, 0.20);
  --wg-color-base-warning-alpha-60: rgba(250, 157, 59, 0.60);
  --wg-color-base-warning-alpha-80: rgba(250, 157, 59, 0.80);
  --wg-color-bg-active: var(--wg-color-base-neutral-200);
  --wg-color-bg-danger: var(--wg-color-base-danger-alpha-10);
  --wg-color-bg-info: var(--wg-color-base-info-alpha-10);
  --wg-color-bg-inverse: var(--wg-color-base-neutral-900);
  --wg-color-bg-muted: var(--wg-color-base-neutral-100);
  --wg-color-bg-page: var(--wg-color-base-neutral-300);
  --wg-color-bg-promotion: var(--wg-color-base-promotion-alpha-10);
  --wg-color-bg-subtle: var(--wg-color-base-neutral-50);
  --wg-color-bg-success: var(--wg-color-base-success-alpha-10);
  --wg-color-bg-surface: var(--wg-color-base-static-white);
  --wg-color-bg-warning: var(--wg-color-base-warning-alpha-10);
  --wg-color-border-danger: var(--wg-color-base-danger-alpha-20);
  --wg-color-border-default: var(--wg-color-base-neutral-alpha-08);
  --wg-color-border-focus: var(--wg-color-base-brand-500);
  --wg-color-border-info: var(--wg-color-base-info-alpha-20);
  --wg-color-border-promotion: var(--wg-color-base-promotion-alpha-20);
  --wg-color-border-strong: var(--wg-color-base-neutral-alpha-10);
  --wg-color-border-subtle: var(--wg-color-base-neutral-alpha-03);
  --wg-color-border-success: var(--wg-color-base-success-alpha-20);
  --wg-color-border-warning: var(--wg-color-base-warning-alpha-20);
  --wg-color-divider-default: var(--wg-color-base-neutral-alpha-08);
  --wg-color-divider-strong: var(--wg-color-base-neutral-alpha-10);
  --wg-color-divider-subtle: var(--wg-color-base-neutral-alpha-03);
  --wg-color-feedback-toast-bg: rgba(63, 67, 71, 0.96);
  --wg-color-feedback-toast-text: var(--wg-color-base-static-white);
  --wg-color-overlay-light: var(--wg-color-base-neutral-alpha-30);
  --wg-color-overlay-modal: var(--wg-color-base-neutral-alpha-60);
  --wg-color-overlay-strong: var(--wg-color-base-neutral-alpha-80);
  --wg-color-state-disabled-bg: var(--wg-color-base-neutral-100);
  --wg-color-state-disabled-text: var(--wg-color-base-neutral-500);
  --wg-color-state-focus: var(--wg-color-base-brand-500);
  --wg-color-state-hover: var(--wg-color-base-neutral-alpha-03);
  --wg-color-state-pressed: var(--wg-color-base-neutral-alpha-06);
  --wg-color-state-selected: var(--wg-color-base-neutral-alpha-10);
  --wg-color-status-danger-bg: var(--wg-color-base-danger-alpha-10);
  --wg-color-status-danger-border: var(--wg-color-base-danger-alpha-20);
  --wg-color-status-danger-default: var(--wg-color-base-danger-500);
  --wg-color-status-danger-text: var(--wg-color-base-danger-500);
  --wg-color-status-info-bg: var(--wg-color-base-info-alpha-10);
  --wg-color-status-info-border: var(--wg-color-base-info-alpha-20);
  --wg-color-status-info-default: var(--wg-color-base-info-500);
  --wg-color-status-info-text: var(--wg-color-base-info-500);
  --wg-color-status-promotion-bg: var(--wg-color-base-promotion-alpha-10);
  --wg-color-status-promotion-border: var(--wg-color-base-promotion-alpha-20);
  --wg-color-status-promotion-default: var(--wg-color-base-promotion-500);
  --wg-color-status-promotion-text: var(--wg-color-base-promotion-500);
  --wg-color-status-success-bg: var(--wg-color-base-success-alpha-10);
  --wg-color-status-success-border: var(--wg-color-base-success-alpha-20);
  --wg-color-status-success-default: var(--wg-color-base-success-500);
  --wg-color-status-success-text: var(--wg-color-base-success-500);
  --wg-color-status-warning-bg: var(--wg-color-base-warning-alpha-10);
  --wg-color-status-warning-border: var(--wg-color-base-warning-alpha-20);
  --wg-color-status-warning-default: var(--wg-color-base-warning-500);
  --wg-color-status-warning-text: var(--wg-color-base-warning-500);
  --wg-color-surface-active: var(--wg-color-base-neutral-200);
  --wg-color-surface-default: var(--wg-color-base-static-white);
  --wg-color-surface-inverse: var(--wg-color-base-neutral-900);
  --wg-color-surface-muted: var(--wg-color-base-neutral-100);
  --wg-color-surface-subtle: var(--wg-color-base-neutral-50);
  --wg-color-surface-toolbar-solid: #F6F6F6;
  --wg-color-surface-toolbar-translucent: rgba(246, 246, 246, 0.80);
  --wg-color-text-danger: var(--wg-color-base-danger-500);
  --wg-color-text-disabled: var(--wg-color-base-neutral-500);
  --wg-color-text-info: var(--wg-color-base-info-500);
  --wg-color-text-inverse: var(--wg-color-base-static-white);
  --wg-color-text-link: var(--wg-color-base-link-500);
  --wg-color-text-placeholder: var(--wg-color-base-neutral-500);
  --wg-color-text-primary: var(--wg-color-base-neutral-900);
  --wg-color-text-promotion: var(--wg-color-base-promotion-500);
  --wg-color-text-secondary: var(--wg-color-base-neutral-700);
  --wg-color-text-success: var(--wg-color-base-success-500);
  --wg-color-text-tertiary: var(--wg-color-base-neutral-600);
  --wg-color-text-warning: var(--wg-color-base-warning-500);

  /* Typography */
  --wg-font-family-number-decorative: "WegoKeyboard N9", "DIN Alternate", "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif;
  --wg-font-family-number-fallback: "DIN Alternate", "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif;
  --wg-font-family-system: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  --wg-font-family-text: "PingFang SC", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
  --wg-font-lineheight-10: 14px;
  --wg-font-lineheight-12: 18px;
  --wg-font-lineheight-14: 20px;
  --wg-font-lineheight-16: 24px;
  --wg-font-lineheight-18: 26px;
  --wg-font-lineheight-22: 30px;
  --wg-font-number-nf12: 12px;
  --wg-font-number-nf14: 14px;
  --wg-font-number-nf16: 16px;
  --wg-font-number-nf20: 20px;
  --wg-font-number-nf24: 24px;
  --wg-font-number-nf32: 32px;
  --wg-font-size-10: 10px;
  --wg-font-size-12: 12px;
  --wg-font-size-14: 14px;
  --wg-font-size-16: 16px;
  --wg-font-size-18: 18px;
  --wg-font-size-22: 22px;
  --wg-font-weight-medium: 500;
  --wg-font-weight-regular: 400;
  --wg-font-weight-semibold: 600;

  /* Spacing */
  --wg-spacing-0: 0px;
  --wg-spacing-12: 12px;
  --wg-spacing-16: 16px;
  --wg-spacing-2: 2px;
  --wg-spacing-24: 24px;
  --wg-spacing-32: 32px;
  --wg-spacing-4: 4px;
  --wg-spacing-40: 40px;
  --wg-spacing-48: 48px;
  --wg-spacing-8: 8px;

  /* Radius */
  --wg-radius-full: 999px;
  --wg-radius-lg: 12px;
  --wg-radius-md: 8px;
  --wg-radius-none: 0px;
  --wg-radius-sm: 6px;
  --wg-radius-xl: 16px;
  --wg-radius-xs: 4px;

  /* Size & Touch */
  --wg-component-button-width-compact-max: 120px;
  --wg-component-button-width-container-max: 420px;
  --wg-component-button-width-page-paired: 120px;
  --wg-component-button-width-page-single: 180px;
  --wg-component-dialog-button-gap: 16px;
  --wg-component-dialog-button-height: 48px;
  --wg-component-dialog-padding-block: 24px;
  --wg-component-dialog-padding-inline: 20px;
  --wg-component-dialog-width: 300px;
  --wg-size-10: 10px;
  --wg-size-12: 12px;
  --wg-size-16: 16px;
  --wg-size-20: 20px;
  --wg-size-24: 24px;
  --wg-size-28: 28px;
  --wg-size-32: 32px;
  --wg-size-40: 40px;
  --wg-size-48: 48px;
  --wg-size-56: 56px;
  --wg-size-72: 72px;
  --wg-touch-comfortable: 48px;
  --wg-touch-default: 44px;
  --wg-touch-min: 40px;

  /* Layout */
  --wg-layout-group-g1-inside: 0px;
  --wg-layout-group-g1-outside: 16px;
  --wg-layout-group-g2-inside: 8px;
  --wg-layout-group-g2-outside: 32px;
  --wg-layout-modal-height-375-full: 812px;
  --wg-layout-modal-height-375-standard: 594px;
  --wg-layout-modal-height-375-top44: 768px;
  --wg-layout-modal-height-375-top88: 724px;
  --wg-layout-modal-height-430-full: 932px;
  --wg-layout-modal-height-430-standard: 652px;
  --wg-layout-modal-height-430-top44: 888px;
  --wg-layout-modal-height-430-top88: 844px;
  --wg-layout-page-m0-margin: 8px;
  --wg-layout-page-m1-margin: 0px;
  --wg-layout-page-m2-margin: 16px;
  --wg-layout-page-m3-margin: 32px;
  --wg-layout-screen-375: 375px;
  --wg-layout-screen-430: 430px;
  --wg-layout-width-375-m0: 359px;
  --wg-layout-width-375-m1: 375px;
  --wg-layout-width-375-m2: 343px;
  --wg-layout-width-375-m3: 311px;
  --wg-layout-width-430-m0: 414px;
  --wg-layout-width-430-m1: 430px;
  --wg-layout-width-430-m2: 398px;
  --wg-layout-width-430-m3: 366px;

  /* Elevation */
  --wg-shadow-lg: 0 8px 32px rgba(30, 32, 40, 0.12);
  --wg-shadow-md: 0 4px 16px rgba(30, 32, 40, 0.08);
  --wg-shadow-none: none;
  --wg-shadow-sm: 0 2px 8px rgba(30, 32, 40, 0.06);
  --wg-shadow-xl: 0 12px 48px rgba(30, 32, 40, 0.16);
  --wg-shadow-xs: 0 1px 4px rgba(30, 32, 40, 0.04);

  /* Stroke */
  --wg-stroke-color-danger: var(--wg-color-base-danger-500);
  --wg-stroke-color-default: var(--wg-color-base-neutral-alpha-08);
  --wg-stroke-color-focus: var(--wg-color-base-brand-500);
  --wg-stroke-color-strong: var(--wg-color-base-neutral-alpha-10);
  --wg-stroke-color-subtle: var(--wg-color-base-neutral-alpha-03);
  --wg-stroke-color-success: var(--wg-color-base-success-500);
  --wg-stroke-color-warning: var(--wg-color-base-warning-500);
  --wg-stroke-style-dashed: dashed;
  --wg-stroke-style-none: none;
  --wg-stroke-style-solid: solid;
  --wg-stroke-width-default: 1px;
  --wg-stroke-width-hairline: 0.5px;
  --wg-stroke-width-icon: 1.5px;
  --wg-stroke-width-icon-strong: 2.25px;
  --wg-stroke-width-none: 0px;
  --wg-stroke-width-strong: 1.5px;

  /* Blur */
  --wg-blur-frosted: 20px;
  --wg-blur-lg: 24px;
  --wg-blur-md: 16px;
  --wg-blur-none: 0px;
  --wg-blur-sm: 8px;
  --wg-blur-xl: 32px;
  --wg-blur-xs: 4px;

  /* Motion */
  --wg-motion-duration-fast: 150ms;
  --wg-motion-duration-instant: 0ms;
  --wg-motion-duration-normal: 250ms;
  --wg-motion-duration-slow: 350ms;
  --wg-motion-duration-xslow: 500ms;
  --wg-motion-ease-emphasized: cubic-bezier(0.2, 0, 0, 1);
  --wg-motion-ease-enter: cubic-bezier(0, 0, 0.2, 1);
  --wg-motion-ease-exit: cubic-bezier(0.4, 0, 1, 1);
  --wg-motion-ease-linear: linear;
  --wg-motion-ease-standard: cubic-bezier(0.4, 0, 0.2, 1);

  /* Z-Index */
  --wg-zindex-base: 0;
  --wg-zindex-critical: 900;
  --wg-zindex-dropdown: 200;
  --wg-zindex-modal: 600;
  --wg-zindex-overlay: 500;
  --wg-zindex-popover: 300;
  --wg-zindex-raised: 10;
  --wg-zindex-sticky: 100;
  --wg-zindex-toast: 400;
}

body,
h1,
h2,
h3,
h4,
h5,
h6,
p,
ul,
ol,
dl,
figure,
blockquote,
hr,
fieldset,
pre {
  margin: var(--wg-spacing-0);
}

ul, ol {
  padding: var(--wg-spacing-0);
  list-style: none;
}

body {
  font-family: var(--wg-font-family-text);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  color: var(--wg-color-text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

## 引用示例

```css
.example {
  color: var(--wg-color-text-primary);
  background: var(--wg-color-bg-surface);
  padding: var(--wg-spacing-16);
  border-radius: var(--wg-radius-md);
  font-size: var(--wg-font-size-14);
}
```

Copywriting Token 不生成 CSS 变量，请从 `02-tokens/token-reference.md` 读取对应文案。
