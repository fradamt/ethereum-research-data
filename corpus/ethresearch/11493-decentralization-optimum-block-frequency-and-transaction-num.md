---
source: ethresearch
topic_id: 11493
title: Decentralization, optimum block frequency and transaction numbers for ETH 2.0
author: Michael2Crypt
date: "2021-12-12"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/decentralization-optimum-block-frequency-and-transaction-numbers-for-eth-2-0/11493
views: 2072
likes: 0
posts_count: 1
---

# Decentralization, optimum block frequency and transaction numbers for ETH 2.0

I’d like to share a few thoughts about the article called [Endgame](https://vitalik.ca/general/2021/12/06/endgame.html) .

It’s an important article because it deals with the parameters of ETH 2.0, among them the block frequency and the number of transactions per second.

**1) Block frequency :**

The time required to validate a transaction is linked to the block frequency, because the sooner a transaction is included in a block, the sooner it is validated.

Centralized systems just like Visa or Mastercard can reach a latency of 1 or 2 seconds before validation.

Endgame article discusses “big block chain” with very high block frequency, which are nearly centralized. One of the first blockchain of this type was Bitshares, created by Dan Larimer.

Bitshares uses a DPOS consensus, meaning it has a few dozen of nodes called delegates, and reaches a block frequency of approximately 3 seconds : https://coincentral.com/what-is-bitshares/

I remember a video of Dan Larimer explaining how he managed to reach such a high block frequency : he had very powerful computers, connected with super fast internet cables.

This architecture would not be a good choice for Ethereum because it would be too centralized, with a low censorship resistance.

The more decentralization is wanted, the more nodes need to reach consensus, and it requires time.

A minimum level of decentralization for Ethereum would be a few hundred of first layer nodes, at least 200 to 500 nodes.

With reasonably good computers and good internet speed, a consensus would require 10 to 15 seconds. The block frequency for ETH 2.0 is said to be around 12 seconds, which is enough for a few hundred nodes to reach a consensus.

If Ethereum would like to prioritize decentralization, then a few thousand of first layers nodes would have to reach a consensus, which would require around 15 - 25 seconds in my opinion.

I don’t consider a 25 seconds block frequency as a problem if :

- it enables much more nodes to participate and to be full first layers nodes (5 000 first layer nodes well distributed all over the world would be very good in my opinion)
- it increases decentralization and censorship resistance
- it increases security, because nodes, and secondary layer nodes have the time to check transactions
- it reduces the specialization of block producers, requiring less powerful computers and internet speed.

It would be even possible to hide this 25 seconds block frequency to ordinary users, with a system of prevalidation : under 3 to 5 seconds, it’s possible for a few nodes to prevalidate a transaction and tell the user that the transaction is likely to be confirmed. It would only be an informative message, but it would be satisfying enough for ordinary users, even if the final confirmation occurs after 25 seconds when a block is fully validated by the consensus of first layer nodes, or if the final confirmation occurs even later with a second layer nodes confirmation.

**2) Number of transactions supported by the first layer of nodes :**

Centralized systems like Visa and Mastercard currently support a few thousand of transactions par second.

Another big blockchain of Dan Larimer, EOS, has reached 1,000 transactions per second, but it is nearly centralized, with only 21 block producers.

To reach such amounts of transactions per second, very specialized computers are needed, and the number of nodes should be very limited, because it would be too difficult for thousands of nodes to reach a consensus of thousands of transactions per second, at least with current ordinary computers.

Supporting thousand of transactions per seconds would not be a good choice for Ethereum currently, because it would be too centralized.

To keep a good level of decentralization, a consensus of a few thousand nodes should be reached.

With current computers, a few dozen or a few hundred of transactions per second for the first layer nodes would be reasonable.

**3) The secondary layer of nodes :**

As explained in Endgame article, there should be a secondary layer of nodes, with lower resource requirements.

This secondary layer could be in charge of different tasks : distributed block validation, but also partial storage of the blockchain history, signaling of anomalies, and even prevention of DDOS attacks if transactions are sent to the secondary layer nodes before reaching the first layer nodes, …

This secondary layer of nodes could therefore increase both the decentralization and security of Ethereum, but, at the same time, it would increase a little bit the time necessary to fully validate a block.

**4) Conclusion :**

The main value of Ethereum is it decentralization, not its low block frequency or high number of transactions supported per second (Visa and Mastercard do better concerning the validation time and the number of transactions per second).

To keep a very good level of decentralization and censorship resistance, the number of first layer nodes should be more than 1 000 and preferably a few thousand.

The block latency and confirmation time should be something between 12 - 30 seconds, and the number of validated transactions of the first layer nodes should be something between a few dozen and a few hundred per second.
