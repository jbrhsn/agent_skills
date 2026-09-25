# Lean decision examples

Use when a design or verification choice is ambiguous. These examples illustrate decisions, not mandatory architectures or size limits.

| Situation | Decision and reason |
|---|---|
| A one-use `canRefund` helper expresses eligibility rules | Keep it if the name and boundary make the rule easier to understand or test. One caller does not make it wasteful. |
| A new helper only forwards unchanged arguments to an existing function | Call the existing function directly unless the wrapper supplies a concrete public contract, lifecycle boundary, or useful substitution point. |
| Two handlers contain similar code, but their authorization or failure rules differ | Keep their policies distinct. Share a transformation only if its semantics are genuinely common; avoid a flag-heavy universal handler. |
| A new interface or plugin registry serves only hypothetical future backends | Use the current concrete implementation unless an actual contract requires the indirection. Extend when requirements arrive. |
| A standard library can format the required timestamp correctly | Use it after checking version, timezone, and output-contract requirements; adding a package has no demonstrated benefit. |
| Safe rich-HTML handling needs a sanitizer | Reuse a suitable maintained sanitizer. A short regex or custom parser does not replace its security guarantees. |
| Existing code uses a maintained HTTP client | Reuse it when suitable; replacing it with a standard-library client solely to remove a dependency may discard configured authentication, pooling, deadlines, or retry behavior. |
| Duplicate records arise from concurrent requests | Exercise the real datastore constraint or transaction with concurrent attempts. A mocked repository that always succeeds cannot establish the guarantee. |
| A pure formatter mishandles an empty value | Add a focused input/output regression check and run relevant project checks. A load test or new end-to-end harness adds no evidence for this defect. |

Before retaining a new abstraction or dependency, be able to name the current behavior, contract, or operational need it serves. Prefer the clearer implementation when alternatives meet the same requirements; fewer lines are useful only if they also reduce maintenance work.
