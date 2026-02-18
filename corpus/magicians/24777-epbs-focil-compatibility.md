---
source: magicians
topic_id: 24777
title: ePBS 🤝 FOCIL compatibility
author: soispoke
date: "2025-07-10"
category: Magicians
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/epbs-focil-compatibility/24777
views: 582
likes: 9
posts_count: 1
---

# ePBS 🤝 FOCIL compatibility

by [Thomas Thiery](https://x.com/soispoke), July 10th 2025

*Thanks to [Julian](https://x.com/_julianma), [Terence](https://x.com/terencechain), [Anders](https://x.com/weboftrees), [Caspar](https://x.com/casparschwa) and [Potuz](https://x.com/potuz_eth) for their feedback and comments on this post.*

## Mechanism overview

In this short note, we demonstrate that **ePBS** ([EIP-7732](https://eips.ethereum.org/EIPS/eip-7732)) and **FOCIL** ([EIP-7805](https://eips.ethereum.org/EIPS/eip-7805)) can be integrated without conflict. We highlight the key design considerations for ensuring their compatibility in practice.

> #### Brief reminder.
>
>
>
> ePBS enables slot pipelining, effectively increasing time dedicated to execute and propagate the execution payload and blobs in any given slot.
> FOCIL improves censorship resistance by allowing multiple validators to force include specific transactions in each block.

Although both proposals introduce significant changes to the slot structure, we show that their interaction presents no conflicts *provided that inclusion lists (ILs) do not have to be built on the latest head to be considered valid*.

Here’s a diagram illustrating what the slot anatomy would look like in a world post ePBS ![:handshake:](https://ethereum-magicians.org/images/emoji/twitter/handshake.png?v=15) FOCIL.

![Screenshot 2025-07-09 at 16.57.32](https://hackmd.io/_uploads/BJLF-f3Bxl.png)

> Slot N-1:
>
>
> Includers build and broadcast ILs on the consensus layer (CL) p2p network. Towards the end of the slot, attesters of slot N freeze their views and stop storing new ILs.
> A couple of seconds later, the builder also stops storing new ILs, and updates its execution payload to make sure it satisfies IL conditions (i.e., the union of transactions across all ILs are included in the payload, unless the block is full).

> Slot N:
>
>
> The proposer runs its fork-choice rule to determine the valid parent block to build on, which incorporates the PTC vote outcome for the slot N-1 payload. It then selects and broadcasts a beacon block from a builder, depending on:
>
> The value specified in the PayloadHeader (the builder’s bid).
> Whether the IL bitlist includes all ILs seen by the proposer until its IL freeze deadline.
>
>
> Attesters then vote for the beacon block N only if all of the following conditions are met:
>
> The block builds on a valid head according to the attester’s view of the fork-choice rule. This rule incorporates the Payload Timeliness Committee (PTC) votes from slot N-1, which determined whether the payload N-1 was made available on time.
> The  payload for slot N-1 satisfied its own IL conditions. If the payload from slot N-1 was not compliant (e.g., did not include valid IL transactions in its block), attesters of slot N will not vote for block N to reorg of the non-compliant  payload N-1.
> The IL bitlist in the block include all ILs the attester was aware of at its own IL freeze deadline (this check could instead be done by the PTC, see more in the Split enforcement section below).
>
>
> The builder reveals its full Payload N (e.g., a builder could choose to reveal, for example, after having seen enough attestations for the beacon block including its PayloadHeader)
> The PTC votes for Payload N if made available on time by the builder.

## Overlap between ePBS and FOCIL duties

Now let’s look at how protocol duties overlap between ones that already exist today (even if modified in their timing or exact nature), ones introduced by ePBS and ones introduced by FOCIL.

![Screenshot 2025-07-09 at 16.25.03](https://hackmd.io/_uploads/B1VeqZnHle.png)

### Order Independence

The most important point to begin with is that the exact order in which FOCIL and ePBS duties occur is not crucial. This is mainly because we don’t require ILs to be built on the canonical latest head of the chain to be considered enforceable. In other words, even if an includer builds its IL using an outdated or incorrect head, IL transactions must still be considered for inclusion by the builder. So it’s fine if this leads to some IL transactions becoming invalid due to having been previously included. Of course, we should still aim to optimize for situations in which includers have seen the latest payload so they can build ILs with up-to-date, relevant transactions.

What is most likely to happen is that the local IL freeze deadline will happen after the builder releases its payload, but before the PTC vote. If that’s indeed the case, ILs should be built by prioritizing transactions not seen in the latest available payload according to their local view. Otherwise, includers should just run `get_head` and build and release their ILs based on the node’s local head.

### Split IL enforcement

Another important consideration is determining who should enforce that IL conditions are satisfied.

> A brief reminder of how FOCIL achieves this without ePBS: Attesters for slot N+1 verify whether all transactions from their stored ILs are included in the proposer’s execution payload, except for ILs whose sender has equivocated. Based on their frozen view of ILs from the previous slot, attesters check whether the execution payload satisfies IL conditions. They do this either by confirming that all transactions are present or by determining if any missing transactions would become invalid if appended to the end of the payload.

Instead, we can require builders to include and commit to an `IL bitlist` in their blocks, explicitly indicating which ILs were considered when constructing their payload. This allows proposers to select blocks based on the `IL bitlist` inclusivity (i.e., whether the builder’s `IL bitlist` covers all ILs stored by the proposer before the freeze deadline).

Interestingly, **attesters** or **the PTC** of `slot N` can also condition their votes on `IL bitlist` inclusivity. Their votes provide an early signal to the proposer regarding whether the builder’s payload considers all ILs known before the deadline.

1. Using attesters of slot N:
Attesters verify whether the IL bitlist matches their local frozen view before attesting. The primary advantage is that it leverages the entire beacon committee, but it means a beacon block can be reorged because it fails to satisfy the IL bitlist inclusivity check.
2. Using the PTC of slot N:
Alternatively, the PTC can perform the IL bitlist inclusivity check. This approach creates a cleaner abstraction by protecting the beacon chain from being reorged due to IL-related conditions.
 With this design, a beacon block would no longer be rejected simply for containing a commitment to a payload with an insufficiently inclusive IL bitlist. Instead, if the builder’s final payload fails the deterministic post-check, then only the payload is reorged. The beacon block itself remains canonical, and the next proposer simply builds on it with a new, valid payload.
 The main tradeoff is that this initial inclusivity signal relies on the smaller set of validators in the PTC rather than the entire attester committee.

Both options are acceptable, it’s more a question around whether we want more attesters to give an earlier, more robust signal, or whether we would like the PTC to provide the IL bitlist inclusivity signal, so IL bitlist checks can not cause beacon chain reorgs.

Finally, it’s worth noting that the split IL enforcement design is compatible with both [block and slot auctions](https://efdn.notion.site/Arguments-in-Favor-and-Against-Slot-Auctions-in-ePBS-c7acde3ff21b4a22a3d41ac4cf4c75d6) (h/t Potuz). Even if a builder doesn’t commit to a specific `PayloadHash`, it can still commit to an `IL bitlist`, which it is then forced to satisfy.

### IL satisfaction with missing payloads

In previous IL designs like EIP‑7547, an IL published in slot `N – 1` remains enforceable until it is fully satisfied. If the execution payload for `slot N` never appears, both `IL(N – 1)` and `IL(N)` roll forward together, so every subsequent payload must clear an ever‑growing backlog before newer ILs can be considered.

With FOCIL and ePBS the rule is simpler and far more liveness‑friendly. Beacon blocks can continue to be proposed even if several consecutive payloads are missing, because each empty block’s `IL bitlist` is treated as temporary. When a payload finally arrives, it must satisfy only the `IL bitlist` from the most recent block with a missed payload; and older `IL bitlists` are simply ignored/discarded. This avoids unbounded IL accumulation while still enforcing the latest, most up-to-date IL.

### ePBS and FOCIL synergies

A key synergy between FOCIL and ePBS revoles around the separation of beacon blocks and execution payloads. This separation enables to enforce IL conditions by rejecting non-compliant payloads without affecting the beacon chain stability. This is a significant improvement over others proposals (e.g., Delayed Execution [EIP-7886](https://eips.ethereum.org/EIPS/eip-7886) in which the block and execution payload are combined.

Specifically, in ePBS, beacon blocks and execution payloads are validated separately. The beacon block becomes canonical in the chain through attester votes. If the payload later proves to not satisfy IL conditions, it receives no support (e.g., from the PTC) and can be cleanly discarded by the next proposer.

Without this separation, a non-compliant block would initially receive full support in `slot N`. Once discovered as non-compliant, the next proposer (`slot N+1`) attempts to reorg this block with a competing block. This leads to two blocks (the original non-compliant block and the competing compliant block) having equal full weight, thus creating chain instability.

Another advantage of cleanly separating beacon blocks from execution payloads is that attesters no longer need static checks with post-state values (e.g., requiring objects like Block-Level Access Lists [EIP-7928](https://ethereum-magicians.org/t/eip-7928-block-level-access-lists/23337)) to be confident that the next payload will satisfy IL conditions. Under ePBS, a payload that later proves non-compliant is simply discarded, while the beacon block remains canonical.
