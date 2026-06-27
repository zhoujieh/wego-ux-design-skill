(function () {
  'use strict';

  /* ── State ── */
  var state = {
    visibility: 'public',
    selectedGroups: [],
    unit: '件',
    minQty: 1,
    pickMethod: 'single'
  };

  /* ── DOM refs ── */
  var fanGroups = document.getElementById('fan-groups');
  var inputUnit = document.getElementById('input-unit');
  var inputQty = document.getElementById('input-qty');
  var qtyUnit = document.getElementById('qty-unit');

  /* ── Radio: visible range ── */
  function selectVisibility(value) {
    state.visibility = value;

    var showFanGroups = value === 'partial' || value === 'exclude';
    if (showFanGroups) {
      fanGroups.classList.remove('hidden');
    } else {
      fanGroups.classList.add('hidden');
    }

    var cells = document.querySelectorAll('#group-visibility [data-radio]');
    cells.forEach(function (cell) {
      var radio = cell.querySelector('.wg-radio');
      var radioVal = radio.getAttribute('data-value');
      if (radioVal === value) {
        radio.classList.add('wg-radio--checked');
        radio.setAttribute('aria-checked', 'true');
      } else {
        radio.classList.remove('wg-radio--checked');
        radio.setAttribute('aria-checked', 'false');
      }
    });
  }

  document.querySelectorAll('#group-visibility [data-radio]').forEach(function (cell) {
    cell.addEventListener('click', function () {
      var radio = this.querySelector('.wg-radio');
      selectVisibility(radio.getAttribute('data-value'));
    });
  });

  /* ── Checkbox: fan groups ── */
  function toggleGroup(value) {
    var idx = state.selectedGroups.indexOf(value);
    if (idx > -1) {
      state.selectedGroups.splice(idx, 1);
    } else {
      state.selectedGroups.push(value);
    }
  }

  document.querySelectorAll('#fan-groups [data-checkbox]').forEach(function (cell) {
    cell.addEventListener('click', function () {
      var checkbox = this.querySelector('.wg-checkbox');
      var val = checkbox.getAttribute('data-value');
      toggleGroup(val);

      if (state.selectedGroups.indexOf(val) > -1) {
        checkbox.classList.add('wg-checkbox--checked');
        checkbox.setAttribute('aria-checked', 'true');
      } else {
        checkbox.classList.remove('wg-checkbox--checked');
        checkbox.setAttribute('aria-checked', 'false');
      }
    });
  });

  /* ── Radio: pick method ── */
  function selectPickMethod(value) {
    state.pickMethod = value;

    var cells = document.querySelectorAll('[data-radio-pick]');
    cells.forEach(function (cell) {
      var radio = cell.querySelector('.wg-radio');
      var radioVal = radio.getAttribute('data-value');
      if (radioVal === value) {
        radio.classList.add('wg-radio--checked');
        radio.setAttribute('aria-checked', 'true');
      } else {
        radio.classList.remove('wg-radio--checked');
        radio.setAttribute('aria-checked', 'false');
      }
    });
  }

  document.querySelectorAll('[data-radio-pick]').forEach(function (cell) {
    cell.addEventListener('click', function () {
      var radio = this.querySelector('.wg-radio');
      selectPickMethod(radio.getAttribute('data-value'));
    });
  });

  /* ── Unit input ── */
  inputUnit.addEventListener('input', function () {
    var val = this.value.trim();
    state.unit = val || '件';
    if (val.length > 0) {
      qtyUnit.textContent = val;
      qtyUnit.classList.remove('hidden');
    } else {
      qtyUnit.textContent = '件';
      qtyUnit.classList.remove('hidden');
    }
  });

  inputUnit.addEventListener('blur', function () {
    var val = this.value.trim();
    state.unit = val || '件';
    if (val.length > 0) {
      qtyUnit.textContent = val;
      qtyUnit.classList.remove('hidden');
    } else {
      qtyUnit.textContent = '件';
    }
  });

  /* ── Quantity stepper ── */
  function updateQty(val) {
    var n = parseInt(val, 10);
    if (isNaN(n) || n < 1) n = 1;
    if (n > 99999) n = 99999;
    state.minQty = n;
    inputQty.value = n;
  }

  inputQty.addEventListener('input', function () {
    updateQty(this.value);
  });

  inputQty.addEventListener('blur', function () {
    updateQty(this.value);
  });

  document.querySelector('#stepper-qty .stepper-btn--minus').addEventListener('click', function () {
    updateQty(state.minQty - 1);
  });

  document.querySelector('#stepper-qty .stepper-btn--plus').addEventListener('click', function () {
    updateQty(state.minQty + 1);
  });

  /* ── Save ── */
  function getConfig() {
    return {
      visibility: state.visibility,
      selectedGroups: state.selectedGroups.slice(),
      unit: state.unit,
      minQty: state.minQty,
      pickMethod: state.pickMethod
    };
  }

  function saveConfig() {
    var btn = document.getElementById('btn-save');
    var label = btn.querySelector('.wg-button__label');
    var original = label.textContent;

    btn.disabled = true;
    label.textContent = '保存中...';

    setTimeout(function () {
      console.log('Config saved:', getConfig());
      label.textContent = '已保存';

      setTimeout(function () {
        label.textContent = original;
        btn.disabled = false;
      }, 1500);
    }, 400);
  }

  document.getElementById('btn-save').addEventListener('click', saveConfig);

  /* ── Cancel ── */
  function cancel() {
    if (history.length > 1) {
      history.back();
    } else {
      alert('已取消');
    }
  }

  document.getElementById('btn-cancel').addEventListener('click', cancel);

  /* ── 全店混批 link ── */
  document.getElementById('link-mix-rule').addEventListener('click', function (e) {
    e.preventDefault();
    alert('跳转至全店混批规则设置页面');
  });

  /* ── Init ── */
  qtyUnit.classList.remove('hidden');
  inputQty.addEventListener('focus', function () {
    this.select();
  });
})();
