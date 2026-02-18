---
source: magicians
topic_id: 23517
title: System level transactions and bypassing EVM execution
author: OlivierBBB
date: "2025-04-13"
category: EIPs
tags: [evm]
url: https://ethereum-magicians.org/t/system-level-transactions-and-bypassing-evm-execution/23517
views: 59
likes: 0
posts_count: 1
---

# System level transactions and bypassing EVM execution

AFAICT there are currently two system transaction EIPs

- EIP-4788: Beacon block root in the EVM (Cancun)
- EIP-2935: Serve historical block hashes from state (Prague, as of https://notes.ethereum.org/@ethpandaops/pectra-devnet-6)

Both feature a note about how execution clients may bypass EVM execution. From the [Block processing section of EIP 2935](https://eips.ethereum.org/EIPS/eip-2935#block-processing):

> Note: Alternatively clients can choose to directly write to the storage of the contract but EVM calling the contract remains preferred. Refer to the rationale for more info.

and from the [Block processing section of EIP 4788](https://eips.ethereum.org/EIPS/eip-4788#block-processing):

> Clients may decide to omit an explicit EVM call and directly set the storage values. Note: While this is a valid optimization for Ethereum mainnet, it could be problematic on non-mainnet situations in case a different contract is used.

It is of note that the set of authors of these two EIPs are disjoint.

---

I have some related questions:

1. Is there an explicitly spelled out expectation that with future system level transactions EIPs clients should also be able to bypass EVM execution, as they are currently ?
2. Is there an explicitly spelled out expectation that future system future level transactions should also be executed before (standard) transaction processing ?

I would also be curious to find out if there are more system level transaction EIPs in the works besides the two I cite. Thank you.
