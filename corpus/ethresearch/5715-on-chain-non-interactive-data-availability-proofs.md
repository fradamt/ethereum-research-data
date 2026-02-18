---
source: ethresearch
topic_id: 5715
title: On-Chain Non-Interactive Data Availability Proofs
author: adlerjohn
date: "2019-07-08"
category: Layer 2
tags: []
url: https://ethresear.ch/t/on-chain-non-interactive-data-availability-proofs/5715
views: 6616
likes: 14
posts_count: 6
---

# On-Chain Non-Interactive Data Availability Proofs

Written in collaboration with [@Mikerah](/u/mikerah).

# Overview

We present a practical scheme for on-chain non-interactive data availability proofs. It can be implemented as a pre-compile on Ethereum. Moreover, we provide a definition for a standardized content-addressable filestore, a **s**tandardized **f**ile**s**ystem (SFS), that may be of independent interest.

# Background

## Prerequisite Reading

- Towards on-chain non-interactive data availability proofs
- Minimal Viable Merged Consensus
- A data availability blockchain with sub-linear full block validation (i.e., LazyLedger)

## Extra Reading

- Validity Proofs vs. Fraud Proofs
- Cryptographic proof of custody for incentivized file-sharing

## Data Availability Proofs Using Erasure Codes

- A note on data availability and erasure coding
- Fraud and Data Availability Proofs: Maximising Light Client Security and Scaling Blockchains with Dishonest Majorities

The essence of sub-linear data availability proofs is client-side random sampling of erasure codes. *Erasure codes* allow for the reconstruction of some data (of size M encoded as N chunks) using any M of N chunks. While this may seem linear in cost, we can do better by splitting up the data in two dimensions, requiring only \sqrt{M} chunks to be probabilistically sampled.

Unfortunately, this scheme is subjective and cannot be readily executed on-chain at present. [An earlier attempt](https://ethresear.ch/t/towards-on-chain-non-interactive-data-availability-proofs/4602) at turning this protocol non-interactive and running it on-chain is extremely complex, requires a Sybil-free set of providers, and makes strong assumptions.

## Data Availability In Eth 2.0

The data availability proof method described above is central to the viability of a sharded blockchain. Indeed, it is trivial to see that if all nodes were required to process data on all shards, the resultant sharded blockchain would be isomorphic in performance and resource requirements to a blockchain with a larger blocksize.

If a shard chain block is withheld, [“clients with data availability verification can detect the fault and reject it”](https://twitter.com/VitalikButerin/status/1127325893293113346) by using data availability checking as described above. Under [a synchrony assumption and an uncoordinated-majority assumption](https://twitter.com/VitalikButerin/status/1143760401043079168), this allows arbitrarily high levels of confidence that all data across all shards is available.

We note that blocks in a blockchain aren’t inherently more accessible to clients than any other data. It is only that nodes [have access to block data through a standardized API by default](https://ethresear.ch/t/phase-one-and-done-eth2-as-a-data-availability-engine/5269).

# Definitions

We define the *standardized filesystem* (SFS) as a hash-indexed (*i.e.*, content-addressed) data store accessible to a node. Potential examples include, but are not limited to: chain data, [IPFS](https://ipfs.io), [Swarm](https://ethersphere.github.io/swarm-home), or [Filecoin](https://github.com/filecoin-project/research). Swarm is of especial interest as it “is designed to deeply integrate with the devp2p multiprotocol network layer of Ethereum,” *i.e.*, it is a SFS by design.

# On-Chain Non-Interactive Data Availability Proofs

## Assumptions

This scheme makes no stronger [assumptions](https://medium.com/@VitalikButerin/thank-you-for-engaging-dac3e1a24a0d) [than](https://twitter.com/VitalikButerin/status/1143760401043079168) are necessary for Eth 2.0 to be viable. Namely, an honest majority of main chain block producers assumption for liveness. When used in conjunction with fraud proofs, a [(full) synchrony](https://twitter.com/VitalikButerin/status/1143760735626907648) assumption (which requires the main chain to be censorship-resistant *i.e.*, the majority of main chain block producers aren’t actively censoring transactions/blocks) is also needed for safety.

## Scheme

We propose a scheme that involves a new precompiled contract, `C`. The contract has two methods, `check(bytes32 hash) -> (void)` and `isAvailable(bytes32 hash) -> (bool)`.

`check` starts [a client-side data availability check](https://twitter.com/VitalikButerin/status/1127325893293113346)  on a `hash` in the SFS. This may take some time to actually finish executing, so the task can be dispatched in parallel. Additionally, it saves the hash of the pending check along with the current block number in storage (*e.g.*, in a map).

`isAvailable` returns the results of a previously-requested data availability check of `hash` in the SFS. If fewer than D blocks (D is a system parameter) have passed since the request, or if a data availability check of `hash` has not been requested, this method `revert`s. If not, the method returns `true` if the data availability check was positive or `false` if the data availability check was negative. Successful completion of this method call also clears the request (hash and block number) from storage.

These methods should have significant gas costs, but are by construction reasonably cheap to execute client-side—otherwise performing data availability checks in Eth 2.0 would make the whole system intractably expensive. The gas cost of `check` should be proportional to the size of data, [specifically](https://ethresear.ch/t/a-data-availability-blockchain-with-sub-linear-full-block-validation/5503/1) O(\sqrt{blocksize} + \log(\sqrt{blocksize})).

Note that `hash` addresses data in the SFS, not just chain or side chain data. This scheme can be used for any arbitrary data in the SFS (*i.e.*, data accessible in a standardized manner to clients). This is in fact identical to the core idea of [LazyLedger](https://arxiv.org/pdf/1905.09274.pdf).

Also note that the precompiled contract interface here is agnostic to the underlying data availability technique used. If a new one superior to the one used here is discovered, it can be used instead by simply changing the precompile’s functionality.

## Example Usage

Suppose we want to deploy a side chain with optimal state safety guarantees. It borrows security from the main chain by committing side chain block headers on-chain, but funds can still be stolen if the side chain operators withhold an invalid block. To do this naively would require all transaction data to be posted on-chain to guarantee data availability (so that potential fraud proofs can always be computed). This is already a big step up in terms of scalability, as the Ethereum chain now only needs to come to consensus on ordered data rather than execution as well, but we want to do even better!

We can instead *not* post the side chain block data on-chain, and use on-chain non-interactive data availability proofs. If the side chain block producer(s) withhold data for side chain block with header hash `h`, a data availability check is requested `C.check(h)`. D blocks later, the result of this request is acquired `C.isAvailable(h)`. If the data isn’t available, the side chain can be halted, or the block producer(s) penalized, etc.

## Safety Analysis

Just as block producers cannot forge digital signatures or create coins out of thin air, they cannot cause safety violations, *even with a dishonest majority*. Block producers that evaluate the results of an `isAvailable` call incorrectly are in fact attempting to cause a safety violation on the main chain. Under an honest majority assumption this will never happen. Should the majority of main chain block producers attack the main chain to cause a safety violation, social governance can be used to mitigate this (this is fundamental to Eth 2.0 as well, though doing this requires an additional weak subjectivity assumption).

# Applications

The scheme we present here for non-interactive on-chain data availability proofs has a wide range of applications:

- Trust-minimized side chains
- Optimistic (forkful) merged consensus, potentially opens the door for stake-based merged consensus
- Permissionless Plasma
- Rollups without having to post all non-witness data on-chain all the time
- A two-way bridge to/from Eth 2.0

## Replies

**vbuterin** (2019-07-08):

What happens if data is published near the time boundary, and some nodes pass a data availability check and others fail? Is there a way to avoid a chain split? Or is the idea that some kind of majority vote between block proposers take place, and they can at least be held accountable for false-positives through some kind of proof-of-custody-like scheme?

---

**adlerjohn** (2019-07-08):

Excellent question! Maybe there’s already a well-thought out answer to this, so for starters: how is this solved in Eth 2.0? A shard chain block producer can equivalently selectively withhold data until close to the boundary (would this be the finalization time, or a different parameter?), and encourage a chain split. My understanding is that this scenario is currently not fully resolved in Eth 2.0, with proof-of-custody schemes still being very preliminary, though I may be mistaken. If you’re going the voting route, then this can be done in PoS trivially (access to a shard chain block vs any other part of the SFS is isomorphic to the global set of validators). With PoW this is simulated by orphaning blocks. Both require majority honesty assumptions of course.

Either way, “just do what Eth 2.0 is going to need to do” is the simple answer, in a PoS context.

In a PoW context, I don’t really see that as a problem. The only one who would be able to encourage a chain split in such a manner would be a miner (as a non-miner wouldn’t know when `isAvailable` is executed, or when a new block is found), and they’d be doing so at a greatly increased risk of having their block orphaned.

---

**vbuterin** (2019-07-08):

> A shard chain block producer can equivalently selectively withhold data until close to the boundary (would this be the finalization time, or a different parameter?),

There is no “boundary” in the eth2 context. There’s an argument that if one node sees a block as available through the data availability proof mechanism, then with very high probability >=50% of the block is out there, so “soon” (ie. within 2 * delta) an honest node will see those chunks, reconstruct the full data and rebroadcast the full data, so all future nodes will see their checks pass. This mirrors the status quo (ie. eth1, bitcoin, etc), where if an honest node sees a block it can rebroadcast it, guaranteeing that other honest nodes will see the block within time delta.

Data availability checking isn’t a “do it once, pass or fail” operation, it’s more like “choose some indices, keep looking for the data corresponding to those indices, and accept the block once you get all of the responses, even if you don’t get them at first”.

I suppose you could argue that kind of “voting” happens implicitly, in that if a node delays publication of data and too many nodes see a block as unavailable at first then that block will not be accepted into the canonical chain, even if the data is published later.

---

**musalbas** (2019-07-08):

The idea of including data availability verification as a pre-compiled smart contract is interesting. However with regards to the time-dependence of data availability, I’m also concerned about this case: what happens if `isAvailable` returns true for everyone at a certain point, but the data is then lost because the data behind that particular hash isn’t very popular, causing future nodes that validate the chain to reject that chain and thus fork? When data availability proofs are used in the Ethereum 2.0 context, it’s not as much as an issue, because only the availability of the block is being verified, and the data behind the block is assumed to be sufficiently popular as the community using the chain has an interest in it (which is also the status quo in Eth1 etc when it comes to e.g. pruned nodes).

I suppose to prevent that you also need the nodes that are checking data availability to also store the chunks that they are sampling in the long-term, to guarantee their availability in the future. In that case, I think the scheme could have similar properties to LazyLedger as nodes in the network are collectively helping to guarantee the availability of user-submitted data, though with higher overheads as you have to sample from multiple erasure coded Merkle trees of data.

The ‘data published near the time boundary’ issue seems harder to solve though, as the person who holds the data behind an arbitrary hash could release it long after a block has been generated and `isAvailable` is false, causing future block validators to reject that chain because `isAvailable` should actually be true. The implicit voting suggestion by [@vbuterin](/u/vbuterin) seems reasonable though. Even if `isAvailable` returns false incorrectly as data was released too late, that only effects liveness but not safety, and you could re-submit the data availability check again via the pre-compiled contract.

Nitpicks:

- This isn’t non-interactive in the same way as my earlier attempt, as nodes verifying the chain have to interactively sample chunks of the specified hashes, i.e. you wouldn’t be able to verify blocks offline. However I suppose you could make it non-interactive using the Fiat–Shamir heuristic but this would mean a lot of people would be sampling the same chunks and would reduce the security of data availability proofs, or use a client-specific precomputed challenges or hidden services (but that wouldn’t be completely non-interactive).
- The hash addressed data can’t be arbitrary data, but must be erasure coded data correctly formatted for the type of data availability proof. Also, the pre-compiled contract would have to accept fraud proofs of incorrectly generated erasure codes (or some kind of proof that the erasure code is correct). I guess this means you need to factor in some delay to wait for fraud proofs before isAvailable returns true.
- > The essence of sub-linear data availability proofs is client-side random sampling of erasure codes. Erasure codes allow for the reconstruction of some data (of size M encoded as N chunks) using any M of N chunks. While this may seem linear in cost, we can do better by splitting up the data in two dimensions, requiring only √M chunks to be probabilistically sampled.

 The number of chunks that need to be sampled by each client is actually O(1) (and for the entire network collectively it’s O(M)). The reason for using 2D coding instead of 1D coding is so that fraud proofs for incorrectly constructed code can be roughly O(\sqrt{M}) instead of O(M). The cost of performing a data availability check is O(\sqrt{\mathsf{blocksize}} + \log(\sqrt{\mathsf{blocksize}})) as you need to need to sample a fixed number of chunks, plus Merkle proofs for those chunks (from row/column roots) which are each \log(\sqrt{\mathsf{blocksize}}) sized, plus 2\sqrt{\mathsf{blocksize}} row and column Merkle roots. So the \sqrt{\mathsf{blocksize}} bit isn’t for downloading chunks, but fixed-sized Merkle roots for each row/column.

---

**loredanacirstea** (2019-07-19):

[@Mikerah](/u/mikerah), regarding the use of On-Chain Non-Interactive Data Availability Proofs in place of the [Master/Cache Shard](https://ethresear.ch/t/a-master-shard-to-account-for-ethereum-2-0-global-scope/5730):

There is first, second and third tier data. First tier is entirely contained in layer 1, highly used, small size public data (even user-created). Second tier is highly used, big size (per item). Third tier is less used data, regardless of size. Second and third tier data can have a seed kept as first tier data and the rest can be stored in Swarm/IPFS.

First tier needs to be available in the VM in full -> a Master Shard (global scope) can do this.

Your proposal is very good for 2nd and 3rd tier.

