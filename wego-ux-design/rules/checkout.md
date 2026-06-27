# Checkout Rules

> 微购 Design System Skill / rules
> Version 4.0
> 本文档定义 AI 输出前必须执行的最终检查清单。对照阶段二《设计库消费计划》验证，而非泛泛检查。硬性约束（hardConstraints）以 `design-library/library-consumption.json` 为准。

---

# 1. Step 1：验证

**方式 A：浏览器验证（环境支持时）**

```text
□ 关键交互链路可操作（对照阶段二状态覆盖）
□ 控制台无阻断错误
□ 资源加载成功（字体、图标、图片）
□ 响应式表现合理（max-width 基准 + 宽屏验证）
```

执行方式：

- 能启动本地服务并打开浏览器时，必须执行方式 A，不得跳过后在最终回复中补一句"没有额外做浏览器视觉回归"
- 方式 A 未执行时，必须在最终输出的"验证结果"中明确写明降级原因

**方式 B：静态代码审查（环境不支持浏览器时）**

```text
□ 资源路径在交付目录内可解析（字体、图标、图片文件存在）
□ CSS 中所有颜色、间距、字号、圆角通过 var(--wg-*) 引用
□ JavaScript 中状态转换逻辑完整覆盖阶段二状态覆盖
□ HTML 语义结构正确，无内联业务 CSS 和 JavaScript
□ 样式加载顺序正确：tokens.css → scaffold.css → iconfont.css → components.css → app.css
```

**方式 C：移动端真机验证（AI 自动执行）**

AI 在验证通过后自动部署，无需用户手动操作：

1. 检查 Vercel 授权：`npx vercel whoami`
   - 已授权 → 直接部署
   - 未授权 → 提示用户执行一次 `npx vercel login`，授权后继续
2. 部署：`npx vercel --prod --yes`
3. 将返回的公网链接写入最终输出

输出约束：

- 已完成交付时，不得写"没有额外做线上部署""未额外部署"这类免责声明
- 未拿到公网链接时，必须明确说明是 `npx vercel login` 未完成、CLI 故障，还是其他部署门禁阻断
- 若部署门禁阻断，最终输出必须标注"在线链接：阻断"，不得留空或写成已完成任务后的附带说明

部署项见 `rules/execution.md#2.4` 自动部署步骤。
对照阶段二《设计库消费计划》逐项验证是否落地。

## 2.1 页面壳与 ui_kit

```text
□ 页面粗类型是否明确，并与页面目标相符（对照 page-layout.json pageTypes）
□ 是否按 page-layout.json 选择了正确的布局模式（M/G）
□ 是否按 `ui_kits/index.json` 完成页面模式匹配
□ 命中 ui_kit 时，是否读取并遵守对应 `quality-report.json`
□ 未命中 ui_kit 时，是否按 `rules/execution.md#4` 标注缺失
□ openMode / background / maxWidth / 固定区是否落地
□ NavBar 左侧为取消或关闭叉的全屏模块是否使用 present-bottom
□ 页面背景色与 NavBar 背景色是否联动（对照 page-layout.json pageBackground.navbarLinkage）
□ 页面主体最大宽度是否 ≤ --wg-layout-page-max-width
□ 页面高度、滚动区、固定区和底部安全距离是否正确
□ 滚动区域是否隐藏浏览器默认滚动条
□ 页面转场是否使用 Push/Present/Fade 动画而非 display:none 硬切
□ M/G 模式是否通过 scaffold 工具类表达，而非在 app.css 中手写 padding-inline / gap
```

## 2.2 组件消费

```text
□ 命中组件是否来自 `design-library/components/index.json`
□ 每个命中组件是否读取对应 contract 与 preview 文件
□ 组件 markup 是否通过 @component-markup-start/end 标记定位，从 preview 复制
□ 组件 markup 的 class、modifier、DOM anatomy 是否未被改写
□ 命中组件的 Canonical CSS 是否逐字复制写入 styles/components.css
□ 组件状态和变体是否来自契约 variantDimensions，未自创组件变体
□ 未注册结构是否使用页面级命名，且未使用 `.wg-{component}` 命名
□ 未注册结构具备复用价值时是否标注为组件候选
□ 是否先组织页面，再选择组件（禁止从组件拼页面）
□ 同一业务动作是否只有一个 primary / strong
□ 重复业务动作是否已降级为 text / weak / secondary
□ 同一个 form group 内是否左右对齐统一
□ 组件交互是否可点击并同步原生属性或 ARIA 状态
```

## 2.3 资源与 Token

```text
□ 资源消费是否仅包含当前页面实际使用的 iconfont / app icon / media / video
□ iconfont 资源目录结构是否完整（iconfont.css 与字体文件在同一目录）
□ 样式加载顺序是否为 tokens.css → scaffold.css → iconfont.css → components.css → app.css
□ 业务 CSS 是否全部通过 var(--wg-*) 使用设计值
□ Token 定义层之外是否没有 HEX / RGBA / 裸 px / rem 等硬编码设计值
□ 页面级业务样式是否没有覆盖组件内部 Token
```

## 2.4 状态覆盖与交互链路

```text
□ 阶段二状态覆盖是否全部实现
□ 状态链路是否覆盖初始、输入、校验、处理中、成功、失败、恢复
□ Loading 是否表达具体任务，不是空转圈
□ 错误修正后是否清除 error 状态（error class、错误文案、aria-invalid、边框/背景色）
□ 关键状态是否通过真实交互转换，而不是静态并列展示
□ 不可逆操作是否有确认文案、后果说明、取消路径、失败恢复
```

---

# 3. Step 3：合规验证

对照 `design-library/library-consumption.json` → `hardConstraints` 逐项验证：

```text
□ 业务 CSS 无硬编码设计值
□ 未自创正式组件变体
□ 无装饰性视觉（复杂渐变、重阴影、多层卡片）
□ HTML 不内联业务 CSS
□ HTML 不内联业务 JavaScript
□ 文案清晰，操作文案使用动词
□ 空状态说明当前状态
□ 错误状态有恢复路径
□ 危险操作说明后果
□ 避免恐吓式表达
□ 视觉风格简洁、干净、克制、淡雅、符合微信生态
□ 是否完成阶段二《设计库消费计划》
□ 组件 CSS 是否不存在非法单位
```

---

# 4. 最终交付检查

```text
□ 结果是否可执行
□ 结构是否清晰
□ 是否符合用户要求
□ 是否交付完整项目目录
□ HTML、CSS、JavaScript 是否分离
□ 本地资源路径是否有效
□ 是否包含入口和启动方式
□ 是否实际验证关键交互链路
□ 浏览器控制台是否无阻断错误
□ 验证结果是否明确写明"浏览器验证"或"静态代码审查降级"
□ 在线链接是否提供真实公网链接；若缺失，是否明确标注"阻断"及原因
□ 是否没有输出推理过程
□ 是否没有多余解释
□ 是否可直接交付开发
□ 项目根目录名是否使用中文、精简表达页面内容（禁止 prototype/demo/page1 等通用占位名）
□ iconfont 资源目录结构是否完整（iconfont.css 与字体文件在同一目录）
□ scaffold.css 是否已复制到 styles/scaffold.css 并在 HTML 中正确加载
```

---

# 5. 门禁规则

- 自查清单逐项通过后才允许输出
- 未通过项必须修复后重新验证
- 不得跳过任何步骤直接输出
- 不得在未完成阶段二设计产物时进入验证
- 如果任一关键项不满足，必须重新修改，不得交付
- 不得用"没有额外做浏览器视觉回归或线上部署"之类免责声明替代验证结果或阻断说明
