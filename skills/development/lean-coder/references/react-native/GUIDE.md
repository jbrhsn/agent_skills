# React Native (TypeScript) — Lean Rules

Read `references/typescript-react/GUIDE.md` for the TypeScript and React rules. This file adds only what is RN-specific.

## Platform / RN first

| Need | Use | Not |
|---|---|---|
| Navigation | React Navigation (native stack) | custom router |
| Secure storage | `expo-secure-store` / Keychain-backed lib | `AsyncStorage` for tokens |
| Lists | `FlashList` or `FlatList` with `keyExtractor` | `.map()` inside `ScrollView` |
| Animation | Reanimated worklets, `LayoutAnimation` | `Animated` chains on the JS thread |
| Gestures | `react-native-gesture-handler` | `PanResponder` |
| Env config | `expo-constants` / build-time config | committed config files |
| Platform branch | `Platform.select` | duplicated `.ios.tsx`/`.android.tsx` files for a 3-line diff |
| Images | `expo-image` with cache policy | manual cache layer |

## Cut

- Custom `Button`/`Text` wrappers that only pass props through
- StyleSheet entries used once → inline style object
- One deep `styles` object per file; delete unused keys aggressively
- `useEffect` fetch-on-mount → a data library's `useQuery` (already handles loading, error, retry, cache: ~10 lines saved per screen)
- Redux for server state — that is cache, not state
- Manual keyboard/dimension listeners when `useWindowDimensions` / `KeyboardAvoidingView` exist
- Separate `styles.ts` files that force two-file edits for one visual change

## Rules

- Screens are thin: navigation params → hook → presentational components.
- Keep the JS thread free: heavy work in Reanimated worklets or native modules, never in `onScroll` handlers.
- Type navigation params once (`RootStackParamList`) and derive screen props from it.
- Memoize `renderItem` and row components only for long lists — that is the one place it pays.

## Security (never cut)

- Anything bundled is readable. No API secrets in the app; proxy through your backend.
- Tokens in SecureStore/Keychain/Keystore, never `AsyncStorage`.
- Validate deep-link params before navigating or acting.
- HTTPS only; block cleartext in both `Info.plist` and the Android network security config.
- No PII in `console.log` — strip logs in release builds.
- Sanitize anything rendered into a `WebView`; disable JS in it unless required.

## Testability

- Logic lives in hooks and pure functions → test with `@testing-library/react-hooks` / plain Jest, no renderer needed.
- Component tests via `@testing-library/react-native` querying by accessibility role/label — which also improves accessibility.
- MSW or a single fetch stub at the boundary; do not mock components.
- Detox only for critical flows (login, checkout); everything else at unit level.

## Example

```tsx
// before — 24 lines: useState x3, useEffect, ScrollView.map
// after — 4
const { data = [], isLoading } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });
if (isLoading) return <ActivityIndicator />;
return <FlatList data={data} keyExtractor={u => u.id}
  renderItem={({ item }) => <Text>{item.name}</Text>} />;
```
