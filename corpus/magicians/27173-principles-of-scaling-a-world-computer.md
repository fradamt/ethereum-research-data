---
source: magicians
topic_id: 27173
title: Principles of scaling a "world computer"
author: bipedaljoe
date: "2025-12-15"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/principles-of-scaling-a-world-computer/27173
views: 37
likes: 0
posts_count: 1
---

# Principles of scaling a "world computer"

Scaling ideas typically tend to try and be “trustless” but typically fail because the Nakamoto consensus with cpu-vote, coin-vote or people-vote is not trustless. The digital signatures and hash-chain are, but not the attestation to the correctness of the ledger (the signature from the validator under the consensus mechanism). It may be theoretically possible to make such attestation “trustless” with “encrypted computation that cannot lie” or something similar (and many here probably know more about that than me as I know nothing about it other than that there are people working on that) but with traditional model in Bitcoin and Ethereum, the validator attestation is based on trust.

My broader message here is that people are trying to make a thing based on assumptions of a thing but those initial assumptions are wrong.

The alternative to chase trustless scaling prematurely (while still a valid goal long-term) is to simple scale by the paradigm the consensus operates under: trust.

My scaling model (in “trust-based attestation” paradigm) is simple. A validator can be a team operating in lockstep, with multiple people, each shard could be under a separate person on a separate machine that is geographically in separate locations. But the team still operates as a singular entity. And they are responsible for producing a valid block, and if they do not, they do not get rewarded. Such teams then compete under the consensus mechanism. It is the same paradigm as it always was, and it just scales “internally”.

Compare this to the typical scaling idea (that splits the consensus), such as randomly assigning validators to shards from the central validator pool, maybe using some public proofs for cross-shard transactions, then running into problems like “syncing a new shard every time reassigned is problem” and solving it with “let us have stateless validation” which runs into a new problem of the validator no longer attesting to having validated the entire chain but rather they arbitrarily trust previous signatures which breaks the fundamental game theory of the paradigm. The problem, I think, in scaling, is people have started from the wrong initial assumptions. A very rare number of people may have taken that to a new paradigm of “trustless attestation”, but until that is matured, scaling has to be by “teams” that have trust internally.

So the good news is: scaling is much more “low-tech” than often assumed, as *what is scaled is based on trust* and thus scaling continues to be based on trust. The bad news is, Ethereum is in its architecture not built to be parallelized (parts of it are, but parts are not). There is no separation into parallel and sequential contract calls, all transactions in a block are done in sequence (this prevents parallel processing). A true Ethereum 2.0 is needed to go from single-threaded to multi-threaded. But the good news is, if we can understand the principles of scaling, there is fewer “wrong directions”.

A very easy way to demonstrate these ideas is on the older paradigm, the pre-Ethereum paradigm, Bitcoin. In Bitcoin parallelization is quite easy (it is a much simpler system, like a calculator vs. a computer). The transaction Merkle tree needs to be upgraded to be ordered (one of the forks did this in 2018), but once you have some kind of ordered tree, you can simply run everything in parallel. Shard by most significant bits of transaction hash, allow filtered propagation of mempool transactions and “sub-blocks” so it goes directly between “sub-nodes” between different nodes (thus no bandwidth limitations). Let shards “own” their transacting hash range, and any shard wanting to spend a “unspent output” another shard owns simply requests the right to do so, and the first to request gets the right.

There is no computation, storage or bandwidth bottlenecks in such architecture. The fundamental principle is that in a paradigm that is built on trust, you have to scale by trust. If you want to scale trustlessly you have to first transcend the paradigm.

[![scalefree](https://ethereum-magicians.org/uploads/default/optimized/3X/5/b/5bb21579d72c66f121f5d7601a3b7528524c6336_2_690x172.jpeg)scalefree3168×792 155 KB](https://ethereum-magicians.org/uploads/default/5bb21579d72c66f121f5d7601a3b7528524c6336)

Understanding how to scale a simpler ledger (Bitcoin), it becomes possible to start to figure out how to scale the Ethereum paradigm (and eventually with “trustless attestation” there may be a new paradigm for scaling, but nothing prevents scaling in current paradigm as long as the principles I define here are followed).
