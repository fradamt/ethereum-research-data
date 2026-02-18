---
source: magicians
topic_id: 22826
title: "RIP-7876: Canonical ERC-7802 token bridge address"
author: yoavw
date: "2025-02-11"
category: RIPs
tags: []
url: https://ethereum-magicians.org/t/rip-7876-canonical-erc-7802-token-bridge-address/22826
views: 95
likes: 1
posts_count: 1
---

# RIP-7876: Canonical ERC-7802 token bridge address

[RIP-7876](https://github.com/ethereum/RIPs/pull/59) sets a standard address for the ERC-7802 token bridge address trusted by ERC-20 tokens that support ERC-7802 Crosschain minting/burning.

[ERC-7802](https://ethereum-magicians.org/t/erc-7802-crosschain-token-interface/21508) proposed a minimal interface for crosschain minting/burning of ERC-20 tokens. The token is requires to trust a bridge address and allow it to call `crosschainMint`/`crosschainBurn`. The bridge address would typically be immutable and affect the token’s address as determined by CREATE2.

[EIP-7587](https://eips.ethereum.org/EIPS/eip-7587) reserved a range for standardized precompiles/predeploys used by rollups. The proposal makes use of this range to reserve the token bridge address.

By standardizing the bridge address we gain two advantages:

1. Tokens can be deployed in a future-proof manner on every chain. If/when a rollup adds native ERC-7802 capability to their canonical bridge, existing immutable tokens can benefit from the improved interoperability even though they were deployed earlier.
2. Tokens can deploy to the same CREATE2 address if they wish. Having the same bridge address means they don’t need to pass a different argument during deployment.

We propose that rollups that implement a native ERC-7802 bridge will use this standard address to help token devs with interop and avoid fragmentation.
