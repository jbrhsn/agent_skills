# Kotlin — Lean Rules

## Language and stdlib first

| Need | Use | Not |
|---|---|---|
| Data holders | `data class` | class + equals/hashCode/toString |
| Null safety | `?.`, `?:`, `let` | manual null checks / `!!` |
| Errors | sealed `Result`-style class | exceptions across layers |
| Collections | `map`/`filter`/`groupBy`/`associateBy` | loops with mutable lists |
| Concurrency | coroutines, `Flow`, `viewModelScope` | RxJava, `AsyncTask`, threads |
| DI | constructor injection; Hilt only if the graph is real | a container for 3 objects |
| Serialization | `kotlinx.serialization` | Gson + manual TypeToken |
| Constants | `enum class` / `sealed interface` | string keys |
| Extensions | extension functions | Utils classes with static methods |

## Android / Compose

- `@Composable` state hoisted upward; stateless composables take data + lambdas. That alone deletes most ViewModel glue.
- One `StateFlow<UiState>` per screen, `UiState` a single data class — not five `LiveData` fields.
- `collectAsStateWithLifecycle()`; no manual lifecycle observers.
- No `Fragment` + `View` + XML for a screen Compose renders in one function.
- Repository returns `Flow`; ViewModel maps it; UI renders it. No callbacks in between.

## Cut

- `findViewById` / `ViewBinding` boilerplate once on Compose
- Interfaces with one implementation (very common in Android DI cargo cult)
- `Builder` classes — named + default arguments replace them
- `object Utils` holders → top-level or extension functions
- `if (x != null) { x.y() }` → `x?.y()`
- Explicit `return` types on obvious one-expression functions
- Getters/setters; `companion object` constants that only wrap a literal

## Security (never cut)

- No secrets in `BuildConfig`, source, or `strings.xml` — they ship in the APK.
- `EncryptedSharedPreferences` / Keystore for tokens.
- `exported="false"` by default on components; validate every `Intent` extra and deep link.
- Cleartext traffic off; use the network security config; pin for high-value APIs.
- `PendingIntent` with `FLAG_IMMUTABLE`.
- Never log tokens or PII; strip logs in release via ProGuard/R8 rules.

## Testability

- ViewModels take repositories via constructor — a fake repo is 5 lines and needs no mocking framework.
- Pure mapper functions (`Dto -> UiState`) hold the real logic and test as plain JVM unit tests.
- `runTest` + `TestDispatcher` injected, never `Dispatchers.Main` hardcoded.
- Turbine for `Flow` assertions; assert on emitted `UiState` values, not on view state.

## Example

```kotlin
// before — 15 lines: LiveData fields, null checks, callback
// after — 3
val uiState: StateFlow<UiState> = repo.users()
    .map { UiState(users = it, loading = false) }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), UiState())
```
