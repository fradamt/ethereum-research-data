---
source: ethresearch
topic_id: 1486
title: PoS Plasma Cash with Sharded Validation
author: karl
date: "2018-03-24"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/pos-plasma-cash-with-sharded-validation/1486
views: 9252
likes: 12
posts_count: 8
---

# PoS Plasma Cash with Sharded Validation

A very special thanks to [@JustinDrake](/u/justindrake)  for all the yummy availability help!

# Overview

Plasma Cash, as defined in the [Simple Spec](https://karl.tech/plasma-cash-simple-spec/), relies on a single Plasma operator. This operator has two strategies which can cause some harm to users of the Plasma Cash chain. The strategies are as follows:

**i)** The Plasma operator can withhold a single block, forcing all users to exit the chain before they can spend their coins.

**ii)** The Plasma operator can censor and order transactions.

Because these two strategies exist, users must place significant trust in the central Plasma operator. With these constraints, Plasma Cash would be most comparable to a much safer centralized exchange. We might see multiple Plasma Cash instances, each one being run by a single operator who looks similar to the current centralized exchange operators we have today. This is great for removing any chance of coin theft, but each Plasma Cash chain would end up competing.

An alternative vision for Plasma Cash is, through the use of a PoS sharding solution, constrain the Plasma operators in order to minimize trust. To do this we extend the Plasma Cash Simple Spec with the following alterations:

**a)** Decentralize block finalization with proof of stake consensus, to mitigate operator strategy (i).

**b)** Rotate block proposers, to mitigate operator strategy (ii).

With these changes, Plasma Cash operators no longer have privileged status. Multiple exchange-like entities can use the same Plasma Cash chain as block proposers. These proposers are constantly cycled in and out. Without privileged status, users and service providers can pool their liquidity into a single large Plasma Cash chain.

# Sharding Validation

Plasma Cash is special because it allows for extremely large blocks. This is what provides its scalability. However, this is problematic for PoS validation because naively all validators would have to download and validate each block. With huge bandwidth and verification requirements, validators would be restricted to well connected data centers–a large centralization vector.

How do we solve this? Well we shard validation! How do we shard validation? There are a number of reasonable schemes. One possibility is a [DFinity-style scheme using BLS signatures](https://dfinity.org/pdf-viewer/pdfs/viewer?file=../library/dfinity-consensus.pdf) & an honest majority assumption. This is the scheme assumed to be used in this spec, but further exploration regarding sharded availability schemes is *very* valuable. Please research!

# Protocol Overview

### Bonded Participants

1. A large set of validators, each with a bond of X tokens at stake in the Plasma contract on the mainchain.
2. A set of block proposers with a large bond of tokens on the mainchain.

### Step by step

1. A Plasma block proposer is selected. This can be done with limited predictability or even privately.
2. The block proposer collects huge numbers of transactions and creates a huge block (merkle tree). I don’t want to make promises, but I’d say the number of transactions can be pretty massive
3. Proof of Stake validators are pooled into committees, which are randomly sampled to validate subsections of the block’s merkle tree.
4. Block proposer distributes subsections of the merkle tree to relevant validators.
5. Validators check availability & validity of the transactions, and sign a message approving the subsection of the merkle tree.
6. If a majority of validators in each committee sign off on availability & validity, the Plasma Cash block is included in the main chain. We use BLS signatures so the on-chain overhead is simply checking a single signature. It is important to note this signature verification does cost ~200,000 gas which is rather pricy.
7. Validators propagate merkle branches of coins to relevant users.
8. Repeat step (1).

The following is a diagram which further describes this process:

[![](https://ethresear.ch/uploads/default/optimized/2X/9/9a9c67ceeb21364c5314c78bef410d82961a61fd_2_398x500.jpg)1182×1482 253 KB](https://ethresear.ch/uploads/default/9a9c67ceeb21364c5314c78bef410d82961a61fd)

# Closing Thoughts

### Data Availability

Fundamentally the most critical component to this mechanism is its guarantees around data availability. If all data is available, a Plasma Cash chain can live forever. However, data availability is one of the most difficult problems in the blockchain scalability space.

A DFinity-style scheme guarantees data availability with an honest majority assumption (66%+). However, ideally we can weaken these assumptions in the long term with [fraud proofs and erasure encoding](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding).

### Slashing

Slashing conditions can be added to the Plasma block proposers. Some example slashing conditions can be:

1. Slash if an invalid state transition is included in a block.
2. Slash if two conflicting blocks are signed for the same block height.

The first rule protects against invalid state transitions, and the second rule provides stronger guarantees around a kind of “soft finality” when a block is included in the mainchain Plasma contract. The only way for a block which is signed by a proposer to not be included would be if the Plasma operator slashed themselves. The amount of coins slashed can be tuned but potentially could go very high.

### Censorship

In a single block proposer approach, transaction censorship is a big problem. The operator could blacklist coins and just never include transactions which reference these coins. With block proposer rotation, a single censorship-free block proposer can ensure censorship resistance.

### Next Steps

- Better sharding schemes with weaker honesty assumptions.
- Concise exit challenge-response scheme even on coins which have had invalid transactions included in the Plasma chain.
- State channels for instant finality! This could be useful for trading with high throughput. Please please please tell me how to do this!

#  One Love

## Replies

**vbuterin** (2018-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/karl/48/9_2.png) karl:

> reorder

There’s an important distinction here between two meanings of “reorder”:

1. Decide on the order at the time, possibly for front-running or other manipulative purposes.
2. Manipulate the order after the fact.

Centralized Plasma lets the operator do (1), but not (2).

> b) Rotate block proposers, to mitigate operator strategy (ii).

This is better, but still imperfect, because individual proposers can extract rent from front-running during the blocks that they create. One technology that is really worth considering is leader-free consensus algorithms of the sort that were researched and pioneered by Dominic Williams: [x.com](https://twitter.com/dominic_w/status/932047605386924032) ; here, there is no single actor that manipulates transaction ordering, and actually manipulating ordering effectively requires an actor that has close to 1/3 of the entire validator set.

Now that I think about it, one really interesting direction in which to drag the whole Plasma concept is in allowing individual applications to essentially choose their own block proposal mechanisms that they give priority to transactions; this would allow the emergence of a market in solutions that provide low-latency and anti-front-running properties, allowing those problems to be solved in multiple ways where applications can choose which tradeoffs they want.

---

**phil** (2018-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This is better, but still imperfect, because individual proposers can extract rent from front-running during the blocks that they create.

Exactly this.  You’ve traded one actor who can frontrun you for a set, which is better than a centralized Plasma chain, but is exactly the situation we have with PoW mining today.

---

**ldct** (2018-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/karl/48/9_2.png) karl:

> State channels for instant finality! This could be useful for trading with high throughput. Please please please tell me how to do this!

It’s worth pointing out that there are two different delays which state channels can help with:

1. users withdrawing plasma-ETH and redeeming ETH, which takes 14 days
2. users trading on the plasma chain (e.g. swapping 1 MKR for 20 REP with a counterparty on the plasma chain), which normally takes about 300 seconds (the time to commit a plasma block header to the plasma contract, then waiting for ethereum block confirmations)

for the first delay, even implementing cross-chain atomic swaps can bring the delay down to 300 seconds-ish; users will do cross-chain swaps with “liquidity providers” who maintain plasma-ETH and ETH balances and rebalance them using deposits and exits.

---

**jannikluhn** (2018-03-25):

What happens if a proposer does not propose (because he’s malicious, he’s DDoSed, or just because his machine crashed)? I guess there’s some mechanism to skip proposers?

> State channels for instant finality! This could be useful for trading with high throughput. Please please please tell me how to do this!

Not state channels, and only for reduced latency and not increased throughput, but something like this might be interesting (from [Layer-2 solutions for latency reduction and anti-front-running](https://ethresear.ch/t/layer-2-solutions-for-latency-reduction-and-anti-front-running/1487)):

> The proposal mechanism would be able to cryptoeconomically commit to including transactions potentially much faster than the block time.

For Plasma Cash, such a scheme could work something like this:

1. Sender sends transaction to proposer
2. Proposer responds with signed receipt
3. If the proposer does not include the transaction, the sender can challenge on the main chain with the receipt and a proof of non-inclusion. During a counter-challenge period the proposer can submit a proof that the transaction has already been included in an earlier block. If he fails to do so, he gets slashed.

As a result, the sender will instantly know the following:

1. either my transaction gets included
2. or the proposer gets slashed
3. or the proposer didn’t propose (or proposed an invalid/unavailable block) and thus forfeited transaction fees of a full block

---

**danrobinson** (2018-03-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Now that I think about it, one really interesting direction in which to drag the whole Plasma concept is in allowing individual applications to essentially choose their own block proposal mechanisms that they give priority to transactions; this would allow the emergence of a market in solutions that provide low-latency and anti-front-running properties, allowing those problems to be solved in multiple ways where applications can choose which tradeoffs they want.

Another cool thing you could do is move a coin from one Plasma Cash chain to another, *without ever touching the parent chain*. You post a “transfer” transaction on the coin’s origin chain (the one where it was originally deposited from the parent chain), at its current slot and signed by the current owner, which specifies a destination chain, a minimum block height on that chain, and a slot in the Merkle tree where transactions will be posted (which could be the same one, but doesn’t have to be). The destination chain would then be responsible for tracking that token until it moves to another chain. The proof of valid history for a coin would involve following the coin as it hopped from chain to chain.

When you want to withdraw a coin to the parent chain, you make the request to the *original chain* that it was deposited on, and provide the coin’s current location, including what chain it’s on. (This will require all Plasma contracts to expose a common interface for verifying a proof that a transaction exists. Other than that, there’s no requirements about how those contracts are implemented; they could use a completely different consensus mechanism from the origin chain.) You could do a TrueBit-style challenge-response game to narrow down what Plasma chain contains the disputed history in log(N) (in the number of chain hops) steps, at which point you’re just a single step away. Maybe you can do even better than that.

---

**bharathrao** (2018-04-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/karl/48/9_2.png) karl:

> One possibility is a DFinity-style scheme using BLS signatures  & an honest majority assumption.

A simple signature per head may be open to sybil attack. Is it possible to weigh the signatures by stake size to mitigate this?

---

**kfichter** (2018-04-21):

I think in the case of DFINITY this is accomplished by requiring each node place a stake. If I want to control more “weight”, I just control more nodes (each requires stake). So it’s anti-sybil and basically weighted, but it’s not clean. Does a construction for weighted threshold BLS signatures exist?

