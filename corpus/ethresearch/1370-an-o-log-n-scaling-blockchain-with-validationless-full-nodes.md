---
source: ethresearch
topic_id: 1370
title: An O(log(n))-scaling blockchain with validationless full nodes using data availability schemes
author: musalbas
date: "2018-03-12"
category: Sharding
tags: []
url: https://ethresear.ch/t/an-o-log-n-scaling-blockchain-with-validationless-full-nodes-using-data-availability-schemes/1370
views: 4087
likes: 3
posts_count: 6
---

# An O(log(n))-scaling blockchain with validationless full nodes using data availability schemes

I’d like to propose a thought experiment/protocol, based on proposed data availability schemes such as [this](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding). Some have [previously argued](https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2014-December/007029.html) that a blockchain is primarily a proof-of-publication system; i.e. once you publish some data on it, you as a full node know that it is available, at least to the participants of that system following the protocol rules correctly. However, if it’s possible to convince yourself that data is available without running a full node, then this leads to some interesting consequences, such as creating a cryptocurrency where full nodes only need to do O(log(n)) operations per block, where n is the number of transactions in a block.

Blockchains that push all the transaction validity consensus rules to clients that care about specific transactions, rather than all the full nodes, have been proposed before, but here we propose one where full nodes only need to do O(log(n)) operations per block, with the help of data availability proofs.

Suppose we have a UTXO-based blockchain where full nodes do no validation on transactions whatsoever; the blockchain is purely there to order transactions. Additionally, this blockchain has the structure of an [Certificate Transparency style Merkle tree](https://tools.ietf.org/html/rfc6962#section-2.1) (aka Merkle Mountain Ranges). This means given two trees A and B, you can prove that the two trees are consistent (i.e. tree B has all of the elements of tree A, plus some additional elements, and thus proving the append-only property of the tree) in O(log(n)) time where n is the number of elements added to tree A to make tree B. Suppose that each block simply contains a) a Certificate Transparency style Merkle tree containing every single transaction in the blockchain, b) a merkle consistency proof to show that transactions were only added to the tree in the last block, not removed and c) the data of the new transactions in the block.

The last one, c), does not need to be downloaded by full nodes, and that node will still be as secure as any other node, in that they cannot be made to accept blocks that are invalid according to the consensus rules through a 51% attack, because the transaction data is not a part of the consensus rules.

Because invalid transactions and double-spends are allowed on this blockchain, we have an implicit, client-side, rule for determining which transactions are valid; and any other client following the same rule will consider the same set of transactions to be valid. We say that a given transaction on the blockchain is valid if a) it meets all the standard transaction validity rules (good signature, enough balance, etc) and b) it is the first transaction on the blockchain to spend all the UTXOs it references as inputs.

One of the properties of a full node is that it does not need to trust anyone to determine the network’s valid chain according to the protocol rules (trustless), but traditionally they need to process and verify all the transactions, an O(n) operation for n transactions per block. However, here we have proposed a type of full node that can still trustlessly determine the network’s valid chain, but with only O(log(n)) operations for n transactions per block. Note we can still enforce blocksize limits if we want to (in the form of number of transaction per block), as we can calculate the number of transactions added to each block from the merkle consistency proofs.

Of course, the system is only useful if we can actually use this as a cryptocurrency, which means we need a way for nodes to figure out which transaction was the first to spend a particular UTXO, to prove that a payment was successful. But this is only possible in the first place if the data in each block is actually available, because a miner can mine a block, withhold the block’s transaction data, and release the data later, and that block may contain transactions that spent certain UTXOs before transactions in future blocks. So nodes have to rely on data availability proofs to make sure that block transaction data is available, before accepting each block.

For nodes to figure out with transactions were first to spend certain UTXOs, we can have a new type of node, an archival node, which nodes can query to ask “Which was the first valid transaction to spend this UTXO?”, and the archival node responds with a signed reponse.

To disincentivise archival nodes from lying, they can deposit some money in a contract, such that they lose their deposit, upon proof that the archival node responded with a certain transaction, when there is evidence that there is in fact an earlier transaction spending a UTXO, and the fraud prover is rewarded with some money. This proof itself should also be backed by a deposit, in case there is an even earlier transaction than specified in the proof. This deposit should be equal to the amount of money transfered by the transaction being referenced, plus some more for the fraud proof reward. Archival nodes can also be further positively incentivised to run such nodes in the first place, by people paying for their service. Therefore we end up with a cryptoeconomic incentive model where it is never profitable for an archival node to lie about what transaction was first, because if they try to do so to trick a user that a money has been transfered when it hasn’t, then the archival node will lose the same amount of money that they lied about anyway. If the transaction is transferred too much money such that it is unlikely for any archival node to have that amount of money, the user can probably afford to run their own archival node.

The cryptoeconomic model proposed is just one of several models to let full nodes discover valid transactions. Other possibilities include solutions such as [VerSum](https://people.csail.mit.edu/nickolai/papers/vandenhooff-versum.pdf), where a full node asks many archival nodes, and only one of them need to be honest.

However, the key to all of this of course, relies on how good the underlying data availability scheme is. If you download the data yourself (i.e. traditional full nodes), then you’re 100% sure the data is available. If you use a [data availability scheme based on i.e. erasure coding](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding), it may be more like 99.99%. Does the 0.001% make all the difference in the confidence of a node to trust that a transaction is valid?

## Replies

**vbuterin** (2018-03-12):

The problem is that you still need an O(log(n))-scaling data availability proof method, and the erasure coding stuff described there doesn’t really achieve that; the best you can do is prove approximately O(c^2) data without super-fancy math like STARKs, and with the super-fancy math you can go much higher but you still need a protocol for actually building the proofs especially if they ultimately consist of much more data than a single node can aggregate. I once thought about this and came up with a recursive protocol that creates an N-dimensional erasure code, but it is tricky and complex.

VerSum-like strategies are also problematic at those scales, because unless coin holdings are heavily concentrated, each signature can only stand for a very small portion of funds, and so causing an escalation in the protocol can be very cheap and this leads to a DoS vector.

---

**musalbas** (2018-03-13):

Ah OK; becase proving that the merkle tree was constructed incorrectly is an O(\sqrt{n}) operation? That’s still much better than O(n).

---

**vbuterin** (2018-03-14):

Wait, how can you prove that the tree was constructed incorrectly in O(sqrt(n)) time? Is that assuming that you’re using a 2D erasure code?

---

**musalbas** (2018-03-16):

Yes. I’m going by the stats for 2D erasure codes on https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding.

```auto
Size of light client proof (1 MB): 48 branches * (256 bytes + 6 Merkle tree intermediate hashes * 32 bytes per hash) + (128 Merkle roots * 32 bytes per hash) = 25600 bytes
Size of light client proof (4 MB): 48 branches * (256 bytes + 7 Merkle tree intermediate hashes * 32 bytes per hash) + (256 Merkle roots * 32 bytes per hash) = 31232 bytes
Time spent to encode in C++ (1 MB): 7.5 seconds
Time spent to encode in C++ (4 MB): 43.45 seconds
Time spent to verify fraud proof (1 MB): < 0.01 seconds
Time spent to verify fraud proof (4 MB): < 0.01 seconds
Maximum size of fraud proof (1 MB): 6 Merkle tree intermediate hashes * 32 bytes per hash * 64 elements = 12288 bytes
Maximum size of fraud proof (4 MB): 7 Merkle tree intermediate hashes * 32 bytes per hash * 128 elements = 28672 bytes
```

For fraud proofs of 1MB blocks (4096 chunks), the proof has \sqrt{4096} elements. For 4MB blocks (16384 chunks), the proof has \sqrt{16384} elements. Same with light client proofs; where the number of merkle roots is 2\sqrt{number\_of\_chunks}.

Of course, the number of Merkle tree intermediate hashes also increases, so I suppose the complexity would be more like O(log(n)\sqrt{n}).

Am I missing something?

---

**musalbas** (2019-10-12):

It looks like this is actually possible in O(\log(n)) now, thanks to [this](https://eprint.iacr.org/2019/1139) paper published last week!

