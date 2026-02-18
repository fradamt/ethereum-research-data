---
source: ethresearch
topic_id: 922
title: Fork choice rule for collation proposal mechanisms
author: JustinDrake
date: "2018-01-26"
category: Sharding
tags: []
url: https://ethresear.ch/t/fork-choice-rule-for-collation-proposal-mechanisms/922
views: 4225
likes: 0
posts_count: 8
---

# Fork choice rule for collation proposal mechanisms

The current [sharding phase 1 doc](https://github.com/ethereum/sharding/blob/develop/docs/doc.md) specifies running the proposer eligibility function `getEligibleProposer` onchain. We suggest an alternative approach based on a fork choice rule, complemented with optional “partial validation” and slashing.

The benefit of the fork choice rule is that `getEligibleProposer` is run offchain. This saves gas when calling `addHeader` and unlocks the possibility for fancier proposer eligibility functions. At the end we detail two proposal mechanisms, one for variable-size deposits and one for private sampling.

**Fork choice rule**

Collation validity is currently done as a fork choice rule, and collation header validity is done onchain with `addHeader`. We suggest extending the fork choice rule to collation headers as follows:

- addHeader always returns True, and always records a corresponding CollationAdded log
- getEligibleProposer is run offchain and filtering of invalid collation headers is done as a fork choice rule

For the logic to fetch candidate heads (c.f. [fetching in reverse sorted order](https://github.com/ethereum/sharding/blob/develop/docs/doc.md#fetch-candidate-heads-in-reverse-sorted-order)) to work and the fork choice rule to be enforceable, the `CollationAdded` logs need to be filterable for validity post facto. This relies on historical data availability of validator sets (and other auxiliary data for sampling, such as entropy).

We are already assuming that the historical `CollationAdded` logs are available so it suffices to extend this assumption to validator sets. A clean solution is to have `ValidatorEvent` logs for additions and removals, and an equivalent `getNextLog` method for such logs.

**Partial validation and slashing condition**

To simplify the fork choice rule and lower the dependence on historical availability of validator sets, there are two hybrid approaches that work well:

1. Partial validation: have addHeader return True only if the signature sig corresponds some collaterised validator
2. Slashing condition (building upon partial validation): if the validator that called addHeader does not match getEligibleProposer (run offchain) then a whitleblower can run getEligibleProposer onchain to burn half the validator’s deposit and keep the other half

**Variable-size deposits**

Let v_1, ..., v_n be the validators with deposits d_1, ..., d_n. Fairly sampling validators when the d_i can have arbitrary size can be tricky because the amount of work to run `getEligibleProposer` is likely bounded below by log(n), which is not ideal. With the fork choice rule we can take any (reasonable) fair sampling function and run it offchain.

For concreteness let’s build `getEligibleProposer` as follows. Let E be 32 bytes of public entropy (e.g. a blockhash, as in the phase 1 sharding doc). Let S_j be the partial sums d_1 + ... + d_j and let \tilde{E} \in [0, S_n-1] where \tilde{E} \equiv E \mod S_n. Then `getEligibleProposer` selects the validator v_i such that S_{i-1} \le \tilde{E} \lt S_i.

**Private sampling**

We now look at the problem of private sampling. That is, can we find a proposal mechanism which selects a *single* validator per period and provides “private lookahead”, i.e. it does not reveal to others which validators will be selected next?

There are various possible private sampling strategies (based on MPCs, SNARKs/STARKs, cryptoeconomic signalling, or fancy crypto) but finding a workable scheme is hard. Below we present our best attempt based on one-time ring signatures. The scheme has several nice properties:

1. Perfect privacy: private lookahead and private lookbehind (i.e. the scheme never matches eligible proposers with specific validators)
2. Full lookahead: the lookahead extends to the end of the epoch (epochs are defined below, and have roughly the same size as the validator set)
3. Perfect fairness: within an epoch validators are selected proportionally according to deposit size, with zero variance

The setup assumes validators have deposits in fixed-size increments (e.g. multiples of 1000 ETH). Without loss of generality we have one validator per fixed-size deposit. The proposal mechanism is organised in variable-size epochs. From the beginning of each epoch to its end, every validator has the right to push a log to be elected in the next epoch. The log contains two things:

1. A once-per-epoch ring signature proving membership in the current validator set
2. An ephemeral identity

The logs are ordered chronologically in an array, and the size of the array at the end of one epoch corresponds to the size of the next epoch (measured in periods). To remove any time-based correlation across logs, we publicly shuffle the array using public entropy. This shuffled array then constitutes a sampling, each entry corresponding to one period. To call `addHeader`, the validator selected for a given period must sign the header with the corresponding ephemeral identity.

With regards to publishing logs, [log shards](https://ethresear.ch/t/log-shards-and-emv-abstraction/747) work well for several reasons:

1. They provide cheap logging facilities (data availability, ordering, witnesses)
2. Gas is paid out-of-bound so this limits opportunities to leak privacy through onchain gas payments

## Replies

**vbuterin** (2018-01-26):

justin:

> getEligibleProposer is run offchain and filtering of invalid collation headers is done as a fork choice rule

Interesting ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

The main concern I have is the practical efficiency issue. The scheme you propose would make it very easy to do a “51% attack” so that the longest chain in the VMC would be an invalid chain, and so clients would absolutely be required to check every single header in the chain personally. There would no longer be an easy option to “fast sync”.

Given that, in the current fixed validator size status quo, the cost of running `getEligibleProposer` is trivial, it’s not clear that the benefit of this kind of change is worth the cost, including the protocol and client complexity cost (currently, the complexity is literally 2-4 lines of code in the contract).

Additionally, even if we want to take the log(N) approach (see implementation here; it’s surprisingly simple [casper/misc at master · ethereum/casper · GitHub](https://github.com/ethereum/casper/tree/master/misc)), the gas cost is only O(log(N)) 200-gas SLOADs, so it should be under 4k gas. I actually now think that I was wrong to have been so uncomfortable with the O(log(N)) approach earlier.

Brilliant job on the ring signature-based lookahead-free validator selection!

---

**JustinDrake** (2018-01-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The scheme you propose would make it very easy to do a “51% attack” so that the longest chain in the VMC would be an invalid chain, and so clients would absolutely be required to check every single header in the chain personally. There would no longer be an easy option to “fast sync”.

This is where partial validation and the slashing condition come in—with them doing a “51% attack” is basically equally hard as before, and fast sync works the same. Slashing acts as a finality mechanism reducing the “global” fork choice rule to a “local” fork choice for the last mile (the time it takes for whistleblowers to react). An attacker wanting to push a single phoney collation header will lose the minimum deposit (say, 1000 ETH), so an attack quickly becomes prohibitively expensive, and validators checking the last few headers is sufficient.

---

**kladkogex** (2018-02-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> We now look at the problem of private sampling. That is, can we find a proposal mechanism which selects a single validator per period and provides “private lookahead”, i.e. it does not reveal to others which validators will be selected next?

Have you considered using a [Common Coin algorithm](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.66.4165&rep=rep1&type=pdf) ? It provides a way for a set of nodes to generate a  common secure random number even if some of the nodes are Byzantine.

You could just generate a common random number C at the beginning of each block proposal, and then choose  validator index I as I = C \% N

The CommonCoin algorithm takes less than a second to run in a realistic network with realistic latencies.  HoneyBadger and Algorand use a common coin instance for each block.  Ethereum could also run it for each block, or for each 10 blocks.

---

**JustinDrake** (2018-02-01):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Have you considered using a Common Coin algorithm ?

I’ve lately been studying dfinity’s random beacon based on threshold signatures. I imagine that’s what you are referring to. It is indeed a pretty awesome way to generate randomness as an alternative to, say, blockhashes or RANDAO.

Having said that, I don’t think that it really helps much for private sampling other than improving the source of randomness to already proposed private sampling schemes. I don’t think the specific scheme you propose has either lookahead privacy or lookbehind privacy.

---

**kladkogex** (2018-02-02):

Hi Justin,

I am referring to “coin tossing schemes” (Page 11 of [this])(http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.66.4165&rep=rep1&type=pdf). Essentially there are 3t + 1 parties, out of which t are bad.

The protocol allows for good guys to generate a random number in O(1) time even if the bad guys do not cooperate. It is used in some protocols, such as HoneyBadger. It is based on threshold signatures - in fact, once you have a deterministic threshold signature,  you could just take the hash of the signature as a common random number.

What I am saying one could do, is at the start of each block proposal one could generate a common random number which would determine the block proposer for this block.

I will ready your proposal in more detail,  I have a suspicion that it can be reformulated as a solution of the “coin tossing”  scheme using a blockchain.  May be it is better for the particular application of block proposal …

---

**JustinDrake** (2018-02-02):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> at the start of each block proposal one could generate a common random number which would determine the block proposer for this block

The definition of lookahead privacy is that *only* the next block proposer knows he will be the next block proposer. In the scheme you suggest *all* validators know who will be the next block proposer.

---

**kladkogex** (2018-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The definition of lookahead privacy is that only the next block proposer knows he will be the next block proposer. In the scheme you suggest all validators know who will be the next block proposer.

Yes … An interesting question is whether common coin can be modified somehow to preserve privacy …

