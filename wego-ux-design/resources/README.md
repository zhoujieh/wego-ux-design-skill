# Resource Assets

> 微购 Design System Skill / resources

本目录保存后续页面规则、业务场景和示例原型可复用的素材资源。资源是内容素材，不是组件规范入口。

## 资源边界

- `images/`：业务图片、场景图和组件预览所需图片。
- `fonts/`：品牌字体、键盘字体和 iconfont 元数据。
- `fonts/iconfont/iconfont.json`：查询图标 `font_class` 的权威来源。
- `fonts/iconfont/iconfont.css`、`woff2`、`woff`、`ttf`：生成原型时可复制的图标字体运行资源。

## 使用规则

- 只有需求、组件契约或规则明确需要素材时，才读取对应资源文件。
- 不扫描素材目录来发现组件；组件发现只从 `design-library/components/index.json` 开始。
- 复制资源时保持原目录结构，避免破坏 CSS 内部字体路径和原型相对路径。
- 图片、视频和 SVG 只作为内容或业务素材；尺寸、圆角、遮罩、层级和间距仍通过 Token 控制。
- iconfont 查询与 SVG 兜底规则以 `rules/icon-guidelines.md` 为准。
