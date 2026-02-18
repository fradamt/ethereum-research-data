---
source: ethresearch
topic_id: 7173
title: Survey of proposals to reduce block witness size
author: poemm
date: "2020-03-22"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/survey-of-proposals-to-reduce-block-witness-size/7173
views: 4163
likes: 10
posts_count: 8
---

# Survey of proposals to reduce block witness size

A [major bottleneck of statelessness is block witness size](https://blog.ethereum.org/2020/01/17/eth1x-files-digest-no-2/). Below are proposals to reduce block witness size. The first five proposals are already planned to be used.

(1) Hexary to binary tree [overlay](https://ethresear.ch/t/overlay-method-for-hex-bin-tree-conversion/7104). Over [3x](https://blog.ethereum.org/2020/01/17/eth1x-files-digest-no-2/) savings in the number of merkle hashes.

(2) Multiproofs to [deduplicate merkle hashes](https://www.wealdtech.com/articles/understanding-sparse-merkle-multiproofs/). ~1.5x savings in number of merkle hashes near the root.

(3) Maximize overlapping merkle paths. Related to (2), but worth mentioning separately. We need fast algorithms to build blocks which maximize overlapping merkle paths. Unfortunately, it is [undecidable](https://en.wikipedia.org/wiki/Rice's_theorem) *a priori* which merkle paths will be used by general transactions. But it may be decidable for [some transactions](https://ethresear.ch/t/stateless-mining-strategies/7172). Users may send overlapping transactions together. Perhaps 2x savings in number of merkle hashes is within reach – open problem.

(4) [Witness encoding](https://github.com/ethereum/stateless-ethereum-specs/pull/1). Tree structure encoding is [a small fraction of the witness size, which is dominated by hashes and code](https://medium.com/@akhounov/the-shades-of-statefulness-in-ethereum-nodes-697b0f88cd04), but maybe this fraction can be further reduced. A few percent savings in witness size.

(5) Code merkleization. Gives [2x code size reduction](https://blog.ethereum.org/2020/01/17/eth1x-files-digest-no-2/). Also noteworthy is that code compression gives [3x-4x code size reduction](https://github.com/ethereum/EIPs/issues/91#issuecomment-576397696).

(6) Deposit-as-rent. Power-users can deposit 1 Eth per byte to store their account in a witness-free way. The total of these bytes will currently be at most 110 MB (plus some overhead). Savings from this is an open question.

(7) Cache. Experiments by [Alexey](https://medium.com/@akhounov/the-shades-of-statefulness-in-ethereum-nodes-697b0f88cd04) and [Igor](https://medium.com/@mandrigin/semi-stateless-initial-sync-experiment-897cc9c330cb) show that a cache of recent block witnesses can give a ~10x (!!!) savings in witness size. Unfortunately, [consensus caches are complicated](https://gist.github.com/holiman/2fae5769b0334b857443b53a5aa746ec), so caches may be at the networking-layer until we become desperate for consensus witness size reductions. If consensus caching is considered, a related option is a consensus transaction pool (a two-step process (i) transactions with access lists but no witnesses are included in blocks and put in a consensus transaction pool, and (ii) their execution is delayed until a reasonable amount of time, say 100 blocks, for their witnesses to propagate).

(8) 20 bytes per merkle hash. We already depend on 20 byte hashes for addresses. For security, the system can be adaptive: when a hash collision is detected, it triggers a tree remerklization to add two extra bytes per hash. This gives a 1.6x savings in hash size.

(9) New stateless-friendly dapps. Stateless-friendly patterns are needed. Savings from this is an open question.

Any block witness size reduction proposals missing? Any feedback on the above proposals?

## Replies

**poemm** (2020-03-23):

Something interesting. Size savings may have non-linear effects – size savings allows more transactions, which allows more deduplication in (2) and more overlapping in (3).

---

**pipermerriam** (2020-03-23):

I wanted to add a note about access lists (a list of accounts and storage slots accessed during a block).  Under the presumption that the state is available, an access list will be smaller than a witness (no intermediate hashes, no code).

Witnesses and Access lists certainly do not serve the same purpose, but this concept feels like it is at least worth including in the mental model.

---

**axic** (2020-03-25):

Two more possibilities to reduce the witness size is by giving the following new options to contracts:

1. Keep trie keys un-hashed so that contracts can optimise their witness layout.
2. Introduce variable length storage (where the storage value can be larger than 256 bits). This allows contracts to reduce the number of trie nodes they occupy. As an example, all the following take at least 4 storage slots which are mostly accessed the same time (e.g. needs to be present in the witness): a Gnosis Multisig Wallet transaction; a DAI CDP position; a DEX trade.

And an option similar to (6) in the initial post is to consider keeping all the contract codes to be kept by each node. According to some measurement all the code currently amounts to around 100-150 MB. This can be further reduced by deduplicating via merklization. The problem however is that blocks are not self-contained anymore as the block witness is not enough to process it.

---

**lithp** (2020-03-26):

Great list, thanks for compiling it!

[Vitalik’s post from a few months ago](https://ethereum-magicians.org/t/protocol-changes-to-bound-witness-size/3885) goes into (1), and also mentions something which isn’t on your list:

(10) Increase gas costs. If transactions pay an increased cost proportional to how much they increase the block’s witness size then the block gas limit will also limit the witness size. Using this we can ensure that witnesses will never exceed 1MB (or whatever number we decide is safe). The other methods of reducing witness size (1-9) then become methods of recapturing throughput.

---

**lithp** (2020-03-26):

Another, more exotic, method:

(11) [Polynomial commitments](https://ethresear.ch/t/using-polynomial-commitments-to-replace-state-roots/7095). I’m not sure if we’re ready for them yet but they might provide significant savings:

> This technique can provide some benefits for multi-accesses of block data. But the advantage is vastly larger for a different use case: proving witnesses for accounts accessed by transactions in a block, where the account data is part of the state. An average block accesses many hundreds of accounts and storage keys, leading to potential stateless client witnesses half a megabyte in size . A polynomial commitment multi-witness could potentially reduce a block’s witness size down to, depending on the scheme, anywhere from tens of kilobytes to just a few hundred bytes.

---

**lithp** (2020-03-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> (3) Maximize overlapping merkle paths. Related to (2), but worth mentioning separately. We need fast algorithms to build blocks which maximize overlapping merkle paths. Unfortunately, it is undecidable  a priori which merkle paths will be used by general transactions. But it may be decidable for some transactions . Users may send overlapping transactions together. Perhaps 2x savings in number of merkle hashes is within reach – open problem.

If a 2x savings were possible it would be a worrying sign, because it would mean that miners would have an incentive to try to run this algorithm themselves. If they can reduce the witness by this much it means they can increase the speed at which their blocks propagate, winning some extra revenue from reduced uncle rates. Because the algorithm would be so complicated, this gives larger miners (or mining pools) an additional advantage over smaller mining pools.

---

Here are some more radical proposals:

(12) Larger and more infrequent blocks (a 30 second block time) would provide more opportunity for witness aggregation, meaning the same number of transactions would lead to smaller witnesses.

(13) Adopting [GHOST](https://eprint.iacr.org/2013/881.pdf) or a similar design (don’t believe the abstract, Ethereum does not implement GHOST) would not make the witness size smaller but it would alleviate much of the impact of large witness sizes. Blocks which take a while to propagate would not pose a security risk.

(14) If transactions included their own witnesses (like how ETH2 is expected to work) then nodes would already have most of the block witness in their mempool. A block propagation protocol which took advantage of that could send much less witness data during block propagation.

(15) An improved block propagation protocol (much like [Bitcoin’s FIBRE](https://bitcoinfibre.org/)) might cause blocks to propagate much faster. If blocks and witnesses propagated faster then increased witness sizes would again not be as much of a concern.

(16) If witnesses did not need to propagate alongside blocks then witness size isn’t a large concern.

(17) A better understanding of how blocks propagate might win us some witness size. Currently, miners which accept a block must first process it before attempting to build new blocks on top of it. Witnesses reduce the amount of time it takes to process blocks. However, witnesses mean that blocks take longer to get to the miners. If the first effect is larger than the second then larger witnesses would be acceptable.

(18) I’m not sure what you meant by (9), but we could encourage Dapps to lean on CALLDATA by giving it a decreased gas cost. CALLDATA is propagated along with transactions so we can expect it to already be in the mempool of receiving nodes, a witness propagation algorithm would took advantage of this would be able to send less data. If we paired this with increased costs for calls such as SLOAD we could heavily incentivize dapps to start leaning on CALLDATA. (this is a variant of 14 which we can move to without forcing dapp developers to change anything)

(19) EXTCODESIZE requires having access to the entire bytecode. The naive answer would be to make it very expensive, but a more reasonable answer would be to store the code size in the account data. This requires re-writing the entire account trie.

---

**SergioDemianLerner** (2020-03-30):

(10) Instead of hashing keys to get the path, you can hash the key, grab the first 10 bytes of the hash and concatenate with the full original key. This is what RSK currently does.

For example, a 20 bytes contract address currently takes 32 bytes for the path (the hash).

We can compress this and at the same time avoid storing the pre-images in a different database by using the following path as key:

10-bytes hash prefix + 20 bytes account address

This requires only 30 bytes (2 bytes less), but saves another 64 bytes if you need to store the (key, pre-image)  entry in a map.

The hashes prefix is used to randomize the position and prevent degeneration attacks to the data structure.

This idea was proposed initially by Angel J. Lopez, working on RSK.

For more info check https://blog.rsk.co/noticia/towards-higher-onchain-scalability-with-the-unitrie/

