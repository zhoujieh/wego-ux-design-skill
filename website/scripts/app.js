/* ═══════════════════════════════════════════
   Wego Design System — 文档网站 SPA
   Hash 路由 + 视图渲染 + 侧边栏交互
   ═══════════════════════════════════════════ */

(function () {
  'use strict';

  // ── 工具函数 ──

  function h(tag, attrs, ...children) {
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
    children.forEach(function (c) {
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
    // 支持 tokens 子锚点（如 #/tokens#colors）
    var base = h.split('#')[0];
    var match = routes.filter(function (r) { return r.path === (h.indexOf('#') > 0 ? '#' + h.split('#')[1].split('#')[0] : h) || r.path === ('#' + h.replace('#/', '')); });
    // simpler: try exact match first, then fallback to home
    for (var i = 0; i < routes.length; i++) {
      if (routes[i].path === h) return routes[i];
    }
    // check for sub-page (e.g., #/tokens with anchor)
    if (h.indexOf('#/') === 0 && h.lastIndexOf('#') > 0) {
      var mainHash = h.substring(0, h.lastIndexOf('#'));
      for (var j = 0; j < routes.length; j++) {
        if (routes[j].path === mainHash) return routes[j];
      }
    }
    return routes[0];
  }

  // ── 侧边栏渲染 ──

  function renderSidebar(currentPath) {
    var groups = [
      { label: '', links: [
        { href: '#/', label: '首页', icon: '' }
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
        { href: '#/layout', label: '布局总览', sub: false }
      ]},
      { label: '组件', links: [
        { href: '#/components', label: '组件总览', sub: false },
        { href: '#/components/button', label: 'Button', sub: true }
      ]},
      { label: '', links: [
        { href: '#/forbidden', label: '禁止事项', sub: false }
      ]}
    ];

    sidebarNavEl.innerHTML = '';

    groups.forEach(function (group) {
      if (group.label) {
        var label = h('div', { class: 'sidebar-group-label' }, group.label);
        sidebarNavEl.appendChild(label);
      }
      group.links.forEach(function (link) {
        var isActive = currentPath === link.href ||
          (currentPath.indexOf('#/tokens') === 0 && link.href.indexOf('#/tokens') === 0 && currentPath === link.href);

        var cls = 'sidebar-link';
        if (link.sub) cls += ' sidebar-link--sub';
        if (isActive) cls += ' active';

        var a = h('a', { class: cls, href: link.href }, link.label);
        a.addEventListener('click', function (e) {
          e.preventDefault();
          var href = this.getAttribute('href');
          window.location.hash = href;
          if (window.innerWidth <= 768) {
            sidebarEl.classList.remove('open');
          }
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
  var views = {
    home: homeView,
    tokens: tokensView,
    layout: layoutView,
    components: componentsView,
    'component-button': componentButtonView,
    forbidden: forbiddenView
  };

  function render() {
    var hash = window.location.hash || '#/';
    var route = getRoute(hash);
    document.title = route.view === 'home' ? 'Wego Design System' : route.view + ' — Wego Design';
    renderSidebar(hash);
    mainEl.innerHTML = '';
    var fn = views[route.view];
    if (fn) fn(mainEl);
    scrollToAnchor();
  }

  window.addEventListener('hashchange', render);
  window.addEventListener('DOMContentLoaded', render);

  // ═══════════════════════════════════════════
  // 首页
  // ═══════════════════════════════════════════

  function homeView(container) {
    container.innerHTML = [
      '<div class="hero">',
        '<h1 class="hero-title">微购设计系统</h1>',
        '<p class="hero-desc">Wego Design System — 帮助商家以最小学习成本、时间成本和操作成本完成经营目标。简洁、干净、克制、高信息密度、微信生态一致。</p>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">设计决策优先级</h2>',
        '<div class="priority-chain">',
          '<span class="priority-item">清晰</span>',
          '<span class="priority-arrow">›</span>',
          '<span class="priority-item">一致</span>',
          '<span class="priority-arrow">›</span>',
          '<span class="priority-item">效率</span>',
          '<span class="priority-arrow">›</span>',
          '<span class="priority-item">美观</span>',
          '<span class="priority-arrow">›</span>',
          '<span class="priority-item">创新</span>',
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">5 条设计原则</h2>',
        '<div class="principle-grid">',
          '<div class="principle-card">',
            '<div class="principle-num">Principle 1</div>',
            '<div class="principle-name">降低认知成本</div>',
            '<div class="principle-desc">用户 3 秒内知道这里是什么、能做什么、下一步是什么。一个页面只保留一个主目标。</div>',
          '</div>',
          '<div class="principle-card">',
            '<div class="principle-num">Principle 2</div>',
            '<div class="principle-name">降低时间成本</div>',
            '<div class="principle-desc">减少等待、点击、输入、跳转、重复判断。自动优于选择、选择优于输入、批量优于单个。</div>',
          '</div>',
          '<div class="principle-card">',
            '<div class="principle-num">Principle 3</div>',
            '<div class="principle-name">复用用户经验</div>',
            '<div class="principle-desc">优先使用已有组件和常见微信式交互。不为创新而改变成熟路径。</div>',
          '</div>',
          '<div class="principle-card">',
            '<div class="principle-num">Principle 4</div>',
            '<div class="principle-name">建立用户信任</div>',
            '<div class="principle-desc">简洁克制的界面 + 数据化表达 + 明确说明操作结果。不可逆操作提供确认和恢复路径。</div>',
          '</div>',
          '<div class="principle-card">',
            '<div class="principle-num">Principle 5</div>',
            '<div class="principle-name">符合人性</div>',
            '<div class="principle-desc">用户怕损失、易出错、会产生情绪。设计必须承认这些事实，提供自动保存、撤销、恢复机制。</div>',
          '</div>',
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">核心设计哲学</h2>',
        '<div class="flex-col gap-16">',
          '<div class="card"><div class="card-title">经营优先</div><div class="card-desc">用户来到微购是为了完成经营行为。所有设计都服务于获客、转化、复购、效率和收益。禁止为视觉效果牺牲经营效率。</div></div>',
          '<div class="card"><div class="card-title">解决问题优先</div><div class="card-desc">没有设计，只有解决问题。设计师的个人表达不能高于用户问题。不得为了"更有设计感"添加无意义视觉元素。</div></div>',
          '<div class="card"><div class="card-title">432 原则</div><div class="card-desc">页面交互方式不超过 4 种，内容样式不超过 3 种，不为 20% 需求打扰 80% 用户。</div></div>',
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">快速导航</h2>',
        '<div class="nav-cards">',
          '<a href="#/tokens" class="nav-card"><div class="nav-card-icon">🎨</div><div class="nav-card-title">设计 Token</div><div class="nav-card-desc">颜色、排版、间距、圆角、阴影、动效等基础变量</div></a>',
          '<a href="#/layout" class="nav-card"><div class="nav-card-icon">📐</div><div class="nav-card-title">布局系统</div><div class="nav-card-desc">M0-M3 页边距、G1-G2 分组、页面类型、信息层级</div></a>',
          '<a href="#/components" class="nav-card"><div class="nav-card-icon">🧩</div><div class="nav-card-title">组件库</div><div class="nav-card-desc">Button、NavBar、Dialog 等 9 个已注册组件</div></a>',
          '<a href="#/forbidden" class="nav-card"><div class="nav-card-icon">🚫</div><div class="nav-card-title">禁止事项</div><div class="nav-card-desc">视觉、Token、组件、布局、交互的禁止模式</div></a>',
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">导航结构</h2>',
        '<div class="card">',
          '<div class="card-desc">首页</div>',
          '<div class="card-desc" style="padding-inline-start:24px;color:var(--wg-color-text-tertiary)">├─ 设计 Token（颜色 / 排版 / 间距 / 圆角 / 阴影 / 动效）</div>',
          '<div class="card-desc" style="padding-inline-start:24px;color:var(--wg-color-text-tertiary)">├─ 布局系统（M0-M3 / G1-G2 / 页面类型 / 信息层级 / 过渡动画）</div>',
          '<div class="card-desc" style="padding-inline-start:24px;color:var(--wg-color-text-tertiary)">├─ 组件库（9 组件总览 → Button 详情）</div>',
          '<div class="card-desc" style="padding-inline-start:24px;color:var(--wg-color-text-tertiary)">└─ 禁止事项</div>',
        '</div>',
      '</div>'
    ].join('\n');
  }

  // ═══════════════════════════════════════════
  // Token 页
  // ═══════════════════════════════════════════

  function tokensView(container) {
    container.innerHTML = [
      '<h1 class="page-title">设计 Token</h1>',
      '<p class="page-subtitle">所有设计值通过 CSS 自定义属性 <code style="background:var(--wg-color-bg-subtle);padding:2px 6px;border-radius:4px;font-size:13px;">var(--wg-*)</code> 使用。tokens.json 是唯一数据源，v3.2.0。</p>',

      // ── Color ──
      '<div class="section" id="colors">',
        '<h2 class="section-title">颜色 Colors</h2>',

        '<h3 class="section-subtitle">品牌色 & 功能色</h3>',
        '<div class="color-grid">',
          colorCard('#03C160', '品牌主色', '--wg-color-base-brand-500'),
          colorCard('#FA5051', '危险 / 错误', '--wg-color-base-danger-500'),
          colorCard('#208BF1', '信息提示', '--wg-color-base-info-500'),
          colorCard('#03C160', '成功', '--wg-color-base-success-500'),
          colorCard('#FA9D3B', '警告', '--wg-color-base-warning-500'),
          colorCard('#FF6045', '营销 / 促销', '--wg-color-base-promotion-500'),
          colorCard('#285B9A', '文本链接', '--wg-color-base-link-500'),
        '</div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">文字色 Text</h3>',
        '<div class="flex-col gap-8">',
          textColorSwatch('--wg-color-text-primary', '一级文字 Primary', '#1E2028'),
          textColorSwatch('--wg-color-text-secondary', '二级文字 Secondary', '#6E7382'),
          textColorSwatch('--wg-color-text-tertiary', '三级文字 Tertiary', '#9097A3'),
          textColorSwatch('--wg-color-text-disabled', '禁用文字 Disabled', '#B7BEC5'),
          textColorSwatch('--wg-color-text-inverse', '反色文字 Inverse', '#FFFFFF'),
          textColorSwatch('--wg-color-text-link', '链接文字 Link', '#285B9A'),
        '</div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">背景色 Background</h3>',
        '<div class="flex-col gap-8">',
          bgColorSwatch('--wg-color-bg-page', '页面背景 (灰底)', '#EDEDED'),
          bgColorSwatch('--wg-color-bg-surface', '容器表面 (白底)', '#FFFFFF'),
          bgColorSwatch('--wg-color-bg-subtle', '极浅灰背景', '#F8F9FA'),
          bgColorSwatch('--wg-color-bg-muted', '浅灰背景', '#F2F3F6'),
          bgColorSwatch('--wg-color-bg-active', '选中态背景', '#E9EAEF'),
        '</div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">交互状态 State</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Token</th><th>CSS Variable</th><th>用途</th></tr>',
          '<tr><td>wg.color.state.hover</td><td>--wg-color-state-hover</td><td>悬停态背景</td></tr>',
          '<tr><td>wg.color.state.pressed</td><td>--wg-color-state-pressed</td><td>按压态背景</td></tr>',
          '<tr><td>wg.color.state.selected</td><td>--wg-color-state-selected</td><td>选中态</td></tr>',
          '<tr><td>wg.color.state.disabled.bg</td><td>--wg-color-state-disabled-bg</td><td>禁用态背景</td></tr>',
          '<tr><td>wg.color.state.disabled.text</td><td>--wg-color-state-disabled-text</td><td>禁用态文字</td></tr>',
          '<tr><td>wg.color.state.focus</td><td>--wg-color-state-focus</td><td>焦点描边</td></tr>',
        '</table></div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">操作色 Action</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Token</th><th>CSS Variable</th><th>用途</th></tr>',
          '<tr><td>wg.color.action.primary.default</td><td>--wg-color-action-primary-default</td><td>主操作默认</td></tr>',
          '<tr><td>wg.color.action.primary.hover</td><td>--wg-color-action-primary-hover</td><td>主操作悬停</td></tr>',
          '<tr><td>wg.color.action.primary.pressed</td><td>--wg-color-action-primary-pressed</td><td>主操作按压</td></tr>',
          '<tr><td>wg.color.action.primary.disabled</td><td>--wg-color-action-primary-disabled</td><td>主操作禁用</td></tr>',
          '<tr><td>wg.color.action.secondary.default</td><td>--wg-color-action-secondary-default</td><td>次操作默认</td></tr>',
          '<tr><td>wg.color.action.danger.default</td><td>--wg-color-action-danger-default</td><td>危险操作默认</td></tr>',
          '<tr><td>wg.color.action.link.default</td><td>--wg-color-action-link-default</td><td>链接操作默认</td></tr>',
        '</table></div>',
      '</div>',

      // ── Typography ──
      '<div class="section" id="typography">',
        '<h2 class="section-title">排版 Typography</h2>',

        '<h3 class="section-subtitle">字体族</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Token</th><th>字体</th><th>用途</th></tr>',
          '<tr><td>wg.font.family.text</td><td style="font-family:var(--wg-font-family-text)">PingFang SC, -apple-system, ...</td><td>默认正文字体</td></tr>',
          '<tr><td>wg.font.family.number.decorative</td><td style="font-family:\'WegoKeyboard N9\'">WegoKeyboard N9</td><td>装饰数字（价格、指标）</td></tr>',
          '<tr><td>wg.font.family.system</td><td>系统默认</td><td>系统回退</td></tr>',
        '</table></div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">字号与行高</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Token</th><th>字号</th><th>行高</th><th>预览</th></tr>',
          '<tr><td>wg.font.size.f10</td><td>10px</td><td>14px</td><td style="font-size:10px;line-height:14px">微购设计系统</td></tr>',
          '<tr><td>wg.font.size.f12</td><td>12px</td><td>18px</td><td style="font-size:12px;line-height:18px">微购设计系统</td></tr>',
          '<tr><td>wg.font.size.f14</td><td>14px</td><td>20px</td><td style="font-size:14px;line-height:20px">微购设计系统</td></tr>',
          '<tr><td>wg.font.size.f16</td><td>16px</td><td>24px</td><td style="font-size:16px;line-height:24px">微购设计系统</td></tr>',
          '<tr><td>wg.font.size.f18</td><td>18px</td><td>26px</td><td style="font-size:18px;line-height:26px">微购设计系统</td></tr>',
          '<tr><td>wg.font.size.f22</td><td>22px</td><td>30px</td><td style="font-size:22px;line-height:30px;font-weight:600">微购设计系统</td></tr>',
        '</table></div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">字重</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Token</th><th>CSS Variable</th><th>值</th><th>预览</th></tr>',
          '<tr><td>wg.font.weight.regular</td><td>--wg-font-weight-regular</td><td>400</td><td style="font-weight:400;font-size:18px">Regular 常规</td></tr>',
          '<tr><td>wg.font.weight.medium</td><td>--wg-font-weight-medium</td><td>500</td><td style="font-weight:500;font-size:18px">Medium 中等</td></tr>',
          '<tr><td>wg.font.weight.semibold</td><td>--wg-font-weight-semibold</td><td>600</td><td style="font-weight:600;font-size:18px">Semibold 半粗</td></tr>',
        '</table></div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">数字专用字号</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Token</th><th>字号</th><th>预览</th></tr>',
          '<tr><td>wg.font.number.nf12</td><td>12px</td><td style="font-family:\'WegoKeyboard N9\',sans-serif;font-size:12px">¥1,234.56</td></tr>',
          '<tr><td>wg.font.number.nf16</td><td>16px</td><td style="font-family:\'WegoKeyboard N9\',sans-serif;font-size:16px">¥1,234.56</td></tr>',
          '<tr><td>wg.font.number.nf24</td><td>24px</td><td style="font-family:\'WegoKeyboard N9\',sans-serif;font-size:24px;font-weight:500">¥1,234.56</td></tr>',
          '<tr><td>wg.font.number.nf32</td><td>32px</td><td style="font-family:\'WegoKeyboard N9\',sans-serif;font-size:32px;font-weight:500">¥1,234.56</td></tr>',
        '</table></div>',
      '</div>',

      // ── Spacing ──
      '<div class="section" id="spacing">',
        '<h2 class="section-title">间距 Spacing</h2>',
        '<p class="card-desc" style="margin-block-end:16px">10 级间距体系，默认值 16px。</p>',
        spacingBar(0), spacingBar(2), spacingBar(4), spacingBar(8), spacingBar(12),
        spacingBar(16, true), spacingBar(24), spacingBar(32), spacingBar(40), spacingBar(48),
        '<h3 class="section-subtitle" style="margin-block-start:24px">触摸目标</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Token</th><th>值</th><th>用途</th></tr>',
          '<tr><td>wg.touch.min</td><td>40px</td><td>最小触摸目标</td></tr>',
          '<tr><td>wg.touch.default</td><td>44px</td><td>默认触摸目标</td></tr>',
          '<tr><td>wg.touch.comfortable</td><td>48px</td><td>舒适触摸目标</td></tr>',
        '</table></div>',
      '</div>',

      // ── Radius ──
      '<div class="section" id="radius">',
        '<h2 class="section-title">圆角 Radius</h2>',
        '<p class="card-desc" style="margin-block-end:16px">7 级圆角体系。默认使用 xs-sm，避免大圆角作为默认风格。</p>',
        '<div class="radius-grid">',
          radiusCell('none', '0px'),
          radiusCell('xs', '4px'),
          radiusCell('sm', '6px'),
          radiusCell('md', '8px'),
          radiusCell('lg', '12px'),
          radiusCell('xl', '16px'),
          radiusCell('full', '999px'),
        '</div>',
      '</div>',

      // ── Elevation ──
      '<div class="section" id="elevation">',
        '<h2 class="section-title">阴影 Elevation</h2>',
        '<p class="card-desc" style="margin-block-end:16px">默认无阴影。只有层级确实浮起时使用。</p>',
        '<div class="shadow-grid">',
          shadowCell('none', 'none'),
          shadowCell('xs', '0 1px 4px rgba(30,32,40,0.04)'),
          shadowCell('sm', '0 2px 8px rgba(30,32,40,0.06)'),
          shadowCell('md', '0 4px 16px rgba(30,32,40,0.08)'),
          shadowCell('lg', '0 8px 32px rgba(30,32,40,0.12)'),
          shadowCell('xl', '0 12px 48px rgba(30,32,40,0.16)'),
        '</div>',
      '</div>',

      // ── Motion ──
      '<div class="section" id="motion">',
        '<h2 class="section-title">动效 Motion</h2>',
        '<h3 class="section-subtitle">时长 Duration</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Token</th><th>CSS Variable</th><th>值</th><th>用途</th></tr>',
          '<tr><td>wg.motion.duration.instant</td><td>--wg-motion-duration-instant</td><td>0ms</td><td>瞬时</td></tr>',
          '<tr><td>wg.motion.duration.fast</td><td>--wg-motion-duration-fast</td><td>150ms</td><td>微交互、icon、toggle</td></tr>',
          '<tr><td>wg.motion.duration.normal</td><td>--wg-motion-duration-normal</td><td>250ms</td><td>页面转场、弹窗</td></tr>',
          '<tr><td>wg.motion.duration.slow</td><td>--wg-motion-duration-slow</td><td>350ms</td><td>复杂动画、引导</td></tr>',
          '<tr><td>wg.motion.duration.xslow</td><td>--wg-motion-duration-xslow</td><td>500ms</td><td>大型转场</td></tr>',
        '</table></div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">缓动 Easing</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Token</th><th>CSS Variable</th><th>函数</th><th>用途</th></tr>',
          '<tr><td>wg.motion.ease.linear</td><td>--wg-motion-ease-linear</td><td>linear</td><td>匀速</td></tr>',
          '<tr><td>wg.motion.ease.standard</td><td>--wg-motion-ease-standard</td><td>cubic-bezier(0.4,0,0.2,1)</td><td>标准缓入缓出</td></tr>',
          '<tr><td>wg.motion.ease.enter</td><td>--wg-motion-ease-enter</td><td>cubic-bezier(0,0,0.2,1)</td><td>进入（减速）</td></tr>',
          '<tr><td>wg.motion.ease.exit</td><td>--wg-motion-ease-exit</td><td>cubic-bezier(0.4,0,1,1)</td><td>退出（加速）</td></tr>',
          '<tr><td>wg.motion.ease.emphasized</td><td>--wg-motion-ease-emphasized</td><td>cubic-bezier(0.2,0,0,1)</td><td>强调动效（页面转场）</td></tr>',
        '</table></div>',
      '</div>'
    ].join('\n');
  }

  function colorCard(hex, name, cssVar) {
    return '<div class="color-card">' +
      '<div class="swatch-chip swatch-chip--lg" style="background:' + hex + '"></div>' +
      '<div class="flex-col"><span class="color-card-label">' + name + '</span><span class="color-card-value">' + cssVar + '</span></div>' +
    '</div>';
  }

  function textColorSwatch(cssVar, label, hex) {
    return '<div style="display:flex;align-items:center;gap:12px;padding:8px 12px;background:var(--wg-color-bg-surface);border-radius:var(--wg-radius-sm);border:var(--wg-stroke-width-hairline) solid var(--wg-color-border-subtle)">' +
      '<div style="inline-size:80px;block-size:32px;border-radius:var(--wg-radius-xs);background:' + hex + ';border:var(--wg-stroke-width-hairline) solid var(--wg-color-border-subtle)"></div>' +
      '<span style="font-size:var(--wg-font-size-14);color:var(--wg-color-text-primary)">' + label + '</span>' +
      '<span style="font-size:var(--wg-font-size-12);color:var(--wg-color-text-tertiary);margin-inline-start:auto">' + cssVar + '</span>' +
    '</div>';
  }

  function bgColorSwatch(cssVar, label, hex) {
    return '<div style="display:flex;align-items:center;gap:12px;padding:8px 12px;background:var(--wg-color-bg-surface);border-radius:var(--wg-radius-sm);border:var(--wg-stroke-width-hairline) solid var(--wg-color-border-subtle)">' +
      '<div style="inline-size:80px;block-size:32px;border-radius:var(--wg-radius-xs);background:' + hex + ';border:var(--wg-stroke-width-hairline) solid var(--wg-color-border-default)"></div>' +
      '<span style="font-size:var(--wg-font-size-14);color:var(--wg-color-text-primary)">' + label + '</span>' +
      '<span style="font-size:var(--wg-font-size-12);color:var(--wg-color-text-tertiary);margin-inline-start:auto">' + cssVar + '</span>' +
    '</div>';
  }

  function spacingBar(px, isDefault) {
    var width = Math.max(px * 4, 20);
    return '<div class="spacing-bar" style="inline-size:' + width + 'px;' + (isDefault ? 'background:var(--wg-color-base-brand-alpha-60)' : '') + '">' +
      '--wg-spacing-' + px + ' (' + px + 'px)' + (isDefault ? ' ← 默认' : '') +
    '</div>';
  }

  function radiusCell(name, value) {
    return '<div class="radius-cell">' +
      '<div class="radius-box" style="border-radius:' + value + '"></div>' +
      '<span class="radius-label">' + name + ' (' + value + ')</span>' +
    '</div>';
  }

  function shadowCell(name, value) {
    return '<div class="shadow-card" style="box-shadow:var(--wg-shadow-' + name + ')">' +
      '<div style="font-size:var(--wg-font-size-14);color:var(--wg-color-text-primary);margin-block-end:8px">' + name + '</div>' +
      '<div style="font-size:var(--wg-font-size-12);color:var(--wg-color-text-tertiary)">' + value + '</div>' +
    '</div>';
  }

  // ═══════════════════════════════════════════
  // 布局系统页
  // ═══════════════════════════════════════════

  function layoutView(container) {
    container.innerHTML = [
      '<h1 class="page-title">布局系统</h1>',
      '<p class="page-subtitle">移动端优先，设计基准 375px。布局基于 CSS Grid / Flexbox。</p>',

      // M0-M3
      '<div class="section">',
        '<h2 class="section-title">页边距模式 M0–M3</h2>',
        '<div class="table-wrap"><table>',
          '<tr><th>模式</th><th>Margin</th><th>375px 内容宽度</th><th>适用场景</th></tr>',
          '<tr><td><strong>M0</strong></td><td>8px</td><td>359px</td><td>高密度列表、下拉建议、搜索结果、筛选面板</td></tr>',
          '<tr><td><strong>M1</strong></td><td>0px</td><td>375px</td><td>通栏连续内容、沉浸式页面</td></tr>',
          '<tr><td><strong>M2</strong> ← 默认</td><td>16px</td><td>343px</td><td>大多数业务页面、卡片式布局</td></tr>',
          '<tr><td><strong>M3</strong></td><td>32px</td><td>311px</td><td>低密度聚焦页面、引导页</td></tr>',
        '</table></div>',
      '</div>',

      // G1-G2
      '<div class="section">',
        '<h2 class="section-title">分组模式 G1–G2</h2>',
        '<div class="table-wrap"><table>',
          '<tr><th>模式</th><th>内部间距</th><th>外部间距</th><th>适用场景</th></tr>',
          '<tr><td><strong>G1</strong></td><td>0px</td><td>16px</td><td>连续紧密信息（列表项、表单字段、连续文本）</td></tr>',
          '<tr><td><strong>G2</strong></td><td>8px</td><td>32px</td><td>宽松模块信息（卡片组、独立模块、信息分区）</td></tr>',
        '</table></div>',
      '</div>',

      // 页面类型
      '<div class="section">',
        '<h2 class="section-title">页面类型（6 种）</h2>',
        '<div class="table-wrap"><table>',
          '<tr><th>类型</th><th>特征</th><th>信息密度</th><th>典型滚动</th></tr>',
          '<tr><td><strong>浏览型</strong></td><td>内容展示为主，用户浏览信息</td><td>中-高</td><td>可滚动</td></tr>',
          '<tr><td><strong>操作型</strong></td><td>触发操作为主，完成特定任务</td><td>低-中</td><td>通常不滚动</td></tr>',
          '<tr><td><strong>表单型</strong></td><td>信息填写、参数设置</td><td>中</td><td>可滚动（长表单）</td></tr>',
          '<tr><td><strong>结果型</strong></td><td>操作完成后的反馈展示</td><td>低</td><td>不滚动</td></tr>',
          '<tr><td><strong>异常型</strong></td><td>错误、权限不足、过期等异常</td><td>低</td><td>不滚动</td></tr>',
          '<tr><td><strong>空状态</strong></td><td>无数据、无内容</td><td>低</td><td>不滚动</td></tr>',
        '</table></div>',
      '</div>',

      // 信息层级
      '<div class="section">',
        '<h2 class="section-title">信息层级（1–4 级）</h2>',
        '<div class="table-wrap"><table>',
          '<tr><th>层级</th><th>定义</th><th>视觉权重</th><th>示例</th></tr>',
          '<tr><td><strong>一级 L1</strong></td><td>页面核心目标 / 关键结果 / 主标题</td><td>最高，唯一视觉重心</td><td>页面标题、操作结果、核心数据</td></tr>',
          '<tr><td><strong>二级 L2</strong></td><td>主要内容 / 主要表单 / 主要列表</td><td>中等</td><td>卡片内容、表单字段、列表项</td></tr>',
          '<tr><td><strong>三级 L3</strong></td><td>辅助说明 / 状态解释 / 次要信息</td><td>弱化</td><td>帮助文字、备注、状态标签</td></tr>',
          '<tr><td><strong>四级 L4</strong></td><td>弱提示 / 时间戳 / 标签 / 占位内容</td><td>最弱</td><td>时间、来源、水印、placeholder</td></tr>',
        '</table></div>',
        '<div class="card" style="margin-block-start:16px">',
          '<div class="card-title">规则</div>',
          '<ul class="usage-list">',
            '<li>一个页面只允许一个核心视觉重心（L1）</li>',
            '<li>主操作必须清晰可见</li>',
            '<li>辅助信息必须弱化，不能和主信息抢权重</li>',
            '<li>状态信息必须靠近对应对象</li>',
            '<li>同一区域不超过三级文字层级</li>',
          '</ul>',
        '</div>',
      '</div>',

      // 页面背景色规则
      '<div class="section">',
        '<h2 class="section-title">页面背景色规则</h2>',
        '<div class="table-wrap"><table>',
          '<tr><th>场景</th><th>背景色</th><th>示例</th></tr>',
          '<tr><td>多卡片/多模块页面</td><td><strong>bg-page</strong>（灰底 #EDEDED）+ 卡片用 bg-surface（白色）</td><td>列表页、设置页、管理页</td></tr>',
          '<tr><td>聚焦型单任务页面</td><td><strong>bg-surface</strong>（白底）整体</td><td>登录、结果、详情、表单提交</td></tr>',
          '<tr><td>二级页面 — 上级白底</td><td>继承上级白底</td><td>登录 → 注册</td></tr>',
          '<tr><td>二级页面 — 上级灰底</td><td>按自身内容独立选择</td><td>首页 → 详情（白底）</td></tr>',
        '</table></div>',
      '</div>',

      // 页面高度 & 滚动
      '<div class="section">',
        '<h2 class="section-title">页面高度与滚动</h2>',
        '<div class="card">',
          '<ul class="usage-list">',
            '<li>页面容器默认占满一屏：<code>block-size: 100vh</code>（兼容使用 <code>100dvh</code>），不使用 <code>min-height</code></li>',
            '<li>内容不超出一屏：<code>overflow: hidden</code>，禁止滚动</li>',
            '<li>内容超出一屏：<code>overflow-y: auto</code>，允许滚动</li>',
            '<li>所有可滚动区域必须隐藏浏览器默认滚动条</li>',
            '<li>表单型、结果型、聚焦型 → 通常不滚动；浏览型、列表型 → 通常可滚动</li>',
          '</ul>',
        '</div>',
      '</div>',

      // 页面转场
      '<div class="section">',
        '<h2 class="section-title">页面转场动画</h2>',
        '<p class="card-desc" style="margin-block-end:12px">页面切换必须模拟 App 原生导航体验，禁止使用 <code>display: none</code> 硬切。</p>',
        '<div class="table-wrap"><table>',
          '<tr><th>类型</th><th>进入方向</th><th>时长</th><th>缓动</th><th>适用场景</th></tr>',
          '<tr><td><strong>Push 推入</strong></td><td>从右滑入 → 向右滑出</td><td>250ms</td><td>emphasized</td><td>层级深入：详情、表单、子页面</td></tr>',
          '<tr><td><strong>Present 弹出</strong></td><td>从底部滑入 → 向底部滑出</td><td>250ms</td><td>emphasized</td><td>独立流程：绑定手机号、授权、全屏操作</td></tr>',
          '<tr><td><strong>Fade 淡入</strong></td><td>渐显 → 渐隐</td><td>150ms</td><td>standard</td><td>同级切换：Tab 切换、模式切换</td></tr>',
        '</table></div>',

        '<div class="card" style="margin-block-start:16px">',
          '<div class="card-title">返回按钮规则</div>',
          '<ul class="usage-list">',
            '<li>推入进入 → 返回时向右滑出</li>',
            '<li>弹出进入 → 返回时向底部滑出</li>',
            '<li>淡入进入 → 返回时渐隐</li>',
            '<li>返回按钮必须绑定 click 事件，调用视图切换函数</li>',
          '</ul>',
        '</div>',
      '</div>',

      // 页面宽度
      '<div class="section">',
        '<h2 class="section-title">页面宽度约束</h2>',
        '<div class="table-wrap"><table>',
          '<tr><th>页面类型</th><th>最大宽度</th><th>适用场景</th></tr>',
          '<tr><td>默认业务页面</td><td>670px</td><td>大多数表单、详情、列表页面</td></tr>',
          '<tr><td>沉浸式页面</td><td>无限制</td><td>视频播放、图片预览等全屏内容</td></tr>',
        '</table></div>',
        '<p class="card-desc" style="margin-block-start:8px">实现：<code>max-inline-size: var(--wg-layout-page-max-width)</code> + <code>margin-inline: auto</code></p>',
      '</div>',

      // 432 原则
      '<div class="section">',
        '<h2 class="section-title">432 原则</h2>',
        '<div class="card">',
          '<div class="flex-col gap-16">',
            '<div><strong style="color:var(--wg-color-base-brand-500)">4</strong> — 页面交互方式不超过 4 种（点击、输入、选择、滑动等）</div>',
            '<div><strong style="color:var(--wg-color-base-brand-500)">3</strong> — 页面内容样式不超过 3 种（标题、正文、辅助说明等）</div>',
            '<div><strong style="color:var(--wg-color-base-brand-500)">2</strong> — 不为 20% 需求的少数用户打扰 80% 用户</div>',
          '</div>',
        '</div>',
      '</div>'
    ].join('\n');
  }

  // ═══════════════════════════════════════════
  // 组件总览
  // ═══════════════════════════════════════════

  function componentsView(container) {
    container.innerHTML = [
      '<h1 class="page-title">组件库</h1>',
      '<p class="page-subtitle">9 个已注册组件，按类别分组。点击卡片查看详情。</p>',

      '<div class="section">',
        '<h2 class="section-title">操作 Action</h2>',
        '<div class="component-grid">',
          compCardLink('#/components/button', 'Button', '按钮', '触发明确操作。提交、保存、确认、下一步。支持 page/container/compact 三种 Scope 和 strong/medium/weak 三种 Emphasis。', 'stable'),
          compCardWip('Link', '链接', '页面跳转或行内命令操作。支持 standalone/inline 两种 Context 和 navigation/command 两种 Behavior。'),
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">导航 Navigation</h2>',
        '<div class="component-grid">',
          compCardWip('NavBar', '导航栏', '页面顶部导航和标题。支持 standard/title-only/search 三种模式，左按钮支持 back/close/text。'),
          compCardWip('Tabs', '标签栏', '页面内容切换。支持 standard/mini 两种尺寸和 divide/scroll 两种布局。'),
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">反馈 Feedback</h2>',
        '<div class="component-grid">',
          compCardWip('Dialog', '对话框', '模态弹窗，用于确认、提示、警告。支持 text/title/status/custom 四种变体。'),
          compCardWip('ActionSheet', '操作表', '底部弹出操作面板。支持 action/select 两种模式和多种 header 配置。'),
          compCardWip('Toast', '轻提示', '操作结果反馈，自动消失。支持 default/action 两种变体。'),
          compCardWip('Result', '结果页', '操作结果展示。支持 3 种布局和 10+ 图像类型。'),
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">表单 Form</h2>',
        '<div class="component-grid">',
          compCardWip('Input', '输入框', '文本/多行/数字输入。支持 full/card 两种布局和完整的校验状态。'),
        '</div>',
      '</div>'
    ].join('\n');
  }

  function compCardLink(href, name, category, desc, status) {
    return '<a href="' + href + '" class="comp-card">' +
      '<div class="comp-card-header"><span class="comp-card-name">' + name + '</span><span class="badge badge--' + status + '">稳定</span></div>' +
      '<div class="comp-card-category">' + category + '</div>' +
      '<div class="comp-card-desc">' + desc + '</div>' +
    '</a>';
  }

  function compCardWip(name, category, desc) {
    return '<div class="comp-card comp-card--wip">' +
      '<div class="comp-card-header"><span class="comp-card-name">' + name + '</span><span class="badge badge--wip">待补充</span></div>' +
      '<div class="comp-card-category">' + category + '</div>' +
      '<div class="comp-card-desc">' + desc + '</div>' +
    '</div>';
  }

  // ═══════════════════════════════════════════
  // Button 详情
  // ═══════════════════════════════════════════

  function componentButtonView(container) {
    container.innerHTML = [
      '<h1 class="page-title">Button 按钮</h1>',
      '<p class="page-subtitle">操作 Action · 状态：稳定 Stable · 交互模式：纯 CSS</p>',

      // 使用场景
      '<div class="section">',
        '<h2 class="section-title">使用决策</h2>',
        '<div class="flex-row gap-24">',
          '<div class="card" style="flex:1">',
            '<div class="card-title">✓ 使用 Button</div>',
            '<ul class="usage-list">',
              '<li>提交、保存、发布、完成、确认等会执行动作的操作</li>',
              '<li>推进流程的下一步操作</li>',
              '<li>局部容器内最重要的功能操作</li>',
              '<li>卡片、列表项或横条区域中的紧凑操作</li>',
            '</ul>',
          '</div>',
          '<div class="card" style="flex:1">',
            '<div class="card-title">✗ 不使用 Button</div>',
            '<ul class="usage-list usage-list--dont">',
              '<li>页面跳转但不执行动作 → 使用 Link 或可点击 Cell</li>',
              '<li>标签切换 → 使用 Tabs 或 Segmented Control</li>',
              '<li>只有图标且无稳定图标规范 → 暂不生成</li>',
              '<li>三个及以上并列操作 → 保留主要操作，其余进入更多菜单</li>',
            '</ul>',
          '</div>',
        '</div>',
      '</div>',

      // 决策维度
      '<div class="section">',
        '<h2 class="section-title">决策维度</h2>',
        '<p class="card-desc" style="margin-block-end:12px">Button 只有三个决策维度：<strong>scope</strong>（影响范围）、<strong>emphasis</strong>（操作优先级）、<strong>state</strong>（交互状态）。</p>',

        '<h3 class="section-subtitle">Scope 影响范围</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Scope</th><th>应用场景</th><th>视觉高度</th><th>宽度规则</th></tr>',
          '<tr><td><strong>page</strong></td><td>页面级主要操作、流程推进、结果页操作</td><td>48px</td><td>单个：180px；成对：120px×2；表单：自适应</td></tr>',
          '<tr><td><strong>container</strong></td><td>卡片、模块、局部区域内的核心操作</td><td>40px</td><td>自适应容器，最大 420px</td></tr>',
          '<tr><td><strong>compact</strong></td><td>列表、导航栏、横幅、卡片行内操作</td><td>32px</td><td>跟随内容，最大 120px</td></tr>',
        '</table></div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">Emphasis 操作优先级</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Emphasis</th><th>含义</th><th>样式</th><th>组合规则</th></tr>',
          '<tr><td><strong>strong</strong></td><td>最重要、推荐或推进流程的操作</td><td>品牌绿色背景 + 白色文字</td><td>同一区域只有一个 strong</td></tr>',
          '<tr><td><strong>medium</strong></td><td>有明确功能但不需要重点引导</td><td>浅灰背景 + 品牌绿色文字</td><td>仅用于单按钮场景</td></tr>',
          '<tr><td><strong>weak</strong></td><td>次要、取消、关闭等不需强调的操作</td><td>浅灰背景 + 一级文字色</td><td>双按钮允许 strong+weak 或 weak+weak</td></tr>',
        '</table></div>',

        '<h3 class="section-subtitle" style="margin-block-start:24px">允许组合</h3>',
        '<div class="table-wrap"><table>',
          '<tr><th>Scope</th><th>单按钮</th><th>双按钮</th><th>三个及以上</th></tr>',
          '<tr><td>page</td><td>strong / medium / weak</td><td>只允许 strong + weak</td><td>禁止</td></tr>',
          '<tr><td>container</td><td>strong / medium / weak</td><td>strong+weak 或 weak+weak</td><td>禁止</td></tr>',
          '<tr><td>compact</td><td>strong / medium / weak</td><td>strong+weak 或 weak+weak</td><td>最多两个，其余进入更多菜单</td></tr>',
        '</table></div>',
      '</div>',

      // 静态效果预览
      '<div class="section">',
        '<h2 class="section-title">效果预览</h2>',
        '<p class="card-desc" style="margin-block-end:12px">3 种 Scope × 3 种 Emphasis 的组合效果。每列是一个 scope，每行是一个 emphasis。</p>',
        '<div class="preview-area">',
          '<div class="preview-grid">',
            // page column
            '<div class="preview-col">',
              '<div class="preview-col-label">page (48px)</div>',
              buttonPreview('page', 'strong', '完成'),
              buttonPreview('page', 'medium', '了解更多'),
              buttonPreview('page', 'weak', '取消'),
            '</div>',
            // container column
            '<div class="preview-col">',
              '<div class="preview-col-label">container (40px)</div>',
              buttonPreview('container', 'strong', '确认退款'),
              buttonPreview('container', 'medium', '查看详情'),
              buttonPreview('container', 'weak', '取消'),
            '</div>',
            // compact column
            '<div class="preview-col">',
              '<div class="preview-col-label">compact (32px)</div>',
              buttonPreview('compact', 'strong', '再来一次'),
              buttonPreview('compact', 'medium', '复制'),
              buttonPreview('compact', 'weak', '删除'),
            '</div>',
          '</div>',
        '</div>',
      '</div>',

      // 状态
      '<div class="section">',
        '<h2 class="section-title">状态 States</h2>',
        '<div class="table-wrap"><table>',
          '<tr><th>State</th><th>HTML / CSS 表达</th><th>规则</th></tr>',
          '<tr><td>default</td><td>默认 class</td><td>正常可用</td></tr>',
          '<tr><td>hover</td><td><code>:hover</code></td><td>仅用于桌面预览，不作为移动端必需状态</td></tr>',
          '<tr><td>pressed</td><td><code>:active</code></td><td>只改变背景色，不位移、不缩放</td></tr>',
          '<tr><td>focus-visible</td><td><code>:focus-visible</code></td><td>必须显示清晰焦点描边</td></tr>',
          '<tr><td>disabled</td><td><code>disabled</code> 属性</td><td>统一禁用背景+文字，cursor: not-allowed</td></tr>',
        '</table></div>',
        '<p class="card-desc" style="margin-block-start:8px;color:var(--wg-color-text-tertiary)">V1 未定义 loading、success、error 视觉变体。这些需求通过 disabled + aria-busy + 页面级反馈区域实现。</p>',
      '</div>',

      // 宽度策略
      '<div class="section">',
        '<h2 class="section-title">宽度策略（page 级）</h2>',
        '<div class="table-wrap"><table>',
          '<tr><th>页面类型</th><th>策略</th><th>实现</th></tr>',
          '<tr><td>表单型（登录、注册、设置）</td><td>自适应容器宽度</td><td>给 wg-button-group 加 --form 修饰符</td></tr>',
          '<tr><td>结果型（操作成功/失败）</td><td>固定宽度 180px</td><td>使用默认 --single 模式</td></tr>',
          '<tr><td>浏览型底部操作栏</td><td>自适应容器宽度</td><td>给 wg-button-group 加 --form 修饰符</td></tr>',
        '</table></div>',
      '</div>',

      // 文案规则
      '<div class="section">',
        '<h2 class="section-title">文案规则</h2>',
        '<div class="card">',
          '<ul class="usage-list">',
            '<li>使用能说明结果的动词或动宾短语，如"保存""发布商品""确认退款"</li>',
            '<li>避免只有"确定"，能说明具体结果时必须写清结果</li>',
            '<li>单行展示，不换行</li>',
            '<li>同组按钮文案使用一致的语法结构</li>',
            '<li>危险操作必须写明对象和后果</li>',
          '</ul>',
        '</div>',
      '</div>',

      // Anatomy
      '<div class="section">',
        '<h2 class="section-title">Anatomy</h2>',
        '<div class="card">',
          '<pre style="font-size:13px;line-height:1.8;color:var(--wg-color-text-secondary)">button.wg-button.wg-button--{scope}.wg-button--{emphasis}\n└── span.wg-button__surface\n    └── span.wg-button__label</pre>',
          '<p class="card-desc" style="margin-block-start:8px">V1 仅允许文字按钮。不得自行加入图标、角标、副标题或加载图标。</p>',
        '</div>',
      '</div>'
    ].join('\n');

    // 为 disabled preview 设置 disabled 属性
    setTimeout(function () {
      var disabledBtn = container.querySelector('.preview-disabled');
      if (disabledBtn) disabledBtn.disabled = true;
    }, 0);
  }

  function buttonPreview(scope, emphasis, label) {
    var isDisabled = (scope === 'compact' && emphasis === 'weak');
    var disabledAttr = isDisabled ? ' disabled' : '';
    var disabledClass = isDisabled ? ' preview-disabled' : '';
    return '<div class="preview-row">' +
      '<span class="preview-row-label">' + emphasis + '</span>' +
      '<button class="wg-button wg-button--' + scope + ' wg-button--' + emphasis + disabledClass + '" type="button"' + disabledAttr + '>' +
        '<span class="wg-button__surface">' +
          '<span class="wg-button__label">' + label + '</span>' +
        '</span>' +
      '</button>' +
    '</div>';
  }

  // ═══════════════════════════════════════════
  // 禁止事项
  // ═══════════════════════════════════════════

  function forbiddenView(container) {
    container.innerHTML = [
      '<h1 class="page-title">禁止事项</h1>',
      '<p class="page-subtitle">设计系统强制执行规则，违反将导致设计不合规。</p>',

      '<div class="section">',
        '<h2 class="section-title">视觉禁止</h2>',
        '<div class="forbidden-list">',
          forbiddenItem('多个主目标 / 多个视觉焦点同时存在'),
          forbiddenItem('隐藏关键操作在深层菜单'),
          forbiddenItem('依赖用户记忆而非可见选项'),
          forbiddenItem('用装饰（阴影、渐变、复杂卡片）制造虚假层级'),
          forbiddenItem('复杂渐变、重阴影、多层卡片等装饰性视觉'),
          forbiddenItem('低龄化视觉风格、夸张营销表达、多处同时引导'),
          forbiddenItem('用高饱和色制造焦虑'),
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">Token 禁止</h2>',
        '<div class="forbidden-list">',
          forbiddenItem('业务 CSS 中硬编码 HEX/RGBA/px 设计值（必须使用 var(--wg-*)）'),
          forbiddenItem('使用随机间距、随机圆角、随机颜色'),
          forbiddenItem('用任意大数字解决 z-index 层级冲突'),
          forbiddenItem('为单页面新增 Token（Token 至少需要 3 个场景复用）'),
          forbiddenItem('通过临时 padding 伪造页面布局规则'),
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">组件禁止</h2>',
        '<div class="forbidden-list">',
          forbiddenItem('自创已注册组件的新变体（如自定义 Button 的 loading/danger/icon-only 变体）'),
          forbiddenItem('修改组件内部 Anatomy（如向 Button 加入图标、角标或副标题）'),
          forbiddenItem('在 app.css 中覆盖组件的 inline-size、背景色、圆角'),
          forbiddenItem('使用 div/span 模拟 button 的点击行为'),
          forbiddenItem('把页面级临时结构声明为正式组件规范'),
          forbiddenItem('三个及以上按钮并列（必须保留主要操作，其余进更多菜单）'),
          forbiddenItem('使用 display: none/flex 做页面切换（必须用 transition 动画）'),
          forbiddenItem('页面级临时结构使用 .wg-{component} 命名'),
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">布局禁止</h2>',
        '<div class="forbidden-list">',
          forbiddenItem('无主次结构的页面（必须明确一二级信息）'),
          forbiddenItem('多个核心视觉重心同时存在'),
          forbiddenItem('高密度页面过多留白；稀疏页面过度压缩'),
          forbiddenItem('混乱混用 M/G 模式'),
          forbiddenItem('伪造页面布局（通过临时 padding 模拟 M 值）'),
          forbiddenItem('浏览器默认滚动条可见（必须隐藏）'),
          forbiddenItem('页面使用 min-height 代替 100vh/100dvh'),
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">交互禁止</h2>',
        '<div class="forbidden-list">',
          forbiddenItem('不可恢复操作（如删除、清空不提供确认和撤销）'),
          forbiddenItem('高风险操作无确认、无后果说明、无取消路径'),
          forbiddenItem('推广信息打断用户当前任务流程'),
          forbiddenItem('非必要弹窗、重复确认、重复输入'),
          forbiddenItem('只提示失败，不提供下一步操作或恢复路径'),
          forbiddenItem('指责用户的错误提示（如"你输入错了"）'),
          forbiddenItem('用静态 DOM 同时陈列所有状态代替真实状态转换'),
          forbiddenItem('返回按钮无响应或响应后无动画'),
        '</div>',
      '</div>',

      '<div class="section">',
        '<h2 class="section-title">文案禁止</h2>',
        '<div class="forbidden-list">',
          forbiddenItem('只有"确定"，不说明具体结果'),
          forbiddenItem('恐吓式表达（如"不操作将失去所有数据"）'),
          forbiddenItem('技术术语出现在用户可见的错误提示中'),
          forbiddenItem('空状态不说明当前状态和下一步操作'),
          forbiddenItem('陈述显而易见的信息'),
        '</div>',
      '</div>'
    ].join('\n');
  }

  function forbiddenItem(text) {
    return '<div class="forbidden-item">' +
      '<span class="forbidden-icon">✕</span>' +
      '<span>' + text + '</span>' +
    '</div>';
  }
})();
