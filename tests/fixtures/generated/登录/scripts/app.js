/* ═══════════════════════════════════════════════════════════════════════════
   App JS — 登录页交互逻辑
   驱动状态链：初始 → 输入校验 → 提交中 → 成功/失败 → 恢复
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── DOM 引用 ── */
  const loginPage = document.getElementById('loginPage');
  const loginSuccess = document.getElementById('loginSuccess');
  const loginForm = document.getElementById('loginForm');
  const phoneInput = document.querySelector('#phoneInput .wg-input__field');
  const phoneInputWrapper = document.getElementById('phoneInput');
  const codeInput = document.querySelector('#codeInput .wg-input__field');
  const codeInputWrapper = document.getElementById('codeInput');
  const getCodeBtn = document.getElementById('getCodeBtn');
  const loginBtn = document.getElementById('loginBtn');
  const loginBtnLabel = loginBtn.querySelector('.wg-button__label');
  const enterBtn = document.getElementById('enterBtn');
  const toastContainer = document.getElementById('toastContainer');
  const toastMessage = document.getElementById('toastMessage');

  /* ── 状态 ── */
  let codeTimer = null;
  let countdownSeconds = 0;
  let toastTimeout = null;
  let isSubmitting = false;

  /* ── 手机号校验 ── */
  function validatePhone(value) {
    if (!value || value.trim() === '') {
      return '请输入手机号';
    }
    if (!/^1[3-9]\d{9}$/.test(value.trim())) {
      return '手机号格式不正确';
    }
    return null;
  }

  /* ── 验证码校验 ── */
  function validateCode(value) {
    if (!value || value.trim() === '') {
      return '请输入验证码';
    }
    return null;
  }

  /* ── 设置输入框错误 ── */
  function setInputError(wrapper, message) {
    // 清除已有错误
    clearInputError(wrapper);
    wrapper.classList.add('wg-input--error');
    const errorEl = document.createElement('p');
    errorEl.className = 'wg-input__error';
    errorEl.textContent = message;
    wrapper.appendChild(errorEl);
  }

  /* ── 清除输入框错误 ── */
  function clearInputError(wrapper) {
    wrapper.classList.remove('wg-input--error');
    const errorEl = wrapper.querySelector('.wg-input__error');
    if (errorEl) {
      errorEl.remove();
    }
  }

  /* ── Toast ── */
  function showToast(message, duration) {
    duration = duration || 2000;
    if (toastTimeout) {
      clearTimeout(toastTimeout);
    }
    toastMessage.textContent = message;
    toastContainer.setAttribute('data-state', 'visible');
    toastTimeout = setTimeout(function () {
      hideToast();
    }, duration);
  }

  function hideToast() {
    toastContainer.setAttribute('data-state', 'hidden');
  }

  /* ── 按钮加载态 ── */
  function setButtonLoading(button, labelEl, loading) {
    if (loading) {
      button.disabled = true;
      labelEl.textContent = '登录中...';
    } else {
      button.disabled = false;
      labelEl.textContent = '登录';
    }
  }

  /* ── 获取验证码倒计时 ── */
  function startCodeCountdown() {
    countdownSeconds = 60;
    getCodeBtn.disabled = true;
    updateCountdownLabel();

    codeTimer = setInterval(function () {
      countdownSeconds--;
      if (countdownSeconds <= 0) {
        clearInterval(codeTimer);
        codeTimer = null;
        getCodeBtn.disabled = false;
        getCodeBtn.textContent = '重新获取';
        return;
      }
      updateCountdownLabel();
    }, 1000);
  }

  function updateCountdownLabel() {
    getCodeBtn.textContent = countdownSeconds + 's后重发';
  }

  /* ── 获取验证码 ── */
  function handleGetCode() {
    // 先校验手机号
    var phoneVal = phoneInput.value;
    var phoneError = validatePhone(phoneVal);
    if (phoneError) {
      setInputError(phoneInputWrapper, phoneError);
      phoneInput.focus();
      return;
    }
    clearInputError(phoneInputWrapper);

    // 模拟发送验证码
    showToast('验证码已发送', 2000);
    startCodeCountdown();
    codeInput.focus();
  }

  /* ── 显示成功页 ── */
  function showSuccessPage() {
    loginPage.style.display = 'none';
    loginSuccess.classList.add('login-success--visible');
  }

  /* ── 返回登录页（用于后续扩展） ── */
  function showLoginPage() {
    loginSuccess.classList.remove('login-success--visible');
    loginPage.style.display = '';
  }

  /* ── 表单提交 ── */
  function handleSubmit(event) {
    event.preventDefault();

    if (isSubmitting) {
      return;
    }

    // 清除所有错误
    clearInputError(phoneInputWrapper);
    clearInputError(codeInputWrapper);

    var phoneVal = phoneInput.value;
    var codeVal = codeInput.value;
    var hasError = false;

    // 校验手机号
    var phoneError = validatePhone(phoneVal);
    if (phoneError) {
      setInputError(phoneInputWrapper, phoneError);
      hasError = true;
    }

    // 校验验证码
    var codeError = validateCode(codeVal);
    if (codeError) {
      setInputError(codeInputWrapper, codeError);
      hasError = true;
    }

    if (hasError) {
      return;
    }

    // 进入提交状态
    isSubmitting = true;
    setButtonLoading(loginBtn, loginBtnLabel, true);

    // 模拟登录请求
    simulateLogin(phoneVal.trim(), codeVal.trim());
  }

  /* ── 模拟登录 ── */
  function simulateLogin(phone, code) {
    // 模拟网络延迟
    setTimeout(function () {
      // 模拟：验证码 "123456" 为成功，其他为失败
      var isSuccess = code === '123456';

      if (isSuccess) {
        handleLoginSuccess();
      } else {
        handleLoginFailure();
      }
    }, 1500);
  }

  /* ── 登录成功 ── */
  function handleLoginSuccess() {
    isSubmitting = false;
    setButtonLoading(loginBtn, loginBtnLabel, false);
    showToast('登录成功', 1500);

    // 短暂延迟后切换到成功页
    setTimeout(function () {
      showSuccessPage();
    }, 800);
  }

  /* ── 登录失败 ── */
  function handleLoginFailure() {
    isSubmitting = false;
    setButtonLoading(loginBtn, loginBtnLabel, false);
    showToast('验证码错误，请重试', 2500);
    // 清空验证码，聚焦以便重试
    codeInput.value = '';
    codeInput.focus();
  }

  /* ── 事件绑定 ── */
  getCodeBtn.addEventListener('click', handleGetCode);

  loginForm.addEventListener('submit', handleSubmit);

  // 输入时清除对应错误
  phoneInput.addEventListener('input', function () {
    clearInputError(phoneInputWrapper);
  });

  codeInput.addEventListener('input', function () {
    clearInputError(codeInputWrapper);
  });

  // 进入后台按钮
  enterBtn.addEventListener('click', function () {
    showToast('已进入后台', 2000);
  });

})();
