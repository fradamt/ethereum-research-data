---
source: ethresearch
topic_id: 707
title: Infinite gas limit?
author: 3esmit
date: "2018-01-15"
category: Sharding
tags: []
url: https://ethresear.ch/t/infinite-gas-limit/707
views: 2109
likes: 3
posts_count: 6
---

# Infinite gas limit?

There are cases, where a contract have loops upon an array that grow with user input, causing contract fail due gas limit.

I see that through zero-knowledgbe techniques we might be able to process those offchain and submit the result with the proof.

Would be possible to ethereum implement this to make gas limit infinite?

## Replies

**gititGoro** (2018-01-22):

As I understand it, you’d still need to update the final state, once the off chain processing has finished. That will take some non zero amount of gas. So while each of these off chain processes can be infinitely “gassy”, you can only have so many of them running within the span of one block.

How would you do this with zero knowledge proof. I didn’t get that link.

---

**DanielRX** (2018-03-18):

Is the intention not verifiable computation? So the chain needs only verify the computation in some sense, while a near infinite loop can take place off chain?

---

**hochbergg** (2018-03-18):

I’m not sure what the forum rules are about post necromancy, but I thought its worth answering.

One of the reasons for the gas limit (as I understand it) is to limit the required node size.

Given the (mostly) constant block time, nodes need to be able to execute all code required from transactions in the block to be able to verify the block. As such, the gas limits puts a hard cap on the amount of computation (and storage) that would be required to validate a block.

If gas limits were infinite, we would need either infinitely sized nodes, or infinitely long block lengths.

Regarding zero-knowledge proofs - If a ‘succint’ zero-knowledge proof system (like zkSNARKs or zkSTARKs) is used, the proof length is independent of the amount of computation required - and the amount of work required to check it as well (I’m 99% sure on the second one).

Due to that, if you compute a transaction off-chain, and build a zkSNARK proof for it, you could theoretically have an ‘infinite gas’ transaction.

It is worth mentioning that creating and proving zkSNARKs is an expensive process, and so this might not go as far as we’d like. There are ways around this (eg. TrueBit, recursive zkSNARKs) which I recommend you to look into.

---

**3esmit** (2018-03-18):

Thanks or the answer. Would be nice if ethereum had natively a way of including proofs to “view functions”, when a proof is provided for a view internal call, than the internal call gas cost becomes of verifing the proof, not doing further calls to other contracts.

---

**DanielRX** (2018-03-18):

Apologies, it appeared on the top of the page so I assumed it was a new post, mobile view is not my friend.

