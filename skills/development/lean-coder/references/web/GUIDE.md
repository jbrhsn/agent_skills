# Web applications and services

Use alongside a language guide for browser, HTTP, backend, and full-stack changes.

## Contracts and security

Trace the user action through validation, authentication, resource authorization, persistence, and response. Enforce tenant/object permissions on the server for reads and writes, including jobs and downloads. Client validation is not a security boundary.

For browser sessions, use secure cookie attributes and CSRF protection appropriate to the authentication model. CORS is not authentication. Encode output for its context; sanitize rich HTML with a maintained sanitizer. Bound upload size/type/storage exposure and validate outbound destinations against SSRF, including redirects and resolution where relevant.

Define API errors/statuses, stable pagination/sorting, concurrency conflicts, and retry semantics. Preserve consumers or plan migration. Return explicit response fields rather than exposing persistence objects wholesale.

## State and performance

Represent meaningful loading, empty, error, success, and retry states without erasing usable prior data unnecessarily. Handle stale responses, double submission, optimistic update rollback, and expired sessions. Use semantic controls, labels, keyboard navigation, focus management, and accessible error feedback; check narrow layouts and text scaling.

Scope caches by inputs affecting visibility, including user/tenant, permissions, locale, and query. Define invalidation/staleness and test cross-user isolation. Server rendering does not automatically make personalized cache entries safe.

Measure browser load/interaction, waterfalls, server latency, query counts, and payload size where relevant. Fix demonstrated N+1 access, serialization, or render costs before adding caches or memoization. Do not indiscriminately lazy-load primary content or critical imagery.

## Verification

Exercise the owning boundary with server authorization, API/database integration, component behavior, and selected end-to-end tests. Include direct requests bypassing the UI, session expiry, concurrent writes, and recovery when affected. Check deployed builds where rendering, cache, assets, or environments differ.

For Next.js security details, consult installed versions and [official data-security guidance](https://nextjs.org/docs/app/guides/data-security); exported server actions are externally callable endpoints.
