---
source: ethresearch
topic_id: 7225
title: Weighted Threshold BLS for Ethereum 2.0
author: nemothenoone
date: "2020-04-01"
category: Cryptography
tags: []
url: https://ethresear.ch/t/weighted-threshold-bls-for-ethereum-2-0/7225
views: 2180
likes: 2
posts_count: 10
---

# Weighted Threshold BLS for Ethereum 2.0

The subject is self-explanatory.

Any need in that? It seems we’ve managed to construct that. For transaction signing at first, then we will see.

And, yes, this scheme would not mean there would be a need to change specs - we’ve managed to keep the verification function the same as in the original BLS.

## Replies

**tvanepps** (2020-04-01):

do you have a link to any of this work or a writeup?

---

**nemothenoone** (2020-04-01):

That is the point of this thread. To understand if there is any interest in such construction, so we could finalize the paper for publishing (with links and writeups in here as well).

---

**DamianStraszak** (2020-04-02):

This would be an important result in cryptography both in theory and in practice. Please share as soon as possible.

---

**djrtwo** (2020-04-03):

This could be useful for decentralized validator pools.

The alternative is to have N subkeys spread among M participants in such a way that each participant has a fraction of the N subkeys to make up the desired weight

---

**sherif** (2020-04-07):

threshold BLS aggregate signatures & aggregated public key have a huge impact on Compact multi-signatures for any small blockchains. i hope i can see security proof for the proposal .

---

**kladkogex** (2020-04-30):

Well - if we are talking about aggregated signatures the solution is trivial - simply add the weights.

Since ETH2 is using aggregated signatures and not threshold signatures,  there is not need for weighted threshold signatures in ETH2

---

**nemothenoone** (2020-04-30):

Nah, we are talking about weighted aggregation. Adding weights turned out to be not as trivial as it may look like.

By the way threshold signing is just one of BLS properties - it can be achieved with aggregated signatures or with more traditional interactive multiparty communication protocols.

A little update on what is going on with this particular project of ours. We’ve finished the theoretical construction and now moved on to security proofs formalization. Spoiler: They will be more formal, than we used to see.

---

**kladkogex** (2020-04-30):

What is the nontrivial part in adding weights?![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**sherif** (2020-05-04):

can i see a link to any of this work or a manuscript.

