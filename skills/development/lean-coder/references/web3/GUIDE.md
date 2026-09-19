# Web3 integrations

Use for wallets, RPC, submission, signing, indexing, and on-chain/off-chain workflows. Add Solidity for EVM contracts or Rust plus chain-specific official guidance for Rust programs. Do not transfer one chain's account, finality, or execution assumptions to another.

## Identity and authorization

Bind requests to intended chain, account, contract/program, asset, and units. Wallet connection is not authentication. Signed challenges need domain separation, nonce, expiry, intended action, and replay protection; support the chain's verification paths, including contract wallets where applicable.

Protect private keys, seed phrases, signing services, RPC credentials, and approvals. Keep custody secrets out of clients and logs. Match transaction targets and approval amounts to user intent; simulation neither authorizes broadcast nor guarantees execution.

## Transaction lifecycle

Distinguish prepared, awaiting signature, rejected, submitted, pending, included, failed, replaced/dropped, and sufficiently finalized states as applicable. A hash is not success. Resolve ambiguous submission before resending; an RPC timeout may follow acceptance.

Coordinate nonce/sequence management under concurrency. Handle account/network switching and stale estimates. Use integer/base-unit arithmetic with explicit decimals and rounding for balances and financial calculations.

## External state

Track chain identity, block height/hash, event identity, and finality assumptions. Detect reorgs and reconcile affected derived state with idempotent ingestion and bounded replay. Handle RPC limits, lag, pagination, reconnect gaps, and malformed responses.

Consider oracle freshness/decimals/manipulation, MEV, slippage/deadlines, fees, and external token/program semantics where relevant. A healthy RPC does not prove indexed data is current.

## Verification and release

Use deterministic local-chain tests and pinned-height fork/integration tests for external protocols. Record chain IDs, blocks, ABI/program versions, compiler settings, and addresses needed to reproduce results. Test rejection, revert, duplicate submission, replacement, stale data, and reorg recovery when relevant.

For deployment, upgrades, or fund movement, prepare reviewable targets, parameters, simulations, permissions, and recovery plans within existing authorization. Automated tests and analysis are evidence, not an independent security audit.
