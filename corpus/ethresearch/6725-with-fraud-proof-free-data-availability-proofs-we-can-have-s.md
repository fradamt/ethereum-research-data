---
source: ethresearch
topic_id: 6725
title: With fraud-proof-free data availability proofs, we can have scalable data chains without committees
author: vbuterin
date: "2020-01-05"
category: Sharding
tags: []
url: https://ethresear.ch/t/with-fraud-proof-free-data-availability-proofs-we-can-have-scalable-data-chains-without-committees/6725
views: 3986
likes: 16
posts_count: 10
---

# With fraud-proof-free data availability proofs, we can have scalable data chains without committees

Between [STARKed data availability roots](https://ethresear.ch/t/stark-proving-low-degree-ness-of-a-data-availability-root-some-analysis/6214) and Kate commitments (plus some not-yet-published techniques for computing N reveals of a deg-N polynomial in O(N * log(N)) time), we have the possibility of fraud-proof-free data availability checking schemes.

Fraud-proof-free data availability checking schemes have the advantage that they preserve many more of the properties of traditional non-sharded blockchains: if a block is accepted by a client at time T, it will continue to be accepted at any time after T, there’s no possibility that a fraud proof will invalidate it after the fact. This opens the door to the following possibility: what if we have a sharded blockchain *without* committees, where the *only* mechanism for verifying data is data availability checks?

Here is one possible design:

- There exists a base chain, similar to an ethereum-like non-scalable blockchain. Anyone can post transactions to it, etc.
- Users have the ability to pay a fee to send a special type of transaction, which contains a data commitment (think: STARKed data availability root, or a Kate commitment) to some data D.
- When including a data-commitment-carrying transaction, block proposers/miners first do a data availability check (ie. sample eg. 30 random coordinates) to verify that the data is available. They would need to do this through an anonymizing network to avoid an attacker satisfying only their checks and not anyone else’s.
- When verifying a block for any purpose (as a client or a block proposer/miner), for any data-commitment-carrying transaction you would do a data availability check. You would only accept a block for which every availability check passed.

These are the entire rules of the system; particularly, there are no committees, proofs of custody, etc. We lean on data availability sampling fully and absolutely for security.

Why do this?

- It’s extremely simple, in fact it’s arguably as simple as a sharded system can be. It provides consensus on a chain and on the fact that the data in that chain is available, which can be used as a base layer to build systems like rollup on top of.
- It’s secure; there’s always some risk that a small number of block producers and users get tricked by some unavailable data by random chance, but with overwhelming probability the rest of the network will not be tricked, and so will reject any blocks containing commitments to that unavailable data.
- It does not have 2/3 online assumptions that committee-based systems do

Why possibly not do this? A few reasons:

- We might strongly desire to scale computation and not just data, doing computation at layer 1 rather than layer 2, so as to avoid layer 2 relying on synchrony assumptions
- Committees have important side benefits, so we may need committees anyway. Particularly, (i) a Casper FFG chain already need thousands of validators per slot to send messages to reach finality, so we may as well dual-use those signatures, and (ii) there’s stability benefits to having a randomly selected ~128 validators that are guaranteed to have actually downloaded and stored the data.

That said, this certainly is possible as a construction.

## Replies

**as1ndu** (2020-01-05):

Is there recommend resource where I can read about specific  data availability checking mechanisms that you think are ready for use?

Upon this:

> We might strongly desire to scale computation and not just data, doing computation at layer 1 rather than layer 2, so as to avoid layer 2 relying on synchrony assumptions

Have you guys thought of scaling computation via dataflow programming paradigms?

---

**adlerjohn** (2020-01-05):

This is basically the design I originally proposed [here](https://ethresear.ch/t/on-chain-non-interactive-data-availability-proofs/5715), but with validity proofs rather than fraud proofs.

---

**dankrad** (2020-01-06):

I think this is actually very similar to [@musalbas](/u/musalbas) LazyLedger construction (possibly without the smart contract layer at the base chain). I think it provides weaker guarantees than what Eth2 wants to. In fact, one of the advantages of the scaled computation layers is that if you add another data availability layer to it (which I am a fan of – I think LazyLedger on top of Eth2 would be a great future enhancement), the space for including fraud proofs or rollup proofs would be much larger, potentially supporting many more possible applications than with one computation base chain.

---

**musalbas** (2020-01-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Users have the ability to pay a fee to send a special type of transaction, which contains a data commitment (think: STARKed data availability root, or a Kate commitment) to some data D.

It would be awesome if in the future, one can submit arbitrary data availability roots on-chain in Ethereum 2.0. This would allow greater interoperability with other chains. Consider for example, a version of an SPV relay contract where Ethereum verifies not only the consensus of the other SPV chain, but also the data availability of it, and thus can accept fraud proofs for it so it can indirectly verify its state validity.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> When including a data-commitment-carrying transaction, block proposers/miners first do a data availability check (ie. sample eg. 30 random coordinates) to verify that the data is available.

How do you determine the fee for spending the special type of transaction that contains a data commitment? Would it be proportional to the data that is committed to by the commitment, thus miners should sample more of the data? Or would it be static? If the latter, then one caveat is that a user may submit a data commitment that doesn’t have enough clients sampling it for it to be reconstructed. However, I think this is OK if we assume that it is up to the users of a smart contract to decide if the assumptions a smart contract makes on data commitments it relies on are OK (and whether they believe there are enough clients sampling it).

---

**vbuterin** (2020-01-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> Consider for example, a version of an SPV relay contract where Ethereum verifies not only the consensus of the other SPV chain, but also the data availability of it, and thus can accept fraud proofs for it so it can indirectly verify its state validity.

Why not just submit the body of the blocks of the other chain into the chain via the same mechanism as you would submit any other data? It’s the same cost/risk profile to assure validity of N bytes, regardless of where it comes from, so may as well push it through the same channel.

---

**dankrad** (2020-01-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why not just submit the body of the blocks of the other chain into the chain via the same mechanism as you would submit any other data? It’s the same cost/risk profile to assure validity of N bytes, regardless of where it comes from, so may as well push it through the same channel.

You could have data roots that are not any shard and don’t have to be downloaded by any validator – only acting as an insurance for the application layer.

---

**vbuterin** (2020-01-09):

But if that’s feasible then why not make *all* data roots “not have to be downloaded by any validator”? You can unbundle consensus and storage guarantees and charge for storage guarantees separately.

---

**musalbas** (2020-01-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why not just submit the body of the blocks of the other chain into the chain via the same mechanism as you would submit any other data? It’s the same cost/risk profile to assure validity of N bytes, regardless of where it comes from, so may as well push it through the same channel.

The cost/risk profile for some chain A to assure validity of N bytes in some chain B is lower when you can verify the data availability of N bytes in a chain B produced by another network B, under the assumption *that the other network B alone* has a sufficient number of clients making sample requests such that the other network can reconstruct the block.

If you can’t make this assumption, then the transaction fee that users pay to submit a data availability root has to proportional to the size of the data committed to the root. This is because validators must sample more chunks if there’s more data, as they need to ensure that their network A is sampling all of the chunks, so that the block can be reconstructed by network A alone.

If you can make this assumption however, then you can have a static cost to verify a data availability root, regardless of the size of the data its committing to, because validators only need to sample a constant number of chunks.

For use cases such as a SPV relay smart contract, then this assumption is reasonable to make, because the validators are basically acting as light clients (with almost-full-node-security) to the other network.

---

**dankrad** (2020-01-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> But if that’s feasible then why not make all data roots “not have to be downloaded by any validator”? You can unbundle consensus and storage guarantees and charge for storage guarantees separately.

The idea would be that there are two different kinds of data. One which is on shard chains and on which computation is performed by the validators who are processing that chain. So obviously they would have to download that data.

Then add another kind of data that is only available. So a ZKP on the shard chain can say “I prove that X is the state resulting from the transactions in Y, and by the way if you wonder what Y is you can download it here” [but no validator will have to do that, they only do data availability checks].

I think adding the second one to Eth2 at some point would be a real benefit.

