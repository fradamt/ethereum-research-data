---
source: ethresearch
topic_id: 1298
title: "Plasma Cash: Plasma with much less per-user data checking"
author: vbuterin
date: "2018-03-04"
category: Layer 2 > Plasma
tags: [new-extension]
url: https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298
views: 108383
likes: 72
posts_count: 116
---

# Plasma Cash: Plasma with much less per-user data checking

[2018.03.10: updated with exit procedure]

Special thanks to Karl Floersch for discussion and coming up with much of this, as well as [@danrobinson](/u/danrobinson)’s [earlier posts](https://ethresear.ch/t/cryptoeconomic-probabilistic-tumbler/1103) that expressed similar ideas.

Basically, we can design a version of Plasma with the following modifications:

1. Every single deposit corresponds to a unique coin ID; tokens are indivisible and cannot be merged.
2. Instead of storing transactions in a binary Merkle tree in order of txindex, we require them to be stored in either a sparse simple Merkle tree or a patricia tree, with the index being the ID of the coin that is spent.

Note that this now allows a user to have a somewhat compact proof that their coin is valid: all the transactions since the time the coin was deposited that represent that coin’s history, plus a proof of non-inclusion for every block that does not contain a transaction spending the coin, to verify that the coin was not double spent. With n coins and t blocks, this proof has size t * log(n). If a user transfers a coin to another user, he could simply pass along the entire proof to that user.

Hence, a Plasma operator could simply maintain connections with each user, and every time they create a block they would publish to them only the proofs, not any data related to coins that they do not own. It’s clearly the case that any data that is not part of these proofs could not be used to fraudulently exit or double-spend the user’s coin, so the user is safe. Because coins are non-fungible, successfully defrauding other users cannot allow the Plasma contract to turn into a fractional reserve, as is possible in minimal viable plasma.

The Plasma chain operator could be sharded, so there is virtually no limit to the system’s scalability from the point of view of either the chain operator or the users, though the limitation that if Plasma-like systems (and channel systems) start processing a very high transaction load, mass challenge attacks may overflow the blockchain and prevent some users from exiting or responding to challenges still remain. This kind of setup seems ideal for very-high-throughput but low or medium-state applications, like micropayments and exchanges.

Additionally, we can remove the need for confirmations. We do this by having the following exit procedure:

1. Anyone can exit their coin by providing the last two transactions in the coin’s ownership history (ie. the coin they are exiting C and its parent P( C )).
2. An exit can be challenged in three ways: (i) provide a proof of a transaction spending C, (ii) provide a proof of a transaction spending P( C ) that appears before C, (iii) provide a transaction C* in the coin’s history before P( C )
3. A challenge of type (i) and (ii) blocks the exit immediately. A challenge of type (iii) can be responded to by providing the direct child of C*, which must be either equal to or before P( C )

This relies on honest users maintaining the key property that they never spend a coin until they have fully authenticated the entire history up to that coin. It could be the case that a Plasma chain starts including unavailable or invalid data while a transaction is in flight, in which case double spends or invalid spends could appear between P( C ) and C; the slightly more complicated exit mechanism takes this into account.

## Replies

**vbuterin** (2018-03-04):

Addenda:

1. You don’t actually have to pass around t * log(n) data if you can instead pass on a ZK-SNARK of data. This could be done with recursive snarks to keep the total data passed around O(1) size.
2. Confirmations could easily be removed from the scheme. The solution is effectively a design where there is one level of interactive history verification, and spending a coin effectively takes on the role of a confirmation. That is, withdrawing requires a proof of a coin C, and if someone challenges with an earlier coin, then you can provide the parent P(C ); they would then need to prove a coin spending P(C ) that comes earlier than C to challenge.

---

**danrobinson** (2018-03-05):

This is great—and definitely improves on the trade-offs in a Plasma context, relative to my previous suggestions.

Few questions:

1. Perhaps you could cut down on the size of the non-existence proofs by putting a Bloom filter of the spent coins in the Plasma block header. Everyone could receive and cache the Bloom filters, and you’d only need a proof for blocks for which there’s a false positive for your coin. I’m not that familiar with probabilistic data structures but I wonder if there’s a way to parametrize it so that the shared data is pretty small but, absent misbehavior by the Plasma chain operator, false positives will happen so rarely (say 1 in a billion transactions) that withdrawal would be a sufficient remedy.
2. I’m not sure it would work to use a ZK-snark for the non-existence proofs, unless the parent chain is willing to accept ZK-snarks for the exit transactions. Otherwise, you don’t have enough information to respond to a challenger, right?

---

**vbuterin** (2018-03-05):

> I’m not sure it would work to use a ZK-snark for the non-existence proofs, unless the parent chain is willing to accept ZK-snarks for the exit transactions. Otherwise, you don’t have enough information to respond to a challenger, right?

Now that I think about it, you are right. In order to be able to respond to type (iii) challenges you have the proofs for every transfer in the coin’s actual history. If there are t blocks and h transfers (history length), then this already reduces required data size from 32 * t * log(n) to 32 * h * log(n) + 288. What we can also do is make a recursive SNARK that proves the list of block numbers for which a proof exists; this would bring it down to h * \frac{log(t)}{8} + 288 bytes (\frac{log(t)}{8} because we need log(t) bits to represent each block number, and a byte is 8 bits). To see how small this is, consider a Plasma chain with one block per Ethereum block that lasts for one year, with a history 500 transfers long; the chain would have 2.2 million blocks, so the data size would be 500 * 21 bits + 288 bytes = 1600 bytes.

---

**danrobinson** (2018-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> Perhaps you could cut down on the size of the non-existence proofs by putting a Bloom filter of the spent coins in the Plasma block header. Everyone could receive and cache the Bloom filters, and you’d only need a proof for blocks for which there’s a false positive for your coin. I’m not that familiar with probabilistic data structures but I wonder if there’s a way to parametrize it so that the shared data is pretty small but, absent misbehavior by the Plasma chain operator, false positives will happen so rarely (say 1 in a billion transactions) that withdrawal would be a sufficient remedy.

According to this [Bloom filter calculator](https://hur.st/bloomfilter?n=200&p=1.0E-9), a 1 KB Bloom filter with a maximum of 200 items has a false positive probability of 1 in 1 billion. If my math is right, that means if you have one Plasma block per Ethereum block, that’s < 3 GB of block header storage per year, and you’d expect to see a false positive on one of your coins about every 380 years (in which case you’d be able to respond by withdrawing anyway, or perhaps by revealing the transactions that generated the false positive). So perhaps you could cut out the Patricia tree entirely, and just store transactions in a normal Merkle tree, with the Bloom filter serving as the only proof of non-existence. (EDIT: nope, you would still need to store the transactions in a sparse Merkle tree or Patricia tree, so you could prove that your transaction is the *only* one spending that coin in that block. It’s still a very small proof, though.) The main benefit of this scheme is that most of the data would be common to all users and coins, rather than having coin-specific proofs that need to be passed around with every transaction.

If you use a cryptographic hash function for the filter and coin IDs are generated using entropy from the chain operator, I think that weakens anyone else’s ability to grind out a false positive for your coin, although maybe you still need some additional hardening (like using a per-block salt for the hashes).

This does give up a little privacy (anyone, not just the chain operator, can tell when a coin is spent), although maybe there’s a way to preserve that too.

---

**kfichter** (2018-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> According to this Bloom filter calculator, a 1 KB Bloom filter with a maximum of 200 items has a false positive probability of 1 in 1 billion. If my math is right, that means if you have one Plasma block per Ethereum block, that’s  plus a proof of non-inclusion for every block that does not contain a transaction spending the coin, to verify that the coin was not double spent

What if a block contains two transactions that spend the same coin?

---

**vbuterin** (2018-03-06):

> What if a block contains two transactions that spend the same coin?

In my design, not possible. The transaction’s position in the Merkle tree must be the ID of the coin, so you cannot have two transactions in one block that spend the same coin.

---

**kfichter** (2018-03-10):

Would coin ID => denomination be stored as a mapping on the root chain? That would limit the minimum viable deposit. You might be able to improve ux/decrease gas cost with a “change machine,” i.e. insert `n` root chain tokens/ETH and receive `m` coin IDs each with value `n/m`.

Also, how are transactions actually validated? Something like this?

1. Validate that each transaction in the history I was given is actually included in its corresponding block with a Merkle membership proof and then
2. Validate each proof of non-inclusion

I’m also interested in understanding how the non-inclusion proofs are generated.

---

**vbuterin** (2018-03-10):

> Would coin ID => denomination be stored as a mapping on the root chain?

Yes.

> I’m also interested in understanding how the non-inclusion proofs are generated.

A non-inclusion proof is basically a proof that there exists an object at the given position in the Merkle tree, and this object is empty data.

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Also, how are transactions actually validated? Something like this?
>
>
> Validate that each transaction in the history I was given is actually included in its corresponding block with a Merkle membership proof and then
> Validate each proof of non-inclusion

Basically yes.

---

**ldct** (2018-03-10):

Could the coin ID => denomination mapping be deterministic, e.g. create a complete binary tree of height 31, label each node with a 32-bit id and the denomination of a coin is 2^h where h is the height of its id in the tree. Users can only deposit in powers of two, there is an upper bound on the total amount that the chain can hold, and are allowed to split coins in half and merge them. A constraint is maintained that along each root-to-leaf path only one coin can be issued.

---

**kfichter** (2018-03-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> deposit in powers of two

I don’t see why you couldn’t also just make it a non-binary tree. Say root node is worth some large value, second layer splits the value into many usable chunks (`n` 100 ETH coins), then each broken down into more (five 20 ETH coins), etc. etc.

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> merge them

How would this work? Would the user have to own the specific two consecutive coins in order to merge a layer up?

---

**kfichter** (2018-03-10):

David Knott and I discussed a “merge/split” transaction where a user could point to specific coin IDs they own (by referencing outputs) and reshape them into new coin IDs that have different denominations but the same total value. This maintains the property that only specific users can be grieved (owners of those coin IDs). The transaction would require a challenge period much like the Plasma MVP exit transaction. A merge/split is invalidated under the same conditions as

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A challenge of type (i) and (ii) blocks the exit immediately. A challenge of type (iii) can be responded to by providing the direct child of C*, which must be either equal to or before P( C )

This construction would allow users to modify their coins without having to exit and deposit again.

I also started thinking about the idea of “change providers” - users who carry a large amount of change to assist in transactions where one or both parties can’t make correct change. To illustrate:

Alice wants to send 7 ETH to Bob, but doesn’t have a 7 ETH coin. Alice has a 10 ETH coin and some smaller coins. Bob does not have a 3 ETH coin to send in return. Carol is a change provider who happens to have both a 7 ETH coin and a 3 ETH coin. Alice and Carol construct a transaction in which the following ownership transfers occur:

1. Alice sends a 10 ETH coin to Carol
2. Carol sends a 7 ETH coin to Bob
3. Carol sends a 3 ETH coin to Alice
4. Alice sends some small ETH coin to Carol as a fee

This last fee component is obviously the complicating factor, as it requires Alice to have some specific small ETH coin on hand to make the transaction. In the absence of a change provider, Alice could use the merge/split transaction mentioned above to convert her 10 ETH coin into 7 ETH and 3 ETH coins to transact with Bob. However, this is significantly slower due to the challenge period.

---

**MaxC** (2018-03-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Now that I think about it, you are right. In order to be able to respond to type (iii) challenges you have the proofs for every transfer in the coin’s actual history. If there are

Hey Dan/Vitalik, would you mind explaining why ZK snarks wouldn’t work to prove ownership of a coin non-interactively?

From what I understand, exit transactions for a coin would be recorded on the parent block-chain, and you would need to prove no exit transactions had been made. So would that not just increase the number of the proofs by a factor of d, the depth of the plasma tree for a coin.

---

**danrobinson** (2018-03-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> Hey Dan/Vitalik, would you mind explaining why ZK snarks wouldn’t work to prove ownership of a coin non-interactively?

I’m assuming you can’t use any ZK-snarks on the parent chain (which would require trusted setup, and for everyone to share your security assumptions, etc); you can only use ZK-snarks for user-to-user proofs. So the receiving user needs enough data to be able to respond to any possible type (iii) challenge, for when they attempt to exit.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> From what I understand, exit transactions for a coin would be recorded on the parent block-chain, and you would need to prove no exit transactions had been made. So would that not just increase the number of the proofs by a factor of d, the depth of the plasma tree for a coin.

That’s not the hard part of the proof (the Ethereum state root suffices to prove that); you have to prove (directly) that you own the coin at time T, and (cryptoeconomically) that nobody spent that coin on the plasma chain after time T, and that there is a valid history of that output tracing back to the deposit, with no double-spends. That last part is what you need the additional data for; otherwise you can’t respond to a type (iii) challenge (even if you know, through a ZK-snark, that your coin does have a valid history).

---

**vbuterin** (2018-03-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> Hey Dan/Vitalik, would you mind explaining why ZK snarks wouldn’t work to prove ownership of a coin non-interactively?

They can prove integrity of a history, but a ZK snark does NOT give you the information that you need to fend of challenges in the challenge-response game that tries to prove that there are no *earlier* correct histories.

---

**MaxC** (2018-03-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> That’s not the hard part of the proof (the Ethereum state root suffices to prove that); you have to prove (directly) that you own the coin at time T, and (cryptoeconomically) that nobody spent that coin on the plasma chain after time T, and that there is a valid history of that output tracing back to the deposit, with no double-spends. That last part is what you need the additional data for; otherwise you can’t respond to a type (iii) challenge (even if you know, through a ZK-snark, that your coin does have a valid history).

Ok thanks. It seems to me, as long as you share information about which coins are being spent every epoch, you can have ZK proofs for non-existence. However, you don’t need to share all the information relating to that coin.

Suppose leaf nodes of the transaction tree were two tiered,  with data at the bottom relating to a transaction , and a hash of the data at the top.

Operators could share general data about the whole tree excluding the bottom tier of leaf nodes to the network.

To construct a non-existence proof, you can:

(1) show that your coin is not included in the merkle tree

(2) Suppose wlg. that you have a coin, and someone has just now fraudulently double spent it. You can prove that this person spending the coin could not have been you, the person with (up until now) a valid proof of ownership. We do this by including an extra field in the leaves.

- In the bottom tier of the leaf we also include a signature of the hash of the transaction.
- We now have two hashes on the top tier, one for the transaction and one for your signature of the hash of the transaction. A non-existence proof is a proof that your signature of the transaction hash could not hash to the value stored and so the transaction is invalid.

I think that is sufficient as a construction to prove that you are the rightful owner of a coin at time t, if indeed you are.

---

**vbuterin** (2018-03-11):

> To construct a non-existence proof, you can:
> (1) show that your coin is not included in the merkle tree

Yes, but what if A sends a transaction to B, while that transaction is inflight the Plasma chain becomes byzantine, and so the transaction gets included after some unavailable Plasma blocks? Then B does not have the data to prove that the transaction is not a double-spend.

---

**MaxC** (2018-03-11):

A few thoughts, please correct me if I am wrong:

(1) Transactions could contain a block number so it would be impossible to put a transaction in a later block, and generate a proof for it.

(2) If A doesn’t receive the merkle information from the byzantine chain, she could exit before the new block is finalised in the parent block.

(3) We assume it is A’s responsibility to pass on the merkle information to B.

I guess such a scheme might then require proofs of non-existence for withdrawals in the parent chain.

---

**vbuterin** (2018-03-11):

> Transactions could contain a block number so it would be impossible to put a transaction in a later block, and generate a proof for it.

So a transaction generated after block N would have N+1 included in them and so could only be included in block N+1? That is brilliant; it actually does remove the need to worry about inflight transactions.

---

**kfichter** (2018-03-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So a transaction generated after block N would have N+1 included in them and so could only be included in block N+1?

How is N+1 counted? Would have to ignore deposit/exit blocks.

Also, what if the tx is included in block N+1, N+1 is published to the root chain but withheld?

---

**MaxC** (2018-03-11):

You could just have the parent chain broadcast the hash of the merkle  tree and wait a period of time, allowing others to withdraw, before it commits.


*(95 more replies not shown)*
