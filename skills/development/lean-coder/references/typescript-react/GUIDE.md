# TypeScript / React / Next.js — Lean Rules

## Platform first (do not npm install for these)

| Need | Use | Not |
|---|---|---|
| HTTP | `fetch` | axios |
| Dates | `Intl.DateTimeFormat`, `Temporal` where available | moment, date-fns for one format |
| IDs | `crypto.randomUUID()` | uuid |
| Deep clone | `structuredClone` | lodash.clonedeep |
| Grouping | `Object.groupBy` / `Map` | lodash.groupby |
| Query params | `URLSearchParams` | qs |
| Debounce | `AbortController` + `setTimeout` (6 lines) | lodash.debounce |
| Validation | one `zod` schema shared by type + runtime | separate interface and validator |
| State | `useState`, `useReducer`, URL params | Redux for <10 pieces of state |
| Forms | uncontrolled inputs + `FormData` | form library for 3 fields |

## React

- Derive, don't store: if it can be computed from props/state during render, do not put it in `useState`.
- `useEffect` is for external synchronization only. Not for computing values, not for reacting to prop changes, not for fetching in an app that has server components or a data library.
- No `useMemo`/`useCallback` until a profiler says so. Each one is 2 lines and a dependency array to get wrong.
- One component = one concern. Split when JSX branches on a boolean prop into two different shapes.
- Server Components / server actions by default in Next.js; `"use client"` only on the leaf that needs interactivity.
- Colocate: component, its types, and its test in one folder; no shared `types.ts` dumping ground.
- Error boundaries per independently-failing region (a widget, a route segment) — not one global catch-all that blanks the whole page. In Next.js, use `error.tsx`/`loading.tsx` at the route segment instead of hand-rolled `isError`/`isLoading` state.
- Suspense for async boundaries the framework already understands (data fetching, lazy components) instead of manual loading flags layered on top.
- Lazy/dynamic import (`next/dynamic`, `React.lazy`) for below-the-fold or rarely-used components; don't ship code the initial render never touches.
- `next/image` or native `loading="lazy"` over an unmanaged `<img>`; avoid passing new object/array/function literals as props on every render where it causes a measurable re-render cascade downstream.

## Accessibility (never cut)

- Semantic HTML elements (`button`, `nav`, `label`) over `div`+ARIA — ARIA is a patch for when semantics run out, not the default.
- Every form input has an associated `label`; every interactive element is reachable and operable by keyboard alone.
- Images carry meaningful `alt` text (or `alt=""` when purely decorative) — never omit the attribute.

## TypeScript

- Infer return types; annotate only exported signatures and empty containers.
- `type` unions over `enum`. Discriminated unions over optional-field soup.
- `unknown` at boundaries, narrowed once — never `any`, never `as` to silence an error.
- Derive types (`Pick`, `Awaited<ReturnType<typeof f>>`) instead of restating shapes.

## Cut

- `index.ts` barrel files that only re-export
- Interfaces implemented once
- Try/catch that only `console.error`s
- Prop drilling wrappers that pass everything through
- `useState(false)` for a value only read in an event handler
- Class components; `React.FC`; `PropTypes`

## Security (never cut)

- Never `dangerouslySetInnerHTML` on user content; if unavoidable, sanitize first.
- Secrets are server-only. Anything in `NEXT_PUBLIC_*` is published — treat it as such.
- Validate request bodies with the shared schema in every route handler and server action; a server action is a public endpoint.
- Authorize inside the action/handler, not in the component that renders the button.
- Escape/parameterize DB queries; no template-literal SQL.
- `rel="noopener noreferrer"` on `target="_blank"`; set CSP headers.

## Testability

- Pure functions in `lib/`, components that only render props → test the logic without a DOM.
- Test through the accessible interface (`getByRole`, user events), not implementation details or snapshots.
- MSW at the network boundary rather than mocking `fetch` per call site.
- If a component needs 3 providers to render in a test, it is doing 3 jobs.

## Example

```tsx
// before — 12 lines: state + effect + memo
// after — 2
const visible = items.filter(i => i.name.includes(query));
return <ul>{visible.map(i => <li key={i.id}>{i.name}</li>)}</ul>;
```
