---
source: ethresearch
topic_id: 7844
title: Adding cross-transaction BLS signature aggregation to ethereum
author: vbuterin
date: "2020-08-15"
category: Cryptography
tags: [signature-aggregation]
url: https://ethresear.ch/t/adding-cross-transaction-bls-signature-aggregation-to-ethereum/7844
views: 3941
likes: 10
posts_count: 4
---

# Adding cross-transaction BLS signature aggregation to ethereum

BLS signature aggregation is a powerful technology that allows many signatures for many messages signed by many keys to be compressed into a single signature, which can be verified against the entire set of (message, pubkey) pairs that it represents simultaneously.

That is, if there are:

- A set of private keys k_1, k_2 ... k_n (held by different users)
- The corresponding pubkeys K_1, K_2 ... K_n
- Messages m_1, m_2 ... m_n, where m_i is signed by the corredponding k_i and the signatures are S_i = k_i * H(K_i, m_i)

Then you can make an aggregate signature S = S_1 + S_2 + ... + S_n, where S has a fixed size (usually 32-96 bytes depending on configuration), and S can be verified against the entire set of pairs [(K_1, m_1), (K_2, m_2) ... (K_n, m_n)] (the messages and the *public* keys), confirming that S is a valid aggregate of signatures for those key and message combinations.

The challenge when deploying this in a ethereum context, however, is that signature aggregation is at its most powerful when we aggregate many signatures together, and this implies somehow aggregating together signatures across many transactions within a block. Unfortunately, the EVM is not suited to this, because each EVM execution’s scope is limited to being within a particular transaction.

I propose a simple extension to the EVM to alleviate this difficulty. We add a new opcode, `EXPECT_BLS_SIGNATURE`, which takes two arguments off the stack: (i) a memory slice representing the pubkey (represented on the stack by the starting position in memory, as we know how many bytes a pubkey contains), and (ii) the message (standardized to be a 32 byte hash). The block verification procedure processes this opcode by adding the pair `(pubkey, message)` to an `expected_signatures` list (this list starts off empty at the start of every block). We also add to the block header a field `bls_aggregate`. At the end of block processing, we take the whole `expected_signatures =` [(K_1, m_1), (K_2, m_2) ... (K_n, m_n)] list, and perform the BLS aggregate signature check:

 e(K_1, H(K_1, m_1)) * e(K_2, H(K_2, m_2)) * ... * e(K_n, H(K_n, m_n)) ?= e(S, G_2)

Where S is the `bls_aggregate` and G_2 is the elliptic curve generator. If the check does not pass, the entire block is invalid.

At network layer, we add a wrapper to the `Transaction` class, where each transaction can come with a signature that covers the expected signatures during execution. A block proposer (ie. miner) would receive the transaction, attempt to verify it by running the transaction, computing the `expected_signatures` array *just for that transaction*, and seeing if the signature provided with the transaction matches that array. If it does, and the transaction passes the other usual validity and fee sufficiency checks, the block proposer incldues the transaction, and adds (using elliptic curve addition) the transaction’s provided BLS signature to the block’s `bls_aggregate`; if it does not, then the block proposer ignores the transaction.

Note that this breaks the invariant that a transaction cannot be made to be *invalid* as a result of things that happen during execution (which is important to [prevent DoS attacks](https://hackingdistributed.com/2016/06/28/ethereum-soft-fork-dos-vector/)). Hence, if deployed on the base layer, it should be combined with [account abstraction](https://ethereum-magicians.org/t/implementing-account-abstraction-as-part-of-eth1-x/4020), with the `EXPECT_BLS_SIGNATURE` opcode only usable before the `PAYGAS` opcode is called.

## Replies

**emilianobonassi** (2020-08-17):

That’s great!

This could be an enabler for plenty of (efficient) schemas, not only related to batching operations but also for novel (authentication) protocols.

It would be nice to see more native instructions for PBC, not only restricted for BLS, e.g IBE.

---

**SergioDemianLerner** (2020-08-17):

Pairings are costly in terms of CPU, and each signature aggregation requires one pairing operation. Last time I checked, this cost was approximately 10 times more (in terms of CPU cycles) than validating a ECDSA signature. Therefore your proposal trades space for higher CPU cost.

In 2018 I proposed a hybrid solution to send transactions with both ECDSA and BLS signatures, verifying only ECDSA signatures for some time, and then switching to BLS when the block is sufficiently mature. Therefore only nodes that are synchronizing from zero need to use more CPU cycles, but they benefit from reduced bandwidth and space.

This is ok since most of the times nodes that synchronize from zero can use weak subjectivity to get signed snapshots.

The idea is here:


      [github.com](https://github.com/rsksmart/RSKIPs/blob/6e233db72a163ebdd5be828fadabd02bf65ef45e/IPs/RSKIP63.md)




####

```md
# Double Signing for Delayed Signature Aggregation

|RSKIP          |63           |
| :------------ |:-------------|
|**Title**      | Double Signing for Delayed Signature Aggregation|
|**Created**    |07-MAY-2018 |
|**Author**     |SDL |
|**Purpose**    |Sca |
|**Layer**      |Core |
|**Complexity** |2 |
|**Status**     |Draft |

# **Abstract**

Blockchain historic size is one of the restrictions for scaling. A RSK transaction uses 70 bytes for ECDSA signature data and approximately 30 for the transaction payload itself. Therefore by removing the signatures from transactions the blockchain can scale 2.3 times. One technique to reduce the size of signatures is signature aggregation.  This RSKIP proposes aggregating signatures in a novel construction to reduce blockchain space consumption.

## Introduction

There are several types of signature aggregation: sequential (ordered), underdered, interactive and non-interactive. In this RSKIP we’re interested in non-interactive aggregation. The type of aggregation that can be accomplished by a miner on third party transactions. Therefore we are interested in signature aggregation of signatures of different messages and different public keys. Some signature schemes, such as BLS, allow it. However the state-of-the-art signature schemes that provide this kind of signature aggregation are slow. Aggregating a BLS signature may cost 10 times more (in terms of CPU cycles) than validating a ECDSA signature. Signature verification can be cached, so signature verification is generally not part of the critical path when broadcasting a block. The same happens with signature aggregation: the heavy non-constant operations can be cached. However, in the worse case a block can contain all new transactions, and each node would need to perform the slow operations. The slow operations would grow linearly with the number of transactions, and will affect the critical path of block verification. This RSKIP brings a new solution to this problem, based on double-signing transactions

```

  This file has been truncated. [show original](https://github.com/rsksmart/RSKIPs/blob/6e233db72a163ebdd5be828fadabd02bf65ef45e/IPs/RSKIP63.md)

---

**sherif** (2021-02-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/sergiodemianlerner/48/1059_2.png) SergioDemianLerner:

> each signature aggregation requires one pairing operation

we only need one signature aggregation for all block transactions, but BLS signature or Multisignature wasn’t used in Eth2.

