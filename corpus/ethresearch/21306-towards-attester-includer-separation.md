---
source: ethresearch
topic_id: 21306
title: Towards Attester-Includer Separation
author: soispoke
date: "2024-12-20"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/towards-attester-includer-separation/21306
views: 937
likes: 17
posts_count: 3
---

# Towards Attester-Includer Separation

[![Screenshot 2024-12-17 at 10.44.05](https://ethresear.ch/uploads/default/optimized/3X/4/2/42eec809c897c5cf696a014a8c53b46f35f78c02_2_498x500.jpeg)Screenshot 2024-12-17 at 10.44.051556×1562 318 KB](https://ethresear.ch/uploads/default/42eec809c897c5cf696a014a8c53b46f35f78c02)

*^Rare picture of an includer, chilling and effortlessly collecting rewards for improving Ethereum’s censorship resistance.*

*by [Thomas Thiery](https://x.com/soispoke)* - December 17th, 2024

Thanks to [Julian Ma](https://x.com/_julianma) and [Barnabé Monnot](https://x.com/barnabemonnot), [Terence Tsao](https://x.com/terencechain) and [Jacob Kaufmann](https://x.com/jacobykaufmann) for feedback and discussions on this post.

# Introduction

Lately I’ve been stumbling upon more and more discussions and research around incentives for transaction inclusion via [FOCIL EIP-7805](https://eips.ethereum.org/EIPS/eip-7805), state vs. inclusion [preconfirmations](https://www.youtube.com/playlist?list=PLJqWcTqh_zKHDFarAcF29QfdMlUpReZrR), and further separating protocol [roles](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683) and [duties](https://mirror.xyz/barnabe.eth/QJ6W0mmyOwjec-2zuH6lZb0iEI2aYFB9gE-LHWIMzjQ).  It has become increasingly clear to me that thinking from first principles about state and inclusion as two orthogonal dimensions could be useful in guiding future protocol development.

*Disclaimer: In this post, I’ll use simplified, somewhat caricature-like definitions to differentiate inclusion transactions from state transactions, acknowledging that in practice there is much more nuance.*

## Informal definitions, properties and life cycles

### Inclusion transactions

By **inclusion transactions**, I mean ***order-invariant** transactions (h/t James Prestwich) whose outcome remains the same regardless of the state on which they are executed*; the only important factor is that they are included somewhere in the block. Examples include making a payment at a coffee shop or transferring tokens to a friend.

Because of their order-invariant property, **inclusion transactions** are typically sent to the public mempool. Publicly disclosing transaction information before inclusion is acceptable since no one can exploit these transactions (e.g., by frontrunning), as they don’t intrinsically carry Maximal Extractable Value (MEV). To be considered valid for inclusion, these transactions must pay the `base fee` for each unit of gas consumed.

In a post-EIP-7805 world, inclusion transactions would mostly be included in Ethereum blocks by multiple IL proposers via FOCIL (using inclusion rules like time pending in the mempool, or priority fee ordering). By being publicly broadcast to the mempool, these transactions benefit from increased chances that one of multiple IL proposers will include them via their inclusion lists.

### State transactions

By **state transactions**, I mean ***order-dependent** transactions whose outcomes change based on the state at the time of execution*. For example, a transaction performing a token swap on an automated market maker like Uniswap.

**State transactions** originating from regular users potentially carry Maximal Extractable Value (MEV) and can be exploited by searchers—for example, through frontrunning or sandwich attacks—if their content is publicly available before inclusion. These transactions are often time-sensitive and benefit from being sent through private channels to ensure MEV protection and/or receive rebates. When state transactions carry MEV and are made available to sophisticated parties like searchers, whether willingly or unwillingly, they are usually bundled together with other transactions to extract the MEV opportunity they create. Note that state transactions can also originate from sophisticated parties themselves; for example, arbitrageurs who take advantage of price differences between different exchanges to make a profit. In both cases, when state transactions generate MEV opportunities, they are usually accompanied by tips to validators (in the form of `priority fees` or by using [coinbase transfers](https://docs.flashbots.net/flashbots-auction/advanced/coinbase-payment)) in addition to the `base fee`.

Because FOCIL does not provide any guarantees on transaction ordering or inclusion during network congestion (i.e., when blocks are full), we can assume that the market structure for state transactions wouldn’t change much in a post-EIP-7805 world.

> Here’s a brief recap of the main differences between inclusion and state transactions:
>
>
> Inclusion transactions:
> - Pay base fees to be considered for inclusion in the block.
> - Do not use priority fees to signal order preferences.
> - Benefit from being publicly broadcast to a large number of parties.
> - Do not have to rely on sophisticated actors for inclusion.
> State transactions:
> - Pay base fees to be considered for inclusion in the block.
> - Add priority fees to express preferences regarding the specific state on which they would like to be executed, which corresponds to a particular position in the block.
> - Benefit from being sent privately to one or a few sophisticated parties.

[![Meme Generator from Attester-Includer Separation](https://ethresear.ch/uploads/default/original/3X/0/3/03a416a65a12f994c473f6199d3c94adc78e03b9.jpeg)Meme Generator from Attester-Includer Separation500×500 61.8 KB](https://ethresear.ch/uploads/default/03a416a65a12f994c473f6199d3c94adc78e03b9)

***Note:** An inclusion transaction might pay priority fees for reasons unrelated to order preferences. For example, it may need to compensate the block producer for [additional resource usage](https://ethresear.ch/t/reducing-latency-games-by-levelling-the-playing-field-on-block-size-for-pbs/19356)—such as the extra propagation time required by blobs. Priority fees can also signal a desire for faster inclusion rather than a specific placement in the block. In other words, even if a transaction does not care about its position, it may be willing to pay more to reduce delays and be included sooner (e.g., blob transactions, fraud proof transactions).*

## Zooming in on Fees

### Base and Priority Fees

Since EIP-1559 was implemented, all transactions—both inclusion and state transactions—must pay `base fees` to be considered for inclusion in a block. `Priority fees`, on the other hand, can serve different purposes depending on whether there is network congestion:

- No Congestion: When there is enough space in the block to include all pending transactions:

Inclusion transactions do not generally need to pay priority fees since they will be included as long as they pay the base fee and do not care about being inserted at a specific position in the block.
- State transactions will pay priority fees to incentivize the block producer to execute them on a particular state.

**Congestion**:

- Inclusion transactions might then choose to add priority fees to increase their chances of being included in the next block—for example, ahead of other inclusion transactions— rather than waiting until the network is no longer congested.
- State transactions will use priority fees regardless of whether there is network congestion.

The interesting takeaway here is that the boundary between state and inclusion transactions blurs during periods of congestion. When there isn’t enough space for every transaction, simply wanting to be included anywhere in a given block conceptually becomes very similar to wanting to be executed on a specific state. `Priority fees` can thus be thought of as a one-size-fits-all mechanism to incentivize block producers and secure an advantageous position in a block.

However, there is another obvious reason a transaction might not be included in a block even without congestion: **censorship**.

### Costs of censorship

In a post-EIP-7805 world, there are still a couple of ways to censor a transaction:

- Block Stuffing: Given FOCIL’s conditional and anywhere-in-block properties, the proposer can stuff its block up to the gas limit in order to exclude the transaction and still satisfy the IL conditions. To estimate the cost of stuffing multiple consecutive blocks, I used the following formula:

\text{Block Stuffing Cost} = (\text{Gas Limit} - \text{Gas Used}) \times \text{Base Fees} \times \left( \frac{1}{0.125} \times 1.125^N - 1 \right)

 where N is the number of consecutive blocks.
 The figure below estimates the average costs of block stuffing over the past three months (based on this Dune query), highlighting how market conditions and base fees influence them, and illustrating how stuffing multiple blocks in a row becomes exponentially more expensive for the attacker.
Dec 9 Screenshot from Attester-Includer Separation1986×586 66.9 KB
- Missing slot: Alternatively, the proposer can choose to skip block proposal for their assigned slot, causing them to forgo both consensus (issuance) and execution (MEV) layer rewards, which amount to approximately 0.04 ETH combined per block on average during the past three months.
 Screenshot 2024-12-18 at 18.21.351986×588 37.7 KB

*Note that in both cases above, increasing a transaction’s `priority fees` makes it more costly for the proposer to exclude it.*

- IL committee bribing:  Lastly, an obvious way to censor a transaction is to convince all IL proposers not to include it in their ILs. Under EIP-7805, IL proposers are not rewarded for including transactions in their ILs. In practice, convincing all IL proposers in a committee to act dishonestly and against the ethos of the Ethereum network might be difficult. With FOCIL, we only need one member of the committee to act honestly and include all transactions without censoring for the mechanism to work as expected. However, in theory, an attacker could offer a very small bribe to all 16 committee members to exclude a given transaction. If the IL proposers are rational, they might accept any bribe greater than zero.

*By relying on the altruistic behavior of IL proposers, there is no way to control the cost they incur when censoring a transaction.*

|  | Block Stuffing | Missing Slot | IL committee bribing |
| --- | --- | --- | --- |
| Cost of censorship | 0.02 to 0.4 ETH | ∼ 0.1 ETH | > 0 ETH |

## Wat do?

## Inclusion fees

Given the distinct properties and life cycles of state and inclusion transactions—and the imbalance where users can tip the proposer but cannot affect the cost incurred by IL proposers when censoring transactions in protocol—one option is introducing an independent inclusion fee (IF) and reward mechanism to increase inclusion guarantees and cost of censorship, while preserving the role of priority fees (PF) as proposer tips.

This approach allows users to craft their transactions based on network conditions (base fees) while controlling how much they are willing to pay for **(1)** Being executed on a specific **state** via PFs and **(2)** Increasing their **inclusion** guarantees via IFs, or both. In the diagram below, you can see how transactions are sent either privately to the block producer or to the public mempool, and are specifying both priority and inclusion fees. We assume that transactions are added to inclusion lists (ILs) and sorted in descending order based on inclusion fees (more on this in the next section). The block producer then orders the full payload—by default according to priority fees or in any other order depending on MEV opportunities—incorporating transactions from ILs and those they received privately.

[![Nov 21 Screenshot from Attester-Includer Separation](https://ethresear.ch/uploads/default/optimized/3X/4/5/458e427b697fce606bf034ad7638c3e2e969d83b_2_690x289.png)Nov 21 Screenshot from Attester-Includer Separation1872×786 101 KB](https://ethresear.ch/uploads/default/458e427b697fce606bf034ad7638c3e2e969d83b)

### Reward mechanism

A simple way to distribute inclusion fees among IL proposers is to allocate them proportionally based on their contributions, rewarding only those who included the transactions in their ILs (i.e., [conditional tips](https://arxiv.org/abs/2301.13321)). This leads to greater incentives to include transactions no one else wants to include (e.g., “censorable transactions”).

In the example above, IL Proposer 1 included all pending transactions from the mempool. Their rewards would thus be calculated as follows:

- Transaction g: Inclusion fee of 6 divided by 4 proposers = 6 ⁄ 4 = 1.5
- Transaction d: Inclusion fee of 4 divided by 3 proposers = 4 ⁄ 3 ≈ 1.333
- Transaction e: Inclusion fee of 1 divided by 3 proposers = 1 ⁄ 3 ≈ 0.333
- Transaction f: Inclusion fee of 0 divided by 4 proposers = 0 ⁄ 4 = 0

Adding these up, IL Proposer 1 would receive approximately  **1.5 + 1.333 + 0.333  + 0 = 3.166** in rewards for including these transactions in its IL.

Alternative approaches to rewarding IL proposers include using issuance rather than fees,  [weighting rewards based on past performance](https://warpcast.com/pintail/0x8233d2f5). It is also important that any such reward mechanism be independent of the existing Transaction Fee Mechanisms (TFMs)—in other words, separate from both the base fee and the priority fee. Attempting to repurpose the base fee to reward IL proposers is not incentive-compatible because EIP-1559’s economic design relies on burning the base fee to prevent block producers from manipulating transaction inclusion and inflating fees for personal gain. By ensuring that the base fee is never directly redistributed, the system maintains a balanced incentive structure. Similarly, relying on a model that redirects priority fees to IL proposers fails under network congestion, as block producers would then have a greater incentive to include non-IL transactions for higher direct rewards.

## Roles and participants

Is it possible—and desirable— to go further and separate protocol participants who are tasked with transaction inclusion (IL committee members) from those who focus on valuable state transactions (proposers)? Let’s now imagine a post-FOCIL, post-APS (Attester-Proposer Separation) world. In this scenario, we still have IL proposers including transactions from the public mempool in their inclusion lists and being rewarded via inclusion fees. However, there’s now a separation between attesters/the beacon proposer, the execution proposer and the builder (whether PBS is enshrined in the protocol or not is not relevant for this part of the discussion).

**Here’s a quick overview of each participant’s responsibilities:**

[![Nov 19 Screenshot from Attester-Includer Separation](https://ethresear.ch/uploads/default/optimized/3X/1/a/1a5912c06b48482ca41ba5572740ef21bcf301bb_2_545x500.jpeg)Nov 19 Screenshot from Attester-Includer Separation1041×954 72.6 KB](https://ethresear.ch/uploads/default/1a5912c06b48482ca41ba5572740ef21bcf301bb)

> IL Committee Members:
> - Level of Sophistication: Low – IL proposers create Inclusion Lists (ILs) containing transactions pending in the public mempool.
> - Capital Requirements:
> - Medium – From 1 ETH to 2,048 ETH if/when maxEB and minEB are implemented.
> - Heavy — Capital is staked, locked upfront, and at risk of being slashed for other forms of misbehavior (e.g., proposing more than one distinct block at the same height), but not for failing IL-specific duties (e.g., IL equivocation) at least in the current version of FOCIL.

> Beacon Proposer:
> - Level of Sophistication: Low – Determines the head of the chain according to its local view and proposes the beacon block, which includes all consensus-related information such as the block header, attestations, withdrawals, deposits, and slashing penalties. Post-APS, beacon proposers are not incentivized to play timing games and can stay unsophisticated.
> - Capital Requirements:
> - Medium – From 1 ETH to 2,048 ETH if/when maxEB and minEB are implemented.
> - Heavy — Capital is staked, locked upfront, and put at risk of being slashed (e.g., for proposing more than one distinct block at the same height).

> Attesters:
> - Level of Sophistication: Low – Ensure that both the consensus and execution information contained in the full block are valid according to their views. They vote for the block if it passes all validity checks, such as being built on the correct head, containing valid transactions, and satisfying IL conditions.
> - Capital Requirements:
> - Medium – From 1 ETH to 2,048 ETH if/when maxEB and minEB are implemented.
> - Heavy — Capital is staked, locked upfront, and put at risk of being slashed (e.g., for attesting to different head blocks).

> Execution Proposer (Assuming the execution proposer does not outsource block production to a builder):
> - Level of Sophistication: High – Responsible for proposing a complete and valid execution payload to the network, with final authority over transaction inclusion and ordering, provided that the execution payload includes IL transactions. Must operate sophisticated infrastructure to implement complex strategies and efficiently extract MEV.
> - Capital Requirements:
> - High – Requires sufficient capital to secure execution proposing rights, to successfully execute advanced MEV strategies, such as non-atomic arbitrages and provide additional services like pre-confirmations.
> - Heavy - Execution proposers also need slashable capital to ensure they’re disincentivized from misbehavior, but this requirement comes into play after they’ve been selected (in contrast to attesters and beaucon proposers). At that point, they must gather the necessary capital to secure pre-confirmations, cover missed slot penalties, or pay their bids.

Interestingly, by separating attesters from proposers, APS also effectively separates execution proposers from IL committee members. However, in the next section, we argue that IL committee members should be considered a separate class of participants. Because their responsibilities are limited in complexity and they are not directly involved in the system’s economic security, they don’t need to be subject to the same capital requirements as attesters.

### Attester-Includer Separation

[![Attester Includer Separation](https://ethresear.ch/uploads/default/optimized/3X/f/f/ffa05a37c0b9b788141ddc3944402063b7f2d2d0_2_684x500.jpeg)Attester Includer Separation2000×1461 219 KB](https://ethresear.ch/uploads/default/ffa05a37c0b9b788141ddc3944402063b7f2d2d0)

*h/t Barnabé*

Building on the idea of unbundling roles to better align them with protocol duties, and drawing inspiration from tiered staking models like [Rainbow Staking](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683) and validator selection mechanisms such as [Orbit](https://ethresear.ch/t/orbit-ssf-solo-staking-friendly-validator-set-management-for-ssf/19928), we propose further separating attesters from IL committee members (includers).

Thinking from first principles, we would want both attesters and includers to be geographically decentralized and unsophisticated. However, there are some crucial differences between these sets of participants regarding capital requirements and the importance of their roles in securing the network:

- Attesters:

Security: Overall, attesters play an extremely crucial role in securing the network by participating in consensus and ensuring liveness and finality. This critical role comes with some constraints. For example, it is important to avoid rotating attesters too quickly, as it might not be optimally secure from a consensus perspective. Similarly, we do not want validators to enter or exit the active set of attesters too rapidly, which is why we have withdrawal and deposit queues.
- Capital requirements: We want attesters to consolidate by maximizing the balance of a single validator (e.g., up to 2,048 ETH) instead of running multiple instances with lower balances (e.g., 32 ETH). This consolidation enables us to achieve high levels of economic security with a manageable number of participants, and facilitates moving towards faster finality (e.g., 3SF). Additionally, attesters must have at least some amount of ETH at stake to allow for slashing in cases where they do not fulfill their duties, whether intentionally or not. This means their capital needs to be staked and locked upfront (i.e., heavy).

**IL Committee Members**:

- Security: IL committee members are not involved with consensus and don’t play a role in securing the network. They are only tasked to improve censorship resistance by including transactions in ILs using their local view of the public mempool. Moreover, we only need one-out-of-n IL proposers to honestly build its IL for FOCIL to be effective and impose constraints on what transactions builders have to include in their blocks.
- Capital Requirements: Ideally, we want very low barriers to entry so that anyone wishing to contribute to Ethereum’s censorship resistance can easily do so with 0.01 ETH for example, or just enough to ensure Sybil resistance and prevent participants to “just signing up” but then being offline. The IL committee also rotates every slot, so there is potentially no need for queues or penalties other than missing rewards if an inclusion fee of sorts exists.

**The question is**: Do these differences justify moving towards two independent sets of participants, each fulfilling a specific duty, or should it remain the same set of participants?

[![Dec 9 Screenshot from Attester-Includer Separation (1)](https://ethresear.ch/uploads/default/optimized/3X/7/d/7dd163c48298cfcc1a93c701ab91bb9b462466eb_2_690x448.png)Dec 9 Screenshot from Attester-Includer Separation (1)1526×992 66.6 KB](https://ethresear.ch/uploads/default/7dd163c48298cfcc1a93c701ab91bb9b462466eb)

**We argue that it does. By allowing anyone to join and contribute to Ethereum’s censorship resistance as an “includer”—with minimal hardware requirements (e.g., a smartwatch), a simple, low-friction user experience (no queues), as well as *light* and *minimal* capital requirements—and by rewarding them with an independent transaction fee mechanism (inclusion fees), the network can self-regulate based on the level of censorship. If many transactions are being censored, users can raise inclusion fees, thereby increasing the cost of censorship. As these higher fees get distributed among includers, more individuals will be incentivized to participate in creating inclusion lists (ILs), ultimately improving Ethereum’s censorship resistance. Lastly, includers should also be able to participate in improving the network’s censorship-resistant properties and uphold chain neutrality without publicly revealing their preferences via the specific transactions included in their lists. To this end, we can leverage [anonymous ILs](https://ethresear.ch/t/anonymous-inclusion-lists-anon-ils/19627), using a combination of linkable ring signatures and anonymous broadcast protocols to protect their identities.**

## Replies

**Nero_eth** (2024-12-20):

Great write-up! I really like the concept of splitting the validator role into smaller, specialized components. This approach could enable more focused improvements across different areas.

The idea of includers is a cool one, but I think we should explore compensating them through issuance rather than requiring potentially censored parties to pay higher fees for inclusion.

From the user’s perspective, the inclusion fee seems a bit odd. For example, as a user willing to spend x on my transaction, I have two options:

1. Pay x via the priority fee (no inclusion fee).
2. Pay x via the inclusion fee (no priority fee).

As a result, I can choose who to compensate for inclusion: the includer or the proposer. Currently, the proposer receives the payment, which makes sense as they secure the network and arguably deserve it.

---

**soispoke** (2024-12-26):

Thanks for the feedback [@Nero_eth](/u/nero_eth)!

From the user’s perspective, adding an independent inclusion fee means you can specifically choose to allocate x to:

1. The proposer, to express a preference (usually regarding the state on which you want your transaction to be executed)
2. The includers, so the cost of censoring your transaction increases
3. Or both (e.g., 1/3 of x goes to the proposer, 2/3 goes to includers)

Alternatively, you could think of a mechanism that “transfers” fees to either the proposer or includers based on who included a given transaction. While the details obviously need to be worked out rigorously, a significant advantage of using inclusion fees, imo, is the dynamic I described here:

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> The network can self-regulate based on the level of censorship. If many transactions are being censored, users can raise inclusion fees, thereby increasing the cost of censorship. As these higher fees get distributed among includers, more individuals will be incentivized to participate in creating inclusion lists (ILs), ultimately improving Ethereum’s censorship resistance.

I don’t think the same dynamic can be achieved with issuance since there isn’t an objective criterion to determine whether a transaction is being censored or not. What’s nice with issuance, of course, is the guaranteed payment, so you always have some parties willing to participate in the mechanism (although what we want to incentivize is making “good” lists, not just making lists). But it also comes with choosing a specific issuance curve, etc., which we know is tricky and opinionated.

