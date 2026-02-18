---
source: magicians
topic_id: 19000
title: "EIP-7640: Transaction Revert Protection"
author: jcp
date: "2024-02-29"
category: EIPs
tags: [evm, opcodes, transactions]
url: https://ethereum-magicians.org/t/eip-7640-transaction-revert-protection/19000
views: 1030
likes: 8
posts_count: 15
---

# EIP-7640: Transaction Revert Protection

This proposal is to modify to the Ethereum consensus for an opt-in transaction flag to define reverted transactions as invalid (cannot be included in a block). Consideration is made for default mempool DoS mitigation and an attempt at minimizing implementation complexity.

The goal is to make it so that Ethereum can have more decentralized transaction propagation of transactions with “intents” (currently these types of services are usually centralized with a trusted server), more decentralization in block building and transaction propagation, increased market formation directly via publicly gossiped transactions on mempools using tx gas tips, and more decentralized bundling in Account Abstraction transactions.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/8267)














####


      `master` ← `josephpoon:tx_revert_protection`




          opened 05:54AM - 29 Feb 24 UTC



          [![](https://avatars.githubusercontent.com/u/13424781?v=4)
            josephpoon](https://github.com/josephpoon)



          [+228
            -0](https://github.com/ethereum/EIPs/pull/8267/files)







Proposal to modify the Ethereum consensus for an opt-in transaction flag to defi[…](https://github.com/ethereum/EIPs/pull/8267)ne reverted transactions as invalid (cannot be included in a block).














      [github.com/josephpoon/EIPs](https://github.com/josephpoon/EIPs/blob/4c236bbef6e6c84787705daaea274de5af8b7f7a/EIPS/eip-7640.md)





####

  [4c236bbef](https://github.com/josephpoon/EIPs/blob/4c236bbef6e6c84787705daaea274de5af8b7f7a/EIPS/eip-7640.md)



```md
---
eip: 7640
title: Transaction Revert Protection
description: Defines a new transaction type which rejects reverted transactions
author: Joseph Poon (@josephpoon), Christopher Jeffrey (@chjj), Boyma Fahnbulleh (@boymanjor)
discussions-to: https://ethereum-magicians.org/t/eip-7640-transaction-revert-protection/19000
status: Draft
type: Standards Track
category: Core
created: 2024-02-28
requires: 140, 141, 658, 1559, 2718, 2930
---

## Abstract

A consensus rule to flag a reverted transaction as invalid, i.e., ineligible for
block inclusion, providing consensus layer assurance that users do not pay gas
fees for unsuccessful transaction execution.

[EIP-658](./eip-658.md) designates a transaction as "failed" if its receipt
```

  This file has been truncated. [show original](https://github.com/josephpoon/EIPs/blob/4c236bbef6e6c84787705daaea274de5af8b7f7a/EIPS/eip-7640.md)

## Replies

**Arvolear** (2025-07-19):

Pretty cool idea. Not sure why there was no discussion whatsoever regarding the topic. I have several comments though:

1. Let’s imagine a scenario when a user sends a swap transaction on some dex. Currently, if the prices change beyond the acceptable slippage, the transaction reverts and the user understands that the swap wasn’t successful. However, if the revert_protect was to be set, the user would not be notified that they need to try to swap again. Probably, there needs to be some mechanism incorporated for dapps to be able to track those “dropped” transactions.
2. It would be great to have a better understanding (probably the rational section extended) of how this proposal would co-exist with ePBS (EIP-7732) and FOCIL (EIP-7805), which will likely be included in the Glamsterdam fork.
3. There is a very good benefit to the revert_protect approach. It would free up block space (up to ~10% of all the transactions on Ethereum are reverted transactions) and achieve 10% L1 scalability basically for free. It would be amazing to see some numbers on that matter.

Thanks!

---

**RubyEDE** (2025-07-19):

It increases UX but at the same time it ALSO increases network CPU usage without any compensation for it. It’s a bad implementation that do not fit in the network itself but as a separate layer(Like flashbots for example).

---

**bbjubjub** (2025-07-21):

This is not the case. The EIP explicitly ordains that

> [as] a policy rule, [revert-protected transactions are] neither propagated nor accepted on the default Ethereum mempool p2p network.

Thus the network, understood here as honest nodes that maintain a mempool, is not forced to deal with revert-protected transactions in any way. Specific actors, in particular block builders, can opt-in to process said transactions if they see a benefit in it. (e.g. private order flow)

Observe that flashbots, in the way it currently operates, relies on trusted parties (in-part through TEEs) that could include reverting transactions and collect the transaction fee if they were compromised. This EIP removes this possibility. Although it does not, on its own, replace flashbots, it make it more trust-minimized.

---

**RubyEDE** (2025-07-21):

It’s an even bigger problem.

By allowing only certain actors to see specific transactions, we massively increase centralization, as some builders will opt in, some won’t, and the rest of the network won’t see these transactions. Now we’re not just centralizing block production, we are centralizing the visibility of them as well.

There’s a big fragmentation risk, as this proposal wants to create two separate mempools.

---

**bbjubjub** (2025-07-21):

This is already happening and is not a problem. We already have non-transparent routes for transactions to land on-chain like flashbots and other such services. This is an inherent feature of having a block proposer: we give them the right to put anything they want in the block, with no requirement to disclose it beforehand. At the same time, the public mempool operates just fine: you can distribute your transactions to any prospective block proposer or builder through it, and it is censorship resistant. It will soon become even more powerful with inclusion lists, and that doesn’t require banning non-public transaction flows at all.

---

**RubyEDE** (2025-07-21):

There’s a huge difference between optional private routing and protocol enforced exclusion.

Flashbots is optional → I can choose to use it or just use the public mempool

EIP 7640 → makes this fallback impossible for these specific transactions.

The problem isn’t that private routing exists it’s that we want to enforce it, bottom line, it’s more centralization for Ethereum.

---

**bbjubjub** (2025-07-21):

The fact that a transaction with the revert protection flag set is excluded from the mempool is a feature. It is the point of the flag. If you want to use the public mempool, you reset the flag and re-sign what is an equivalent and otherwise identical transaction. This is not centralization, it is an additional opt-in feature that helps Ethereum better serve concrete use cases, in particular out-of-protocol account abstraction (no revert for bundlers) MEV auctions (no reverts for auction losers) and MEV extraction (no revert if your block gets reorged) based rollups (no reverts in case of conflicting batches) etc. Taiko Labs and some bundlers on Polygon have already lost money on this, and the network didn’t really benefit: there’s better uses for gas than reverts that do nothing.

---

**RubyEDE** (2025-07-22):

You’re saying this is an optional feature, but it’s only optional for the people who control the infrastructure. A user can unset the revert protection flag, but that just reintroduces the same issues we are trying to avoid, it doesn’t solve the main problem. It’s like a bad hotfix.

The point of revert protection is to not pay gas fees for failed transactions. If we tell them to just unset the flag, they now have 2 choices:

1. Use revert protection → protocol enforced exclusion
2. Use public mempool → back to the original problem

There’s no real choice here.

---

**jcp** (2025-08-12):

Hi Arvolear,

1. Yes, the simplest solution would be to embed a TTL as part of the contract or wrapper contract, whereby a TX is invalid after a set date, which could be embedded in the calldata. A logical thing to do would be to auto-expire past a certain time as well, and to not have guarantees of checks of validity/inclusion on every block.
2. For FOCIL, I believe FOCIL as proposed increases the risk of withholding attacks significantly, as coordinated subsets of validators can easily prevent future block producers from being able to produce a block (as they do not have the data required to produce the FOCIL block), this likely increases the attack surface of Ethereum dramatically. There is no easy way to prevent this, as inherently the design is placing the responsibility of having data availability on future 3rd party block producers which is a significant new risk exposure. For ePBS, it enshrines in-protocol MEV extraction which opens to attacks similar (but less exposed) to FOCIL (since it has a subset of voters on whether data is available). However, the key relevant aspect which affects this EIP is that delayed execution impacts any type of revert protection – block inclusion would have to charge in a delayed manner as well, which seems complex. Both these protocols insert a voting pool on data availability for future blocks in different ways (with FOCIL much more exploitable).
3. I think it can be most useful if also implemented in L2s, as there is opportunity for intents-like structures, and this would result in reduction in blob data.

Thanks for the review.

---

**jcp** (2025-08-12):

I think there is a fundamental misunderstanding the role of revert protection and its relationship to the mempool.

It does not reintroduce the same problem, and simply asserting that it “doesn’t solve the main problem” is disingenuous.

Flashbots is optional in the exact same way, except this allows you to construct revert protection without Flashbots. It isn’t centralization, it is specifically designed to open the possibility to evade centralization pressures in MEV services. There is no possible method to implement things like decentralized intents without some way to do revert protection as part of consensus, as this is a failure on the L1 consensus protocol. Fragmentation risk isn’t changing whatsoever de-facto, as there is already fragmentation of mempools, and it is going to get MUCH worse with Account Abstraction. Please detail how this is worse than Flashbots et al. It also doesn’t increase CPU usage for full nodes, it checks for a bit and rejects if it is out of consensus. There’s no disk lookup and it’s O(1) for a single bit. It can be helpful to specify an example of how fragmentation worse than AA/Flashbots, or increased CPU usage would be possible.

A significant amount of thought was put into this proposal in making it simple, easy to implement, with near-zero implementation costs (or computational costs) for current consensus nodes.

This single change allows for other beneficial results such as the possibility of open propagation of certain transactions amongst MEV providers, creating less lock-in and centralization.

---

**RubyEDE** (2025-08-13):

Flashbots work because they monetize MEV to pay for simulation costs. Remove that revenue stream (which is what this EIP proposes) and the economics collapses, it’s proposing Flashbots but not profitable, you’re not reducing centralization, you’re moving it from entities that have sustainable business models to entities that burn money on simulations out of kindness of their hearts.

Again, because revert-protected transactions are subject to protocol enforced exclusion from the public mempool, you’re forcing them into a separate, private lane. That’s not optional like Flashbots, it’s structural fragmentation. ONLY large builders with the infrastructure to run high throughput simulators will be able to compete for this flow, which *increases* centralization pressure rather than reducing it.

Look bottom line you’ve designed a system where the expensive work still happens, but removed the economic incentives that make it sustainable. That’s not solving centralization, that’s creating unsustainable centralization, I have yet to see a decentralized system that requires participants to do work for free and became successful.

---

**jcp** (2025-08-15):

Let’s agree that decentralization of Ethereum is one of the most important properties for its success. The purpose of Ethereum is not ensuring highly profitable rent for permanently centralized, trusted intermediaries.

Your argument rests on two premises:

1. Simulation costs are inherently high and removing MEV monetization makes block building economically unsustainable.
2. Without profit incentives, transaction flow will fragment into private lanes, increasing centralization.

Both premises appear to mischaracterize the actual cost structure and market dynamics.

## Cost Structure

The computational burden isn’t inherent to block building – it’s an artifact of current market structure. Block construction resembles a knapsack problem, but the complexity stems from volume (*n*) rather than algorithmic difficulty.

Current MEV infrastructure processes millions of redundant transactions because searchers must defensively submit to avoid missing opportunities. This creates artificial load:

- Multiple searchers target identical opportunities (arbitrage, liquidations)
- Each submits defensively, assuming others will too
- Builders process orders of magnitude more transactions than ultimately execute
- The actual computational work per transaction remains trivial

With protocol-enforced revert protection, the submission pattern changes fundamentally. Searchers can submit with confidence that failed transactions won’t cost them, with observation of others’ bids. While some may elect to use private pools (i.e. the existing infrastructure of relayers), a sufficient amount of searchers will optimize for maximum propagation over bid privacy. Further, propagation based flow control naturally reduces spam by creating constraint on transaction volume. Flow naturally reduces to actual opportunities rather than probabilistic spam.

The notion that block building requires datacenter-scale infrastructure misunderstands where value accrues. Current MEV providers don’t provide computational power – they provide reputational guarantees about transaction inclusion. The technical requirements for transaction simulation and ordering are modest; what’s expensive is maintaining trust relationships and network effects. The trust relationships have been required since any leakage of bids/transactions will cause costly revert.

The margin for MEV intermediaries largely goes to bribing validators, it doesn’t go into servers for builders. The server cost for builders’ simulation is an infinitesimal rounding error.

## Private Lanes

The private lane concern inverts the current reality. Today’s MEV infrastructure already operates through private channels – builders/relayers and similar services are, by definition, private transaction pools separated from public mempools.

Searchers use these private channels for one reason: without revert protection, public submission risks paying for failed transactions. Ostensibly some claim the desire to hide strategies, but strategies at this point are well known and obvious (since you can look at on-chain history), unique strategies are definitionally rare and irrelevant. When multiple searchers target the same opportunity, only one succeeds while others pay for reverts. This economic reality forces rational actors into private pools.

EIP-7640 addresses this at the protocol level. With consensus-enforced revert protection:

- Searchers can safely broadcast to public networks (using existing p2p infrastructure, no new tokens or validator sets required)
- Competition occurs through transparent gas pricing
- Failed transactions don’t incur costs
- The economic rationale for private pools disappears

This doesn’t eliminate sophisticated block building – builders can still optimize transaction ordering if validators don’t want to do it themselves. But it removes the gatekeeping function where intermediaries control access based on trust relationships. The distinction is critical: optimization services can compete on merit, while trust-based gatekeeping creates monopolistic bottlenecks. Relayers and builders do not need to be a trusted, centralized, priestly class.

## Implementation Mechanics

Consider a concrete scenario: five searchers identify an arbitrage opportunity. Currently:

1. All five submit to builders (often through relay services) to avoid revert costs
2. Builder selects the highest value transaction and constructs an optimal block
3. Builder includes winning transaction, excludes the four others, sends complete block to relay
4. Relay sends only block header to validator, withholding full block data
5. Validator blindly commits to the block header without seeing contents, trusting the relay to reveal valid block data after commitment
6. Builder captures MEV value, pays most (~90%) to validator through proposer payment, relay provides trust infrastructure

There are a few notable security risks with this form of centralization. Specifically, the relayer/builder can withhold the block data, they can construct bad block data (reverted txes when they promised not to do so, or coercive censorship), and they are in a privileged position to front-run searcher transactions (getting *flash trading* data and selectively frontrunning searchers). Secure Enclaves/TEEs merely delay the relayer/builder frontrunning problem, as TEEs are highly vulnerable as they are on-premises to the attacking relayer/builder (stealing millions/billions over time is too lucrative to assume security of TEEs held at the potential attacker’s data center).

With EIP-7640:

1. All five submit to public alt-mempools with revert protection flags, flow is gated by address stake-weight
2. Validators naturally select the highest gas bid, or use public builders which help construct blocks
3. One transaction executes, four get dropped/ignored without cost
4. No closed intermediary captures value for trust provision

While existing builders may still exist, you can move traffic into public lanes to compete, and even the existing relayer/builder infrastructure can be more open (reduced trust between builders and relayer, with the possibility of removing most of the trusted roles of the relayer entirely).

This architectural change has downstream effects on builder infrastructure. Currently, builders require relay partnerships because transaction gossip risks revert costs for searchers. Remove that risk at the protocol level, and builders can share transactions without trust requirements.

The result is a more competitive builder ecosystem. New builders can enter without establishing relay relationships. Existing builders compete on optimization quality rather than trust networks. The entire MEV supply chain becomes more permissionless and competitive.

Note that this doesn’t eliminate the need for block construction – optimal ordering still provides value. But it transforms block building from a trust-gated activity to an open competition based on technical merit. The economic rent currently extracted for trust provision gets competed away, benefiting users and the wider ecosystem instead of trusted intermediaries.

This tiny change enables the Ethereum ecosystem to build tooling which reduces dependence upon permanently entrenched participants responsible for truthfully and correctly relaying transactions/blocks.

---

**RubyEDE** (2025-08-23):

With all due respect this is a lot of chatgpt, I’m asking a simple question: who is paying for all the revert transaction processing?

---

**jcp** (2025-08-23):

You’re absolutely right to delve into the notion of payment! However–Ethereum as it exists today does not take into account payment for its mempool either. Similarly, an alt-mempool would also be free, but constrained by p2p policy like it already is today (e.g. Bittorrent). If it was economically constrained or requires profit motivation, the Ethereum mempool would not exist.

Consensus payment is not the only tool in the toolbox–policy propagation rules are just as important, if not more so. Bitcoin’s mempool (as well as Bittorrent) relies upon policy much more heavily due to the lack of gas as an on-chain direct payment for mempool risk–and innovation in policy standardness is an important, overlooked tool.

Do you have any further questions or observations which can assist in mutual understanding?

