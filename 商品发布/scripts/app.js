/**
 * 商品发布页 — 交互逻辑
 * 状态链：初始 → 填写 → 校验 → 提交中 → 成功/失败 → 恢复
 */

// ============================================================
// 表单状态
// ============================================================
const formState = {
  title: '',
  images: [],
  match: '',
  tags: [],
  watermark: '',
  category: '',
  visibility: 'public',
  source: '',
  sku: '',
  shortName: '',
  specs: '',
  price: '',
  wholesalePrice: '',
  bulkPrice: '',
  dropshipPrice: '',
  procurementPrice: '',
  distribution: '',
  promotion: '',
  stock: '',
  weight: '',
  shippingTemplate: '',
  remark: '',
};

// 记录表单是否被修改过（用于离开确认）
let isDirty = false;

// ============================================================
// Toast 工具
// ============================================================
let toastTimer = null;

function showToast(message, type) {
  const container = document.getElementById('toastContainer');
  const icon = document.getElementById('toastIcon');
  const msg = document.getElementById('toastMessage');

  if (toastTimer) clearTimeout(toastTimer);

  icon.className = 'wg-toast__icon';
  if (type === 'success') {
    icon.classList.add('wg-toast__icon--success', 'wg-toast__icon--show');
  } else if (type === 'error') {
    icon.classList.add('wg-toast__icon--error', 'wg-toast__icon--show');
  }

  msg.textContent = message;
  container.setAttribute('data-state', 'visible');

  toastTimer = setTimeout(() => {
    container.setAttribute('data-state', 'hidden');
  }, 3000);
}

// ============================================================
// Dialog 工具
// ============================================================
function showDialog(id) {
  const overlay = document.getElementById(id);
  overlay.setAttribute('data-state', 'open');
}

function hideDialog(id) {
  const overlay = document.getElementById(id);
  overlay.setAttribute('data-state', 'closed');
}

// ============================================================
// Loading 工具
// ============================================================
function showLoading() {
  document.getElementById('loadingModal').setAttribute('data-state', 'visible');
}

function hideLoading() {
  document.getElementById('loadingModal').setAttribute('data-state', 'hidden');
}

// ============================================================
// ActionSheet 工具
// ============================================================
let currentActionSheet = null; // { field, callback }

function showActionSheet(field, options, selectedValue, callback) {
  const sheet = document.getElementById('actionSheet');
  const header = document.getElementById('actionSheetHeader');
  const headerText = document.getElementById('actionSheetHeaderText');
  const list = document.getElementById('actionSheetList');
  const panel = document.getElementById('actionSheetPanel');

  // 设置头部
  const headers = {
    match: '选择搭配',
    watermark: '选择水印',
    category: '选择产品分类',
    visibility: '谁可以看',
    source: '选择来源',
    shippingTemplate: '选择运费模板',
  };
  if (headers[field]) {
    header.style.display = 'flex';
    headerText.textContent = headers[field];
  } else {
    header.style.display = 'none';
  }

  // 构建选项列表
  list.innerHTML = '';
  options.forEach((opt) => {
    const btn = document.createElement('button');
    btn.className = 'wg-actionsheet__item';
    btn.type = 'button';
    btn.setAttribute('aria-selected', opt.value === selectedValue ? 'true' : 'false');

    const title = document.createElement('span');
    title.className = 'wg-actionsheet__item-title';
    title.textContent = opt.label;

    const check = document.createElement('i');
    check.className = 'wg-actionsheet__item-check';

    btn.appendChild(title);
    btn.appendChild(check);

    btn.addEventListener('click', () => {
      currentActionSheet = null;
      hideActionSheet();
      if (callback) callback(opt.value, opt.label);
    });

    list.appendChild(btn);
  });

  // 设置面板模式为 select
  panel.className = 'wg-actionsheet__panel wg-actionsheet__panel--select';

  currentActionSheet = { field, callback };
  sheet.style.display = 'flex';
}

function hideActionSheet() {
  const sheet = document.getElementById('actionSheet');
  sheet.style.display = 'none';
}

// ActionSheet 遮罩点击关闭
document.getElementById('actionSheet').querySelector('.wg-actionsheet__overlay').addEventListener('click', hideActionSheet);

// ActionSheet 取消按钮
document.getElementById('actionSheetCancel').addEventListener('click', hideActionSheet);

// ============================================================
// 选择字段数据配置
// ============================================================
const selectOptions = {
  match: [
    { value: 'none', label: '无' },
    { value: 'shoes', label: '鞋子' },
    { value: 'bag', label: '包包' },
    { value: 'accessory', label: '配饰' },
  ],
  watermark: [
    { value: 'none', label: '无水印' },
    { value: 'center', label: '居中水印' },
    { value: 'tile', label: '平铺水印' },
    { value: 'corner', label: '角落水印' },
  ],
  category: [
    { value: 'clothing', label: '服装' },
    { value: 'shoes', label: '鞋靴' },
    { value: 'bags', label: '箱包' },
    { value: 'accessories', label: '配饰' },
    { value: 'beauty', label: '美妆' },
    { value: 'home', label: '家居' },
    { value: 'digital', label: '数码' },
  ],
  visibility: [
    { value: 'public', label: '公开：所有粉丝可见' },
    { value: 'vip', label: '会员可见' },
    { value: 'private', label: '仅自己可见' },
  ],
  source: [
    { value: '', label: '无' },
    { value: 'factory', label: '工厂直供' },
    { value: 'agent', label: '代理货源' },
    { value: 'self', label: '自主生产' },
  ],
  shippingTemplate: [
    { value: 'default', label: '运费模板' },
    { value: 'free', label: '包邮' },
    { value: 'by-weight', label: '按重量计费' },
    { value: 'by-distance', label: '按距离计费' },
  ],
};

// ============================================================
// 绑定选择字段点击事件
// ============================================================
function bindSelectField(formEl, field) {
  const action = formEl.querySelector('.wg-form__action--select');
  if (!action) return;

  const display = formEl.querySelector('.wg-form__display');

  action.addEventListener('click', () => {
    const currentValue = formState[field] || '';
    showActionSheet(field, selectOptions[field], currentValue, (value, label) => {
      formState[field] = value;
      if (display) {
        display.textContent = label;
        display.classList.remove('wg-form__display--placeholder');
      }
      markDirty();
    });
  });
}

// 绑定选择类型表单字段
document.querySelectorAll('[data-field]').forEach((el) => {
  const field = el.getAttribute('data-field');
  if (selectOptions[field]) {
    bindSelectField(el, field);
  }
});

// ============================================================
// 标签多选
// ============================================================
document.getElementById('tagGroup').addEventListener('click', (e) => {
  const tag = e.target.closest('.wg-tag');
  if (!tag || tag.classList.contains('wg-tag--20')) return;

  const isSelected = tag.getAttribute('aria-pressed') === 'true';
  if (isSelected) {
    tag.classList.remove('wg-tag--selected');
    tag.setAttribute('aria-pressed', 'false');
  } else {
    tag.classList.add('wg-tag--selected');
    tag.setAttribute('aria-pressed', 'true');
  }

  // 更新 formState
  const allTags = document.querySelectorAll('#tagGroup .wg-tag');
  formState.tags = [];
  allTags.forEach((t) => {
    if (t.getAttribute('aria-pressed') === 'true') {
      formState.tags.push(t.getAttribute('data-value'));
    }
  });

  markDirty();
});

// ============================================================
// 图片上传
// ============================================================
const MAX_IMAGES = 9;
const imageGrid = document.getElementById('imageGrid');
const btnAddImage = document.getElementById('btnAddImage');
const fileInput = document.getElementById('fileInput');
const imageUploadHint = document.querySelector('[data-field="images"] .wg-form__hint--count');

btnAddImage.addEventListener('click', () => {
  if (formState.images.length >= MAX_IMAGES) return;
  fileInput.click();
});

fileInput.addEventListener('change', (e) => {
  const files = Array.from(e.target.files);
  const remaining = MAX_IMAGES - formState.images.length;
  const toAdd = files.slice(0, remaining);

  toAdd.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (ev) => {
      formState.images.push(ev.target.result);
      renderImages();
      markDirty();
    };
    reader.readAsDataURL(file);
  });

  fileInput.value = '';
});

function renderImages() {
  // 清除现有缩略图（保留添加按钮）
  const items = imageGrid.querySelectorAll('.image-upload__item');
  items.forEach((item) => item.remove());

  // 渲染缩略图
  formState.images.forEach((src, index) => {
    const item = document.createElement('div');
    item.className = 'image-upload__item';

    const img = document.createElement('img');
    img.src = src;
    img.alt = `商品图片 ${index + 1}`;

    const removeBtn = document.createElement('button');
    removeBtn.className = 'image-upload__remove';
    removeBtn.type = 'button';
    removeBtn.setAttribute('aria-label', '移除图片');
    removeBtn.innerHTML = '&#x2715;';
    removeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      formState.images.splice(index, 1);
      renderImages();
      markDirty();
    });

    item.appendChild(img);
    item.appendChild(removeBtn);
    imageGrid.insertBefore(item, btnAddImage);
  });

  // 控制添加按钮显隐
  if (formState.images.length >= MAX_IMAGES) {
    btnAddImage.classList.add('image-upload__add--hidden');
  } else {
    btnAddImage.classList.remove('image-upload__add--hidden');
  }

  // 更新数量提示
  if (imageUploadHint) {
    imageUploadHint.textContent = `${formState.images.length}/${MAX_IMAGES} 张`;
    imageUploadHint.style.display = 'block';
  }
}

// ============================================================
// 表单输入监听
// ============================================================

// 文本输入框
document.querySelectorAll('.wg-form__input').forEach((input) => {
  const formEl = input.closest('[data-field]');
  if (!formEl) return;

  const field = formEl.getAttribute('data-field');

  input.addEventListener('input', () => {
    formState[field] = input.value;

    // 金额字段：更新 ¥ 符号颜色
    const currency = formEl.querySelector('.wg-form__currency');
    if (currency) {
      if (input.value.trim()) {
        currency.classList.add('wg-form__currency--filled');
      } else {
        currency.classList.remove('wg-form__currency--filled');
      }
    }

    // 标题字数统计
    if (field === 'title') {
      const hint = formEl.querySelector('.wg-form__hint--count');
      if (hint) {
        hint.textContent = `${input.value.length}/60`;
        hint.style.display = 'block';
      }
    }

    markDirty();
  });
});

// ============================================================
// Cell 跳转字段
// ============================================================
document.querySelectorAll('.wg-cell[data-field]').forEach((cell) => {
  cell.addEventListener('click', () => {
    const field = cell.getAttribute('data-field');
    const display = cell.querySelector('.wg-cell__action-text');

    // 模拟跳转：弹出简单的输入/选择交互
    // 对于规格、帮卖分销、添加活动 — 触发简单设置
    // 对于商品备注 — 触发输入
    if (field === 'remark') {
      const note = prompt('请输入商品备注：', formState.remark || '');
      if (note !== null) {
        formState.remark = note;
        if (display) {
          display.textContent = note || '写备注';
        }
        markDirty();
      }
    } else if (field === 'specs') {
      const specs = prompt('请输入规格（如：S/M/L）：', formState.specs || '');
      if (specs !== null) {
        formState.specs = specs;
        if (display) {
          display.textContent = specs || '无';
        }
        markDirty();
      }
    } else {
      // 帮卖分销、添加活动 — 切换"已设置"/"未设置"
      if (formState[field]) {
        formState[field] = '';
        if (display) display.textContent = '未设置';
      } else {
        formState[field] = 'set';
        if (display) display.textContent = '已设置';
      }
      markDirty();
    }
  });
});

// ============================================================
// 脏标记
// ============================================================
function markDirty() {
  isDirty = true;
}

// ============================================================
// 表单校验
// ============================================================
function validate() {
  const errors = [];

  // 清除之前的错误状态
  document.querySelectorAll('.wg-form--error').forEach((el) => {
    el.classList.remove('wg-form--error');
    const hint = el.querySelector('.wg-form__hint:not(.wg-form__hint--count)');
    if (hint) hint.remove();
  });

  // 必填：产品标题
  if (!formState.title.trim()) {
    errors.push({ field: 'title', message: '请输入产品标题' });
  }

  // 必填：商品图片
  if (formState.images.length === 0) {
    errors.push({ field: 'images', message: '请上传商品图片' });
  }

  // 必填：产品分类
  if (!formState.category) {
    errors.push({ field: 'category', message: '请选择产品分类' });
  }

  // 必填：售价
  if (!formState.price.trim()) {
    errors.push({ field: 'price', message: '请输入售价' });
  }

  // 显示错误
  errors.forEach((err) => {
    const formEl = document.querySelector(`[data-field="${err.field}"]`);
    if (formEl) {
      formEl.classList.add('wg-form--error');
      const hint = document.createElement('p');
      hint.className = 'wg-form__hint';
      hint.textContent = err.message;
      formEl.appendChild(hint);
    }
  });

  return errors.length === 0;
}

// ============================================================
// 发布流程
// ============================================================
function handlePublish() {
  if (!validate()) {
    // 滚动到第一个错误
    const firstError = document.querySelector('.wg-form--error');
    if (firstError) {
      firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    return;
  }

  // 弹出发布确认 Dialog
  showDialog('dialogPublish');
}

// 底部发布按钮
document.getElementById('btnPublish').addEventListener('click', handlePublish);

// 导航栏发布按钮
document.getElementById('btnQuickPublish').addEventListener('click', handlePublish);

// 发布确认 — 确认
document.getElementById('btnPublishConfirm').addEventListener('click', () => {
  hideDialog('dialogPublish');
  showLoading();

  // 模拟提交
  setTimeout(() => {
    hideLoading();

    // 模拟成功/失败（90% 成功率）
    const success = Math.random() > 0.1;

    if (success) {
      showToast('发布成功', 'success');
      // 重置脏标记
      isDirty = false;
      // 2秒后模拟返回
      setTimeout(() => {
        if (window.history && window.history.length > 1) {
          window.history.back();
        } else {
          showToast('商品已发布', 'success');
        }
      }, 2000);
    } else {
      showToast('发布失败，请重试', 'error');
    }
  }, 1500);
});

// 发布确认 — 取消
document.getElementById('btnPublishDismiss').addEventListener('click', () => {
  hideDialog('dialogPublish');
});

// ============================================================
// 离开确认
// ============================================================
document.getElementById('btnBack').addEventListener('click', (e) => {
  e.preventDefault();
  if (isDirty) {
    showDialog('dialogLeave');
  } else {
    if (window.history && window.history.length > 1) {
      window.history.back();
    } else {
      showToast('已在首页', 'error');
    }
  }
});

// 离开 — 确认
document.getElementById('btnLeaveConfirm').addEventListener('click', () => {
  hideDialog('dialogLeave');
  if (window.history && window.history.length > 1) {
    window.history.back();
  } else {
    showToast('已在首页', 'error');
  }
});

// 离开 — 取消
document.getElementById('btnLeaveDismiss').addEventListener('click', () => {
  hideDialog('dialogLeave');
});

// ============================================================
// 浏览器后退拦截
// ============================================================
window.addEventListener('beforeunload', (e) => {
  if (isDirty) {
    e.preventDefault();
    e.returnValue = '';
  }
});

// 监听 popstate（用户点浏览器后退）
window.addEventListener('popstate', (e) => {
  if (isDirty) {
    // 阻止后退，先弹确认
    window.history.pushState(null, '', window.location.href);
    showDialog('dialogLeave');
  }
});

// 初始化历史记录状态以便拦截后退
window.history.pushState(null, '', window.location.href);

// ============================================================
// ESC 关闭弹窗
// ============================================================
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (document.getElementById('dialogLeave').getAttribute('data-state') === 'open') {
      hideDialog('dialogLeave');
    } else if (document.getElementById('dialogPublish').getAttribute('data-state') === 'open') {
      hideDialog('dialogPublish');
    } else if (document.getElementById('actionSheet').style.display === 'flex') {
      hideActionSheet();
    }
  }
});

// ============================================================
// Dialog 遮罩点击关闭（双按钮 Dialog 支持）
// ============================================================
document.querySelectorAll('.wg-dialog-overlay').forEach((overlay) => {
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      // 不关闭 — 需显式选择按钮
    }
  });
});

// ============================================================
// 初始化：设置默认值
// ============================================================
// 来源（仅自己可见）说明
document.querySelector('[data-field="source"] .wg-form__right .wg-link').addEventListener('click', () => {
  showToast('来源信息仅自己可见', 'error');
});
