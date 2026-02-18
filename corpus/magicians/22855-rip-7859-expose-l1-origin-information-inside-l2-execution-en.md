---
source: magicians
topic_id: 22855
title: "RIP-7859: Expose L1 origin information inside L2 execution environment"
author: i-norden
date: "2025-02-13"
category: RIPs
tags: []
url: https://ethereum-magicians.org/t/rip-7859-expose-l1-origin-information-inside-l2-execution-environment/22855
views: 303
likes: 11
posts_count: 7
---

# RIP-7859: Expose L1 origin information inside L2 execution environment

This proposal defines a contract interface for exposing inside the L2 execution environment information about the L1 block that the L2 most recently included bridge inputs from- the so-called “L1 origin”.

This view is useful to any contract on the L2 that needs to verify arbitrary L1 state, storage, transaction, or receipt data inside the L2. It can be used for verification in cross-L2 communication such as RIP-7755, for enforcing L2 consistency checks such as RIP-7789,

and for verifying reads from the L1 such as RIP-7728 and ERC-3668.

This proposal includes an interface for exposing L1 origin info and invariants rules on the meaning of that L1 origin but does not prescribe a specific underlying implementation. The goal is to be able to support a common interface across rollups with differences in implementations.

Link to the latest PR:



      [github.com/ethereum/RIPs](https://github.com/ethereum/RIPs/pull/57)














####


      `ethereum:master` ← `polymerdao:ian/expose_l1_info`




          opened 12:59AM - 29 Jan 25 UTC



          [![i-norden](https://avatars.githubusercontent.com/u/28617060?v=4)
            i-norden](https://github.com/i-norden)



          [+140
            -334](https://github.com/ethereum/RIPs/pull/57/files)







This is an update to RIP-7859 that performs a major overhaul in light of @tynes'[…](https://github.com/ethereum/RIPs/pull/57) comment [here](https://github.com/ethereum/RIPs/pull/52#issuecomment-2591619509). This RIP now defines the interface for accessing L1 info and rules for the meaning of L1 info, rather than stipulating a specific underling EIP-4788-like ring buffer implementation.

EIP-2935 portions of this RIP have largely been removed as I believe

1. We can use the existing EIP-2935 spec or write a new RIP for it if needed
2. Usage of EIP-2935 as envision in the original state of this RIP is more implementation detail reliant- we want to standardize the storage layout for consistent usage when verifying proofs through the L2 outputs on the L1.
3. It makes this RIP cleaner

## Replies

**jackchuma** (2025-03-20):

I would absolutely love to see this adopted - nice job! Do you think there’s merit in generalizing the interface to reference a “parent chain” instead of specifying “L1”? As we end up with L3s and beyond, it would be useful to allow higher level chains to adopt this as well. Or if trying to also leave support for directly accessing L1 block data from within an L3, maybe a “layer” parameter could be worked into the interface to keep it simple.

Also, tiny nit but the interface has a return value with the wrong name

```diff
- function getL1OriginParentBeaconRoot() external view returns (bytes32 blockHash);
+ function getL1OriginParentBeaconRoot() external view returns (bytes32 beaconRoot);
```

---

**i-norden** (2025-04-01):

Yeah I think it is a good idea to generalize it to a parent-child relationship vs L1-L2! The intent is definitely for this to be supported at higher layers.

Directly supporting views of lower-than-parent layers is a good idea too, since it would make it cheaper to verify claims of those layers’ state vs the current approach where you need to e.g. use the L2 view inside the L3 to prove the L1 view inside the L2. This will complicate things a little bit for a L3+ sequencer as they will need to perform some introspection into their parent layer to (recursively, if we get to L4+) extract information about the lower layers’ “origins”.

Thanks for catching the interface typo. Will make a PR to fix that and switch to using the parent-child naming. I will give some more thought on how best to support lower layer views and I’m curious what your opinion is on the tradeoff there.

---

**dipkakwani** (2025-04-16):

We have implemented PoC for this RIP in the rollup-geth project: [Rip 7859: Store L1 Origin Information by dipkakwani · Pull Request #30 · NethermindEth/rollup-geth · GitHub](https://github.com/NethermindEth/rollup-geth/pull/30) Any feedback regarding the implementation is welcome ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

More about rollup-geth here: [Introducing rollup-geth](https://ethereum-magicians.org/t/introducing-rollup-geth/21458)

---

**i-norden** (2025-04-21):

This is great! Can we reference this from the RIP as an example implementation?

---

**dipkakwani** (2025-04-22):

Yes sure, please feel to reference the PR!

---

**thnhnv** (2025-06-06):

Great proposal!

But quick questions: Does RIP-7859 expose more data (state root, transaction root, receipt root) than needed? What are the tradeoffs? Verification will be cheaper but L2 nodes must store more data than needed.

