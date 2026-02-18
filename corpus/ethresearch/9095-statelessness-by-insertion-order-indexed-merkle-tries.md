---
source: ethresearch
topic_id: 9095
title: Statelessness by Insertion-order Indexed Merkle Tries
author: BoltonBailey
date: "2021-04-05"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/statelessness-by-insertion-order-indexed-merkle-tries/9095
views: 2977
likes: 2
posts_count: 9
---

# Statelessness by Insertion-order Indexed Merkle Tries

I’m taking the opportunity to post some some research that my colleague Surya Sankagiri and I did which relates to stateless cryptocurrencies. You can find a link to our paper [here](https://eprint.iacr.org/2021/340.pdf). While our project focused on applying statelessness to Bitcoin, it took inspiration from the use of the binary Merkle Tries that [this forum](https://ethresear.ch/t/binary-trie-format/7621) has discussed for an Ethereum shift to statelessness, and I think that there are a few ideas that the Ethereum community will find interesting, especially in light of [Vitalik’s](https://ethresear.ch/t/resurrection-conflict-minimized-state-bounding-take-2/8739) [recent](https://hackmd.io/@HWeNw8hNRimMm2m2GH56Cw/state_size_management) [posts](https://hackmd.io/@HWeNw8hNRimMm2m2GH56Cw/state_expiry_paths) on paths forward for limiting the Ethereum state size.

## The Locality Principle for Statelessness

The main idea of our work stems from the [UTREEXO](https://eprint.iacr.org/2019/611.pdf) paper, which made the observation that in the Bitcoin network, coins tend to be spent very soon after they are sent. This has implications for stateless nodes that use hash tree accumulators, as UTREEXO and our work do, and as the Ethereum stateless initiative seems to be planning to do.

To summarize our findings, *it is good to keep recently touched parts of the state nearby each other on the state tree, as this leads to smaller witness sizes*. Our paper constructs an accumulator which conforms to this principle by keeping the transactions in the Bitcoin state in a binary trie. Transactions are appended to this trie in the order of their insertion into the blockchain, and they are deleted when they are spent. This strategy makes witnesses tend to share proof data with each other and ultimately cuts down the witness size as compared to UTREEXO.

There is a good chance that this approach would work even better for Ethereum than it does for Bitcoin. In addition to direct externally-owned-account-to-externally-owned-account transfers, Ethereum also has popular smart contracts that are touched frequently. Under this proposal, accessing these smart contracts would contribute very little per-contract cost to the witness size, since these contracts would tend to be located nearby each other in the trie.

## What would this look like as a stateless Ethereum proposal?

Current proposals for binarizing the state tree stateless ethereum involve storing the balance, nonce, code, and storage for an account at certain [locations](https://ethresear.ch/t/binary-trie-format/7621/14) in the tree associated with the address of the account. What I would propose is to instead include *the address itself* as a value to be stored alongside these other pieces of data, and have the location of the account in the tree depend on the time the account was last changed.

- location + 0x00 for address
- location + 0x01 for balance
- location + 0x02 for nonce
- location + 0x03 + chunk_id for code
- location + 0x04 + storage_key for storage.

Whenever an account is touched in a block, this subtree is deleted from its location and reinserted at `new_location := current_block_height + index_within_block`

### How would state expiry work

Vitalik’s post on State size management identified “Refresh by touching” as a nice way to do state expiry. This proposal integrates this idea rather naturally: If we are expiring all data that has not been touched since a given block height, we just forget the left part of the tree consisting of nodes in locations below that corresponding to the block height.

This can also be seen as a compromise between the “one-tree approach” of having one tree, some of which is expired, vs the “two-tree approach” of having a second separate tree for the expired data. In this case the “second tree” is just the left part of the main tree. We sidestep the problem of tree rot, where expired parts of the tree prevent new accounts from being created, by creating all new accounts on the right side of the tree, irrespective of address.

## Drawbacks

There are a few drawbacks to this scheme, which I’ll cover here.

- The subtree delete and move operation is a complicated primitive to implement.
- To prevent account collisions, it would be necessary to ensure that new accounts can’t be made that have the same identification as old accounts. One could do something similar to the extended address scheme proposed here, but instead of appending the year to the account, you append the block number to the account.
- The proposal as I’ve stated it does not have storage slot level granularity but only contract level granularity. This would mean that if an old contract were resurrected it would only bring back the touched parts of the state, but if an contract were to stay alive in the state for a long time, it could accumulate storage indefinitely. This could be fixed by a separate inclusion of timestamps into the storage tree to expire parts of contract data that had not been recently touched.

## Thanks

I’d be happy to know what you all think of this, and whether there are any other big drawbacks I may have missed.

## Replies

**vbuterin** (2021-04-05):

How would you make a proof that an account does not yet exist in this scheme?

---

**pipermerriam** (2021-04-05):

Thank you for the write-up.  I think there’s some valuable concepts in here even if we don’t end up using all of it.

IIUC this scheme has the property of sort of constantly shuffling the most recently touched stuff to the “right” of the trie, meaning that as you scan from left to right, you are also scanning from least recently touched to most recently touched.  This property would be really nice as it would allow for low complexity rolling state expiry (aka, expiring state at every block rather than at epoch boundaries).

But I believe this comes with a significant downside, which is that you can’t know the `location` for a given account without processing a non-trivial amount of the history.  If this is accurate, it has significant negative implications on building out “lightweight” nodes, since they would not be able to know where in the trie to look for account or contract data without either doing this processing themselves (and thus violating the lightweight requirements) or depending on a “full” node to tell them where the data lives.

I’ll also note that the drawback you list about “subtree delete and move operation is complicated” seems very significant.  Taking the Tether ERC20 contract, which I believe is one of the contracts with massive storage size, we would be relocating a massive subtree at a very regular interval.  This seems like it would have significant performance implications, but it’s possible these can be worked around.

---

**BoltonBailey** (2021-04-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How would you make a proof that an account does not yet exist in this scheme?

I guess my answer is that I’m not sure there’s any good way to do this - As you’ve pointed out, if you have to be able to prove an account (in the sense of a particular public-key controlled account) does not exist, you will need access to an archival node anyway. So in this scheme, you simply have to guarantee that the IDs of new accounts are generated in a way that guarantees they don’t collide with previous one. To elaborate more on what I said regarding doing “something similar to the extended address scheme”, I guess I would say that public keys could be completely divorced from account numbers. Account numbers could actually just be sequentially given out - (Account #00001, Account #00002 …) and the public key associated with the account would be included in the account data.

This of course raises other problems, such as how do you send to a public key not registered on chain? One solution to this could be some standard for creating smart contracts that are controlled by a particular public key, along with functionality in archival nodes that allows you to query them, perhaps for a fee, for accounts you control (the UTXO model is creeping back in here). Perhaps some smart contracts have functionality that depends on proving that accounts don’t exist - I’m not sure what to do if this is the case.

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> But I believe this comes with a significant downside, which is that you can’t know the location for a given account without processing a non-trivial amount of the history.

This is a good point. In theory, a wallet could keep track of the `location` for accounts it is interested in, but whenever it wanted to interact with a new account, or even when the wallet itself was backed up from seed phrase, it would need to access some kind of lookup table in a full node to locate the accounts. This is similar to how a node might need to keep track of the changing upper portion of its account Merkle branch in some versions of statelessness.

---

**vbuterin** (2021-04-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/boltonbailey/48/5188_2.png) BoltonBailey:

> As you’ve pointed out, if you have to be able to prove an account (in the sense of a particular public-key controlled account) does not exist, you will need access to an archival node anyway

Right, but to *verify* that proof in the scheme I proposed you don’t need an archival node. Whereas in this scheme you would.

---

**BoltonBailey** (2021-04-05):

Yep, it’s true that you can verify a proof that an account does not exist using your scheme without an archival node. But it’s actually *not* possible to do so in this scheme, even with an archival node. Even if an archival node had the whole tree, it would have to prove that the account did not exist at any location of the tree (since accounts are not tied to locations) which would be too expensive.

What a non-archival node can do in this scheme is verify the Merkle branch provided by an archival node that a particular account exists at a particular expired location, just as it would for a non-expired account.

Going back to the example of Alice who is stranded on an island from epochs 9 through 13, to resurrect her account, Alice no longer has to provide 3 archival-node-supplied proofs of non-inclusion of her account in epochs 9, 10 and 11. She instead provides a single archival-node-supplied proof of her account in its location in epoch 8, after which the account is moved to the right side of the trie, with all the other accounts touched in epoch 13.

---

**vbuterin** (2021-04-06):

> Even if an archival node had the whole tree, it would have to prove that the account did not exist at any location of the tree (since accounts are not tied to locations) which would be too expensive.

This is actually not a problem; the archival node could keep an extra client-side (non-merklized) index.

---

**BoltonBailey** (2021-04-06):

An archival node client-side non-merklized index would certainly be helpful for the archival node determining if an account with a particular key had ever been made and locating it in the expired portion of the tree/proving its existence if it had. However, I don’t think it would help with producing a proof of nonexistence of a particular key that would be verifiable by a stateless node. This is why I try to redefine account numbers in a way that includes the block number in which they are created, to make it impossible to create conflicting accounts and avoid the need for these nonexistence proofs.

---

**BoltonBailey** (2021-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> we would be relocating a massive subtree at a very regular interval.

Indeed, if the cost of the subtree delete-and-move operation had even linear dependence on the size of the subtree being moved, I think this entire proposal would be infeasible. Making this operation sublinear in the size of the subtree requires us to be very careful about the structure of the trie. Various potential structures were discussed in [this thread](https://ethresear.ch/t/binary-trie-format/7621/) but I’m not sure any work for this purpose - any information about the trie index in leaf nodes will not work, since then it will have to be changed when the subtree is moved.

A binary trie structure that would permit an \tilde{O}(1) subtree delete-and-move operation would be

```plaintext
tree_depth

left_child_hash

right_child_hash

extension_bits_to_left_child

extension_bits_to_right_child

```

Unlike other proposals, the `prefix` of the node (that is, the bit string which is the common prefix of all leaf indices of the node) is not present here. This allows the subtree nodes to be agnostic about their location in the tree so that they can be moved without touching them in the database.

