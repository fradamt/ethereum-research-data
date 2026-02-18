---
source: ethresearch
topic_id: 4423
title: ERC20 Snapshot using Merkle Proofs
author: jochem-brouwer
date: "2018-11-29"
category: Security
tags: []
url: https://ethresear.ch/t/erc20-snapshot-using-merkle-proofs/4423
views: 3289
likes: 4
posts_count: 8
---

# ERC20 Snapshot using Merkle Proofs

If an ERC20 contract has a vulnerability, we want to redeploy the contract but hence (in most cases) also have to copy the entire storage to this new address. Most implementations simply upload all accounts and their associated balances to the chain, but this costs a lot of gas and many accounts will be untouched forever since users forgot about their tokens or they are dust amounts of tokens.

I created a proof of concept using Merkle Trees. A new ERC20 contract is uploaded to the chain with a certain Merkle Root. Users can now prove that they had an address associated with a balance by uploading the Merkle Proof to the chain. This means that: 1) users pay for gas themselves (if this is ethical, that is debatable) 2) only users who wish to get their tokens back have the incentive to go on-chain and 3) users can forever claim their tokens, the only requirement is connecting to an Ethereum archive node.

[Github](https://github.com/jochem-brouwer/ERC20Snapshot)

[Medium article](https://medium.com/@jochembrouwer96/erc20-snapshot-using-merkle-trees-aeeac48ce925)

## Replies

**kowalski** (2018-11-29):

Cool, thanks for sharing this.

I can see that in your leafs you put `soliditySha3([address, balance])` and than making a list of data points in arbitrary order. That’s okay I guess.

You could consider using sparse merkle tree instead and just having your leafs as `balance`. In such setup your tree would always be of height of 40 levels and have 2^{40} leafs. To get a proof of a balance of certain address you simply take it’s index treating the address as integer (or it’s bit representation of map to the leaf).

I believe it gives you exactly same length of proof, but is also more flexible. For example you can generate a proof that certain address’s balance is zero. In your setup such proof would require revealing the whole tree, because there is no way to know upfront on which leaf position specific address balance would have been included.

---

**jochem-brouwer** (2018-11-29):

Thank you [@kowalski](/u/kowalski) ! I have heard of sparse merkle trees before but did not realize it also allows one to prove non-inclusion in the tree.

If the goal of the snapshot is to reduce gas costs for the end-user, the merkle tree as implemented currently should be used, since this reduces the amount of leaves. However, if it is also necessary to indeed prove that an address had a zero balance then the sparse tree should be used.

However, what I have against using a sparse tree (and please correct me if I’m wrong) is that you would indeed need 2^{40} leafs - this would also require one to hash 2^{40} leafs which is unfeasible at this moment in order to obtain the Merkle Root. Furthermore, if a client wishes to generate a proof, they need to redo the entire process in order to obtain the necessary hash items to generate a proof. Can you also elaborate how you get the number 2^{40}? If the leafs include all addresses this should be 2^{160} leafs? (An address is 20 bytes, so 20*8 = 160 bits?)

Am I missing something here?

EDIT: I guess a cache can be used per https://eprint.iacr.org/2016/683.pdf ?

---

**hkalodner** (2018-11-29):

Somebody more familiar with sparse Merkle trees should correct me if I’m wrong, but I think the trick to make them efficient is to define a special hash value which is the hash of an empty subtree. From there the computation is based on the number of non-null items in the tree rather than the number of leaves. Further, Merkle proofs can be compressed assuming that many of the hashes in the Merkle proof will be this special empty value.

---

**jochem-brouwer** (2018-11-29):

[@hkalodner](/u/hkalodner) Yes that concept appears to be the idea behind this article: https://eprint.iacr.org/2016/683.pdf ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=9). That realization will indeed make the proof less computationally expensive. If you think about it, it indeed makes no sense to keep hashing the same value over and over if you can cache it.

---

**kowalski** (2018-11-29):

My bad, indeed the tree has to have 160 levels, but that doesn’t mean that the proof requires passing all 159 hashes leading from leaf to the root.

As @khalodner pointed out the idea behind sparse merkle tree is that the vast majority of leafs hold `balance = 0`. That’s what “sparsness” stands for.

As a result majority of hashes on level 2 are `hash(0, 0)`, on level 3 `hash(hash(0, 0), hash(0, 0))` and so on.

In merkle proof you only provided the hashes which are different than `zeroHash[level]` and you include along one additional 20-byte integer which is a bitmap telling the verifier which hashes are to be taken from `zeroHash[]` and which from the proof `bytes`.

As a result, if your sparse tree has `N` non-zero elements and they are evenly distributed you get that you will only get log_2 N non-zero hashes in the proof, which is exactly the same length as you would have gotten in regular merkle tree. The whole structure is usefull in context of ERC20 tokens and ethereum addresses in general because ethereum addresses satisify the requirements of being evenly distributed.

---

**jochem-brouwer** (2018-11-29):

[@kowalski](/u/kowalski) I like this and will add it for completeness. This will also reduce the calldata since the “order” of hashes do not need to be included.

I think I will implement the proof as a function which takes `bytes32[]` and an `uint`. The uint is actually a boolean array (which can hence store 256 bools) which determines if the next leaf is te cached version of `null` hashes or not.

---

**kowalski** (2018-11-29):

Yeah, I think you’re on right path. Good luck!

