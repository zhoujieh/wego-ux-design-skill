const sourceCatalog = [
  {
    id: "local",
    name: "本地相册",
    count: "128 件",
    desc: "自拍上传、店员拍摄商品，库存同步最快"
  },
  {
    id: "supplier",
    name: "供应商图库",
    count: "74 件",
    desc: "来自供应商共享图册，适合统一规则管理"
  },
  {
    id: "distribution",
    name: "分销代发",
    count: "63 件",
    desc: "库存依赖上游回传，适合单独限制超卖风险"
  },
  {
    id: "booking",
    name: "拍摄预约",
    count: "21 件",
    desc: "预售和预约类商品较多，通常允许灵活开单"
  },
  {
    id: "ai",
    name: "AI 生图",
    count: "40 件",
    desc: "用于快速上新，适合与现货商品区分管理"
  }
];

const defaultState = {
  mode: "unified",
  globalPolicy: "deny",
  allowOrderWhenOos: false,
  autoDelistZero: true,
  sourceMode: "partial-allow",
  selectedSources: ["booking", "ai"]
};

let savedState = cloneState(defaultState);
let draftState = cloneState(defaultState);
let bootOpened = false;
let toastTimer = null;
let saveTimer = null;

const root = document.querySelector(".prototype-shell");
const homeView = document.querySelector('[data-view="home"]');
const modalView = document.querySelector('[data-view="oversell"]');
const discardDialog = document.getElementById("discard-dialog");
const savingLoading = document.getElementById("saving-loading");
const pageToast = document.getElementById("page-toast");
const toastMessage = document.getElementById("toast-message");
const sourceList = document.getElementById("source-list");
const sourceError = document.getElementById("source-error");
const summarySubtitle = document.getElementById("summary-subtitle");
const livePreviewTitle = document.getElementById("live-preview-title");
const livePreviewDesc = document.getElementById("live-preview-desc");
const livePreviewScope = document.getElementById("live-preview-scope");
const livePreviewExtra = document.getElementById("live-preview-extra");
const selectedCountTag = document.getElementById("selected-count-tag");
const sourceModeDesc = document.getElementById("source-mode-desc");
const sourceSelectionTip = document.getElementById("source-selection-tip");
const selectAllLabel = document.getElementById("select-all-label");
const settingsScroll = document.querySelector(".page__scroll--settings");

buildSourceList();
bindEvents();
render();

requestAnimationFrame(() => {
  window.setTimeout(() => {
    if (!bootOpened) {
      openSheet();
      bootOpened = true;
    }
  }, 0);
});

function bindEvents() {
  document.querySelectorAll("[data-open-sheet]").forEach((node) => {
    node.addEventListener("click", openSheet);
  });

  document.querySelector("[data-cancel]").addEventListener("click", handleCancel);
  document.querySelector("[data-save]").addEventListener("click", handleSave);
  document.querySelector("[data-close-discard]").addEventListener("click", closeDiscardDialog);
  document.querySelector("[data-confirm-discard]").addEventListener("click", discardDraft);

  document.querySelectorAll("[data-mode-option]").forEach((node) => {
    bindRowAction(node, () => {
      draftState.mode = node.dataset.modeOption;
      clearSourceError();
      render();
    });
  });

  document.querySelectorAll("[data-global-option]").forEach((node) => {
    bindRowAction(node, () => {
      draftState.globalPolicy = node.dataset.globalOption;
      render();
    });
  });

  document.querySelectorAll("[data-source-mode-option]").forEach((node) => {
    bindRowAction(node, () => {
      draftState.sourceMode = node.dataset.sourceModeOption;
      render();
    });
  });

  document.querySelectorAll("[data-switch]").forEach((node) => {
    node.addEventListener("click", () => {
      const key = node.dataset.switch;
      draftState[key] = !draftState[key];
      render();
    });
  });

  document.querySelectorAll("[data-toggle-help]").forEach((node) => {
    node.addEventListener("click", () => {
      const key = node.dataset.toggleHelp;
      const panel = document.querySelector(`[data-help-panel="${key}"]`);
      panel.hidden = !panel.hidden;
    });
  });

  document.querySelector("[data-toggle-select-all]").addEventListener("click", () => {
    if (draftState.selectedSources.length === sourceCatalog.length) {
      draftState.selectedSources = [];
    } else {
      draftState.selectedSources = sourceCatalog.map((item) => item.id);
    }

    clearSourceError();
    render();
  });

  discardDialog.addEventListener("click", (event) => {
    if (event.target === discardDialog) {
      closeDiscardDialog();
    }
  });
}

function buildSourceList() {
  sourceList.innerHTML = sourceCatalog
    .map((item, index) => {
      const dividerClass = index < sourceCatalog.length - 1 ? " wg-cell--divider-full" : "";

      return `
        <div class="wg-cell wg-cell--select wg-cell--double source-item interactive-row${dividerClass}" tabindex="0" role="button" data-source-item="${item.id}">
          <div class="wg-cell__select">
            <button class="wg-checkbox wg-checkbox--mark-check" type="button" aria-checked="false" tabindex="-1" data-source-checkbox="${item.id}">
              <span class="wg-checkbox__indicator"></span>
            </button>
          </div>
          <div class="wg-cell__main">
            <div class="wg-cell__text">
              <div class="wg-cell__title-row">
                <div class="wg-cell__title">${item.name}</div>
                <div class="wg-tag wg-tag--20 wg-tag--grey">
                  <span class="wg-tag__text">${item.count}</span>
                </div>
              </div>
              <div class="wg-cell__subtitle">${item.desc}</div>
            </div>
          </div>
        </div>
      `;
    })
    .join("");

  document.querySelectorAll("[data-source-item]").forEach((node) => {
    bindRowAction(node, () => {
      const id = node.dataset.sourceItem;
      const exists = draftState.selectedSources.includes(id);
      draftState.selectedSources = exists
        ? draftState.selectedSources.filter((value) => value !== id)
        : [...draftState.selectedSources, id];

      clearSourceError();
      render();
    });
  });
}

function openSheet() {
  clearTimers();
  closeDiscardDialog();
  draftState = cloneState(savedState);
  clearSourceError();
  render();
  modalView.dataset.active = "true";
  homeView.classList.add("is-underlay");
}

function closeSheet() {
  modalView.dataset.active = "false";
  homeView.classList.remove("is-underlay");
}

function handleCancel() {
  if (isDirty()) {
    openDiscardDialog();
    return;
  }

  closeSheet();
}

function handleSave() {
  clearSourceError();

  if (draftState.mode === "classified" && draftState.selectedSources.length === 0) {
    sourceError.hidden = false;
    showToast("请至少选择 1 个商品来源");
    settingsScroll.scrollTo({
      top: sourceList.offsetTop - settingsScroll.offsetTop - sourceCatalog.length,
      behavior: "smooth"
    });
    return;
  }

  savingLoading.dataset.state = "visible";

  clearTimeout(saveTimer);
  saveTimer = window.setTimeout(() => {
    savedState = cloneState(draftState);
    savingLoading.dataset.state = "hidden";
    closeSheet();
    render();
    showToast("超卖策略已保存并生效");
  }, 900);
}

function discardDraft() {
  draftState = cloneState(savedState);
  closeDiscardDialog();
  render();
  closeSheet();
}

function openDiscardDialog() {
  discardDialog.dataset.state = "open";
  discardDialog.setAttribute("aria-hidden", "false");
}

function closeDiscardDialog() {
  discardDialog.dataset.state = "closed";
  discardDialog.setAttribute("aria-hidden", "true");
}

function clearSourceError() {
  sourceError.hidden = true;
}

function showToast(message) {
  clearTimeout(toastTimer);
  toastMessage.textContent = message;
  pageToast.dataset.state = "visible";

  toastTimer = window.setTimeout(() => {
    pageToast.dataset.state = "hidden";
  }, 2200);
}

function render() {
  renderMode();
  renderUnified();
  renderClassified();
  renderPreview();
  renderSummary();
}

function renderMode() {
  const isUnified = draftState.mode === "unified";

  document.querySelectorAll("[data-mode-option]").forEach((node) => {
    node.setAttribute("aria-pressed", String(node.dataset.modeOption === draftState.mode));
  });

  document.querySelectorAll("[data-mode-radio]").forEach((node) => {
    const selected = node.dataset.modeRadio === draftState.mode;
    node.classList.toggle("wg-radio--checked", selected);
    node.setAttribute("aria-checked", String(selected));
  });

  document.querySelectorAll("[data-panel]").forEach((node) => {
    const shouldShow = node.dataset.panel === draftState.mode;
    node.hidden = !shouldShow;
  });

  if (isUnified) {
    clearSourceError();
  }
}

function renderUnified() {
  const deny = draftState.globalPolicy === "deny";

  document.querySelectorAll("[data-global-radio]").forEach((node) => {
    const selected = node.dataset.globalRadio === draftState.globalPolicy;
    node.classList.toggle("wg-radio--checked", selected);
    node.setAttribute("aria-checked", String(selected));
  });

  document.querySelector('[data-sub-panel="deny"]').hidden = !deny;
  updateSwitch("allowOrderWhenOos", draftState.allowOrderWhenOos);
  updateSwitch("autoDelistZero", draftState.autoDelistZero);
}

function renderClassified() {
  document.querySelectorAll("[data-source-mode-radio]").forEach((node) => {
    const selected = node.dataset.sourceModeRadio === draftState.sourceMode;
    node.classList.toggle("wg-radio--checked", selected);
    node.setAttribute("aria-checked", String(selected));
  });

  sourceCatalog.forEach((item) => {
    const checked = draftState.selectedSources.includes(item.id);
    const node = document.querySelector(`[data-source-checkbox="${item.id}"]`);
    node.classList.toggle("wg-checkbox--checked", checked);
    node.setAttribute("aria-checked", String(checked));
  });

  const count = draftState.selectedSources.length;
  selectedCountTag.textContent = `已选 ${count} 个来源`;
  selectAllLabel.textContent = count === sourceCatalog.length ? "清空" : "全选";

  sourceModeDesc.textContent = draftState.sourceMode === "partial-allow"
    ? "勾选的来源允许超卖，未勾选的来源默认不允许超卖"
    : "勾选的来源不允许超卖，未勾选的来源默认允许超卖";

  sourceSelectionTip.textContent = draftState.sourceMode === "partial-allow"
    ? "适合把预约、AI 生图等灵活货源单独放开"
    : "适合把分销代发、供应商图库等高风险货源重点拦截";
}

function renderPreview() {
  const preview = buildPreview(draftState);
  livePreviewTitle.textContent = preview.title;
  livePreviewDesc.textContent = preview.description;
  livePreviewScope.textContent = preview.scope;
  livePreviewExtra.textContent = preview.extra;
}

function renderSummary() {
  summarySubtitle.textContent = buildSummary(savedState);
}

function updateSwitch(key, value) {
  const node = document.querySelector(`[data-switch="${key}"]`);
  node.classList.toggle("wg-switch--on", value);
  node.setAttribute("aria-checked", String(value));
}

function buildSummary(state) {
  if (state.mode === "unified") {
    if (state.globalPolicy === "allow") {
      return "统一设置，允许超卖，全部商品可继续销售";
    }

    const parts = ["统一设置，不允许超卖"];

    if (state.allowOrderWhenOos) {
      parts.push("允许库存不足时继续开单");
    }

    if (state.autoDelistZero) {
      parts.push("库存为零自动下架");
    }

    return parts.join("，");
  }

  const selectedNames = sourceCatalog
    .filter((item) => state.selectedSources.includes(item.id))
    .map((item) => item.name)
    .slice(0, 2)
    .join("、");

  const actionText = state.sourceMode === "partial-allow" ? "允许超卖" : "不允许超卖";
  const suffix = state.selectedSources.length > 2 ? "等来源" : "来源";

  return `分类设置，${selectedNames || "未选择"}${suffix}${actionText}`;
}

function buildPreview(state) {
  if (state.mode === "unified") {
    if (state.globalPolicy === "allow") {
      return {
        title: "全店统一，允许超卖",
        description: "所有相册商品都会继续销售，适合库存波动大但履约灵活的场景。",
        scope: "作用于全部商品",
        extra: "限制项不生效"
      };
    }

    return {
      title: "全店统一，不允许超卖",
      description: state.autoDelistZero
        ? "库存不足时优先拦截，库存归零后会自动下架并在补货后重新上架。"
        : "库存不足时优先拦截，但不会自动下架，需要商家手动管理上架状态。",
      scope: "作用于全部商品",
      extra: state.allowOrderWhenOos ? "超卖开单开启" : "超卖开单关闭"
    };
  }

  const count = state.selectedSources.length;
  const actionText = state.sourceMode === "partial-allow" ? "允许超卖" : "不允许超卖";

  return {
    title: `按来源分类，${count} 个来源${actionText}`,
    description: state.sourceMode === "partial-allow"
      ? "适合把预约、AI 生图等灵活货源单独放开，其余来源继续严格控量。"
      : "适合把分销、供应商图库等高风险来源重点收紧，其余来源保留灵活销售。", 
    scope: `作用于 ${count} 个来源`,
    extra: state.sourceMode === "partial-allow" ? "其余来源不允许超卖" : "其余来源允许超卖"
  };
}

function isDirty() {
  return JSON.stringify(savedState) !== JSON.stringify(draftState);
}

function cloneState(state) {
  return {
    mode: state.mode,
    globalPolicy: state.globalPolicy,
    allowOrderWhenOos: state.allowOrderWhenOos,
    autoDelistZero: state.autoDelistZero,
    sourceMode: state.sourceMode,
    selectedSources: [...state.selectedSources]
  };
}

function clearTimers() {
  clearTimeout(saveTimer);
  clearTimeout(toastTimer);
}

function bindRowAction(node, callback) {
  node.addEventListener("click", (event) => {
    if (event.target.closest("[tabindex='-1']")) {
      callback();
      return;
    }

    callback();
  });

  node.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      callback();
    }
  });
}
