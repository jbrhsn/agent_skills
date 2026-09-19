# Swift and iOS

Inspect the deployment target, Swift version, existing SwiftUI/UIKit architecture, persistence, and dependencies. Use platform capabilities where they fit without forcing a framework migration.

## State and lifecycle

Choose a clear state owner and appropriate actor isolation for mutable state. Keep UI updates on the required actor and expensive work off the main thread. Match observation APIs to supported OS versions; avoid introducing availability failures.

Tie tasks to intended lifetimes and prevent stale responses from overwriting newer state. Cancellation is cooperative: propagate it and check it during long work. Account for navigation, backgrounding, termination, restoration, and offline retry; a view task is not a durable background job.

Validate HTTP status and response shape before treating decoded data as success. Distinguish network, server, decoding, and cancellation outcomes. Test persistence migrations and recovery from interrupted writes.

## Platform and security

Use Keychain for appropriate secrets with accessibility settings matched to required background access. Consider file protection, backups, logout cleanup, and locked-device behavior. Bundled configuration cannot hold server secrets.

Validate deep/universal links and authorization before sensitive actions. Local biometric success gates local access; backend actions still require server authorization. Use normal TLS/ATS protections; pinning requires a threat model and rotation/recovery plan rather than being a default.

Support Dynamic Type, VoiceOver, focus, safe areas, permission denial/revocation, and meaningful offline/error states. Verify current platform/store requirements when release work touches them.

## Verification

Test business/state logic and network/persistence boundaries, plus selected UI tests for navigation, accessibility, and lifecycle. Use appropriate XCTest or Swift Testing conventions already present. Exercise supported OS/device configurations and release builds when affected; simulator evidence does not cover every hardware, performance, or background-execution property.

See [Apple's Task documentation](https://developer.apple.com/documentation/swift/task/) for cancellation and structured concurrency details.
