# KuiklyUI 文档

本文档库是腾讯官方 [KuiklyUI/docs](https://github.com/Tencent-TDS/KuiklyUI/tree/main/docs) 的一个fork。 KuiklyUI 是基于 Kotlin 多平台（KMP）构建的跨平台 UI 开发框架，支持 Android、iOS、HarmonyOS、H5/Web 和微信小程序。

## 📚 文档结构

- **[基础参考文档](./basic_reference.md)** - **最重要的核心文档**
- [API 文档](./API/) - 详细的 API 接口说明
- [开发指南](./DevGuide/) - 完整的开发教程和最佳实践
- [快速开始](./QuickStart/) - 项目初始化和入门指南（包含原生侧桥接指南）
- [介绍](./Introduction/) - 框架概述和特性介绍
- [问答](./QA/) - 常见问题解答
- [博客](./Blog/) - 技术文章和案例分享（包含 Kuikly 原理）

## ✍️ 项目架构

将该文档库（docs）克隆到 Kuikly 项目根目录 (`kuikly_shared`) 下
```plaintext
项目结构
kuikly_shared/                   # Kuikly 项目根目录
├── docs/                        # 本文档项目
│   ├── basic_reference.md       # 基础参考文档（**需要添加到上下文中**）
│   ├── API/                     # API 文档
│   ├── DevGuide/                # 开发指南
│   ├── (...)
├── src/                         # 代码
├── build/                       # 构建输出
├── build.gradle.kts             # 项目构建脚本
├── settings.gradle.kts          # 项目设置
├── (...)
```

## ⭐ 重要提示：LLM 交互时的上下文使用

**`basic_reference.md` 是本文档库中最重要的文件**，包含了 KuiklyUI 框架的完整参考信息。

### 在与 LLM 进行 KuiklyUI 相关对话时，请务必：

1. **将 `basic_reference.md` 添加到对话上下文中**
2. **优先参考该文档中的语法、API 和示例**
3. **确保生成的代码符合文档中的规范**

该文档包含：
- 框架架构说明
- 页面（Pager）和组件（ComposeView）的生命周期和声明
- 所有提供的 UI 组件的使用方法
- 状态管理和数据绑定
- 路由和导航
- 样式系统

### 提示词案例
- “参考 @docs/basic_reference.md 中的指南，帮我写一个 Button 组件，支持自定义高度和背景颜色。”
- “参考 @docs/Refactor/refactoring-best-practices.md 和 @docs/basic_reference.md 中的指南，帮我重构 Toast 组件，使用私有方法分离样式。”
- “在 @docs 中查找 ComposeView 组件的生命周期函数。”

## 学习指南

### 新手开发者
1. 阅读 [介绍](./Introduction/) 了解框架概念
2. 参考 [API](./API/) 和 [开发指南](./DevGuide/) 学习框架使用
3. 英语好的人直接参考 [基础参考文档](./basic_reference.md) ，以最快速度学习核心概念

### 进一步了解
1. 查看 [基础参考文档](./basic_reference.md) 了解 API
2. 浏览 [入门](./Introduction/) 和 [博客](./Blog/) 学习 Kuikly 框架原理

---

**注意**：本文档持续更新中，建议关注最新版本以获取准确信息。