---
source: ethresearch
topic_id: 4790
title: The optimal SNARK-less on-chain scaling solution
author: kladkogex
date: "2019-01-10"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/the-optimal-snark-less-on-chain-scaling-solution/4790
views: 5006
likes: 7
posts_count: 14
---

# The optimal SNARK-less on-chain scaling solution

Since people are actively discussing I would like to propose a simple and better solution which does not use  SNARKs. SNARKs are in my view grossly overhyped at the moment.

The solution  goes as follows:

1. Users submit transactions to the operator, using user indexes instead of user public keys to save space.
2. The operator combines signatures in a block B.
3. The operator submits the block back to every user from this block.
4. The user creates a BLS signature share and sends it back to the operator.
5. The operator waits a while, combines signatures into a multi-signature and
sends B, the multi-signature, and the list of users that signed to the smart contract.
6. The smart contract verifies the signature and saves the block into Ethereum log storage.
7. To enter you simply deposit money, which will post a corresponding log entry. You can exit by passing your coin to someone who wants to enter.
8. To find out how much money anyone has, just follow the on-chain history from the beginning of time.
9. If someone tries to withdraw more than this person has, simply assume that the transaction size is the maximum of what the person has and the transaction value.

Note that this is totally on-chain and no exit required at all.  Also there could be any number of operators, concurrently posting.

If you, say, have a billion of indices, (32 byte indices) you can have the price of the index go to infinity Bancor style, and if you release an index, you get your money back.

## Replies

**barryWhiteHat** (2019-01-10):

Nice idea, would be nice to hear some numbers on a few things

Are the users signing different data or the same? Its dififcult to aggragate BLS signtures when the data is different.

How many signatures can you aggragate in BLS signtures? How difficult is this?

Also i think there is some dos attacks in step 4 when users refuse to join a block forcing everyone else to recalulate their group signtures, or maybe i am missing something.

---

**JustinDrake** (2019-01-11):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The smart contract verifies the signature

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Its dififcult to aggragate BLS signtures when the data is different.

That’s a key weakness. The verification costs of an aggregate signature are at least one pairing per distinct message, which equates to one pairing per transaction. Each pairing costs 80,000 gas so the current gas limit (8,000,000) would allow for less than 100 transactions per block (~6 transactions per second, worse than standard 21,000 gas transactions).

---

**denett** (2019-01-12):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> To enter you simply deposit money, which will post a corresponding log entry. You can exit by passing your coin to someone who wants to enter.

So the coins can never leave the contract? This means that the value of the coins on the side-chain will not be the same as on the main chain. For a side-chain to work, we need a proper exit mechanism.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Are the users signing different data or the same?

As I understand it the users will sign the block hash, so the signatures will be on the same message. This means verification needs only 2 parings.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Also i think there is some dos attacks in step 4 when users refuse to join a block forcing everyone else to recalulate their group signtures, or maybe i am missing something.

If you do not sign the block, your transaction will still be in the block, but not in the list of users that signed, so the transaction is ignored. Next time the operator will less likely include your transaction in the block.

---

**kilic** (2019-01-14):

It requires at least one G2 multiplication for BLS verification which [costs around 2M gas](https://github.com/musalbas/solidity-BN256G2).

Do you think schnorr signature aggregation also works?

---

**kladkogex** (2019-01-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Are the users signing different data or the same? Its dififcult to aggragate BLS signtures when the data is different.

All users are signing the same data.  The idea is that you glue all transactions in a block and what is signed is this block.  The malicious users may decide to withold their signatures, but it is not a problem since the list of the users that actually signed is passed to the smartcontract, and the transactions inside the block from users that did not sign are ignored.

---

**kladkogex** (2019-01-18):

[quote=“barryWhiteHat, post:2, topic:4790”]

How many signatures can you aggragate in BLS signtures? How difficult is this?

My understanding that one can aggregate as many as one wants, there does not seem to be a problem with that.

[quote=“barryWhiteHat, post:2, topic:4790”]

Also i think there is some dos attacks in step 4 when users refuse to join a block forcing everyone else to recalulate their group signtures, or maybe i am missing something.

If some users refuse to join,  the others do not need to recalculate, since the hash of the block will not change,  what will happen is the multi-signature will have less participants

---

**kladkogex** (2019-01-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> So the coins can never leave the contract? This means that the value of the coins on the side-chain will not be the same as on the main chain. For a side-chain to work, we need a proper exit mechanism.

One can have a version where coins will be able to exit. In this case you will need to pay a bit more gas per transaction, since you will need to keep ERC-20 balances for each user.

Constantinople fork will make this much cheaper because you will be able to push many user accounts in the same 256 bit value, and this value can be updated many times during a single transaction while utilizing the reduced gas cost …

---

**kladkogex** (2019-01-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> That’s a key weakness. The verification costs of an aggregate signature are at least one pairing per distinct message, which equates to one pairing per transaction. Each pairing costs 80,000 gas so the current gas limit (8,000,000) would allow for less than 100 transactions per block (~6 transactions per second, worse than standard 21,000 gas transactions).

Justin - it is just one single message verification, so it is one pairing per transaction …  What is signed is a block of messages …

---

**ldct** (2019-04-05):

I would like to point out one way that this is asymptotically less optimal than SNARKs

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The smart contract verifies the signature and saves the block into Ethereum log storage.

This requires the smart contract to compute the aggregate public key, e.g. by multiplying all the signers’ public keys together; hence the cost of verifying a state transition is linear in the number of transactions (whereas roll_up’s cost of verifying a state transition is constant AIUI)

(Note: of course the amount of calldata that roll_up uses per state transition is linear in the number of transactions, and that data has to be hashed together or similar, but I am excluding this from the “computational” cost of verifying a state transition)

---

**kladkogex** (2019-04-05):

Scalar multiplication is about 40,000 gas … pretty reasonable …

---

**mohamedbaza** (2019-04-09):

I have a simple question,  what is the problem that you suggest a solution for ?

---

**burdges** (2020-03-09):

BLS makes sense when you require truly non-interactive aggregation, normally by different signers on the same messages.  You’d need 1000 signers before you reach batched Schnorr verification speed even there however.

In this case, your protocol is interactive between wallets and the block producer, which makes deploying it extremely hard, i.e. no air gaped wallets here.

If you avoid the air gap issue and can do this, then you could use a Schnorr-like multi-signatures that achieves 2RTT by hashing all witnesses seperately, which massively improves performance but avoids the 3RTT from true Schnorr multi-signatures.

At first blush, I’d look into Mimble Wimble if you need a slightly less interactive version, possibly using BLS, or maybe Schnorr with witness Merkle tree.  There is also a layer two zoo in which nodes could sign that you signed or whatever.

---

**kladkogex** (2020-03-10):

Interesting … we can definitely consider Schnorr … Thank you

