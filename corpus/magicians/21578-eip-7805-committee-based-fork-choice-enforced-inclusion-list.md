---
source: magicians
topic_id: 21578
title: "EIP-7805: Committee-based, Fork-choice enforced Inclusion Lists (FOCIL)"
author: soispoke
date: "2024-11-04"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7805-committee-based-fork-choice-enforced-inclusion-lists-focil/21578
views: 836
likes: 14
posts_count: 11
---

# EIP-7805: Committee-based, Fork-choice enforced Inclusion Lists (FOCIL)

Discussion thread for [Committee-based, Fork-choice enforced Inclusion Lists (FOCIL) EIP by soispoke · Pull Request #9010· ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9010)

# Abstract

Implement a robust mechanism to preserve Ethereum’s censorship resistance properties by guaranteeing timely transaction inclusion.

FOCIL (**Fo**rk-choice enforced **I**nclusion **L**ists) is built in a few simple steps:

- In each slot, a set of validators is selected as inclusion list (IL) committee members. Each member gossips one IL according to their subjective view of the mempool.
- The proposer and all attesters of the next slot monitor, store and forward available ILs.
- The proposer (or the builder if the block is not built locally by the proposer) includes transactions from all collected ILs in its block. The proposer broadcasts the block including IL transactions to the rest of the network.
- Attesters only vote for the proposer’s block if it includes transactions from all stored ILs.

# Motivation

In an effort to shield the Ethereum validator set from centralizing forces, the right to build blocks has been auctioned off to specialized entities known as *builders*. This has led to a few sophisticated builders dominating block production, leading to a deterioration of the network’s censorship resistance properties. To address this issue, research has focused on improving Ethereum’s transaction inclusion guarantees by enabling validators to impose constraints on builders. This is achieved by force-including transactions in blocks via ILs.

## Replies

**perama-v** (2024-11-25):

FOCIL is nice in that it essentially creates a parallel building process of 16 independent actors. Only one of them needs to be honest about seeing a transaction for it to be included.

However, ILs point back to specific IL members. This information is kept on chain allowing specific transactions to be mapped to specific validators. So an IL member must always be willing to go on record that they did not censor specific transactions. This may deter some IL members. Can we do better?

We may be able to extend FOCIL so that no specific validator is attributable. Only that one of the 16 committee members was honest about the mempool state.

FOCILIS: FOCIL with indistinguishable submissions

This is an outline of an extension which involves to additions to FOCIL.

1. Instead of signing an IL, a member creates a zero knowledge proof that they are a member of the committee.
2. To identify equivocation, IL members generate IDs in advance. These serve as nullifiers. The IDs are broadcast in the preceding slot and included in the fork choice rule using the same mechanism used for the ILs. Attesters vote for blocks that have ID lists that match the local view.

Another framing is that this is a semaphore-like construction to enable private voting by the committee members on mempool contents.

I go into more detail in the repository below.



      [github.com](https://github.com/perama-v/FOCILIS)




  ![image](https://opengraph.githubassets.com/86e25bcb352e920f8f5e3fd6cb7348cd/perama-v/FOCILIS)



###



FOCIL with Indistinguishable Submissions

---

**perama-v** (2024-11-28):

FOCIL can be deployed in a near-future fork and in a later fork be upgraded to FOCILIS if desired. I think this is probably the wisest approach as FOCIL is specced, simple and ready. I’ve added some notes to this effect (basically around SNARK selection considerations being dependent on other potential consensus upgrades).

---

**soispoke** (2024-11-28):

Thanks for your nice feedback and suggestions!

I think the general direction of unlinking IL committee members from specific lists of transactions is a very promising one.

This is also what we had in mind with [anonymous inclusion lists (anon-ILs)](https://ethresear.ch/t/anonymous-inclusion-lists-anon-ils/19627), my general intuition is that more research is needed to settle on a design we want to implement, but it’s great to see efforts in this direction.

---

**poojaranjan** (2025-02-18):

[PEEPanEIP 141: EIP-7805: Fork-choice enforced Inclusion Lists (FOCIL)](https://youtu.be/cUGyLx-mf6I) with [@soispoke](/u/soispoke) and [@Julian](/u/julian)

  [![image](https://img.youtube.com/vi/cUGyLx-mf6I/maxresdefault.jpg)](https://www.youtube.com/watch?v=cUGyLx-mf6I)

---

**marchhill** (2025-02-20):

I have some thoughts on the IL building rules. Currently the spec leaves the IL building rules fully unspecified, allowing clients to decide. While this aims to promote a diversity of IL building rules which can strengthen censorship resistance, I believe there is a risk that many clients could implement similar deterministic rules.

For example many clients could implement a simple order-by-priority fee strategy. If all IL committee members are using the same deterministic ordering strategy then (assuming they have a similar set of transactions in the client txpools) all members would build the same IL. When we take the union we will get an 8KiB IL rather than the theoretical maximum of 128KiB. This undermines censorship resistance, as now a single 8KiB transaction with a high priority fee can censor all other transactions from the mempool. Reducing the amount of overlap between ILs would increase the size of the IL when they are combined, meaning there is more throughput to force-include transactions.

Even if different clients use different ordering rules, it is still possible that we end up with an IL committee all running the same EL client. If these rules are deterministic then we would have the same situation of completely overlapping ILs.

I propose to recommend that implementers should aim for a more *disjoint* and *nondeterministic* set of ILs while leaving the exact algorithm unspecified. This can be done by introducing randomness, and using bias to pick some transactions more often than others. This would work by giving each committee member an id from `0` to `f`; the member with id `a` would then be more likely to pick transactions with hashes that start with `a`. Adding bias could further reduce the amount of overlap between ILs while crucially not eliminating it entirely.

---

**aelowsson** (2025-03-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/marchhill/48/14528_2.png) marchhill:

> I propose to recommend that implementers should aim for a more disjoint and nondeterministic set of ILs while leaving the exact algorithm unspecified.

This would be desirable. An author of this EIP (Francesco) previously outlined such ideas with further details in the [following write-up](https://meet-focil.vercel.app/il-flooding-in-focil/) (refer to the second half of the post).

---

**stakersunion** (2025-11-07):

# Stakers Union Backs EIP-7805 (FOCIL) for Glamsterdam

Stakers Union has formally voted to support EIP-7805: Fork-choice enforced Inclusion Lists (FOCIL) for inclusion in the next Ethereum network upgrade, Glamsterdam. We believe FOCIL measurably improves censorship resistance, reduces builder centralization risk, and strengthens solo-validator sovereignty without adding undue operational burden to home stakers.

You can read more on our website (linked in profile).

---

**michaelsproul** (2025-11-11):

Is there any subtlety to how FOCIL interacts with EIP-1559? I’m assuming FOCIL transactions still need to pay the `base_fee` to be considered valid for inclusion in a block – that’s implicit as part of this check, right?

> Validate T against S by checking the nonce and balance of T.origin.
> - If T is invalid, then continue to the next transaction.
> - If T is valid, terminate process and return an INCLUSION_LIST_UNSATISFIED status.

I’m concerned that IL transactions could be used to bypass regular fees (priority fees?), which would incentivise users to bribe IL committee members to include their transaction in an IL rather than going via the normal route. However, I think this doesn’t work, as the block builder can choose not to include the IL transactions if the block is otherwise full of more profitable transactions. In other words, users gain no benefit from using IL transactions *other than* censorship resistance. There is no fee-benefit to using an IL transaction, right?

---

**soispoke** (2025-11-11):

that’s exactly right, FOCIL transactions definitely still need to pay the `base_fee`, so they need to have sufficient `balance` and a correct `nonce`.

And with the [conditional inclusion](https://eips.ethereum.org/EIPS/eip-7805#execution-layer) property, builders can exclude IL transactions from their block if it’s full. So yeah, there’s definitely no fee benefit from using an IL transaction.

---

**dnstaked** (2025-11-23):

Does FOCIL take OFAC into consideration?

