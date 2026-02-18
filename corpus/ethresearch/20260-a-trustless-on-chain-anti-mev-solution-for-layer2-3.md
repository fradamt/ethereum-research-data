---
source: ethresearch
topic_id: 20260
title: A trustless on-chain anti-MEV solution for Layer2/3
author: Lawliet-Chan
date: "2024-08-13"
category: Layer 2
tags: [mev]
url: https://ethresear.ch/t/a-trustless-on-chain-anti-mev-solution-for-layer2-3/20260
views: 2395
likes: 4
posts_count: 8
---

# A trustless on-chain anti-MEV solution for Layer2/3

We have a solution to resolve the Layer2 MEV onchain trustlessly.

Here is the arch:

[![image](https://ethresear.ch/uploads/default/optimized/3X/a/e/aeec6e16bbf3b6864d66ae84ecf5b663f9c55ce5_2_336x500.jpeg)image1244×1848 122 KB](https://ethresear.ch/uploads/default/aeec6e16bbf3b6864d66ae84ecf5b663f9c55ce5)

1. Users only send their txHash to the L2 chain with some advance charge (to prevent DOS attack)
2. The chain accepts these txHashes, sort them based on the amount of tips, and then make a Tx-Order-commitment and broadcast it to the other chain nodes.  Also, user can subscribe this commitment.
3. When users see the order-commitments, they will send their tx-content to the L2 chain and the DA-layers.
4. Chain accepts the tx-content from users, and also fetch txs from DA-layers ,  pack them according to the previously promised order. If the tx-content does not match the previously tx-hash, chain will put them behind the txs which made order-commitment.
All promised txs will be sorted before the unpromised txs.
NOTICE: In this way, the chain may deduct tx-content and pretend not to receive it.  To prevent this situation. We have to:
i. Decentralise chain node.
ii. Use DA to complete the txs if one node does not accept the txs.

In this case, we call it MEVless protocol,   it means you don’t have to trust any group and institution.  You do not have to depend on a privacy node, not through MEVA, to protect your transactions from MEV attack.  Because all the attackers(besides miners themselves) cannot see your tx-content when it orders.   Once the tx-content is packed and executed, it must be packed by the previously commitment, attackers cannot front-run and sandwich attack you.

We have developed some of it and you can see the running effect:


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/yu-org/nine-tripods/tree/main/MEVless)





###



Contribute to yu-org/nine-tripods development by creating an account on GitHub.











      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/VersechainLabs/versechain/tree/mevless)





###



[mevless](https://github.com/VersechainLabs/versechain/tree/mevless)



A high performance decentralized modular sequencer for Starknet










[![image](https://ethresear.ch/uploads/default/optimized/3X/b/f/bfa58e407bea18228ba10bbc90f904aca2c776aa_2_607x500.jpeg)image1920×1580 376 KB](https://ethresear.ch/uploads/default/bfa58e407bea18228ba10bbc90f904aca2c776aa)

You can see the txHash order-commitment in the above red box and you can try MEV-attacking these txs when they are completed by tx-contents later, then you will find you cannot insert your tx into their order at all.

## Replies

**qzhodl** (2024-08-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/lawliet-chan/48/12316_2.png) Lawliet-Chan:

> i. Decentralise chain node.
> ii. Use DA to complete the txs if one node does not accept the txs.

Does the user need to post the transaction content to the DA layer every time, or is it just a backup solution? If it’s a backup solution, how does the user know that the sequencer won’t include the transaction before the block is mined?

---

**Lawliet-Chan** (2024-08-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/qzhodl/48/9870_2.png) qzhodl:

> Does the user need to post the transaction content to the DA layer every time, or is it just a backup solution? If it’s a backup solution, how does the user know that the sequencer won’t include the transaction before the block is mined?

Yes.

The DA is an enhance solution that users can choose to protect their txs further because the decentralization of L2/3  may not higher than L1, the DA can protect users from L2 deduct the tx-content.

It is possible that sequencer miss the tx-content:

1. The L2 does not accept the user’s tx timely due to some objective reasons such as public network delay
2. The L2 subjectively accepts the tx but maliciously withheld txs to facilitate MEV attacks.

So, in this case, if L2 can obtain the tx-content from multiple channels as much as possible, it will be more healthy and strong.

---

**netdev1** (2024-08-13):

Traditionally the main criticism against this type of commit-reveal scheme has been that users get a 2nd choice to cancel their tx by not revealing the hashed data. This likely solves sandwitch attacks but  front-running, back running, cex/dex arb are still possible.

You can spam arbitrage tx for high volatility pools and only reveal them if you can make a profitable trade (pool price vs CEX price). You’ll still have to pay a fee all tx even those that are not revealed it’s not hard to still be profitable

---

**Lawliet-Chan** (2024-08-13):

If you cancel the tx by not revealing the txHash, your tx will be put behind all the commitment ordered txs. That means you cannot front-running, the back-running will be possible.

MEVless protect all the order-commitment txs from sandwich and front-running.

As for arb and clearing, I believe they are MEVs in a broad sense, and their harm to blockchain is not as bad as the previous ones. So our design is not aimed at arb and clearing.

---

**qzhodl** (2024-08-13):

What if an attacker tries to DDoS this Layer 2 network by spamming transaction hashes without revealing the content?

---

**Lawliet-Chan** (2024-08-13):

As I said above:

```auto
1.Users only send their txHash to the L2 chain with some advance charge (to prevent DOS attack)
```

All users must send the advance charge for payment when they send the txHash onto chain to prevent DOS attack, after order commitment, chain will reset these txHash from TxPool before block mined([nine-tripods/MEVless/mev_less.go at 456baedf119493891a5f5db2a611c2817bab16b1 · yu-org/nine-tripods · GitHub](https://github.com/yu-org/nine-tripods/blob/456baedf119493891a5f5db2a611c2817bab16b1/MEVless/mev_less.go#L124))

So,  don’t worry. The spamming txs will cost for attackers and they will not include the block

---

**qizhou** (2024-08-23):

I believe there is a relationship of the proposed idea with [Alleviate MEV on Sequencer with Partial-Fields-VDF-Encoded Tx and ZK-based Validity Proof](https://ethresear.ch/t/alleviate-mev-on-sequencer-with-partial-fields-vdf-encoded-tx-and-zk-based-validity-proof/15668) :

- Addressing DoS attack: A better way may reveal the tip fields of an existing Ethereum transaction and use ZK to verify the validity (sufficient fund) of the existing Ethereum transactions.  This avoids introducing a new Tx type and creating the compatibility issue.
- DA issue: small Tx content itself may not be efficient using existing DA.  E.g., EIP-4844 BLOB is 128KB, while a transfer Tx is about ~100B. A VDF may address the DA problem at the cost of delay.

