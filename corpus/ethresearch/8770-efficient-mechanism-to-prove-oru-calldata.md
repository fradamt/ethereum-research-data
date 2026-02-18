---
source: ethresearch
topic_id: 8770
title: Efficient mechanism to prove ORU calldata
author: matt
date: "2021-02-26"
category: Layer 2
tags: []
url: https://ethresear.ch/t/efficient-mechanism-to-prove-oru-calldata/8770
views: 3495
likes: 3
posts_count: 7
---

# Efficient mechanism to prove ORU calldata

*Thanks to [@djrtwo](/u/djrtwo) for collaborating on this idea.*

### Problem

In order to prove a fraudulent transition of an optimistic rollup, the challenger typically needs to first prove that the input to the fraud proof is the same input the sequencer originally attested to. This avoids challengers fabricating the input to the state transition.

To prove the input, the transactions in the sequencer’s calldata must be authenticated. This can be done by creating a commitment to the input within the contract during a block submissions. This would give the rollup a trusted root to authenticate against in future fraud proofs. The downside is that this incurs costs, such as memory expansion for loading the calldata, calculating the root in EVM, and finally, storing the root in storage.

This is unfortunate because the calldata is *already* merkleized in the the transaction trie as part of normal consensus operations. It would be preferable to utilize the transaction trie root instead. This is accessible via the `BLOCKHASH` opcode, however it can only provide hashes of the 256 most recent blocks. Proofs beyond those blocks would need to be recursively proved against the oldest available block hash. This is problematic because the proof size would increase linear overtime, and would eventually no longer be able to processed in a single block.

### Solution

To avoid this, we propose that the rollup contract support the retroactive creation of “trusted checkpoints”. Instead of recursively proving the block in question all in one go, the challenger(s) can iteratively build trusted checkpoints in the rollup contract until root of the block in question is trusted by the contract. At that point, the fraud proof may be submitted as normal.

With a long challenge period, it is infeasible for an adversary to censor the root chain long enough to stop challengers from recursively proving the root of the invalid block and submitting the fraud proof to roll the chain back. In most cases, the fraud proof will be able to be submitted immediately and immediately use the output of `BLOCKHASH`.

Yes, this will cause fraud proofs to be much more costly in the worst case. However, it greatly optimizes for the optimistic case.

#### Feasibility

To show the feasibility of this approach, we’ll sketch out a rough estimate for the number of headers that can be authenticated in a block.

The formula will generally follow the form of `intrinsic_cost + calldata_cost + mem_expansion_cost + hashing_cost + overhead_cost`.

A header is approximately 500 bytes. At `16` gas per non-zero byte, providing a single header will cost `500 * 16 = 8000` gas. The cost to hash the header is `126` gas1. The memory will need to be large enough to fit the parent header’s hash, the current header being hashed, and it’s hash. That works out to `32 * 2 + 500 = 564` bytes. To expand the memory to this size is `54` gas2. Each header will need to be loaded from calldata into memory. This costs `51` gas3.

Filling in the formula from above, we should have something like:

`21000 + X * (8000 + 126) + 51` where `X` is the number of headers. Solving for a gas limit of `12.5mm`, we find `X` to be 1535 blocks. To account for the many jumps, comparisons, and shuffling of data, we should safely assume that we can authenticate *at least* `1400` headers per block.

#### Example

Suppose there exists an ORU with a 1 week finalization delay. At block N, an invalid state transition is committed to. The sequencer who submitted the invalid transition is able to censor fraud proof attempts for 23,000 blocks (~3.5 days). Roughly 1400 blocks can be authenticated at a time on L1, so at block `N + 23000 + ceil(23000 / 1400) = N + 23017`, the header for block N will be authenticated and the fraud proof can proceed.

–

1: https://github.com/wolflo/evm-opcodes/blob/aec21e512e0f303513c3cd9d306f8661afd2fc65/gas.md#a4-sha3

2: https://github.com/wolflo/evm-opcodes/blob/aec21e512e0f303513c3cd9d306f8661afd2fc65/gas.md#a2-memory-expansion

3: https://github.com/wolflo/evm-opcodes/blob/aec21e512e0f303513c3cd9d306f8661afd2fc65/gas.md#a5-copy-operations

## Replies

**MicahZoltu** (2021-03-02):

IIUC, the goal here is to make it easier for contracts to verify that a particular transaction was included at a particular point in history?

I think we can solve that by introducing a couple new features:

1. Global transaction merkle tree that contains all transactions in history.
2. A mechanism for the EVM (precompile) to validate that a particular transaction (by its hash) appeared in a particular block at a particular index.

(1) may sound intimidating at first, but I think we can mitigate unbounded growth and the need to store all transactions forever by just asserting that the tree is only guaranteed to contain the last `n` blocks worth of transactions.  We can do this using a mechanism similar to [Resurrection-conflict-minimized state bounding, take 2](https://ethresear.ch/t/resurrection-conflict-minimized-state-bounding-take-2/8739/2) except without the resurrection semantics (which makes it even easier).  We simply have the path to a transaction be `block_number || transaction_index || transaction_hash`.  This way, we end up with transactions grouped by block in the tree and we can simply prune that entire branch of the tree once it reaches expiration.  We can set this to say a month or something that should be more than enough for any ORU and I don’t think we would run into any significant state growth problems from it.  We could *also* drop the per-block transaction root I think because it would essentially be a branch of this new larger tree.

(2) would then allow any ORU fraud proof validator to receive a `block_number, transaction_index, transaction` as input and validate that it did get included in the chain at that position without having to do merkle proof validation in the EVM.  The only thing the ORU validator would need to know how to do is hash the transaction.

We could take this a step further and allow the encoded transaction to be passed to the precompile, which would mean that when we add new transaction types the ORU doesn’t actually need to support the signing mechanisms, it only needs to know how to pluck data out of an encoded transaction.

---

**vbuterin** (2021-03-02):

**I would highly recommend against implementing something like this right now.** The issue is that we are planning a likely move to Verkle trees and/or SSZ, and so the RLP branch verification logic will change in backwards-incompatible ways at some point in the next 1-2 years and break all existing contracts that rely on it. I would instead recommend continuing to use calldata for the moment, and then waiting for eth2 sharding at which point we may well just add an explicit opcode that verifies that a piece of shard block data matches its commitment, which would be forward-compatible.

---

**matt** (2021-03-02):

Agreed, probably should have mentioned that after the merge it should be possible to authenticate historic calldata through the eth2 block root and so this mechanism will no longer be needed. However, I think it is a nice reduction in the happy case today and as long as teams are aware that this will likely stop working in the future, I don’t see an issue with them utilizing it until something better comes along.

---

**matt** (2021-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> IIUC, the goal here is to make it easier for contracts to verify that a particular transaction was included at a particular point in history?

Yes, exactly.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I think we can solve that by introducing a couple new features:
>
>
> Global transaction merkle tree that contains all transactions in history.
> A mechanism for the EVM (precompile) to validate that a particular transaction (by its hash) appeared in a particular block at a particular index.

These make sense, although I don’t have a comment on their viability. One nice property about the precompile is that it will be more resilient to changes of the header than other approaches which must rely on the header and its underlying representation.

---

**r1cs** (2021-10-19):

Maybe we can just record transactions which prefer to be stored in a totally different tree storing tx hash which can be verified directly no matter how old this transaction is, they just need to pay a bit more gas fee is fine.

---

**MicahZoltu** (2021-10-19):

SSZification of blocks would, I believe, make it so we can prove transaction presence anywhere in history with a single proof.  This has been discussed in the past, though isn’t currently under active development.

