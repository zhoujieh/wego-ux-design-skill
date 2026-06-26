(function () {
  'use strict';

  const $ = function (sel) { return document.querySelector(sel); };

  const phoneInput = $('#phone');
  const phoneInputWrap = $('#phoneInput');
  const phoneError = $('#phoneError');
  const codeInput = $('#code');
  const codeInputWrap = $('#codeInput');
  const codeError = $('#codeError');
  const sendCodeBtn = $('#sendCodeBtn');
  const loginBtn = $('#loginBtn');

  let countdownTimer = null;

  /* ── 手机号格式校验 ── */
  function isValidPhone(value) {
    return /^1[3-9]\d{9}$/.test(value);
  }

  /* ── 清除手机号错误 ── */
  function clearPhoneError() {
    phoneInputWrap.classList.remove('wg-input--error');
    phoneError.hidden = true;
  }

  /* ── 显示手机号错误 ── */
  function showPhoneError(msg) {
    phoneInputWrap.classList.add('wg-input--error');
    phoneError.textContent = msg;
    phoneError.hidden = false;
  }

  /* ── 清除验证码错误 ── */
  function clearCodeError() {
    codeInputWrap.classList.remove('wg-input--error');
    codeError.hidden = true;
  }

  /* ── 显示验证码错误 ── */
  function showCodeError(msg) {
    codeInputWrap.classList.add('wg-input--error');
    codeError.textContent = msg;
    codeError.hidden = false;
  }

  /* ── 手机号输入时清除错误 ── */
  phoneInput.addEventListener('input', function () {
    clearPhoneError();
  });

  /* ── 验证码输入时清除错误 ── */
  codeInput.addEventListener('input', function () {
    clearCodeError();
  });

  /* ── 发送验证码 ── */
  sendCodeBtn.addEventListener('click', function () {
    var phone = phoneInput.value.trim();
    clearPhoneError();

    if (!phone) {
      showPhoneError('请输入手机号');
      return;
    }
    if (!isValidPhone(phone)) {
      showPhoneError('手机号格式不正确');
      return;
    }

    // 模拟发送
    var seconds = 60;
    var label = sendCodeBtn.querySelector('.wg-button__label');
    sendCodeBtn.disabled = true;

    label.textContent = seconds + 's后重发';
    countdownTimer = setInterval(function () {
      seconds--;
      if (seconds <= 0) {
        clearInterval(countdownTimer);
        countdownTimer = null;
        sendCodeBtn.disabled = false;
        label.textContent = '发送验证码';
      } else {
        label.textContent = seconds + 's后重发';
      }
    }, 1000);

    // 聚焦到验证码输入框
    codeInput.focus();
  });

  /* ── 登录 ── */
  loginBtn.addEventListener('click', function () {
    var phone = phoneInput.value.trim();
    var code = codeInput.value.trim();

    clearPhoneError();
    clearCodeError();

    // 校验手机号
    if (!phone) {
      showPhoneError('请输入手机号');
      return;
    }
    if (!isValidPhone(phone)) {
      showPhoneError('手机号格式不正确');
      return;
    }

    // 校验验证码
    if (!code) {
      showCodeError('请输入验证码');
      return;
    }
    if (!/^\d{4,6}$/.test(code)) {
      showCodeError('验证码为4-6位数字');
      codeInput.value = '';
      return;
    }

    // 登录 loading
    var label = loginBtn.querySelector('.wg-button__label');
    var originalText = label.textContent;
    loginBtn.classList.add('wg-button--loading');
    loginBtn.disabled = true;
    label.textContent = '登录中...';

    // 模拟异步登录（1.5s）
    setTimeout(function () {
      var success = code === '123456';

      loginBtn.disabled = false;
      loginBtn.classList.remove('wg-button--loading');
      label.textContent = originalText;

      if (success) {
        // 登录成功 — Toast 提示后跳转
        showToast('登录成功', 1500, function () {
          window.location.href = 'album-list.html';
        });
      } else {
        // 登录失败 — 显示错误
        showCodeError('验证码错误，请重新输入');
        codeInput.value = '';
        codeInput.focus();
      }
    }, 1500);
  });

  /* ── 轻提示 Toast（临时实现，页面级结构） ── */
  function showToast(message, duration, callback) {
    var existing = document.querySelector('.login-toast');
    if (existing) existing.remove();

    var toast = document.createElement('div');
    toast.className = 'login-toast';
    toast.textContent = message;
    toast.setAttribute('role', 'status');
    document.body.appendChild(toast);

    requestAnimationFrame(function () {
      toast.classList.add('login-toast--visible');
    });

    setTimeout(function () {
      toast.classList.remove('login-toast--visible');
      setTimeout(function () {
        toast.remove();
        if (typeof callback === 'function') callback();
      }, 200);
    }, duration);
  }
})();
