---
source: ethresearch
topic_id: 5009
title: Semaphore RLN, rate limiting nullifier for spam prevention in anonymous p2p setting
author: barryWhiteHat
date: "2019-02-18"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/semaphore-rln-rate-limiting-nullifier-for-spam-prevention-in-anonymous-p2p-setting/5009
views: 8656
likes: 8
posts_count: 8
---

# Semaphore RLN, rate limiting nullifier for spam prevention in anonymous p2p setting

# Semaphore RLN, rate limiting nullifier

Thanks to [HarryR](https://github.com/harryR/) for review and suggesting using shamir secret sharing here instead of weak key cryptography.

Thanks to [Mikerah](https://github.com/mikerah) for review.

## Intro

Using [semaphore](https://github.com/barryWhiteHat/semaphore) we use nullifiers to limit the rate at which someone can signal. However if someone breaks this we cannot punish them because we cant link the signal to them.

This has lead to [Anon rep proposal](https://ethresear.ch/t/anonymous-reputation-risking-and-burning/3926). This solution should work well in some situations. It imposes a high cost requiring every member of the group to take action in the case of a fork. This can be mitigated with a stake but the gasBlockLimit imposes an upper limit on the number of participants these groups can have.

This excludes a bunch of interesting user cases so here we propose a new kind of nullifier that for a single `external_nullifier` reveals no information but if someone repeats the same `external_nullifier` with different signal (ie they spam) it reveals their private key allowing us to remove them from the tree.

We hope to build upon this work to define

1. mix networks with strong privacy AND spam resistant.
2. anonymous rate limited universal logins; We limit participants to make more than x requests per second and if you do you get kicked out.

## Background

We have a merkle tree that stores a list of our members. Each member has a public key in the tree to which they know the private key.

Each member in the group can signal. They use a snark to prove that they are a member of the group without revealing which member they are. Each signal has the following public parameters

1. Signal; What you are saying
2. External_nullfiers; This prevents the linking of differnt signals together.
3. nullifiers; hash(extrenal_nullfier , leaf_private_key) which is a finger print uniuq to this member for this external_nullifier.

The main weakness here is that it does not let us remove anyone for bad behavior as every time they use a different `external_nullifier` they are anonymous again.

We define one class of “bad behavior” being making more than X signals per second. Where X is some parameter that we define about our system.

To enforce this we can set the `external_nullifier` to be a time stamp and each epoch every member is allowed to make one signal. Participants can ignore a signal if it comes from a future epoch or a epoch in the past.

## Method

Firstly we have a smart contract that allows anyone to deposit some currency and join our group. At any point a users can be removed from the group if someone calls a function passing their private key as an input. Anyone who does this will receive 33% of the slashed stake the remainder is burned.

So we want to have a way to force anyone who spams the network to reveal their private key so they can be burned.

In the previous snark the nullifier is `hash(external_nullifier, leaf_private_key)`

We need to add a few things to the snark

1. We generate a nullifier_private_key based upon hash(external_nullifier, leaf_private_key)
2. We encrypt the leaf_private_key with the nullfier_private_key and reveal the result as a public input.
3. We user shamir secret sharing to encode the nullifier_private_key so that 51% of the shares are required to reconstruct the secret.
4. We then use signal to randomly select 50% of the shares and reveal them.

Now each time you create a signal with the same `external_nullifier` but different `signal` it

1. calculates the same nullifier_private_key key and encrypts your leaf_private_key with it.
2. It calculates the same shamir secret and shares.
3. But it reveals a different 50% of the shares.

The chances are very small that a different signal will result in the same 50% of the share being revealed. So we are confident that any spammer will reveal their whole private key on their second message.

## Limitations

1. In the p2p context its difficult to identify users who are spamming because sharing every message would be very expensive.

We should also include as public parameter the `hash(external_nullifier, leaf_private_key, constant)` so its easy to see if two signals were created with the same member for the same `external_nullifier` but different signals. Furthermore we could share a bloom filter of these with our peers who can then request the snark from us and slash the participant.

## Replies

**HarryR** (2019-02-19):

Some recent discussion about anonymous reputation has turned this into a system where each account is rate-limited as to the number of actions that it can perform. Whenever an account makes some action, say submits a post or votes, a unique tag with a timeout is entered into a holding pool - this is linked to their post/vote etc.

If it turns out that the post is malicious or bad, or whatever, then some administrative process can flag the unique tag, which means that it will never expire.

This provides a basic mechanism for rate-limiting, as well as a binary reputation system (e.g. you are not allowed to continue participating).

When the tag has expired the user provides a zero-knowledge proof of:

1. Their tag has expired
2. Their account exists in the tree
3. The tag belongs to the tag
4. The tag is the most recent one

This is then used to duplicate insert a duplicate account in the account tree with an incremented nonce, this doesn’t link their old account, the action or the tag to this new action - so provides forward secrecy. However, the zkSNARK circuit forces the new account to be a duplicate of the other, but in a way which an observer can’t determine that they are.

The account tree and pool of tags are both merkle trees, managed by an on-chain contract and compatible with zkSNARK circuits.

The problems I’m coming across are:

1. How do you prove the account is the most recent one for that user?
2. Requiring two trees, one for tags and one for accounts, is a significant overhead.

---

**barryWhiteHat** (2019-02-21):

So here I try to design a system where the only “illegal” think that you can do is make more than x proofs per second. This has a bunch of dos prevention usecases.

Trying to have a list of more subjective illegal things is a little more complicated and this does lead to the overheard you are talking about. Perhaps we should try and design this as payment channel kind of game so that in the happy case nothing has to go on chain. Except a reputation revocation perhaps.

---

**burdges** (2019-02-25):

Just fyi, there is already a scheme called AnonRep by Ennan Zhai, Bryan Ford, at al. published in USENIX 2016.


      [usenix.org](https://www.usenix.org/system/files/conference/nsdi16/nsdi16-paper-zhai.pdf)


    https://www.usenix.org/system/files/conference/nsdi16/nsdi16-paper-zhai.pdf

###

---

**burdges** (2019-02-25):

Anti-Sibel techniques depend upon your goals normally.  If you accept restricting to a known group, like staked nodes, then you can play many games with VRFs producing tickets, so probably no nullifiers.

If otoh you want anyone to participate, then you cannot really prevent one party pretending to be many parties.  You could maybe ensure that nothing can be gained.

As an example, the pond messanger required conversing parties to exchange a password, and authenticated sent messages with a group signature scheme, so despite the system’s extremely low throughput and corresponding DoS vulnerability, an adversary could not really gain anything by attacking it.

---

**barryWhiteHat** (2019-02-26):

> Just fyi, there is already a scheme called AnonRep by Ennan Zhai, Bryan Ford, at al. published in USENIX 2016.

Ah okay i’ll find a new name. Thanks for pointing this out.

> Anti-Sibel techniques depend upon your goals normally. If you accept restricting to a known group, like staked nodes, then you can play many games with VRFs producing tickets, so probably no nullifiers.

I do not propose this as an anti-sibel technique. Rather I assume some anti sibel method is used. Like stakeing. And then build an anonymous group that can remove users who break our rate limiting rule.

What do you mean by VRF producing tickets?

> If otoh you want anyone to participate, then you cannot really prevent one party pretending to be many parties. You could maybe ensure that nothing can be gained.

If in the stake mechanizim someone want to create multiple accounts this is fine. But we limit the amount that each account can signal.

---

**tux** (2020-05-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> We user shamir secret sharing to encode the nullifier_private_key so that 51% of the shares are required to reconstruct the secret.
> We then use signal to randomly select 50% of the shares and reveal them.

Sorry to bump this, but this proposal was pointed out to me and these bullets stuck out:

How do you enforce that the shares of the split `nullifier_private_key` are in a 51%-required threshold? Wouldn’t a dishonest user be able to simply just make it such that they require, say, 75% of the shares? Then your reveal scheme would fail.

Or does the SNARK make this attack impossible?

---

**kobigurk** (2020-05-09):

The idea is that the revealed share depends on the signal. So if you broadcast a different signal, a different share would be revealed.

