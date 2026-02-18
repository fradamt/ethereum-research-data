---
source: magicians
topic_id: 27619
title: "Hegotá Headliner Proposal: SSZ execution blocks"
author: etan-status
date: "2026-01-29"
category: Magicians
tags: [hegota, headliner-proposal]
url: https://ethereum-magicians.org/t/hegota-headliner-proposal-ssz-execution-blocks/27619
views: 124
likes: 4
posts_count: 2
---

# Hegotá Headliner Proposal: SSZ execution blocks

[EIP-7807: SSZ execution blocks](https://eips.ethereum.org/EIPS/eip-7807) proposes to change most of Ethereum’s EL data structures to be based on [Simple Serialize (SSZ)](https://github.com/ethereum/consensus-specs/blob/master/ssz/simple-serialize.md).

## Summary

- Add SSZ library to EL: Basic impl, with progressive type extensions EIP-7916, EIP-7495, EIP-8016
- Hash transactions, receipts, withdrawals, and block hash with SSZ instead of RLP when building blocks
- Binary engine API to access EL data via SSZ
- EIP-6493 Native SSZ transactions as a platform to build new transaction / signature types on (only as headliner)
- Out of scope: Log revamps, EL state trie.

## Primary benefits

- Typed signatures: Signature types can evolve independently of transaction types, providing a straight-forward avenue towards PQ signatures.
- Tree-based hashes: Replacing flat hashes with binary Merkle trees enables proofs of partial data, e.g., for just the first chunk of calldata that contains the function signature.
- Binary API: Switching to SSZ allows reuse of a canonical binary REST API inspired by beacon-APIs. This also reduces latency for data format conversion on the engine API.

## Secondary benefits

- Forward compatibility: Common transaction / receipt fields share the same relative location in the Merkle tree across all transaction types. Smart contracts consuming them need less maintenance.
- Metadata verifiability: Sender address, deployed contract address, and per-transaction gas used, are hashed into the receipt, reducing round trips to obtain common data, and simplifying RPC server design.
- Simpler sync: CL no longer needs RLP / MPT support for optimistically syncing without an EL during maintenance. ELs no longer need to verify blob KZG commitments and block hashes on behalf of the CL. EL no longer needs a separate SSZ library for syncing beacon block headers (light client protocol).

## Why now?

- Dependent EIPs: EIPs that add new transaction / signature types benefit from having SSZ from the getgo. Further, this is another step towards the verifiable log filter (EIP-7745) proposal.
- Future plans: Doing this EIP now is in line with proposals that enshrine a specific transaction serialization (e.g., native rollups, FOCIL), needs efficient and verifiable data structures (e.g., lean Ethereum), or benefits from simpler reasoning (e.g., max block size discussions).
- Scaling needs: The JSON based engine API starts to become a relevant bottleneck as the number of blobs increases and block data grows bigger (e.g., BALs)

## Alternative solutions

- This headliner would combine well with a transaction type headliner based on the native SSZ transactions platform (EIP-6493). The new transaction type would be built on top of the new platform and provide immediate validation of the design.
- The scope could be reduced to non-headliner by doing just the hashing changes (i.e., transactions_root, receipts_root, withdrawals_root, and block_hash). Potentially complex updates to database, network, and internal logic no longer has to be synced across implementations. However, EIP-6493 may have to be deferred as it adds new functionality instead of just revamping an existing hash.

## Stakeholder impact

- Positive: Verifying applications and smart contracts, transaction EIP authors
- Negative: Daunting database / network protocol changes

## Technical readiness

Prototypes in EthereumJS and NimbusEL (epf). [devnet 0](https://hackmd.io/@razorclient/BJCT0WlIbe) sketch.

EIP overall structure ready, details subject to change.

## Replies

**etan-status** (2026-01-29):

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/1/a/1a25e800824b78dba3c7da82fbd431e61f59197a_2_690x445.jpeg)image1920×1241 187 KB](https://ethereum-magicians.org/uploads/default/1a25e800824b78dba3c7da82fbd431e61f59197a)

