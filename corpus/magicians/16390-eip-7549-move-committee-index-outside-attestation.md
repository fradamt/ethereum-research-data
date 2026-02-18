---
source: magicians
topic_id: 16390
title: "EIP-7549: Move committee index outside Attestation"
author: dapplion
date: "2023-11-01"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7549-move-committee-index-outside-attestation/16390
views: 2084
likes: 2
posts_count: 5
---

# EIP-7549: Move committee index outside Attestation

Discussion thread for EIP-7549: Move committee index outside Attestation

https://github.com/ethereum/EIPs/pull/7944

## Replies

**etan-status** (2024-04-29):

Implementing this has proven to be nontrivial in some clients. Would be best to reevaluate inclusion based on that hidden implementation complexity. From my understanding, we gain some potential gains for future ZK snarks that are currently under research. Personally I’d prefer completing that research on a custom branch before applying all of the necessary changes in one go, over introducing some change in a hasty way before it produces benefits. Prior to ZK snarks, do we gain something substantial from this EIP alone?

Besides implementation complexity due to new data types, the initial fork transition also needs to be revisited (that changes from one attestation type to the new one).

Furthermore, as the data type is broken, [EIP-7495](https://eips.ethereum.org/EIPS/eip-7495) style StableContainer could also be considered so that breakage isn’t repeated every time new data type gets introduced. That would also allow dropping the now unused (and always set to 0) `index` field of the new attestation type. Consider impact for trust-minimized consumers of CL data such as decentralized staking pools, i.e., [EIP-7688](https://github.com/ethereum/EIPs/pull/8439/files).

---

**etan-status** (2024-04-29):

Another aspect to consider is impact on web3signer / hardware signers / validator client API.

---

**tbenr** (2024-05-22):

From my experience implementing it, the complexity was in:

- swapping attestation type trying to reduce the impact as much as possible (attestation type is everywhere in the code base and has never being changed)
- In particular, the attestation pool together with aggregation logic requires to swap to a different comparison\aggregation algorithm that now requires the knowledge of committee sizes (for teku not easily accessible from the pool in all cases)
- new validator API v2 required on probably several APIs (should we introduce versioning in the payload?) while I don’t think web3signer is impacted.
- complexity at fork activation, with two different attestation types being relevant at the same time. (we decide the “do nothing” approach and drop the old type)

a side note:

- leaving the index in attestationData and set it to 0, while is a great idea for compatibility, leave the door open for several bugs (you can easily leave traces in your codebase that refer to it, so you’ll consider the wrong committee index).

---

**poojaranjan** (2024-07-01):

To learn more about  [EIP-7549: Move committee index outside Attestation](https://youtu.be/oZfV4Ell9WQ), follow the talk with [@dapplion](/u/dapplion) on [PEEPanEIP](https://www.youtube.com/playlist?list=PL4cwHXAawZxqu0PKKyMzG_3BJV_xZTi1F)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/1/169348ad4bec5d1142b8f6266bd0d95a69bd587c.jpeg)](https://www.youtube.com/watch?v=oZfV4Ell9WQ)

