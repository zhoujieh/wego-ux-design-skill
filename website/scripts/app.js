/* ═══════════════════════════════════════════
   Wego Design System — 文档网站 SPA
   Hash 路由 + 视图渲染 + 侧边栏交互
   ═══════════════════════════════════════════ */

(function () {
  'use strict';

  // ── 工具函数 ──

  function h(tag, attrs, children) {
    var el = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === 'class' || k === 'className') el.className = attrs[k];
        else if (k === 'href') el.setAttribute('href', attrs[k]);
        else if (k === 'id') el.id = attrs[k];
        else if (k.startsWith('data-')) el.setAttribute(k, attrs[k]);
        else if (k === 'style' && typeof attrs[k] === 'string') el.setAttribute('style', attrs[k]);
        else if (k === 'innerHTML') el.innerHTML = attrs[k];
        else el.setAttribute(k, attrs[k]);
      });
    }
    (children || []).forEach(function (c) {
      if (c == null || c === false) return;
      if (typeof c === 'string' || typeof c === 'number') el.appendChild(document.createTextNode(c));
      else if (c instanceof Node) el.appendChild(c);
    });
    return el;
  }

  // ── 侧边栏状态 ──
  var sidebarEl = document.getElementById('sidebar');
  var sidebarNavEl = document.getElementById('sidebar-nav');
  var sidebarToggleEl = document.getElementById('sidebar-toggle');

  function toggleSidebar() {
    sidebarEl.classList.toggle('open');
  }

  sidebarToggleEl.addEventListener('click', function (e) {
    e.stopPropagation();
    toggleSidebar();
  });

  document.addEventListener('click', function (e) {
    if (sidebarEl.classList.contains('open') && !sidebarEl.contains(e.target) && e.target !== sidebarToggleEl) {
      sidebarEl.classList.remove('open');
    }
  });

  // ── 路由表 ──
  var routes = [
    { path: '#/', view: 'home' },
    { path: '#/tokens', view: 'tokens' },
    { path: '#/layout', view: 'layout' },
    { path: '#/components', view: 'components' },
    { path: '#/components/button', view: 'component-button' },
    { path: '#/forbidden', view: 'forbidden' }
  ];

  function getRoute(hash) {
    var h = hash || window.location.hash || '#/';
    for (var i = 0; i < routes.length; i++) {
      if (routes[i].path === h) return routes[i];
    }
    return routes[0];
  }

  // ── 侧边栏渲染 ──
  function renderSidebar(currentPath) {
    var groups = [
      { label: '', links: [
        { href: '#/', label: '首页' }
      ]},
      { label: '设计 Token', links: [
        { href: '#/tokens', label: 'Token 总览', sub: true },
        { href: '#/tokens#colors', label: '颜色 Colors', sub: true },
        { href: '#/tokens#typography', label: '排版 Typography', sub: true },
        { href: '#/tokens#spacing', label: '间距 Spacing', sub: true },
        { href: '#/tokens#radius', label: '圆角 Radius', sub: true },
        { href: '#/tokens#elevation', label: '阴影 Elevation', sub: true },
        { href: '#/tokens#motion', label: '动效 Motion', sub: true }
      ]},
      { label: '布局系统', links: [
        { href: '#/layout', label: '布局总览' }
      ]},
      { label: '组件', links: [
        { href: '#/components', label: '组件总览' },
        { href: '#/components/button', label: 'Button', sub: true }
      ]},
      { label: '', links: [
        { href: '#/forbidden', label: '禁止事项' }
      ]}
    ];

    sidebarNavEl.innerHTML = '';
    groups.forEach(function (group) {
      if (group.label) {
        var label = h('div', { class: 'sidebar-group-label' }, [document.createTextNode(group.label)]);
        sidebarNavEl.appendChild(label);
      }
      group.links.forEach(function (link) {
        var cls = 'sidebar-link';
        if (link.sub) cls += ' sidebar-link--sub';
        if (currentPath === link.href || (currentPath.indexOf('#/tokens') === 0 && link.href.indexOf('#/tokens') === 0)) {
          cls += ' active';
        }
        var a = h('a', { class: cls, href: link.href }, [document.createTextNode(link.label)]);
        a.addEventListener('click', function (e) {
          e.preventDefault();
          window.location.hash = this.getAttribute('href');
          if (window.innerWidth <= 768) sidebarEl.classList.remove('open');
        });
        sidebarNavEl.appendChild(a);
      });
    });
  }

  // ── 滚动到子锚点 ──
  function scrollToAnchor() {
    var hash = window.location.hash;
    var anchorIdx = hash.lastIndexOf('#');
    if (anchorIdx > 0) {
      var anchor = hash.substring(anchorIdx + 1);
      setTimeout(function () {
        var el = document.getElementById(anchor);
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    }
  }

  // ── 主渲染 ──
  var mainEl = document.getElementById('main-content');

  function render() {
    var hash = window.location.hash || '#/';
    var route = getRoute(hash);
    document.title = (route.view === 'home' ? '' : route.view + ' — ') + 'Wego Design';
    renderSidebar(hash);
    mainEl.innerHTML = '';

    switch (route.view) {
      case 'home': renderHome(mainEl); break;
      case 'tokens': renderTokens(mainEl); break;
      case 'layout': renderLayout(mainEl); break;
      case 'components': renderComponents(mainEl); break;
      case 'component-button': renderButtonDetail(mainEl); break;
      case 'forbidden': renderForbidden(mainEl); break;
    }
    scrollToAnchor();
  }

  window.addEventListener('hashchange', render);
  window.addEventListener('DOMContentLoaded', render);

  // ═══════════════════════════════════════════
  // 首页
  // ═══════════════════════════════════════════
  function renderHome(el) {
    el.innerHTML =
      '<div class="hero">' +
        '<h1 class="hero-title">微购设计系统</h1>' +
        '<p class="hero-desc">Wego Design System — 帮助商家以最小学习成本、时间成本和操作成本完成经营目标。简洁、干净、克制、高信息密度、微信生态一致。</p>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">设计决策优先级</h2>' +
        '<div class="priority-chain">' +
          '<span class="priority-item">清晰</span><span class="priority-arrow">›</span>' +
          '<span class="priority-item">一致</span><span class="priority-arrow">›</span>' +
          '<span class="priority-item">效率</span><span class="priority-arrow">›</span>' +
          '<span class="priority-item">美观</span><span class="priority-arrow">›</span>' +
          '<span class="priority-item">创新</span>' +
        '</div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">5 条设计原则</h2>' +
        '<div class="principle-grid">' +
          principleCard('1', '降低认知成本', '用户 3 秒内知道这里是什么、能做什么、下一步是什么。一个页面只保留一个主目标。') +
          principleCard('2', '降低时间成本', '减少等待、点击、输入、跳转、重复判断。自动优于选择、选择优于输入、批量优于单个。') +
          principleCard('3', '复用用户经验', '优先使用已有组件和常见微信式交互。不为创新而改变成熟路径。') +
          principleCard('4', '建立用户信任', '简洁克制的界面 + 数据化表达 + 明确说明操作结果。不可逆操作提供确认和恢复路径。') +
          principleCard('5', '符合人性', '用户怕损失、易出错、会产生情绪。设计必须承认这些事实，提供自动保存、撤销、恢复机制。') +
        '</div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">核心设计哲学</h2>' +
        '<div class="flex-col gap-16">' +
          '<div class="card"><div class="card-title">经营优先</div><div class="card-desc">用户来到微购是为了完成经营行为。所有设计都服务于获客、转化、复购、效率和收益。禁止为视觉效果牺牲经营效率。</div></div>' +
          '<div class="card"><div class="card-title">解决问题优先</div><div class="card-desc">没有设计，只有解决问题。设计师的个人表达不能高于用户问题。不得为了"更有设计感"添加无意义视觉元素。</div></div>' +
          '<div class="card"><div class="card-title">432 原则</div><div class="card-desc">页面交互方式不超过 4 种，内容样式不超过 3 种，不为 20% 需求打扰 80% 用户。</div></div>' +
        '</div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">快速导航</h2>' +
        '<div class="nav-cards">' +
          navCard('#/tokens', '🎨', '设计 Token', '颜色、排版、间距、圆角、阴影、动效等基础变量') +
          navCard('#/layout', '📐', '布局系统', 'M0-M3 页边距、G1-G2 分组、页面类型、信息层级') +
          navCard('#/components', '🧩', '组件库', 'Button、NavBar、Dialog 等 9 个已注册组件') +
          navCard('#/forbidden', '🚫', '禁止事项', '视觉、Token、组件、布局、交互的禁止模式') +
        '</div>' +
      '</div>';
  }

  function principleCard(num, name, desc) {
    return '<div class="principle-card"><div class="principle-num">Principle ' + num + '</div><div class="principle-name">' + name + '</div><div class="principle-desc">' + desc + '</div></div>';
  }

  function navCard(href, icon, title, desc) {
    return '<a href="' + href + '" class="nav-card"><div class="nav-card-icon">' + icon + '</div><div class="nav-card-title">' + title + '</div><div class="nav-card-desc">' + desc + '</div></a>';
  }

  // ═══════════════════════════════════════════
  // Token 页
  // ═══════════════════════════════════════════
  function renderTokens(el) {
    el.innerHTML =
      '<h1 class="page-title">设计 Token</h1>' +
      '<p class="page-subtitle">所有设计值通过 CSS 自定义属性 <code style="background:var(--wg-color-bg-subtle);padding:2px 6px;border-radius:4px;font-size:13px">var(--wg-*)</code> 使用。tokens.json 是唯一数据源，v3.2.0。</p>' +

      // ── Color ──
      '<div class="section" id="colors">' +
        '<h2 class="section-title">颜色 Colors</h2>' +
        '<h3 class="section-subtitle">品牌色 & 功能色</h3>' +
        '<div class="color-grid">' +
          clrCard('#03C160', '品牌主色', '--wg-color-base-brand-500') +
          clrCard('#FA5051', '危险 / 错误', '--wg-color-base-danger-500') +
          clrCard('#208BF1', '信息提示', '--wg-color-base-info-500') +
          clrCard('#03C160', '成功', '--wg-color-base-success-500') +
          clrCard('#FA9D3B', '警告', '--wg-color-base-warning-500') +
          clrCard('#FF6045', '营销 / 促销', '--wg-color-base-promotion-500') +
          clrCard('#285B9A', '文本链接', '--wg-color-base-link-500') +
        '</div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">文字色 Text</h3>' +
        '<div class="flex-col gap-8">' +
          txtSwatch('#1E2028', '一级文字 Primary', '--wg-color-text-primary') +
          txtSwatch('#6E7382', '二级文字 Secondary', '--wg-color-text-secondary') +
          txtSwatch('#9097A3', '三级文字 Tertiary', '--wg-color-text-tertiary') +
          txtSwatch('#B7BEC5', '禁用文字 Disabled', '--wg-color-text-disabled') +
          txtSwatch('#FFFFFF', '反色文字 Inverse', '--wg-color-text-inverse') +
          txtSwatch('#285B9A', '链接文字 Link', '--wg-color-text-link') +
        '</div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">背景色 Background</h3>' +
        '<div class="flex-col gap-8">' +
          bgSwatch('#EDEDED', '页面背景 Page', '--wg-color-bg-page') +
          bgSwatch('#FFFFFF', '容器表面 Surface', '--wg-color-bg-surface') +
          bgSwatch('#F8F9FA', '极浅灰背景 Subtle', '--wg-color-bg-subtle') +
          bgSwatch('#F2F3F6', '浅灰背景 Muted', '--wg-color-bg-muted') +
          bgSwatch('#E9EAEF', '选中态背景 Active', '--wg-color-bg-active') +
        '</div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">交互状态 State</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Token</th><th>CSS Variable</th><th>用途</th></tr>' +
          '<tr><td>wg.color.state.hover</td><td>--wg-color-state-hover</td><td>悬停态背景</td></tr>' +
          '<tr><td>wg.color.state.pressed</td><td>--wg-color-state-pressed</td><td>按压态背景</td></tr>' +
          '<tr><td>wg.color.state.selected</td><td>--wg-color-state-selected</td><td>选中态</td></tr>' +
          '<tr><td>wg.color.state.disabled.bg</td><td>--wg-color-state-disabled-bg</td><td>禁用态背景</td></tr>' +
          '<tr><td>wg.color.state.disabled.text</td><td>--wg-color-state-disabled-text</td><td>禁用态文字</td></tr>' +
          '<tr><td>wg.color.state.focus</td><td>--wg-color-state-focus</td><td>焦点描边</td></tr>' +
        '</table></div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">操作色 Action</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Token</th><th>CSS Variable</th><th>用途</th></tr>' +
          '<tr><td>wg.color.action.primary.default</td><td>--wg-color-action-primary-default</td><td>主操作默认</td></tr>' +
          '<tr><td>wg.color.action.primary.hover</td><td>--wg-color-action-primary-hover</td><td>主操作悬停</td></tr>' +
          '<tr><td>wg.color.action.primary.pressed</td><td>--wg-color-action-primary-pressed</td><td>主操作按压</td></tr>' +
          '<tr><td>wg.color.action.primary.disabled</td><td>--wg-color-action-primary-disabled</td><td>主操作禁用</td></tr>' +
          '<tr><td>wg.color.action.secondary.default</td><td>--wg-color-action-secondary-default</td><td>次操作默认</td></tr>' +
          '<tr><td>wg.color.action.danger.default</td><td>--wg-color-action-danger-default</td><td>危险操作默认</td></tr>' +
          '<tr><td>wg.color.action.link.default</td><td>--wg-color-action-link-default</td><td>链接操作默认</td></tr>' +
        '</table></div>' +
      '</div>' +

      // ── Typography ──
      '<div class="section" id="typography">' +
        '<h2 class="section-title">排版 Typography</h2>' +
        '<h3 class="section-subtitle">字体族</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Token</th><th>字体</th><th>用途</th></tr>' +
          '<tr><td>wg.font.family.text</td><td>PingFang SC, -apple-system, ...</td><td>默认正文字体</td></tr>' +
          '<tr><td>wg.font.family.number.decorative</td><td>WegoKeyboard N9</td><td>装饰数字（价格、指标）</td></tr>' +
          '<tr><td>wg.font.family.system</td><td>系统默认</td><td>系统回退</td></tr>' +
        '</table></div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">字号与行高</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Token</th><th>字号</th><th>行高</th><th>预览</th></tr>' +
          typeRow('f10', '10px', '14px', '10px') +
          typeRow('f12', '12px', '18px', '12px') +
          typeRow('f14', '14px', '20px', '14px') +
          typeRow('f16', '16px', '24px', '16px') +
          typeRow('f18', '18px', '26px', '18px') +
          typeRow('f22', '22px', '30px', '22px') +
        '</table></div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">字重</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Token</th><th>CSS Variable</th><th>值</th><th>预览</th></tr>' +
          weightRow('regular', '400', '400') +
          weightRow('medium', '500', '500') +
          weightRow('semibold', '600', '600') +
        '</table></div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">数字专用字号</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Token</th><th>字号</th><th>预览</th></tr>' +
          numRow('nf12', '12px', '12px') +
          numRow('nf16', '16px', '16px') +
          numRow('nf24', '24px', '24px') +
          numRow('nf32', '32px', '32px') +
        '</table></div>' +
      '</div>' +

      // ── Spacing ──
      '<div class="section" id="spacing">' +
        '<h2 class="section-title">间距 Spacing</h2>' +
        '<p class="card-desc" style="margin-block-end:16px">10 级间距体系，默认值 16px。</p>' +
        spBar(0) + spBar(2) + spBar(4) + spBar(8) + spBar(12) + spBar(16, true) + spBar(24) + spBar(32) + spBar(40) + spBar(48) +
        '<h3 class="section-subtitle" style="margin-block-start:24px">触摸目标</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Token</th><th>值</th><th>用途</th></tr>' +
          '<tr><td>wg.touch.min</td><td>40px</td><td>最小触摸目标</td></tr>' +
          '<tr><td>wg.touch.default</td><td>44px</td><td>默认触摸目标</td></tr>' +
          '<tr><td>wg.touch.comfortable</td><td>48px</td><td>舒适触摸目标</td></tr>' +
        '</table></div>' +
      '</div>' +

      // ── Radius ──
      '<div class="section" id="radius">' +
        '<h2 class="section-title">圆角 Radius</h2>' +
        '<p class="card-desc" style="margin-block-end:16px">7 级圆角体系。默认使用 xs-sm，避免大圆角作为默认风格。</p>' +
        '<div class="radius-grid">' +
          radCell('none', '0') + radCell('xs', '4px') + radCell('sm', '6px') + radCell('md', '8px') + radCell('lg', '12px') + radCell('xl', '16px') + radCell('full', '999px') +
        '</div>' +
      '</div>' +

      // ── Elevation ──
      '<div class="section" id="elevation">' +
        '<h2 class="section-title">阴影 Elevation</h2>' +
        '<p class="card-desc" style="margin-block-end:16px">默认无阴影。只有层级确实浮起时使用。</p>' +
        '<div class="shadow-grid">' +
          shadCell('none', 'none') +
          shadCell('xs', '0 1px 4px rgba(30,32,40,0.04)') +
          shadCell('sm', '0 2px 8px rgba(30,32,40,0.06)') +
          shadCell('md', '0 4px 16px rgba(30,32,40,0.08)') +
          shadCell('lg', '0 8px 32px rgba(30,32,40,0.12)') +
          shadCell('xl', '0 12px 48px rgba(30,32,40,0.16)') +
        '</div>' +
      '</div>' +

      // ── Motion ──
      '<div class="section" id="motion">' +
        '<h2 class="section-title">动效 Motion</h2>' +
        '<h3 class="section-subtitle">时长 Duration</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Token</th><th>CSS Variable</th><th>值</th><th>用途</th></tr>' +
          '<tr><td>wg.motion.duration.instant</td><td>--wg-motion-duration-instant</td><td>0ms</td><td>瞬时</td></tr>' +
          '<tr><td>wg.motion.duration.fast</td><td>--wg-motion-duration-fast</td><td>150ms</td><td>微交互、icon、toggle</td></tr>' +
          '<tr><td>wg.motion.duration.normal</td><td>--wg-motion-duration-normal</td><td>250ms</td><td>页面转场、弹窗</td></tr>' +
          '<tr><td>wg.motion.duration.slow</td><td>--wg-motion-duration-slow</td><td>350ms</td><td>复杂动画、引导</td></tr>' +
          '<tr><td>wg.motion.duration.xslow</td><td>--wg-motion-duration-xslow</td><td>500ms</td><td>大型转场</td></tr>' +
        '</table></div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">缓动 Easing</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Token</th><th>CSS Variable</th><th>函数</th><th>用途</th></tr>' +
          '<tr><td>wg.motion.ease.linear</td><td>--wg-motion-ease-linear</td><td>linear</td><td>匀速</td></tr>' +
          '<tr><td>wg.motion.ease.standard</td><td>--wg-motion-ease-standard</td><td>cubic-bezier(0.4,0,0.2,1)</td><td>标准缓入缓出</td></tr>' +
          '<tr><td>wg.motion.ease.enter</td><td>--wg-motion-ease-enter</td><td>cubic-bezier(0,0,0.2,1)</td><td>进入（减速）</td></tr>' +
          '<tr><td>wg.motion.ease.exit</td><td>--wg-motion-ease-exit</td><td>cubic-bezier(0.4,0,1,1)</td><td>退出（加速）</td></tr>' +
          '<tr><td>wg.motion.ease.emphasized</td><td>--wg-motion-ease-emphasized</td><td>cubic-bezier(0.2,0,0,1)</td><td>强调动效（页面转场）</td></tr>' +
        '</table></div>' +
      '</div>';
  }

  function clrCard(hex, name, cssVar) {
    return '<div class="color-card"><div class="swatch-chip swatch-chip--lg" style="background:' + hex + '"></div><div class="flex-col"><span class="color-card-label">' + name + '</span><span class="color-card-value">' + cssVar + '</span></div></div>';
  }

  function txtSwatch(hex, label, cssVar) {
    return '<div style="display:flex;align-items:center;gap:12px;padding:8px 12px;background:var(--wg-color-bg-surface);border-radius:var(--wg-radius-sm);border:var(--wg-stroke-width-hairline) solid var(--wg-color-border-subtle)"><div style="inline-size:80px;block-size:32px;border-radius:var(--wg-radius-xs);background:' + hex + ';border:var(--wg-stroke-width-hairline) solid var(--wg-color-border-subtle)"></div><span style="font-size:var(--wg-font-size-14);color:var(--wg-color-text-primary)">' + label + '</span><span style="font-size:var(--wg-font-size-12);color:var(--wg-color-text-tertiary);margin-inline-start:auto">' + cssVar + '</span></div>';
  }

  function bgSwatch(hex, label, cssVar) {
    return '<div style="display:flex;align-items:center;gap:12px;padding:8px 12px;background:var(--wg-color-bg-surface);border-radius:var(--wg-radius-sm);border:var(--wg-stroke-width-hairline) solid var(--wg-color-border-subtle)"><div style="inline-size:80px;block-size:32px;border-radius:var(--wg-radius-xs);background:' + hex + ';border:var(--wg-stroke-width-hairline) solid var(--wg-color-border-default)"></div><span style="font-size:var(--wg-font-size-14);color:var(--wg-color-text-primary)">' + label + '</span><span style="font-size:var(--wg-font-size-12);color:var(--wg-color-text-tertiary);margin-inline-start:auto">' + cssVar + '</span></div>';
  }

  function spBar(px, isDefault) {
    var w = Math.max(px * 4, 20);
    return '<div class="spacing-bar" style="inline-size:' + w + 'px;' + (isDefault ? 'background:var(--wg-color-base-brand-alpha-60)' : '') + '">' + '--wg-spacing-' + px + ' (' + px + 'px)' + (isDefault ? ' ← 默认' : '') + '</div>';
  }

  function radCell(name, value) {
    return '<div class="radius-cell"><div class="radius-box" style="border-radius:' + value + '"></div><span class="radius-label">' + name + ' (' + value + ')</span></div>';
  }

  function shadCell(name, value) {
    return '<div class="shadow-card" style="box-shadow:var(--wg-shadow-' + name + ')"><div style="font-size:var(--wg-font-size-14);color:var(--wg-color-text-primary);margin-block-end:8px">' + name + '</div><div style="font-size:var(--wg-font-size-12);color:var(--wg-color-text-tertiary)">' + value + '</div></div>';
  }

  function typeRow(tokenSuffix, size, lineH, fontSize) {
    return '<tr><td>wg.font.size.' + tokenSuffix + '</td><td>' + size + '</td><td>' + lineH + '</td><td style="font-size:' + fontSize + '">微购设计系统</td></tr>';
  }

  function weightRow(name, value, weight) {
    return '<tr><td>wg.font.weight.' + name + '</td><td>--wg-font-weight-' + name + '</td><td>' + value + '</td><td style="font-weight:' + weight + ';font-size:18px">' + name.charAt(0).toUpperCase() + name.slice(1) + '</td></tr>';
  }

  function numRow(tokenSuffix, size, fontSize) {
    return '<tr><td>wg.font.number.' + tokenSuffix + '</td><td>' + size + '</td><td style="font-family:\'WegoKeyboard N9\',sans-serif;font-size:' + fontSize + ';font-weight:500">¥1,234.56</td></tr>';
  }

  // ═══════════════════════════════════════════
  // 布局系统页
  // ═══════════════════════════════════════════
  function renderLayout(el) {
    el.innerHTML =
      '<h1 class="page-title">布局系统</h1>' +
      '<p class="page-subtitle">移动端优先，设计基准 375px。布局基于 CSS Grid / Flexbox。</p>' +

      '<div class="section">' +
        '<h2 class="section-title">页边距模式 M0–M3</h2>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>模式</th><th>Margin</th><th>375px 内容宽度</th><th>适用场景</th></tr>' +
          '<tr><td><strong>M0</strong></td><td>8px</td><td>359px</td><td>高密度列表、下拉建议、搜索结果、筛选面板</td></tr>' +
          '<tr><td><strong>M1</strong></td><td>0px</td><td>375px</td><td>通栏连续内容、沉浸式页面</td></tr>' +
          '<tr><td><strong>M2</strong> ← 默认</td><td>16px</td><td>343px</td><td>大多数业务页面、卡片式布局</td></tr>' +
          '<tr><td><strong>M3</strong></td><td>32px</td><td>311px</td><td>低密度聚焦页面、引导页</td></tr>' +
        '</table></div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">分组模式 G1–G2</h2>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>模式</th><th>内部间距</th><th>外部间距</th><th>适用场景</th></tr>' +
          '<tr><td><strong>G1</strong></td><td>0px</td><td>16px</td><td>连续紧密信息（列表项、表单字段、连续文本）</td></tr>' +
          '<tr><td><strong>G2</strong></td><td>8px</td><td>32px</td><td>宽松模块信息（卡片组、独立模块、信息分区）</td></tr>' +
        '</table></div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">页面类型（6 种）</h2>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>类型</th><th>特征</th><th>信息密度</th><th>滚动策略</th></tr>' +
          '<tr><td><strong>浏览型</strong></td><td>内容展示为主，用户浏览信息</td><td>中-高</td><td>可滚动</td></tr>' +
          '<tr><td><strong>操作型</strong></td><td>触发操作为主，完成特定任务</td><td>低-中</td><td>通常不滚动</td></tr>' +
          '<tr><td><strong>表单型</strong></td><td>信息填写、参数设置</td><td>中</td><td>长表单可滚动</td></tr>' +
          '<tr><td><strong>结果型</strong></td><td>操作完成后的反馈展示</td><td>低</td><td>不滚动</td></tr>' +
          '<tr><td><strong>异常型</strong></td><td>错误、权限不足、过期等异常</td><td>低</td><td>不滚动</td></tr>' +
          '<tr><td><strong>空状态</strong></td><td>无数据、无内容</td><td>低</td><td>不滚动</td></tr>' +
        '</table></div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">信息层级（1–4 级）</h2>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>层级</th><th>定义</th><th>视觉权重</th><th>示例</th></tr>' +
          '<tr><td><strong>L1 一级</strong></td><td>页面核心目标 / 关键结果 / 主标题</td><td>最高，唯一视觉重心</td><td>页面标题、核心数据</td></tr>' +
          '<tr><td><strong>L2 二级</strong></td><td>主要内容 / 主要表单 / 主要列表</td><td>中等</td><td>卡片内容、表单字段</td></tr>' +
          '<tr><td><strong>L3 三级</strong></td><td>辅助说明 / 状态解释 / 次要信息</td><td>弱化</td><td>帮助文字、备注</td></tr>' +
          '<tr><td><strong>L4 四级</strong></td><td>弱提示 / 时间戳 / 标签 / 占位</td><td>最弱</td><td>时间、来源</td></tr>' +
        '</table></div>' +
        '<div class="card" style="margin-block-start:16px"><div class="card-title">层级规则</div>' +
          '<ul class="usage-list">' +
            '<li>一个页面只允许一个核心视觉重心（L1）</li>' +
            '<li>主操作必须清晰可见</li>' +
            '<li>辅助信息必须弱化，不能和主信息抢权重</li>' +
            '<li>状态信息必须靠近对应对象</li>' +
          '</ul></div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">页面背景色规则</h2>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>场景</th><th>背景色</th><th>示例</th></tr>' +
          '<tr><td>多卡片/多模块页面</td><td><strong>bg-page</strong> (灰底 #EDEDED) + 卡片 bg-surface (白)</td><td>列表页、设置页</td></tr>' +
          '<tr><td>聚焦型单任务页面</td><td><strong>bg-surface</strong> (白底) 整体</td><td>登录、结果、详情</td></tr>' +
          '<tr><td>二级页面 — 上级白底</td><td>继承上级白底</td><td>登录 → 注册</td></tr>' +
          '<tr><td>二级页面 — 上级灰底</td><td>按自身内容独立选择</td><td>首页(灰) → 详情(白)</td></tr>' +
        '</table></div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">页面高度与滚动</h2>' +
        '<div class="card"><ul class="usage-list">' +
          '<li>页面容器默认占满一屏：<code>block-size: 100vh</code> (或 <code>100dvh</code>)，不使用 <code>min-height</code></li>' +
          '<li>内容不超出一屏：<code>overflow: hidden</code></li>' +
          '<li>内容超出一屏：<code>overflow-y: auto</code></li>' +
          '<li>所有可滚动区域必须隐藏浏览器默认滚动条</li>' +
          '<li>表单型、结果型、聚焦型 → 通常不滚动；浏览型、列表型 → 通常可滚动</li>' +
        '</ul></div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">页面转场动画</h2>' +
        '<p class="card-desc" style="margin-block-end:12px">页面切换必须模拟 App 原生导航体验，禁止 <code>display: none</code> 硬切。</p>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>类型</th><th>进入方向</th><th>时长</th><th>缓动</th><th>适用场景</th></tr>' +
          '<tr><td><strong>Push 推入</strong></td><td>从右滑入 → 向右滑出</td><td>250ms</td><td>emphasized</td><td>层级深入：详情、表单</td></tr>' +
          '<tr><td><strong>Present 弹出</strong></td><td>从底部滑入 → 向底部滑出</td><td>250ms</td><td>emphasized</td><td>独立流程：绑定、授权</td></tr>' +
          '<tr><td><strong>Fade 淡入</strong></td><td>渐显 → 渐隐</td><td>150ms</td><td>standard</td><td>同级切换：Tab 切换</td></tr>' +
        '</table></div>' +
      '</div>' +

      '<div class="section">' +
        '<h2 class="section-title">432 原则</h2>' +
        '<div class="card"><div class="flex-col gap-16">' +
          '<div><strong style="color:var(--wg-color-base-brand-500)">4</strong> — 页面交互方式不超过 4 种</div>' +
          '<div><strong style="color:var(--wg-color-base-brand-500)">3</strong> — 页面内容样式不超过 3 种</div>' +
          '<div><strong style="color:var(--wg-color-base-brand-500)">2</strong> — 不为 20% 需求打扰 80% 用户</div>' +
        '</div></div>' +
      '</div>';
  }

  // ═══════════════════════════════════════════
  // 组件总览
  // ═══════════════════════════════════════════
  function renderComponents(el) {
    el.innerHTML =
      '<h1 class="page-title">组件库</h1>' +
      '<p class="page-subtitle">9 个已注册组件，按类别分组。点击卡片查看详情。</p>' +

      '<div class="section"><h2 class="section-title">操作 Action</h2><div class="component-grid">' +
        compLink('#/components/button', 'Button', '按钮', '触发明确操作。提交、保存、确认、下一步。支持 page/container/compact 三种 Scope 和 strong/medium/weak 三种 Emphasis。', 'stable') +
        compWip('Link', '链接', '页面跳转或行内命令操作。支持 standalone/inline 两种 Context。') +
      '</div></div>' +

      '<div class="section"><h2 class="section-title">导航 Navigation</h2><div class="component-grid">' +
        compWip('NavBar', '导航栏', '页面顶部导航和标题。支持 standard/title-only/search 三种模式。') +
        compWip('Tabs', '标签栏', '页面内容切换。支持 standard/mini 两种尺寸和 divide/scroll 两种布局。') +
      '</div></div>' +

      '<div class="section"><h2 class="section-title">反馈 Feedback</h2><div class="component-grid">' +
        compWip('Dialog', '对话框', '模态弹窗，用于确认、提示、警告。支持 text/title/status/custom 四种变体。') +
        compWip('ActionSheet', '操作表', '底部弹出操作面板。支持 action/select 两种模式。') +
        compWip('Toast', '轻提示', '操作结果反馈，自动消失。支持 default/action 两种变体。') +
        compWip('Result', '结果页', '操作结果展示。支持 3 种布局和 10+ 图像类型。') +
      '</div></div>' +

      '<div class="section"><h2 class="section-title">表单 Form</h2><div class="component-grid">' +
        compWip('Input', '输入框', '文本/多行/数字输入。支持 full/card 两种布局和完整的校验状态。') +
      '</div></div>';
  }

  function compLink(href, name, category, desc, status) {
    return '<a href="' + href + '" class="comp-card"><div class="comp-card-header"><span class="comp-card-name">' + name + '</span><span class="badge badge--' + status + '">稳定</span></div><div class="comp-card-category">' + category + '</div><div class="comp-card-desc">' + desc + '</div></a>';
  }

  function compWip(name, category, desc) {
    return '<div class="comp-card comp-card--wip"><div class="comp-card-header"><span class="comp-card-name">' + name + '</span><span class="badge badge--wip">待补充</span></div><div class="comp-card-category">' + category + '</div><div class="comp-card-desc">' + desc + '</div></div>';
  }

  // ═══════════════════════════════════════════
  // Button 详情
  // ═══════════════════════════════════════════
  function renderButtonDetail(el) {
    el.innerHTML =
      '<h1 class="page-title">Button 按钮</h1>' +
      '<p class="page-subtitle">操作 Action · 稳定 Stable · 交互模式：纯 CSS</p>' +

      '<div class="section"><h2 class="section-title">使用决策</h2><div class="flex-row gap-24">' +
        '<div class="card" style="flex:1"><div class="card-title">✓ 使用 Button</div><ul class="usage-list">' +
          '<li>提交、保存、发布、完成、确认等执行动作的操作</li>' +
          '<li>推进流程的下一步操作</li>' +
          '<li>局部容器内最重要的功能操作</li>' +
          '<li>卡片、列表项或横条区域中的紧凑操作</li>' +
        '</ul></div>' +
        '<div class="card" style="flex:1"><div class="card-title">✗ 不使用 Button</div><ul class="usage-list usage-list--dont">' +
          '<li>页面跳转但不执行动作 → 使用 Link</li>' +
          '<li>标签切换 → 使用 Tabs</li>' +
          '<li>只有图标无规范 → 暂不生成</li>' +
          '<li>三个及以上并列操作 → 进更多菜单</li>' +
        '</ul></div>' +
      '</div></div>' +

      '<div class="section"><h2 class="section-title">决策维度</h2>' +
        '<p class="card-desc" style="margin-block-end:12px">Button 三个决策维度：<strong>scope</strong>（影响范围）、<strong>emphasis</strong>（操作优先级）、<strong>state</strong>（交互状态）。</p>' +

        '<h3 class="section-subtitle">Scope 影响范围</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Scope</th><th>应用场景</th><th>高度</th><th>宽度规则</th></tr>' +
          '<tr><td><strong>page</strong></td><td>页面级主要操作、流程推进</td><td>48px</td><td>单个180px; 成对120px×2</td></tr>' +
          '<tr><td><strong>container</strong></td><td>卡片、模块内核心操作</td><td>40px</td><td>自适应，最大420px</td></tr>' +
          '<tr><td><strong>compact</strong></td><td>列表、导航栏、行内操作</td><td>32px</td><td>随内容，最大120px</td></tr>' +
        '</table></div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">Emphasis 操作优先级</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Emphasis</th><th>含义</th><th>样式</th></tr>' +
          '<tr><td><strong>strong</strong></td><td>最重要、推荐操作</td><td>品牌绿背景 + 白色文字</td></tr>' +
          '<tr><td><strong>medium</strong></td><td>有功能但不需重点引导</td><td>浅灰背景 + 品牌绿文字（仅单按钮）</td></tr>' +
          '<tr><td><strong>weak</strong></td><td>次要、取消、关闭</td><td>浅灰背景 + 一级文字</td></tr>' +
        '</table></div>' +

        '<h3 class="section-subtitle" style="margin-block-start:24px">允许组合</h3>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>Scope</th><th>单按钮</th><th>双按钮</th><th>三个及以上</th></tr>' +
          '<tr><td>page</td><td>strong/medium/weak</td><td>只允许 strong+weak</td><td>禁止</td></tr>' +
          '<tr><td>container</td><td>strong/medium/weak</td><td>strong+weak 或 weak+weak</td><td>禁止</td></tr>' +
          '<tr><td>compact</td><td>strong/medium/weak</td><td>strong+weak 或 weak+weak</td><td>最多两个，其余进更多菜单</td></tr>' +
        '</table></div>' +
      '</div>' +

      // Button 效果预览
      '<div class="section"><h2 class="section-title">效果预览</h2>' +
        '<p class="card-desc" style="margin-block-end:12px">3 种 Scope × 3 种 Emphasis 的组合效果。</p>' +
        '<div class="preview-area"><div class="preview-grid">' +
          btnCol('page (48px)',
            btnHtml('page', 'strong', '完成'),
            btnHtml('page', 'medium', '了解更多'),
            btnHtml('page', 'weak', '取消')) +
          btnCol('container (40px)',
            btnHtml('container', 'strong', '确认退款'),
            btnHtml('container', 'medium', '查看详情'),
            btnHtml('container', 'weak', '取消')) +
          btnCol('compact (32px)',
            btnHtml('compact', 'strong', '再来一次'),
            btnHtml('compact', 'medium', '复制'),
            '<div class="preview-row"><span class="preview-row-label">weak (disabled)</span>' +
            '<button class="wg-button wg-button--compact wg-button--weak" type="button" disabled>' +
            '<span class="wg-button__surface"><span class="wg-button__label">删除</span></span></button></div>') +
        '</div></div>' +
      '</div>' +

      // 状态
      '<div class="section"><h2 class="section-title">状态 States</h2>' +
        '<div class="table-wrap"><table>' +
          '<tr><th>State</th><th>表达方式</th><th>规则</th></tr>' +
          '<tr><td>default</td><td>默认 class</td><td>正常可用</td></tr>' +
          '<tr><td>hover</td><td><code>:hover</code></td><td>仅桌面预览</td></tr>' +
          '<tr><td>pressed</td><td><code>:active</code></td><td>只改背景，不位移不缩放</td></tr>' +
          '<tr><td>focus-visible</td><td><code>:focus-visible</code></td><td>清晰焦点描边</td></tr>' +
          '<tr><td>disabled</td><td><code>disabled</code></td><td>统一禁用态</td></tr>' +
        '</table></div>' +
        '<p class="card-desc" style="margin-block-start:8px;color:var(--wg-color-text-tertiary)">V1 未定义 loading、success、error 视觉变体。通过 disabled + aria-busy + 页面级反馈实现。</p>' +
      '</div>' +

      '<div class="section"><h2 class="section-title">Anatomy</h2>' +
        '<div class="card"><pre style="font-size:13px;line-height:1.8;color:var(--wg-color-text-secondary)">button.wg-button.wg-button--{scope}.wg-button--{emphasis}\n  └── span.wg-button__surface\n      └── span.wg-button__label</pre>' +
        '<p class="card-desc" style="margin-block-start:8px">V1 仅允许文字按钮。不得加入图标、角标、副标题或加载图标。</p></div>' +
      '</div>';
  }

  function btnCol(label, html1, html2, html3) {
    return '<div class="preview-col"><div class="preview-col-label">' + label + '</div>' + html1 + html2 + html3 + '</div>';
  }

  function btnHtml(scope, emphasis, label) {
    return '<div class="preview-row"><span class="preview-row-label">' + emphasis + '</span>' +
      '<button class="wg-button wg-button--' + scope + ' wg-button--' + emphasis + '" type="button">' +
      '<span class="wg-button__surface"><span class="wg-button__label">' + label + '</span></span></button></div>';
  }

  // ═══════════════════════════════════════════
  // 禁止事项
  // ═══════════════════════════════════════════
  function renderForbidden(el) {
    el.innerHTML =
      '<h1 class="page-title">禁止事项</h1>' +
      '<p class="page-subtitle">设计系统强制执行规则，违反将导致设计不合规。</p>' +

      forbSection('视觉禁止', [
        '多个主目标 / 多个视觉焦点同时存在',
        '隐藏关键操作在深层菜单',
        '依赖用户记忆而非可见选项',
        '用装饰（阴影、渐变、复杂卡片）制造虚假层级',
        '低龄化视觉风格、夸张营销表达',
        '用高饱和色制造焦虑'
      ]) +

      forbSection('Token 禁止', [
        '业务 CSS 中硬编码 HEX/RGBA/px 设计值',
        '使用随机间距、随机圆角、随机颜色',
        '用任意大数字解决 z-index 层级冲突',
        '为单页面新增 Token（至少需要 3 个场景）',
        '通过临时 padding 伪造布局规则'
      ]) +

      forbSection('组件禁止', [
        '自创已注册组件的新变体（如 Button 的 loading/danger/icon-only）',
        '修改组件内部 Anatomy（如向 Button 加图标、角标）',
        '在 app.css 中覆盖组件的 inline-size、背景色',
        '使用 div/span 模拟 button 点击行为',
        '把页面级临时结构声明为正式组件规范',
        '三个及以上按钮并列',
        '使用 display: none/flex 做页面切换'
      ]) +

      forbSection('布局禁止', [
        '无主次结构的页面',
        '多个核心视觉重心同时存在',
        '混乱混用 M/G 模式',
        '浏览器默认滚动条可见',
        '页面使用 min-height 代替 100vh/100dvh'
      ]) +

      forbSection('交互禁止', [
        '不可恢复操作（删除、清空不提供确认和撤销）',
        '高风险操作无确认、无后果说明、无取消路径',
        '推广信息打断用户当前任务',
        '只提示失败，不提供下一步',
        '用静态 DOM 同时陈列所有状态代替真实状态转换'
      ]) +

      forbSection('文案禁止', [
        '只有"确定"，不说明具体结果',
        '恐吓式表达',
        '技术术语出现在用户可见错误提示中',
        '空状态不说明当前状态和下一步操作'
      ]);
  }

  function forbSection(title, items) {
    var html = '<div class="section"><h2 class="section-title">' + title + '</h2><div class="forbidden-list">';
    items.forEach(function (item) {
      html += '<div class="forbidden-item"><span class="forbidden-icon">✕</span><span>' + item + '</span></div>';
    });
    html += '</div></div>';
    return html;
  }
})();
