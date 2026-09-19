# TypeScript, React, and Next.js

Follow the installed framework/router/runtime and existing data, form, state, and design-system choices. Do not migrate architecture for an incidental change. Add [web guidance](../web/GUIDE.md) for HTTP, security, caching, and accessibility.

## Types and state

Use runtime validation for external data and narrow unknown values. Model meaningful states with types that prevent invalid combinations; avoid assertions that merely hide errors. Keep explicit public contracts where helpful and infer local types when clear.

Derive values from current props/state when practical. Effects synchronize external systems and need dependency, cleanup, and race handling. Use framework data loading or established cache libraries when they fit; account for cache keys, invalidation, cancellation, stale responses, and mutation rollback.

Extract components/hooks to clarify ownership or isolate behavior, including single-use ones. Memoization should address a demonstrated cost or required identity contract, not a quota. Stable list keys represent identity rather than current array position when items can move.

## Rendering and security

Place client/server boundaries according to required interactivity and data ownership. Check hydration consistency, serialization, error boundaries, and framework-specific cache behavior. Keep secrets server-side and authorize server handlers/actions independently of rendered controls.

Validate external inputs before using them. Sanitize rich HTML when needed, parameterize database access, and return only intended fields. TypeScript does not enforce authorization or sanitize data.

Use semantic elements, labels, focus management, keyboard behavior, and meaningful loading/error states. Measure bundle cost, waterfalls, rendering, and interaction delays before adding lazy loading or broad memoization.

## Verification

Test observable behavior through accessible roles and user actions; use API/integration tests for server contracts and selected browser tests for critical flows. Reuse providers/fakes that mirror the actual app without mocking away the contract under test. Check production builds when rendering/runtime differences matter.
