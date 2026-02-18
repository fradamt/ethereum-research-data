---
source: ethresearch
topic_id: 1474
title: Proof of stake using secondary slave consensus
author: arowley85
date: "2018-03-23"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/proof-of-stake-using-secondary-slave-consensus/1474
views: 2205
likes: 0
posts_count: 2
---

# Proof of stake using secondary slave consensus

We know that a pure proof of stake must always solve the problem of who mints the next block. Traditionally, I have seen it proposed that a pseudo-random method is used either BFT or chain based - but this can lead to problems in grinding if more than just the next block creator is determined at once.

But what would be the merits of deciding next block creator via a secondary (slaved) consensus protocol instead of entropy?

As an idea… validators could nominate, subject to constraints, which block (by block height) they would forge during the next epoch and a secondary consensus method would be used to get agreement on validators proposals. The secondary consensus would have to front-run the main proof of stake blockchain (occur in advance) for the information generated to be useful. It would decide the order of block creation for the main blockchain only and not have an impact on economic return. The method for the secondary consensus could even be a proof of work method but without the burden of the security implications implicit in traditional POW it could be computationally less difficult or even decrease in computational complexity as each epoch gets closer (resetting as epochs pass).

The advantage are those that come with specifying block forger in advance and would presumably be an overall more coordinated flow of network traffic. In a moderate latency environment this could allow a faster block creation speed. It would also potentially allow validators to plan downtime without the consequent reduction in network security because their contributions end up concentrated into a single part of the epoch (of their own choosing).

## Replies

**nate** (2018-03-23):

If I follow correctly, it seems like you’re proposing a generalization of the “proposal mechanism” that Casper FFG lives on top of.

This seems reasonable in some ways (see proposals for this in full PoS [here](https://ethresear.ch/t/initial-explorations-on-full-pos-proposal-mechanisms/925) and [here](http://vitalik.ca/files/randomness.html)) but also not totally in others. For example, we could switch the proposal mechanism out for [Tendermint](https://tendermint.com/static/docs/tendermint.pdf) as the “secondary consensus” you describe, but in this case, Casper FFG doesn’t make much sense (as all blocks in the main chain are already finalized).

So I guess my pushback is: we don’t necessarily need a secondary layer of consensus - we really just need a well-defined forkchoice for some proposal mechanism (where many blocks at many heights can exist without needing to be finalized by a “secondary consensus”).

> The advantage are those that come with specifying block forger in advance and would presumably be an overall more coordinated flow of network traffic.

I’m not totally sure how this makes sense. For example, in the PoW-as-secondary-consensus example, you give in the previous example, it doesn’t seem like there is really a way to optimize network traffic (beyond what PoW already does).

