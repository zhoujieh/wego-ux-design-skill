# React + MobX → KuiklyUI Migration Guide

A working reference for porting `wsxc_*` React + MobX pages to KuiklyUI in `kuikly_shared/`. This guide is intentionally architecture-first: it tells you **where things go** in the Kuikly monorepo, **what each layer is responsible for**, and **which familiar React patterns dissolve vs. translate 1-to-1**. The framework API surface itself lives in [`basic_reference.md`](./basic_reference.md) and [`extended_reference.md`](./extended_reference.md) — refer to those for `attr {}` / `event {}` / DSL syntax once you have the shape.

Audience: someone who knows React 16 + MobX 4 at the level the `wsxc_*` codebases use (class with `@observable/@action/@computed/@inject/@observer`, FC with hooks, singleton-store-per-page, `wgoo.$http`, `hashHistory`, less / css-modules), and who is moving a page off `wsxc_portal` and into Kuikly.

The canonical reference port for this guide is the 好友 (Friends) page — `wsxc_portal/src/routes/followed/` → `kuikly_business_customer/.../features/friends/`. Where this guide says "see the friends port", read [`features/friends/README.md`](../kuikly_business_customer/src/commonMain/kotlin/com/truedian/wg/customer/features/friends/README.md).

---

## Table of contents

1. [Mental model](#1-mental-model)
2. [Project architecture](#2-project-architecture)
3. [Page shape](#3-page-shape)
4. [State: MobX → observables](#4-state-mobx--observables)
5. [View: JSX → ViewBuilder DSL](#5-view-jsx--viewbuilder-dsl)
6. [Lifecycle](#6-lifecycle)
7. [Network and data layer](#7-network-and-data-layer)
8. [Navigation](#8-navigation)
9. [Lists, refresh, sticky](#9-lists-refresh-sticky)
10. [UI primitives (forms, modals, animation, styling)](#10-ui-primitives)
11. [Native bridges (placeholder — see §11)](#11-native-bridges)
12. [Things that don't map](#12-things-that-dont-map)
13. [Migration recipe](#13-migration-recipe)
14. [Pitfalls](#14-pitfalls)

---

## 1. Mental model

React + MobX is closer to Kuikly than the syntactic difference suggests. Both build a tree by **declaring** UI, both use **fine-grained observables** so only what changed re-renders, both treat state and view as the only durable units. The cleanest one-liner: **MobX 4 with decorators + mobx-react `observer` ≈ KuiklyUI built in.**

What's genuinely different:

| Concept | React + MobX | KuiklyUI |
|---|---|---|
| Thread | Browser main thread, free access. | Dedicated **Kuikly thread** owns observables, layout, timers, animation. Touching state from another thread is a bug. |
| Re-render unit | `observer` walks the whole component on every observable read. | Each `attr {}` / `event {}` / `vif {}` / `renderList {}` **closure** subscribes only to the observables it actually read — finer than React. |
| `render()` vs `body()` | `render()` runs on every change. | `body(): ViewBuilder` runs **once** at mount. The closures inside it re-run reactively. Putting logic at `body()`'s top level is a footgun. |
| `@action` / `enforceActions` | Mandatory wrap; `runInAction` after `await`. | None. Be on the Kuikly thread; the framework batches per frame automatically. |
| The DOM | HTML + CSS. | A tree of `DeclarativeBaseView`s mapped to native widgets per platform. No DOM, no CSS, no `querySelector`. |
| Styling | LESS / css-modules, class-based, build-time. | Inline `attr { backgroundColor(…); padding(…); }`. No selectors, no cascade. |
| Layout | Browser's flex / grid / block. | **FlexBox only**, defaults differ — `flexDirection` is **column**, `alignItems` stretches, `overflow` does **not** clip ([extended_reference §6.1](./extended_reference.md#61-defaults-that-bite)). |
| Routing | `react-router` v3 + `hashHistory`. | `wg.toKuiklyPage(name, params)` / `closePage()`. No URL bar. |
| Code splitting | `React.lazy(() => import(...))`. | Pages register via `@Page("name")`. Dynamic mode (per-page JS bundles) is a separate opt-in. |
| Provider / inject | `<Provider>` + `@inject`. | None. Either a singleton object, or pass through a `ComposeAttr`. |
| Portals | `ReactDOM.createPortal`. | `Modal { inWindow(true) }` or a `BaseVisuals` helper. |
| i18n | `react-intl` + `IntlProvider`. | No built-in; the project provides a `wgRes`/`wgRaw` string-table keyed by a global locale. |
| Imperative DOM | `ref.current.scrollIntoView()`. | `ViewRef<XxxView>` + `ref?.view?.method(...)`. |
| Animation | CSS transitions / Lottie. | Declarative `animate(Animation.linear(0.3f), trigger)` or `view.animateToAttr(...)`. **No Lottie player — re-encode as PAG.** |

Everything below is an elaboration of this table.

> **Important framing.** Migration is rarely line-by-line. A 1600-line `friends.js` with twenty `_renderXxx` methods is not migrated by translating each method — it's migrated by recognising the *shapes* it expresses (a header-list page with two sort modes, search, pull-to-refresh, swipe-to-delete, a side rail) and rebuilding from those shapes inside the architecture in §2.

---

## 2. Project architecture

`kuikly_shared/` is a Kotlin Multiplatform (KMP) monorepo built on Tencent's KuiklyUI (`com.tencent.kuikly-open`). One root aggregator + six sub-modules, each a git submodule:

```
kuikly_shared                       (root aggregator, namespace com.truedian.wg.shared)
 ├── kuikly_init                    glue — declares every business + core, hand-written KuiklyCoreEntry_init
 ├── kuikly_core                    foundation: components/router/servicebus/utils  [moduleId "wgcore"]
 ├── kuikly_business_album   ─┐     相册云                                          [moduleId "wgalbum"]
 ├── kuikly_business_bcg     ─┼─→ kuikly_business_common ──api──→ kuikly_core
 ├── kuikly_business_customer─┘     客户云 — owns the friends page                   [moduleId "wgcustomer"]
 └── kuikly_business_common         shared UI/services + cross-cutting bridges       [moduleId "wgcommon"]
```

Authoritative spec is the root [`AGENTS.md`](../AGENTS.md). Read it once before adding anything new.

### 2.1 Four per-platform build entry points

In the **repo root**, not in any module:

| Build file | Targets | Project paths it references |
|---|---|---|
| [`build.android.gradle.kts`](../build.android.gradle.kts) | `androidTarget()` + KSP | `:kuikly_shared:*` |
| [`build.ios.gradle.kts`](../build.ios.gradle.kts) | `iosX64/iosArm64/iosSimulatorArm64` + cocoapods | `:shared:*` (note: not `:kuikly_shared:*`) |
| [`build.h5.gradle.kts`](../build.h5.gradle.kts) | `js(IR)` | `:kuikly_shared:*`; pre-copies sub-module assets, deletes them post-build |
| [`build.ohos.gradle.kts`](../build.ohos.gradle.kts) | `ohosArm64` | `:kuikly_shared:*` |

**Critical**: the KSP `subModules` arg (currently `"init&wgcore&wgalbum&wgcustomer&wgbcg&wgcommon"`) must stay in sync across all four files. A mismatch produces `Unresolved reference 'KuiklyCoreEntry_<id>'` errors in the generated aggregator.

### 2.2 Per-module shape

Every business module follows the same internal layout. Customer is the example:

```
kuikly_business_customer/
└── src/
    ├── commonMain/
    │   ├── kotlin/com/truedian/wg/customer/
    │   │   ├── features/<page_name>/          ← @Page implementations
    │   │   │   ├── README.md                  ← page-level architecture doc (mandatory for non-trivial ports)
    │   │   │   ├── page/<X>Page.kt            ← @Page entry — thin: NavBar + body() + lifecycle
    │   │   │   ├── viewModel/<X>ViewModel.kt  ← all observable state + suspend fetch fns
    │   │   │   ├── bean/<X>Beans.kt           ← @Serializable response/request models
    │   │   │   ├── network/<X>ApiPaths.kt     ← REST URL constants
    │   │   │   ├── helper/                    ← pure functions, decoders, bridge wrappers, router util
    │   │   │   └── components/                ← ComposeView<Attr,Event> per visual block
    │   │   ├── demos/                         ← internal test pages
    │   │   ├── components/                    ← cross-page domain UI
    │   │   ├── domain/                        ← business logic
    │   │   ├── openapi/                       ← cross-domain API surface (pages/data/UI capabilities exposed to other businesses)
    │   │   └── router/                        ← XxxRouteRegistry, app/h5/miniprogram/offline route configs
    │   └── assets/<page_name>/                ← page-scoped static assets (images, PAG, fonts)
    ├── androidMain/ iosMain/ jsMain/ ohosArm64Main/   ← platform-specific `actual`s only; per-feature code lives in commonMain
    └── build.gradle.kts
```

The friends port populates this template literally — `features/friends/` with `page/`, `viewModel/`, `bean/`, `network/`, `helper/`, `components/`. Mirror it.

### 2.3 Where to put new code — the decision tree

- **A page on its own**: `features/<page_name>/` in the owning business module. Register with `@Page("<page_name>")` and add the name to that module's `PageConfig` + `<Module>ExposedPages` (the latter only if cross-domain navigation needs it).
- **A view block reused only inside one page**: `features/<page_name>/components/<X>View.kt`.
- **A view block reused across pages within the same business**: `<module>/components/` (top-level of the module).
- **A view block reused across businesses**: `kuikly_business_common/components/`.
- **A business helper for this page only**: `features/<page_name>/helper/`.
- **A shared business service (e.g. `IosCompliance`)**: `kuikly_business_common/service/`.
- **Cross-domain navigation glue**: `<module>/openapi/page/` exposes the page; the caller uses `wg.navigateToPage(pageName, fromModuleName, toModuleName, params)`.
- **A new business module**: register it in all four root `build.<platform>.gradle.kts` `subModules` args, add it to `kuikly_init`'s dependencies, give it a `moduleId`, follow the per-module shape above.

### 2.4 Hosting model (no React Native bridge)

A Kuikly page is hosted by a thin platform shell — one per platform. The shell instantiates a Kuikly render-view delegator, calls `openPage(name, moduleName, pageData)`, forwards lifecycle, and shuttles events both ways. Mappings:

| Platform | Shell type | How it loads bytecode | Module-name → bundle |
|---|---|---|---|
| Android | `Fragment` (`KuiklyFocusFragment` for friends) | DEX per `moduleId`, swapped at runtime | one bundle per business module |
| iOS | `UIViewController` (subclassing/wrapping `WGKuiklyRenderViewController`) | single `shared.framework` from `:shared:syncFramework` | all modules in one framework; `fetchContextCodeWithPageName:` always returns `@"shared"` |
| HarmonyOS | `ets` component (`KuiklyComponent`/`KuiklyContainer`); the **tabbar itself is a Kuikly page** (`app_main_tabs_page`) launched by `pages/KuiklyRootPage` | per-module HAR (`core-ohosarm64`) | one HAR per business module; a tab embeds another module's page via a cross-domain UI `ViewBuilder` (§11.11), not a separate shell |
| H5 | `<div>` host in an HTML page (kuikly_h5 / kuikly_h5_bcg) | one `nativevue.js` produced by Kotlin/JS IR | one JS bundle per host app, page resolved by `?page_name=` |
| Mini Program | (not in scope for friends) | — | — |

The shell is where the host platform's navigation, lifecycle, and bridge dispatchers live. The contract between shell and page is laid out in §11.

---

## 3. Page shape

In Kuikly you write **one shape**: `Pager` for top-level pages, `ComposeView<Attr, Event>` for reusable views. There is no class-vs-FC distinction.

### 3.1 Page-level class component → Pager

```jsx
// wsxc_portal/src/routes/<page>/index.js (or friends.js — same shape)
@observer
class Friends extends React.Component {
    state = { showError: false };
    async componentDidMount() {
        await this.props.vm.fetchInit();
    }
    componentWillUnmount() {
        document.removeEventListener('click', this.onDocClick);
    }
    render() {
        if (this.state.showError) return <ErrorPage />;
        return (
            <div className={styles.root}>
                <Header />
                {this.props.vm.showCart && <CartBar />}
                <List items={this.props.vm.items} />
            </div>
        );
    }
}
```

```kotlin
// features/friends/page/FriendsPage.kt
@Page("album_friends_page")
internal class FriendsPage : BasePager() {

    private val vm by lazy { FriendsViewModel(this) }
    private var showError by observable(false)

    override fun created() {
        super.created()
        async { vm.fetchInit() }                // was componentDidMount
    }

    override fun pageWillDestroy() {
        super.pageWillDestroy()
        // cleanup; pair every addNotify with removeNotify
    }

    override fun body(): ViewBuilder {
        val ctx = this
        return {
            attr { flexDirectionColumn() }      // was className={styles.root}
            vif({ ctx.showError }) { ErrorPage { } }
            velse {
                Header { }
                vif({ ctx.vm.showCart }) { CartBar { } }
                ItemList { attr { items = ctx.vm.items } }
            }
        }
    }
}
```

Notes:
- `this.state` → `by observable(...)`. No `setState`.
- `@observer` + `@inject` decorators disappear. Reactivity is automatic; "injection" is a plain Kotlin reference.
- `render()`'s if-return becomes `vif / velse`. **`body()` runs once**; returning early from it is a bug.
- `componentDidMount` → `created()`; the `async { … }` wrapper lets you `await` suspending requests without a post-`await` re-thread.

### 3.2 Sub-component → ComposeView<Attr, Event>

```kotlin
internal class FriendItemAttr : ComposeAttr() {
    var friend by observable<Friend?>(null)
    var forceWhiteBg = false
}
internal class FriendItemEvent : ComposeEvent() {
    fun onTap(h: (Friend) -> Unit) { this.tap = h }
    internal var tap: ((Friend) -> Unit)? = null
}
internal class FriendItemView : ComposeView<FriendItemAttr, FriendItemEvent>() {
    override fun createAttr() = FriendItemAttr()
    override fun createEvent() = FriendItemEvent()
    override fun body(): ViewBuilder { /* … */ }
}
internal fun ViewContainer<*, *>.FriendItem(init: FriendItemView.() -> Unit) =
    addChild(FriendItemView(), init)
```

Callsite:

```kotlin
FriendItem {
    attr { friend = ctx.vm.items[idx]; forceWhiteBg = (sectionTitle != STAR_KEY) }
    event { onTap { ctx.vm.handleTap(it) } }
}
```

Props are reactive: assigning `attr { friend = x }` re-runs the assignment closure when `x` changes; the child's `attr.friend` getter is reactive inside its own `attr {}` / `vif {}` / etc. closures.

---

## 4. State: MobX → observables

### 4.1 The translation

| MobX | Kuikly |
|---|---|
| `@observable foo = 0` | `var foo by observable(0)` |
| `@observable.shallow arr = []` | `var arr by observableList<T>()` |
| `@observable.shallow map = new Map()` | `var map by observableMap<K, V>()` |
| `@observable.deep obj = { … }` | wrap each field individually; deep observation is not free |
| `@computed get y() { … }` | `val y: T get() = …` (a plain Kotlin getter — reactive when it reads other observables) |
| `@action setX = (n) => { this.x = n }` | regular function; no decorator |
| `runInAction(() => { … })` | direct assignment; just be on the Kuikly thread |
| `@observer class …` / `observer(FC)` | not needed |
| `@inject('store')` | plain Kotlin import / constructor injection |
| `<Provider store={s}>` | none; pass via `attr` or hold a singleton |
| `useLocalStore(() => ({...}))` | declare observables on the ComposeView |
| `useEffect(fn, [dep])` | `bindValueChange({ dep }) { fn() }` inside `created()` |
| `mobx.reaction(() => x, fn)` | same — `bindValueChange` |

### 4.2 ViewModel scope

Every observable belongs to a scope. Top-level `var x by observable(0)` declared at file scope is **inert** (it never notifies). Bind to a Pager / ComposeView / `(scope: PagerScope)` constructor argument:

```kotlin
internal class FriendsViewModel(private val scope: PagerScope) {
    var sortType by scope.observable(SortType.TAG)
    var totalCount by scope.observable(0)
    var tagGroupList by scope.observableList<Friend>()
    val isLetterView: Boolean get() = sortType == SortType.LETTER

    suspend fun fetchInit() {
        loading = true
        try {
            val resp = getRequest(FriendsApiPaths.LIST).urlParams(...).send<FriendsResp>()
            totalCount = resp.totalCount
            tagGroupList = resp.list.toObservableList()
        } finally { loading = false }
    }
}
```

The ViewModel is **per-page**: instantiate in the Pager, not as a singleton, unless you genuinely want cross-page shared state (rare). The friends port uses one ViewModel held by `FriendsPage`.

> **PageScope gotcha.** An observable bound to one Pager only drives UI on that Pager. Cross-page sync requires `NotifyModule` or a re-read on the receiving side ([extended_reference §10.4](./extended_reference.md)).

---

## 5. View: JSX → ViewBuilder DSL

### 5.1 Element table

| JSX | Kuikly DSL |
|---|---|
| `<div>` / `<span>` / generic block | `View { }` |
| `<p>` / `<h1>` / text node | `Text { attr { text("…") } }` |
| `<img src={url} />` | `Image { attr { src(url) } }` (or house's `WGImage`) |
| `<input value={v} onChange>` | `Input { attr { text(v) }; event { textDidChange { v = it.text } } }` |
| `<button onClick>` | `Button { … }` (or `WGButton`) |
| `<ScrollView>` | `Scroller { … }` |
| `<FlatList>` / virtualized | `List { renderList(...) { … } }` (must be **direct** parent for `isLazy = true`) |
| `<Modal>` | `Modal { attr { inWindow(true) } }` |
| `{cond && <X/>}` | `vif({ ctx.cond }) { X { } }` |
| `cond ? <A/> : <B/>` | `vif(...) { A { } }; velse { B { } }` |
| `arr.map(item => <X key={...} />)` | `renderList({ ctx.arr }) { item, i, _ -> X { attr { … } } }` |
| `<>…</>` (fragment) | no fragment node; just emit siblings inside the parent |
| `className={styles.foo}` | inline `attr { backgroundColor(...); padding(...); … }` |
| `style={{ width: 100 }}` | inline `attr { width(100f); … }` |

### 5.2 Syntactic translation

```jsx
<div className={cn(styles.root, { [styles.active]: isActive })} onClick={onTap}>
    <span>{title}</span>
    {showIcon && <Icon name="check" />}
</div>
```

```kotlin
View {
    attr {
        flexDirectionRow()                       // be explicit — Kuikly default is column
        backgroundColor(if (ctx.isActive) Color.BLUE else Color.WHITE)
        padding(8f)
    }
    event { click { ctx.onTap() } }
    Text { attr { text(ctx.title) } }
    vif({ ctx.showIcon }) { Icon { attr { name = "check" } } }
}
```

The `attr {}` / `event {}` / `vif {}` lambdas are the **reactive units**. They re-run when an observable they read changes. The DSL outside them runs once.

### 5.3 Lazy lists — the receiver requirement

`renderList(... isLazy = true)` only works when the receiver is literally a `ListView<*,*>`. Putting a `renderList` inside a `vif {} / velse {}` (whose receiver is a `VirtualView`) silently degrades to eager `vforIndex` and you lose virtualization. The friends `TagGroupListView` works around this by giving each case its own `List` and passing the inner `ListView` as the body's receiver. See [`features/friends/components/TagGroupListView.kt`](../kuikly_business_customer/src/commonMain/kotlin/com/truedian/wg/customer/features/friends/components/TagGroupListView.kt) for the canonical `shellList(body: ListView<*,*>.() -> Unit)` pattern.

---

## 6. Lifecycle

| React | Kuikly |
|---|---|
| `constructor` (sync init) | property initializers and `init {}` block |
| `componentDidMount` | `Pager.created()` / `ComposeView.viewDidLoad()` |
| `componentWillUnmount` | `Pager.pageWillDestroy()` / `ComposeView.viewDidUnload()` |
| `componentDidUpdate(prev) { if (prev.x !== x) }` | rarely needed; otherwise `bindValueChange({ ctx.x }) { … }` |
| `useEffect(fn, [])` (mount-only) | `created()` body |
| `useEffect(fn, [a, b])` | `bindValueChange({ a to b }) { fn() }` |
| `useEffect(() => () => cleanup, [])` | pair with `pageWillDestroy` |
| (no analog — page came back to foreground) | `Pager.pageDidAppear()` |
| (no analog — page went away) | `Pager.pageDidDisappear()` |

**The `pageDidAppear` / `pageDidDisappear` window is important** — it replaces the web's `visibilitychange` and the H5 host's `window.activityResume`/`onAppPageHide`. The friends port uses `pageDidAppear` to flush pending unfollow events and refresh tab badges; see §11.

Layout-dependent work (e.g. measuring children) must wait for `viewDidLayout` (ComposeView) or a `layoutFrameDidChange` event (arbitrary children). `pagerData.pageViewWidth` is valid from `created()` onward, but child frames are not.

---

## 7. Network and data layer

Use the `elegantNetWorkRequest` wrapper, not raw `NetworkModule`:

```kotlin
// GET ?a=1&b=2
val resp = getRequest(ApiPaths.X)
    .urlParams("a" to 1, "b" to 2)
    .send<Resp>()                            // suspend

// POST form
val resp = postFormRequest(ApiPaths.Y)
    .formParams("name" to "x")
    .send<Resp>()

// POST JSON body
val resp = postRequest(ApiPaths.Z)
    .bodyJson(JSON.encodeToString(Req(...)))
    .send<Resp>()
```

Conventions:
- URL constants live in `<page>/network/<X>ApiPaths.kt`.
- Response shapes live in `<page>/bean/<X>Beans.kt` as `@Serializable` data classes — field names match the API. If you need camelCase locally, use `@SerialName("snake_field") val camelField`.
- Loading state is a regular observable on the ViewModel: `var loading by scope.observable(false)`. Track in a `try/finally` around the request.
- Cancellation uses standard kotlinx.coroutines — wrap calls in `async { … }` and cancel the job on `pageWillDestroy`.

Don't reach for `axios` interceptors. Cross-cutting concerns (auth headers, app version, etc.) are baked into the wrapper. Add per-request headers via `.header(k, v)`.

---

## 8. Navigation

### 8.1 Opening another Kuikly page

```kotlin
wg.toKuiklyPage(
    pageName = "personal_album_page",
    params = JSONObject().apply { put("shop_id", id) },
)
```

If the destination is in a different business module, use `wg.navigateToPage(pageName, currentModuleName, toModuleName, params)` and ensure the target is in that module's `<Module>ExposedPages.exposedPages` list (whitelist; the call is otherwise rejected).

### 8.2 Opening an H5 page

```kotlin
wg.toH5Page(routeId = H5RouterConfig.ROUTE_NEW_FANS, params = ...)
```

`routeId` must exist in the native shell's `simpleH5RouterMap`. For ad-hoc H5 routes not in the map, use `CommonRouterUtil.toH5CommonPage(pageHash = "/some_route")` which sets `h5RoutID = ROUTE_H5_COMMON` and lets the native side build the URL.

### 8.3 Reading params

```kotlin
val shopId = pageData.params.optString("shop_id")           // from openPage call
val fromQuery = pageData.params.optString("from")           // same shape
```

`pagerData` is available from `created()` onward. There is **no URL**; "deep link" = host passes initial params.

### 8.4 Returning data from a closed page

```kotlin
// In the page being closed:
acquireModule<NotifyModule>(NotifyModule.MODULE_NAME)
    .postNotify("friends.deleted", JSONObject().apply { put("shop_id", id) })
closePage()

// In the page that opened it (in created()):
acquireModule<NotifyModule>(NotifyModule.MODULE_NAME)
    .addNotify("friends.deleted") { data -> vm.removeShop(data.optString("shop_id")) }
```

Pair every `addNotify` with `removeNotify` in `pageWillDestroy`.

### 8.5 Project convention

All navigation off a page goes through a `<Page>RouterUtil` helper (one file in `<page>/helper/`). See [`features/friends/helper/FriendsRouterUtil.kt`](../kuikly_business_customer/src/commonMain/kotlin/com/truedian/wg/customer/features/friends/helper/FriendsRouterUtil.kt) — every user-visible tap goes through there, and any cross-domain or H5 route is captured as a typed `fun toXxx(...)`.

---

## 9. Lists, refresh, sticky

### 9.1 Plain list

```kotlin
List {
    attr { flex(1f); width(100.pct); }
    renderList({ ctx.vm.items }, isLazy = true) { item, i, _ ->
        ItemRow { attr { this.item = item } }
    }
}
```

### 9.2 Pull-to-refresh + load-more

```kotlin
List {
    attr { flex(1f) }
    Refresh {
        // header content while refreshing
        attr { allowRefresh(true) }
        event { refreshStateDidChange { state -> if (state == RefreshState.REFRESHING) ctx.handlePullRefresh(this) } }
        // ... PAG indicator inside
    }
    renderList({ ctx.vm.items }, isLazy = true) { item, _, _ -> ItemRow { … } }
    FooterRefresh {
        attr { footerRefreshState(ctx.footerState) }
        event { footerRefreshStateDidChange { state -> if (state == FooterRefreshState.REFRESHING) ctx.handleLoadMore(this) } }
    }
}
```

Convention from the friends port: keep `handlePullRefresh()` / `handleLoadMore()` `suspend` on the Page, let the component fire them via `ctx.async { … endRefresh() }`, and have `handleLoadMore` **return** a `FooterRefreshEndState` so the component picks the right end state.

### 9.3 Sticky headers (吸顶)

Wrap the header in `Hover { … }`. The `renderList`'s receiver must be a `ListView<*,*>` for the hover to register; if it's nested, fall back to a plain non-sticky `View`. The friends letter mode does both — see `LetterGroupListView.kt`'s `type==0` branch.

### 9.4 Side rail / fast scroll

For an A-Z anchor rail, see [`components/LetterAnchorRailView.kt`](../kuikly_business_customer/src/commonMain/kotlin/com/truedian/wg/customer/features/friends/components/LetterAnchorRailView.kt). Key choices: `pan` + tap gestures, `BubbleUtil.show` for the letter overlay, content-sensitive key on `bindValueChange` (don't key on `.size` — single-friend lists rename without changing count), and lazy-safe scroll via `ListView.scrollToPosition(globalIndex, 0f, animated)` walking `ListContentView.templateChildren()` so off-screen sections still target precisely.

### 9.5 Swipe-to-delete

See [`components/SwipeableRowView.kt`](../kuikly_business_customer/src/commonMain/kotlin/com/truedian/wg/customer/features/friends/components/SwipeableRowView.kt). Pan-driven, direction-locked with a 4dp deadzone, snap animation via `animate(Animation.easeOut(0.22f), isSnapping)`.

---

## 10. UI primitives

### 10.1 Styling

Inline `attr {}`. No selectors, no cascade, no class names. Reusable values live in a tiny `Theme` / `WGColor` / `WGFont` object next to the component. Conditional styling is a branched `attr` write:

```kotlin
attr {
    backgroundColor(if (ctx.isActive) WGColor.PRIMARY else WGColor.WHITE)
    if (ctx.isPCClient) padding(16f) else padding(12f)
}
```

Pseudo-classes (`:hover`, `:focus`) are not a Kuikly concept. On PC builds you can detect `AppConfig.isH5ForPC()` and synthesise hover from pointer events if needed.

### 10.2 Forms

`Input.text(initial)` only sets the **initial** value. Updates go via `ref?.view?.setText(s)`. The other direction (UI → state) works as expected through `event { textDidChange { ctx.foo = it.text } }`.

For multi-field forms, observables on the ViewModel + a `vif`-gated error state per field. No `Formik` analog.

### 10.3 Modals, toasts, dialogs

| React/H5 | Kuikly |
|---|---|
| `wgoo.$toast({ title, icon: 'error' })` | `BaseVisuals.showSimpleErrorToast(pagerId, title)` |
| `wgoo.$toast({ title })` | `BaseVisuals.showSimpleSuccessToast(pagerId, title)` |
| `wgoo.$modal({ title, content, onOk })` | `BaseVisuals.showTextDialog(pagerId, title, content, … )` |
| `wgoo.$actionsheet(items)` | `BaseVisuals.showActionSheet(pagerId, items)` |
| Bottom sheet (heavier content) | `BaseVisuals.showModalFrame(pagerId, builder)` |
| In-place `{showX && <X/>}` | keep it: `vif({ ctx.showX }) { X { … } }` |
| Popover / hint | `createPopover(...)` or `PopViewSelectController.showPopViewSelect(...)` |

Render-in-place is preferred for state-heavy overlays (forms, search panels); imperative `BaseVisuals` for fire-and-forget messages.

### 10.4 Refs

```kotlin
private var listRef: ViewRef<ListView<*,*>>? = null
// in body():
List {
    ref { listRef = it as ViewRef<ListView<*,*>> }
    // …
}
// call:
listRef?.view?.scrollToPosition(0, 0f, true)
```

### 10.5 Animation

Declarative:

```kotlin
attr {
    animate(Animation.linear(0.3f), ctx.isOpen)   // trigger value; animates when it changes
    opacity(if (ctx.isOpen) 1f else 0f)
}
```

Imperative one-shot:

```kotlin
viewRef.view?.animateToAttr(Animation.easeOut(0.22f)) {
    translationX(0f)
}
```

No Lottie. Re-encode as PAG (Tencent vector format) — wire the adapter (`KuiklyRenderAdapterManager.setKrPagViewAdapter`) on the native side once, then use `PAG { attr { src(...); repeatCount(0); autoPlay(true) } }`. For ring/loading PAGs the page already uses, see `loading_gray.pag`.

---

## 11. Native bridges

The bridge layer is the biggest delta between H5 (`window.appShare(N, data)` + `window.functionInJs(type, data)` over a `WKWebView` / Android WebView) and Kuikly (`wg.commonBridgeAsync(key, payload)` + `delegator.sendEvent(name, payload)` between a Kuikly pager and a host shell). It is also the most platform-shaped part of a port — the section below is what we learned from porting the 好友 page across **all four hosts: Android, iOS, the kuikly_h5 host, and HarmonyOS** (`WegoKuikly`).

The canonical worked example is [`features/friends/README.md`](../kuikly_business_customer/src/commonMain/kotlin/com/truedian/wg/customer/features/friends/README.md) — read that for actual key/payload inventory. This section is the *recipe* for new ports.

### 11.1 The two directions

| Direction | Kuikly side | Native / host side |
|---|---|---|
| Kuikly → host | `wg.commonBridgeAsync(key, payload)` | Dispatcher in the host's common-bridge module routes by string key |
| Host → Kuikly | Host calls `delegator.sendEvent(name, payload)` | Page handles in `onReceivePagerEvent(name, data)` or in a pager lifecycle hook |

Lifecycle (`pageDidAppear` / `pageDidDisappear`) is the third channel — it covers the App-resume / page-hide events that used to flow as `window.activityResume` / `window.onAppPageHide`. The host shell forwards platform visibility to the SDK delegator automatically, you just override the pager hooks.

### 11.2 The dual-constant convention

Every bridge key is a **string** declared on both sides. A missing or mistyped key on either side silently no-ops; the SDK won't warn. The friends port keeps both sides in the same file region for review:

- Kuikly side: `<module>/router/CommonBridgeKey.kt` (`FRIENDS_*` constants).
- Android host: `app/.../AppRouterConfig.kt` (`ROUTE_FRIENDS_*`, same string).
- iOS host: ObjC selector name on the bridge category literally equals the string (`- (void)friendsDismissNewPushRing:`).
- H5 host: `when (method) { "friendsDismissNewPushRing" -> … }` in `WGCommonBridgeModule.kt`'s `call`.
- HarmonyOS host: the same string is an entry in the `BRIDGE_NAME_KUIKLY` enum (`wgCore/.../Base/enumerations/Bridge.ets`), plus a handler registered by that key in the module's `bridgeKuiklyRouterConfig.ets`.

Pager event names follow the same convention. Add a key — add the matching declaration in every shell you ship.

### 11.3 The platform shells

| Platform | Host type | How it loads bytecode | Notes |
|---|---|---|---|
| Android | `Fragment` (e.g. `KuiklyFocusFragment`) | DEX per `moduleId`, swapped at runtime | One bundle per business module. Tab-switch fires `onHiddenChanged`, *not* `onResume`/`onPause` — override both. `broadcastMessage` payload arrives as `{nameValuePairs: {from: …}}` from FastJSON; unwrap on the native side before dispatching to Kuikly. |
| iOS | `UIViewController` (subclass of `WGKuiklyRenderViewController`) | Single `shared.framework` from `:shared:syncFramework` | `fetchContextCodeWithPageName:` always returns `@"shared"`. Swift classes (e.g. `ShareWeChatManager`) reach ObjC through the auto-generated `<App>-Swift.h` bridging header that `PrefixHeader.pch` pulls in — don't import them explicitly. CocoaPods evaluates `spec.resources` globs at `pod install` time, so re-run `pod install` whenever you add an asset folder. |
| H5 (kuikly_h5) | HTML page bootstrap (`Main.kt` mounting `KuiklyWebRenderViewDelegator` on `#root`) | One `nativevue.js` produced by Kotlin/JS IR, page resolved by `?page_name=` URL param | The kuikly_h5 host is brand new — it does **not** carry a wgoo `appShare` bridge or any other native↔web channel that wsxc_portal had. The "native" side is just the surrounding browser plus what `index.html` loads (wgoo, sensors SDK, jweixin). Each bridge is plain JS calling those globals; many are not implementable at all. |
| HarmonyOS (`WegoKuikly`) | ETS — Kuikly mounted via `KuiklyComponent`/`KuiklyContainer`; the **bottom tabbar is itself a Kuikly page** (`app_main_tabs_page` / album's `MainTabsPage`) launched by `pages/KuiklyRootPage` | per-module HAR; `core-ohosarm64` (Kuikly 2.18.0) | Bridge dispatch: `KRBridgeModule.call(method, params, cb)` → `BridgeKuiklyRouter` (string-keyed EventBus) → the matching `bridgeKuiklyRouterConfig` entry → handler `apply()`. **Unlike Android (one `@Page` per native `Fragment` tab), a tab's content is embedded *inside* the Kuikly tabbar page** (visibility-toggled), so a cross-module tab goes through a cross-domain UI `ViewBuilder` — see §11.11. |

### 11.4 Adding a bridge

Four steps. Skip steps for shells the project doesn't target.

1. **Add the key** to `<module>/router/CommonBridgeKey.kt`. Choose a `friendsFooBar` style; this string IS the contract.
2. **Add a typed wrapper** in a per-page helper (e.g. `FriendsAppShareBridge.fooBar(...)`) that builds the `JSONObject` and calls `wg.commonBridgeAsync(KEY, payload)`. Callers in Kotlin never touch the string directly.
3. **Add a host handler** in every shell you ship:
    - Android: `when` branch in `KRCommonBridgeModule.call(...)` calling a private helper. Add a matching `ROUTE_FRIENDS_FOO` to `AppRouterConfig.kt`.
    - iOS: a method on `WGCommonBridgeModule+<Page>.m` whose selector name equals the key.
    - H5: a `when` branch in `WGCommonBridgeModule.kt`'s `call` calling a private function.
    - HarmonyOS: add the key to the `BRIDGE_NAME_KUIKLY` enum (`wgCore/.../Base/enumerations/Bridge.ets`); add an ETS class implementing `IKuiklyBaseBridge` in `<module>/src/main/ets/kuiklyApi/FriendsFooBar.ets` (its `apply(data, callback)` does the work); register it in `<module>/.../bridgeRouterConfig/bridgeKuiklyRouterConfig.ets`; and ensure `wgCore`'s `BridgeKuiklyRouter` deep-imports that module's config (the way it already does `wg_album`). Mirror an existing `wgAlbum/.../kuiklyApi/*.ets` handler (`Toast`, `OpenMiniProgram`, `ShareImage`, `ShareGoodsMiniAppToWechat`) and the `wechat.*` facade rather than reinventing.
4. **Call** the wrapper from the page Kotlin code.

If the underlying action already maps cleanly to an existing `wg.*` helper (e.g. `wg.vibrateLong`, `wg.toH5Page`, `BaseVisuals.showActionSheet`, `wg.openMiniProgram`), use that helper. Don't reinvent.

### 11.5 The three categories of bridges

This is the load-bearing part. When you map an App-only feature to other platforms, every bridge falls into one of these:

**(a) Direct port — same semantics, different SDKs.** Each host implements the same action with its native API.

```kotlin
// Kotlin caller — platform-agnostic
FriendsAppShareBridge.shareImagePosterToWeChat(posterUrl)
```
- Android: `ShareUtils.shareWxImage(url, …)` after permission dialog.
- iOS: download → `ShareWeChatManager.shareImageWithImage:scene:completion:` on a background queue then main.
- H5: usually not reachable (see (c) below).

**(b) Opt out at the Kotlin wrapper — work covered elsewhere on that platform.** Bridge is a no-op on the platform; *don't* write a no-op handler on the host side — gate it in the wrapper and never dispatch.

```kotlin
// FriendsAppShareBridge.kt
fun dismissNewPushRing(shopId: String) {
    if (AppConfig.isH5()) return                 // server clear already done from Kotlin
    wg.commonBridgeAsync(CommonBridgeKey.FRIENDS_DISMISS_NEW_PUSH_RING, …)
}
```
On Android/iOS this invalidates a native cache. On H5 the Kotlin code already covers the equivalent server clear (`vm.cancelAvatarCirclet`) — gating in the wrapper makes the platform asymmetry explicit at the contract level. Don't leave an empty handler in `WGCommonBridgeModule.kt`; drop the case from the `when` block entirely.

**(c) Branch at the call site — different UX per platform.** When the *user-facing flow* differs (App opens native modal, H5 shows an inline dialog), the page Kotlin branches, and only the App branch hits the bridge.

```kotlin
// FriendsContentView.handleInviteAction(ACTION_FANS)
if (AppConfig.isH5() || AppConfig.isOhos()) {
    showInviteFansActionSheet()                  // BaseVisuals.showActionSheet with 3 options
} else {
    FriendsAppShareBridge.openWebViewDialog("#customer/invite-fans-dialog?pageType=friend")
}
```
The H5/ohos branch uses an *existing* primitive — `BaseVisuals.showActionSheet` — and routes through *existing* helpers (`FriendsRouterUtil.toPhoneSearch`, `toShopQrCode`); it does not reinvent a modal/iframe/popup. **HarmonyOS joins H5 here** because its tabbar is Kuikly-hosted — there's no native WebView-dialog chrome to cooperate with, so the Kuikly ActionSheet is the natural render. And when a platform takes the actionsheet branch, **drop that platform's now-dead bridge handler**: the HarmonyOS `friendsOpenWebViewDialog` ETS handler + its `BRIDGE_NAME_KUIKLY` enum entry were removed (ohos never dispatches it), while Android/iOS keep theirs and the Kotlin wrapper/key stay for them.

### 11.6 Improvise vs. drop — the decision tree

Most App-only features should *not* turn into Kuikly improvisations. The default is to mirror what the original codebase already did. Walk the tree top-down:

1. **Look at the original wsxc_portal H5 source** (or wsxc_data sub-component) for the same feature.
    - If the original H5 had a real implementation: port that implementation to Kuikly H5. Use existing `BaseVisuals.*` / `wg.*` / `CommonRouterUtil` helpers. (Example: the App's native invite-fans dialog → H5's `<InviteFansWayDialog>` ActionSheet → Kuikly H5's `BaseVisuals.showActionSheet` with the same 3 options.)
    - If the original H5 dropped the feature: drop it on Kuikly H5 too. A no-op is the correct port.
2. **If you're tempted to invent a new UX** — pause and tell the human. Improvising is rare. The single canonical example in this codebase is [`MiniCodeFloatView`](../kuikly_business_album/src/commonMain/kotlin/com/truedian/wg/album/features/personalAlbum/components/MiniCodeFloatView.kt): the personal album's App share button has no H5 equivalent, so a floating QR code is permanently anchored to the right edge of the H5 page. It's a pattern to point at, not to apply by default.
3. **Don't bridge to a JS layer that isn't there.** kuikly_h5 doesn't host wgoo's `appShare` (it's a new H5 host, not an extension of wsxc_portal). Detecting `window.native.appclienShare` / `window.webkit.messageHandlers.webViewApp` and trying to dispatch through them is a dead end inside this bundle. Branch by `Client.iOS` / `Client.Android` / browser if the *web* behavior should differ — don't pretend the App is available.

### 11.7 "Intentionally not bridged"

`appShare(60)` / `appShare(331)` / `appShare(38)` were how the H5 page asked the WebView's native chrome to register/clear right-top icons. Kuikly pages draw their own `NavBar` (`actionComponent1` / `actionComponent2`) — there is no host chrome to cooperate with. Delete those bridges; don't port them.

Same principle applies elsewhere: any App bridge that exists only to drive a WebView host slot (status bar, navigation bar, swipe-back configuration) has no Kuikly counterpart, because the Kuikly page owns the slot itself.

### 11.8 Native → Kuikly events

Same dual-constant rule. The host shell turns a platform signal into a pager event:

| Pager event | Android source | iOS source | H5 source |
|---|---|---|---|
| `albumUpdateFollowed` (unfollow / set-top from another page) | `PrefsUtils(PREF_NOATTENTION_ALBUM)` flushed in `KuiklyFocusFragment.onResume` | `NSNotificationCenter` observers on `kWGNotificationCancelAttention` / `DeleteFans` / `SetTopFriend`, payload's `shop_id` | (none — no cross-page navigation context in the standalone H5 host) |
| `getAppTabsTip` (red-dot / tab status refresh) | `MainActivity.webViewTabStatuses` iterates Fragments | `BADGE_KEY` notification `userInfo[@"tab"]` | (none) |
| `broadcastMessage` (in-app event bus: bindPhoneSuccess / copyPhone / contact toasts) | `MainActivity.h5Callback(@EventObserver Constants.H5_CALLBACK)` from WgBus; unwrap FastJSON's `nameValuePairs` before forwarding | (no clean source — wsxc_rn iOS has no WgBus analog; left unwired) | (none) |

Lifecycle covers the other two H5 globals — `pageDidAppear` for `activityResume`, `pageDidDisappear` for `onAppPageHide`. On Android tab switches you must override `onHiddenChanged` *in addition to* `onResume`/`onPause`, because show/hide doesn't fire the resume callbacks.

**HarmonyOS** delivers pager events through the render controller: `KuiklyContainer.kuiklyViewControllerReady` hands back a `KRNativeRenderController`, and `controller.sendEvent(name, KRRecord)` lands in `onReceivePagerEvent`. But when the page is *embedded* in the Kuikly tabbar (the friends content inside `MainTabsPage` — §11.11), the host holds only an opaque `ViewBuilder`, no typed ref to forward into; and HarmonyOS has no unfollow-pref / tab-status / broadcast-bus source yet — so these three events aren't wired there (the ComposeView's `created()` covers first-load). A `FriendsPagerEvents` helper wraps `controller.sendEvent` for when a source appears.

If a pager event has no source on a platform, **don't wire it**. The handler simply never fires, which is correct.

### 11.9 Per-platform gotchas

**Android**
- `broadcastMessage` payload arrives `{nameValuePairs: {from: …}}` (FastJSON wrap); flatten on the native side.
- Tab switches: `onHiddenChanged` fires, `onResume`/`onPause` don't. Override both.
- KSP `subModules` arg in all four `build.<platform>.gradle.kts` must list the same modules; mismatch produces `Unresolved reference 'KuiklyCoreEntry_<id>'`.

**iOS**
- Single `shared.framework` — `fetchContextCodeWithPageName:` always returns `@"shared"`.
- Swift bridging: import via `PrefixHeader.pch` ↔ `<App>-Swift.h`; no per-file `#import` for Swift classes.
- CocoaPods `spec.resources` globs expand at `pod install` time. After adding an asset folder, re-run `pod install`.
- WeChat OpenSDK miniprogram send: decode the thumb + JPEG encode on a background queue (`USER_INITIATED`), hop to main for `WXApi.send`. Calling from main races against the compression and ships an empty `hdImageData`. This mirrors Android's `AppExecutors.autoExecute` wrap.
- Kuikly's `view.toImage(ImageType.FILE)` returns `file://…` on iOS. `[UIImage imageWithContentsOfFile:]` silently returns `nil` for the URI form — strip the prefix.
- `WGWechatHelper.getMiniProgramObj` compresses to ≤128 KB into `WXMiniProgramObject.hdImageData` (NOT 32 KB `thumbData`). Don't pre-compress on the bridge side.

**H5**
- No `appShare`. Use what `index.html` already loaded: `window.wgoo.$toast`, `window.sensorsDataAnalytic201505.track`, jweixin's `wx.*` if running inside WeChat.
- Three of the friends bridges are gated upstream (`shareImagePosterToWeChat`, `openWeChatMiniApp`, `shareMiniProgramCard`) and never reach H5. Don't add empty `when` cases for them.
- Native → Kuikly event sources don't exist. The friends page's event handlers simply don't fire, which is correct.
- For App-only flows that DO leak through, follow §11.6 — port the original H5 alternative (e.g. `BaseVisuals.showActionSheet` for invite-fans), don't invent.
- Asset packaging is build-pipeline, not bridge: `aggregateSubModuleAssets` copies sub-module `commonMain/assets/` into the H5 bundle output; static-hosting upload is out of band.

**HarmonyOS**
- Host is ETS (`WegoKuikly/ohosApp`). Kuikly pages mount via `KuiklyComponent`/`KuiklyContainer`; the production main UI is the Kuikly `app_main_tabs_page` (`MainTabsPage`) launched by `pages/KuiklyRootPage` — the tabbar is Kuikly, **not** native. A tab's content is embedded in that page (visibility-toggled); cross-module tabs come through a cross-domain UI `ViewBuilder` (§11.11). (`old/pages/Index.ets`, 5 ArkUI WebView tabs, is only the legacy `entryType == "H5"` build entry — don't wire features there.)
- Bridge handlers are ETS classes implementing `IKuiklyBaseBridge` in `<module>/src/main/ets/kuiklyApi/`, registered in the module's `bridgeKuiklyRouterConfig.ets`; `wgCore`'s `BridgeKuiklyRouter` deep-imports each business module's config (the circular dep `wgCore` ↔ business module is tolerated, same as `wg_album`). Keys live in the `BRIDGE_NAME_KUIKLY` enum. Reuse `wgAlbum/.../kuiklyApi/*.ets` handlers and the `wechat.*` facade.
- `WLog` only has `.d` / `.e` / `.i` — **no `.w`**.
- ArkTS strict mode (`arkts-no-untyped-obj-literals`): an object literal must correspond to a declared class/interface/`Record`. `objLiteral as <ConcreteType>` does **not** satisfy it — use an annotated assignment (`const x: Record<string, Object> = {…}`). `as tsType.tsAny` / ESObject is exempt. A raw `@kit.BasicServicesKit` `emitter.EventData` literal also trips it. `ESObject` param types only *warn* (`arkts-limited-esobj`), don't fail the build.
- New HAR module: its `module.json5` name (e.g. `wgCustomer`) differs from its oh-package name (`wg_customer`); register the module in `build-profile.json5` and add the package to the root `oh-package.json5`.
- Build/verify with `ohosApp/build_remote_ohos.sh` — it compiles the Kotlin shared layer to `ohosArm64` (konanc) *and* the ETS app into a signed HAP, so it catches both Kotlin and ArkTS errors.

### 11.10 Page registry and module identity

`@Page("album_friends_page")` is the canonical pageName. Native shells (`KuiklyFocusFragment.PAGE_NAME`, iOS `WGKuiklyRouterPageManager.pageNameWithPageType:`, H5 `?page_name=` URL parameter) all reference this string. The friends page kept the `album_*` prefix even after moving from `kuikly_business_album` to `kuikly_business_customer` — page names are public contracts with native shells and the dynamic-publish system; module ownership can move, page names cannot.

Cross-domain navigation (`wg.navigateToPage(pageName, currentModuleName, toModuleName, params)`) requires the target page to be listed in the destination module's `<Module>ExposedPages.exposedPages` whitelist. The customer→album shop-detail navigation is the worked example in `FriendsRouterUtil.toShopDetail`. (Note: the `wg.navigateToPage` signature has evolved across core versions — newer core takes `(moduleName, pageName, …)` and auto-resolves the target domain from `pageName`. Match whatever signature the core you build against exposes.)

### 11.11 Embedding a page's content cross-domain (Kuikly-hosted tabbars)

On Android the friends tab is a standalone `@Page` mounted in its own native `Fragment` (`KuiklyFocusFragment`). On HarmonyOS the tabbar is *itself* a Kuikly page (`app_main_tabs_page` / album's `MainTabsPage`), so a tab's content must be a **child view inside that page**, not a separately-mounted `@Page`. Two constraints make this non-trivial: a `Pager` can't be embedded as a child, and the tabbar lives in a *different* business module (album) that doesn't depend on the friends module (customer). The pattern:

1. **Extract the page body into a `ComposeView`.** `FriendsContentView : ComposeView<…>` holds all the UI + VM + handlers. `created()` does first-load init; `viewDestroyed()` cleans up; public `pageDidAppear()` / `handlePagerEvent(...)` are forwarded by whatever host holds a ref. `pagerId` / `pagerData` / `async{}` / `PopViewSelectController.create(this)` all work on a `ComposeView` (it *is* a `PagerScope`) — mirror album's `DynamicMainView`. (Gotchas during extraction: `lifecycleScope.launch` → `async{}`; `pageData` → `pagerData`; a VM's `pagerId` getter should read `pagerScope.pagerId`, not `(pagerScope as? Pager)?.pagerId`.)
2. **Keep a thin `@Page`** for the standalone hosts: `FriendsPage.body()` = `DialogContainer { FriendsContent { } }`, forwarding `pageDidAppear`/`onReceivePagerEvent` into the ComposeView via a ref. (Android's Fragment still mounts this `@Page`.)
3. **Expose it cross-domain** via the UI capability service: add `getFriendsTabView(): ViewBuilder` to `I<Domain>UIService` (`kuikly_core/servicebus/service/<domain>/`), implement in `<Module>UICapability` → a delegate returning `{ FriendsContent { } }`, and register the capability in `WGCrossDomainService` (`kuikly_init`).
4. **Host embeds it** without a compile dependency on the other module: `MainTabsPage` (album) renders `CrossDomainServiceManager.getCustomerUIService()?.getFriendsTabView()?.invoke(this)` inside a visibility-toggled `View`.

This is the canonical way to place one domain's full page into another domain's Kuikly-hosted container.

---

## 12. Things that don't map

A "rebuild rather than translate" list. Plan for these.

1. **`react-intl`** — no built-in i18n. The project provides `wgRes`/`wgRaw` string tables; analytics labels and server-side fixed tokens go in `wgRaw`, user-facing copy in `wgRes`. `:scanKmpAll` fails otherwise.
2. **`react-router` URL / hash semantics** — Kuikly has no URL bar, no browser back. Forward = `openPage`, back = `closePage`. Deep links = host passes initial params; live URL sync does not exist.
3. **`React.lazy` + `Suspense`** — page-level code splitting is implicit (each `@Page` can be its own bundle in dynamic mode); arbitrary component-level lazy boundaries do not exist.
4. **`React.memo` / `useMemo` / `useCallback`** — Kuikly's reactivity is per-closure, so most of these become unnecessary. If you find a true perf issue, the levers are: minimise observable surface area, set `keepAlive(true)` on heavy scroll items, push hot loops to native via a Module.
5. **DOM measurement (`getBoundingClientRect`)** — no DOM. Use `event { layoutFrameDidChange { frame -> … } }` or `viewDidLayout()` + `ref?.view?.frame`.
6. **Portals mounted outside the root** — `Modal { inWindow(true) }` or a `BaseVisuals` helper.
7. **`window.location.href = '…'` for full reload** — pages don't reload. Re-open or invalidate + re-fetch.
8. **`window.scrollTo`** — pages don't auto-scroll. Scroll a `List` / `Scroller` you own (`ref?.view?.setContentOffset(0f, 0f, animated = true)`).
9. **Browser-only APIs** (clipboard, geolocation, file pickers, push, Bluetooth) — each becomes a custom Module per platform.
10. **Lottie** — re-encode as PAG.
11. **CSS `:hover`** — not a Kuikly concept; synthesise from pointer events on PC if needed.
12. **`document.execCommand('copy')`, drag-and-drop** — custom modules per platform.
13. **CSS Grid** — convert to nested FlexBox; for card grids use `WaterFallList`.
14. **`react-virtuoso` with custom item heights** — Kuikly's `List` wants consistent shape; use `WaterFallList` or measure-then-rebuild.

---

## 13. Migration recipe

### Phase 1 — Survey
- [ ] Identify the page's stores (singleton vs Provider-injected vs `useLocalStore`).
- [ ] List `componentDidMount` side effects (fetch, listeners, analytics).
- [ ] List `componentWillUnmount` cleanups.
- [ ] Enumerate every `wgoo.*` / `motify.*` / `localStorage.*` / `window.*` / `appShare(N, …)` call. Each is either a `BaseVisuals` mapping, a `wg.*` helper, or a new bridge (see §11).
- [ ] List sub-components and which have their own state.
- [ ] Note imperative vs render-in-place modals.
- [ ] Find DOM-poking (`getBoundingClientRect`, `querySelector`, `localStorage`, `URL`) — flag for rebuild.

### Phase 2 — Skeleton
- [ ] Pick the owning business module. Create `features/<page_name>/`.
- [ ] Create `page/<X>Page.kt` with `@Page("<page_name>")` (preserve the H5 page name string if any system identifier — analytics, dynamic publish, native shell mounts — references it).
- [ ] Register the page name in the module's `PageConfig` and (if cross-domain navigation is involved) `<Module>ExposedPages`.
- [ ] Create `viewModel/<X>ViewModel.kt` taking `(scope: PagerScope)`. Declare `var x by scope.observable(…)` for every observable.
- [ ] Define `@Serializable` data classes for every response (`bean/`).
- [ ] Define `<X>ApiPaths.kt` (`network/`).
- [ ] Empty `body()` returning `View { }` — verify it loads.

### Phase 3 — Lifecycle
- [ ] Move `componentDidMount` content into `created()`, wrap async work in `async { … }`.
- [ ] Move `componentWillUnmount` into `pageWillDestroy()`.
- [ ] Map any `[dep]`-deps `useEffect` to `bindValueChange({ … }) { … }` in `created()`.
- [ ] Pair every `addNotify` with `removeNotify`.

### Phase 4 — Data layer
- [ ] Convert each `@action async` to `suspend fun`. Direct-assign; no `runInAction`.
- [ ] `wgoo.$http.get/post` → `getRequest/postFormRequest/postRequest(...).send<T>()`.
- [ ] Loading flag = an observable + `try/finally`.

### Phase 5 — View
- [ ] Walk JSX top-down: each `<div>` → `View`, each `{cond && …}` → `vif`, each `arr.map(...)` → `renderList`.
- [ ] Convert CSS: `.module.less` → inline `attr {}`; tokens → `WGColor` / `WGFont`.
- [ ] Convert each sub-component to its own `ComposeView<Attr, Event>` with a `ViewContainer<*,*>.XView { … }` DSL helper.
- [ ] Move callback props into `Event`.

### Phase 6 — Modals & overlays
- [ ] Render-in-place: keep `{showX && <X/>}` as `vif({ ctx.showX }) { … }`.
- [ ] Imperative dialogs → `BaseVisuals.show*`.

### Phase 7 — Animation
- [ ] CSS transitions → `animate(Animation.linear(0.3f), trigger)`.
- [ ] CSS keyframes → `viewRef.view?.animateToAttr(…)`.
- [ ] Lottie → PAG.

### Phase 8 — Wire native bridges
- [ ] For each `appShare(N, …)`, `window.*` listener, and `window.*` callback: pick a side (bridge call vs pager event vs lifecycle hook) and add it on **both** Kuikly and native sides — the constants must match across the two declaration sites. See [`features/friends/README.md`](../kuikly_business_customer/src/commonMain/kotlin/com/truedian/wg/customer/features/friends/README.md) for one platform's worked end-to-end inventory; the full cross-platform template lands in §11 when iOS and H5 ports complete.

### Phase 9 — Verify
- [ ] Run on each target platform actually shipping this page.
- [ ] Verify pull-refresh, infinite scroll, navigation params, return-data flows (NotifyModule), analytics PVs/clicks.
- [ ] Watch for `PagerNotFoundException` (touching `pagerData`/`acquireModule` before `created()`).
- [ ] Watch for "UI doesn't update" — usually a non-reactive read of `ctx.foo` outside an `attr {}` / `event {}` / `vif {}`.

---

## 14. Pitfalls

Most of these you'll hit at least once.

1. **`val ctx = this`.** Inside `body()`, the receiver is a `ViewContainer`, not the Pager. Capture: `val ctx = this@MyPage`.
2. **Treating `body()` like `render()`.** `body()` runs once. Reactive work belongs inside `attr {}` / `event {}` / `vif {}` / `renderList {}`.
3. **Top-level `by observable(...)`.** Inert. Move into a Pager / ComposeView / `ViewModel(scope: PagerScope)`.
4. **Mutating an observable from off-thread.** Wrap in `KuiklyContextScheduler.runOnKuiklyThread(pagerId) { … }`, or have your Module callbacks come back on the Kuikly thread by default.
5. **`Input.text(initial)` is initial-only.** Programmatic updates: `ref?.view?.setText(s)`. The reactive direction (UI → state) works through `textDidChange`.
6. **`vif` unmounts.** Hidden subtree loses scroll position, focus, internal observables. To hide without losing state, use `visibility(false)`.
7. **Expecting `Provider` / context.** None exists. Pass via `attr`, hold a singleton, or use `NotifyModule`.
8. **PageScope-bound observables leak across pages.** Observable bound to one Pager only drives UI in that Pager. Cross-page sync = `NotifyModule`.
9. **Forgetting that `renderList(isLazy = true)` needs a `ListView` receiver.** Nesting under a `vif {}` silently degrades to eager rendering.
10. **Calling suspending HTTP from a non-suspend function.** Wrap in `async { … }`. Forgetting to launch silently does nothing.
11. **Layout math against `pageViewWidth` before `pageDidAppear`.** `pagerData` is good from `created()`; child frames are valid only after `viewDidLayout` / a `layoutFrameDidChange` event.
12. **Assuming `flexDirection` defaults to `ROW`.** Kuikly's default is `COLUMN`. Set `flexDirectionRow()` explicitly where the web sense expected rows.
13. **Relying on `overflow: hidden` by default.** Kuikly's default is no clipping. Set `overflow(true)` on the parent to clip.
14. **Hashed routing's URL-state habit.** No URLs. Bookmarkability, browser back, deep links — all native-side.
15. **`useMemo` for "expensive computation in render".** Not needed. A pure getter recomputes only when its inputs change *and* it's read from a reactive scope.
16. **Looking for `JSX.Element` children.** Children are `ViewContainer<*,*>.() -> Unit` builder lambdas. The "render whatever the parent gives me" pattern: `var content: (ViewContainer<*,*>.() -> Unit)? = null` on `Attr`, invoke as `ctx.attr.content?.invoke(this)`.
17. **`pageWillDestroy` access to Modules is best-effort.** Native may have torn down. Critical cleanup goes to the native side.
18. **KSP module-list drift.** Adding a new business module requires updating all four root `build.<platform>.gradle.kts` `subModules` args. The `KuiklyCoreEntry_<id>` aggregator is generated; a mismatch breaks the build.

---

## Cross-references

- [`AGENTS.md`](../AGENTS.md) — root authoritative spec (page recipe, module setup, KSP wiring).
- [`basic_reference.md`](./basic_reference.md) — KuiklyUI surface API summary (Pager, components, attr, observable, renderList, vif, network, BaseVisuals).
- [`extended_reference.md`](./extended_reference.md) — full understanding, gotchas, edge cases.
- [`features/friends/README.md`](../kuikly_business_customer/src/commonMain/kotlin/com/truedian/wg/customer/features/friends/README.md) — the canonical worked example for this guide.
- [`basic_components/`](./basic_components/index.md) — in-house WG component library.
- [`DevGuide/`](./DevGuide/) — framework-level concept docs (中文).
- [`API/components/`](./API/components/) and [`API/modules/`](./API/modules/) — per-component / per-module APIs.
