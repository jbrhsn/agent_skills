# Solidity and EVM contracts

Start with assets at risk, invariants, roles, compiler/EVM target, deployed storage, and external protocol assumptions. Use maintained, version-compatible libraries for established standards; library reuse does not prove the integration safe. Read [Web3](../web3/GUIDE.md) for signing and transaction lifecycle.

## Security and semantics

Differentiate permissionless entry points from privileged administration. Enforce the intended authorization and accounting on each operation; do not add owner-only restrictions to public token transfers or deposits.

Analyze reentrancy across functions/contracts, including callbacks and observable intermediate state. Apply checks-effects-interactions and suitable guards where they uphold the invariant. Validate external-call results and account for token behavior such as missing return values, transfer fees, rebasing, and callbacks.

For signatures, check domain/chain binding, nonces, expiry, and replay. Never use tx.origin for authorization. Consider oracle freshness, decimals, bounds, manipulation, rounding direction, slippage, and transaction ordering where relevant.

Bound user-driven loops and gas growth. Preserve events needed for accounting, governance, debugging, and indexing even when no current consumer is known.

## Changes and upgrades

Do not introduce proxies by default. For existing upgradeable contracts, verify storage compatibility, initializer/reinitializer behavior, implementation locking, and upgrade authority. Do not reorder deployed storage to save gas. Use the applicable validation tooling and [OpenZeppelin upgrade guidance](https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable); do not bypass storage checks.

Optimize gas using measurements under the project's compiler settings. Use unchecked arithmetic only with a demonstrated bound and invariant; brevity is not a proof. Identify governance and recovery limitations for irreversible changes.

## Verification

Test unauthorized administration and legitimate permissionless access, reverts, adversarial callbacks, boundary values, rounding, and state transitions. Use fuzz/property and invariant tests for asset/accounting properties, with harnesses exposing internal behavior as needed. Use pinned-block fork tests for external integration and deterministic fakes for adversarial failures.

Record compiler/optimizer versions, test evidence, gas changes when relevant, and security-review limitations. Passing tests is not an audit, and preparation does not authorize broadcasting deployments or upgrades.
