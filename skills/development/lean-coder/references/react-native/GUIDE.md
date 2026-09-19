# React Native

Use [TypeScript / React](../typescript-react/GUIDE.md) for shared language/state guidance and Swift or Kotlin when modifying native code. Check the repository's React Native/Expo versions, native architecture, navigation, and supported OS targets before choosing APIs.

## Boundaries and lifecycle

Reuse the established native and JavaScript libraries where suitable. Cross-platform code does not imply identical behavior: specify platform differences in permissions, background execution, navigation/back handling, links, keyboards, safe areas, and storage.

Handle app suspension, termination, offline state, reconnection, and account changes. Separate pending optimistic state from server-confirmed state. Durable background work requires a supported platform mechanism, not an assumed long-lived JS timer.

Virtualize genuinely large lists, use stable item identity, and measure JS/UI thread work, memory, startup, image cost, and bridge/native calls. Do not move arbitrary heavy computation into animation worklets; it may block UI work. Choose workers/native processing or batching based on measured workload and runtime support.

## Security and compatibility

Use maintained Keychain/Keystore-backed storage for appropriate secrets, with explicit backup and logout behavior. AsyncStorage and bundled environment values are not secret stores. Validate deep links, WebView navigation/messages, and server authorization independently of UI state.

Check native dependency compatibility, autolinking/build configuration, and release behavior. Over-the-air updates must match installed native capabilities and the project's release policy; a JS-only change can still require a new native binary.

## Verification

Test hooks/components with the project's supported tooling through observable user behavior. Add native integration or device end-to-end tests where permission, link, storage, navigation, or lifecycle behavior crosses the boundary. Test both supported platforms, accessibility, denied permissions, and release builds when affected. Do not present one simulator's debug performance as a production benchmark.
