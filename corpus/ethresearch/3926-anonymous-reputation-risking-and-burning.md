---
source: ethresearch
topic_id: 3926
title: Anonymous reputation risking and burning
author: barryWhiteHat
date: "2018-10-25"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/anonymous-reputation-risking-and-burning/3926
views: 21024
likes: 9
posts_count: 14
---

# Anonymous reputation risking and burning

# Abstract

If we allow groups of people to signal with complete anonymity we can reduce the signaling components in human interactions. This will considerably reduce the cost of expressing contention opinions. However these systems can be abused. So its important to have the ability to revoke users from these groups if they break the rules.

Previously we build [Semaphore](https://github.com/barryWhiteHat/semaphore) allows static anonymous reputation system. Here we propose an expansion of Semaphore where we can destroy a users reputation without knowing their Identity. We use this to build a binary reputation system which can trivially be expanded to a non binary reputation system.

# Background

With semaphore we create a merkle tree of user identities. Where each user knows some secret information (the hash seed of the leaf) about their leaf in the merkle tree.

We then use snarks to prove that users know the secret information of a leaf in the tree. They can also signal their support of statements (32 bytes string currently), like a vote or a tweet. We call this a signature. Finally we expanded this with a malleable nullfier so that users can only signal once about a given statement. So a user can signal about the same string twice but everyone will know that they did. If a user signals about different strings it will be impossible to link them together.

This is quite powerful construction and can be used for voting, social media, anonymous credentials…

# Reputation system

In order to build a reputation system we need to be able to burn users reputation if they break some rules.

## Roles in the system

The system has two roles

1. The users who signal about things
2. The admin who is able to remove users from the system if they break some rules, this could be a smart contract.

## Reputation system

We can use the nullifier to prevent a user from signalling but because it is malliable we cannot tell when they are signalling about something different. So its trivial for an attacker to avoid some nullifier based bans.

To prevent this we have an epoch system, during the epoch the users can signal. The admin can select various signals that broke the rules.  They collect these illegal signals into a smart contract.

At the end of the epoch each user is required to move to a new merkle tree, to move to this new tree they must prove via snark that they did not make any of the `illegal signals`. If they cannot prove this they cannot move and their reputation is burned.

This way we can burn users reputations if they break the rules.

# Conclusions

Forcing users to move merkle trees once an epoch is a limitation choosing the epoch length is difficult If its too short users will need to be online to perform this action. If its too long the admin will be unable to stop malicious activity until the end of an epoch. There are a few ways to limit this be allowing users to jump from epoch 1 to epoch 12 skipping the intermediate stages, however this limits the anonymity set.

We can use this to build non binary reputation systems in a few ways. We could add an int `reputation` to the leaves and limit how much people are able to transfer to the new tree if they made an “illegal” signal we could just give multiple users multiple leaves each being 1 unit of reputation

## Replies

**khovratovich** (2018-10-25):

I started reading “How Miximus works” and noticed you use nullifiers to prevent double spending. However if nullifier can be chosen arbitrarily, there is a potential front-run vulnerability: an attacker sees your nullifier before the transaction is mined and tries to slip in with his own leaf and the same nullifier, trying to spend it immediately.

This attack applies to Zerocoin, but in Zerocash/Zcash it was fixed by requiring the nullifier be deterministic function of the recipient public key. You can do something similar.

---

**barryWhiteHat** (2018-10-25):

This is not a problem. The nullifier is half the seed of the leaf, an attacker needs to find the other half of the seed in order to withdraw front run which is very difficult.

---

**khovratovich** (2018-10-25):

Attacker uses his own secret in a new leaf, just the nullifier is the same.

---

**barryWhiteHat** (2018-10-25):

> Attacker uses his own secret in a new leaf, just the nullifier is the same.

Ah yes that is a nice attack. So with miximus we will need to switch to something like how semaphore handles nullifiers. Let me breifly explain this as i think its not vulnerable.

With semaphore we want to be able to reuse the same nullifier without linking to signals together. So to prevent this we have the idea of an external nullifier. Which is defined by the user and should be consistent for that type of signal. So basically semaphore returns `hash(nullifier, external_nullifier)` So the nullifier gets hidden and an attacker does not know what the nullifier is at withdraw time which prevents them from front running.

Can you see some problems with this approach?

---

**yondonfu** (2018-10-26):

For Miximus, instead of using `external_nullifier`, perhaps you can define `nullifier = H(nullifier_secret)` and use `nullifier_secret` as a private input in the circuit while keeping `nullifier` as a public input. The zkSNARK proof would then also demonstrate that you know the pre-image for `nullifier` allowing you to withdraw from the contract. An attacker doesn’t gain anything from front-running your withdraw tx because even though he/she can create a leaf with the same `nullifier`, he/she will not be able to withdraw it without knowing the pre-image for `nullifier`.

---

**Commoneffort** (2018-11-06):

It’s great to see a big progress on this. I was wondering what are the illegal signals and how a user can defend himself in case he’s been banned by an admin?

---

**HarryR** (2018-11-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/yondonfu/48/3265_2.png) yondonfu:

> For Miximus, instead of using external_nullifier , perhaps you can define nullifier = H(nullifier_secret) and use nullifier_secret as a private input in the circuit while keeping nullifier as a public input. The zkSNARK proof would then also demonstrate that you know the pre-image for nullifier allowing you to withdraw from the contract. An attacker doesn’t gain anything from front-running your withdraw tx because even though he/she can create a leaf with the same nullifier , he/she will not be able to withdraw it without knowing the pre-image for nullifier .

I agree that this is a good approach, I’ve filled in some detail in a ticket: [Nullifier front-running in Miximus · Issue #2 · HarryR/ethsnarks-miximus · GitHub](https://github.com/HarryR/ethsnarks/issues/72)

Where the pseudocode for the circuit becomes:

```python
spend_hash = H(spend_preimage_var, nullifier_secret)
leaf_hash = H(nullifier_secret, spend_hash)
assert merkle_authenticate(path_var, address_bits, leaf_hash)
assert H(nullifier_secret) == nullifier_var
```

Where `spend_preimage_var` is known only to the person authorised to spend the leaf, and `nullifier_secret` is chosen by either the depositor or the owner of the spend secret.

However, these could also be replaced by public key operations, where the spender has a public key and must sign the leaf as authorisation which creates the nullifier. e.g.

```python
leaf_hash = H(spend_public_key)
assert merkle_authenticate(path_var, address_bits, leaf_hash) # verify exists in tree
assert eddsa_verify(spend_public_key, leaf_hash, signature)
nullifier = H(signature, leaf_hash)
```

But, by going through the logic I also came across another problem:

When the person who inserts the leaf to deposit the payment and the person withdrawing (the only person who knows the spend secret) are different parties, then the depositor knows when the withdrawer has withdrawn…

In the example above where eddsa signatures are used, the depositor doesn’t know what the nullifier will be unless the spender provides it to them, but the signature will be unique. Another problem is malleability of signatures, as that would allow double spend.

---

**seresistvan** (2018-11-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/harryr/48/1671_2.png) HarryR:

> When the person who inserts the leaf to deposit the payment and the person withdrawing (the only person who knows the spend secret) are different parties, then the depositor knows when the withdrawer has withdrawn…

So, basically this means that Miximus only provides anonymity against outsiders if you adhere to the security definitions of the [Möbius paper](https://eprint.iacr.org/2017/881.pdf).

Moreover, as [@barryWhiteHat](/u/barrywhitehat) explained it to me a malicious Miximus contract deployer could steal funds from others via a compromised proving key generation. Not sure how would affect a compromised zkSNARK setup the anonymous reputation system.

---

**barryWhiteHat** (2018-11-12):

> So, basically this means that Miximus only provides anonymity against outsiders if you adhere to the security definitions of the Möbius paper .

What do you mean? That any member of the MT knows whos money is withdrawn?

> Moreover, as @barryWhiteHat explained it to me a malicious Miximus contract deployer could steal funds from others via a compromised proving key generation. Not sure how would affect a compromised zkSNARK setup the anonymous reputation system.

That is the case with any contract deployer. You need to use deploy variables that everyone agrees is correct. So you can do a MPC for the trusted setup and then the deployer is powerless.

---

**seresistvan** (2018-11-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> What do you mean? That any member of the MT knows whos money is withdrawn?

Exactly! In case if Alice sends funds to Bob via the mixer she will know when Bob withdrawn money. So anonymity against senders is not guaranteed in this case as you explained it above.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> That is the case with any contract deployer.

Is there a way to figure out or even better formally verify that a zkSNARK trusted setup was done correctly…or is this absolutely out of reach? ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=12)

---

**barryWhiteHat** (2018-11-12):

> Exactly! In case if Alice sends funds to Bob via the mixer she will know when Bob withdrawn money. So anonymity against senders is not guaranteed in this case as you explained it above.

In this case Bob can tell alice to add leaf X to the tree. Then Alice will not know when it was withdrawn. Because she does not know the nullifier.

> Is there a way to figure out or even better formally verify that a zkSNARK trusted setup was done correctly…or is this absolutely out of reach?

For trusted setup where we have x participants. If 1 of the participants is honest we know it was done correctly.

---

**khovratovich** (2018-11-14):

To prevent nullifier correlation it is sufficient to publish a hash of the original nullifier concatenated to Bob’s private key and prove its format.

---

**barryWhiteHat** (2018-12-23):

One of the limitation here is that for each `illegal_signal` you need a user to create an individual snark to prove that they did not make that signal. But turns out you can batch multiple signals into a single snark.

The solution is to create an ordered merkle tree of `illegal_signals` force a user to calculate their nullifier for each singal and then prove that each signal was not part of the merkle tree.

So instead of having n snarks per epoch. We can have a snark that includes n proofs that each user did not make this signal. Where each epoch contains n `illegal proofs`

If we bond the users we can use the burned bond of the people who make illegal signals to pay for the gas of every user who transition to the new tree.

