# Swift — Lean Rules

## Platform first

| Need | Use | Not |
|---|---|---|
| JSON | `Codable` + `CodingKeys` | manual dictionary parsing |
| HTTP | `URLSession` + `async/await` | Alamofire for basic requests |
| Local storage | `SwiftData` / Core Data / `UserDefaults` (settings only) | custom file format |
| Formatting | `.formatted()`, `FormatStyle` | `DateFormatter` instances everywhere |
| Reactive state | `@Observable`, `@State`, `@Binding` | Combine pipelines for simple state |
| Concurrency | `async let`, `TaskGroup`, `actor` | DispatchQueue juggling, completion handlers |
| Collections | `map`/`filter`/`reduce`/`compactMap` | index loops |

## SwiftUI

- View bodies stay short: extract a subview only when it is reused or the body exceeds a screen — not to hit an arbitrary line count.
- One source of truth. `@State` private to the view, `@Binding` down, `@Observable` model for shared state.
- No ViewModel for a view that only renders and calls one async function — put the call in a `.task {}`.
- Modifiers over conditionals: `.opacity(isOn ? 1 : 0)` instead of two `if` branches returning near-identical views.
- Let `struct` + `Identifiable` drive `ForEach`; no manual index bookkeeping.

## Cut

- `init` that only assigns stored properties (memberwise init exists)
- Getters wrapping private stored properties
- Protocols with one conformer
- `guard let x = x else { return }` chains → `if let` shorthand `if let x`
- `self.` where not required
- Explicit types where inference is clear
- Completion-handler versions of functions that now have async equivalents

## Security (never cut)

- Tokens and keys in Keychain, never `UserDefaults`, never in code or `.plist`.
- ATS on; no arbitrary-loads exception. Pin certs for high-value endpoints.
- Biometric/`LocalAuthentication` result must be verified server-side too — local success alone is not authorization.
- Mark sensitive fields `.privacy(.private)` in `Logger`; default `os_log` interpolation of strings is redacted, but check.
- Validate deep-link and universal-link parameters before acting on them.
- File writes with `.completeFileProtection`.

## Testability

- Business logic in plain `struct`s with pure methods — testable without a host app.
- Inject `URLSession` (or a `protocol` with one real + one stub conformer) instead of calling `.shared` inside the type.
- Swift Testing (`@Test`, `#expect`) with parameterized arguments over duplicated test funcs.
- Keep `View` bodies free of logic so snapshot/UI tests stay unnecessary.

## Example

```swift
// before — 18 lines: ViewModel + completion handler + manual JSON
// after — 4
func loadUsers() async throws -> [User] {
    let (data, _) = try await URLSession.shared.data(from: usersURL)
    return try JSONDecoder().decode([User].self, from: data)
}
```
