---
source: ethresearch
topic_id: 8047
title: State of block header sync in light clients
author: sinamahmoodi
date: "2020-09-29"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/state-of-block-header-sync-in-light-clients/8047
views: 5374
likes: 12
posts_count: 13
---

# State of block header sync in light clients

There’s desire for more client diversity in the Ethereum ecosystem. Specifically there seems to be room for clients with different capabilities. EthereumJS [VM](https://github.com/ethereumjs/ethereumjs-vm) was my entry point for working on the protocol, and I would like to see it become a light client running in the browser one day.

Light clients currently overwhelm altruistic servers and require complicated incentivization models to be sustainable. This problem can be attacked by minimizing the amount of data **pulled** from servers and where possible replacing that with servers **broadcasting** data to the network.

## Overview

For the purposes of this post we’ll focus on one of the problems light clients try to solve: verify the inclusion of a transaction in the chain and its validity, on a resource-constrained device (equivalent to SPV nodes in Bitcoin). In order to do this check, the light client first needs to determine the canonical chain. The most naive, but secure approach is to download and validate all the block headers of the chain advertised to have the most accumulated difficulty. With the total size of block headers nearing somewhere between 5Gb and [~8Gb](https://ledgerwatch.github.io/turbo_geth_release.html#Disk-space) (depending on the implementation) this approach is completely infeasible. In LES this is worked around by hardcoding checkpoints in the form of [CHTs](https://github.com/ethereum/devp2p/blob/4ba94c8a2ab5781d754d56ba840abfe38f502342/caps/les.md#canonical-hash-trie) in the client.

In the rest of this document we’ll go over some alternatives to the status quo. At a high-level these approaches imply different bandwidth requirements and have varying consensus complexity.

[![light-client-sync-spectrum](https://ethresear.ch/uploads/default/original/2X/d/d26ddda9e1cc43f568bd08a680da1cf0d70a01f9.png)light-client-sync-spectrum543×193 14.1 KB](https://ethresear.ch/uploads/default/d26ddda9e1cc43f568bd08a680da1cf0d70a01f9)

### ZKP

The goal of this **hypothetical** approach (similar to the [Coda](https://eprint.iacr.org/2020/352.pdf) blockchain) is to demonstrate the other end of the spectrum, where blocks include a zero-knowledge proof proving that:

1. There exists an unbroken chain of blocks from genesis to the current block
2. Block headers are valid according to the consensus rules
3. The total difficulty of the chain is a certain value. In the presence of competing forks the light client can verify the proof in each fork’s head block and compare the total difficulty to find the heaviest chain.

What I want you to take away from this is the properties of the ideal approach:

- Short proof: Depending on the exact proof system the bandwidth required is likely less than 1Kb.
- Non-interactive proof: The proofs are so short they can be distributed along with the block. No need for light clients to request any data from servers. Having full nodes respond to light client requests is a massive bottleneck and severely limits the numbers of light clients each full node can serve.
- Guaranteed security: Same as in the naive approach of downloading all block headers, the light client can be sure about the canonical chain.

### FlyClient

[FlyClient](https://eprint.iacr.org/2019/226.pdf) is the state of the art when it comes to the initial syncing for light clients. It was recently activated on Zcash as part of the [Heartwood](https://electriccoin.co/blog/introducing-heartwood/) network upgrade. It gives you relatively **short proofs** (500Kb for 7,000,000 blocks assuming 66% honest mining power according to the paper). These proofs are non-interactive and similar to the ZKP approach can be gossiped in scale. FlyClient is secure with an *overwhelming* probability. It can further be configured to tolerate more or less dishonet mining power by trading off bandwidth.

This approach requires a *consensus change* in the form of a new field in the block header. The new field `historicalBlocks` is the root hash of a tree storing all block hashes from genesis up to the parent block. The tree in question is a *modified* [Merkle Mountain Range](https://github.com/opentimestamps/opentimestamps-server/blob/1b191439f66d603d3d5d32a60b691ce8c92746ad/doc/merkle-mountain-range.md) (MMR). The Difficulty MMR stores some extra metadata in the nodes of a vanilla MMR. The metadata allows us to verify the aggregate difficulty of all the blocks in the subtree under each node.

Now let’s see how this change helps light clients sync. Assume `LC` is a light client who performs a network handshake with multiple full nodes `FN_i` each of which advertise the total difficulty of their best chain and the hash of its head. Some of the full nodes might be malicious. `LC` sorts the full nodes in descending order of their advertised total difficulty and for each performs the following:

- Fetch and verify the last block H’s header
- Randomly sample log(N) historical blocks B, for each:

Verify the header (incl. PoW)
- Verify proof against H.historicalBlocks to make sure B’s hash matches the MMR leaf in H
- Verify that B’s historical blocks are a prefix of H’s. MMR allows this check to be performed efficiently. However because we can’t modify past blocks, this condition can only performed for blocks after the hardfork that introduces the historicalBlocks field.

The sampling algorithm tries to maximize the chance of finding at least one invalid block in a dishonet chain regardless of the adversary’s strategy. It samples from a smooth probability distribution, with relatively low probability for selecting a block from the beginning of the chain and continuosly increasing probably as you move towards the end of the chain. However to take Ethereum’s variable difficulty in mind, the beginning and end of the chain are not in terms of block numbers, rather in terms of cumulative difficulty. Hence the reason for embedding difficulty information in the tree nodes is to be able to query e.g. the block at 1/2 of the total difficulty.

Each sampling step is separate and doesn’t depend on the result of any other step. Hence the whole process above can be made non-interactive by using a publicly verifiable source of randomness, like the parent block’s hash or [drand](https://drand.love), as seed for the sampling algorithm. The result is a single proof that a full node can generate independently and broadcast for a host of light clients to verify. The proof shows there exists a connected chain from genesis to the advertised head with the given total difficulty.

### EIP-2935

[EIP-2935](https://eips.ethereum.org/EIPS/eip-2935) proposes a simpler consensus change in comparison, which involves storing the hash of historical blocks in the storage slots of a system contract. Light client sync is stated as one of the motivations, along with being able to prove a historical block against only the head of the chain which would be useful in L2 state providing networks. Making the blockhashes explicitly part of the state also [helps](https://ethresear.ch/t/the-curious-case-of-blockhash-and-stateless-ethereum/7304) with stateless block witnesses.

So the question is how can we use this EIP for the purpose of syncing light clients. Here we go into two variants, both of which require the EIP to be modified to store all the historical block hashes since genesis, as opposed to the block hashes since the hardfork block.

#### Variant 1: Random sampling

I think you can build a protocol which somewhat resembles FlyClient—in that it does random sampling of blocks—on top of this EIP. However it will either have lower probabilistic security if we keep the bandwidth requirement constant, or require higher bandwidth if we want to have the same amount of security as in FlyClient.

First, let’s see the similarities between this variant and FlyClient. The general flow of the protocol will be very similar: Light client fetches the last block header. The state root in the header also commits to the hashes of the historical blocks stored in the blockhash contract (BHC). Therefore the client can verify the hash of a sampled block header by verifying a merkle branch against the storage root of the BHC. Note that if you wanted to sample a subset of the chain today on the mainnet an adversary could return blocks that are not necessarily chained together. Having the adversary commit to a whole chain as EIP-2935 makes these kind of attacks harder.

The major difference between the two approaches lies in the tree structure they use to store the historical block hashes. Two properties that the Difficulty MMR has which the storage trie doesn’t are (among others):

1. Each node stores the cummulative difficulty of the blocks in that subtree
2. MMR allows efficient subrange check, i.e. checking that two MMRs share the first N leaves. To do this check with the storage trie, you’d have to send all the first N leaves.

Both of these properties make it harder for a malicious actor to deceive a light client. Without the first one, an attacker could craft a chain with a high number of low difficulty but valid (PoW-wise) block headers and insert a few high difficulty but invalid blocks in the middle to raise the total advertised difficulty of the chain. When sampling blocks without knowing the relative difficulties you have less chance of discovering these invalid blocks. When sampling an old block `B`, the second property allows you to verify that the chain from genesis to `B` is a prefix of the chain from genesis to the head.

As such we won’t be able to use the same sampling algorithm as in FlyClient. The naive option is of course to do uniform sampling, which requires many more samples to achieve relatively high security. Paul Dworzanski proposed adding the cummulative difficulty to the leaves in the BHC alongside the blockhash, and then do a binary search (similar to section 5.2 in the FlyClient paper) over the blocks, zooming in on subchains that have suspicious difficulty. Overally the sampling strategy to use in combination with this EIP, its bandwidth requirement and security guarantees are open problems.

#### Variant 2: Superblock-based

An alternative variant to random sampling was suggested by the author of EIP-2935:

> Make a subchain containing only blocks passing 1000x the difficulty threshold, with those blocks linked to each other through the history contract.

You might remember that each Ethereum block has a `difficulty` threshold that a PoW solution must surpass. Sometimes the PoW solution is higher than the threshold by a large margin. Since hashes are uniformly random, a PoW solution with a value double that of the threshold has 1/2 chance of occuring compared to a solution barely above the threshold.

Similar to [NiPoPoW](https://eprint.iacr.org/2017/963.pdf) (where I borrowed the term superblock from to refer to these lucky blocks), this approach uses these rare events to “compress” the header chain. Effectively a full node sends all the block headers in the chain where the solution is 1000 times the difficulty target. This should convince a light client that there’s a lot of mining power behind this chain. To choose between forks, light clients count the number of the superblocks in the proof.

With regards to security, let’s set the difficulty adjustment mechanism aside for a moment. Assuming that an adversary controls less than 50% of the mining power, the probability that they produce as many superblocks as the honest chain is very low. But difficulty is not constant in Ethereum. A hypothetical attack is to fork off and bring the difficulty down significantly. Given that downwards difficulty adjustment is capped at ~5%, the attacker could for example bring the difficulty down by a factor of 10^8 in ~350 blocks. Afterwards mining superblocks would be easier. The adversary might require significant mining resources to pull off this attack, but I haven’t estimated how much exactly. To alleviate this we can modify the fork comparison algorithm to be the sum of the actual difficulty of the superblocks in a proof (changed from a simple count of the superblock).

At any time there could be several thousand blocks of distance between the head of the chain and the last produced superblock on the honest chain. To avoid the scenario where an adversary fools a light client by forking off after the last produced superblock, the proof includes the headers for several thousand blocks at the tip. To reduce proof sizes, it should be possible to instead send fewer superblocks of a lower degree, e.g. blocks with 512, 256 and 128 times the difficulty target.

With all this in mind, the size of the proof a full node has to send to a light client was estimated by Vitalik as follows. Note that the parent’s header is required to compute the canonical difficulty, so the first part of the estimate might need to be roughly doubled.

> That would be roughly 10000 * (512 block header + 1500 for the proof), so about 20 MB, and then a bit more for the last few thousand blocks in the chain.

## Conclusion

To wrap up, we went briefly over the landscape for syncing light clients. From full verification of every block header being one end of the spectrum, and the hypothetical ZKP approach being close to an ideal syncing experience. There are feasible improvements to be found in the middle of the spectrum. If complexity wasn’t an issue FlyClient provides very good trade-offs without sacrificing any of the other use-cases.

The competitor is EIP-2935, with a simpler consensus change, on top of which we can design various light client sync protocols, e.g. via random sampling or superblocks. These protocols might not match FlyClient in some metrics and haven’t been formally analysed, they might however suffice to remove the need for CHTs. A more detailed comparison of the superblock approach and CHTs in terms of bandwidth requirement is still pending. The next concrete step is to define a more precise superblock-based algorithm on top of EIP-2935 and prototype it in a client to get quantitative data.

*Acknowledgements: This write-up would not have been possible without discussions and feedback from my teammates Alex Beregszaszi and Paul Dworzanski (from Ewasm), and Vitalik Buterin.*

## Replies

**BoltonBailey** (2020-09-29):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> MMR allows efficient subrange check, i.e. checking that two MMRs share the first N leaves. To do this check with the storage trie, you’d have to send all the first N leaves.

It’s not clear to me why it would be necessary to send the first N leaves of the storage trie. Isn’t it sufficient to simply send O(log(N)) of the internal nodes of the storage tree which correspond to the highest common ancestors of the leaves in the range?

More broadly, if the locations of the leaves in storage are byte-aligned and placed contiguously in memory, it seems to me like the trie acts just like an MMR: Updating requires O(log(N)) values along the right spine of the trie, and any binary interval range corresponds to an internal node of the trie.

---

**sinamahmoodi** (2020-09-30):

If I understood your comment correctly: the problem with the storage trie is that the keys are hashed. Hence the leaves won’t be in any particular order.

---

**vbuterin** (2020-09-30):

Thanks a lot for the writeup [@sinamahmoodi](/u/sinamahmoodi)! I think it would be great to have *any* kind of <25 MB proof that can be provided to a light client to prove that some block is part of the canonical chain; it would greatly improve light clients’ safety and efficiency properties.

---

**barryWhiteHat** (2020-09-30):

So just to summarize to check my understanding, basically we can make much better light clients if we have a hard fork to somehow link all historic blocks to the current block. Then we just randomly look some up to convince ourselves that they are all correct.

So I think I have a solution that i think will remove the need for the hard fork. How a server proves to a client that they are on the correct chain

1. Client asks server for latest block
2. Server gives client that block
3. Client says server send me the list of lucky blocks, which are blocks that contain a transaction where the EVM accesses the 256 previous block hashes
4. Client gets the lucky blocks, executes them and validates they are correct. Then adds the list of block hashes include in the execution to historic blocks it knows about.
5. Randomly selects some historic blocks to ask the server to give it.
6. Light client gets all the blocks that are not accounted for in its historic block list and checks their POW.

So we change the definition of lucky blocks to just be a block where the EVM accessed the 256 historic blocks it could see. RNG generates use these so these kind of lucky blocks should be pretty common.

---

**sinamahmoodi** (2020-09-30):

I see your point about not needing a hardfork and actually both flyclient and nipopow have gradual upgrade paths they call a velvet fork. I haven’t thought about them since I thought having a commitment to history is useful for other purposes, e.g. if clients start pruning history newly joined nodes can fetch an old block with a proof against the head.

Re this definition of a lucky block: it seems to me this kind of block can be crafted purposefully on an invalid chain. In fact they can only include such a lucky block after 256 valid blocks but never after an invalid block.

---

**barryWhiteHat** (2020-09-30):

> I see your point about not needing a hardfork and actually both flyclient and nipopow have gradual upgrade paths they call a velvet fork. I haven’t thought about them since I thought having a commitment to history is useful for other purposes, e.g. if clients start pruning history newly joined nodes can fetch an old block with a proof against the head.

Hardforks can sometimes be hard to get so having a non hardfork way to do this would make sense.

> Re this definition of a lucky block: it seems to me this kind of block can be crafted purposefully on an invalid chain. In fact they can only include such a lucky block after 256 valid blocks but never after an invalid block.

It depends how common these lucky blocks are. If someone uses this opcode more than 1 every 55 minutes / 2  then you should have these lucky blocks covering the entirity of history and its basically the same as the hard fork version. If its less than that you would have to get these “connecting” blocks and validate them. But this could be a constant dtat for historic chain and could be gossiped around rather than fetched from the server.

This idea also makes sense for covering the historic chain whihc i assume a hardfork woudl not cover.

Moving forward we could just ping this opcode every 55 mins / 2 in order to ensure that we always have coverage.

---

**BoltonBailey** (2020-10-01):

Thanks, I didn’t realize this (I haven’t looked at Ethereum in depth until recently).

Is there any particular reason why the location is hashed, rather than using the location itself as the index into the storage trie? It seems like this would take better advantage of locality of reference in terms of the batch proof size.

The only real downside I can see in this approach, which I guess might be serious, would be an attack where a contract is made having storage branches which are 256 hashes long.

To expand on this idea though, we could store not just the blockhashes, but also *a full MMR of block hashes within the EIP-2935 contract storage*. This would allow subrange checking, and would only take up twice the storage of the blockhashes themselves. We could also save the cumulative difficulty in this contract if we wanted to.

---

**guthlStarkware** (2020-10-01):

Thanks a lot for the wrap-up. Really nice to see people getting interested in light sync. It has significant importance in the context of ReGenesis and stateless Ethereum.

When it comes to the Velvel Fork in FlyClient, my understanding is that submitting a FlyClient MMR commitment would be equivalent to a PoW checkpoint.

Let me elaborate

1. Alice generates a non-interactive FlyClient proof of all previous blocks up to block 3000
2. Alice publishes the FlyClient proof, verifies it onchain, and stores it in a dedicated contract. Proof gets included at block 3010
3. At Block 4000, Bob requests the FlyClient proof from Alice.
4. Alice provides Block 3000 to Bob.
5. Bob replays the block and verifies the proof.
6. Alices provides blockhash 3001 - 4000.
7. Bob verifies the chainhash from block 3000 to 4000
8. Bob listens to the chain to get upcoming blocks

Bob could skip PoW verification from block 0 - 3000.

It does not provide commitment to history but would work for Proof of PoW in the context of Regenesis or to speed up sync (especially in the context of Beam sync)

Is it a correct understanding of Velvet fork?

---

**sinamahmoodi** (2020-10-06):

Sorry for the delayed response everyone.

[@barryWhiteHat](/u/barrywhitehat)

> This idea also makes sense for covering the historic chain whihc i assume a hardfork woudl not cover.

This is definitely a nice property. I’m specifically concerned about the following scenario: Say there is a valid chain and an adversary chain. The attacker can create these lucky blocks at will, and can position them in a way as to “hide” some invalid sections of the chain on *his fork*. Or possibly make every block in his fork a lucky block to increase the fork’s “lucky score”. I guess my intuition is that these “lucky blocks” are possibly not randomly lucky and can be created at any time which could lead to some edge cases. But I realize these sort of attacks require significant mining power from the attacker, and your approach has merits before we can hardfork a commitment to the chain.

[@BoltonBailey](/u/boltonbailey)

> Is there any particular reason why the location is hashed, rather than using the location itself as the index into the storage trie?

If I’m not mistaken otherwise contracts could grind for a narrow but very deep storage trie and this’d be a dos vector because the storage-accessing opcode gas costs don’t depend on the depth of that slot. I’m wondering however if this worry goes away after clients adopt the flat database layout.

[@guthlStarkware](/u/guthlstarkware) Unfortunately I don’t have a good understanding of the velvet fork. AFAIK contrary to a hard fork not all miners are expected to have activated FlyClient and blocks that don’t include the MMR are not rejected. Instead the FlyClient proof is modified to consider all the blocks between two upgraded-blocks as one block. But generally I think commitment to history is valuable even outside the light client context as you also mention and we should strive to hardfork it in.

---

**barryWhiteHat** (2020-10-06):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> This is definitely a nice property. I’m specifically concerned about the following scenario: Say there is a valid chain and an adversary chain. The attacker can create these lucky blocks at will, and can position them in a way as to “hide” some invalid sections of the chain on his fork . Or possibly make every block in his fork a lucky block to increase the fork’s “lucky score”. I guess my intuition is that these “lucky blocks” are possibly not randomly lucky and can be created at any time which could lead to some edge cases. But I realize these sort of attacks require significant mining power from the attacker, and your approach has merits before we can hardfork a commitment to the chain.

So I am not proposing to give each chain a score based upon “lucky blocks”

What i am proposing is to use “lucky blocks” as a kind of helper. I define a “lucky block” to mean a block that contains a transaction that accesses one of the past 256 blocks in the EVM.

Our helper points these blocks out to our user. The user downloads this block. Executes it and gets the list of the 256 historic blocks that were referenced. It does not get all of these blocks but it looks up some of the ransomly to confirm the chain.

Any blocks that are not covered by lucky blocks would need to be downloaded and verified as we do currently.

---

**BoltonBailey** (2020-10-17):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> If I’m not mistaken otherwise contracts could grind for a narrow but very deep storage trie and this’d be a dos vector because the storage-accessing opcode gas costs don’t depend on the depth of that slot. I’m wondering however if this worry goes away after clients adopt the flat database layout.

To be clear, a grinding attack is what can be carried out on the state tree as it currently is: The attacker can grind to find storage writes which hash to generate keys similar to keys which already exist. In a binary tree, the attacker can create a storage-access Merkle branch which is about \log_2(\text{Number of hashes the attacker can compute}) in expected length.

Without hashing the location, an attacker does not need to grind through hashes, and can immediately create a storage access Merkle branch of length 256 by writing to every location with index equal to a power of two.

Making the storage-accessing opcode gas cost would perhaps cause problems, such as making it harder to predict with certainty the gas cost of a transaction. I still think its interesting though, since it would encourage contracts to be written in a space efficient way.

---

**axic** (2020-12-04):

For the interested, during the ETHOnline summit [@sinamahmoodi](/u/sinamahmoodi) gave an overview and explanation of the above:

