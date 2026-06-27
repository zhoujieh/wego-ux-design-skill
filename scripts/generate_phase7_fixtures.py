#!/usr/bin/env python3
"""Generate deterministic Phase 7 regression fixtures.

The fixtures simulate the outputs expected from the wego-ux-design skill. CI
validates these static outputs instead of calling an LLM.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "generated"
TOKENS = ROOT / "wego-ux-design" / "design-library" / "tokens.css"


COMPONENTS_CSS = """
.wg-button-group {
  display: flex;
  gap: var(--wg-spacing-8);
}

.wg-button-group--page {
  justify-content: center;
}

.wg-button {
  --button-visual-height: var(--wg-size-40);
  appearance: none;
  display: inline-flex;
  min-inline-size: 0;
  min-block-size: max(var(--wg-touch-min), var(--button-visual-height));
  padding: var(--wg-spacing-0);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: var(--wg-color-transparent);
  color: inherit;
  cursor: pointer;
}

.wg-button__surface {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  inline-size: 100%;
  block-size: var(--button-visual-height);
  padding-inline: var(--wg-spacing-16);
  overflow: hidden;
  border-radius: var(--wg-radius-sm);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
  transition: background-color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard), color var(--wg-motion-duration-fast) var(--wg-motion-ease-standard), opacity var(--wg-motion-duration-fast) var(--wg-motion-ease-standard);
}

.wg-button__label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.wg-button--page {
  --button-visual-height: var(--wg-size-48);
  inline-size: 100%;
}

.wg-button--container {
  --button-visual-height: var(--wg-size-40);
  inline-size: 100%;
}

.wg-button--compact {
  --button-visual-height: var(--wg-size-32);
  inline-size: fit-content;
}

.wg-button--strong .wg-button__surface {
  background-color: var(--wg-color-action-primary-default);
  color: var(--wg-color-text-inverse);
}

.wg-button--medium .wg-button__surface {
  background-color: var(--wg-color-action-secondary-default);
  color: var(--wg-color-action-primary-default);
}

.wg-button--weak .wg-button__surface {
  background-color: var(--wg-color-action-secondary-default);
  color: var(--wg-color-text-primary);
}

.wg-button--strong:not(:disabled):hover .wg-button__surface {
  background-color: var(--wg-color-action-primary-hover);
}

.wg-button--strong:not(:disabled):active .wg-button__surface {
  background-color: var(--wg-color-action-primary-pressed);
}

.wg-button:disabled {
  cursor: not-allowed;
}

.wg-button:disabled .wg-button__surface {
  background-color: var(--wg-color-state-disabled-bg);
  color: var(--wg-color-state-disabled-text);
}

.wg-navbar {
  position: sticky;
  inset-block-start: var(--wg-spacing-0);
  z-index: var(--wg-zindex-sticky);
  display: flex;
  align-items: center;
  min-block-size: var(--wg-touch-default);
  padding-inline: var(--wg-spacing-16);
  background: var(--wg-color-bg-page);
  border-block-end: var(--wg-stroke-width-hairline) var(--wg-stroke-style-solid) var(--wg-color-divider-default);
}

.wg-navbar__left,
.wg-navbar__actions {
  display: flex;
  align-items: center;
  flex: 1 1 0;
  gap: var(--wg-spacing-8);
}

.wg-navbar__actions {
  justify-content: flex-end;
}

.wg-navbar__center {
  display: flex;
  align-items: center;
  justify-content: center;
  min-inline-size: 0;
}

.wg-navbar__title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: var(--wg-font-size-18);
  line-height: var(--wg-font-lineheight-18);
  font-weight: var(--wg-font-weight-semibold);
  color: var(--wg-color-text-primary);
}

.wg-navbar__left-btn,
.wg-navbar__action {
  appearance: none;
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: var(--wg-color-transparent);
  color: var(--wg-color-action-primary-default);
  font: inherit;
  cursor: pointer;
}

.wg-navbar__search-box {
  display: flex;
  align-items: center;
  inline-size: 100%;
  gap: var(--wg-spacing-8);
  min-block-size: var(--wg-size-32);
  padding-inline: var(--wg-spacing-12);
  border-radius: var(--wg-radius-md);
  background: var(--wg-color-bg-subtle);
}

.wg-navbar__search-input {
  min-inline-size: 0;
  inline-size: 100%;
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: var(--wg-color-transparent);
  color: var(--wg-color-text-primary);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
}

.wg-form-group,
.wg-input {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-8);
}

.wg-form {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-4);
  padding-block: var(--wg-spacing-12);
  border-block-end: var(--wg-stroke-width-hairline) var(--wg-stroke-style-solid) var(--wg-color-divider-default);
}

.wg-form__body {
  display: flex;
  align-items: center;
  gap: var(--wg-spacing-16);
}

.wg-form__label {
  flex: 0 0 auto;
  color: var(--wg-color-text-primary);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
}

.wg-form__action {
  display: flex;
  align-items: center;
  flex: 1 1 0;
  min-inline-size: 0;
}

.wg-form__input,
.wg-input__field {
  appearance: none;
  inline-size: 100%;
  min-inline-size: 0;
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: var(--wg-color-transparent);
  color: var(--wg-color-text-primary);
  font-family: var(--wg-font-family-text);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  outline: none;
}

.wg-form__hint,
.wg-input__error {
  color: var(--wg-color-status-danger-text);
  font-size: var(--wg-font-size-12);
  line-height: var(--wg-font-lineheight-12);
}

.wg-form--error .wg-form__input,
.wg-input--error .wg-input__field {
  color: var(--wg-color-status-danger-text);
}

.wg-dialog-overlay {
  position: fixed;
  inset: var(--wg-spacing-0);
  z-index: var(--wg-zindex-modal);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--wg-spacing-24);
  background: var(--wg-color-overlay-light);
  opacity: 1;
  pointer-events: auto;
  transition: opacity var(--wg-motion-duration-normal) var(--wg-motion-ease-standard);
}

.wg-dialog-overlay[data-state="closed"] {
  opacity: 0;
  pointer-events: none;
}

.wg-dialog {
  inline-size: min(100%, var(--wg-component-dialog-width));
  overflow: hidden;
  border-radius: var(--wg-radius-lg);
  background: var(--wg-color-bg-surface);
  box-shadow: var(--wg-shadow-xl);
}

.wg-dialog__content {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-12);
  padding: var(--wg-component-dialog-padding-block) var(--wg-component-dialog-padding-inline);
}

.wg-dialog__title {
  color: var(--wg-color-text-primary);
  font-size: var(--wg-font-size-18);
  line-height: var(--wg-font-lineheight-18);
  font-weight: var(--wg-font-weight-semibold);
}

.wg-dialog__description {
  color: var(--wg-color-text-secondary);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
}

.wg-dialog__buttons {
  display: grid;
  border-block-start: var(--wg-stroke-width-hairline) var(--wg-stroke-style-solid) var(--wg-color-divider-default);
}

.wg-dialog__buttons--dual {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.wg-dialog__button {
  appearance: none;
  min-block-size: var(--wg-component-dialog-button-height);
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  background: var(--wg-color-transparent);
  color: var(--wg-color-action-link-default);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
  cursor: pointer;
}

.wg-dialog__button--danger {
  color: var(--wg-color-action-danger-default);
}

.wg-tabs {
  display: flex;
  gap: var(--wg-spacing-8);
  padding: var(--wg-spacing-8);
  background: var(--wg-color-bg-surface);
}

.wg-tab {
  appearance: none;
  flex: 1 1 0;
  border: var(--wg-stroke-width-none) var(--wg-stroke-style-none);
  border-radius: var(--wg-radius-sm);
  background: var(--wg-color-transparent);
  color: var(--wg-color-text-secondary);
  padding: var(--wg-spacing-8) var(--wg-spacing-12);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
  cursor: pointer;
}

.wg-tab--active {
  background: var(--wg-color-state-selected);
  color: var(--wg-color-action-primary-default);
  font-weight: var(--wg-font-weight-medium);
}

.wg-cell {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--wg-spacing-16);
  padding: var(--wg-spacing-16);
  border-block-end: var(--wg-stroke-width-hairline) var(--wg-stroke-style-solid) var(--wg-color-divider-default);
  background: var(--wg-color-bg-surface);
}

.wg-cell__title {
  color: var(--wg-color-text-primary);
  font-size: var(--wg-font-size-16);
  line-height: var(--wg-font-lineheight-16);
  font-weight: var(--wg-font-weight-medium);
}

.wg-cell__meta {
  color: var(--wg-color-text-secondary);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
}

.wg-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--wg-spacing-16);
  padding: var(--wg-spacing-32) var(--wg-spacing-16);
  text-align: center;
}

.wg-result__icon {
  inline-size: var(--wg-size-64);
  block-size: var(--wg-size-64);
  display: grid;
  place-items: center;
  border-radius: var(--wg-radius-full);
  background: var(--wg-color-bg-success);
  color: var(--wg-color-status-success-text);
  font-size: var(--wg-font-size-22);
  font-weight: var(--wg-font-weight-semibold);
}

.wg-result--error .wg-result__icon {
  background: var(--wg-color-bg-danger);
  color: var(--wg-color-status-danger-text);
}

.wg-result__title {
  color: var(--wg-color-text-primary);
  font-size: var(--wg-font-size-18);
  line-height: var(--wg-font-lineheight-18);
  font-weight: var(--wg-font-weight-semibold);
}

.wg-result__description {
  color: var(--wg-color-text-secondary);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
}

.wg-toast {
  position: fixed;
  inset-inline: var(--wg-spacing-16);
  inset-block-end: var(--wg-spacing-24);
  z-index: var(--wg-zindex-toast);
  display: none;
  justify-content: center;
  pointer-events: none;
}

.wg-toast--visible {
  display: flex;
}

.wg-toast__surface {
  max-inline-size: 100%;
  padding: var(--wg-spacing-12) var(--wg-spacing-16);
  border-radius: var(--wg-radius-md);
  background: var(--wg-color-bg-toast);
  color: var(--wg-color-feedback-toast-text);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
}

.wg-loading {
  display: inline-flex;
  align-items: center;
  gap: var(--wg-spacing-8);
  color: var(--wg-color-text-secondary);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
}
""".strip()


APP_CSS = """
.app-shell {
  min-block-size: 100vh;
  min-block-size: 100dvh;
  background: var(--wg-color-bg-page);
  color: var(--wg-color-text-primary);
}

.page {
  inline-size: 100%;
  max-inline-size: var(--wg-layout-page-max-width);
  min-block-size: 100vh;
  min-block-size: 100dvh;
  margin-inline: auto;
  background: var(--wg-color-bg-surface);
}

.content {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-16);
  padding: var(--wg-spacing-16);
}

.section {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-12);
}

.card {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-12);
  padding: var(--wg-spacing-16);
  border-radius: var(--wg-radius-md);
  background: var(--wg-color-bg-surface);
  box-shadow: var(--wg-shadow-sm);
}

.muted-card {
  background: var(--wg-color-bg-subtle);
  box-shadow: var(--wg-shadow-none);
}

.toolbar {
  display: flex;
  align-items: center;
  gap: var(--wg-spacing-8);
}

.toolbar > * {
  flex: 1 1 0;
}

.headline {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-4);
}

.title {
  margin: var(--wg-spacing-0);
  color: var(--wg-color-text-primary);
  font-size: var(--wg-font-size-22);
  line-height: var(--wg-font-lineheight-22);
  font-weight: var(--wg-font-weight-semibold);
}

.subtitle,
.helper {
  margin: var(--wg-spacing-0);
  color: var(--wg-color-text-secondary);
  font-size: var(--wg-font-size-14);
  line-height: var(--wg-font-lineheight-14);
}

.stack {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-12);
}

.grid {
  display: grid;
  gap: var(--wg-spacing-12);
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--wg-spacing-12);
}

.badge {
  display: inline-flex;
  align-items: center;
  inline-size: fit-content;
  padding: var(--wg-spacing-4) var(--wg-spacing-8);
  border-radius: var(--wg-radius-full);
  background: var(--wg-color-bg-success);
  color: var(--wg-color-status-success-text);
  font-size: var(--wg-font-size-12);
  line-height: var(--wg-font-lineheight-12);
}

.badge--danger {
  background: var(--wg-color-bg-danger);
  color: var(--wg-color-status-danger-text);
}

.upload-panel,
.state-panel {
  display: flex;
  flex-direction: column;
  gap: var(--wg-spacing-8);
  padding: var(--wg-spacing-16);
  border-radius: var(--wg-radius-md);
  background: var(--wg-color-bg-subtle);
}

.view {
  display: none;
  flex-direction: column;
  gap: var(--wg-spacing-16);
}

.view--active {
  display: flex;
}

[hidden] {
  display: none;
}
""".strip()


APP_JS = """
const app = document.querySelector('[data-app]');
const toast = document.querySelector('[data-toast]');

function showToast(message) {
  if (!toast) return;
  toast.querySelector('[data-toast-message]').textContent = message;
  toast.classList.add('wg-toast--visible');
  toast.dataset.state = 'visible';
  window.setTimeout(() => {
    toast.classList.remove('wg-toast--visible');
    toast.dataset.state = 'hidden';
  }, 700);
}

function setLoading(button, loading) {
  if (!button) return;
  button.disabled = loading;
  button.dataset.loading = loading ? 'true' : 'false';
  button.setAttribute('aria-busy', loading ? 'true' : 'false');
}

function validateForm(scope) {
  let valid = true;
  scope.querySelectorAll('[data-required]').forEach((field) => {
    const wrapper = field.closest('.wg-form, .wg-input') || field.parentElement;
    const message = wrapper.querySelector('[data-error]');
    const empty = !field.value.trim();
    wrapper.classList.toggle('wg-form--error', empty);
    wrapper.classList.toggle('wg-input--error', empty);
    if (message) message.hidden = !empty;
    if (empty) valid = false;
  });
  return valid;
}

function recoverFromError(scope) {
  scope.querySelectorAll('.wg-form--error, .wg-input--error').forEach((node) => {
    node.classList.remove('wg-form--error', 'wg-input--error');
  });
  scope.querySelectorAll('[data-error]').forEach((node) => {
    node.hidden = true;
  });
  scope.dataset.recovered = 'true';
}

function switchView(target) {
  document.querySelectorAll('[data-view]').forEach((view) => {
    view.classList.toggle('view--active', view.dataset.view === target);
  });
  app.dataset.view = target;
}

document.querySelectorAll('[data-required]').forEach((field) => {
  field.addEventListener('input', () => recoverFromError(document));
});

document.querySelectorAll('[data-action]').forEach((control) => {
  control.addEventListener('click', () => {
    const action = control.dataset.action;
    const dialog = document.querySelector('[data-dialog]');
    if (action === 'submit') {
      if (!validateForm(document)) {
        showToast('请补全必填信息后重新提交');
        return;
      }
      setLoading(control, true);
      window.setTimeout(() => {
        setLoading(control, false);
        showToast('提交成功');
        app.dataset.status = 'success';
      }, 300);
    }
    if (action === 'open-dialog' && dialog) {
      dialog.dataset.state = 'open';
      dialog.removeAttribute('hidden');
    }
    if (action === 'close-dialog' && dialog) {
      dialog.dataset.state = 'closed';
      dialog.setAttribute('hidden', '');
    }
    if (action === 'confirm-delete') {
      setLoading(control, true);
      window.setTimeout(() => {
        setLoading(control, false);
        document.querySelector('[data-removable]')?.remove();
        showToast('删除成功，可重试其他操作');
        if (dialog) {
          dialog.dataset.state = 'closed';
          dialog.setAttribute('hidden', '');
        }
      }, 300);
    }
    if (action === 'retry' || action === 'reset') {
      recoverFromError(document);
      showToast('已恢复，可重新操作');
    }
    if (action === 'search') {
      app.dataset.status = 'loading';
      window.setTimeout(() => {
        app.dataset.status = 'empty';
        showToast('未找到结果，已展示推荐操作');
      }, 300);
    }
    if (action === 'navigate-detail') switchView('detail');
    if (action === 'back-home') switchView('home');
    if (action === 'toggle-result') {
      document.querySelectorAll('[data-result]').forEach((node) => node.toggleAttribute('hidden'));
    }
  });
});
""".strip()


def button(label: str, *, tone: str = "strong", scope: str = "page", action: str = "submit") -> str:
    return (
        f'<button class="wg-button wg-button--{scope} wg-button--{tone}" type="button" data-action="{action}">'
        f'<span class="wg-button__surface"><span class="wg-button__label">{label}</span></span>'
        "</button>"
    )


def navbar(title: str, action: str = "") -> str:
    return f"""
<header class="wg-navbar wg-navbar--standard wg-navbar--bg-default wg-navbar--divider">
  <div class="wg-navbar__left">
    <button class="wg-navbar__left-btn" type="button" data-action="back-home" aria-label="返回">返回</button>
  </div>
  <div class="wg-navbar__center"><span class="wg-navbar__title">{title}</span></div>
  <div class="wg-navbar__actions">{action}</div>
</header>
""".strip()


def form_row(label: str, placeholder: str, name: str, *, required: bool = True) -> str:
    req = " data-required" if required else ""
    return f"""
<div class="wg-form wg-form--horizontal">
  <div class="wg-form__body">
    <div class="wg-form__label">{label}</div>
    <div class="wg-form__action"><input class="wg-form__input" name="{name}" placeholder="{placeholder}"{req}></div>
  </div>
  <div class="wg-form__hint" data-error hidden>{label}不能为空</div>
</div>
""".strip()


def dialog(title: str, description: str, confirm: str = "确认") -> str:
    return f"""
<div class="wg-dialog-overlay" data-dialog data-state="closed" hidden>
  <div class="wg-dialog wg-dialog--text" role="dialog" aria-modal="true">
    <div class="wg-dialog__content">
      <div class="wg-dialog__header"><span class="wg-dialog__title">{title}</span></div>
      <p class="wg-dialog__description">{description}</p>
    </div>
    <div class="wg-dialog__action">
      <div class="wg-dialog__buttons wg-dialog__buttons--dual">
        <button class="wg-dialog__button wg-dialog__button--dismiss" type="button" data-action="close-dialog">取消</button>
        <button class="wg-dialog__button wg-dialog__button--confirm wg-dialog__button--danger" type="button" data-action="confirm-delete">{confirm}</button>
      </div>
    </div>
  </div>
</div>
""".strip()


def result(title: str, description: str, *, error: bool = False) -> str:
    modifier = " wg-result--error" if error else ""
    mark = "!" if error else "✓"
    return f"""
<section class="wg-result{modifier}" data-result>
  <div class="wg-result__icon">{mark}</div>
  <h2 class="wg-result__title">{title}</h2>
  <p class="wg-result__description">{description}</p>
</section>
""".strip()


PROJECTS = {
    "主按钮": {
        "title": "strong 主按钮",
        "body": f"""
<main class="content">
  <section class="card">
    <div class="headline">
      <h1 class="title">主操作按钮</h1>
      <p class="subtitle">用于保存、提交、确认等页面级主任务。</p>
    </div>
    <div class="wg-button-group wg-button-group--page">{button("保存设置")}</div>
  </section>
</main>
""",
    },
    "弹窗": {
        "title": "带标题和操作的 dialog",
        "body": f"""
<main class="content">
  <section class="card">
    <div class="headline">
      <h1 class="title">确认操作</h1>
      <p class="subtitle">点击按钮打开包含标题、正文和双操作区的对话框。</p>
    </div>
    {button("打开确认弹窗", action="open-dialog")}
  </section>
  {dialog("开启自动上新", "开启后系统将按所选规则同步商品，请确认当前设置。", "开启")}
</main>
""",
    },
    "店铺设置": {
        "title": "微购店铺设置",
        "body": f"""
{navbar("店铺设置")}
<main class="content">
  <section class="card">
    <div class="headline">
      <h1 class="title">基础设置</h1>
      <p class="subtitle">维护店铺展示信息和联系资料。</p>
    </div>
    <div class="wg-form-group">
      {form_row("店铺名称", "请输入店铺名称", "shop")}
      {form_row("联系电话", "请输入手机号", "phone")}
      {form_row("发货地址", "请输入详细地址", "address")}
    </div>
  </section>
  <div class="wg-button-group wg-button-group--page">{button("保存设置")}</div>
</main>
""",
    },
    "登录": {
        "title": "微购登录",
        "body": f"""
<main class="content">
  <section class="card">
    <div class="headline">
      <h1 class="title">登录微购后台</h1>
      <p class="subtitle">使用手机号和验证码完成首次登录。</p>
    </div>
    <div class="wg-form-group">
      {form_row("手机号", "请输入手机号", "mobile")}
      {form_row("验证码", "请输入验证码", "code")}
    </div>
    {button("登录")}
  </section>
  {result("登录成功", "已进入微购后台，可以开始管理商品。")}
</main>
""",
    },
    "商品发布": {
        "title": "商品发布",
        "body": f"""
{navbar("商品发布", '<button class="wg-navbar__action" type="button" data-action="open-dialog">草稿</button>')}
<main class="content">
  <section class="card">
    <div class="headline"><h1 class="title">基本信息</h1><p class="subtitle">按商品发布流程补全必要字段。</p></div>
    <div class="wg-form-group">
      {form_row("商品名称", "请输入商品名称", "title")}
      {form_row("价格", "请输入销售价", "price")}
      {form_row("库存", "请输入库存数量", "stock")}
    </div>
  </section>
  <section class="upload-panel">
    <span class="badge">图片上传成功</span>
    <p class="helper">上传失败时可重新选择图片并重试。</p>
  </section>
  <div class="toolbar">{button("保存草稿", tone="weak", action="open-dialog")}{button("发布商品")}</div>
  {dialog("保存草稿", "当前内容会保存为草稿，稍后可继续编辑。", "保存")}
</main>
""",
    },
    "订单列表": {
        "title": "订单列表",
        "body": f"""
{navbar("我的订单")}
<main class="content">
  <nav class="wg-tabs" aria-label="订单状态">
    <button class="wg-tab wg-tab--active" type="button">全部</button>
    <button class="wg-tab" type="button">待付款</button>
    <button class="wg-tab" type="button">待发货</button>
  </nav>
  <section class="state-panel"><span class="wg-loading">加载中</span><p class="helper">下拉刷新和分页加载会展示处理中状态。</p></section>
  <section class="stack">
    <article class="wg-cell"><div><div class="wg-cell__title">订单 2026062701</div><div class="wg-cell__meta">待发货 · 2 件商品</div></div>{button("处理", scope="compact")}</article>
    <article class="wg-cell"><div><div class="wg-cell__title">订单 2026062702</div><div class="wg-cell__meta">网络错误后可重试</div></div>{button("重试", scope="compact", action="retry")}</article>
  </section>
</main>
""",
    },
    "搜索空状态": {
        "title": "搜索空状态",
        "body": f"""
{navbar("搜索商品")}
<main class="content">
  <section class="card">
    <div class="wg-navbar__search-box">
      <input class="wg-navbar__search-input" type="search" value="蓝色毛呢外套" data-required>
      <button class="wg-navbar__action" type="button" data-action="search">搜索</button>
    </div>
  </section>
  {result("暂无搜索结果", "换个关键词试试，或直接发布新品。", error=True)}
  {button("发布新品", action="navigate-detail")}
</main>
""",
    },
    "删除确认": {
        "title": "删除确认",
        "body": f"""
{navbar("客户标签")}
<main class="content">
  <section class="stack">
    <article class="wg-cell" data-removable><div><div class="wg-cell__title">高意向客户</div><div class="wg-cell__meta">128 人</div></div>{button("删除", scope="compact", tone="weak", action="open-dialog")}</article>
    <article class="wg-cell"><div><div class="wg-cell__title">复购客户</div><div class="wg-cell__meta">76 人</div></div>{button("管理", scope="compact")}</article>
  </section>
  {dialog("确认删除", "删除后标签不会再出现在客户筛选中，失败后可重试。", "删除")}
</main>
""",
    },
    "表单校验失败": {
        "title": "表单校验失败",
        "body": f"""
{navbar("创建客户")}
<main class="content">
  <section class="card">
    <div class="headline"><h1 class="title">客户资料</h1><p class="subtitle">逐项校验姓名、手机号和地址。</p></div>
    <div class="wg-form-group">
      {form_row("姓名", "请输入客户姓名", "name")}
      {form_row("手机号", "请输入手机号", "mobile")}
      {form_row("地址", "请输入收货地址", "address")}
    </div>
    {button("提交资料")}
    {button("重置错误", tone="weak", action="reset")}
  </section>
</main>
""",
    },
    "结果页": {
        "title": "支付结果",
        "body": f"""
<main class="content">
  {result("支付成功", "订单已生成，买家会收到支付通知。")}
  {result("支付失败", "网络异常导致支付失败，请重试支付。", error=True)}
  <div class="toolbar">{button("查看订单", tone="medium", action="navigate-detail")}{button("重试支付", action="retry")}</div>
  <button class="wg-button wg-button--page wg-button--weak" type="button" data-action="toggle-result"><span class="wg-button__surface"><span class="wg-button__label">切换结果</span></span></button>
</main>
""",
    },
    "多页导航": {
        "title": "多页导航",
        "body": f"""
<main class="content">
  <section class="view view--active" data-view="home">
    {navbar("商品列表")}
    <article class="wg-cell"><div><div class="wg-cell__title">夏季套装</div><div class="wg-cell__meta">点击进入详情页</div></div>{button("查看", scope="compact", action="navigate-detail")}</article>
  </section>
  <section class="view" data-view="detail">
    {navbar("商品详情")}
    <section class="card"><h1 class="title">夏季套装</h1><p class="subtitle">详情页返回会切回首页，并保留页面状态。</p>{button("返回首页", tone="weak", action="back-home")}</section>
  </section>
</main>
""",
    },
}


def render_page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="styles/tokens.css">
  <link rel="stylesheet" href="styles/components.css">
  <link rel="stylesheet" href="styles/app.css">
</head>
<body>
  <div class="app-shell" data-app data-status="initial">
    <div class="page">
      {body.strip()}
    </div>
  </div>
  <div class="wg-toast" data-toast data-state="hidden">
    <div class="wg-toast__surface" data-toast-message>操作完成</div>
  </div>
  <script src="scripts/app.js"></script>
</body>
</html>
"""


def write_project(dirname: str, title: str, body: str) -> None:
    project = FIXTURES / dirname
    (project / "styles").mkdir(parents=True, exist_ok=True)
    (project / "scripts").mkdir(parents=True, exist_ok=True)
    (project / "index.html").write_text(render_page(title, body), encoding="utf-8")
    (project / "styles" / "tokens.css").write_text(TOKENS.read_text(encoding="utf-8"), encoding="utf-8")
    (project / "styles" / "components.css").write_text(COMPONENTS_CSS + "\n", encoding="utf-8")
    (project / "styles" / "app.css").write_text(APP_CSS + "\n", encoding="utf-8")
    (project / "scripts" / "app.js").write_text(APP_JS + "\n", encoding="utf-8")


def main() -> int:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    for dirname, spec in PROJECTS.items():
        write_project(dirname, spec["title"], spec["body"])
        print(f"generated {dirname}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
