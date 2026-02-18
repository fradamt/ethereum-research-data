---
source: magicians
topic_id: 17828
title: "EIP 7587: Reserve Precompile Address range for RIPs/L2s"
author: CarlBeek
date: "2024-01-02"
category: EIPs > EIPs Meta
tags: []
url: https://ethereum-magicians.org/t/eip-7587-reserve-precompile-address-range-for-rips-l2s/17828
views: 1768
likes: 4
posts_count: 7
---

# EIP 7587: Reserve Precompile Address range for RIPs/L2s

This post is for discussion of [EIP 7587](https://github.com/ethereum/EIPs/pull/8074) wherein precompile addresses `0x100` to `0x1ff` are reserved for use by the RIP process as discussed in [ACDE 177](https://www.youtube.com/watch?v=7amkZxKobX4).

## Replies

**ulerdogan** (2024-01-02):

Thanks for preparing this EIP. My suggestion is to have a living proposal that can be organized for any future possible address reserve or registry needs (in case of the need for defining a new range), also including the native-L1 precompile range. So that reserved address management will be better defined and followable.

---

**CarlBeek** (2024-01-02):

Yes absolutely, expect an RIP for tracking RIP precompiles once we have this address range reserved

---

**ulerdogan** (2024-01-02):

It’s also nice, but I mean this proposal to keep track of all L1 registries like

- L1-native → 0x01…
- RIP → 0x100-0x1ff
- then, to be updated for any future need

---

**CarlBeek** (2024-01-02):

Aah, I see. I agree this would definitely be helpful, but not sure that an EIP is necessarily the right place to track it. Personally, I use https://www.evm.codes/precompiled for checking this for L1.

---

**dror** (2024-03-25):

One thing that is currently missing from this EIP, is the “pureness” of the called precompile.

Most existing precompiles are “pure”, in the sense that they only read from memory or stack, and return their result on the stack - but nothing prevents precompiles to depend or modify the state.

My suggestion is to split the range, and have an explicit range for such “pure” precompiles.

### The reasoning:

In ERC-7562 we define validation rules for account-abstraction, which forbids state-dependency during validation.

We explicitly allow precompiles 1-9, since they are all known to be “pure”, and forbid other precompiles, since we can’t tell if they depend on the state or not.

With new RIPs (eg, RIP-7212), we need to update the rules to allow this precompile

Instead, it would be best if we could depend on the precompile address range, to know this has to be a pure code (for the validation rule, we don’t care if the precompile actually does anything: we only need to assert that it is consistent when called using off-chain `eth_call` and on-chain, and doesn’t depend on storage - which is exactly the definition of `pure`/

---

**CarlBeek** (2024-04-01):

I think this is a really important point to bring up and the idea of having a sub-range reserved for dedicated L2 stateful precompiles makes sense. That said, I think this should be a separate RIP as it only concerns RollUps and would be a subset of this EIP.

