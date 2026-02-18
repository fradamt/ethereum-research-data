---
source: magicians
topic_id: 24500
title: "EIP-7886: Delayed Execution : The Case for Glamsterdam"
author: Nerolation
date: "2025-06-09"
category: Uncategorized
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/eip-7886-delayed-execution-the-case-for-glamsterdam/24500
views: 445
likes: 3
posts_count: 7
---

# EIP-7886: Delayed Execution : The Case for Glamsterdam

# Delayed Execution: A Proposal for Glamsterdam

by [Toni](https://x.com/nero_eth) & [Francesco](https://x.com/fradamt).

> This short note follows a template designed by @timbeiko to propose a headline feature for fork inclusion.

In this document, we propose **Delayed Execution (EIP-7886)** for inclusion in the Glamsterdam hard fork.

## Summary

[EIP-7886](https://eips.ethereum.org/EIPS/eip-7886) introduces a mechanism to decouple block validation from immediate execution. By introducing static, pre-execution checks and allowing the execution outputs to be deferred, validators can attest to block validity without executing every transaction upfront. This offers a path to higher throughput, relieves the critical path of block validation from execution, and gets us closer to real-time proving in zkEVMs.

## Detailed Justification

Today, validators must fully execute each block before attesting to it. This design ties block validation directly to execution, creating a bottleneck for scalability.

Delayed Execution introduces **asynchronous block validation** by separating structural correctness from execution correctness. If execution fails or exceeds the block gas limit, the beacon block is still valid, but the execution payload becomes a no-op (i.e., the state is reverted to what it was before starting transaction execution). This decoupling reduces critical path complexity and allows for faster attestation.

## Primary Benefits

**zkEVM Compatibility (*long-term*):**

Delayed execution is particularly beneficial for zkEVM-based nodes. Since execution outputs (state root, receipts, logs) are deferred, zkEVMs gain valuable time to generate proofs. This moves us closer to a future where blocks can be validated by verifying succinct proofs instead of re-executing transactions.

**Higher Throughput Potential (*short-term*):**

Validators can attest to blocks earlier in the slot and use the remaining slot for execution. Because execution is no longer in the critical path, block gas limits can be safely increased without impacting consensus performance.

## Why Now?

The community wants to scale the execution layer. Delayed Execution directly addresses this by relieving the critical path from immediate execution, unlocking potential for higher gas limits or shorter slot times.

At the same time, recent breakthroughs in zk cryptography are making real-time proving of Ethereum blocks increasingly viable. By deferring execution outputs, EIP-7886 gives zkEVMs time they need to generate validity proofs—moving us closer to a world where nodes can verify proofs instead of executing transactions, reducing hardware requirements and enabling executionless clients.

## Compared to Alternatives

Proposals like [ePBS](https://eips.ethereum.org/EIPS/eip-7732) (enshrined Payload-Block Separation) also aim to relieve the critical path by giving the network more time to execute blocks. However, ePBS is less effective in doing so and comes at the cost of added complexity: it introduces new enshrined roles (e.g., builders), significantly modifies the fork-choice rule, and adds a new committee, the Payload Timeliness Committee.

In contrast, EIP-7886 localizes most complexity within the execution layer and avoids introducing new actors or changing fork-choice logic. This design makes it easier to adopt and implement, and it aligns directly with the needs of zkEVM-based proving systems by deferring execution outputs.

In contrast to ePBS, delayed execution does not provide more time for blob propagation or remove trust assumptions between validators and relays.

## Stakeholder Impact

**Positive:**

- Users benefit from increased L1 throughput, as delayed execution enables higher gas limits and more efficient block validation, leading to faster and potentially cheaper transactions on the L1.
- zkEVM proofers gain critical flexibility: by deferring execution outputs, EIP-7886 gives zk-based provers more time to generate validity proofs. This is a step toward executionless full nodes that validate blocks using succinct proofs instead of re-execution.

**Negative:**

- Invalid transactions may remain on the canonical chain. Under delayed execution, a block containing invalid or underfunded transactions can still become canonical, with the full EL payload—and all state updates from it—being reverted. While this avoids complex fork-choice changes, it means invalid transactions are visible on-chain without senders paying for them. However, this comes at a significant cost: the proposer forfeits all execution rewards (i.e. priority fees and the MEV-Boost payment) for that block, creating a very strong disincentive against including malformed or unexecutable transactions.

## Technical Readiness

EIP-7886 is fully specified in the [exectution-specs](https://github.com/ethereum/execution-specs/compare/forks/prague...fradamt:execution-specs:delayed-execution-noop-for-gas-used), with working implementations underway and discussions on the best design ongoing. It is compatible with other proposals such as [FOCIL](https://eips.ethereum.org/EIPS/eip-7805) or [Block-level Access Lists](https://eips.ethereum.org/EIPS/eip-7928).

## Security & Open Questions

**Known Concerns:**

- Free DA: While not actually being “free,” the current design specified in the EIP focuses on not introducing changes to the fork-choice, having staked entities on the EL, or reusing the validator stake on the CL side. Consequently, senders can include transactions without payment, but proposers must forgo the entire block, strongly disincentivizing such behavior.

**Open Questions:**

- While several different designs were explored, with the “payload reversion” one selected as the best option, there’s still the opportunity to switch to a different design (there are specs for all designs described here).

## Replies

**terence** (2025-06-09):

> In contrast, EIP-7886 keeps the consensus layer untouched.

I dont think this is true, every time you touch execution payload, and execution header, there are CL changes for these structure. Both execution API, builder API, beacon API will have to change

> In contrast to ePBS, delayed execution does not provide more time for blob propagation or remove trust assumptions between validators and relays.

I’d also add EIP7732(epbs) is only consensus layer changes, there’s no execution layer changes

---

**Nerolation** (2025-06-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> I dont think this is true, every time you touch execution payload, and execution header, there are CL changes for these structure. Both execution API, builder API, beacon API will have to change

Yeah, good point, thanks. I changed this sentence to reflect that.

---

**shemnon** (2025-06-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> the proposer forfeits all execution rewards (i.e. priority fees and the MEV-Boost payment) for that block,

Is forfeiting lost execution revenue a sufficient incentive?  Should we consider charging carriage costs (intrinsic costs such as calldata for each claimed transaction) to the proposer of the block if the block is invalid?  Otherwise a “post and find out” block is the same cost as an empty block, and carries more data across the network.

And to clarify, this penalty would be paid only in cases where the transaction is invalid with checks that can be done prior to execution: balances, nonces, data formatting, etc.

Or perhaps the proposer is charged carriage in the proposal step always?  Then refund it to the coinbase if valid, so if they are the coinbase they will get it back.  We can’t charge any old coinbase (the signature is from the propser), but they could credit any old coinbase, such as a pool.

---

**Nerolation** (2025-06-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Is forfeiting lost execution revenue a sufficient incentive?

I would argue it’s enough to ensure we’d only see such cases when there’s a bug, and won’t see something like a market around reverted blocks developing.

The [initial design](https://ethresear.ch/t/delayed-execution-and-skipped-transactions/21677) of delayed exec proposed charging the block’s coinbase for inclusion costs (calldata, blobs, access list) to ensure that data doesn’t end up on-chain without someone paying for it. But this approach had other issues:

It would require every proposer, even those relying on MEV-Boost, to have some stake on the EL. Normally, the builder is the coinbase, but in practice, every validator would need to maintain additional EL stake in case of a MEV-Boost failure leading to proposers falling-back to local building.

To have replay protection, we’d likely need to use signing and withdrawal keys (have a signed commitment to the *inclusion cost sponsoring*), along with a SC wallet that supports EIP-1271 for signature verification, mirroring the setup used on the CL. While this approach brings us closer to a model where someone (here, the coinbase) can sponsor the base fee for transactions, which is great, it also adds significant complexity.

Charging the proposer on the CL for skipped transaction costs introduces new risks. Currently, if a proposer signs a blinded block from a relay and that block turns out to be invalid, the worst-case outcome is a missed reward.

But with this new mechanism, a proposer could *lose funds* if the block they signed includes many skipped transactions. These losses would generally be small (depending on the base fee) but could vary a lot.

Both options, charging the coinbase or using the proposer’s stake, were considered. However, it now seems that **payload reversion** is the least complex and most practical path forward.

This is the post with a more detailed design space exploration:


      ![image](https://ethresear.ch/uploads/default/optimized/2X/b/b5d7a1aa2f70490e3de763bef97271864784994f_2_32x32.png)

      [Ethereum Research – 5 May 25](https://ethresear.ch/t/delayed-execution-and-free-da/22265)



    ![image](https://ethresear.ch/uploads/default/original/3X/3/5/351f26e76f12521fd7ec1672e93008a1a636c0c6.jpeg)



###





          Execution Layer Research






            delayed-execution







Delayed Execution and Free DA by Toni and Francesco   Thanks to Łukasz, Ansgar, Dankrad and Terence for feedback!   Today, free DA (Data Availability) is not a problem. Every transaction sender must pay for all resources consumed during...



    Reading time: 5 mins 🕑
      Likes: 5 ❤

---

**shemnon** (2025-06-10):

I didn’t ask if it was the easiest or most expedient mechanism in context of mev_boost, I asked if payload reversion was a *sufficient* mechanism.

Incentive wise there is no difference between an empty block and a 10MB garbage block. Like an empty block they get all rewards except fee revenue. Without carriage fees an attacker can stake eth, lose none of it, still receive baseline rewards, and ship garbage 10MB blocks whenever it is asked to build.

Is losing out on fee revenue enough to curtail this behavior?

If we argue that the 10MB block won’t be propagated well then that is also a concern for valid 10MB blocks, and will need to be addressed as gas limits go up, and the attack just moves to the largest well-propagated block size.

---

**Nerolation** (2025-06-11):

Yeah, I’d say it’s definitely sufficient. Losing all EL rewards is already a quite harsh penalty, especially since every validator has only 2-3 blocks per year. [~14% of the annual validator rewards come from EL rewards](https://ethresear.ch/t/is-it-worth-using-mev-boost/19753), so, missing out on them might turn a validators’ operation unprofitable in the long run, ofc, this assumes that you’re not “bribed” some significant amount by someone to build a “reverted payload”-block. Theoretically, you shouldn’t get more from such a bribe than you get from EL rewards (at least non on a sustainable basis), because this would mean the entity bribing you isn’t acting economically rational.

I’m not worried about the 10MB blocks. Those are full of zero-bytes and very well compressible. A more realistic size of a block that actually has some meaningful content is 1 MiB in the worst-case.

We could introduce some additional penalty that is deducted from the proposers CL stake in case of reverted payloads. The problem with that is that MEV-Boost users would sign a blinded block, risking that they’d lose money (whereas the worst-case today is an invalid block - so, walking away empty handed but at least not losing something).

