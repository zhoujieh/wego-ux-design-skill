
# KuiklyUI 代码重构最佳实践

## 概述

本文档基于 KuiklyUI 框架的真实重构案例，总结了代码重构的最佳实践。这些原则和模式有助于保持代码质量，提高可维护性，并确保整个代码库的架构一致性。

## 目录

1. [重构原则](#重构原则)
2. [架构模式](#架构模式)
3. [组件统一策略](#组件统一策略)
4. [UI 分离技术](#ui-分离技术)
5. [API 设计最佳实践](#api-设计最佳实践)
6. [代码组织](#代码组织)
7. [命名规范](#命名规范)
8. [文档标准](#文档标准)
9. [实际案例：导航栏重构](#实际案例导航栏重构)

## 重构原则

### 1. 单一职责原则 (SRP)

每个组件应该有一个单一、明确定义的职责。重构时，识别承担过多职责的组件并适当拆分。

**重构前：**
```kotlin
// 单体导航栏组件处理所有变体
class NavBarView : ComposeView<NavBarAttr, NavBarEvent>() {
    override fun body(): ViewBuilder {
        return {
            // 复杂的条件逻辑处理不同导航栏类型
            if (attr.hasBackButton) {
                // 返回按钮逻辑
            } else if (attr.hasSearchButton) {
                // 搜索按钮逻辑
            } else if (attr.hasCustomButton) {
                // 自定义按钮逻辑
            }
            // ... 数百行混合逻辑
        }
    }
}
```

**重构后：**
```kotlin
// 统一架构的基础组件
internal class BaseNavBarView : ComposeView<BaseNavBarAttr, BaseNavBarEvent>() {
    // 专注于核心导航栏功能
}

// 特定用例的专门组件
internal class NavBarWithBackButtonView : ComposeView<NavBarWithBackButtonAttr, NavBarWithBackButtonEvent>() {
    // 只处理返回按钮变体
}
```

### 2. 不要重复自己 (DRY)

将通用功能提取到共享的基类或工具函数中。

**示例：**
```kotlin
// 通用常量提取到单一位置
private object NavBarConstants {
    const val DEFAULT_HEIGHT = 44f
    const val ICON_FONT_SIZE = 24f
    const val TEXT_FONT_SIZE = 16f
    const val BUTTON_WIDTH = 52f
    const val BUTTON_RADIUS = 6f
}
```

### 3. 开闭原则

组件应该对扩展开放，对修改关闭。策略性地使用组合和继承。

**示例：**
```kotlin
// 基类对扩展开放
internal open class BaseNavBarAttr : ComposeAttr() {
    open var operateText1: String = ""
    open var operateText2: String = ""
    open var operateText3: String = ""
}

// 扩展基础属性的专门属性
internal class NavBarButtonAttr : BaseNavBarAttr() {
    override var cancelText: String = "取消"
    override var buttonText: String = "按钮"
}
```

## 架构模式

### 1. 适当使用组合模式

在创建复杂组件时，可以使用组合模式。但是，组合模式并不总是最好的选择，需要根据情况具体评估是否需要使用组合模式。

**示例：**
```kotlin
// 使用组合构建复杂的导航栏变体
internal class NavBarWithBackButtonView : ComposeView<NavBarWithBackButtonAttr, NavBarWithBackButtonEvent>() {
    override fun body(): ViewBuilder {
        return {
            BaseNavBar {  // 与基础组件组合
                attr {
                    navBarType = NavBarType.WITH_BACK_BUTTON
                    // 配置特定属性
                }
                event {
                    backClick { ctx.event.backClick?.invoke() }
                }
            }
        }
    }
}
```

### 2. 变体的策略模式

使用枚举和策略模式来清晰地处理不同的组件变体。

**示例：**
```kotlin
enum class NavBarType {
    WITH_ACTIONS,
    WITH_BACK_BUTTON,
    WITH_CLOSE_BUTTON,
    WITH_SEARCH_BUTTON,
    WITH_CUSTOM_BUTTON
}

// 基础组件中的策略实现
private fun createLeftButton(view: ViewContainer<*, *>) {
    when (this@BaseNavBarView.attr.navBarType) {
        NavBarType.WITH_BACK_BUTTON -> createIconButton(NavBarIconType.BACK, view)
        NavBarType.WITH_CLOSE_BUTTON -> createIconButton(NavBarIconType.CLOSE, view)
        NavBarType.WITH_CUSTOM_BUTTON -> createCancelButton(view)
        // ... 其他策略
    }
}
```

## 使用私有方法分离 UI 部分

在一个组件（ComposeView）中，将复杂的 UI 构建逻辑分解为专门的私有方法，每个方法负责创建特定的 UI 部分，以提高代码可读性。

**核心原则：**
- 每个私有方法负责创建一个逻辑上独立的 UI 部分
- 方法名应该清楚地描述它创建的 UI 部分
- 将 UI 配置逻辑与布局逻辑分离

**示例：**
```kotlin
internal class BaseNavBarView : ComposeView<BaseNavBarAttr, BaseNavBarEvent>() {
    
    /**
     * 创建图标按钮的专门方法
     * 负责处理返回和关闭按钮的创建逻辑
     */
    private fun createIconButton(iconType: NavBarIconType, view: ViewContainer<*, *>) { // 在参数末尾传递当前 View
        val iconText = this@BaseNavBarView.getIconText(iconType)
        
        // 配置事件处理
        view.event {
            click {
                this@BaseNavBarView.event.backClick?.invoke()
            }
        }
        
        // 创建图标文本
        view.Text {
            attr {
                // 根据图标类型调整边距
                if(iconType == NavBarIconType.BACK)
                    margin(left = NavBarConstants.BUTTON_PADDING_HORIZONTAL + 4f, 
                           right = NavBarConstants.BUTTON_PADDING_HORIZONTAL - 4f)
                else 
                    margin(left = NavBarConstants.BUTTON_PADDING_HORIZONTAL, 
                           right = NavBarConstants.BUTTON_PADDING_HORIZONTAL)
                
                text(iconText)
                fontSize(NavBarConstants.ICON_FONT_SIZE)
                fontFamily(IconUnicodeManager.customFont_k)
                color(ColorManager.text_100)
            }
        }
    }
    
    /**
     * 创建取消按钮的专门方法
     * 处理自定义按钮导航栏中的取消按钮
     */
    private fun createCancelButton(view: ViewContainer<*, *>) {
        view.attr {
            padding(left = NavBarConstants.BUTTON_PADDING_HORIZONTAL * 2, 
                    right = NavBarConstants.BUTTON_PADDING_HORIZONTAL)
        }
        
        view.event {
            click {
                this@BaseNavBarView.event.backClick?.invoke()
            }
        }
        
        view.Text {
            attr {
                text(this@BaseNavBarView.attr.cancelText)
                maxWidth(NavBarConstants.CANCEL_TEXT_MAX_WIDTH)
                fontSize(NavBarConstants.TEXT_FONT_SIZE)
                lines(1)
                overflow(true)
                color(ColorManager.text_100)
            }
        }
    }
    
    /**
     * 创建右侧操作区域的专门方法
     * 根据导航栏类型创建不同的右侧内容
     */
    private fun createRightOperate(view: ViewContainer<*, *>) {
        when (this@BaseNavBarView.attr.navBarType) {
            NavBarType.WITH_ACTIONS, NavBarType.WITH_BACK_BUTTON, NavBarType.WITH_CLOSE_BUTTON -> {
                view.OperateAll {
                    attr {
                        barHeight = this@BaseNavBarView.attr.barHeight
                        operate1 = this@BaseNavBarView.attr.operate1
                        operate2 = this@BaseNavBarView.attr.operate2
                        operate3 = this@BaseNavBarView.attr.operate3
                    }
                }
            }
            NavBarType.WITH_CUSTOM_BUTTON -> this@BaseNavBarView.createCustomButton(view)
            NavBarType.WITH_SEARCH_BUTTON -> {/* 在 body() 中渲染成搜索框 */}
        }
    }
    
    /**
     * 创建自定义按钮的专门方法
     */
    private fun createCustomButton(view: ViewContainer<*,*>) {
        view.attr {
            height(this@BaseNavBarView.attr.barHeight)
            padding(left = NavBarConstants.BUTTON_PADDING_HORIZONTAL, 
                    right = NavBarConstants.BUTTON_PADDING_HORIZONTAL)
            allCenter()
        }
        
        view.Button {
            attr {
                setSize(ButtonSize.SMALL_32_CUSTOM)
                setColor(this@BaseNavBarView.attr.buttonColor)
                setConfig(ButtonConfig(
                    btnWidth = NavBarConstants.BUTTON_WIDTH,
                    text = truncateText(this@BaseNavBarView.attr.buttonText, 4),
                    textColor = Color.WHITE,
                    radius = NavBarConstants.BUTTON_RADIUS
                ))
            }
            event {
                click1 {
                    this@BaseNavBarView.event.operateClick?.invoke()
                }
            }
        }
    }
    
    /**
     * 创建搜索区域的专门方法
     */
    private fun createSearchArea(view: ViewContainer<*, *>) {
        view.View {
            attr {
                flex(1f)
            }
            Search {
                attr {
                    flex(1f)
                    isShowPicture = this@BaseNavBarView.attr.isShowPicture
                    picList = this@BaseNavBarView.attr.pics
                }
            }
        }
    }
}
```

### UI 分离的优势

**可读性提升：**
- [`body()`](src/commonMain/kotlin/com/truedian/wg/kuikly/navbar/NavBar.kt:291) 方法专注于整体布局结构
- 每个私有方法专注于特定 UI 部分的创建
- 代码逻辑更清晰，更容易理解

**可维护性提升：**
- 修改特定 UI 部分时，只需要修改对应的私有方法
- 减少了方法之间的耦合
- 更容易进行单元测试

**可复用性提升：**
- 私有方法可以在同一组件的不同地方复用
- 相似的 UI 创建逻辑可以提取为通用方法

### UI 分离的最佳实践

**方法命名规范：**
```kotlin
// 好的命名：清楚描述创建的内容
private fun createLeftButton()
private fun createRightOperate()
private fun createSearchArea()
private fun createIconButton()

// 避免的命名：模糊或不清楚
private fun doLayout()
private fun makeButton()
private fun handleStuff()
```

**方法职责划分：**
```kotlin
// 每个方法应该有明确的职责边界
private fun createLeftButton(view: ViewContainer<*, *>) {
    // 只负责创建左侧按钮，不处理其他逻辑
}

private fun createRightOperate(view: ViewContainer<*, *>) {
    // 只负责创建右侧操作区域
}

private fun calculateSpaceBalance() {
    // 只负责计算空间平衡，不创建 UI
}
```

**参数传递：**
```kotlin
// 传递必要的容器和配置参数
private fun createIconButton(iconType: NavBarIconType, view: ViewContainer<*, *>) {
    // iconType: 明确指定图标类型
    // view: 传递要添加内容的容器
}
```
## 使用私有方法分离样式部分

在组件重构中，将样式应用逻辑分离到专门的私有方法中，避免使用扩展函数，采用标准的方法参数传递模式，提高代码的可维护性和一致性。

**核心原则：**
- 将样式应用逻辑从主体方法中分离出来
- 使用私有方法而非扩展函数来处理样式
- 采用标准的参数传递模式，明确依赖关系
- 每个样式方法负责一个特定的样式应用场景

**重构前（使用扩展函数）：**
```kotlin
internal class ButtonView : ComposeView<ButtonAttr, ButtonEvent>() {
    
    override fun body(): ViewBuilder {
        return {
            Button {
                attr {
                    // 直接在 attr 块中调用扩展函数
                    if (config.isBrush) {
                        val colors = if (isPressed) config.clickColor else config.startColor
                        val startColor = colors.getOrNull(0) ?: Color.TRANSPARENT
                        val endColor = colors.getOrNull(1) ?: Color.TRANSPARENT
                        backgroundLinearGradient(
                            Direction.TO_RIGHT,
                            ColorStop(startColor, 0f),
                            ColorStop(endColor, 1f)
                        )
                    } else {
                        // ...
                    }
                }
            }
        }
    }
}
```

**重构后（使用私有方法分离样式）：**
```kotlin
import com.tencent.kuikly.core.base.ContainerAttr

internal class ButtonView : ComposeView<ButtonAttr, ButtonEvent>() {
    
    override fun body(): ViewBuilder {
        return {
            Button {
                attr {
                    // 调用专门的样式应用方法
                    ctx.applyBackgroundStyling(ctx, this) // remember to add prefix ctx. for all private methods
                }
            }
        }
    }
    
    /**
     * 根据配置应用背景样式的统一入口
     */
    private fun applyBackgroundStyling(ctx: ButtonView, attr: ContainerAttr) { // 在参数末尾传递当前 Attr
        val config = ctx.attr.buttonConfig
        
        if (config.isBrush) {
            ctx.applyGradientBackground(config, ctx.isPressed, attr)
        } else {
            ctx.applySolidBackground(config, ctx, attr)
        }
    }
    
    /**
     * 应用渐变背景，安全访问颜色
     */
    private fun applyGradientBackground(config: ButtonConfig, isPressed: Boolean, attr: ContainerAttr) {
        val colors = if (isPressed) config.clickColor else config.startColor
        
        // 安全访问颜色，带有回退机制
        val startColor = colors.getOrNull(0) ?: Color.TRANSPARENT
        val endColor = colors.getOrNull(1) ?: Color.TRANSPARENT

        attr.backgroundLinearGradient(
            Direction.TO_RIGHT,
            ColorStop(startColor, 0f),
            ColorStop(endColor, 1f)
        )

        /*
         if you need to add multiple attr, you can use like:
         attr.apply {
            backgroundLinearGradient(
                Direction.TO_RIGHT,
                ColorStop(startColor, 0f),
                ColorStop(endColor, 1f)
            )
            borderRadius(8f)
            padding(left = 8f, right = 8f)
         }
         */
    }
    
    /**
     * 应用纯色背景
     */
    private fun applySolidBackground(config: ButtonConfig, ctx: ButtonView, attr: ContainerAttr) {
        val backgroundColor = when {
            !config.isCanClick -> ColorManager.bg_gray_03
            ctx.isPressed -> ctx.attr.buttonColor.btnPreColor
            else -> ctx.attr.buttonColor.btnColor
        }
        attr.backgroundColor(backgroundColor)
    }
}
```

### 样式分离的优势

**代码清晰度提升：**
- [`body()`](src/commonMain/kotlin/com/truedian/wg/kuikly/button/Button.kt:69) 方法专注于组件结构，不包含复杂的样式逻辑
- 样式应用逻辑被封装在专门的私有方法中
- 每个样式方法有明确的职责边界

**可维护性提升：**
- 样式逻辑的修改不会影响主体布局代码
- 更容易进行样式相关的单元测试
- 减少了方法之间的隐式依赖

**一致性提升：**
- 避免了扩展函数的使用，保持代码风格一致
- 采用标准的参数传递模式，依赖关系更明确
- 无需返回值，简化了方法签名

### 样式分离的最佳实践

**方法命名规范：**
```kotlin
// 好的命名：清楚描述样式应用的目的
private fun applyBackgroundStyling()
private fun applyGradientBackground()
private fun applySolidBackground()
private fun applyTextStyling()

// 避免的命名：模糊或不清楚
private fun setStyle()
private fun doBackground()
private fun handleColor()
```

**参数传递模式：**
```kotlin
// 推荐：明确传递所需的参数
private fun applyGradientBackground(config: ButtonConfig, isPressed: Boolean, attr: ContainerAttr) {
    // config: 样式配置信息
    // isPressed: 状态信息
    // attr: 要应用样式的属性对象
}

// 避免：使用扩展函数或隐式依赖
private fun Attr.applyGradientBackground(config: ButtonConfig, isPressed: Boolean): Attr
```

**职责分离：**
```kotlin
// 每个方法应该有单一的样式职责
private fun applyBackgroundStyling(ctx: ButtonView, attr: ContainerAttr) {
    // 只负责决定使用哪种背景样式
}

private fun applyGradientBackground(config: ButtonConfig, isPressed: Boolean, attr: ContainerAttr) {
    // 只负责应用渐变背景
}

private fun applySolidBackground(config: ButtonConfig, ctx: ButtonView, attr: ContainerAttr) {
    // 只负责应用纯色背景
}
```

### 实际应用案例

在 [`Button.kt`](src/commonMain/kotlin/com/truedian/wg/kuikly/button/Button.kt) 的重构中（Git commit `2657d02f52a75891dde02330a7c347cf67cbb3d7`），我们成功地将样式应用逻辑从扩展函数模式重构为私有方法模式：

**重构要点：**
1. **移除扩展函数**：将 `Attr.applyGradientBackground()` 和 `Attr.applySolidBackground()` 改为普通私有方法
2. **标准化参数传递**：明确传递 `attr` 参数，而不是作为扩展函数的接收者
3. **简化方法签名**：移除不必要的返回值，方法专注于副作用操作
4. **统一样式入口**：通过 [`applyBackgroundStyling()`](src/commonMain/kotlin/com/truedian/wg/kuikly/button/Button.kt:210) 方法统一管理样式应用逻辑

这种重构模式特别适用于：
- 复杂的样式应用逻辑
- 需要根据状态动态切换样式的场景
- 多种样式变体的组件
- 需要进行样式相关单元测试的组件


## 组件统一策略

### 1. 识别通用模式

重构前，分析现有组件以识别：
- 共享的属性和行为
- 通用的布局模式
- 重复的代码块
- 相似的事件处理

### 2. 创建基础组件

将通用功能提取到基础组件中：

```kotlin
/**
 * 支持多种导航栏变体的统一基础组件
 */
internal class BaseNavBarView : ComposeView<BaseNavBarAttr, BaseNavBarEvent>() {
    // 所有导航栏类型的通用功能
    
    private fun calculateSpaceBalance() {
        // 共享的布局计算逻辑
    }
    
    private fun createLeftButton(view: ViewContainer<*, *>) {
        // 统一的左侧按钮创建策略
    }
    
    private fun createRightOperate(view: ViewContainer<*, *>) {
        // 统一的右侧操作区域创建
    }

    override fun body(): ViewBuilder {
        ctx.calculateSpaceBalance()
        return {
            View {
                // ...
                ctx.createLeftButton(this) // remember to add prefix ctx.
                ctx.createRightOperate(this) // remember to add prefix ctx.
            }
        }
    }
}
```

### 3. 保持向后兼容性

重构现有 API 时，确保向后兼容性：

```kotlin
// 保持现有公共 API 正常工作
internal fun ViewContainer<*,*>.NavBarWithBackButton(init: NavBarWithBackButtonView.() -> Unit) {
    addChild(NavBarWithBackButtonView(), init)  // 委托给新实现
}
```

## API 设计最佳实践

### 1. 一致的命名

在相关组件中使用一致的命名模式：

```kotlin
// 所有导航栏变体的一致命名模式
NavBarWithActions
NavBarWithBackButton
NavBarWithCloseButton
NavBarWithSearchButton
```

### 2. 逻辑属性分组

在基类中逻辑性地分组相关属性：

```kotlin
internal open class BaseNavBarAttr : ComposeAttr() {
    // 核心属性
    var navBarType: NavBarType = NavBarType.WITH_ACTIONS
    var barHeight: Float = NavBarConstants.DEFAULT_HEIGHT
    var themeConfig: ThemeConfig = ThemeConfig()
    
    // 布局属性
    var isCenterTheme: Boolean = true
    var isTextCenter: Boolean = true
    
    // 按钮属性
    open var cancelText: String = "取消"
    open var buttonText: String = "按钮"
    open var buttonColor: ButtonColor = ButtonColor.GREEN
}
```

### 3. 事件处理一致性

提供一致的事件处理模式：

```kotlin
internal open class BaseNavBarEvent : ComposeEvent() {
    var backClick: (() -> Unit)? = null
    open var operateClick: (() -> Unit)? = null
    
    // 一致的 DSL 方法
    fun backClick(handler: () -> Unit) {
        this.backClick = handler
    }
    
    open fun operateClick(handler: () -> Unit) {
        this.operateClick = handler
    }
}
```

## 代码组织

### 1. 文件结构

用清晰的部分组织重构后的代码：

```kotlin
// 1. 包和导入
package com.truedian.wg.kuikly.navbar

// 2. 常量和枚举
private object NavBarConstants { /* ... */ }
enum class NavBarType { /* ... */ }

// 3. DSL 工厂函数
internal fun ViewContainer<*,*>.BaseNavBar(init: BaseNavBarView.() -> Unit) { /* ... */ }

// 4. 核心实现类
internal class BaseNavBarView : ComposeView<BaseNavBarAttr, BaseNavBarEvent>() { /* ... */ }

// 5. 专门实现
internal class NavBarWithActionsView: ComposeView<NavBarWithActionsAttr, NavBarWithActionsEvent>() { /* ... */ }

// 6. 属性和事件类
internal open class BaseNavBarAttr : ComposeAttr() { /* ... */ }
internal open class BaseNavBarEvent : ComposeEvent() { /* ... */ }
```

### 2. 逻辑分组

将相关功能组合在一起：

```kotlin
// ==================== 基础属性和事件类 ====================
internal open class BaseNavBarAttr : ComposeAttr() { /* ... */ }
internal open class BaseNavBarEvent : ComposeEvent() { /* ... */ }

// ==================== 具体属性和事件类 ====================
internal class NavBarWithActionsAttr : ComposeAttr() { /* ... */ }
internal class NavBarWithActionsEvent : ComposeEvent() { /* ... */ }
```

### 3. 方法组织

按职责组织方法：

```kotlin
internal class BaseNavBarView : ComposeView<BaseNavBarAttr, BaseNavBarEvent>() {
    // 1. 属性和状态
    private var leftButtonView: ViewRef<DivView>? = null
    private var spaceLeft by observable(0f)
    
    // 2. 生命周期方法
    override fun viewDidLayout() { /* ... */ }
    
    // 3. 布局计算方法
    private fun calculateSpaceBalance() { /* ... */ }
    
    // 4. 组件创建方法
    private fun createLeftButton(view: ViewContainer<*, *>) { /* ... */ }
    private fun createRightOperate(view: ViewContainer<*, *>) { /* ... */ }
    
    // 5. 工具方法
    private fun getIconText(iconType: NavBarIconType): String { /* ... */ }
    
    // 6. 主体方法
    override fun body(): ViewBuilder { /* ... */ }
}
```

## 命名规范

### 1. 组件名称

为组件使用描述性、一致的命名：

```kotlin
// 模式：[组件类型][With][功能][组件后缀]
NavBarWithActionsView
NavBarWithBackButtonView
NavBarWithSearchButtonView
```

### 2. 方法名称

使用清晰、面向动作的方法名称：

```kotlin
// 好的：描述方法的作用
private fun calculateSpaceBalance()
private fun createLeftButton()
private fun createRightOperate()

// 避免：模糊或不清楚的名称
private fun doLayout()
private fun makeButton()
private fun handleStuff()
```

### 3. 属性名称

使用清楚表明其用途的描述性属性名称：

```kotlin
// 好的：清晰和描述性
var navBarType: NavBarType
var barHeight: Float
var isCenterTheme: Boolean
var cancelText: String

// 避免：缩写或不清楚
var type: Int
var h: Float
var center: Boolean
var txt: String
```

## 文档标准

### 1. 类文档

提供全面的类文档：

```kotlin
/**
 * 统一的导航栏基础组件
 * 使用组合模式支持不同类型的导航栏变体
 * 
 * 支持的导航栏类型：
 * - WITH_ACTIONS: 带操作按钮的导航栏
 * - WITH_BACK_BUTTON: 带返回按钮的导航栏
 * - WITH_CLOSE_BUTTON: 带关闭按钮的导航栏
 * - WITH_SEARCH_BUTTON: 带搜索按钮的导航栏
 * - WITH_CUSTOM_BUTTON: 带自定义按钮的导航栏
 */
internal class BaseNavBarView : ComposeView<BaseNavBarAttr, BaseNavBarEvent>() {
```

### 2. 方法文档

为复杂方法提供清晰的解释：

```kotlin
/**
 * 计算左右空间平衡
 * 确保导航栏标题居中显示
 * 
 * 算法说明：
 * 1. 获取左侧按钮和右侧操作区域的宽度
 * 2. 计算宽度差异并添加适当的空间调整
 * 3. 确保标题区域在视觉上居中
 */
private fun calculateSpaceBalance() {
    // 实现...
}
```

### 3. 属性文档

为所有公共属性提供文档：

```kotlin
internal open class BaseNavBarAttr : ComposeAttr() {
    /** 导航栏类型，决定显示哪种导航栏变体 */
    var navBarType: NavBarType = NavBarType.WITH_ACTIONS

    /** 导航栏高度，默认44f */
    var barHeight: Float = NavBarConstants.DEFAULT_HEIGHT

    /** 主题配置，包含标题文本、图标等设置 */
    var themeConfig: ThemeConfig = ThemeConfig()
}
```

## 重构检查清单

重构 KuiklyUI 组件时，使用此检查清单：
(you don't have to follow this strictly. Just get the idea.)

### 重构前
- [ ] 识别代码重复和通用模式
- [ ] 分析现有 API 的一致性问题
- [ ] 记录当前组件行为和需求
- [ ] 规划向后兼容性策略

### 重构期间
- [ ] 将常量提取到共享对象
- [ ] 为通用功能创建基类
- [ ] 在适当的地方使用组合优于继承
- [ ] 实施一致的命名约定
- [ ] 使用私有方法分离 UI 部分
- [ ] 添加全面的文档

### 重构后
- [ ] 验证所有现有功能仍然正常工作
- [ ] 更新相关组件以使用新模式
- [ ] 为新基础组件添加单元测试
- [ ] 更新文档和示例
- [ ] 与团队审查代码的一致性

## 性能考虑

### 1. 延迟初始化

对昂贵的操作使用延迟初始化：

```kotlin
private val expensiveCalculation by lazy {
    // 只有在需要时才运行的复杂计算
    calculateComplexLayout()
}
```

### 2. 可观察优化

在重构组件中谨慎使用可观察：

```kotlin
// 好的：只观察变化的内容
private var spaceLeft by observable(0f)
private var spaceRight by observable(0f)

// 避免：不必要地观察整个复杂对象
private var entireConfig by observable(ComplexConfig()) // 可能导致不必要的重组
```

### 3. 组件复用

设计重构组件以便复用：

```kotlin
// 可复用的基础组件
internal class BaseNavBarView : ComposeView<BaseNavBarAttr, BaseNavBarEvent>() {
    // 可以在变体间复用的高效实现
}
```

## 结论

在 KuiklyUI 中进行有效的重构需要仔细规划、一致的模式，以及对代码质量和性能的关注。导航栏重构示例展示了如何成功合并相似组件，同时保持向后兼容性并改善可维护性。

关键要点：
1. **重构前规划** - 分析现有代码并识别模式
2. **使用组合** - 优先使用组合而非继承以获得灵活性
3. **保持一致性** - 应用一致的命名和 API 模式
4. **UI 分离** - 使用私有方法将复杂的 UI 创建逻辑分解为可管理的部分
5. **彻底记录** - 为重构组件提供清晰的文档
6. **广泛测试** - 确保重构代码保持现有功能

通过遵循这些最佳实践，您可以创建更可维护、高效和一致的 KuiklyUI 组件，这些组件更容易理解、扩展和调试。