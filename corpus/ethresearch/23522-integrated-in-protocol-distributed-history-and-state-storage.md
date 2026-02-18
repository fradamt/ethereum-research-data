---
source: ethresearch
topic_id: 23522
title: Integrated in-protocol distributed history and state storage
author: vbuterin
date: "2025-11-24"
category: Sharding
tags: []
url: https://ethresear.ch/t/integrated-in-protocol-distributed-history-and-state-storage/23522
views: 472
likes: 8
posts_count: 7
---

# Integrated in-protocol distributed history and state storage

This post will describe a fairly simple and well-integrated approach to doing distributed storage of Ethereum’s history, and an extension to storing state.

## Step 1: put block contents into blobs

We put Ethereum’s history into blobs. The natural way to do this is to have a function `get_blobs(block_body) -> List[Blob]` that serializes the block body and splits it up into blobs. We then require the first blob versioned hashes in a block header’s blob versioned hash list to equal `[get_versioned_hash(blob) for blob in get_blobs(block.body)]`.

For convenience, we can separate the blobs for the CL body from the blobs for the EL body (ie. `ExecutionPayload`), then we can have the ZK-EVM proofs include only those versioned hashes as a public witness. This allows a block to be verified purely by

1. downloading the headers
2. doing a DAS check for the blobs
3. downloading and directly verifying the CL part only,
4. verifying the ZK-EVM proof

When the full Lean Consensus features are introduced, the CL part will also get a ZK proof, and we will have achieved the full ideal of having a chain you can verify by only checking headers, DAS and proofs - total “verifiability on a smartwatch”.

We can make the above cleaner by doing [payload chunking](https://ethresear.ch/t/payload-chunking/23008), and adjusting a few constants. Particularly, if we (i) do [EIP-7976](https://eips.ethereum.org/EIPS/eip-7976) and with the same gasprice for zero and nonzero bytes, and (ii) increase the blob size when we upgrade blobs to quantum-resistant (or even earlier), then we can achieve the guarantee that each payload chunk can fit inside one blob (!!). For example, if we set calldata cost to 64 gas per byte, then thanks to [EIP-7825](https://eips.ethereum.org/EIPS/eip-7825), we have a hard cap that a serialized tx is under 256 kB, so if we set blob size to 256 kB, we get this guarantee.

We will also need to do the same for block-level access lists, including ensuring that the hard “64 gas per byte” invariant is reflected for each component and for the combination.

## Step 2: random blob history storage

We add a rule that each client must store a randomly selected one sample of each blob that it sees. If we:

- Set sample size to 512 bytes (shrunk from the current 2048), to maximize PeerDAS bandwidth
- Assume an aggressive average 64 256 kB-sized blobs per slot (16 MB), which is enough for either a ~20x increase in L2 blob space compared to status quo, or ~128x the current gas limit, or a mix of both

Then we get:

- Each client stores 1/512 of each blob, so you need ~710 honest nodes (above 512 due to overlap) to store >= 50% of the blobs to be able to recover all of them.
- Each client’s load will be (at an aggressive 128 blobs per slot) 512 * 62 * 31556926 / 12 bytes = 80 GB per year, which is roughly in line with reasonable extra load to impose on consensus nodes

Querying for blobs can be done either by re-purposing the existing DAS mechanism, or by creating a dedicated protocol more optimized to the syncing process.

## Step 3: add storage

This actually does not require any work. If block-level access lists are included in blobs, then you can already sync blobs from the latest state you know (if needed the merge-time snapshot) and replay the updates to compute the current state. If desired, we could also add a “repeatedly walk through the tree from left to right” mechanism, though it is not clear if it is worth the complexity.

## Replies

**weiihann** (2025-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This actually does not require any work. If block-level access lists are included in blobs, then you can already sync blobs from the latest state you know (if needed the merge-time snapshot) and replay the updates to compute the current state. If desired, we could also add a “repeatedly walk through the tree from left to right” mechanism, though it is not clear if it is worth the complexity.

Let’s assume that snap sync no longer works because no one holds the full state anymore.

If a new node wants to recompute the state at the latest head, it must first download a verified state snapshot from a block prior to BAL activation. It can then replay the state diffs in BALs to compute the latest state root. The big question is: who is supposed to provide this state snapshot?

---

**vbuterin** (2025-11-25):

If we want snap sync to work, one strategy is to split the state into eg. 16 pieces, and ask each node to store 1/16 of the state. Then you can snap sync each piece separately. Though this is less optimal in terms of resilience because it does not benefit from erasure coding; I would predict it works fine for 16, but if you try to scale it further, you will run into the problem where there’s too high a probability that a client just can’t find a peer for one of the prefixes, and no way to recover.

One way to add back maximum resilience is to sort the BAL, and add a header that labels which samples contain updates for which prefixes of the state. Then a node that fails to snap sync one part of the tree can walk through BALs just for that one part.

---

**dryajov** (2025-11-26):

I think this is really elegant. But I have a few questions:

- Does L1 payload data have priority? If a block is 2 MB and there’s 14 MB of L2 blob demand, fine. But what if execution blocks size increase further?

- Is the fee market unified or separate? If L2s are bidding up blob fees, does that implicitly tax L1 execution by making block propagation more expensive?

- What happens during L1 congestion vs L2 congestion - do they interfere with each other?

---

**vbuterin** (2025-11-26):

> - Does L1 payload data have priority? If a block is 2 MB and there’s 14 MB of L2 blob demand, fine. But what if execution blocks size increase further?

Yes, I think it has to. One way to do it is to set the params so that theoretical max L1 payload capacity is always under the blob count target. Then the L2 blob maximum would be the “base maximum” minus the target, and so it would always be greater than the target, so the fee market would function.

The other way is to do 2D gas pricing at L1, and make calldata a separate dimension, and then have the blob basefee added in to the calldata gas price.

---

**qizhou** (2025-12-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> We add a rule that each client must store a randomly selected one sample of each blob that it sees.

Great idea!  One question is how to enforce the rule?  E.g., will there be any penalty (or incentive) for storing the blobs?

---

**Po** (2025-12-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> 512 * 62 * 31556926 / 12 bytes = 80 GB

Typo: should be 64 instead of 62, `512 * 64 * 31556926 / 12 bytes = 80 GB` ?

