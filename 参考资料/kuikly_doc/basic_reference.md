# KuiklyUI Framework Reference Documentation
**本文档的中文版链接：https://slowisfast.feishu.cn/wiki/WAkuwVNUaiFoDnkZgpLc3LeUnkg**

## Overview

KuiklyUI is a cross-platform development framework built on Kotlin Multiplatform (KMP) that enables developers to create native-performance applications for Android, iOS, HarmonyOS, H5/Web, and WeChat Mini Programs using a single Kotlin codebase.

### Architecture

**KuiklyCore**: Cross-platform declarative + reactive implementation with unified UI components
- Compiles to platform-specific outputs (.aar for Android, .framework for iOS, .so for HarmonyOS)

**KuiklyRender**: Platform-specific rendering implementation
- Handles actual UI rendering using native platform components

## Reading guide: when to consult extended_reference.md

`basic_reference.md` (this file) is the get-things-done reference — enough surface to read and write KuiklyUI code competently. [`extended_reference.md`](./extended_reference.md) is the deep companion: same topics, but with the *why*, the full APIs, and the corners that bite.

Reach for `extended_reference.md` when:

- **You hit unexpected behavior** — "my UI doesn't update", "my animation jumps", "my `addNotify` callback fires after the page closed", "my absolute child changes parent size". Its §26 "Common pitfalls and idioms" is a numbered list of these.
- **You want to understand a concept**, not just call it — what `observable` actually does and what `PageScope` it binds to, how the Kuikly thread relates to coroutines, what `animate()`'s scope rule means, why `vif` loses state but `visibility(false)` doesn't.
- **You need the full API surface** of a built-in component (List, Scroller, Input, RichText, Canvas, PAG, Slider, ScrollPicker, Mask, Video, …) — its §24 consolidates every attribute, event, and method for 31 components.
- **You're extending the framework** — custom Module (sync/async `toNative`, per-platform registration), custom View (`DeclarativeBaseView`), per-prop extension via `viewPropExternalHandler`, multi-module KSP setup, Protobuf bridge with Wire.
- **You're crossing the bridge** — raw `NetworkModule` instead of the elegant wrapper, multi-page state via `NotifyModule`, `MemoryCacheModule` + `Canvas.drawImage` integration, threading off the Kuikly thread (`Dispatchers.Kuikly[ctx]`, `KuiklyContextScheduler`).
- **You need the FlexBox defaults written down** — `alignItems = STRETCH` by default, `overflow = false` (iOS-like, not Android-like), `flexDirection = COLUMN` (unlike CSS), what `flex(1f)` actually fills.
- **You're picking between two APIs** — `vfor`/`vforIndex`/`vforLazy` vs `renderList`/`renderLazyList`, declarative `animate` vs imperative `animateToAttr`, three tiers of async (Module callbacks vs Kuikly built-in coroutines vs `kotlinx.coroutines` + Kuikly dispatcher).

If you're skim-reading this doc for the first time, you don't need to jump to the extended one — finish here, build something, then go back for whatever surprises you.

## Pages (Pager)

### Page Declaration

Every KuiklyUI page is a class that extends `Pager` and must be annotated with `@Page`:

```kotlin
import com.tencent.kuikly.core.pager.Pager

@Page("HelloWorld")
class HelloWorldPage : Pager() { // or BasePager //MARK
    override fun body(): ViewBuilder {
        return {
            attr { allCenter() }
            Text {
                attr {
                    text("Hello Kuikly")
                    fontSize(14f)
                }
            }
        }
    }
}
```

### Page Lifecycle

1. **created**: Called before `body()`, used for initialization and data fetching
2. **pageDidAppear**: Page becomes visible on screen
3. **pageDidDisappear**: Page becomes invisible
4. **pageWillDestroy**: Page about to be destroyed, cleanup operations

```kotlin
override fun created() {
    super.created()
    // Initialize data, fetch from API
}

override fun pageDidAppear() {
    super.pageDidAppear()
    // Page visible operations
}
```

### Page Data (PagerData)

Access page parameters passed from native side:

```kotlin
override fun created() {
    super.created()
    val pageWidth = pagerData.pageViewWidth
    val pageHeight = pagerData.pageViewHeight
    val customParam = pagerData.params.optInt("customKey")
}
```

**Basic Parameters:**
- `pageViewWidth/pageViewHeight`: Page root view dimensions
- `statusBarHeight`: Status bar height (top)
- `deviceWidth/deviceHeight`: Screen dimensions
- `params`: JSONObject containing business parameters //MARK
- `safeAreaInsets`: Safe area insets

## DSL Structure & Components

### Basic DSL Pattern

```kotlin
override fun body(): ViewBuilder {
    return {
        // Component declaration
        ComponentA {
            attr {
                // Style and layout attributes
            }
            event {
                // Event handlers
            }
            // Child components
          	ComponentB {
              	// attr, event...
            }
        }
    }
}
```

### Core Components

#### View (Container)
Basic container component, equivalent to FrameLayout (Android) / UIView (iOS):

```
import com.tencent.kuikly.core.views.View
```

```kotlin
View {
    attr {
        size(100f, 100f)
        backgroundColor(Color(0xFF03C160)) // hex color
        borderRadius(10f)
    }
    // Child components
}
```

#### Text
Text display component:

```
import com.tencent.kuikly.core.views.Text // appends a TextView child
import com.tencent.kuikly.core.base.Color
```

```kotlin
Text {
    attr {
        text("Hello World")
        fontSize(16f)
        color(Color.BLACK)
        fontWeightBold()
        textAlignCenter()
        lines(2) // Max lines with ellipsis
    }
}
```

#### Image
Image display component:

```
import com.tencent.kuikly.core.views.Image
```

```kotlin
Image {
    attr {
        src("https://example.com/image.jpg")
        size(50f, 50f)
        borderRadius(25f)
    }
}
```

#### WGButton (WG Basic Component)

```
import com.truedian.wg.core.components.foundation.wgButton.WGButton
import com.truedian.wg.core.components.foundation.wgButton.WGButtonType
import com.truedian.wg.core.components.foundation.wgButton.WGButtonScale
```

```kotlin
WGButton {
    attr {
            text = "按钮"
            type = WGButtonType.PRIMARY
            scale = WGButtonScale.SCALE_48
    }
    onClick {
        BaseVisuals.showSimpleSuccessToast(pagerId, "操作成功") // 调用弹窗式基础组件
    }
}
```



### Other Components

#### Built-in Components

| Component | Key Parameters | Description |
|-----------|----------------|-------------|
| **DatePicker** | Year/month/day selection (based on Scroller) | Date picker component |
| **FooterRefresh** | `preloadDistance`, `minContentSize` | Footer refresh functionality for ListView |
| **Hover** | `bringIndex`, `hoverMarginTop` | Auto-hover component for lists (floats to top when scrolling) |
| **Blur** | `blurRadius` (max 12.5f) | Gaussian blur component for frosted glass effects |
| **Input** | `text`, `fontSize`, `placeholder`, `placeholderColor`, `tintColor`, `maxTextLength`, `autofocus` | Single-line input box with text styling and keyboard control |
| **List** | `scrollEnable`, `bouncesEnable`, `flexDirection`, `pagingEnable`, `preloadViewDistance` | List component for displaying series of items, supports vertical/horizontal |
| **PAG** | `src`, `repeatCount`, `autoPlay`, `replaceLayerContents` | Lottie-like animation player with layer content replacement |
| **PageList** | `pageItemWidth`, `pageItemHeight`, `pageDirection`, `defaultPageIndex`, `keepItemAlive` | Paged list where each item matches PageList dimensions |
| **Refresh** | `refreshEnable` | Pull-to-refresh component for ListView |
| **RichText** | `Span`, `ImageSpan`, `PlaceholderSpan` | Rich text with different styles, inherits Text properties |
| **ScrollPicker** | `itemList`, `defaultIndex`, `itemWidth`, `itemHeight`, `countPerScreen` | Scroll picker based on Scroller, combinable for custom scenarios like clock time or provinces/cities |
| **Scroller** | `scrollEnable`, `bouncesEnable`, `flexDirection`, `pagingEnable`, `nestedScroll` | Scroll container for uncertain height content in fixed container |
| **SliderPage** | `defaultPageIndex`, `isHorizontal`, `pageItemWidth`, `pageItemHeight`, `loopPlayIntervalTimeMs` | Carousel with auto-play and manual switching |
| **Slider** | `currentProgress`, `progressColor`, `trackColor`, `thumbColor`, `trackThickness`, `sliderDirection` | Drag progress bar with customizable appearance |
| **Tabs** | `scrollParams`, `defaultInitIndex`, `indicatorInTabItem`, alignment methods | Tab switching component (used with PageList) |
| **TextArea** | All Input properties + multi-line support | Multi-line input box component |
| **Video** | `src`, `playControl`, `resizeMode`, `muted`, `rate` | Video player with playback control and resize modes |
| **WaterFallList** | `listWidth`, `columnCount`, `itemSpacing`, `lineSpacing`, `contentPadding` | Waterfall layout with automatic positioning, inherits from List |
| **Canvas** | Drawing methods: `beginPath()`, `moveTo()`, `lineTo()`, `arc()`, `stroke()`, `fill()` | Custom drawing canvas aligned with H5 Canvas capabilities |

For the detailed componet usage of these components, search in @kuikly_doc/API/ ; 

#### WG Basic Components (A Component Library Provided by Our Company)

The full WG basic component library lives under `kuikly_doc/basic_components/`. See [`basic_components/index.md`](./basic_components/index.md) for the categorized index of all 43 components with one-line descriptions and demo page names — go there first when picking a component.

Quick map by category (full attribute lists and examples are in each component's own doc):

| Category | Components |
|----------|-----------|
| **Foundation** | WGButton, WGImage, WGSwitch, WGColor, WGFont, Icon, Tag, Badge, Link, Loading, Spacer |
| **Input** | InputSimple, InputText, InputNumber, Counter, CheckBox, Search, Form |
| **Navigation** | NavBar, NavBarActionButton, ActionBar, TabBar, SegmentControl, Breadcrumb, SideBar |
| **Feedback** | Dialog, DialogContainer, ModalFrame, ModalFrameX, ActionSheet, ActionArea, PopOver, PopViewSelect, Toast, SnackBar, Push, Result, Stepper |
| **Layout** | Cell, Footer, RenderList |

Most feedback components (Toast, Dialog, ActionSheet, ModalFrame/X, PopOver, PopViewSelect, …) are launched imperatively via `BaseVisuals` helpers — `showSimpleSuccessToast`, `showTextDialog`, `showActionSheet`, `showModalFrame`, `createPopover`, etc. Each component's doc lists the exact entry point; `BaseVisuals.kt` has the full set.

## Attributes System

### Layout Attributes (FlexBox)

KuiklyUI uses FlexBox layout system for cross-platform consistency:

**Size & Position:**
```kotlin
attr {
    width(100f)
    height(50f)
    size(100f, 50f) // Shorthand
}
```

*Note*: **If you don't specify it, it will automatically wrap content in the flex direction.**

**Margin & Padding:**

```kotlin
attr {
    margin(10f) // All sides
    margin(top = 10f, bottom = 5f)
    padding(15f)
    padding(left = 20f, right = 20f) // IMPORTANT! NO vertical / horizontal, you need to specify each side.
}
```

**FlexBox Properties:**

```
import com.tencent.kuikly.core.layout.FlexDirection
import com.tencent.kuikly.core.layout.FlexJustifyContent
```

```kotlin
attr {
    flexDirection(FlexDirection.ROW) // ROW, COLUMN, ROW_REVERSE, COLUMN_REVERSE
    justifyContent(FlexJustifyContent.CENTER) // FLEX_START, CENTER, FLEX_END, SPACE_BETWEEN, SPACE_AROUND, SPACE_EVENLY
    alignItems(FlexAlign.CENTER) // FLEX_START, CENTER, FLEX_END, STRETCH
    alignSelf(FlexAlign.FLEX_END) // Override parent alignItems
    flex(1f) // Flex grow factor
    flexWrap(FlexWrap.WRAP) // NOWRAP, WRAP
}
```

**Positioning:**
```kotlin
attr {
    positionAbsolute() // or positionRelative()
    top(10f)
    left(20f)
    bottom(30f)
    right(40f)
    absolutePosition(top = 10f, left = 20f, bottom = 30f, right = 40f) // same as above
}
```

**Helper Methods:**
```kotlin
attr {
    allCenter() // Center both axes
    justifyContentCenter() // Center main axis
    alignItemsCenter() // Center cross axis
    flexDirectionRow() // Horizontal layout
    flexDirectionColumn() // Vertical layout
}
```

### Style Attributes

**Background:**

```
import com.tencent.kuikly.core.base.Direction
import com.tencent.kuikly.core.base.Color
import com.tencent.kuikly.core.base.ColorStop
```

```kotlin
attr {
    backgroundColor(Color.RED)
    backgroundLinearGradient(
        Direction.TO_BOTTOM,
        ColorStop(Color.RED, 0f),
        ColorStop(Color.BLUE, 1f)
    )
}
```

**Border & Radius:**
```
import com.tencent.kuikly.core.base.Border //MARK
import com.tencent.kuikly.core.base.BorderStyle
import com.tencent.kuikly.core.base.BorderRectRadius

```

```kotlin
attr {
    border(Border(2f, BorderStyle.SOLID, Color(0xFF03C160))) // Color Hex
    borderRadius(10f) // All corners
    borderRadius(BorderRectRadius(10f, 5f, 0f, 15f)) // Individual corners
}
```

**Shadow:**
```kotlin
attr {
    boxShadow(BoxShadow(offsetX = 2f, offsetY = 2f, shadowRadius = 4f, shadowColor = Color.GRAY))
}
```

**Transform:**
```kotlin
attr {
    transform(
        rotate = Rotate(45f), // of course, it needs import from core.base
        scale = Scale(1.5f, 1.5f),
        translate = Translate(0.5f, 0.5f), // Percentage of own size
        anchor = Anchor(0.5f, 0.5f) // Transform origin
    )
}
```

**Visibility & Interaction:**
```kotlin
attr {
    visibility(true) // true/false
    opacity(0.8f) // 0.0 to 1.0
    touchEnable(true)
    zIndex(1) // Layer order
    overflow(clipChildren = true) // Clip children
}
```

## State Management & Reactivity

### Observable Fields

Use `observable` delegate for reactive single values:

```kotlin
import com.tencent.kuikly.core.reactive.handler.observable
import com.tencent.kuikly.core.reactive.handler.observableList
```

```kotlin
class MyPage : Pager() {
    private var counter by observable(0)
    private var isVisible by observable(true)
    private var userName by observable("")

    override fun body(): ViewBuilder {
        val ctx = this // required to access the properties
        return {
            Text {
                attr {
                    text("Count: ${ctx.counter}")
                }
            }

            Button {
                attr {
                    titleAttr { text("Increment") }
                }
                event {
                    click { ctx.counter++ } // Auto-updates UI
                }
            }
        }
    }
}
```

### Observable Collections

Use `observableList` and `observableSet` for reactive collections:

```kotlin
private var items by observableList<String>()

override fun created() {
    super.created()
    for (i in 0 until 10) {
        items.add("Item $i")
    }
}

override fun body(): ViewBuilder {
    val ctx = this
    return {
        List {
            attr { flex(1f) }

            renderList({ ctx.items }) { item, _, _ ->
                Text {
                    attr {
                        text(item)
                        margin(10f)
                    }
                }
            }
        }
    }
}
```

## Control Flow Directives

### Loop Directives

**renderList** - loop with reactive updates:

```
import com.truedian.wg.core.components.organism.list.renderList
import com.truedian.wg.core.components.organism.list.renderLazyList
```

```kotlin
renderList({ ctx.list }) { item, index, count ->
    Text {
        attr { text(item) }
    }
}

// Lazy render, create views only when needed
renderList({ ctx.list }, isLazy = true, maxLoadItem = 20 /* default 30 */) { item, index, count ->
    Text {
        attr { text(item) }
    }
}

// or simply:
renderLazyList({ ctx.list }) {
    Text {
        attr { text(it) }
    }
}
```

**render** - extension function of List (non-reactive, single-pass):

```
import com.truedian.wg.core.components.organism.list.map
```

```kotlin
list.render { item, index, count ->
    Text {
        attr { text(it) }
    }
}.invoke(this)
```

*Note*: 
- The default API (vfor, vforIndex, vforLazy) is not recommended to use.


### Conditional Directives

```
import com.truedian.wg.core.directives.vif // and velseif, velse
import com.truedian.wg.core.directives.vbind
```

**vif/velseif/velse** - Conditional rendering:

```kotlin
vif({ ctx.showFirst }) {
    Text { attr { text("First option") } }
}
velseif({ ctx.showSecond }) {
    Text { attr { text("Second option") } }
}
velse {
    Text { attr { text("Default option") } }
}
```

**vbind** - Switch-like conditional rendering:

```kotlin
vbind({ ctx.currentState }) {
    it as Int
    when (it) {
        1 -> Text { attr { text("State One") } }
        2 -> View { attr { backgroundColor(Color.GREEN) } }
        else -> Text { attr { text("Unknown state") } }
    }
}
```

**renderList** - iterate through an `observableList`:

```kotlin
//... inside a ComposeView class

private val items by observableList<LiveItem>()

override fun created() {
    super.created()
    items.addAll(attr.liveItems) // get items from `attr`
}
override fun body(): ViewBuilder {
  	val ctx = this
	  return {
        List {
            renderList({ ctx.items }) { item: LiveItem, _, _ ->
                LiveItemCardComponent {
                    attr {
                        this.item = item
                    }
                }
            }
        }
    }
}
```

## Event System

### Basic Events

All components support *basic events* (click, doubleClick, longPress, pan, layoutFrameDidChange, willAppear):

```kotlin
class PopupView(function: () -> Unit) : ComposeView<PopupAttr, PopupEvent>() {

// ...
private var dragOffsetX by observable(0f) // persist across drags
private var dragOffsetY by observable(0f)
private var dragAnchorX by observable(0f) // re-initialize before each drag
private var dragAnchorY by observable(0f)

// ... 
  
attt {
    transform(translate = Translate( // see handle drag logic below
        percentageX = 0f, // required
        offsetX = ctx.dragOffsetX,
        offsetY = ctx.dragOffsetY
    ))
}
event {
    click { clickParams ->
        val x = clickParams.x // Relative to component
        val y = clickParams.y
        // Handle click
    }

    doubleClick { clickParams ->
        // Handle double click
    }

    longPress { longPressParams ->
        val state = longPressParams.state // "start", "move", "end"
        // Handle long press
        // usually, only handle "start"
    }

    pan { panGestureParams ->
        val x = panGestureParams.x
        val y = panGestureParams.y
        val state = panGestureParams.state
        val pageX = panGestureParams.pageX // Relative to page
        val pageY = panGestureParams.pageY
         
        // Handle drag logic
        when (panParams.state) {
        		"start" -> {
              	ctx.dragAnchorX = panGestureParams.pageX
              	ctx.dragAnchorY = panGestureParams.pageY
            }
          	"move" -> {
                val deltaX = panGestureParams.pageX - ctx.dragAnchorX
                val deltaY = panGestureParams.pageY - ctx.dragAnchorY
                ctx.dragOffsetX += deltaX
                ctx.dragAnchorX += deltaX

                ctx.dragOffsetY += deltaY
                ctx.dragAnchorY += deltaY
            }
          	"end" -> {
              // Drag ended - could animate back to a position
              // e.g.
              // ctx.dragOffsetX = 0f
              // ctx.dragOffsetY = 0f
              // ctx.isAnimating = true
              // setTimeout(0.2f){ctx.isAnimating = false}
            }
        }
    }
}

```

### Lifecycle Events

```kotlin
event {
    willAppear {
        // Component about to become visible
    }

    didAppear {
        // Component fully visible
    }

    willDisappear {
        // Component about to become invisible
    }

    didDisappear {
        // Component fully invisible
    }

    appearPercentage { percentage01 ->
        // percentage01 is 0.0 to 1.0
        // Useful for scroll-based animations
    }

    layoutFrameDidChange { frame ->
        val x = frame.x
        val y = frame.y
        val width = frame.width
        val height = frame.height
        // Layout changed
    }

    animationCompletion { params ->
        val finished = params.finish == 1
        val animatedProperty = params.attr
        // Animation completed
    }
}
```

### Touch Events (View component)

```kotlin
event {
    touchDown { touchParams ->
        val touches = touchParams.touches // Multi-touch support
        val pointerId = touchParams.pointerId
        // Touch started
    }

    touchMove { touchParams ->
        // Touch moved
    }

    touchUp { touchParams ->
        val action = touchParams.action // "up" or "cancel"
        // Touch ended
    }
}
```

## Animation

```kotlin
import com.tencent.kuikly.core.base.Animation
```

### Animation Types

```kotlin
// Predefined animation curves
Animation.linear
Animation.easeIn
Animation.easeOut
Animation.easeInOut
Animation.springLinear
Animation.springEaseIn
Animation.springEaseOut
Animation.springEaseInOut
```

### Animatable Properties

- **transform**: Translation, rotation, scaling
- **opacity**: Transparency
- **backgroundColor**: Background color
- **frame**: Position and size

### Animation Usage

```kotlin
//... in a ComposeView class
val isPressed by observable(false)

// ... in body()
attr {
    animate(Animation.easeInOut(0.3f), isPressed) // Triggers when animationFlag is true (time unit: second)
    backgroundColor(ctx.isPressed ? Color.BLUE : Color.GRAY)
    transform(scale = Scale(ctx.isPressed ? 0.95f : 1f, ctx.isPressed ? 0.95f : 1f))
}
```

or:

```kotlin
attr {
  if (ctx.isAnimated) {
    transform(scale = Scale(0.95f, 0.95f))
	} else {
  	  transform(scale = Scale(1f, 1f))
	}
	animate(Animation.easeOut(1f), ctx.isAnimated)
}
```

There's more caveats in Kuikly's animation system. Refer to animation-basic.md, animation-declarative.md, and animation-imperative.md in the kuikly_doc/DevGuide/ for advanced usages. 

## Development Patterns

### Component Composition

Create reusable components using ComposeView:

```
import com.tencent.kuikly.core.base.ComposeAttr
import com.tencent.kuikly.core.base.ComposeEvent
import com.tencent.kuikly.core.base.ComposeView
import com.tencent.kuikly.core.base.ViewContainer
```

```kotlin
class CustomCardView : ComposeView<ComposeAttr, ComposeEvent>() { // ComposeView = reusable components
    override fun body(): ViewBuilder {
        return {
            View {
                attr {
                    backgroundColor(Color.WHITE)
                    borderRadius(8f)
                    boxShadow(BoxShadow(0f, 2f, 4f, Color.GRAY))
                    padding(16f)
                }
                // Card content
            }
        }
    }
}

// declare it so that it can be referenced
fun ViewContainer<*, *>.CustomCard(init: CustomCardView.() -> Unit) {
    addChild(CustomCardView(), init)
}
```

### State Management and ViewModels

For complex state, organize observables logically:

```
import com.truedian.wg.core.base.extension.async
```

```kotlin
class UserProfile : ComposeView<ComposeAttr, ComposeEvent>() {
    // UI State
    private var isLoading by observable(false)
    private var showError by observable(false)

    // Data State
    private var user by observable<User?>(null)
    private var friends by observableList<User>()

    // Computed properties using reactive fields
    private val displayName: String
        get() = user?.name ?: "Unknown User"

    private fun loadUserData() {
        isLoading = true
        showError = false

        async { // launches a coroutine
            try {
                val userData = api.getUser()
                user = userData
                friends.clear()
                friends.addAll(userData.friends)
            } catch (e: Exception) {
                showError = true
            } finally {
                isLoading = false
            }
        }
    }
}
```

Use ViewModels:

```
import com.tencent.kuikly.core.base.PagerScope  // every observable must be in a pagerScope; every ViewContainer implements PagerScope
```

```kotlin
class CounterViewModel(pagerScope: PagerScope) {
    var count by pagerScope.observable(0)
    var isLoading by pagerScope.observable(false)

    fun increment() {
        count++
    }

    fun reset() {
        count = 0
    }
}

// Use across pages
class Counter : ComposeView<ComposeAttr, ComposeEvent>() {
    private val counterLogic = CounterViewModel(this)

    override fun body(): ViewBuilder {
        val ctx = this
        return {
            Text { attr { text("${ctx.counterLogic.count}") } }
        }
    }
}
```


### Error Handling

```kotlin
override fun body(): ViewBuilder {
    val ctx = this
    return {
        vif({ ctx.isLoading }) {
            Text { attr { text("Loading...") } }
        }
        velseif({ ctx.showError }) {
            Text {
                attr {
                    text("Error occurred")
                    color(Color.RED)
                }
            }
        }
        velse {
            // Main content
        }
    }
}
```

## Advanced ComposeView Usage

### Custom ComposeView with Attributes and Events

Create reusable UI components with custom attributes and events:

```kotlin
// Custom Attribute Class
class NavBarAttr : ComposeAttr() {
    var title by observable("") // reactive props
    var showBackButton = true   // non-reactive props
}

// Custom Event Class
class NavBarEvent : ComposeEvent() {
    var backClickHandler: (() -> Unit)? = null

    fun onBackClick(handler: () -> Unit) {
        backClickHandler = handler
    }
}

// ComposeView Implementation
class NavigationBarView : ComposeView<NavBarAttr, NavBarEvent>() {
    override fun createAttr(): NavBarAttr = NavBarAttr()
    override fun createEvent(): NavBarEvent = NavBarEvent()

    // ================== Properties ==================

    var viewRef: ViewRef<DivView>? = null      // import com.tencent.kuikly.core.base.ViewRef

    // ================== Lifecycle Methods ==================

    override fun created() {
        // called before body(), but after attr and event creation
        bindValueChange({ attr.title }) {
            // react to title changes
            wg.logD("NavigationBarView", "title: ${attr.title}")
        }
    }

    override fun viewDidLayout() {
        wg.logD("NavigationBarView", "component height: ${viewRef?.view?.frame?.height}")
    }

    // ================== Exposed Methods ==================
    override fun resetText() { // can be called with a NavigationBarView's ViewRef.view
        attr.title = "默认标题"
    }

    // ======== Utility Methods (very useful for code refactors) ========
    private fun createBackButton(view: ViewContainer<*,*>) {
        view.vif({ ctx.attr.showBackButton }) {
            Image {
                attr {
                    size(16f, 16f)
                    src("data:image/png;base64,...")
                    absolutePosition(left = 15f, top = 14f)
                }
                event {
                    click {
                        ctx.event.backClickHandler?.invoke()
                    }
                }
            }
        }
    }

    private fun createTitle(view: ViewContainer<*,*>) {
        view.Text {
            attr {
                text(ctx.attr.title)
                fontWeightBold()
                fontSize(16f)
            }
        }
    }

// ================== Main Body Method ==================
    override fun body(): ViewBuilder {
        val ctx = this
        return {
            View {
                ref {
                    viewRef = it // a View is actually a DivView
                }
                attr {
                    size(pagerData.pageViewWidth, 44f)
                    marginTop(pagerData.statusBarHeight)
                    allCenter()
                    backgroundColor(Color.GRAY)
                }

                // Back button (conditional)
                ctx.createBackButton(this)

                // Title
                ctx.createTitle(this)
            }
        }
    }
}

// Extension function for DSL usage
fun ViewContainer<*, *>.NavigationBar(init: NavigationBarView.() -> Unit) {
    addChild(NavigationBarView(), init)
}
```

### Using Custom ComposeView

```kotlin
var navBarRef: ViewRef<DivView>? = null

override fun viewDidLayout() {
    navBarRef?.view?.let {
        // Access the view directly
        it.resetText()
    }
}

override fun body(): ViewBuilder {
    return {
        NavBar {
            ref {
                navBarRef = it
            }
            attr {
                title = "My Page Title"
                showBackButton = true
            }
            event {
                onBackClick {
                    // Handle back navigation
                }
            }
        }

        // Other page content...
    }
}
```

## Assets and Resources

1. **Directory Structure**:
```
shared/src/commonMain/
├── assets/
│   ├── common/          # commonAssets
│   │   └── logo.png
│   ├── page1/           # Page-specific assets for @Page("page1")
│   │   └── background.jpg
│   └── page2/
│       └── icon.png
└── kotlin/
```

2. **Using Assets in Components**:

```kotlin
// Common assets (available to all pages)
WGImage {
    attr {
        commonAssetPath = "logo.png"
        imageWidth = 100f
        imageHeight = 50f
    }
}

// Page-specific assets
WGImage {
    attr {
        pageAssetPath = "background.jpg"
        imageWidth = pagerData.pageViewWidth
        imageHeight = 200f
    }
}

// Dynamic image loading based on state
vbind({ctx.isActive}) {
    WGImage {
        attr {
            if (ctx.isActive) {
                pageAssetPath = "active_icon.png"
            } else {
                commonAssetPath = "inactive_icon.png"
            }
            imageWidth = 24f
            imageHeight = 24f
        }
    }
}
```

## Network Requests & JSON Handling

### Elegant Network Request System

Use the **elegantNetWorkRequest** system for all HTTP operations. It provides a fluent, chainable API and automatic JSON deserialization via `kotlinx.serialization`.

```
import com.truedian.wg.core.base.network.elegantNetWorkRequest.postFormRequest
import com.truedian.wg.core.base.network.elegantNetWorkRequest.postRequest
import com.truedian.wg.core.base.network.elegantNetWorkRequest.getRequest
import com.truedian.wg.core.base.extension.jsonOf
import com.truedian.wg.core.base.network.elegantNetWorkRequest.internal.with
import com.truedian.wg.core.base.network.elegantNetWorkRequest.utils.BaseResponseData
import com.truedian.wg.core.base.utils.BaseJsonModel
import com.tencent.kuikly.core.nvi.serialization.json.JSONObject
import com.tencent.kuikly.core.nvi.serialization.json.JSONArray
import kotlinx.serialization.Serializable
import com.truedian.wg.core.base.extension.async
```

### Response Data Model

All response types must implement `BaseResponseData` and extend `BaseJsonModel`, and be annotated with `@Serializable`:

```kotlin
// BaseResponseData interface fields: errcode, errmsg, status, success
// Use BaseResponseBean as a convenient open base class, or implement manually:

@Serializable
data class MyResponse(
    override val errcode: Int = 0,
    override val errmsg: String = "",
    override val status: Int = 0,
    override val success: Boolean = false,
    val result: MyResultBean = MyResultBean()
) : BaseResponseData, BaseJsonModel()

@Serializable
data class MyResultBean(
    val items: List<MyItem> = emptyList(),
    val total: Int = 0
) : BaseJsonModel()

@Serializable
data class MyItem(
    val id: String = "",
    val name: String = ""
) : BaseJsonModel()
```

### Making Requests (inside a coroutine / `async` block)

Requests are **suspend functions** and must be called inside a coroutine. Use `pagerScope.async { }` (or `async { }` inside a `ComposeView`/`Pager`) to launch one:

```kotlin
// POST Form request (most common — used for business APIs)
private suspend fun fetchData(albumId: String) =
    postFormRequest(ApiPaths.SOME_API)
        .bodyParams(jsonOf("albumId" with albumId, "page" with 1))
        .needLog(false) // optional: suppress debug logs
        .send<MyResponse>()

// GET request
private suspend fun fetchConfig() =
    getRequest("https://api.example.com/config")
        .urlParams("version" to "1.0", "platform" to "android")
        .send<MyResponse>()

// POST JSON body request
private suspend fun submitData(payload: JSONObject) =
    postRequest("https://api.example.com/submit")
        .bodyParams(payload)
        .send<MyResponse>()
```

### Full ViewModel Example

```kotlin
class MyViewModel(val pagerScope: PagerScope) {
    var items by pagerScope.observableList<MyItem>()
    var isLoading by pagerScope.observable(false)

    fun loadData(albumId: String) {
        pagerScope.async {
            isLoading = true

            // Build request body
            val body = jsonOf("albumId" with albumId)
            body.put("page", 1)

            val response = postFormRequest(ApiPaths.SOME_API)
                .bodyParams(body)
                .needLog(false)
                .send<MyResponse>()

            isLoading = false

            if (response.success && response.data?.success == true) {
                response.data?.result?.let { result ->
                    items.clear()
                    items.addAll(result.items)
                }
            } else {
                // Handle error: response.error contains error info
                wg.logE("MyViewModel", "Request failed: ${response.error}")
            }
        }
    }
}
```

### Building Request Bodies

Use `jsonOf` + `with` for concise JSONObject construction, then `put` for conditional fields:

```kotlin
import com.truedian.wg.core.base.extension.jsonOf
import com.truedian.wg.core.base.network.elegantNetWorkRequest.internal.with

val body = jsonOf("albumId" with albumId)  // creates JSONObject with initial key-value

// Conditionally add more fields
if (searchText.isNotEmpty()) {
    body.put("searchValue", searchText)
}
if (timestamp != 0L) {
    body.put("timestamp", timestamp)
} else {
    body.put("timestamp", "-1")
}

// Adding a JSONArray (e.g. for tag lists)
val tags = JSONArray()
tagIdList.forEach { tags.put(it) }
body.put("tagList", tags)
```

### JSON Serialization / Deserialization with BaseJsonModel

`BaseJsonModel` wraps `kotlinx.serialization` with lenient settings (ignores unknown keys, coerces input values):

```kotlin
// Deserialize from JSON string (e.g. from cache)
val bean = BaseJsonModel.fromJsonString<MyResultBean>(jsonString)

// Serialize to JSON string (e.g. for caching)
val jsonString = BaseJsonModel.toJsonString(myResultBean)

// Safe deserialization (returns null on failure instead of throwing, but increases performance overhead)
val bean = BaseJsonModel.fromJsonStringSafe<MyResultBean>(jsonString)
```

### Checking Response Success

The `Response<T>` wrapper returned by `.send<T>()` has:
- `response.success`: `true` if the HTTP request itself succeeded and JSON parsed without error
- `response.data`: the deserialized `T` object (nullable)
- `response.data?.success`: the business-level success flag from `BaseResponseData`
- `response.error`: an `Error` object with message/code on failure

```kotlin
val response = postFormRequest(url).bodyParams(body).send<MyResponse>()

if (response.success && response.data?.success == true) {
    val result = response.data?.result
    // use result
} else {
    val error = response.error
    wg.logE("Tag", "error: $error")
}
```

This reference covers the core concepts and APIs needed to build KuiklyUI applications. 

For detailed component-specific documentation, refer to the individual component API documentation.

For more advanced usage, search more in /kuikly_doc/DevGuide/ or in /kuikly_doc/API/ . If the user's problem can't be solved precisely according to existing documentations, please prompt the user.

如果用户在问题中用中文提问，也请你请用中文回答（虽然这篇文档是用英文写的）。