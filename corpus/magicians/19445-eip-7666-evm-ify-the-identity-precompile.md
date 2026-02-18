---
source: magicians
topic_id: 19445
title: "EIP-7666: EVM-ify the identity precompile"
author: vbuterin
date: "2024-03-31"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7666-evm-ify-the-identity-precompile/19445
views: 1262
likes: 5
posts_count: 3
---

# EIP-7666: EVM-ify the identity precompile

Remove the identity precompile at 0x04. At the start of executing the block in which this change activates, put into that contract a short piece of EVM code that has the same functionality.

https://github.com/ethereum/EIPs/pull/8366

## Replies

**jochem-brouwer** (2025-01-17):

> Gas costs are slightly different, though gas repricings have been done in the Ethereum ecosystem several times before and their effects are well understood.

I think “gas costs are slightly different” is a bit of a shortcut here. The identity precompile has linear gas costs, while the proposed bytecode is definitely quadratic since it dumps the calldata in memory. So, for larger inputs, the gas cost is definitely different and also scales differently.

[EIP-3855: PUSH0 instruction](https://eips.ethereum.org/EIPS/eip-3855) (PUSH0) should be added to required EIPs, otherwise the bytecode will run into INVALID opcodes.

> Starting from and including that block, IDENTITY_PRECOMPILE_ADDRESS should no longer be treated as a precompile.

Interesting point, this removes it from the “always warm addresses” for EIP-2929 gas accounting. Also, EIP-7702 accounts pointed to this precompile, should now thus run the bytecode instead of treating it as an account with no code.

---

**jochem-brouwer** (2025-04-20):

Can this mini-update for correctness be merged? [@vbuterin](/u/vbuterin) [Update EIP-7666: Add required PUSH0 EIP by jochem-brouwer · Pull Request #9165 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9165)

