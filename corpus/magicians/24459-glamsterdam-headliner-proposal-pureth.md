---
source: magicians
topic_id: 24459
title: "Glamsterdam headliner proposal: Pureth"
author: etan-status
date: "2025-06-05"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/glamsterdam-headliner-proposal-pureth/24459
views: 430
likes: 9
posts_count: 2
---

# Glamsterdam headliner proposal: Pureth

## Summary

[EIP-7919: Pureth](https://eips.ethereum.org/EIPS/eip-7919) bundles a set of improvements to make Ethereum data easier to access and verify without relying on trusted RPC providers or third-party indexers. The improvements achieve this by changing data structures for blocks, transactions, and receipts, so that efficient correctness (i.e., validity) and completion (i.e., nothing omitted) proofs can be added to the RPC responses.

The ability to verify RPC responses is essential for security. Today, most wallets and dApps consume data from very few large RPC providers, which exposes users to the risk of incorrect and incomplete data in case the RPC provider gets hacked, becomes malicious, or uses a faulty software version. This may trick a user into authorizing a fraudulent transaction. Further, centralized infrastructure is subject to external data collection and privacy policies; users may be profiled across distinct wallets even when there is no on-chain link between them. And external indexers can be quite costly, reducing reliance on them helps lower-funded developers.

The opportunity of the data structure revamp is also used to switch from flat (linear) hashes to tree-based hashes, allowing more compact proofs when only interested in partial data. For example, proving an individual log may reduce gas cost compared to proving the entire receipt, which benefits smart contracts and L2 bridges. Finally, forward compatibility is achieved; verifiers no longer require updates when unrelated Ethereum features change. This has been requested by staking pools (Lido, RocketPool) which already consume tree-based data from the beacon chain today.

Together, these changes lay the foundation for a trust-minimized, privacy-preserving, and cost-efficient data access infrastructure for Ethereum.

## Detailed Justification

### Primary benefits

- Verifiable RPC data: Light clients can verify correctness and completeness of RPC responses, allowing them to use any provider, not just trusted ones. This improves security (prevents fraudulent UI state), privacy (avoids request profiling), and censorship resistance (e.g., geoblocking). This also enables fast, trustless indexing in decentralized archive node networks, significantly reducing access latency.
- Lower indexing cost: All ETH transfers emit logs, reducing reliance on third-party indexers. Logs become provable (i.e., no omission) and significantly faster to retrieve. Geth already implements an early version of the new log structure.
- Tree-based hashes: Replacing flat hashes with SSZ trees enables partial proofs (e.g., a single log instead of full receipt), reducing calldata size and gas cost for bridges, on-chain verifiers, and L2s.

### Secondary benefits

- Forward compatibility: SSZ StableContainer and ProgressiveList ensure data remains at fixed generalized index across forks. Unless semantics change, verifiers become stable across protocol upgrades (e.g., Lido, RocketPool).
- Transaction profiles: SSZ-based transaction structures enable extensions for new features (e.g., calldata fee, post-quantum signatures) without creating new transaction types. This avoids repeated verifier breakage.
- Unified serialization: Using SSZ across execution and consensus layers simplifies client tooling, improves performance (e.g., binary engine API), and reduces complexity of future upgrades. For example, even efforts that seem unrelated, such as blob scaling, benefit from an engine API with lower latency.

### Why now?

- L2 interoperability: An efficient proving system also benefits L2s, as they eventually adopt L1 improvements over time. Efficient, privacy-preserving access to L2 data via standard RPC is a key unlock for decentralized applications.
- SSZ maturity: SSZ is already battle-tested in the consensus layer. Introducing it in the execution layer now avoids further proliferation of RLP / MPT legacy code. This is supported by Vitalik’s purge and simplification roadmaps.
- Relevant in a zk future: Post zk, we will still need indices and data structures that can be proven efficiently. The log index commitment may move from the block header to a side car, but the actual index itself must persist. Laying the groundwork now simplifies the zk transition as the UX improvement unlocks can be inherited.

### Alternative solutions

- EIP-1186: eth_getProof only supports state proofs and is not supported by all providers. This endpoint cannot be used for proving historical data such as logs, transactions, receipts, and validator operations. Further, exhaustively proving ETH balance changes pertaining to one’s wallet still requires an external indexer.
- Ship log index now, SSZ later: The log index is the biggest immediate unlock. Implementing it now using RLP and custom hashing schema, only to migrate to SSZ later, is wasteful. This is a rare opportunity for a clean data structure revamp centered around provable RPC.
- Just use trusted RPC: Contradicts Ethereum’s core values.

## Stakeholder Impact

- Positive: There is active demand from products close to users, including Web3 purifiers (a16z/helios, Nimbus), staking pools (Lido, Rocket Pool), wallets, dApps, and L2s. All benefit from verifiable, privacy-preserving, and forward-compatible access to Ethereum data.
- Negative: Ethereum core developers may not benefit directly from these changes, but carry the cost of implementation and maintenance. Simplicity and forward compatibility should be prioritized in future proposals to preserve provable RPC properties.
- Technical Readiness: The current status is tracked at purified-web3.box. A single-node devnet (based on Nimbus + EthereumJS) is available, focusing on SSZ support (log index not yet integrated). Geth has implemented the 2D log index structure, but the prover is still in progress. BootNode has built a demo client based on Helios, although log querying is blocked due to the missing prover. Most specs are complete, though certain refinements are pending (e.g., reducing SSZ hash count in StableContainer and lists). SSZ and consensus layer tests are mostly complete, execution layer tests are still largely missing.
- Security & Open Questions: These EIPs significantly improve user-facing security. RPC data (transactions, receipts, logs) can be independently verified using standard Merkle proofs.

## Replies

**metony** (2025-07-15):

**I’m fully in favor of this headliner proposal**. It’s not just because it includes EIP-7708 (I’m excited about solving the problem of tracking ETH transfers) – it’s because *the whole package* will make Ethereum’s on-chain data much more accessible and trustless for everyone. Here are the key reasons why I support it:

- Easier tracking of ETH transfers: Today, it’s nearly impossible to track all native ETH movements without running a full trace on every transaction (a nightmare for wallets and dApps). With EIP-770, every ETH transfer will emit a log event, just like token transfers do.
- Trustless, verifiable data access: So light clients and apps can verify the data they get from any RPC provider.
- Modern, future-proof data structures: Upgrades Ethereum’s under-the-hood format to use tree-based (SSZ) structures instead of the old flat hashing. It means we can prove or retrieve just a piece of data (say, one log or part of a transaction) without hauling in an entire block or receipt.

