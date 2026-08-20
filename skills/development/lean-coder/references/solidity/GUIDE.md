# Solidity — Lean Rules

Brevity here is secondary to safety and gas. Never remove a check to save a line.

## Audited libraries first (never hand-roll)

| Need | Use | Not |
|---|---|---|
| Tokens | OpenZeppelin `ERC20`/`ERC721`/`ERC1155` | custom implementation |
| Access control | `Ownable`, `AccessControl` | your own role mapping |
| Reentrancy | `ReentrancyGuard` + checks-effects-interactions | custom mutex |
| Safe transfers | `SafeERC20` | raw `transfer` return value ignored |
| Signatures | `ECDSA`, `EIP712` | manual `ecrecover` |
| Merkle proofs | `MerkleProof` | hand-rolled hashing |
| Upgrades | UUPS proxy from OZ | bespoke delegatecall |
| Math | native checked arithmetic (0.8+) | SafeMath |

## Cut

- SafeMath on ^0.8 — arithmetic is checked by default
- Getters for `public` state variables (auto-generated)
- Custom `Ownable` reimplementations
- Events nobody indexes; keep the ones off-chain consumers actually read
- Redundant `require` re-checking a modifier's condition
- Storage variables that are only read once from an immutable value → `immutable`/`constant`

## Gas = lines saved twice

- `immutable` for constructor-set values, `constant` for literals.
- Pack storage into 32-byte slots; order struct fields by size.
- Cache storage reads in memory inside loops (`uint256 len = arr.length;`).
- `calldata` over `memory` for external function array/string params.
- `unchecked { ++i; }` in loops where overflow is impossible.
- Custom errors (`error Unauthorized();` + `revert`) over `require` strings.

## Security (never cut)

- Checks → Effects → Interactions, in that order, every function.
- Access control on every state-mutating external function; default deny.
- No unbounded loops over user-growable arrays — pull-over-push for payouts.
- Validate external call return values; assume any external contract is hostile.
- Never use `tx.origin` for auth; never use `block.timestamp` for randomness.
- Oracle prices: check staleness and bounds; use TWAP where spot is manipulable.
- Add a pause path only if you also add the access control and tests for it.

## Testability

- Keep logic in `internal pure`/`view` functions — those are directly unit-testable and fuzzable.
- Foundry: unit tests for happy path, `invariant_` tests for supply/balance conservation, fuzz tests on every numeric input.
- Test the revert, not just the success: `vm.expectRevert(Unauthorized.selector)`.
- Fork-test any integration with a live protocol; do not mock it.

## Example

```solidity
// after
error NotOwner();
function withdraw(uint256 amount) external {
    if (msg.sender != owner) revert NotOwner();
    balance -= amount;                       // effect
    (bool ok,) = msg.sender.call{value: amount}(""); // interaction
    require(ok);
}
```
