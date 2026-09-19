# Surface questions

Infer the interaction surface from the brief and existing implementation. Ask only where a missing answer changes the product; this can happen alongside requirements discovery.

For web/mobile/desktop, clarify the primary journey, navigation, meaningful states, accessibility, responsive/device behavior, and existing design system. Mobile may need offline, permission, background, and restoration semantics. Do not ask users to enumerate every component before proposing a reasonable design.

For CLI/chat/voice, clarify invocation, session state, cancellation, error recovery, machine-readable output, and non-interactive operation.

For headless systems, clarify consumers, input/output schemas, authentication/authorization, errors, versioning, ordering, idempotency, and partial success. A pipeline with no UI needs a data/job contract rather than a fabricated dashboard.

For wallet-based applications, clarify account/network changes and transaction status visibility. For troubleshooting plans, clarify the observed failure and permissible experiments rather than launching a product interview.

Record decisions and assumptions directly in the relevant specification. Ask for review when the user requests it or a consequential unresolved choice blocks dependent work.
