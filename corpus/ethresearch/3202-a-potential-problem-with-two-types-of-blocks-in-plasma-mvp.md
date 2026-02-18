---
source: ethresearch
topic_id: 3202
title: A potential problem with two "types" of blocks in Plasma MVP?
author: MihailoBjelic
date: "2018-09-03"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/a-potential-problem-with-two-types-of-blocks-in-plasma-mvp/3202
views: 3662
likes: 8
posts_count: 13
---

# A potential problem with two "types" of blocks in Plasma MVP?

From the original Plasma MVP post:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[Minimal Viable Plasma](https://ethresear.ch/t/minimal-viable-plasma/426/1)

> A Plasma block can be created in one of two ways. First, the operator of the Plasma chain can create blocks. Second, anyone can deposit any quantity of ETH into the chain, and when they do so the contract adds to the chain a block that contains exactly one transaction, creating a new UTXO with denomination equal to the amount that they deposit.

Can anyone explain why we have these two separate “types” of blocks (“regular” blocks with Plasma chain transactions and blocks with a single deposit transaction)? Why don’t we simply include deposit transactions as part of the next “regular” Plasma block?

Also, I wonder how can a smart contract enforce the creation of these deposit blocks on a Plasma chain (how can a contract have control over an operator i.e. the blocks it creates)? In case I’m not being clear enough, I’m referring to this:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[Minimal Viable Plasma](https://ethresear.ch/t/minimal-viable-plasma/426/1)

> anyone can deposit any quantity of ETH into the chain, and when they do so the contract adds to the chain a block that contains exactly one transaction

UPDATE: After [@ldct](/u/ldct) explained how this works on a technical level, I’ve described a potential problem with this design in the [comment bellow](https://ethresear.ch/t/why-do-we-have-two-types-of-blocks-in-plasma-mvp/3202/3), and I look forward to any comments. Thanks.

## Replies

**ldct** (2018-09-03):

As I interpret the spec, the deposit blocks are not created by the operator but by the contract (i.e. when the user calls a certain function on the plasma contract, the contract itself appends a block to the list of plasma blocks)

---

**MihailoBjelic** (2018-09-03):

Oh, that would probably be the case. Then the operator will have to update her version of the chain so she can continue creating blocks on top of that block created by the root contract, otherwise the root contract will not accept them.

Let’s assume this situation:

1. A user deposits some ETH to a Plasma chain root contract
2. The root contract submits a main chain transaction committing a new Plasma block with the deposit
3. At the same time, the Plasma operator submits a main chain transaction committing a new Plasma block with regular Plasma chain transactions (she’s not aware of the root contract’s transaction at this moment)
4. One of the two main chain transactions gets rejected by miners (if I’m not mistaken?)

This could happen quite often and could be quite an annoyance. For a busy Plasma chain with a lot of users and activity (e.g. a popular trading platform), we can even imagine it happening in EVERY main chain block for a long period of time (a lot of traders are constantly trying to deposit and, at the same time, a lot of traders are trading on the Plasma chain, so both the root contract and the operator are constantly submitting transactions trying to to commit blocks). What would happen then? I guess the users will simply start leaving the platform and going back to centralized alternatives… ![:crying_cat_face:](https://ethresear.ch/images/emoji/facebook_messenger/crying_cat_face.png?v=9)

Also, I believe this will slow down the whole Plasma chain. Since we have uncle blocks/probabilistic finality, both parties (the root contract and the operator) will always have to wait a number of blocks after other party submits a transaction, so they can be sure that it’s included in the (longest) main chain and that they can safely append their future blocks to it…

Back to my original question, I still don’t see the advantage/purpose of creating blocks this way… ![:no_mouth:](https://ethresear.ch/images/emoji/facebook_messenger/no_mouth.png?v=9)

---

**ldct** (2018-09-04):

I don’t see why (4) is necessary. Assume for concreteness that deposit blocks create a single-entry merkle tree containing a deposit plasma-transaction. As before, a plasma block created by the operator commits to a merkle tree containing multiple plasma-transactions (none of which are deposit plasma-transactions). Then an ethereum miner can reorder deposit ethereum-transactions from users as well as ethereum-transactions from the operator.

EDIT: the only case where reordering is not possible is if the miner’s ethereum-transaction contains a plasma-transaction that spends a TXO created by a user’s deposit, but we don’t need to worry about it here

---

**MihailoBjelic** (2018-09-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> single-entry SMT

I’m sorry, I don’t know what this is… ![:see_no_evil:](https://ethresear.ch/images/emoji/facebook_messenger/see_no_evil.png?v=12)

---

**ldct** (2018-09-05):

oops, sparse merkle tree

---

**MihailoBjelic** (2018-09-05):

Oh, sure. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I’m a bit confused now, why would SMTs be used for Plasma MVP transaction trees, what is the advantage over simple Bitcoin-like Merkle trees?

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> ethereum miner can reorder deposit ethereum-transactions from users as well as ethereum-transactions from the operator

Can you explain this reordering, please? I think the core of the problem here is that both the root contract and the operator are trying (unaware of each other’s activity) to submit Plasma blocks that point to the same previous Plasma block (if both blocks end up being accepted, the Plasma chain will fork there), and I don’t understand what can any sort of reordering do to solve this?

---

**ldct** (2018-09-05):

Ah my fault again, the original post should just say “Merkle Trees”.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I think the core of the problem here is that both the root contract and the operator are trying (unaware of each other’s activity) to submit Plasma blocks that point to the same previous Plasma block

I think this is underspecified, but I would implement the ordering of plasma blocks just as a list of `bytes32`s on the plasma contract, instead of the plasma blocks explicitly pointing to a previous one. i.e.

```auto
storage bytes32 plasmaBlockCommitments;
constant address operatorAddress;

function deposit() public payable () {
  bytes32 depositCommitment = // compute root of merkle tree of size 1 with a single deposit txn
  plasmaBlockCommitments.append(depositCommitment);
}

function operatorExtendPlasmaBlock(bytes32 newPlasmaBlockCommitment) {
  require(msg.sender == operatorAddress);
  plasmaBlockCommitments.append(newPlasmaBlockCommitment);
}
```

This way most ethereum-transactions that call  `deposit` and `operatorExtendPlasmaBlock`  can be reordered

---

**MihailoBjelic** (2018-09-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> Ah my fault again, the original post should just say “Merkle Trees”.

No problem. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> I would implement the ordering of plasma blocks just as a list of bytes32 s on the plasma contract, instead of the plasma blocks explicitly pointing to a previous one

That’s interesting. Have you maybe checked the code of other implementations, do they do it the same way?

---

**kfichter** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Why don’t we simply include deposit transactions as part of the next “regular” Plasma block?

Basically because this is a super simple way to do deposits without adding any extra mechanisms on top of Plasma. If you make deposits into a sort of request for a UTXO to be created in the next deposit block, then the operator can try to cheat by not including the deposit (or including it after an invalid transaction).

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Also, I wonder how can a smart contract enforce the creation of these deposit blocks on a Plasma chain (how can a contract have control over an operator i.e. the blocks it creates)?

Yeah it just creates/encodes a new transaction on-chain, puts it in a Merkle tree by itself, and inserts the new root like any other block.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> One of the two main chain transactions gets rejected by miners (if I’m not mistaken?)

The blocks don’t necessarily need to specify a block number - if the operator’s transaction gets included first then it’ll be block `X` and the deposit will be block `X+1`, and vice versa. I definitely wouldn’t include a pointer to the previous block (it’s not necessary).

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Since we have uncle blocks/probabilistic finality, both parties (the root contract and the operator) will always have to wait a number of blocks after other party submits a transaction, so they can be sure that it’s included in the (longest) main chain and that they can safely append their future blocks to it…

I think the real problem that can be highlighted here is that a user needs to wait for root chain “finality” before their Plasma transaction is considered final. Likewise, an operator should not allow spends of a deposit until the deposit is probabilistically final on the root chain (more below).

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Can you explain this reordering, please?

Scenario where this would be relevant:

1. User A makes a deposit in Ethereum block X, generating Plasma block Y with UTXO 1.
2. User A spends UTXO 1 in Plasma block Y+1, which is included in Ethereum block X+1.
3. A 2-block reorg occurs on Ethereum. The transaction that submitted Y+1 is now included before the deposit transaction.
4. Y+1 is now invalid because it spends a UTXO that doesn’t exist.

As stated above, the resolution here is waiting for a deposit to be under sufficiently many Ethereum blocks before allowing it to be spent.

Hope that helped. Happy to answer other questions if you have them!

---

**MihailoBjelic** (2018-09-10):

Thanks for the detailed reply [@kfichter](/u/kfichter), you’ve cleared up quite a few things for me! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**qbig** (2018-11-29):

Could you elaborate on “contract itself appends a block to the list of plasma blocks”? I was assuming by contract we are referring to a normal contract on the Ethereum mainnet. How could it mute a state outside Ethereum?

I was assuming Operator of Plasma chain would listen on events on the Mainchain and update side chain accordingly.

---

**ldct** (2018-11-29):

Yes - I meant it appends to the list of plasma block headers (which is stored in the plasma contract)

