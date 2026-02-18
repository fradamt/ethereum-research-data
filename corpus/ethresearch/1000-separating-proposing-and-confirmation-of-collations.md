---
source: ethresearch
topic_id: 1000
title: Separating proposing and confirmation of collations
author: vbuterin
date: "2018-02-04"
category: Sharding
tags: [proposal-commitment]
url: https://ethresear.ch/t/separating-proposing-and-confirmation-of-collations/1000
views: 7119
likes: 9
posts_count: 11
influence_score: 0.95
research_thread: sharding
---

# Separating proposing and confirmation of collations

In standard chain-based consensus algos, *proposal* of transaction packages and *confirmation*  of proposals are the same process; a block/collation is simultaneously a proposal for a new transaction package to be added to the history and a vote in the process of confirming previous blocks.

As discussed in the [previous post on consensus/execution separation](https://ethresear.ch/t/delayed-state-execution-finality-and-cross-chain-operations/987), even if consensus on transaction ordering and state calculation are separated, the nodes participating in the transaction ordering process still need to have access to the state, and still need to perform state executions, because they need to know whether or not the transactions they accept will pay for gas.

However, we could conceivably go one step further, and separate the sharded chain into **three** processes:

1. Collation proposal
2. Collation consensus
3. State execution

(2) **must** have the property that a participant is not local to any single shard, but rather bounces between shards very rapidly, so that one cannot attack the system by just corrupting a few validators in one particular shard. However, as I already mentioned in the previous post, (3) does *not* need this property, because state execution is not a consensus game; it can be designed in a Truebit-style interactive protocol which leads to correct answers even if more than 90% of the participants are malicious.

Here, I will go further and posit that participants in (1) can also be local to one specific shard. This means that participants in (2) would not need to deal with stateless client mechanisms, witnesses and other related mechanics at all, and would simply need to adjudicate availability of regular blocks.

One possible mechanism is simple: anyone can make and sign proposals (ie. packages of transactions) for any shard, and each proposal must contain a “pass-through fee”. A collation is made in the usual way, except instead of including transactions directly, a collation simply includes exactly one proposal. The pass-through fee of the proposal is deducted from the proposer and given to the collator on the VMC level. In this way, proposers *do* need to specialize in making proposals for particular shards, but validators do not need to concern themselves with this at all, as the fee that they receive is guaranteed as part of the proposal header.

Note that one could replicate something similar extra-protocol by having validators outsource the job of making proposals with cryptoeconomic proofs. Validators could solicit collation proposals, where each proposal would come with a signed message signed by a user with a bonded security deposit, saying “if you make a collation in this period on top of this parent, using these transactions, then either your balance will increase by at least XXX ETH due to fees, or I will pay the difference out of my bond”.

Either approach allows validators who need to frequently bounce between shards to not need to worry about the state of any specific shard, allowing specialized nodes to perform the (state-demanding) task of actually creating collations for each shard.

## Replies

**JustinDrake** (2018-02-04):

The separation of collation proposal and consensus makes a lot of sense, beautiful! ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=9)

A few misc remarks:

1. While I pushed back on collation proposals being necessarily state-demanding to access the log inclusion fee market, I can see how being aware of state can only help optimising utility/revenue beyond the log inclusion fee market, and this edge could become a point of centralisation.
2. Outsourcing collation proposals to proposers also means offloading data availability proofs (see Phase 4 of current roadmap). Those proofs can be very heavy computationally (e.g. based on SNARKs/STARKs) so offloading them to specialised proposers seems appropriate to avoid giving computationally powerful validators an edge.
3. One of the thing I liked about having precisely one proposer per period is that (unlike PoW) there is no “waste” with multiple proposers simultaneously building collations and competing. When we separate collation proposal and consensus, we reintroduce this competition with proposers trying to sell to validators the most profitable collation proposals.
4. A “zen philosophy” for protocol design is “embrace whatever you don’t control”. In this case, because collation proposal and consensus can be separated via extra-protocol means, we might as well embrace a clean separation at the protocol layer.

---

**denett** (2018-02-05):

I assume the collators will just pick the proposal with the highest pass-through fee.

Does this not make it easy for a proposer to censor a transaction by paying a high pass-through fee for collations without a certain transaction?

---

**vbuterin** (2018-02-06):

Yes, but in the current system a proposer can censor a transaction by just not including it.

---

**denett** (2018-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Yes, but in the current system a proposer can censor a transaction by just not including it.

In the current system every collation is proposed by a different validator. If you want to censor a transaction for several collations in a row, you have to bribe all validators responsible for those collations. When we have lookahead privacy, it is unknown which validator to bribe. You could try to send a lot of high gas price transactions to keep the target transaction out, but that is expensive and users will notice.

In the proposed system an attacker can make a proposal for every collation. By running a small loss on the pass-through fee, the proposer can censor the target transaction. This is a lot cheaper and attracts less attention.

---

**JustinDrake** (2018-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> One possible mechanism is simple: anyone can make and sign proposals (ie. packages of transactions) for any shard, and each proposal must contain a “pass-through fee”.

A problem with this mechanism is that proposals are public so validators can steal the contents of the packages without rewarding proposers. Below is another scheme.

**Construction**

- Anyone can propose unsigned collation headers, keeping the corresponding collation bodies secret
- Each unsigned collation header has a guaranteed proposer’s fee paid by the proposer to the validator if:

Signing: The collation header is signed by the validator
- Inclusion: The signed collation header is included in the VMC in the validator’s period
- Exclusivity: The signed collation header does not conflict with another collation header in the validator’s period

**Notes**

1. Validators sign collation headers without full knowledge of the collation bodies, and facilitate the inclusion of the signed collation headers in the VMC.
2. The market of collation proposals effectively becomes an open auction, similar to transaction fees today.
3. Proposers are responsible to collect coinbase rewards and transaction fees (including out-of-band transaction fees). They don’t have to disclose this revenue to proposers.
4. Validators get the “lump” proposer’s fee without worrying about transaction fees. This aggregation service is nice for validators because transaction fees will be micro-fees spread out across shards and asset types (account abstraction allows to pay non-ETH transaction fees).
5. Proposers are responsible for data availability of the collation bodies after the collation header is added to the VMC. In particular, the validator’s fee is paid even if the collation body is not properly made available by the proposer.
6. Validators get paid even if the collation header gets orphaned. Individual proposers follow their own preferred fork choice rules when making proposals, and take on the corresponding orphanage risk.
7. Validators can still have some say as to what goes in the collation bodies. For example, they can request particular transactions to be included and the proposers can provide Merkle proofs of inclusion alongside the proposals.

---

**vbuterin** (2018-02-07):

I… preliminarily like this.

Proposers taking on orphanage risk seems a bit iffy but it does seem necessary for the scheme to work.

I see a few weird effects:

1. Once a proposal is made, the proposer has a 1:1 griefing attack against the validator by not publishing the proposal. That said, in a simple blockchain, the validator of a child block has a 1:2 griefing attack against the validator of the parent by building on top of the grandparent instead, so this isn’t that much worse.
2. If all transactions in a proposed collation have been broadcasted, then it may be possible to reconstruct the collation from just the header. This would allow validators to piggyback off of proposers’ state computation and transaction selection efforts for free and claim the fee revenue for themselves. However, this could easily be mitigated by allowing the full collation body to contain even one secret parameter (eg. coinbase) that is not visible from the header.
3. A new censorship vector appears: a censoring attacker could dominate proposing in a particular shard and subsidize their proposed collations that exclude transactions from some account; the validators would have no idea that this is happening. However, this still has the property that censors would have to outbid the transactions they want to exclude for every block that the transactions are being excluded, so it’s not much worse than simple transaction spam.

---

**JustinDrake** (2018-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Proposers taking on orphanage risk seems a bit iffy but it does seem necessary for the scheme to work.

The rationale for having proposers (at least partially) taking on orphanage risk is that proposers can grief validators by never making the collation body available to force an orphan and waste the validator’s period. Two alternatives I can see:

1. Remove the exclusivity condition in the VMC so that multiple proposals can compete, significantly mitigating the collation body withdrawal attack.
2. Have the proposer eventually broadcast a data availability proof of the collation body so the validator can safely take on orphanage risk.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Once a proposal is made, the proposer has a 1:1 griefing attack against the validator by not publishing the proposal.

Having the proposer’s fee be guaranteed regardless of availability of the collation body is to protect validators against this attack.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If all transactions in a proposed collation have been broadcasted, then it may be possible to reconstruct the collation from just the header.

Reconstructing the collation from the header is not computationally feasible. For example, the proposer has full control over the coinbase address which can be used as a private nonce.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A new censorship vector appears: a censoring attacker could dominate proposing in a particular shard and subsidize their proposed collations that exclude transactions from some account

I’d argue this censorship vector has always been (hidden) there, although this scheme makes it obvious and provides the infrastructure to more readily execute this attack. An attacker today could bribe miners 20 ETH per empty block to stall the Ethereum blockchain.

---

**vbuterin** (2018-02-07):

> Having the proposer’s fee be guaranteed regardless of availability of the collation body is to protect validators against this attack.

Ah, now that I think about it, you’re right; I got that the proposer’s money is lost if the block gets orphaned but didn’t see that the validator gets the money. Point taken ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

I was worried for a bit that this would introduce a way for the validator to grief the proposer, but that can’t happen because publication of the full collation data is under the proposer’s full control.

---

**rauljordan** (2018-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Proposers are responsible to collect coinbase rewards and transaction fees (including out-of-band transaction fees). They don’t have to disclose this revenue to proposers.

Can you elaborate more on this? Proposers will be rewarded a part of the coinbase ETH once a supernode appends a block describing their specific collations headers to the main chain, correct?

---

**JustinDrake** (2018-03-01):

Welcome to ethresear.ch Raul ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/rauljordan/48/740_2.png) rauljordan:

> Proposers will be rewarded a part of the coinbase ETH once a supernode appends a block describing their specific collations headers to the main chain, correct?

There are effectively two coinbase addresses, one for the validator and one for the proposer. It makes sense to have the proposer directly receive transaction fees, but there is flexibility as to how we allocate the collation subsidies. We can design the protocol to give collation subsidies in full to the proposer, in full to the validator, or something in between. My initial idea was to give the collation subsidy in full to the proposer to mitigate the proposer griefing the validator by withholding the collation body. I’m now leaning towards giving the collation subsidy in full to the validator for the validator to take responsibility for availability of collation bodies with [this scheme](https://ethresear.ch/t/alternative-fix-for-proposer-withholding-attack/1268).

