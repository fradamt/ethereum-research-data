---
source: ethresearch
topic_id: 3615
title: Vitalik's scaling without SNARKs at all
author: kladkogex
date: "2018-09-30"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/vitaliks-scaling-without-snarks-at-all/3615
views: 2912
likes: 6
posts_count: 15
---

# Vitalik's scaling without SNARKs at all

[@vbuterin](/u/vbuterin) introduced a scaling scheme that can be used to scale transactions



    ![](https://ethresear.ch/user_avatar/ethresear.ch/lebed2045/48/2342_2.png)
    [On-chain scaling to potentially ~500 tx/sec through mass tx validation](https://ethresear.ch/t/on-chain-scaling-to-potentially-500-tx-sec-through-mass-tx-validation/3477/69) [Applications](/c/applications/18)



> Hey, guys. Is anyone has already implemented this? we wanted to take it as a hackathon tasks for  ETHSanFrancisco.

Here is  an alternative implementation that does not use verifiable computation (SNARKS/STARKS).   It may work a little slower than Vitalik’s proposal, but should anyway deliver 10x performance benefit or may be more.

Here is a sketch how it works:

1. Every user deposits money to a smart contract and gets a unique user ID (say 4 bytes).
2. A Merkle tree of all account balances is kept.
3. Each transaction then becomes a  12 byte sequence (source, destination, 4 byte amount)
4. A user broadcasts a transaction to all miners.
5. Any miner can concatenate a set of transactions and send the concatenated list back to the included users.
6. The miner than waits for time T=5 sec and the users respond with BLS/Boldyreva subgroup signature shares on the concatenated list
7. The miner forms BLS subroup signature of the concatenated list for those users that responded. Unsigned transactions are kept in the list and ignored.
8. The miner includes the concatenated list in the block as well as the BLS subgroup signature.
9. The miner also recalculates the new Merkle root and includes it in the mined block.
10. Once the block is mined, each non-mining node that receives it, verifies the new Merkle root as a part of the verification procedure.

Since the transaction size is only 12 bytes one will be able to include 20 times more transactions in the block that the current situation.

The downside of this proposal is that it requires some Layer 1 modifications. The upside is that no zkSNARKS are needed.

Note that you could make it even faster some users, by auctioning off short (one byte) addresses.  A transaction between two short addresses with one byte amount would be yet 4 times faster.

## Replies

**vbuterin** (2018-09-30):

I think you’re just describing replacing ECDSA sigs with aggregable BLS sigs. The problem is that either the state has to be kept around or the Merkle branches have to be passed around, making the scheme nonviable at the 500 tx/sec level.

What *would* work is a scheme where a relayer can submit a list of (from, to, nonce, value) tuples along with a BLS aggregate sig and a Merkle root, and anyone can challenge their submission within the next two weeks, and if left unchallenged for the two week timespan it becomes accepted.

---

**kladkogex** (2018-09-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think you’re just describing replacing ECDSA sigs with aggregable BLS sigs. The problem is that either the state has to be kept around or the Merkle branches have to be passed around, making the scheme nonviable at the 500 tx/sec level.

What is the argument that the state cant be kept around ?)  Because of computational or storage requirements? I am not sure why one cant have a Merkle tree that is updated 500 times a second and stored on each node …

If a simple Merkle tree is not efficient one can come up with a more effective crypto accumulator or have a more effective storage checkpointing scheme - it seems easier than addressing zkSNARK performance problems.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> he entire goal of my scaling scheme was to make it so that only users of the sub-system need to care about the Merkle tree updates for the sub-system, so you can have many sub-systems operating in parallel and no one has to keep track of the whole data.

Vitalik - I understand. Just to make it clear - since in the scheme suggested the transactions need to be placed into blocks anyway, the total for all people will anyway have to be about 500 transactions per second, since currently ETH has roughly 20 TPS  at 200Bytes per block, and in your case the transactions in the block will be roughly 20 times shorter.

So the 500 tps bottleneck for the total number of transactions comes from the number of the transactions in the block, and seems to be independent on details.

Then you could either use SNARKS as you suggested, or somehow figure out a way to update the Merkle tree faster, but 500TPS seems to stay the same.

I hope I understood the scheme correctly ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**vbuterin** (2018-09-30):

> What is the argument that the state cant be kept around ?) Because of computational or storage requirements?

Yes, particularly computational requirements of having to update the merkle tree. The entire goal of my scaling scheme was to make it so that only users of the sub-system need to care about the Merkle tree updates for the sub-system, so you can have many sub-systems operating in parallel and no one has to keep track of the whole data.

---

**denett** (2018-09-30):

Is there is reason you are using a multi step signing scheme instead of just aggregating the signatures directly?

It is not my field of expertise, but I found [this paper](https://link.springer.com/chapter/10.1007%2F3-540-39200-9_26) that describes a method to aggregate n signatures on n distinct messages from n distinct users.

---

**vbuterin** (2018-09-30):

The multi-step-signed signatures are cheaper to verify.

---

**denett** (2018-09-30):

I see, for simple aggregation, it takes N verification’s for N transactions and with the multi step variant, one verification is sufficient, because the signatures are all on the same message.

This would be less of a problem if we take the verification off-chain and only do the challenging process on the chain.

---

**vbuterin** (2018-10-02):

Agree. With my proposal above, I’d say BLS aggregate signatures are fine, as the sigs would only *actually* be verified on chain in the event of a challenge event which would hopefully be quite rare.

---

**gluk64** (2018-10-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I’d say BLS aggregate signatures are fine, as the sigs would only actually be verified on chain in the event of a challenge event which would hopefully be quite rare.

The problem with BLS is that if some submitters won’t sign the root, their transactions must still be included in the concatenated submission. To cover gas costs, [@kladkogex](/u/kladkogex) suggested to demand small security deposit from users, which renders them vulnerable to griefing by the miner.

If signatures are only verified on chain in case of challenge, then n-messages signature aggregation is still efficient: the challenger only needs to demonstrate one wrong signature.

---

**kladkogex** (2018-10-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> To cover gas costs, @kladkogex suggested to demand small security deposit from users, which renders them vulnerable to griefing by the miner.

Deposit ?))) That was not me who required that :))

I think if a guy  did not sign, you just need to include the hash of her transaction which is 256 bit.  You do not need to include the transaction itself since it wont be processed. So this should not cause a lot of troubl imho

---

**gluk64** (2018-10-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Deposit ?))) That was not me who required that :))

Sorry, I misinterpreted your point no 1.

> I think if a guy did not sign, you just need to include the hash of her transaction which is 256 bit. You do not need to include the transaction itself since it wont be processed.

Right, 256 bit = 2176 gas. A block with 500 unsigned transactions will cost 1M gas overhead at no cost for the attacker, that’s quite a strong griefing attack vector.

---

**denett** (2018-10-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> If signatures are only verified on chain in case of challenge, then n-messages signature aggregation is still efficient: the challenger only needs to demonstrate one wrong signature.

Is there a way to verify a single message-signature combination from an aggregated signature? I thought that you could only verify the aggregate as a whole, this taking O(n) time. Although it looks like it is faster than verifying all individual original signatures.

---

**gluk64** (2018-10-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> I thought that you could only verify the aggregate as a whole, this taking O(n) time.

This is correct. However, my understanding is that you can challenge a specific tx signature: ask the miner to provide a product of signatures of other transactions, such that multiplication of the challenged signature and this product yields the aggregate signature. But you need to be sure that this particular signature is not included in the aggregated subgroup – if the miner included signatures of 67 out of 100 tx in aggregation, it will be computationally difficult to find out which ones.

If you are the owner of an account falsely included in tx though, targetted challenging will work. You don’t even need to verify the aggregate sig.

---

**gluk64** (2018-10-03):

In the worst case the challenge can be spread accross multiple blocks.

---

**denett** (2018-10-03):

Yes, if you allow a multiple step TrueBit like verification it is cheaper, but this can holdup the chain for a long time. Both the relayer and the challenger need a fair amount of time to respond.

Maybe the transactions should be grouped in smaller batches such that a batch can be validated on chain in a single block. The incorrect transactions can be rolled back immediately and other relayers can continue the chain.

