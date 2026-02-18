---
source: magicians
topic_id: 21325
title: "EIP-7784: GETCONTRACT code"
author: peersky
date: "2024-10-10"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7784-getcontract-code/21325
views: 183
likes: 1
posts_count: 8
---

# EIP-7784: GETCONTRACT code

This EIP is a proposal to incorporate [ERC-7744](https://ethereum-magicians.org/t/erc-7744-code-index/20569) functionality in core standards track, making indexing any deployed bytecode by it’s hash part of EVM specification.

## Replies

**peersky** (2024-12-07):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9108)














####


      `master` ← `peersky:code-index`




          opened 03:18PM - 07 Dec 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/c/c8d81b2e03d7221d8938d3cc80f74d01c836fbf1.jpeg)
            peersky](https://github.com/peersky)



          [+17
            -11](https://github.com/ethereum/EIPs/pull/9108/files)







**ATTENTION: ERC-RELATED PULL REQUESTS NOW OCCUR IN [ETHEREUM/ERCS](https://gith[…](https://github.com/ethereum/EIPs/pull/9108)ub.com/ethereum/ercs)**

--

When opening a pull request to submit a new EIP, please use the suggested template: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












- Added 7702 boundary case consideration to specification
- Added gas & considerations
- Proposing to move this in to Review

---

**SamWilsn** (2024-12-10):

> address:  If the codehash exists in the state, pushes the corresponding contract address onto the stack. Otherwise, pushes 0.

Perhaps I’m misunderstanding the way this works, but what happens if multiple contracts share the same `codehash`? What gets pushed?

---

**peersky** (2024-12-11):

Thanks for clarifying [@SamWilsn](/u/samwilsn) , it is part of specification that contract shall be added to index only if key is not already taken:

> Every contract stored in EVM MUST be added to the state trie with the key being the keccak256 hash of the contract’s bytecode, provided it is:
>
>
> not already present
>

This means, that if there are N>1 shared `codehash` contracts, only first deployed address will be returned at all times.

Perhaps this needs better phrasing to be more clear?

---

**SamWilsn** (2024-12-11):

No, that’s fine wording. I just missed it.

Is there a frontrunning risk here?

---

**peersky** (2024-12-11):

[@SamWilsn](/u/samwilsn)

Stateful contracts may be giving first deployer some advantage, but only in case if someone uses resolved address not in library-like scenario, which is unexpected behavior.

In security considerations I added following:

> Security Considerations
> Malicious Code: The index does NOT guarantee the safety or functionality of indexed contracts. Users MUST exercise caution and perform their own due diligence before interacting with indexed contracts.
>
>
> Storage contents of registered contracts: The index only refers to the bytecode of the contract, not the storage contents. This means that the contract state is not indexed and may change over time.

Another concern that possibly worth of discussing is potential collusion of code hashes. If a developer pre-approves some particular codehash and uses `GETCONTRACT` within his implementation, an adversary might attempt to front run it by seeking for a collusion value.

---

**SamWilsn** (2024-12-20):

Another question: How is this an improvement over passing an address to the contract, and it doing an extcodehash before using the address? So the off-chain entity would maintain the index, and the on-chain component would verify correctness.

---

**peersky** (2024-12-21):

**Developer experience benefit:**

One of main improvements is that bytecode hashses can be baked in to bytecode, allowing fully stateles contracts that specify full behaviour and they can be shared by different entities.

This is not something off-chain indexing could achieve, as having shared, non permissioned, and available to unrelated entities index is desired.

Solving this without EIP is doable as demonstrated by ERC-7744, it eventually achieves all of the motivation section points, but it requires manual input from developers to index code which invitebly reduce it’s adaption.

Moving 7744 into this as EIP creates such index automatically, making it exceptionally developer friendly.

**Protocol benefit:**

Indexing by codehash enshrines code reusability. For example new EIPs are possible that could allow using pointers within EVM to repeating code deployments instead of duplicating every new ERC20 derived from same OZ library.

I expect that would also become more gas effective, and generally developers would become incentivized to drop out[solc’s generated metadata](https://docs.soliditylang.org/en/latest/metadata.html) to have codehash defined purely by functionality. (Metadata could be easily stored elsewhere, like in contract creation code).

Eventually this will allow reduce size of contract data stored on execution clients, which is important as it cannot be pruned from execution clients easily.

