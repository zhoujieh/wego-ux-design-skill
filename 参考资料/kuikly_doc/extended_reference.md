# KuiklyUI Extended Reference

This document supplements [`basic_reference.md`](./basic_reference.md) with the deeper "why" and "how" behind KuiklyUI — the mental model, the parts that bite you, and the full APIs that the basic reference only mentions in passing. Read `basic_reference.md` first; this one assumes you have already.

Two reading orders work:
- **Top-to-bottom** to *understand* the framework as a whole (recommended on first pass).
- **As a reference** by jumping to a section when something surprises you.

The companion in-house component library (WGButton, WGImage, WGSwitch, …) is documented separately under [`basic_components/`](./basic_components/index.md); this document focuses on the framework itself (Kuikly core) and its bundled components.

---

## Table of contents

1. [Mental model](#1-mental-model)
2. [The Pager (pages)](#2-the-pager-pages)
3. [The ComposeView (reusable components)](#3-the-composeview-reusable-components)
4. [Reactivity in depth](#4-reactivity-in-depth)
5. [Directives (vfor, vif, vbind) — what they actually do](#5-directives-vfor-vif-vbind--what-they-actually-do)
6. [FlexBox layout in depth](#6-flexbox-layout-in-depth)
7. [Style attributes — the full set](#7-style-attributes--the-full-set)
8. [The event system](#8-the-event-system)
9. [ViewRef — talking to a view imperatively](#9-viewref--talking-to-a-view-imperatively)
10. [Animation — declarative and imperative](#10-animation--declarative-and-imperative)
11. [setTimeout and the Kuikly thread](#11-settimeout-and-the-kuikly-thread)
12. [Modules — the platform bridge](#12-modules--the-platform-bridge)
13. [Networking](#13-networking)
14. [Notifications (NotifyModule)](#14-notifications-notifymodule)
15. [Routing (RouterModule) and multi-page communication](#15-routing-routermodule-and-multi-page-communication)
16. [Caching: MemoryCacheModule and SharedPreferencesModule](#16-caching-memorycachemodule-and-sharedpreferencesmodule)
17. [Other built-in modules (Codec, Calendar, Snapshot, Performance)](#17-other-built-in-modules-codec-calendar-snapshot-performance)
18. [Threading and coroutines](#18-threading-and-coroutines)
19. [Assets and images — under the hood](#19-assets-and-images--under-the-hood)
20. [Extending Kuikly: custom Modules](#20-extending-kuikly-custom-modules)
21. [Extending Kuikly: custom Views and view props](#21-extending-kuikly-custom-views-and-view-props)
22. [Multi-module projects](#22-multi-module-projects)
23. [Protobuf](#23-protobuf)
24. [Components reference (deep)](#24-components-reference-deep)
25. [Performance guidelines](#25-performance-guidelines)
26. [Common pitfalls and idioms](#26-common-pitfalls-and-idioms)

---

## 1. Mental model

Kuikly compiles a single Kotlin codebase to native-rendered apps on Android, iOS, HarmonyOS, H5/Web, and WeChat Mini Programs. Two pieces:

- **KuiklyCore** runs your Kotlin code. It builds a **virtual tree** of `DeclarativeBaseView` nodes from your `body()` function, runs FlexBox layout, and tracks reactive dependencies.
- **KuiklyRender** is the per-platform renderer. It maps each virtual node to a real platform widget (`UIView`, `View`, `ArkUI_NodeHandle`, DOM element, …) and applies the styling/events that Core describes.

Two facts fall out of this and they matter constantly:

1. **All Kuikly UI work happens on the "Kuikly thread"** — a single dedicated thread that owns the virtual tree, observables, layout, `setTimeout`, and animations. You may never touch a `View`, `Attr`, observable, or `setTimeout` from another thread.
2. **Components are descriptions, not widgets.** When you write `Text { attr { text("hello") } }`, you are appending a `TextView` virtual node to the parent's child list inside a `ViewBuilder` closure. The body re-runs (or partially re-runs, via reactive bindings) when observables change. The platform widget is created lazily by the renderer.

You will write three kinds of "things":

| Thing | What it is | Where you put it |
|---|---|---|
| `Pager` | A page entry. One per route. | Annotated with `@Page("name")` |
| `ComposeView<A,E>` | A reusable, attribute/event-shaped component without its own native widget — it's a recipe of children. | Anywhere, exposed via `ViewContainer<*,*>.MyView { ... }` DSL helper |
| `DeclarativeBaseView<A,E>` | A leaf that maps to a real platform widget. Almost always **provided** by Kuikly (Text, Image, View, List, …). You only subclass this when extending native UI. | Custom native view authoring only |

Forms of state:

- `observable` / `observableList` / `observableSet` for **reactive UI state**. Bound to the `PageScope` they were created in (see §4).
- Plain Kotlin properties on a `Pager` / `ComposeView` for **non-reactive state** (e.g. cached config, refs you hold imperatively).
- `ComposeAttr` for **inputs from the parent** (props). Some of its fields you mark `by observable` so they trigger updates; others are plain because they're read once at creation.

---

## 2. The Pager (pages)

### 2.1 Registration

Each page is a `Pager` subclass annotated with `@Page("name")`. The framework discovers `@Page` classes through KSP at build time and registers a factory closure keyed by the name string. When the native side asks the renderer to open `"name"`, the closure is invoked and a fresh `Pager` instance is built.

```kotlin
@Page("HelloWorld")
class HelloWorldPage : Pager() {              // or `BasePager`, the project's convention
    override fun body(): ViewBuilder = { ... }
}
```

`Pager` vs `BasePager`: in this codebase business pages extend `BasePager`, which is a thin wrapper adding shared logging, error handling, and module preloading. Follow the local convention.

### 2.2 Lifecycle

```
                ┌────────────────┐
                │   constructor  │
                └───────┬────────┘
                        ▼
                   ┌─────────┐                ← `pagerData` becomes available here.
                   │ created │                  Do data fetches, addNotify, etc.
                   └────┬────┘                  Calling `acquireModule` before this
                        ▼                       throws `PagerNotFoundException`.
                   ┌────────┐
                   │ body() │                 ← Called once; returns a description.
                   └────┬───┘                   Reactive bindings inside it will
                        ▼                       cause partial re-runs later.
              ┌──────────────────┐
              │  pageDidAppear   │
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ pageDidDisappear │            ← Pair these for analytics/timers.
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ pageWillDestroy  │            ← Final teardown. Module calls into
              └──────────────────┘              Native are NOT guaranteed to land
                                                here — clean up on the native side
                                                instead if it must run.
```

Override only what you need. `body()` is the only required override.

Inside `body()`, `attr {}` at the very top sets attributes on the page **root view** (the page itself is a `View`). Don't write a wrapping `View {}` just for that; the page is already one.

### 2.3 PagerData — what the native side hands you

`pagerData` exposes both **framework basics** and **business params** the native opener passed in. See `DevGuide/page-data.md` for the table; the gotchas:

- `pagerData` is **not** safe to access from class initialisers or `companion object` initialisers — there is no current pager yet, so `PagerManager.getCurrentPager()` throws `PagerNotFoundException`. Access it from `created()` onward.
- `params` is a `JSONObject`. The idiom in this codebase is to define typed extensions on `PageData` so business code stays readable:
  ```kotlin
  internal val PageData.fromFirstPage: String
      get() = params.optString("fromFirstPage")
  ```
- `pageViewWidth / pageViewHeight` are the **root view** dimensions in dp/pt — not screen dimensions. Use `deviceWidth / deviceHeight` if you really want the full screen. Most layouts should use `pageViewWidth`.
- `safeAreaInsets` reflects status bar / notch / home indicator. `statusBarHeight` is a convenience for the top inset.

### 2.4 Page events: native → Kuikly

Native code can push named events into a live page (independent of NotifyModule, which is broadcast-style).

```kotlin
override fun onReceivePagerEvent(pagerEvent: String, eventData: JSONObject) {
    super.onReceivePagerEvent(pagerEvent, eventData)
    when (pagerEvent) {
        "refresh" -> reload()
    }
}
```

Native-side sender APIs (see `DevGuide/pager-event.md`):
- Android: `kuiklyRenderViewDelegator.sendEvent("name", mapOf(...))`
- iOS: `[self.delegator sendWithEvent:@"name" data:@{...}]`
- HarmonyOS: `controller.sendEvent("name", { key: value })`

A `ComposeView` deep in the tree can observe page events too — implement `IPagerEventObserver`, register on `viewDidLoad`, **and unregister on `viewDidUnload`** or you will leak the component.

### 2.5 Multi-page communication

Each Kuikly page is a **separately initialized instance** with its own observables. If your app is in *dynamic mode* (downloading JS bundles at runtime), each page is also an *isolated JS context* — global Kotlin `companion object` state is **not shared** across instances. Even in built-in mode where it would be shared, `observable` is bound to the page scope that created it, so a global observable will only update the page that created it.

Pass initial data via `RouterModule.openPage("name", JSONObject().apply { put("digit", 42) })` and read it from `pagerData.params` on the other side. For live updates, use `NotifyModule` (see §14).

---

## 3. The ComposeView (reusable components)

### 3.1 Anatomy

```kotlin
class NavBarAttr : ComposeAttr() {
    var title by observable("")     // reactive prop — changes re-run body() bindings
    var showBackButton = true       // non-reactive — read once when used
}

class NavBarEvent : ComposeEvent() {
    var backClickHandler: (() -> Unit)? = null
    fun onBackClick(handler: () -> Unit) { backClickHandler = handler }
}

class NavBarView : ComposeView<NavBarAttr, NavBarEvent>() {
    override fun createAttr() = NavBarAttr()
    override fun createEvent() = NavBarEvent()
    override fun body(): ViewBuilder = {
        val ctx = this@NavBarView
        // build UI; read `attr.title`, fire `event.backClickHandler`, etc.
    }
}

fun ViewContainer<*, *>.NavBar(init: NavBarView.() -> Unit) {
    addChild(NavBarView(), init)
}
```

Usage:

```kotlin
NavBar {
    attr { title = "Page Title"; showBackButton = true }
    event { onBackClick { /* ... */ } }
}
```

Inside the user's `attr {}` closure the receiver is the **same `NavBarAttr` instance** that `createAttr()` produced. Same story for `event {}`. There is no copying.

### 3.2 Lifecycle (full set)

| Callback | Fires | Typical use |
|---|---|---|
| `created` | Before `body()`. `attr` and `event` already exist. | Pull data; subscribe to NotifyModule; `bindValueChange`. |
| `viewWillLoad` | Before the UI subtree is mounted. | Rare — pre-layout setup. |
| `viewDidLoad` | After the UI subtree has been built. | Register `IPagerEventObserver`; kick off async loads that need refs. |
| `viewDidLayout` | After the first layout pass. Sizes/positions are known. | Start animations; measure-dependent setup. |
| `viewWillUnload` | About to be removed from the tree. | Symmetric teardown of `viewWillLoad`. |
| `viewDidUnload` | Has been removed. | Unregister observers; cancel network. |
| `viewDestroyed` | Final destruction. | Drop refs. |

Cleanup symmetry is what prevents leaks. Anything you registered with the pager from inside a ComposeView (event observers, notify callbacks) must be unregistered in `viewDidUnload` / `viewDestroyed`.

### 3.3 `bindValueChange` — react to a single attr

When `attr.title` changes you usually don't need to do anything (text bindings inside `body()` re-run automatically). But if a change must trigger **side effects** (call into native, log, kick off animation, …), use `bindValueChange`:

```kotlin
override fun created() {
    bindValueChange({ attr.title }) { newTitle ->
        wg.logD("NavBar", "title -> $newTitle")
    }
}
```

The closure also runs once for the initial value.

### 3.4 Composing vs. native: when to extend which

| Need | Use |
|---|---|
| Combine existing Kuikly views into a reusable shape | `ComposeView` |
| Wrap a platform-native widget (e.g. a custom camera preview, an in-house chart) | `DeclarativeBaseView` + per-platform `IKuiklyRenderViewExport` impls (§21) |
| Add one prop to an existing view (e.g. `myProp` that platform-side does X) | `viewPropExternalHandler` (§21) |

---

## 4. Reactivity in depth

### 4.1 What an `observable` actually is

`by observable(initial)` installs a Kotlin property delegate that:

1. Owns a per-property value.
2. On reads, registers the **current reactive scope** as a subscriber. The "current scope" is the closure currently being evaluated — an `attr {}` block, a `vif {}` predicate, a `renderList {}` source, etc.
3. On writes, looks up all subscribers and schedules them to re-run.

That re-run is *fine-grained* — only the dependent expression rebuilds, not the whole `body()`. This is why you typically write:

```kotlin
Text { attr { text(ctx.counter.toString()) } }   // ✅ only this attr re-runs
```

and not:

```kotlin
Text { attr { text(myCachedCounterString) } }    // ❌ won't update on counter++
```

### 4.2 PageScope: where observables live

Every observable is **bound to a `PageScope`** — usually the Pager or ComposeView in which it was declared. The framework looks at the receiver of the `by observable(...)` delegate to figure out the scope. That means:

- **You cannot `by observable(0)` at file or `companion object` top level** — there is no scope to attach to. The Kotlin compiler will warn you that `observable()` is deprecated in that context.
- A "global" observable bound to a specific page only updates that page's UI. If you want true cross-page state, propagate through `NotifyModule` instead, and re-derive the per-page observable on receipt.

If you need a shared `ViewModel` across pages, declare its observables on a `PageScope` parameter:

```kotlin
class CounterVM(scope: PagerScope) {
    var count by scope.observable(0)
}
```

`PagerScope` is implemented by every `Pager` and every `ViewContainer`, so any view holder can be a scope.

### 4.3 `observableList` / `observableSet`

These are reactive containers. Mutations (`add`, `remove`, `clear`, indexed `set`) emit fine-grained change events that `renderList` / `vfor` consume to do incremental DOM updates.

**Mutations are reactive, but only on the container itself.** If you replace an element with the same identity (`list[i] = list[i]`), the framework still treats it as a change and re-renders that one item — useful when you've mutated an internal field of an item:

```kotlin
private inline fun <reified T> ObservableList<T>.notifyUpdate(index: Int) {
    this[index] = this[index]   // force a re-render of just this index
}
```

Use this sparingly; it's a hack against the model.

`ObservableList<T>` exposes the full `MutableList<T>` API. For thread-safety variants:

```kotlin
var thing by observable(ObservableThreadSafetyMode.NONE, init = 0f)
```

Use `NONE` for high-frequency animation-driven state where you've reasoned about access; the default has a tiny synchronization cost.

### 4.4 The `val ctx = this` pattern

`body()` returns a `ViewBuilder` — a function literal with `ViewContainer<*,*>` as its receiver. Inside that closure, `this` is the container, **not** the Pager. To read the Pager's reactive properties you grab a reference outside the closure:

```kotlin
override fun body(): ViewBuilder {
    val ctx = this                  // ← captures the Pager
    return {
        Text { attr { text(ctx.counter.toString()) } }
    }
}
```

If you forget this and write `this.counter`, you'll get a "no such property" error — the receiver is the container, not the Pager.

---

## 5. Directives (vfor, vif, vbind) — what they actually do

Kuikly ships two related families: the original directives (`vfor`, `vforIndex`, `vforLazy`, `vif/velseif/velse`, `vbind`) and the in-house `renderList`/`renderLazyList` wrappers. This codebase prefers `renderList` (see basic_reference.md). Even so, the underlying directives matter because everything reduces to them.

### 5.1 `vfor` — reactive iteration

```kotlin
vfor({ ctx.list }) { item ->
    Text { attr { text(item) } }
}
```

- The closure **must return a reactive container**, hence the `({ ctx.list })` — a closure, not the container directly.
- On `list.add(x)`, only one new child is created. On `list.removeAt(i)`, only that child is destroyed. The framework diffs by index, not identity.
- All virtual nodes are created upfront (even off-screen ones in a `List`). Only platform widgets are recycled.

### 5.2 `vforIndex` — index-aware

Same as `vfor` but the item closure receives `(item, index, count)`. Important caveat: **only items whose data changed re-render.** If your render depends on `index` (e.g. a zebra background) and you insert at the front of the list, items in the middle keep their old `index` from the previous render. To force a refresh, mutate the elements whose index changed (`list[i] = list[i]`).

### 5.3 `vforLazy` — defer virtual-node creation

For `List` only (not `PageList`, `WaterFallList`, etc.), `vforLazy` creates virtual nodes for visible items only, not the full list. Use when:

- Item virtual nodes are themselves heavy (lots of children),
- The list has thousands of items, **and**
- Memory matters more than scroll-time CPU.

The default `vfor` is faster to scroll but heavier on memory and CPU at first paint with very large lists.

### 5.4 `vif` / `velseif` / `velse` — reactive conditional

```kotlin
vif({ ctx.uiState == 1 }) { Text { ... } }
velseif({ ctx.uiState == 2 }) { View { ... } }
velse { Text { ... } }
```

Mounts/unmounts subtrees as the predicate flips. Note this is *unmount*, not *hide*: state inside an unmounted subtree (focus, scroll position, `keepAlive`, …) is gone. Use `visibility(false)` if you want to keep the subtree alive but invisible.

### 5.5 `vbind` — switch-like total replacement

```kotlin
vbind({ ctx.uiState }) {
    when (it as Int) {
        1 -> Text { ... }
        2 -> View { ... }
        else -> Spacer { ... }
    }
}
```

When the bound expression changes, **all children of the enclosing component** are removed and rebuilt. It's the heavy hammer — useful for true mode-switching, but avoid it inside a complex parent because you'll lose unrelated siblings too.

### 5.6 `renderList` / `renderLazyList` (in-house wrappers)

```kotlin
import com.truedian.wg.core.components.organism.list.renderList
import com.truedian.wg.core.components.organism.list.renderLazyList

renderList({ ctx.items }) { item, index, count ->
    LiveItemCard { attr { this.item = item } }
}

renderList({ ctx.items }, isLazy = true, maxLoadItem = 30) { item, _, _ ->
    Cell { /* ... */ }
}

renderLazyList({ ctx.items }) {                  // it: T
    Cell { /* ... */ }
}
```

These wrap `vforIndex` / `vforLazy` with friendlier ergonomics and let you flip `isLazy` without touching the rest. **Use these in this codebase**, not raw `vfor`.

---

## 6. FlexBox layout in depth

KuiklyUI does not use Android's nested-layout system or iOS's autolayout — it uses standard **FlexBox** everywhere. If you've used React Native or web CSS, the rules are the same. Two axes:

- **Main axis** — set by `flexDirection`. `COLUMN` (default) → vertical; `ROW` → horizontal.
- **Cross axis** — perpendicular to main.

```
       flexDirection = COLUMN          flexDirection = ROW
       (default)
       ┌────────────┐                  ┌────────────────┐
       │ ▲ main     │                  │ ◄── main ──►   │
       │ │          │                  │ ▲              │
       │ │          │                  │ │ cross        │
       │ ▼ cross →  │                  │ ▼              │
       └────────────┘                  └────────────────┘
```

### 6.1 Defaults that bite

| Property | Default | Note |
|---|---|---|
| `flexDirection` | `COLUMN` | Children stack top-to-bottom. **Different from web CSS, which defaults to `ROW`.** |
| `alignItems` | `STRETCH` | Children fill the cross axis if they don't specify a size. **This is how a `List { attr { flex(1f) } }` ends up full-width even though you only set `flex(1f)`.** |
| `justifyContent` | `FLEX_START` | Children pack to the start of the main axis. |
| `flexWrap` | `NOWRAP` | Overflow children are clipped or pushed off-screen — they do not wrap. |
| `overflow` | `false` | Children that overflow the parent's bounds are still visible. **Different from Android, same as iOS.** Set `overflow(true)` to clip. |

### 6.2 `width`/`height` vs. content sizing

If you don't set a dimension, the view sizes to its content along that axis. This is why:

```kotlin
Text { attr { text("hi") } }   // sizes to the text width and font line-height
```

Just works. But:

```kotlin
View {                          // empty → 0×0 → invisible
    backgroundColor(Color.RED)
}
```

won't render unless you set a size, give it children, or set both `top/bottom` (absolute) or `left/right` to take a full extent.

### 6.3 `flex(1f)` — what it really means

`flex(1f)` on a child means *take all remaining main-axis space the parent has after fixed-size siblings*. It does **not** mean "fill the parent in both directions". The classic example:

```kotlin
View { attr { flexDirectionColumn(); size(W, H) }
    NavBar { /* fixed 56f tall */ }
    List { attr { flex(1f) } }       // ← takes H - 56f tall; cross-axis (width) is STRETCH default → full width
}
```

To `flex(1f)` along width instead, set the parent's `flexDirection` to `ROW`.

Multiple `flex` siblings split the remaining space in their ratios (`flex(1f) + flex(2f) → 1:2`).

### 6.4 Absolute positioning

`positionAbsolute()` removes the view from the flex flow. The view positions relative to its parent using `left/top/right/bottom`. With both `left(0f); right(0f)` it stretches to parent width; with both `top(0f); bottom(0f)` it stretches to parent height. Absolute children **don't influence the parent's size or sibling layout**.

Common pattern — full-screen background:

```kotlin
View {
    attr { size(pagerData.pageViewWidth, pagerData.pageViewHeight) }
    Image { attr {
        positionAbsolute(); left(0f); right(0f); top(0f); bottom(0f)
        src(BG_URL); resizeCover()
    }}
    // foreground content here, laid out normally
}
```

### 6.5 `padding` vs `margin` and the leaf-component rule

- `padding(left = ..., top = ..., bottom = ..., right = ...)` is space inside the view, between its border and its children.
- `margin(...)` is space outside the view, between it and siblings.
- **Leaf components (Text, Image, Input, …) do not support `padding`.** Use `margin` on the leaf, or wrap it in a `View` and pad the wrapper.
- There is **no `paddingHorizontal` / `paddingVertical` shorthand** — set each side, or use `padding(15f)` for all four.

### 6.6 Common layout recipes (full versions in `DevGuide/flexbox-in-action.md`)

**Title bar with absolute back arrow:**
```kotlin
View {
    attr {
        height(56f); marginTop(pagerData.statusBarHeight)
        justifyContentCenter(); alignItemsCenter()       // centers title
    }
    View {                                                // ← absolute wrapper for back arrow
        attr {
            positionAbsolute(); left(14f); top(0f); bottom(0f)
            justifyContentCenter(); alignItemsCenter()
        }
        Image { /* back arrow */ }
    }
    Text { /* title text */ }
}
```

**List that fills the screen below a navbar:**
```kotlin
View {
    attr { flexDirectionColumn() /* page root */ }
    NavBar { /* 56f */ }
    List { attr { flex(1f) /* fills remaining vertical space */ } }
}
```

**Row with right-aligned button:**
```kotlin
View {
    attr { flexDirectionRow(); alignItemsCenter() }
    View { /* avatar */ }
    View { /* center text column */ }
    View {                                                // spacer + right-aligner
        attr { flex(1f); flexDirectionRow(); justifyContentFlexEnd() }
        Button { /* right-aligned */ }
    }
}
```

---

## 7. Style attributes — the full set

`basic_reference.md` covers the common ones. The complete list of style methods on every component:

### 7.1 Background

```kotlin
attr {
    backgroundColor(Color.RED)
    backgroundColor(0xFFFF0000)                    // also accepts Long hex
    backgroundLinearGradient(
        Direction.TO_BOTTOM,                       // TO_TOP/BOTTOM/LEFT/RIGHT + 4 diagonals
        ColorStop(Color.RED, 0f),
        ColorStop(Color.GREEN, 0.3f),              // can have any number of stops
        ColorStop(Color.BLACK, 1f)
    )
}
```

Caveat: gradient color stops on Android require API ≥ 29.

### 7.2 Border & corners

```kotlin
border(Border(2f, BorderStyle.SOLID, Color.BLACK))       // SOLID, DOTTED, DASHED
borderRadius(10f)                                         // all corners
borderRadius(BorderRectRadius(topLeft, topRight, bottomLeft, bottomRight))
```

### 7.3 Shadow

```kotlin
boxShadow(BoxShadow(offsetX = 0f, offsetY = 2f, shadowRadius = 4f, shadowColor = Color.GRAY))
```

For Text-specific shadow there's also `textShadow(offsetX, offsetY, shadowRadius, color)`.

### 7.4 Transform

```kotlin
attr {
    transform(
        rotate = Rotate(45f),                              // degrees, [-360, 360]
        scale = Scale(1.5f, 1.5f),                         // multiplier
        translate = Translate(0.5f, 0.0f),                 // % of own size, [-1, 1]
        anchor = Anchor(0.5f, 0.5f)                        // pivot, % of own size
    )
}
```

You can pass only the args you need; others default to the identity. The pivot defaults to the center.

`Translate` is in *self-percentages*, not pixels. To translate 100f to the right of a 200f-wide view, `Translate(0.5f, 0f)`.

### 7.5 Visibility, opacity, interaction

```kotlin
visibility(false)        // hides but keeps subtree alive (cf. vif which unmounts)
opacity(0.5f)            // 0.0..1.0
touchEnable(false)       // disables hit-testing on this view + children
zIndex(1)                // higher renders on top of lower; default 0
overflow(true)           // clip children that exceed bounds
keepAlive(true)          // for direct children of scroll containers; survive going off-screen
accessibility("label")   // TalkBack/VoiceOver label
```

`keepAlive` matters for stateful items in long lists — e.g. a video card whose playback you don't want to reset when scrolled offscreen. It costs memory; use it deliberately.

### 7.6 Sizing constraints

```kotlin
width(100f); height(50f); size(100f, 50f)
maxWidth(200f); minWidth(50f); maxHeight(...); minHeight(...)
```

Min/max constraints interact with `flex` — `flex(1f)` plus `maxWidth(300f)` produces a flex-grow item that stops growing at 300f.

### 7.7 Color helpers

`com.tencent.kuikly.core.base.Color`:
- Constants: `Color.RED`, `Color.BLACK`, `Color.WHITE`, `Color.GRAY`, `Color.TRANSPARENT`, …
- Constructors: `Color(0xFF03C160)` (ARGB hex), `Color(red255, green255, blue255, alpha01)`.
- The in-house alternative is `WGColor` from `kuikly_business_*` modules — use that in business code for design-system consistency. See `basic_components/WGColor.md`.

---

## 8. The event system

`basic_reference.md` covers click/longPress/pan. The full set on **every component**:

### 8.1 Touch & gesture events

| Event | Params | Notes |
|---|---|---|
| `click(ClickParams)` | `x`, `y` (relative to component) | Tap. |
| `doubleClick(ClickParams)` | same | Double tap. **Mutually exclusive with click** — registering both delays the click event slightly while the framework waits to see if a second tap arrives. |
| `longPress(LongPressParams)` | `x, y, state` | `state` cycles `start → move → end`. Treat `start` as the firing point. |
| `pan(PanGestureParams)` | `x, y, pageX, pageY, state` | `start → move → end`. `pageX/Y` are page-root coordinates; `x/y` are component-relative. See basic_reference.md for the canonical drag pattern. |

### 8.2 Lifecycle / visibility events (per-component, not per-page)

| Event | Fires |
|---|---|
| `willAppear` | Component about to become visible. |
| `didAppear` | Component fully on-screen. **Do not use on the page root — use `pageDidAppear` on the Pager instead.** |
| `willDisappear` | Component about to leave visibility. |
| `didDisappear` | Component fully off-screen. |
| `appearPercentage((Float) -> Unit)` | Continuously, with 0.0..1.0 visibility ratio. Useful for scroll-driven animation triggers. |
| `layoutFrameDidChange((Frame) -> Unit)` | After every layout pass that changed this component's `x/y/width/height`. |
| `animationCompletion((AnimationCompletionParams) -> Unit)` | After a declarative animation finishes. See §10. |

### 8.3 Raw touch events (View component only)

```kotlin
event {
    touchDown { p ->
        val pointerId = p.pointerId         // multi-touch
        val touches = p.touches              // list of all current touches
        // action: "down" / "move" / "up" / "cancel" — distinguishes lifecycle
    }
    touchMove { p -> ... }
    touchUp { p -> ... }            // up + cancel pre-1.1.86; up only ≥ 1.1.86 if touchCancel is also registered
    touchCancel { p -> ... }        // requires ≥ 1.1.86; otherwise cancel falls into touchUp
}
```

The high-level `click/longPress/pan` consume these; usually you don't need touch events directly. Reach for them when you implement a non-standard gesture (pinch, custom multi-finger).

### 8.4 Component-specific events

Each component has its own additions — `Input.textDidChange`, `List.scroll`, `Refresh.refreshStateDidChange`, `Slider.progressDidChanged`, etc. They live in §24 and in the API docs.

---

## 9. ViewRef — talking to a view imperatively

The reactive system handles state-driven updates. Some operations are *imperative* — scrolling a list to an offset, focusing an input, calling a `Canvas` redraw. For those you need a handle on the actual view.

```kotlin
class MyPage : Pager() {
    private var listRef: ViewRef<ListView<*, *>>? = null

    override fun body(): ViewBuilder {
        val ctx = this
        return {
            List {
                ref { ctx.listRef = it }                     // ← capture
                attr { flex(1f) }
            }
            Button {
                event {
                    click { ctx.listRef?.view?.setContentOffset(0f, 100f, animated = true) }
                }
            }
        }
    }
}
```

Conventions:
- The closure passed to `ref { }` runs **once**, right after the view is registered (well before `viewDidLayout`).
- `ViewRef.view` is nullable — the view may be unmounted by `vif`, list recycling, etc. Always null-check.
- For a `View` component, the ref type is `ViewRef<DivView>`. For a `List`, `ViewRef<ListView<*,*>>`. For custom views, it's your `DeclarativeBaseView` subclass.

`ref` does *not* make the view reactive — capturing a ref doesn't subscribe you to anything.

---

## 10. Animation — declarative and imperative

Kuikly offers two animation styles. They animate the same set of properties — pick by ergonomics.

### 10.1 Animatable properties

- `transform` — translate, rotate, scale (always with optional `Anchor`).
- `opacity`
- `backgroundColor`
- `frame` — i.e. width/height/x/y. Animating `size(w, h)` or `absolutePosition(...)` triggers this.

### 10.2 Curves (`Animation.*`)

Eight built-ins, each constructible as `Animation.linear(durationSeconds, delaySeconds, repeatCount, key)`:

| Curve | Shape |
|---|---|
| `linear` | constant velocity |
| `easeIn` | slow start, fast end |
| `easeOut` | fast start, slow end |
| `easeInOut` | slow at both ends |
| `springLinear`, `springEaseIn`, `springEaseOut`, `springEaseInOut` | spring variants of the above |

All times are in **seconds**, not milliseconds.

The `key` parameter (optional) tags the animation so completion callbacks and child-scope lookup can identify it. Useful when you have multiple animations and need to disambiguate which one finished.

### 10.3 Declarative animation

```kotlin
private var pressed by observable(false)

View { attr {
    if (ctx.pressed) {
        transform(scale = Scale(0.95f, 0.95f))
        backgroundColor(Color.BLUE)
    } else {
        transform(scale = Scale(1f, 1f))
        backgroundColor(Color.GRAY)
    }
    animate(Animation.easeInOut(0.3f), ctx.pressed)   // ← bind the curve to a trigger
}}
```

The trigger value (`ctx.pressed` here) is what `animate` watches — when it changes, all property writes **above** the `animate(...)` call in the same `attr {}` block become animated transitions.

**Scope rule** (`DevGuide/animation-declarative.md`): an `animate(...)` call applies to property writes between *the previous* `animate(...)` (or `attr {` opening) and itself. So you can split:

```kotlin
attr {
    // Group 1: translate over 1s
    absolutePosition(top = 10f, left = if (anim) 110f else 10f)
    animate(Animation.linear(1f), anim)

    // Group 2: rotate over 2s
    transform(Rotate(if (anim) 90f else 0f))
    animate(Animation.linear(2f), anim)

    // Group 3: bg color over 3s
    backgroundColor(if (anim) Color.BLUE else Color.YELLOW)
    animate(Animation.linear(3f, key = "bg"), anim)
}
```

**Parent → child propagation**: `animate(...)` bound to a parent also animates layout changes its children experience as a result of the parent's change (e.g. a sibling shifting because the parent grew). Children with their own `animate` override the parent's.

**Completion**: listen with `animationCompletion`:

```kotlin
event {
    animationCompletion { params ->
        val finished = params.finish == 1       // 0 if cancelled
        val which = params.attr                  // e.g. Attr.StyleConst.TRANSFORM
    }
}
```

The `attr` field is how you tell which property's animation just ended when multiple are active.

### 10.4 Imperative animation (`animateToAttr`)

When you have a `ViewRef`, you can animate from outside the `body()` closure:

```kotlin
viewRef?.view?.animateToAttr(
    Animation.linear(0.5f),
    attrBlock = {
        opacity(0f)
        transform(Scale(0.5f, 0.5f))
    },
    completion = { finished ->
        // chain next step
    }
)
```

This is the preferred path when you need to:
- Chain animations through callbacks (cleaner than tracking flags).
- Trigger from outside `body()` (e.g. a Module callback).
- Animate independently of any observable.

### 10.5 Serial and parallel patterns

**Serial via completion**:
```kotlin
ref?.view?.animateToAttr(Animation.easeInOut(0.5f), {
    transform(Translate(0f, 0.5f))
}, completion = {
    ref?.view?.animateToAttr(Animation.easeIn(0.5f), { backgroundColor(Color.GREEN) })
})
```

**Serial via delay (when animating different properties)**:
```kotlin
absolutePosition(top = 10f, left = if (a) 110f else 10f)
animate(Animation.linear(1f, delay = 0f), a)
transform(Rotate(if (a) 90f else 0f))
animate(Animation.linear(2f, delay = 1f), a)              // ← starts 1s in
```

**Parallel**: put multiple property writes in one `attrBlock`, or bind multiple `animate(...)` calls to the same trigger. Trivial.

---

## 11. setTimeout and the Kuikly thread

```kotlin
setTimeout(2 * 1000) {            // ← delay in milliseconds
    // runs on Kuikly thread, 2s later
}
```

`setTimeout(0)` schedules to the **next frame** on the Kuikly thread — the canonical way to "do this after the current event finishes but before layout/paint". Useful for animation flags that need a tick to settle before they animate.

There is no `clearTimeout`. To make a timer cancelable, gate it with a flag:

```kotlin
private var cancelTimer = false
setTimeout(300) {
    if (cancelTimer) return@setTimeout
    // ...
}
```

`setTimeout` only runs on the Kuikly thread. If you need work off-thread, see §18.

---

## 12. Modules — the platform bridge

Modules expose platform capabilities (network, file I/O, navigation, notifications, calendar, …) through a uniform Kotlin API. The Kotlin side declares the interface; each platform implements it.

### 12.1 Acquiring modules

```kotlin
// In Pager / ComposeView:
val cache = acquireModule<MemoryCacheModule>(MemoryCacheModule.MODULE_NAME)   // throws if missing
val cacheOpt = getModule<MemoryCacheModule>(MemoryCacheModule.MODULE_NAME)    // null if missing

// From a plain class:
val mod = PagerManager.getCurrentPager()
    .acquireModule<MemoryCacheModule>(MemoryCacheModule.MODULE_NAME)
```

Each acquisition is cheap — modules are singletons per page. But idiomatic code stores the result in a `by lazy` property when it's used in event handlers:

```kotlin
private val routerModule by lazy(LazyThreadSafetyMode.NONE) {
    acquireModule<RouterModule>(RouterModule.MODULE_NAME)
}
```

`LazyThreadSafetyMode.NONE` is fine because access is always on the Kuikly thread.

### 12.2 The built-in module catalogue

| Module | What it does | See |
|---|---|---|
| `RouterModule` | Open/close pages | §15, `API/modules/router.md` |
| `NotifyModule` | Page↔page, page↔native event bus | §14, `API/modules/notify.md` |
| `NetworkModule` | Low-level HTTP (GET/POST, binary) | §13, `API/modules/network.md` |
| `MemoryCacheModule` | Page-scoped in-memory cache; also caches images | §16, `API/modules/memory-cache.md` |
| `SharedPreferencesModule` | Tiny key/value disk cache | §16, `API/modules/sp.md` |
| `SnapshotModule` | iOS-only; snapshot the page for first-frame optimisation in dynamic mode | §17, `API/modules/snapshot.md` |
| `CodecModule` | URL/base64 encode/decode, MD5, SHA-256 | §17, `API/modules/codec.md` |
| `CalendarModule` | Date formatting, parsing, arithmetic | §17, `API/modules/calendar.md` |
| `PerformanceModule` | Launch time, FPS, memory metrics | §17, `API/modules/performance.md` |

Application code in this repo also has the **in-house `elegantNetWorkRequest`** wrapper around `NetworkModule` — see basic_reference.md §"Network Requests" — *that's what business code should call*, not `NetworkModule` directly.

---

## 13. Networking

### 13.1 Two layers

1. **`NetworkModule`** — low-level, JSON-string params and callbacks. Use only if you need raw control or the elegant wrapper doesn't cover your case.
2. **`elegantNetWorkRequest`** (`com.truedian.wg.core.base.network.elegantNetWorkRequest`) — high-level, suspend-fn-based, with `kotlinx.serialization` deserialization. **Default to this** in business code. See basic_reference.md for the full pattern.

### 13.2 `NetworkModule` API

| Method | Params | Use |
|---|---|---|
| `requestGet(url, param, responseCallback)` | `String`, `JSONObject`, `NMAllResponse` | GET, JSON response. |
| `requestPost(url, param, responseCallback)` | same | POST, JSON. |
| `httpRequest(url, isPost, param, headers?, cookie?, timeout?, responseCallback)` | + `Boolean`, headers, cookie string, timeout in seconds | General-purpose. |
| `requestGetBinary(url, param, responseCallback)` | last arg is `NMDataResponse` → `ByteArray` | Binary GET. |
| `requestPostBinary(url, bytes, responseCallback)` | `ByteArray` body | Binary POST. |
| `httpRequestBinary(url, isPost, bytes, param?, headers?, cookie?, timeout?, responseCallback)` | mixed | General binary. |

Callback signatures:
```kotlin
typealias NMAllResponse  = (data: JSONObject, success: Boolean, errorMsg: String, response: NetworkResponse) -> Unit
typealias NMDataResponse = (data: ByteArray,  success: Boolean, errorMsg: String, response: NetworkResponse) -> Unit

class NetworkResponse(
    val headerFields: JSONObject,
    val statusCode: Int?           // nullable on some platforms
)
```

Example (only used when the elegant wrapper is unsuitable):

```kotlin
acquireModule<NetworkModule>(NetworkModule.MODULE_NAME).httpRequest(
    url = "https://api.example.com/v1/data",
    isPost = false,
    param = JSONObject().apply { put("id", 1) },
    responseCallback = { data, success, errorMsg, response ->
        if (success) {
            val items = data.optJSONArray("items") ?: JSONArray()
            // ... walk items
        } else {
            wg.logE("Net", "fail: $errorMsg status=${response.statusCode}")
        }
    }
)
```

### 13.3 Suspending wrapper — typical shape

See basic_reference.md for the canonical pattern. The minimal recap:

```kotlin
suspend fun fetchUser() = postFormRequest(ApiPaths.USER_INFO)
    .bodyParams(jsonOf("uid" with uid))
    .send<UserInfoResponse>()

// Inside a Pager:
async {
    val resp = fetchUser()
    if (resp.success && resp.data?.success == true) {
        user = resp.data?.result?.user
    }
}
```

Everything inside `async {}` is on the Kuikly thread by default (the wrapper does thread-hopping for you under the hood).

---

## 14. Notifications (NotifyModule)

Three flows:
1. Page → Page (same app, same Kuikly runtime).
2. Native → Page (push events into Kuikly).
3. Page → Native (Kuikly tells Native something happened).

### 14.1 Page↔Page

```kotlin
class FooPage : Pager() {
    private lateinit var notifyRef: CallbackRef

    override fun created() {
        super.created()
        notifyRef = acquireModule<NotifyModule>(NotifyModule.MODULE_NAME)
            .addNotify("user.login.changed") { data ->
                val newUid = data?.optString("uid") ?: return@addNotify
                // ...
            }
    }

    override fun pageWillDestroy() {
        acquireModule<NotifyModule>(NotifyModule.MODULE_NAME)
            .removeNotify("user.login.changed", notifyRef)
        super.pageWillDestroy()
    }
}
```

To broadcast:
```kotlin
acquireModule<NotifyModule>(NotifyModule.MODULE_NAME)
    .postNotify("user.login.changed", JSONObject().apply { put("uid", uid) })
```

Always pair `addNotify` with `removeNotify` in `pageWillDestroy` — otherwise the callback leaks the page.

`CallbackRef` is opaque — you only use it to remove.

### 14.2 Native → Page

The Kuikly side listens identically (`addNotify`). The Native side posts using each platform's native broadcast mechanism, which the framework forwards into `NotifyModule`:

- **iOS**: `[[NSNotificationCenter defaultCenter] postNotificationName:@"name" object:nil userInfo:@{...}];`
- **Android**: `context.sendKuiklyEvent("name", JSONObject().apply { put("k", v) })` — extension method from the Kuikly Android SDK.
- **HarmonyOS**: `emitter.emit("name", { data: { eventName: "name", stringify: "{...}" } })` — the framework reads `eventName` and `stringify` from the payload.
- **H5**: `KRNotifyModule.dispatchGlobalEvent("name", JSONObject().apply { put(...) })`.

### 14.3 Page → Native

Same `postNotify` call on the Kuikly side. The Native side listens through its platform-native mechanism:

- **iOS**: `[[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(onKr:) name:@"name" object:nil];`
- **Android**: register a `BroadcastReceiver` via the SDK's `context.registerKuiklyBroadcastReceiver(receiver)`. The intent has `getKuiklyEventName()` and `getKuiklyEventParams()` helpers.
- **HarmonyOS**: `emitter.on("name", callback)`.
- **H5**: auto-wired by the SDK; no business code needed.

### 14.4 Event names — convention

Use dotted namespaces: `module.subject.verb`. The bus is global within a runtime, so collisions silently swallow each other.

---

## 15. Routing (RouterModule) and multi-page communication

```kotlin
val router = acquireModule<RouterModule>(RouterModule.MODULE_NAME)
router.openPage("OrderDetail", JSONObject().apply { put("orderId", "12345") })
router.closePage()                                          // closes the *current* page
```

`openPage` does **not** await the new page; it returns immediately. The opened page receives the data through `pagerData.params`.

To send live updates after open, use `NotifyModule`. The canonical multi-page pattern:

1. Page A passes initial data via `openPage(pageName, params)`.
2. Page B reads from `pagerData.params` in `created()`.
3. Both pages `addNotify("the.shared.event")` and `postNotify` to keep their local observables in sync.
4. Both pages `removeNotify` in `pageWillDestroy`.

The "global observable" hack does not work cross-page in dynamic mode (each page is an isolated JS context). Use the bus.

---

## 16. Caching: MemoryCacheModule and SharedPreferencesModule

### 16.1 MemoryCacheModule — page-scoped in-memory KV + image cache

```kotlin
val cache = acquireModule<MemoryCacheModule>(MemoryCacheModule.MODULE_NAME)
cache.setObject("user", userBean)
val u = cache.getObject<UserBean>("user")
```

**Scope**: per-Pager. The cache is created with the page and dies with it. Use this for between-component state inside one page (e.g. data fetched in the parent, consumed by a deep child), not for cross-page state.

**Image caching**:
```kotlin
val status = cache.cacheImage(
    src = ImageUri.pageAssets("avatar.png").toString(),
    sync = true                       // local / base64 supports sync; network is async
)
// status.state, status.errorCode, status.errorMsg, status.cacheKey

cache.cacheImage(src = url, sync = false) { status -> /* async callback */ }
```

The returned `cacheKey` is what `Canvas.drawImage(...)` / `PAG.replaceLayerContents(imageFilePath = key)` accept.

### 16.2 SharedPreferencesModule — small persistent KV

```kotlin
val sp = acquireModule<SharedPreferencesModule>(SharedPreferencesModule.MODULE_NAME)
sp.setString("token", "abc")
sp.setInt("rev", 7)
sp.setFloat("opacity", 0.8f)
sp.setObject("user", userJson)              // JSONObject only

val token: String = sp.getString("token")        // "" if missing
val rev:   Int?   = sp.getInt("rev")             // nullable
val op:    Float? = sp.getFloat("opacity")
val user:  JSONObject? = sp.getObject("user")
```

Use for **small** persisted values (flags, user prefs, last-seen IDs). It's iOS `NSUserDefaults` / Android `SharedPreferences` / similar on other platforms — not a database. Don't store lists or large blobs here.

---

## 17. Other built-in modules (Codec, Calendar, Snapshot, Performance)

### 17.1 CodecModule

```kotlin
val codec = acquireModule<CodecModule>(CodecModule.MODULE_NAME)
codec.urlEncode("hello world")
codec.urlDecode("hello%20world")
codec.base64Encode("hi")
codec.base64Decode("aGk=")
codec.md5("data")             // 32-char hex
codec.sha256("data")          // 64-char hex
```

Same interface on every platform; uses each platform's native crypto/encoding.

### 17.2 CalendarModule

```kotlin
val cal = acquireModule<CalendarModule>(CalendarModule.MODULE_NAME)
cal.formatTime(System.currentTimeMillis(), "yyyy-MM-dd HH:mm:ss.SSS")
cal.parseFormattedTime("2025-01-01 00:00:00", "yyyy-MM-dd HH:mm:ss")   // → Long ms

val c = cal.newCalendarInstance(0L)                       // 0 = now
c.set(ICalendar.Field.YEAR, 2025)
c.add(ICalendar.Field.DAY_OF_MONTH, 7)
val ts = c.timeInMillis
val year = c.get(ICalendar.Field.YEAR)
```

`ICalendar.Field` covers YEAR / MONTH (0-indexed) / DAY_OF_MONTH / HOUR_OF_DAY / MINUTE / SECOND / MILLISECOND.

### 17.3 SnapshotModule (iOS only)

```kotlin
acquireModule<SnapshotModule>(SnapshotModule.MODULE_NAME)
    .snapshotPager("$appVer.$pageName.${if (darkMode) "dark" else "light"}")
```

iOS dynamic-mode pages (loaded from a JS bundle) have a perceivable startup cost. Snapshotting captures the current page state as a bitmap keyed by the string you supply; the next time the same page opens with the same key, the bitmap is shown immediately while the real Kuikly content loads underneath. **No-op on other platforms**, and not needed in framework (built-in) mode.

The key string is *yours* to design. The convention `appVersion + pageName + theme` invalidates the cached image when any of those change.

### 17.4 PerformanceModule

```kotlin
PagerManager.getCurrentPager()
    .acquireModule<PerformanceModule>(PerformanceModule.MODULE_NAME)
    .getPerformanceData { data ->
        // KRPerformanceData: pageName, mode, pageExistTime, coldLaunch,
        // launch timings (firstFramePaintCost, pageBuildCost, pageLayoutCost, ...),
        // FPS, memory increment
    }
```

Native side must enable the monitors first (`KRMonitorType.LAUNCH / FRAME / MEMORY` on Android, `KRMonitorType_*` flags on iOS). The page side then reads back whatever was enabled.

Use for in-app perf telemetry; not all metrics are available on every platform (H5 and Mini Programs lack FPS/memory).

---

## 18. Threading and coroutines

Kuikly's threading model is the single largest source of confusion. Internalising the three-tier model below removes the rest:

### 18.1 The three tiers of async

| Tier | Mechanism | Runs on | Dynamic mode? | Use when |
|---|---|---|---|---|
| 1 | **Module callbacks** (async / sync) | Native side schedules — usually main thread (async) or Kuikly thread (sync) | ✅ | Most cases — your work is delegated to native code anyway. |
| 2 | **Kuikly built-in coroutines** — `GlobalScope.launch`, `Pager.lifecycleScope.launch`, `pagerScope.async` | Kuikly thread, never switches | ✅ | You want suspend-fn ergonomics but don't actually need a thread switch (i.e. you're awaiting callbacks that already do their work elsewhere). |
| 3 | **`kotlinx.coroutines` + `Dispatchers.Kuikly`** | Real multi-threading via `Dispatchers.Default / IO`, then back via `Dispatchers.Kuikly[ctx]` | ❌ | You truly need CPU work off-thread (heavy parse, encryption) and aren't targeting dynamic mode. |

### 18.2 The Kuikly thread rule

UI APIs (`View {}`, `attr`, `event`, `observable`, `setTimeout`, `animate`) **are not thread-safe** and may only be touched from the Kuikly thread. If you're not sure what thread you're on, you're probably on it (because that's where `body()`, `created()`, all event handlers, and `setTimeout` run). When you cross out (via `Dispatchers.IO`, a callback from a custom Module on the main thread, etc.), you must come back before writing to observables.

Coming back:

```kotlin
KuiklyContextScheduler.runOnKuiklyThread(pagerId) { cancelled ->
    if (cancelled) return@runOnKuiklyThread
    ctx.foo = bar
}
```

…or, in coroutines:

```kotlin
GlobalScope.launch(Dispatchers.Kuikly[ctx]) { ctx.foo = bar }
```

### 18.3 `lifecycleScope` and `async` (in-house)

`Pager.lifecycleScope` cancels automatically when the page is destroyed. This codebase exposes a convenience `async { }` on Pager / ComposeView (basic_reference.md §"State Management and ViewModels") that does the same. Prefer it over `GlobalScope.launch` — using `GlobalScope` makes you responsible for cancellation, and forgetting that leaks across page navigations.

### 18.4 Built-in coroutine API summary

```kotlin
GlobalScope.launch { ... }                  // app-lifetime
lifecycleScope.launch { ... }               // page-lifetime, auto-cancelled
async { ... }                               // = lifecycleScope.launch — codebase convention
```

Inside a `suspend` function:
```kotlin
suspend fun loadConfig(): Config = suspendCoroutine { cont ->
    moduleX.fetchConfig { cont.resume(it) }
}
```

This is the canonical "callback → suspend" bridge.

---

## 19. Assets and images — under the hood

`basic_reference.md` covers WGImage assets briefly. The full picture:

### 19.1 Directory layout

```
shared/src/commonMain/assets/
├── common/                        ← shared across all pages
│   └── logo.png
├── home_page/                     ← matches @Page("home_page")
│   └── header.png
└── order_detail/
    └── icon.png
```

### 19.2 Packaging (one-time setup)

| Platform | Config |
|---|---|
| Android | `assets.srcDirs("src/commonMain/assets")` in `android { sourceSets { named("main") { ... } } }` |
| iOS (framework) | `extraSpecAttributes["resources"] = "['src/commonMain/assets/**']"` in the podspec |
| iOS (dynamic JS mode) | assets are bundled in the JS bundle automatically |
| HarmonyOS | Copy to `entry/src/main/resources/resfile/...` (no built-in packaging) |
| H5 | output to `build/dist/js/productionExecutable/assets/`; deploy to CDN |
| Mini Program | `./gradlew :miniApp:copyAssets` |

### 19.3 Loading

Through `ImageUri`:

```kotlin
src(ImageUri.commonAssets("logo.png"))             // common/logo.png
src(ImageUri.pageAssets("header.png"))             // <current pageName>/header.png
src(ImageUri.file(absoluteSandboxPath))            // local file
src("https://...")                                  // network
src("data:image/png;base64,...")                    // base64
```

These resolve to `assets://`, `file://`, `http(s)://`, `data:image` prefixes. The image adapter on each platform branches on the prefix to choose the loader — see `IKRImageAdapter` on Android, `KuiklyRenderViewControllerDelegatorDelegate.assetsPathUrl` on iOS.

### 19.4 Picking common vs page assets

- Shared icons, logos, decorative graphics → `common/`.
- Page-specific large images that only one page needs → that page's folder.

The dynamic-mode packaging only ships `common/` + `<thisPage>/` for a given page bundle, so page-scoping reduces per-page download size.

---

## 20. Extending Kuikly: custom Modules

Sometimes you need platform behaviour that Kuikly doesn't ship. The Module pattern: declare a typed API in Kotlin, implement it natively, register it.

### 20.1 The Kuikly side

```kotlin
class MyLogModule : Module() {
    override fun moduleName(): String = "KRMyLogModule"

    fun log(content: String) {
        toNative(
            keepCallbackAlive = false,
            methodName = "log",
            param = content,
            callback = null,
            syncCall = false
        )
    }

    fun logWithCallback(content: String, cb: CallbackFn) {
        toNative(false, "logWithCallback", content, cb, false)
    }

    fun syncLog(content: String): String {
        return toNative(false, "syncLog", content, null, true).toString()
    }
}
```

Parameters of `toNative`:
- `keepCallbackAlive: Boolean` — `false` for single-fire (default). `true` if the native side will call back multiple times (e.g. a sensor stream).
- `methodName: String` — what the native side dispatches on.
- `param` — supports primitives, primitive arrays, strings, and `JSONObject` (serialized to string). For binary, see §23.
- `callback: CallbackFn?` — invoked when native calls back with a JSONObject result. Null for fire-and-forget.
- `syncCall: Boolean` — `true` blocks the Kuikly thread (cheap because Kuikly thread is the only one in framework mode) and returns the native return value as `String`. Use sparingly — sync calls cannot be used for I/O.

Convenience helpers that build on `toNative`:
```kotlin
syncToNativeMethod(method, params: JSONObject, null): String
syncToNativeMethod(method, arrayOf(value), null): Any?
asyncToNativeMethod(method, params: JSONObject, callback)
asyncToNativeMethod(method, arrayOf(value), callback)
```

### 20.2 Registering on each platform

The native side implements a `KuiklyRenderBaseModule` (or per-platform equivalent) with a `call(method, params, callback)` switch:

```kotlin
// Android (Kotlin)
class KRMyLogModule : KuiklyRenderBaseModule() {
    override fun call(method: String, params: String?, callback: KuiklyRenderCallback?): Any? = when (method) {
        "log" -> { Log.d("MyLog", params ?: ""); null }
        "logWithCallback" -> { Log.d("MyLog", params ?: ""); callback?.invoke(mapOf("result" to 1)); null }
        "syncLog" -> { Log.d("MyLog", params ?: ""); "success" }
        else -> super.call(method, params, callback)
    }
}

// Then in Activity / delegate setup:
override fun registerExternalModule(kuiklyRenderExport: IKuiklyRenderExport) {
    super.registerExternalModule(kuiklyRenderExport)
    kuiklyRenderExport.moduleExport("KRMyLogModule") { KRMyLogModule() }
}
```

Names **must match** across Kotlin and native. The iOS side resolves the class by name at runtime via reflection — `KRMyLogModule` on Kuikly side maps to the iOS class `KRMyLogModule` literally.

### 20.3 Per-platform method-naming rules

- **Android / HarmonyOS / H5 / Mini Program**: route through `call(method, ...)` — any string works.
- **iOS**: each Kuikly method maps to a runtime-selectable Objective-C method *of the same name*. So `log` on Kuikly → `-(void)log:(NSDictionary *)args;` in `KRMyLogModule`. Sync methods return `id` instead of `void`. Args (including the callback) come in through a single `NSDictionary` with keys `HR_PARAM_KEY`, `KR_CALLBACK_KEY`.

### 20.4 Acquiring a custom module

If your module is added only on certain pages, register it in `Pager.createExternalModules()`:

```kotlin
override fun createExternalModules(): Map<String, Module>? = mapOf(
    "KRMyLogModule" to MyLogModule()
)
```

…then `acquireModule<MyLogModule>("KRMyLogModule")` to fetch it. If it's app-wide, register it on the host (Activity/VC) and skip the override.

---

## 21. Extending Kuikly: custom Views and view props

Two extension points:

### 21.1 Whole new view

```kotlin
class MyImageAttr : Attr() {
    fun src(s: String): MyImageAttr { "src" with s; return this }
}
class MyImageEvent : Event() {
    fun loadSuccess(h: (LoadSuccessParams) -> Unit) {
        register("loadSuccess") { h(LoadSuccessParams.decode(it)) }
    }
}
class MyImageView : DeclarativeBaseView<MyImageAttr, MyImageEvent>() {
    override fun createAttr() = MyImageAttr()
    override fun createEvent() = MyImageEvent()
    override fun viewName() = "HRImageView"      // ← name native side registers

    fun reload() {                                // method exposed to Kuikly side
        performTaskWhenRenderViewDidLoad {
            renderView?.callMethod("reload", "")
        }
    }
}
fun ViewContainer<*, *>.MyImage(init: MyImageView.() -> Unit) = addChild(MyImageView(), init)
```

Each platform then implements `HRImageView` natively (Android: `IKuiklyRenderViewExport`, iOS: `KuiklyRenderViewExportProtocol`, HarmonyOS: `KuiklyRenderBaseView`), routing `setProp("src", value)` and `call("reload", ...)` to the underlying widget. See `DevGuide/expand-native-ui.md` for the full per-platform code.

### 21.2 Adding one prop to an existing view

When you only need one new attribute (e.g. an in-house analytics tag), don't bother with a whole new view — extend `Attr` with the prop and register a `IKuiklyRenderViewPropExternalHandler` on each platform that intercepts that prop key:

```kotlin
// Kuikly side:
fun Attr.myProp(value: String) { "myProp" with value }

// Use:
View { attr { ... ; myProp("important") } }

// Android side, in your KuiklyRender setup:
override fun registerViewExternalPropHandler(kuiklyRenderExport: IKuiklyRenderExport) {
    super.registerViewExternalPropHandler(kuiklyRenderExport)
    kuiklyRenderExport.viewPropExternalHandlerExport(MyHandler())
}

class MyHandler : IKuiklyRenderViewPropExternalHandler {
    override fun setViewExternalProp(view, key, value): Boolean = when (key) {
        "myProp" -> { /* apply to view */ true }
        else -> false
    }
    override fun resetViewExternalProp(view, key): Boolean = ...
}
```

iOS resolves automatically via Objective-C runtime: declare `css_myProp` (note the `css_` prefix) on `UIView` and the framework will set it via the reflected setter.

---

## 22. Multi-module projects

When the app is split into several Kuikly KMP modules (`shared`, `shared_business1`, `shared_business2`, …) you must tell the KSP plugin so it doesn't create duplicate entry points:

```kotlin
// settings.gradle.kts
include(":shared", ":shared_biz1", ":shared_biz2")

// shared/build.gradle.kts (the "main" module)
dependencies { implementation(project(":shared_biz1")); implementation(project(":shared_biz2")) }
ksp {
    arg("moduleId", "shared")
    arg("isMainModule", "true")
    arg("subModules", "shared_biz1&shared_biz2")
    arg("enableMultiModule", "true")
}

// shared_biz1/build.gradle.kts (a sub-module)
ksp {
    arg("moduleId", "shared_biz1")
    arg("isMainModule", "false")
    arg("enableMultiModule", "true")
}
```

Sub-modules depend on the main module at compile time and cannot exist standalone.

---

## 23. Protobuf

Kuikly transports primitives, strings, JSON, and `ByteArray` across the bridge. For Protobuf:

1. Generate Kotlin data classes with **[Square Wire](https://square.github.io/wire/)**'s KMP build.
2. Add `com.squareup.wire:wire-runtime:$WIRE_VERSION` to your common dependencies.
3. Use `user.encode()` / `User.ADAPTER.decode(bytes)`.
4. Ship the bytes through a Module method whose parameter type is `ByteArray`:

```kotlin
fun sendProtobuf(data: ByteArray, cb: ((ByteArray) -> Unit)?) {
    asyncToNativeMethod("sendPb", arrayOf(data)) {
        cb?.invoke(it as? ByteArray ?: byteArrayOf())
    }
}
```

The native side accepts the `ByteArray` as a primitive and forwards it to whatever endpoint or decoder it has.

Why use this over JSON? Smaller payloads and faster decode for performance-sensitive flows (real-time feeds, telemetry).

---

## 24. Components reference (deep)

This section consolidates everything the API docs say about each built-in component into a single page, focused on attributes/events/methods that aren't obvious from the name. For component-specific examples, follow the GitHub demo links in each API doc.

> **Convention used throughout**: every component supports all *basic* style and layout attributes (background, border, radius, opacity, transform, margin, padding, size, flex, position, …) and all *basic* events (click, longPress, pan, lifecycle, appearPercentage, layoutFrameDidChange, animationCompletion). Only component-specific additions are listed below.

### 24.1 View — `FrameLayout` / `UIView`

| Extra | Description |
|---|---|
| `backgroundImage(src: String, imageAttr: ImageAttr? = null)` | Background image, default `resizeCover`. Same `src` formats as `Image`. |
| Method `bringToFront()` | Move to top of parent z-order. |
| Touch events `touchDown/touchMove/touchUp/touchCancel(TouchParams)` | Raw touches; supports multi-touch via `touches: List<Touch>`. `pointerId` and `action` (≥ 1.1.86) disambiguate. |

### 24.2 Text

`attr` methods (every one is a builder returning the same `TextAttr`, so they chain):

- Content: `text(s)`, `lines(n)` (max lines with ellipsis), `lineBreakMargin(f)` (reserve space on the last line for a "more" affordance).
- Sizing/spacing: `fontSize(f)`, `lineHeight(f)`, `lineSpacing(f)`, `letterSpacing(f)`, `firstLineHeadIndent(f)`.
- Weight: `fontWeight400() / 500() / 600() / 700()`. Aliases: `fontWeightNormal/Medium/Semisolid/Bold`.
- Style: `fontFamily(name)` (requires native font adapter for custom fonts), `fontStyleItalic()`.
- Color: `color(Color)` or `color(0xFFRRGGBBL)`.
- Alignment: `textAlignLeft/Center/Right()`.
- Decoration: `textDecorationUnderLine()`, `textDecorationLineThrough()`, `textShadow(offsetX, offsetY, radius, color)`.
- Overflow: `textOverFlowTail()` (default, "…" at end), `textOverFlowMiddle()` (Android impl pending), `textOverFlowClip()` (Android impl pending).

Events: `onLineBreakMargin { }` fires when text reached the line-break-margin limit (useful to show a "more" link).

### 24.3 RichText — multi-span text

Inherits all `Text` attrs. Inside the body, declare spans:

```kotlin
RichText {
    Span { text("hello "); color(Color.RED); fontSize(16f) }
    ImageSpan { size(20f, 20f); src("data:image/png;base64,..."); borderRadius(4f) }
    PlaceholderSpan {
        placeholderSize(80f, 80f)
        spanFrameDidChanged { frame -> /* save frame to overlay a custom view */ }
    }
    Span { text(" world") }
}
```

`PlaceholderSpan` is the trick for embedding non-text UI inline with text — measure its rect, then absolutely position a real `View` over it.

### 24.4 Image

Sources via `src(...)`:
- URL (`https://`)
- Base64 (`data:image/...`)
- Asset (`ImageUri.commonAssets(name)` / `ImageUri.pageAssets(name)`) — from 1.1+.
- Local file (`ImageUri.file(absolutePath)`) — from 1.1+.

Layout-fit:
- `resizeCover()` — fill bounds, may crop. Default for `View.backgroundImage`.
- `resizeContain()` — fit inside bounds, may letterbox.
- `resizeStretch()` — distort to fill.

Effects:
- `blurRadius(f)` — Gaussian blur, ≤ 12.5f.
- `tintColor(c)` — replace non-transparent pixels with color (icon recoloring).
- `maskLinearGradient(direction, colorStops...)` — alpha mask via gradient (e.g. fade to bottom).
- `capInsets(top, left, bottom, right)` — 9-patch-style edges; only the middle stretches when `resizeStretch()` is used.

Placeholders: `placeholderSrc(s)` shown while loading.

Events:
- `loadSuccess { (src) }`
- `loadFailure { (src, errorCode) }`  (`errorCode` since 1.1.86)
- `loadResolution { (width, height) }` — raw pixel dimensions.

`isDotNineImage` (in `src(src, isDotNineImage = true)`) — marks the image as a `.9.png` for nine-patch rendering (Mini Program impl pending).

### 24.5 Input — single-line text field

Inherits all relevant `Text` attrs (`color`, `fontSize`, `text`, `textAlignLeft/Center/Right`, etc.).

Input-specific:
- `placeholder(s)`, `placeholderColor(c)`, `tintColor(c)` (caret colour).
- `maxTextLength(n)`.
- `autofocus(b)` — pops the keyboard on appear.
- `editable(b)` — read-only when false.
- `keyboardTypePassword() / keyboardTypeNumber() / keyboardTypeEmail()`.
- `returnKeyTypeDone() / Send() / Search() / Next() / Go() / Continue() <iOS> / Google() <iOS>`.
- `inputSpans(InputSpans)` — make the field render with multiple text styles (rich-text inputs). Update on `textDidChange`.

Events:
- `textDidChange { (text) }` — text changed.
- `inputFocus { (text) }` / `inputBlur { (text) }`.
- `keyboardHeightChange { (height, duration) }`.
- `inputReturn { (text) }` — return key pressed (no-op on TextArea since Return is a newline there).
- `textLengthBeyondLimit { (text) }` — user tried to exceed `maxTextLength`.

Methods (via `ViewRef<InputView>`):
- `setText(s)`, `focus()`, `blur()`.
- `cursorIndex { i -> }` (async), `setCursorIndex(i)`.

### 24.6 TextArea — multi-line input

Everything from `Input` minus `inputReturn`. In TextArea, Return inserts a newline; observe `textDidChange` to react.

### 24.7 List — vertical/horizontal list

Inherits all `Scroller` attrs. Adds:
- `firstContentLoadMaxIndex(n)` — only build the first N items at first paint, defer the rest. Optimizes first-frame cost on long lists.
- `visibleAreaIgnoreTopMargin(f) / visibleAreaIgnoreBottomMargin(f)` — distance from the edge that doesn't count as visible when computing item visibility (use when a navbar or footer overlaps the list).
- `preloadViewDistance(f)` — how far past the visible window to keep platform widgets alive (default: one screen).

Events identical to `Scroller`: `scroll`, `scrollEnd`, `dragBegin`, `dragEnd`, `contentSizeChanged`.

Methods (via `ViewRef<ListView<*,*>>`):
- `setContentOffset(x, y, animated = false, springAnimation = null)`.
- `setContentInset(top, left, bottom, right, animated = false)`.
- `contentInsetWhenEndDrag(top, left, bottom, right)` — where the list settles after over-scroll.

### 24.8 Scroller — generic scroll container

Same attrs as `List` minus the list-virtualisation-specific ones (`firstContentLoadMaxIndex`, `visibleAreaIgnore*`, `preloadViewDistance`). Adds:
- `pagingEnable(b)` — snap to viewport multiples.
- `nestedScroll(forward, backward)` — control how scroll events propagate between parent and child scrollers. `SELF_ONLY` / `SELF_FIRST` / `PARENT_FIRST`.

### 24.9 PageList — viewport-sized pager

Items are forced to `pageItemWidth`/`pageItemHeight` (defaults = container size), and scrolling snaps to one page per swipe.

- `pageItemWidth(f)`, `pageItemHeight(f)`.
- `pageDirection(isHorizontal: Boolean)`.
- `defaultPageIndex(i)` — initial index.
- `keepItemAlive(b)` — keep off-screen pages instantiated.
- `offscreenPageLimit(n)` — when `keepItemAlive=false`, how many adjacent pages to keep alive (default 2).

Events: + `pageIndexDidChanged { (index) }`.

### 24.10 SliderPage — carousel

- `pageItemWidth(f)`, `pageItemHeight(f)`.
- `isHorizontal(b)`, `defaultPageIndex(i)`.
- `itemCount(n)`.
- `loopPlayIntervalTimeMs(ms)` — 0 = no auto-play.
- `initSliderItems(dataList, creator)` — declarative data source.

Methods: `startLoopPlayIfNeed()`, `stopLoopPlayIfNeed()`, `autoLoopPlay()`.

Events: `pageIndexDidChanged { (param: JSONObject) }` — read `param.optInt("index")`.

### 24.11 WaterFallList — masonry / Pinterest-style

Inherits `List`. Adds:
- `listWidth(f)` (required).
- `columnCount(n)` (default 1).
- `itemSpacing(f)` / `lineSpacing(f)` (default 0).
- `contentPadding(f)` — inside the container.

### 24.12 Tabs (with PageList)

Used as the indicator strip for a swipeable `PageList`. Required wiring:
- `scrollParams(scrollParams)` — feed it the `ScrollParams` from the `PageList.scroll` event so the indicator follows the swipe.
- `defaultInitIndex(i)`.
- `indicatorInTabItem { /* indicator view builder */ }`.
- `indicatorAlignCenter()` / `indicatorAlignAspectRatio()` (default).

Events: same family as `Scroller` (`scroll`, `scrollEnd`, `dragBegin`, `dragEnd`).

### 24.13 Refresh — pull-to-refresh header

Only valid inside a `List`/`Scroller`.
- `refreshEnable(b)`.

Events:
- `refreshStateDidChange { RefreshViewState -> }` — `IDLE / PULLING / REFRESHING`.
- `pullingPercentageChanged { (percentage01) }`.

Methods (via ref):
- `beginRefresh(animated = true)`.
- `endRefresh(animated = true)`.
- `contentInsetWhenEndDrag(f)`.
- `refreshState(state)`.

### 24.14 FooterRefresh — load-more footer

- `preloadDistance(f)` — pixels from the bottom to start triggering.
- `minContentSize(w, h)`.

Events:
- `refreshStateDidChange { FooterRefreshState -> }` — `IDLE / REFRESHING / NONE_MORE_DATA / FAILURE`.

Methods: `beginRefresh()`, `endRefresh(endState)`, `resetRefreshState(state)`, `refreshState(state)`.

### 24.15 Hover — sticky-in-scroll

Inside a scrollable container, a `Hover` view sticks to a position when scrolled.
- `bringIndex(i)` — stacking order when multiple hovers overlap.
- `hoverMarginTop(f)` — extra offset from container top.

### 24.16 Modal — full-screen overlay

A floating window covering the page (or whole window if `inWindow(true)`). No special attributes beyond basics.

### 24.17 AlertDialog

- `showAlert(b)` — controls visibility (required).
- `title(s)`, `message(s)`.
- `actionButtons("取消", "确定", ...)` — vararg button titles.
- `actionButtonsCustomAttr({...}, {...}, ...)` — per-button text styling (vararg `TextAttr.() -> Unit`).
- `customContentView { ... }` / `customBackgroundView { ... }` — replace the foreground / backdrop.
- `inWindow(b)` — top-level (default false, page-level).

Events: `clickActionButton { index -> }`, `clickBackgroundMask { (ClickParams) -> }`, `alertDidExit { }`, `willDismiss { }` (back gesture).

### 24.18 ActionSheet — iOS-style bottom sheet

Same shape as `AlertDialog`:
- `showActionSheet(b)`.
- `descriptionOfActions(s)`.
- `actionButtons("Cancel", "Action0", ...)` (first is cancel button).
- `actionButtonsCustomAttr(...)`.
- `customContentView { ... }` / `customBackgroundView { ... }`.
- `inWindow(b)`.

Same events as `AlertDialog`.

### 24.19 Switch

- `isOn(b)`, `onColor(c)`, `unOnColor(c)`, `thumbColor(c)`, `thumbMargin(f)`.
- Event: `switchOnChanged { (on) }`.

### 24.20 CheckBox

- `checked(b)`, `disable(b)`.
- Image variants: `defaultImageSrc(s)`, `checkedImageSrc(s)`, `disableImageSrc(s)`.
- View variants (advanced): `defaultViewCreator { ... }`, `checkedViewCreator { ... }`, `disableViewCreator { ... }`.
- Event: `checkedDidChanged { (checked) }`.

### 24.21 Slider — drag progress bar

- `currentProgress(f)` — 0..1.
- `progressColor(c)`, `trackColor(c)`, `thumbColor(c)`, `trackThickness(f)`, `thumbSize(Size)`.
- `sliderDirection(horizontal: Boolean)`.
- Custom views: `progressViewCreator { }`, `trackViewCreator { }`, `thumbViewCreator { }`.
- Events: `progressDidChanged { (progress) }`, `beginDragSlider { (PanGestureParams) }`, `endDragSlider { (PanGestureParams) }`.

### 24.22 ScrollPicker — wheel picker

Constructor takes `(items: Array<String>, defaultIndex: Int?)`.
- `itemWidth = f`, `itemHeight = f`, `countPerScreen = n`.
- `itemBackGroundColor`, `itemTextColor`.
- Event: `dragEndEvent { centerValue, centerItemIndex -> }`.

### 24.23 DatePicker

Built on `ScrollPicker`. Single event:
- `chooseEvent { (DatePickerDate) -> }` where `DatePickerDate.date.year/month/day` and `.timeInMillis`.

### 24.24 Canvas — H5-aligned 2D drawing

```kotlin
Canvas({
    attr { absolutePosition(0f, 0f, 0f, 0f) }
}) { ctx, width, height ->
    ctx.beginPath(); ctx.strokeStyle(Color.RED); ctx.lineWidth(2f)
    ctx.moveTo(0f, 0f); ctx.lineTo(width, height); ctx.stroke()
}
```

The render closure runs whenever the canvas needs a redraw. `CanvasContext` mirrors HTML5 Canvas:

- Paths: `beginPath()`, `moveTo(x,y)`, `lineTo(x,y)`, `arc(x, y, r, startRad, endRad, counterclockwise)`, `quadraticCurveTo(cpx, cpy, x, y)`, `bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)`, `closePath()`.
- Painting: `stroke()`, `fill()`, `strokeStyle(c)`, `fillStyle(c)`, `lineWidth(f)`, `setLineDash([on, off, ...])`, `lineCapRound()/Butt()/Square()`.
- Text: `fillText(s, x, y)`, `strokeText(s, x, y)`.
- Gradients: `createLinearGradient(x0, y0, x1, y1)` → `CanvasLinearGradient`; on it `addColorStop(stop01, color)`. Use the result as `fillStyle` / `strokeStyle`.
- `clip()` (Android/HarmonyOS impl pending) — clip to current path.

Bitmaps drawn via `drawImage` need the image cached first via `MemoryCacheModule.cacheImage` (see §16.1).

### 24.25 PAG — Tencent's vector animation format (Lottie-like)

- `src(s)` — URL or local path to `.pag` file.
- `repeatCount(n)` — `0` = infinite, default `1`.
- `autoPlay(b)` — default `true`.
- `replaceLayerContents(PAGReplaceItem...)` — replace text layers or image layers at runtime.
  - `PAGReplaceItem(type, layerName = "...", text = "...")` — type 0 = text.
  - `PAGReplaceItem(type, layerName = "...", imageFilePath = "..." / imageFileAsset = "..." / imageViewRef = "..." / imageFilePath = memoryCacheKey)` — type 1 = image (pick one source).

Events: `loadFailure`, `animationStart`, `animationEnd`, `animationCancel`, `animationRepeat`.
Methods: `play()`, `stop()`.

### 24.26 APNG

- `src(s)`, `repeatCount(n)` (0 = infinite, default 0), `autoPlay(b)`.
- Events: `loadFailure`, `animationStart`, `animationEnd`.
- iOS requires an `APNGImageViewProtocol` adapter (see `API/components/apng.md`).

### 24.27 Video

- `src(s)` (URL).
- `playControl(VideoPlayControl)` — `PLAY / PAUSE / STOP`.
- `resizeModeToCover/Contain/Stretch()`.
- `muted(b)`, `rate(1.0f|1.25f|1.5f|2.0f)`.

Events:
- `playStateDidChanged { (PlayState, extInfo: JSONObject) -> }`.
- `playTimeDidChanged { (curMs, totalMs) -> }`.
- `firstFrameDidDisplay { }` — hide your cover image here.

### 24.28 Blur

Frosted-glass overlay on whatever is *below* it in the stack.
- `blurRadius(f)` — max `12.5f`, default `10f`.

### 24.29 Mask

Two-arg constructor:

```kotlin
Mask(
    maskFromView = { Image { /* alpha source */ } },
    maskToView   = { Image { /* image to mask */ } }
)
```

The alpha channel of `maskFromView` is applied to `maskToView`. Useful for shaped image clipping, irregular cutouts, etc. HarmonyOS/H5/Mini Program impl pending.

### 24.30 ActivityIndicator

Spinner. Fixed 20×20 across platforms (iOS limitation); scale with `transform(Scale(...))`.
- `isGrayStyle(b)` — gray instead of white. Cannot be changed dynamically.

### 24.31 Button

Composite of an icon + text.
- `titleAttr { /* TextAttr block */ }` — text styling.
- `imageAttr { /* ImageAttr block */ }` — icon styling.
- `highlightBackgroundColor(c)` — pressed-state background.
- `flexDirection(enum)` — icon/text layout direction.

---

## 25. Performance guidelines

Compiled from `DevGuide/kuikly-perf-guidelines.md` plus the patterns this codebase has learned the hard way.

### 25.1 Bundle size

- Mark internal types/objects `internal`. KSP skips them, and the compiler can dead-code-eliminate more aggressively.
- Don't hardcode base64 image data in source — the string lives in your bundle uncompressed.

### 25.2 First-frame cost

- Load only first-screen data eagerly. Defer the rest to `pageDidAppear` or to a subsequent `setTimeout(0)` tick.
- Load only first-screen images synchronously (the rest can fade in).
- Use `List.firstContentLoadMaxIndex(n)` to build only the first N rows on first paint.

### 25.3 Observable hygiene

- Don't put unrelated state into the same observable — every read in the `body()` is a subscription, so a wide observable invalidates a lot.
- Don't add observables just for "future flexibility". A normal `val`/`var` is cheaper if you don't actually need reactivity.

### 25.4 Heavy native views

If a custom native view (video player, ML camera) is expensive to instantiate, pre-create and pool instances on the native side and hand them out through the Kuikly bridge instead of creating a fresh one per page.

### 25.5 Bridge cost

The async Module bridge has a small serialization + thread-hop cost. For hot paths:
- Switch to a **sync** Module call if you can — no serialization, runs on the Kuikly thread.
- If even sync is too slow, expose the same data through a **KMP `expect/actual` API** that bypasses the bridge entirely.

This matters only at very tight inner loops; for everything else, the bridge is fine.

---

## 26. Common pitfalls and idioms

A reference of the things that look obvious in hindsight but cost an hour the first time.

### 26.1 "My UI doesn't update"

- The expression that should update is **not** reading a reactive field (e.g. you used a local `val` computed once instead of `ctx.foo`).
- The reactive field's setter is being called from off-thread.
- The closure passed to `vif` / `vfor` doesn't capture a reactive read — `vfor({ list })` works, `vfor({ ctx.list })` works, but `vfor({ ctx.snapshot.list })` won't (the snapshot reference doesn't react).

### 26.2 "I get `PagerNotFoundException`"

You called `acquireModule` / `pagerData` / `getCurrentPager()` before `created()` ran — usually from a `val` initializer at class scope. Move the access into `created()` or wrap it in `by lazy`.

### 26.3 "My ComposeView's `body()` reads from `this` and won't compile"

Use `val ctx = this@MyView` outside the returned `{}`, then `ctx.foo` inside. The `body()` closure has a different receiver.

### 26.4 "My input is empty even though `attr.text` is set"

`Input.text(s)` only sets the *initial* value. To programmatically change later, call `inputRef.view?.setText(s)`. To track the typed value, listen to `textDidChange` and keep a local observable.

### 26.5 "My pan handler fires once then nothing"

You probably forgot to handle `state == "move"`. Pan emits `start → move (many) → end`.

### 26.6 "My animation jumps instead of animating"

The `animate(...)` call must appear **after** the property writes it should animate within the same `attr {}` block. The framework only animates writes above it (up to the previous `animate` or block start).

### 26.7 "My `vif` content keeps its state across hides"

It doesn't. `vif` unmounts. To preserve state on hide, use `visibility(false)` instead.

### 26.8 "My `companion object var by observable(0)` is deprecated"

Right — observables must live in a `PageScope`. Either move it to an instance field, or store a `ReadWriteProperty` in the `companion object` and initialize it inside `init`:

```kotlin
companion object { private var prop: ReadWriteProperty<Any, Int>? = null }
init { if (prop == null) prop = observable(0) }
private var counter by prop!!
```

Note: this only "works" within a single Pager scope — see §2.5 for the multi-page caveat.

### 26.9 "My `addNotify` callback fires even after the page closed"

Forgotten `removeNotify` in `pageWillDestroy`. The bus holds the callback alive, which holds the Pager alive.

### 26.10 "I want a global observable shared across pages"

You can't — see §2.5. Use `NotifyModule` plus a per-page observable that re-derives from the latest event.

### 26.11 "iOS Module method isn't being called"

The Objective-C class name must be **exactly** the string `moduleName()` returns. `KRMyLogModule` on Kotlin → `@interface KRMyLogModule : KRBaseModule`. No prefix, no module qualifier.

### 26.12 "Bridge serialization is slow for binary data"

JSONObject is text. Use a Module method with a `ByteArray` parameter (see §23) and pass raw bytes — no serialization.

### 26.13 "My text is cut off in a row"

If a `Text` is in a `flexDirectionRow()` parent without explicit width, it'll size to its full content. Combine with `flex(1f)` or set `width(...)` plus `lines(1) + textOverFlowTail()` to truncate.

### 26.14 "My absolute child changes the parent's size"

It shouldn't — absolute children are removed from the flex flow. If it does, double-check you actually called `positionAbsolute()` and that the value of `flexPositionType` got applied (you may be on an older version where the alias differs).

### 26.15 "iOS shows children outside the parent bounds; Android doesn't"

That's the `overflow` default mismatch (§6.1). Set `overflow(true)` on the parent to clip on both platforms, or accept the iOS default everywhere by relying on Kuikly's cross-platform default of `overflow = false`.

---

## Cross-references

- The framework-level concept docs are in [`DevGuide/`](./DevGuide/).
- The component API references are in [`API/components/`](./API/components/) and the module APIs in [`API/modules/`](./API/modules/).
- The in-house WG component library has its own docs in [`basic_components/`](./basic_components/index.md).
- The high-level network wrapper (`elegantNetWorkRequest`) is documented in [`basic_reference.md`](./basic_reference.md#network-requests--json-handling).

如果你在阅读时遇到中文版的开发者指南（`DevGuide/*.md` 多数为中文），请配合本英文 extended reference 一起看 —— 本文档同时也是对中文开发者指南的英文化总结。
