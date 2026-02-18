---
source: ethresearch
topic_id: 11763
title: "Whisk: A practical shuffle-based SSLE protocol for Ethereum"
author: asn
date: "2022-01-13"
category: Consensus
tags: [single-secret-leader-election]
url: https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763
views: 15851
likes: 32
posts_count: 22
---

# Whisk: A practical shuffle-based SSLE protocol for Ethereum

**EDIT (01/08/2023): Remove any mention of permutation commitments (we don’t need them)**

**EDIT (01/08/2023): Replace [Feistelshuffle](https://github.com/khovratovich/whisk-analysis/blob/ba6a4b1374efe56ebbde692c7fc3b549d1eb0133/WhiskAnalysis.pdf) with the [simplified shuffling strategy](https://eprint.iacr.org/2022/560)**

Hello all,

we are happy to present you **Whisk**: a block proposer election protocol tailored to the Ethereum beacon chain that protects the privacy of proposers.

Whisk is a modified version of the `SSLE from DDH and shuffles` scheme from the paper [“Single Secret Leader Election” by Boneh et al.](https://eprint.iacr.org/2020/025.pdf) and is based on mixnet-like shuffling.

Along with the proposal, we also provide a [feature-complete draft implementation of Whisk](https://github.com/ethereum/consensus-specs/pull/2800) in the consensus-specs format, in an attempt to demonstrate and better reason about the overall complexity of the project. We link to the code throughout the proposal so that the reader gets a better understanding of how the system works.

Please treat this proposal as a draft that will be revised based on community feedback.

- We are particularly interested in feedback about how Whisk compares to VRF-based solutions (like SASSAFRAS) and specifically how hard it would be to fit SASSAFRAS’ networking model into our networking model.
- We are also interested in feedback about active RANDAO attacks against Whisk, and potential protocol variations that could improve the trade-offs involved.

It’s a read, so we invite you to brew some hot coffee, put on some tunes, recline and enjoy the proposal and the code!

Cheers!

PS: We also put the proposal [on a hackmd](https://hackmd.io/@asn-d6/HyD3Yjp2Y) in case people want to add inline comments (also ethresearch did not allow me to post the entire proposal, so the appendix will be in a separate comment).

---

# Whisk: A practical shuffle-based SSLE protocol for Ethereum

## Introduction

We propose and specify Whisk, a privacy-preserving protocol for electing block proposers on the Ethereum beacon chain.

## Motivation

The beacon chain currently elects the next 32 block proposers at the beginning of each epoch. The results of this election are public and everyone gets to learn the identity of those future block proposers.

This information leak enables attackers to **launch DoS attacks** against each proposer *sequentially* in an attempt to disable Ethereum.

## Overview

This proposal attempts to plug the information leak that occurs during the block proposer election.

We suggest using a secret election protocol for electing block proposers. We want the election protocol to produce a **single** winner per slot and for the election results to be **secret** until winners announce themselves. Such a protocol is called a *Single Secret Leader Election* (SSLE) protocol.

Our SSLE protocol, Whisk, is a modified version of the `SSLE from DDH and shuffles` scheme from the paper [“Single Secret Leader Election” by Boneh et al.](https://eprint.iacr.org/2020/025.pdf). Our [zero-knowledge proving system](https://ethresear.ch/t/provable-single-secret-leader-election/7971) is an adaptation of the [Bayer-Groth shuffle argument](http://www0.cs.ucl.ac.uk/staff/J.Groth/MinimalShuffle.pdf).

This proposal is joint work with Justin Drake, Dankrad Feist, Gottfried Herold, Dmitry Khovratovich, Mary Maller and Mark Simkin.

### High-level protocol overview

Let’s start with a ten thousand feet view of the protocol.

The beacon chain first randomly picks a set of election candidates. Then and for an entire day, block proposers continuously shuffle that candidate list thousands of times. After the shuffling is finished, we use the final order of the candidate list to determine the future block proposers for the following day. Due to all that shuffling, only the candidates themselves know which position they have in the final shuffled set.

For the shuffling process to work, we don’t actually shuffle the validators themselves, but cryptographic randomizable commitments that correspond to them. Election winners can *open their commitments* to prove that they won the elections.

To achieve its goals, the protocol is split into events and phases as demonstrated by the figure below. We will give a high-level summary of each one in this section, and then dive into more details on the following sections:

- Bootstrapping event               – where the beacon chain forks and the protocol gets introduced
- Candidate selection event         – where we select a set of candidates from the entire set of validators
- Shuffling phase                   – where the set of candidates gets shuffled and re-randomized
- Cooldown phase                    – where we wait for RANDAO, our randomness beacon, to collect enough entropy so that its output is unpredictable
- Proposer selection event          – where from the set of shuffled candidates we select the proposers for the next day
- Block proposal phase              – where the winners of the election propose new blocks

[![](https://ethresear.ch/uploads/default/optimized/2X/5/58a7d0a3cbbf792d781acbf582b2895aa7e68ed0_2_690x184.png)1054×282 38.3 KB](https://ethresear.ch/uploads/default/58a7d0a3cbbf792d781acbf582b2895aa7e68ed0)

### Document overview

In the [following section](#Protocol) we will be diving into Whisk; specifying in detail the cryptography involved as well as the protocol that the validators and the beacon chain need to follow.

After that, we will perform a [security analysis](#Security-analysis) of Whisk, in an attempt to understand how it copes against certain types of attacks.

Following that we will [calculate the overhead](#Overhead-analysis) that Whisk imposes on Ethereum in terms of block and state size, as well as computational overhead.

We will then move into an analysis of [alternative approaches](#Related-work) to solve the problem of validator privacy and compare their trade-offs to Whisk.

We close this proposal with a [discussion section](#Discussion) which touches upon potential simplifications and optimizations that could be done to Whisk.

---

## Protocol

In this section, we go through the protocol in detail.

We start by introducing the cryptographic commitment scheme used. We proceed with specifying the candidate and proposer selection events, and then we do a deep dive into the shuffling algorithm used.

We have written a [feature-complete draft consensus implementation of Whisk](https://github.com/ethereum/consensus-specs/pull/2800). Throughout this section, we link to specific parts of the code where applicable to better guide readers through the protocol.

### Commitment scheme

For the shuffling to work, we need a commitment scheme that can be randomized by third parties such that the new version is unlinkable to any previous version, yet its owner can still track the re-randomized commitment as her own. Ideally, we should also be able to open commitments in a zero-knowledge fashion so that the same commitment can be opened multiple times. We also need Alice’s commitment to be *bound to her identity*, so that only she can open her commitment.

We use the commitment scheme suggested by the SSLE paper where Alice commits to a random long-term secret k using a tuple (rG, krG) (called a *tracker* [in this proposal](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L88)). Bob can randomize Alice’s tracker with a random secret z by multiplying both elements of the tuple: (zrG, zkrG). Finally, Alice can prove ownership of her randomized tracker (i.e. open it) by providing a *proof of knowledge of a discrete log* (DLOG NIZK) that proves knowledge of a k such that k(zrG) == zkrG.

Finally, we achieve *identity binding* by having Alice provide a deterministic commitment com(k) = kG when she registers her tracker. We store com(k) in [Alice’s validator record](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L97), and use it to check that [no two validators have used the same k](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L266). We also use it at registration and when opening the trackers to check that both the tracker and com(k) use the same k using a *discrete log equivalence proof* (DLEQ NIZK). Fr more details see the [“Selling attacks” section](#Selling-attacks) of this document and the `duplication attack` section in the SSLE paper.

### Protocol flow

Now let’s dive deeper into Whisk to understand how candidates are selected and how proposing works. For this section, we will assume that all validators have registered *trackers*. We will tackle registration later in this document.

[![](https://ethresear.ch/uploads/default/optimized/2X/c/cf50c7896970040bdb477796e53bfc895f636b94_2_690x386.png)800×448 45.9 KB](https://ethresear.ch/uploads/default/cf50c7896970040bdb477796e53bfc895f636b94)

The protocol starts with the beacon chain using public randomness from RANDAO [to sample](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L109) 16,384 random trackers from the entire set of validators (currently around 250,000 validators). The beacon chain places those trackers into a *candidate list*.

After that and for an entire day (8,192 slots), block proposers *shuffle* and randomize the candidate list using private randomness. They also submit a zero-knowledge proof that the shuffling and randomization were performed honestly. During this shuffling phase, each shuffle only touches 128 trackers at a time; a limitation incurred by the ZKP performance and the bandwidth overhead of communicating the newly-shuffled list of trackers. The strategy used for shuffling will be detailed in the [next section](#Shuffling-phase).

After the shuffling phase is done, we use RANDAO to populate our *proposer list*; that is, to [select an ordered list](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L124) of the 8,192 winning trackers that represent the proposers of the next 8,192 slots (approximately a day). We [stop shuffling](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L251) one epoch before the *proposer selection* occurs, so that malicious shufflers can’t shuffle based on the future result of the RANDAO (we call this epoch the *cooldown phase*).

Finally, for the entire next day (8,192 slots), we [sequentially map the trackers](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L174) on the proposer list to beacon chain slots. When Alice sees that her tracker corresponds to the current slot, she can open her tracker [using a DLEQ NIZK](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L156) and submit a valid *block proposal*.

This means that the *proposal phase* lasts for 8,192 slots and the same goes for the *shuffling phase*. This creates a day-long pipeline of Whisk runs, such that when the *proposal phase* ends, the *shuffling phase* has also finished and has prepared the 8,192 proposers for the next day.

### Shuffling phase

In the previous section, we glossed over the strategy used by validators to shuffle the candidate list (of size 16,384) with small shuffles (of size 128). Shuffling a big list using small shuffles (called *stirs* from now on) requires a specialized algorithm, especially when a big portion of shufflers might be malicious or offline. We call our proposed algorithm **Randshuffle**.

##### Randshuffle

At every slot of the *shuffling phase*, the corresponding proposer picks 128 random indices out of the candidate list. The proposer *stirs* the trackers corresponding to those indices by permuting and randomizing them.

See [the Distributed Shuffling in Adversarial Environments paper](https://eprint.iacr.org/2022/560) for the security analysis of the *Randshuffle* algorithm.

### Proofs of correct shuffle

Validators [must use zero-knowledge proofs](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L256) to show that they have shuffled honestly: that is, to prove that the shuffle output was a permutation of the input and that the input trackers actually got randomized. If no such proofs were used, a malicious shuffler could replace all trackers with her own trackers or with garbage trackers.

We will now take a look at the zero-knowledge proofs used by Whisk.

Verifiable shuffling has been a research topic [for decades](http://www.lix.polytechnique.fr/~tomc/P2P/Papers/Theory/MIXes.pdf) due to [its application in mixnets](https://www.iacr.org/archive/eurocrypt2000/1807/18070563-new.pdf) and hence to online anonymity and digital election schemes. Already since twenty years ago, zero-knowledge proofs [based on randomizable ElGamal ciphertexts](https://www.iacr.org/archive/crypto2001/21390366.pdf) have been proposed, and in recent years we’ve seen proofs [based on CRS and pairings](https://eprint.iacr.org/2017/894.pdf) as well as [post-quantum proofs based on lattices](https://eprint.iacr.org/2019/357.pdf).

In Whisk we use shuffling ZKPs that solely rely on the discrete logarithm assumption and don’t require a trusted setup while still maintaining decent proving and verification performance. [Our proofs](https://ethresear.ch/t/provable-single-secret-leader-election/7971) are heavily based on [previous work on shuffling arguments by Bayer and Groth](http://www0.cs.ucl.ac.uk/staff/J.Groth/MinimalShuffle.pdf) and they also incorporate more recent optimizations inspired by the inner product arguments of [Bulletproofs](https://eprint.iacr.org/2017/1066.pdf).

We have [implemented an initial PoC](https://github.com/ethresearch/Shuffle_SSLE/tree/master/rust_code/src) of the shuffling proofs and we are working on a more robust implementation that includes test vectors and can be used as a solid basis for writing production-ready code for Ethereum clients.

### Bootstrapping

In all previous sections, we’ve been assuming that the system has bootstrapped and that all validators have Whisk trackers and commitments associated with them. In this section, we show how to do bootstrapping.

We bootstrap Whisk by having the beacon chain [initialize all validators](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/fork.md?plain=1#L76) with [dummy predictable commitments](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L338). We then allow validators to [register a secure commitment](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L299) when they propose a new block.

This means that the system starts in an insecure state where the adversary can predict future proposers (similar to the status quo), and as more validators register secure commitments, the system gradually reaches a secure steady state.

## Security analysis

In this section, we analyze Whisk’s security and privacy.

We first see how Whisk effectively expands the anonymity set of proposers. We then explore various active attacks that could be performed against Whisk: either by malicious shufflers or by the Ethereum randomness beacon (RANDAO). We close this section by demonstrating how Whisk is protected against selling attacks, where an adversary attempts to buy specific proposer slots.

### Anonymity set

The core idea of Whisk is to significantly increase the anonymity set of block proposers. In particular, the anonymity set increases from the status quo of a single validator to at least 8,192 validators (which correspond to the *number of candidates that did not get selected as proposers*)

To make this concrete, the adversary knows the identities of the validators that got selected as *candidates*. However, because of the shuffling phase, she cannot tell which of those validators got selected as *proposers* at the end of the protocol. This means that the 8,192 candidates that were not selected as proposers become the anonymity set for all proposers.

It’s worth noting that those 8,192 validators actually correspond to a significantly smaller number of nodes on the P2P layer. For example, the current validator set of 250,000 validators is represented [by about 5,000 P2P nodes](https://ethernodes.org/). While it’s not known how validators are distributed to this small number of nodes, for this analysis we can assume that the distribution follows something close to the Pareto principle where “20% of the nodes run 80% of the validators”. Doing [a simulation with this distribution](https://gist.github.com/asn-d6/1d972421667a23a0635f65cd5d12d0e7) we find that an anonymity set of 8,192 validators corresponds to 2,108 nodes on average. That is explained by the fact that even though there are some *“heavy nodes”* that will always appear in the anonymity set and will control a hefty portion of it, there is also a long tail of *“light nodes”* that run one or two validators that helps increase the size of the anonymity set.

Whisk can also be adapted to produce a bigger anonymity set by increasing the size of the *candidate list* while keeping the size of the *proposer list* the same. However, doing such a change requires analyzing our shuffling strategy to see if it can sufficiently shuffle a bigger *candidate list*. Alternatively, we could increase the size of our stirs but we would need to be certain that this does not render our ZKPs prohibitively expensive.

### Active attacks through RANDAO biasing

In this section, we analyze Whisk’s resilience against RANDAO biasing attacks. While we present the main results here, the detailed analysis can be found [in the Appendix](#Appendix-B-RANDAO-attacks).

Whisk uses RANDAO in the *candidate selection* and *proposer selection* events. This opens it up to potential RANDAO biasing attacks by malicious proposers. Since RANDAO is a commit-and-reveal protocol it enables attackers who control the last k proposers before the candidate/proposer selection event to choose between 2^k possible candidate or proposer lists. This quickly becomes profitable for rational attackers, since they can increase profit by abandoning the commit-and-reveal protocol and choosing the list that contains the maximal number of validators they control or that gives them control over specific proposer slots.

Similar attacks can also be performed on the current Ethereum proposer selection where we publicly sample 32 proposers at the beginning of each epoch using RANDAO (see figure below).

[![](https://ethresear.ch/uploads/default/optimized/2X/8/80ce9ba577742caa7428e9e9401f05b62edb5959_2_690x401.png)897×522 36.5 KB](https://ethresear.ch/uploads/default/80ce9ba577742caa7428e9e9401f05b62edb5959)

By comparing Whisk with the status quo, we found that while big adversaries can extract bigger profits in the status quo, Whisk allows even small adversaries to extract profits by attacking RANDAO once per day. Please see [the Appendix](#Appendix-B-RANDAO-attacks) for more details on the results.

One way to completely address such RANDAO attacks is to use an unbiasable VDF-based randomness beacon. However, until a VDF beacon gets deployed, such attacks pose a risk both against the status quo and the Whisk protocol.

One possible variation is to make the security of Whisk identical to the security of the status quo with regards to RANDAO attacks by spreading *candidate selection* and *proposer selection* over an entire day (as seen in the figure below) instead of doing them on a single moment in time. However, even the status quo security is not ideal, and by implementing this defense we complicate the protocol further.

![](https://ethresear.ch/uploads/default/optimized/2X/d/d25acca7ba39e01ee0a5bd5ea8a1fb7503638f90_2_690x75.png)

### Selling attacks

We want to prevent Mallory from being able to buy and open Alice’s k.

It’s important to prevent that since that would allow Mallory to buy proposer slots on the beacon chain from an automated auction smart contract, or it could also create a situation where a single k is opened by two validators causing problems with the fork choice.

The commitment scheme presented above prevents that by doing a uniqueness check against k using com(k), and also by saving com(k) in Alice’s validator record and making sure that whoever opens using k also has com(k) in their validator record.

Let’s walk through a potential selling scenario and see how the identity binding prevents it:

1. Alice registers (rG, krG), com(k)
2. Mallory registers (rG, prG), com(p) (she can’t register with k because of the uniqueness check)
3. …
4. During the proposal phase, (rG, krG) becomes the winning tracker
5. Mallory attempts to propose using k by sending a DLEQ NIZK that proves that k is both the dlog of k(rG) and also the dlog of com(k)=kG

In this case the beacon chain [would dig into Mallory’s validator record](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L180) and use com(p) as the instance when verifying the NIZK. At that point, the verification would fail and Mallory’s proposal would be discarded.

## Overhead analysis

In this section, we calculate Whisk’s overhead in terms of block and state size, as well as the computational overhead imposed on validators.

#### State size overhead

The overhead of Whisk on the `BeaconState` is 45.5MB for 300k validators. In detail:

- a candidate list (16,384 trackers) (16,384*96 = 1.57 MB)
- a proposer list (8,192 trackers) (8,192*96 = 0.78 MB)
- a tracker for each validator (96 bytes per validator) (28.8 MB for 300k validators)
- a com(k) for each validator (48 bytes per validator) (14.4 MB for 300k validators)

In more detail, each validator is currently adding 139 bytes to the state, but with Whisk it will add 283 bytes.

This represents a dramatic increase in the size of the `BeaconState` (currently sitting at 30MB).

It’s worth noting that the tracker and com(k) of each validator (43.2MB for 300k validators) never change once they get registered which allows implementations to save space by keeping a reference of them in memory that can be used across multiple state objects.

For various ideas on how to reduce the state size, [see the discussion section](#Simplifications-Optimization).

#### Block size overhead

The overhead of Whisk on the `BeaconBlockBody` is 16.5 kilobytes. In detail:

- a list of shuffled trackers (128 trackers) (128*96 = 12,288 bytes)
- the shuffle proof (atm approx 82 G1 points, 7 Fr scalars) (4,272 bytes)
- one fresh tracker  (two BLS G1 points) (48*2 = 96 bytes)
- one com(k) (one BLS G1 point) (48 bytes)
- a registration DLEQ proof (two G1 points, two Fr scalars) (48*4 = 192 bytes)

The overhead of Whisk on the `BeaconBlock` is 192 bytes. In detail:

- an opening DLEQ proof (two G1 points, two Fr scalars) (48*4 = 192 bytes)

#### Computational overhead

The main computationally heavy part of this protocol is proving and verifying the zero-knowledge proofs involved.

We [wrote a PoC of the ZKPs](https://github.com/ethresearch/Shuffle_SSLE/tree/master/rust_code/src) using an old version of arkworks-rs (zexe) and the BLS12-381 curve and found that in an average laptop:

- Shuffling and proving the shuffle takes about 880ms (done by block proposers)
- Verifying the proof takes about 21ms (done by validators)

Our benchmarks were a PoC and we believe that a production-ready implementation of the shuffling/verifying procedure can provide a 4x-10x boost on performance by:

- Moving from zexe to the latest arkworks-rs or a more optimized library (e.g. blst)
- Moving from BLS12-381 to a curve with faster scalar multiplications
- Further optimizing the proofs and their implementation

If the proving overhead is considered too high, we can alter the shuffling logic so that validators have time to precompute their proofs in advance. For example, we can avoid shuffling on the last slot before each new round of the shuffling algorithm. At that point, the shuffling matrix for the next round is fully determined and hence validators have at least 12 seconds to shuffle and precompute their proofs for the next round.

## Related work

There are more ways to solve the problem of validator privacy. Each approach comes with its trade-offs and each use case should pick the most suitable approach. In this section, we go over different approaches and discuss their trade-offs.

### SASSAFRAS

The Polkadot team has designed an SSLE protocol called [SASSAFRAS](https://research.web3.foundation/en/latest/polkadot/block-production/SASSAFRAS.html) which works using a combination of a ring-VRF and a network anonymity system.

The scheme works by having each validator publish a VRF output (i.e. election ticket) through a native single-hop anonymity system. After some time, the chain sorts all received tickets to create the future proposer ordering, and when it’s Alice’s time to claim a slot, she submits a proof that it was actually her ticket that won this round.

SASSAFRAS turns their VRF scheme into a *ring-VRF* [through the use of SNARKs](https://github.com/w3f/ring-vrf) ensuring this way that the VRF output was generated from a specific set of public keys and no duplicate or garbage tickets were submitted.

#### Benefits

A significant benefit of SASSAFRAS over Whisk is that it doesn’t require any shuffling which reduces the consensus complexity of the system. This means that state manipulation is minimal in SASSAFRAS, while in Whisk we are fiddling with the state at every slot. For the same reason, the state space required is significantly less, since the chain mainly needs to hold the VRF output of each validator (plus a pubkey), whereas in Whisk we are storing multiple commitments per validator plus the entire shuffling list. Finally and perhaps most importantly, the consensus simplicity of SASSAFRAS makes it more flexible when it comes to supporting other features (e.g. elect multiple leaders per slot or doing gradual RANDAO samplings).

A further benefit of SASSAFRAS is that the anonymity set of each proposer spans the entire validator set, in contrast to Whisk where the worst-case anonymity set is [8,192 validators](#Anonymity-set).

#### Drawbacks

The main drawback of SASSAFRAS is that instead of shuffling, it uses a network anonymity layer to detach the identity of the validator from her ticket.

For this purpose, SASSAFRAS builds a simple single-hop timed mixnet inside its p2p layer: When Alice needs to publish her ticket, she does `ticket (mod len(state.validators))` and that gives her Bob’s validator index. She uses Bob as her proxy and sends her ticket to him. Then Bob uploads it on-chain by sending a transaction with it. Effectively, Bob acted as the identity guard of Alice.

An issue here is that network anonymity comes with a rich literature of attacks that can be applied in adversarial environments like blockchains. At the most basic level, in the above example, Bob can connect the identity of Alice with her published ticket. Effectively this means that a 10% adversary can deanonymize 10% of tickets.

At a more advanced level, an eavesdropper of a validator’s network can launch *traffic correlation attacks* in an attempt to correlate the timing of received tickets with the timing of outbound tickets. Traffic correlation attacks effectively reduce the anonymity set of the system. The classic solution is for protocol participants to send fake padding messages; however designing such padding schemes requires careful consideration to not be distinguishable from real traffic.

Another interesting aspect of SASSAFRAS is that it assumes a mapping between validators and their P2P nodes. Creating and maintaining such a mapping can be done with a DHT protocol but it complicates the networking logic especially when a validator can correspond to multiple dynamic nodes. Fortunately, validators can still fallback to sending their ticket in the clear if such a system experiences a transient break.

Also, if the unique proxy validator of a ticket is faulty or offline, the validator is forced to publish the ticket themselves, effectively getting deanonymized.

With regards to cryptography, the current PoC implementation of the [ring-VRF](https://github.com/w3f/ring-vrf) uses Groth16 SNARKs which require a trusted setup. However, the SNARKs could potentially be rewritten to use Halo2 or Nova which don’t require a ceremony.

Finally, not all parts of SASSAFRAS have been fully specified (e.g. the bootstrapping logic), which might produce some yet unseen complexity.

All in all, SASSAFRAS is an SSLE protocol with higher networking complexity but lower consensus complexity. It’s important to weigh the trade-offs involved especially with regards to Ethereum’s networking model and overall threat model.

### Other networking-level defenses

In this proposal we’ve been assuming that it’s trivial for attackers to [learn the IP address of every beacon chain validator](http://www.cloud-conf.net/ispa2021/proc/pdfs/ISPA-BDCloud-SocialCom-SustainCom2021-3mkuIWCJVSdKJpBYM7KEKW/264600b402/264600b402.pdf).

[Dandelion](https://github.com/bitcoin/bips/blob/3693cdfd192dacdac89cd742f68cd1bb96bf7f7e/bip-0156.mediawiki) and [Dandelion++](https://arxiv.org/pdf/1805.11060.pdf) are privacy-preserving networking protocols designed for blockchains. They make it hard for malicious supernodes on the p2p network to track the origins of a message by propagating messages in two phases: a “stem” anonymity phase, and a spreading “fluff” phase. During the “stem” phase each message is passed to a single randomly-chosen node, making it hard to backtrack it.

Systems similar to Dandelion share [networking complexities](https://bitcoin.stackexchange.com/questions/81503/what-is-the-tradeoff-between-privacy-and-implementation-complexity-of-dandelion/81504#81504) similar to the ones mentioned above for SASSAFRAS. Furthermore, using Dandelion for block proposal needs careful consideration of latency so that it fits inside the four seconds slot model of Ethereum (see Figure 11 of [Dandelion++ paper](https://arxiv.org/pdf/1805.11060.pdf))

An even simpler networking-level defense would be to allow validator nodes to use different network interfaces for attestations and block proposals. This way, validators could use one VPN (or Tor) for attestations and a different one for proposals. The problem with this is that it increases setup complexity for validators and it also increases the centralization of the beacon chain.

### Drawbacks of Whisk

It’s worth discussing the drawbacks of Whisk especially as we go through the process of comparing it against other potential solutions (e.g. VRF-based schemes).

First and foremost, Whisk introduces non-negligible complexity to our consensus protocol. This makes the protocol harder to comprehend and analyze, and it also makes it harder to potentially extend and improve.

For example, because of the lengthy shuffling phase it’s not trivial to tweak the protocol to elect multiple leaders per slot (which could be useful in a sharded/PBS/crList world). That’s because we would need bigger candidate and proposer lists, and hence a bigger shuffling phase. While it’s indeed possible to tweak Whisk in such a way, it would probably be easier to do so in a VRF-based scheme.

Whisk also slightly increases the computational overhead of validators who now need to create and verify ZKPs when creating and verifying blocks. It also increases the computational overhead of P2P nodes, since they now need to do a DLEQ verification (four scalar multiplications) before gossiping.

Finally, a drawback of SSLE in general (not just of Whisk) is that it completely blocks certain protocol designs. For example, it becomes impossible to ever penalize validators who missed their proposal. SSLE also prevents any designs that require the proposer to announce themselves before proposing (e.g. [to broadcast a crList](https://notes.ethereum.org/Dh7NaB59TnuUW5545msDJQ?view)).

## Discussion

### Simplifications and Optimizations

In this section, we quickly mention various simplifications and optimizations that can be done on Whisk and the reason we did not adopt them:

- Moving the commitment scheme from BLS12-381 to a curve with a smaller base field size (but still 128 bits of security) would allow us to save significant state space. For a 256-bit curve, group elements would be 32 bytes which is a 33% improvement over the state space (BLS12-381 G1 elements are 48 bytes). We used BLS12-381 in this proposal because the consensus specs are already familiar with BLS12-381 types and it’s unclear how much work it would be to incorporate a different curve in consensus clients (e.g. curve25519 or JubJub).
- We can store H(kG) in the state instead of com(k) to shave 12 bytes per validator. But then we would need to provide kG when we propose a block and match it against H(kG) which slightly complicates the protocol.
- Instead of using com(k) to do identity binding on k, we could do identity binding by forcing the hash prefix of H(kG) to match Alice’s validator index. Alice would brute force k until she finds the right one. This would save space on the state, but it would make it hard to bootstrap the system (we would need to use a lookup table of {validator_index -> k})
- Instead of registering (rG, krG) trackers, we could just register with kG (i.e. not use a randomized base) to simplify the protocol and save space on the block and on the state. However, this would make it easier for adversaries to track trackers as they move through shuffling gates by seeing if they have the same base, which becomes a problem if the set of honest shufflers is small.
- We could do identity binding by setting k = H(nonce + pubkey) as the SSLE paper suggests which would simplify the protocol. However, we would need to completely reveal k when opening which causes problems if the same validator gets selected as a candidate twice (either in the same run or in adjacent runs) since now adversaries can track the tracker around.

## Replies

**asn** (2022-01-13):

## Appendix

### Appendix B: RANDAO attacks

In this section, we analyze RANDAO attacks against Whisk and the status quo.

In Whisk, over the course of a day (256 epochs) an attacker, Mallory, has two opportunities (*candidate selection* and *proposer selection* events) to control the last RANDAO revealer. If Mallory controls the last RANDAO revealer before the *candidate selection event* she gets to choose between two lists of 16,384 trackers, whereas if she controls the last revealer before the *proposer selection event* she gets to choose between two lists of 8,192 trackers. At that point, she can simply choose the list that contains more of her validators. We [simulated RANDAO attacks](https://github.com/asn-d6/ssle-abort-sim) and found that if Mallory, a 10% adversary, gets to control the last RANDAO revealer before the candidate selection event, she will abort 48% of the time and by doing so she will get 31.5 extra proposals per abort on average. If she follows this strategy for an entire day she can get 1.69 extra proposals on average per day (subject to how often she gets to control the last RANDAO revealer).

[![](https://ethresear.ch/uploads/default/optimized/2X/8/80ce9ba577742caa7428e9e9401f05b62edb5959_2_690x401.png)897×522 36.5 KB](https://ethresear.ch/uploads/default/80ce9ba577742caa7428e9e9401f05b62edb5959)

On the context of RANDAO attacks, it’s also important to compare Whisk against the status quo. In particular, RANDAO attacks are also possible against the status quo where we publicly sample 32 proposers at the beginning of each epoch using RANDAO (see figure above). In this case, over the course of a day (256 epochs), the attacker has 256 distinct opportunities to control the last RANDAO revealer, and every time that happens they get the opportunity to choose over two possible lists of 32 proposers. Our simulations show that while Malory is less likely to abort at each opportunity compared to Whisk (due to the smaller list size), if she follows this strategy for an entire day she can get much greater gains (14.7 extra proposals on average per day).

From the above and from looking at the figures below, we extract the following results:

- An adversary can get greater rewards over time in the status quo compared to Whisk [top-left graph]
- An adversary that exploits the status quo needs to do many aborts over the course of a day (bad for the beacon chain) [top-right graph]
- An adversary can exploit Whisk with only one abort per day for big gains (more deniable) [lower-right graph]
- Even small adversaries can exploit Whisk (a 0.01% adversary will abort with a 10% chance) [lower-left graph]

[![](https://ethresear.ch/uploads/default/optimized/2X/e/e7e21f30fb455f8122e7d8c3483a269e505aee13_2_690x362.png)1160×609 47.4 KB](https://ethresear.ch/uploads/default/e7e21f30fb455f8122e7d8c3483a269e505aee13)

[![](https://ethresear.ch/uploads/default/optimized/2X/3/3985139da50217fff2e625dbecfbef0c9af95382_2_690x362.png)1160×609 51.3 KB](https://ethresear.ch/uploads/default/3985139da50217fff2e625dbecfbef0c9af95382)

All in all, while big adversaries can extract bigger profits with the status quo, Whisk allows even small adversaries to extract profits by attacking RANDAO once per day.

Furthermore, Whisk makes the moments of candidate and proposer selection more juicy targets for attacks and bribes (imagine a RANDAO bias attack against *proposer selection* which places the adversary in a position to do another RANDAO bias attack against *proposer selection* on the next protocol run).

---

**burdges** (2022-01-20):

I’ve only done “complete” or worse “exploratory” protocol descriptions for Sassafras, although Sergey and Fatemeh wrote up one version, and Handan worked on adapting the Praos UC proofs.  We’ll do a “staged” more developer friendly write up eventually.

It’s true “late stage” or “full” sassafras faces mixnet-like anonymous networking issues, both in implementation and analysis, but…

First, we’ve rejected using gossip various places in polkadot for good reasons, like erasure codes and cross chain messages, and tweaked it elsewhere, so sassafras just continues this design theme.

Second, if you use trial decryption then “basic” sassafras works without such fancy networking, and the analysis becomes simpler.  It’ll open a DoS attack vector, but a lesser DoS vector than sassafras with non-ring VRFs.  It’s possible to fix the DoS vector too, but then you’ve a worse ring VRF than what we envision using.  You’d still have repeater code that delays and rebroadcasts the decrypted ring vrfs too, which yes lives “close” to the networking layer.  It depends upon your DoS tolerance and what you consider networking I guess.

We do have multiple tickets per validator in sassafras, so the state won’t be smaller than whisk, but it interact with the state far less.

---

**Killari** (2022-02-04):

Whisk sounds really complex and heavy. Have you considered Algorand’s model? It seems to be a lot simpler solution to this problem. One drawback I can see with it is that each slot gets multiple proposals which results into extra communication, but its significantly less than Whisk requires.

---

**asn** (2022-02-08):

Hello Killari,

Algorand’s *secret non-single leader election* is indeed another plausible route to achieving validator privacy. However, while it might seem simple in theory, in practice it complicates both the fork-choice and the networking subsystems.

In particular, see [Vitalik’s recent secret non-single leader election proposal](https://ethresear.ch/t/secret-non-single-leader-election/11789/3) on how it complicates the fork-choice and also opens it up to potential MEV time-buying attacks. Furthermore, by making the fork-choice more susceptible to forks and reorgs it makes it harder to apply [potential improvements to it](https://ethresear.ch/t/change-fork-choice-rule-to-mitigate-balancing-and-reorging-attacks/11127).

With regards to networking, a non-single leader election considerably increases the communication within the P2P network, especially in a sharded world where blocks are considerably bigger. For this purpose, Algorand uses a mix of smart gossiping and timeouts which would need to be adapted to Ethereum’s P2P logic (see section 6 of [Algorand’s paper](https://people.csail.mit.edu/nickolai/papers/gilad-algorand-eprint.pdf)).

All in all, I agree that Algorand’s approach is still worth examining further and seeing how its tradeoffs apply to our use case.

---

**Killari** (2022-02-09):

Thank you for the excellent reply! That makes a lot sense. I also don’t like the Algorands way to select multiple leaders and then pick the actual leader by selecting the block with the best number (in relative to ones you have seen).

Whisk on the other hand requires a lot computation and communication, just to get a single secret leader election system on board (with no additional benefits that I can see?). I wonder if we can do better.

---

**blagoj** (2022-05-01):

Hey [@asn](/u/asn) great post.

I do have few comments/questions:

1. Whisk proposition is to make it impossible to get to know the next block proposers upfront, the proposers reveal themselves at the time of proposal. Clearly this improves the resilience to attacks that would lead to stalling/destabilizing the network by DoSing the next block proposers (so no block get proposed for some time). However do you think this is enough, and additionally to which level the SSLE method (in general, not just WHISK) solves the block proposer DoS problem?
Also what is your opinion on other attacks, for example getting to know validator’s phyisical IP addresses by other means and just DDoSing them periodically? For example (let’s ignore the practical feasibility for a second), if SSLE is in place, but we obtain the IP addresses of the solo beacon node validators (i.e home stakers) and DDoS them periodically we can do some damage to the network (the question comes down to what is the probability of having the IP addresses of the validators that should propose in the next X slots).
My main point is, are there any known edge cases where WHISK and SSLE do not help?
2. You mentioned the polkadot way of doing things - try to solve things on network layer. Practically speaking, isn’t this more applicable to Ethereum as well? SSLE & Whisk contradicts with the current protocol design of rewards and penalties to block proposers, which would probably mean that the incentive mechanism would need to be changed which would lead more things to be changed. Additionally this proposal requires additional modifications to the consensus layer (data structures and logics). On the other hand changes to network layer would not require consensus layer changes, and additionally these changes could be much simpler implementation wise.
The main drawback of network layer changes are the impact of the latencies introduced to the validator reward and penalties. Additionally more research needs to be done on the latencies introduced by avoiding certain attacks (i.e timing attacks). However theoretically (with using the practical latency stats from the current network) from what we’ve researched so far there is possibility of resolving the block proposer DoS issue without having a negative impacts on the validator reward impacts (how practical this is remains to be seen).
The network layer approach increases the anonymity set (all validators) and is much less complicated design in practice.
Additionally solving problems on network level improves other properties as well (validator client operator privacy).
The question here is, what is your opinion on practicality on consensus layer vs network layer changes?
If we can provide network level privacy, does SSLE and Whisk become obsolete?
3. What are the next phases of the Whisk proposal, what are the requirements for it to become part of the consensus layer specs (if of course this is desired)?

---

**asn** (2022-05-16):

Hello [@blagoj](/u/blagoj). Thanks for the thoughtful response!

> Also what is your opinion on other attacks, for example getting to know validator’s phyisical IP addresses by other means and just DDoSing them periodically? For example (let’s ignore the practical feasibility for a second), if SSLE is in place, but we obtain the IP addresses of the solo beacon node validators (i.e home stakers) and DDoS them periodically we can do some damage to the network (the question comes down to what is the probability of having the IP addresses of the validators that should propose in the next X slots).
> My main point is, are there any known edge cases where WHISK and SSLE do not help?

This is an interesting concern about potential sidesteps that an attacker can do. In particular, even with SSLE, an attacker can indeed enumerate and blind-DDoS the entire set of home stakers. Given the current network size, and assuming a strong adversary, this could even potentially be doable. Hopefully, as the network grows (*it should grow, right?*), this attack would become well out of reach.

Attacks like this highlight the importance of [non-SSLE solutions](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763#other-networking-level-defenses-28) for the short-term future. For example, if validators use separate IPs for attestations and proposals, then an adversary wouldn’t even know what’s the IP address to DoS.

> The question here is, what is your opinion on practicality on consensus layer vs network layer changes?
> If we can provide network level privacy, does SSLE and Whisk become obsolete?

As mentioned in the [SASSAFRAS section above](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763#drawbacks-27), networking solutions can get pretty hairy both in terms of design and implementation, but also in terms of security analysis. When it comes to networking and mixnet-like solutions we are also grinding against the four seconds interval of publishing a block, so as our networking becomes slower, the harder it becomes to satisfy that constraint. Finally, it can also be a challenge to encapsulate certain complexities of the networking stack as it grows and tries to satisfy more requirements.

It would be useful to hear from people more familiar with the networking stack of Ethereum on how they feel about [SASSAFRAS-type solutions](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763#sassafras-25). Do you have any further insights on this, [@blagoj](/u/blagoj)?

> What are the next phases of the Whisk proposal, what are the requirements for it to become part of the consensus layer specs (if of course this is desired)?

Reducing complexity is where it’s at right now. Ideally, SSLE would be a tiny gadget that provides security, and not a complicated beast.

We are currently still exploring the space and figuring out potential improvements to Whisk, but also researching [potential alternative simpler designs](https://ethresear.ch/t/simplified-ssle/12315).

We are also working on documenting and explaining the [Whisk zero-knowledge proofs](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763#proofs-of-correct-shuffle-13) since they are one of the biggest sources of the complexity of this proposal, altho its [fortunately well-encapsulated](https://vitalik.ca/general/2022/02/28/complexity.html).

As we get increased confidence that Whisk is a good solution to the problem at hand, we will attempt to merge it as part of the consensus layer specs.

---

Cheers!

---

**Genya-Z** (2022-05-20):

A few comments on Dmitry Khovratovich’s analysis of Whisk, linked above.

1. The analysis based on 1-touchers and anonymity sets assumes that each 1-touched node is equally likely to correspond to each element of its anonymity set.  This will not necessarily be the case, and if so the cost of the attack decreases since the attacked can focus on attacking the most likely candidates.
2. The notion of “uniformity” as defined at the beginning of section 2 is only good through 2 rounds of F, whereas the analysis in the second bullet at the bottom of page 2 assumes it is good through any number of rounds.  In any case it is easy to come up with a function F that is “uniform” through 129 rounds (the best possible) but isn’t what would be considered a good mixing function by virtue of being linear.  Then again maybe that doesn’t matter for the application here.
3. In proposition 2, the formula given is for 0-touchers, not 1-touchers.
4. I haven’t completely followed the proof of Proposition 3, but it seems like the formula should depend on s, the number of rounds.
5. The formula for A_1 at the bottom on page 2 appears to have been obtained by multiplying the number of 1-touched benign trackers by the minimum size of their anonymity set.  This ignores the possibility the the anonymity sets overlap.
6. Formula (1) from Proposition 2 contains a spurious factor of N.

---

**blagoj** (2022-05-21):

Thanks for your detailed response. After doing some more research around the networking solutions to this problem, we’ve come to a realisation that resolving the validator anonymity problem on networking level is currently not feasible (with the current latency constrains), at least not for reasonable anonymity guarantees.

The reason is that all the solutions involve additional steps in form of additional hops or encryption before a message is published/propagated to the consensus layer p2p. These extra steps add additional latency which break the consensus layer latency constraints (it would not make sense for the validators to run such a solution).

The research we’ve done is only considering network level, while not doing any changes on the consensus layer.

Our conclusion is that network solutions can only improve anonymity marginally (in practical, feasible manner), but this improvement is not worth the added complexity. One such example is Dandelion++ addition to the gossipsub protocol with 1-2 hops of stem phase just to fit latency.

I think the long term solution is something like WHISK, which would require changes on consensus layer. But I think this is the right approach theoretically, because it is a solution that addresses the root of the problem and solve it from the inside and not doing “patches” on the outside (i.e network layer changes). My main concern was the impact on the other consensus layer parts and the analysis required for the impact on the changes., and additionally the process of getting the proposal officially merged into the spect. While it might make more time and effort I think this is the right approach.

We will post a detailed post soon which will contain the conclusion on our Consensus layer validator anonymity research.

---

**burdges** (2022-12-25):

We construct the Sassafras schedule once per epoch, so the anonymous broadcast phase that builds the schedule runs over several hours, and has no latency constraints.

There is a different anonymity limit imposed by the threat model making one hop natural, but doing partial shuffles looses lots of anonymity too, just in a different way.

In our case, and likely yours, analyzing why you want anonymity more closely helps.  SSLEs are not Tor where more anonymity always matters.

---

**Sh4d0wBlade** (2023-01-20):

What is the *permutation* exactly do in the shuffle? I did not find the technicality of it in [consensus-specs/beacon-chain.md at c6333393a963dc59a794054173d9a3969a50f686 · asn-d6/consensus-specs · GitHub](https://github.com/asn-d6/consensus-specs/blob/c6333393a963dc59a794054173d9a3969a50f686/specs/whisk/beacon-chain.md?plain=1#L275)

---

**asn** (2023-01-20):

I’m not sure exactly which *permutation* you are referring to. In general, every shuffle applies a permutation to the set of input trackers, and outputs those trackers permuted (and randomized) as described in [Whisk: A practical shuffle-based SSLE protocol for Ethereum](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763#algorithm-12) .

---

**asdfghjkl1235813** (2023-02-11):

hi,and I see you have used curdleproof and remove the feistel now,what is the advantage to the shuffe and shuffle proof in the article?

---

**asn** (2023-02-13):

Hello. Both of these changes are new developments and we haven’t found the time to write a post about them yet.

In short:

- We greatly simplified the shuffling logic and removed the Feistel. Now each shuffler picks 128 random indices from the entire candidate set instead of organizing validators into a square. See the relevant commit for more details.
- Curdleproofs is an implementation of the shuffle ZK proof that is described in the Whisk post above. We also wrote a technical document with more details on the protocols and security proofs.
- Finally, we have a new PR for Whisk which also includes unittests.

---

**asdfghjkl1235813** (2023-02-17):

Thank you for your reply. I have another question, I have read some articles about SSLE, and I noticed that there is a problem related to SSLE, because the leader election is completely hidden, so if a malicious node is selected, it may not issue a certificate and cause there is no leader in this slot, which seems to violate the liveness property. The Polkadot seems have some protocol to select an alternate block producer. I have these questions:

1.When whisk encounters this situation, how does Ethereum solve it?

2.And maybe any ssle protocol have the same problem there is no leader in the slot when malicious leader doesn’t issue certificate？

3.Can ssle modified to ensure that there is a leader to propose block in the slot, or can ssle be modified to be traceable so as to punish malicious nodes that do not propose block, but traceability seems to be contradict to unpredictability?

---

**Sh4d0wBlade** (2023-02-17):

Talk about your question 3, If a benign leader get DDoSed by a strong adversary that it can not propose any block, in this situation you still want to punish/slash it?

---

**asdfghjkl1235813** (2023-02-27):

Does the whisk test need to be connected to the main network of Ethereum, or is it only tested under the consensus specification, use the minimal?

---

**burdges** (2023-04-11):

> Shuffling and proving the shuffle takes about 880ms (done by block proposers)
> Verifying the proof takes about 21ms (done by validators)

Do you know how many G1 or G2 scalar multiplications here?

You’ve no pairings in the example code, so does the verifier do some scalar multiplications each shuffled ticket?  Or are you batching across proofs?

---

**asn** (2023-04-14):

Each shuffle proof proves that `n` trackers (tickets) got shuffled correctly. Most of the verification time is spent performing MSMs as in most bulletproof-style protocols.

Check out *section 6* of the [curdleproofs technical report](https://github.com/asn-d6/curdleproofs/blob/1aa27a68997d023366970a00e12c4aa97465d511/doc/curdleproofs.pdf) for a detailed performance rundown.

---

**dapplion** (2025-03-20):

For the record: in mid-2023 I implemented Whisk on Lighthouse and successfully ran it on a small devnet.

I noted a few issues caused by the bootstrapping phase of Whisk. In summary:

- Forced missed slots. Current spec will induce ~2% missed slot rate on the initial epochs after the fork ~ 12,000 cumulative missed slots during the first year post-fork

Proposed fix 1 Whisk: fix boostraping induced missed slots - zero proof by dapplion · Pull Request #3481 · ethereum/consensus-specs · GitHub
- Proposed fix 2 Whisk: fix boostraping induced missed slots - delay registration by dapplion · Pull Request #3488 · ethereum/consensus-specs · GitHub

Expensive duty discovery for validator clients. Current spec forces validators into doing hundreds of thousands of G1 multiplications per slot and per keypair (attached active validator index)

- Proposed fix Whisk: use public key as initial commitment by dapplion · Pull Request #3487 · ethereum/consensus-specs · GitHub

Note that both issues can be solved if there’s no bootstrapping phase. This proposal uses fancy cryptography to get rid of it [The return of Torus Based Cryptography: Whisk and Curdleproof in the target group](https://ethresear.ch/t/the-return-of-torus-based-cryptography-whisk-and-curdleproof-in-the-target-group/16678)


*(1 more replies not shown)*
