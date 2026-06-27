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
