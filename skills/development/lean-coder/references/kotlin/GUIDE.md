# Kotlin and Android

Inspect minimum/target SDK, Kotlin/toolchain versions, and the project's Compose/View architecture. Preserve existing conventions unless changing them is part of the task.

## State and lifecycle

Give screen state a clear owner and collect observable state with lifecycle-aware APIs. Hoist state where shared ownership helps; do not remove ViewModels or interfaces based on size alone.

Use structured coroutine scopes appropriate to operation lifetime. Propagate cancellation rather than swallowing it in broad exception handlers. Move blocking I/O and CPU work to appropriate dispatchers. Avoid duplicate requests or collectors during recreation and navigation.

Distinguish configuration recreation, process death, and durable work. Use saved state for appropriate UI state and persistent storage/schedulers for work that must survive process loss. Define offline retries, duplicate prevention, permission denial, and restoration behavior. Test database migrations and concurrent updates.

## Security and UX

Keep secrets out of APK resources and build constants. Use a maintained secure-storage approach and Android Keystore for key protection where appropriate; plaintext preferences/DataStore are not encrypted secret storage. The old security-crypto APIs are deprecated; check supported replacements and migration needs rather than introducing EncryptedSharedPreferences by default. See [Android cryptography guidance](https://developer.android.com/privacy-and-security/cryptography).

Limit exported components, validate intents/deep links, scope PendingIntent capabilities, and keep TLS validation enabled. Pinning needs an operational rotation/recovery plan; consult [network security configuration](https://developer.android.com/privacy-and-security/security-config).

Support TalkBack, text scaling, focus, touch targets, system insets, and relevant device sizes. Handle permission revocation, background restrictions, and process restart without losing committed work.

## Verification

Use JVM tests for logic, coroutine test dispatchers for deterministic scheduling, and instrumentation/Compose/View tests for platform behavior. Test process recreation, offline recovery, persistence upgrades, and relevant API levels. Validate release builds where shrinking/obfuscation, manifests, signing, or build configuration differs. Profile startup, jank, memory, and battery on representative devices when performance is in scope.
