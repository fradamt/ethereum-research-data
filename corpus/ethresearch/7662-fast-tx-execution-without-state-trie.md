---
source: ethresearch
topic_id: 7662
title: Fast Tx Execution Without State Trie
author: qizhou
date: "2020-07-09"
category: EVM
tags: []
url: https://ethresear.ch/t/fast-tx-execution-without-state-trie/7662
views: 2919
likes: 2
posts_count: 3
---

# Fast Tx Execution Without State Trie

To make sure every node in the network agrees on the same result of transaction execution, a lot of blockchains such as Ethereum, Cosmos Hub, include the hash of the state trie, where the state is represented as a key-value map.  After a transaction is executed and parts of the key-value pairs in the state are updated, the state trie is also updated, and the hash is re-calculated and included in the block header. As long as all nodes agree on the same hash, we ensure that all the nodes also agree on exactly the same state.

However, reading and writing the state trie can be expensive - a read will traverse the internal nodes of the path to the key and a write will update several internal nodes of the path to the key-value pair.  Consider a trie with depth 5, a trie read may perform 5 underlying DB reads, and a trie write may perform 5 underlying DB writes besides 5 DB reads.  When the number of entries in the state trie is large, the executing of a transaction can be slow, and thus system throughput will be lowered.

The proposed fast tx execution without state trie uses a traditional key-value DB to represent the state.  To make sure every node agrees on the same tx result, instead of including the hash of the state in each block, we include the hash of the updates of the state, i.e., a list of DB write and delete operations, after performing all the transactions in the block.  As a result, a read from the state always takes one DB read, and a write to the state always takes one DB write - no matter how many entries are in the state.  In addition, as long as we ensure the hash of the updates (deltas) are the same for every node, we could ensure every node will have the same state of the network.

However, using the hash of updates instead of the hash of the state creates several questions:

- If the chain is re-organized, how to recover the state of a previous block?  A way is to undo the transactions like Bitcoin does, or we could resort to the underlying DB snapshot feature, which is very cheap for most DBs such as leveldb.
- How to quickly synchronize a node?  A quick sync will only download the block headers and then the state of a close-to-latest block.  It could use the state trie hash to verify the correctness of the state of the block downloaded from another untrusted client.  Without state trie hash, a solution may require every node to periodically create a snapshot block (maybe every 2 weeks or 80000 blocks) - a normal block containing the hash of the state of the previous snapshot block (likely using a trie). This means that a client could use 2 weeks to re-calculate the hash of the state trie instead of every block.  As a result, a quick sync can be done by obtaining the hash of the latest snapshotted state, downloading the state, and verifying it.  After the quick sync is done, the node could download the remaining blocks and replay them to obtain the latest state.
- How to lightly check if a key-value pair is in the latest state?  Given the hash of a state trie, a user could quickly check the existence of a key-value pair (e.g., such as the balance of an account) by querying the cryptographic proof of the inclusion of the key-value pair (the paths to the key-value pair in the state trie).  Without state trie in each block, we could check by using the most recent snapshot and its hash, which can be out-dated. To obtain the latest result, there are a couple of ways.  One way is that a user may need to replay the remaining blocks, or a mini trie (likely a sparse tree mostly in memory) that represents the latest updated key-value pairs since the latest snapshot is maintained and the hash is included in the header.

## Replies

**adlerjohn** (2020-07-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> instead of including the hash of the state in each block, we include the hash of the updates of the state

You’re describing the Merkle root of transactions in an UTXO-based chain: [Block Chain — Bitcoin](https://developer.bitcoin.org/reference/block_chain.html#block-headers).

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> a list of DB write and delete operations, after performing all the transactions in the block. As a result, a read from the state always takes one DB read, and a write to the state always takes one DB write - no matter how many entries are in the state.

You’re describing the UTXO data model: [Practical parallel transaction validation without state lookups using Merkle accumulators](https://ethresear.ch/t/practical-parallel-transaction-validation-without-state-lookups-using-merkle-accumulators/5547).

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> If the chain is re-organized, how to recover the state of a previous block

Just un-apply the state deltas.

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> How to quickly synchronize a node?

Since you don’t need to compute a state root at every block, you can simply apply all the state updates from genesis (very cheap) and compute the final root. Signature verification can be skipped if we only care about verifying the integrity of a state snapshot, not its correctness: [bitcoin/doc/release-notes/release-notes-0.14.0.md at cc9d09e73de0fa5639bd782166b171448fd6b90b · bitcoin/bitcoin · GitHub](https://github.com/bitcoin/bitcoin/blob/cc9d09e73de0fa5639bd782166b171448fd6b90b/doc/release-notes/release-notes-0.14.0.md#introduction-of-assumed-valid-blocks).

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> How to lightly check if a key-value pair is in the latest state?

One way is by changing the block format to order inputs and outputs: [Compact Fraud Proofs for UTXO Chains Without Intermediate State Serialization](https://ethresear.ch/t/compact-fraud-proofs-for-utxo-chains-without-intermediate-state-serialization/5885). Then you can provide exclusion proofs for each block that a UTXO wasn’t spent. Linear in the number of blocks unfortunately, so maybe not applicable to on-chain light clients.

---

**qizhou** (2020-10-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> You’re describing the Merkle root of transactions in an UTXO-based chain: https://developer.bitcoin.org/reference/block_chain.html#block-headers .

Actually, it has nothing to do with what type of ledger model is (UTXO/Account-based).  For account-based, the updates of the state means the following KV operations

- update(addr, account) (for balance/nonce update, create a new account, etc)
- delete(addr, account) (for contract suicide)
- update(addr + "/" + storage_slot, storage_data) (for SSTORE)
- delete(addr + "/" + storage_slot, storage_data) (fro SSTORE with zero value)

A following work for the idea can be also found [here](https://ethresear.ch/t/eip-alternative-eth2-0-a-non-sharding-approach/8170).

