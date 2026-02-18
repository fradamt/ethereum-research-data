---
source: ethresearch
topic_id: 6049
title: "Anonymity: a ZKP to remove the mapping ip address / wallet's public key of a validator"
author: liochon
date: "2019-08-28"
category: Sharding
tags: []
url: https://ethresear.ch/t/anonymity-a-zkp-to-remove-the-mapping-ip-address-wallets-public-key-of-a-validator/6049
views: 3317
likes: 14
posts_count: 5
---

# Anonymity: a ZKP to remove the mapping ip address / wallet's public key of a validator

With the validators participating on the p2p network, it’s easy (and trivial if you use Handel) to deduce the mapping between validator’s wallet public keys (pk) <–> ip address. Simply track pk’s committee membership over time and compare with the ip addresses actually participating. A few epochs are enough to deduce the one-to-one mapping.

Hiding behind Tor is a good solution, but can be complicated at scale. Tor has also been attacked in the past. We may spend more time of Tor-like solutions going forward; AFAWK Mikerah is already working on this.

What we describe here is a solution to render the one-to-one mapping pk-ip completely opaque. Our scheme uses linkable ring signatures, or alternatively a zero knowledge proof (ZKP). The idea is that validators will use a new public key for participating, without revealing the link between the wallet used to stake and this new public key.

Here is the high level mechanism, for a user U who wants to be a validator. The detailed ZKP is below.

a) U burns 32 eth by calling a specific contract.

b) U waits up to three months (the idea is that U waits until enough people have burnt stake.)

c) U registers himself as a validator, with the new pk he will be using as a validator, by sending a transaction with a linkable ring signature.

This does not break slashing:

- rewards are put on the new pk.
- when U exits, 32 eth are deposited to the new pk.
- if U is slashed the amount given back is decreased as defined by the slashing rules.

There are a few subtleties, though:

- The new pk has to be used carefully by the user if he doesn’t want to reveal his identity.
- The transaction at step c) cannot pay any fee, and this could be used for DoS attacks. However, all nodes can check if the transaction is valid before forwarding it.

Blazej, Nicolas, Olivier

Here’s how to replace linkable ring signatures by a ZKP. Let us define:

1. x: a random number;
2. h: Hash(x);
3. h_!: Hash(!x);
4. L: a list of h;
5. L_!: a list of h_!
6. pk_v: new public key / validator public key
7. \Delta_t:  A length of time, typically 3 months, less than the minimal duration a of a validator appointment.

- ValidatorContract#burnEth method
inputs: h
state: L
actions:
(1) burns 32 eth
(2) add h to L
(3) remove from L all h older than \Delta_t
- ZK circuit
public inputs: L', h_!, pk_v
private inputs: x, h, \mathit{pos}: position of h in the L' vector
statements:
(1) Hash(x) = h
(2) L'[\mathit{pos}] = h
(3) Hash(!x) = h_!
- ValidatorContract#registerValidator method
inputs: L', h_!, pk_v,  ZKP(L', h_!, \mathit{pk}_v)
state: L_!
statements:
(1) ZKP is a valid proof
(2) all elements of L' are in L
(3) L_! does not include h_!
actions:
(1) add h_! to L_!
(2) all the standard job of adding a validator
(3) remove from L_! all h_! which older than \Delta_t.

And the scenario for the wannabe validator becomes:

a) U (1) chooses a random number x; (2) calculates h = Hash(x)

(3) choose the pk_v to use as a validator

b) U calls \mathit{ValidatorContract\#burnEth(h)}

c) U waits for a while

d) U (1) select the h from \mathit{ValidatorContract\#L} to be included in L'. Calculate \mathit{pos}

(2) generates \mathit{zkp} = ZKP(L', h_!, pk_v, x, h, \mathit{pos})

e) U calls \mathit{ValidatorContract\#registerValidator(L', pk_v, zkp)}

## Replies

**Mikerah** (2019-08-28):

This is interesting. I have a few comments.

1. @barryWhiteHat proposed a few months ago a way to use Semaphore for spam in the anonymous p2p setting. This could be combined with what you proposed in order to ensure that validators don’t end up spamming the network.
2. I have previously thought of using traceable ring signatures which are an extension of linkable ring signatures in a similar fashion. However, I thought of it as a way to get privacy-preserving casper FFG since traceable ring signatures give us a way to get anonymous voting by associating a tag with a signature. Combined with your proposal, we can almost get anonymous validators (with some caveats of course!).

---

**liochon** (2020-02-07):

There is a subtlety related to slashing with anonymous validators that is worth mentioning explicitly. Slashing aims to prevent the nothing-at-stake problem, by forcing validators to choose a side when a fork occurs.

If there is any way to be anonymous, you can stake in the two forks without being identifiable, i.e. slashable. Imagine that a set of entities *plan* a fork. If there is an anonymity service such as a mixer available, they will do the following steps:

1. exit as validator (if already a validator).
2. move the funds to the mixer
3. fork
4. in the two branches of the fork exit from the mixer and start validating again, with the same funds, on the two branches.

This is very impractical today because of the entry/exit time (and actually possible without anonymity with the current deposit contract).

In any case, a validator anonymity scheme must ensure that validators already registered remain identifiable (it is the case with the scheme above, but it is actually natural to create schemes where the anonymous validators can participate in the two branches without being identifiable).

---

**Mikerah** (2020-02-07):

Mixers won’t help with anonymity here. Due to how PoS and sharding systems are designed, anybody can be probabilistically tie deposits + withdrawals with high confidence.

I think it’s possible to have 1) anonymous onboarding of validators and 2) still be held accountable. Indeed, the cryptographic primitives needed for this are currently not efficient. I do have some more thoughts around. I may post something later for feedback.

---

**liochon** (2020-02-10):

Yep withdrawals add complexity. Note that when you want to participate in two forks with the same funds, the point of using a mixer is not to be fully anonymous, but just anonymous enough to escape automated slashing.

> I think it’s possible to have 1) anonymous onboarding of validators and 2) still be held accountable. Indeed, the cryptographic primitives needed for this are currently not efficient. I do have some more thoughts around. I may post something later for feedback.

Please do ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

