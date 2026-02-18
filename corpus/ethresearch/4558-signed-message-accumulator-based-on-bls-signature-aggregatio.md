---
source: ethresearch
topic_id: 4558
title: Signed message accumulator based on BLS signature aggregation
author: irakliy81
date: "2018-12-11"
category: Cryptography
tags: [signature-aggregation, accumulators]
url: https://ethresear.ch/t/signed-message-accumulator-based-on-bls-signature-aggregation/4558
views: 3687
likes: 5
posts_count: 8
---

# Signed message accumulator based on BLS signature aggregation

It seems to me that [BLS signature aggregation](https://crypto.stanford.edu/~dabo/pubs/papers/BLSmultisig.html) can be easily used as a very efficient accumulator of signed messages. If this is already widely known, I apologize - but I haven’t run into this before. Here is how it could work:

Suppose:

- We have a set of n messages m_1....m_n (these could be votes from n validators).
- Each message is signed using BLS signature scheme such that S_i = p_i \cdot H(m_i), where p_i is a private key, and P_i would be a corresponding public key.

We can then use a simple BLS aggregated signature as an accumulator of tuples (m_i, S_i). Specifically:

A = S_1 + S_2 + ... + S_n

For such an accumulator, a witness needed to prove inclusion/exclusion is just the public key P_i. So, given a witness, we can check if a given tuple (m_i, S_i) is in the accumulator by checking:

e(G, A - S_i) = \frac{e(G, A)}{e(P_i, H(m_i))}

This accumulator also has some nice properties:

- Since it’s just a BLS signature, it’s less than 100 bytes in size.
- Witnesses are just the public keys - so, also less than 100 bytes in size.
- Adding/removing values to/from the accumulator is just adding/subtracting signatures - so, very easy.
- Moreover, the witness remains constant even as values get added or removed to/from the accumulator.
- Two non-overlapping accumulators can be aggregated just by summing them.

The obvious drawback is that this accumulator can hold only signed messages (not arbitrary messages), but I think there are plenty of examples in crypto when we deal with signed messages.

## Replies

**burdges** (2018-12-12):

You linked a delinearized signature aggregation strategy, but you wrote it up using proof-of-possession.  As a rule, proof-of-possession sounds viable for staked validators, but becomes risky outside staking situations.

I suppose delinearized schemes could work with keys introduced *after* your accumulator starts by further aggregating your existing aggregate public keys, but now you require the aggregation history, which gets painful.

I do not believe this qualifies as an accumulator since I can replace A by absolutely anything and the verification equation still holds.  If you want a signature accumulator then you might check if delinearization interacts nicely with existing pairing-based accumulator schemes.  Or just use an RSA accumulator along side.

I’ve forgotten anything I ever read about pairing-based accumulator schemes sorry, but…  Read that literature with caution, not sure if they have complexities compared with RSA accumulators, or if maybe some broken scheme in print, but my brain remembers some reason to be cautious.

There are theoretical limits on batch accumulation, which make accumulators rather tricky to use in “big” ways.

---

**irakliy81** (2018-12-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> I do not believe this qualifies as an accumulator per se since I can replace A by absolutely anything and the verification equation still holds.

I’m not sure I follow this statement. Wouldn’t this be possible only if BLS signature scheme is broken? Or am I missing something?

As far as I can tell, the scheme I described is secure as long as BLS signature scheme is secure.

---

**burdges** (2018-12-12):

No.  Your signature verification equation is the sum of the usual BLS signature verification equation and e(G,A-S_i) = e(G,A-S_i), so any A works fine.

---

**irakliy81** (2018-12-12):

Hmmm, I see. I’ll think about it some more - but I think you are right.

In general, given an aggregated BLS signature A, is there a way to prove that signature S_i is in it?

---

**burdges** (2018-12-12):

Yes, you still list signers and messages.

---

**ldct** (2018-12-12):

Have you read [Pragmatic signature aggregation with BLS](https://ethresear.ch/t/pragmatic-signature-aggregation-with-bls/2105)? It describes using BLS aggregate signatures for PoS (among other things).

---

**burdges** (2018-12-15):

Right the pairing based accumulators look crazy slow without using this trap door: https://crypto.stackexchange.com/questions/25928/bilinear-pairing-arithmetic-cryptographic-accumulators

