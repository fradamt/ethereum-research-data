---
source: ethresearch
topic_id: 3257
title: Questions about Ethereum priorities
author: Etherbuddy
date: "2018-09-06"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/questions-about-ethereum-priorities/3257
views: 1707
likes: 7
posts_count: 9
---

# Questions about Ethereum priorities

Hello,

I wonder about the priorities of Ethereum development.

Approximately half of the new cryptocurrencies listed on Coinmarketcap are masternodes (token excepted).

The reason is that masternodes are very efficient for fast transactions, reliability, scalability and rewarding of holders. They can be eco-friendly with little power usage and allow little or no fees, especially with POS. The funds are safe thanks to cold storage masternodes.

They are currently 3 cryptocurrencies based on Go Ethereum which have succeeded to implement masternodes :  Etherzero (POS masternodes), Akroma (POW masternodes) and Pirl (POW masternodes). Others are on the way like Exereum.

These cryptocurrencies have been able to implement masternodes on Go Ethereum within a few months with very limited resources.

Yet, Ethereum, with huge resources, is still running on POW without masternodes.

It seems Ethereum developers prefer to focus on difficult and untested concepts like plasma and sharding, whereas there are hundreds of masternode cryptocurrencies running swiftly, more than 130 being listed on Coinmarketcap.

Plasma and sharding may be interesting ideas, but making them a priority is debatable :

- the size of the blockchain (one of the big argument for plasma and sharding) is not a real problem : just implement an option allowing nodes to choose the size of the blockchain they want to store. The nodes which have little storage will store only the most recent transactions, and the nodes with a lot of storage could store the whole blockchain if they want. And why not include in the blockchain, once a month, a snapshot of account balances and smart-contracts. With this simple solution, there would be no need for ordinary nodes to store more than a month of blocks.
- 51 % attacks are not a big problem with POS, because taking control of the blockchain would require to invest billions to buy the required ethers. If some organizations decide to invest so much to take control of the blockchain, it will be a huge benefit for ethereum holders, and it would be possible to make a fork at any moment in case of misbehavior.
- there’s no need of plasma and sharding to handle a lot of transactions. With a good network of masternodes, instantsend options enable a lot of transactions.

Major problems are solved with a network of POS masternodes enabling instantsend.

Regarding the safety of the funds deposited for masternodes, cold storage, which is used in most masternodes currencies, is a much better option than locking the funds in a contract.

Regarding penalties to solve the “nothing-at-stake” problem, I’m not sure it’s a real problem, because many masternode currencies have been running for years without penalties. If some penalties were needed, it would be easy to implement a small stake, a small amount paid to other masternodes when a new masternode joins the network.

## Replies

**drcode1** (2018-09-06):

I’m no expert, but my understanding is (1) that masternodes/federated nodes greatly hamper economic analysis, as decisions of node owners basically become pure political decisions and (2) using nodes of this type only gives a small one-time boost in blockchain capacity which does not amount to a worthwhile tradeoff long term.

---

**Etherbuddy** (2018-09-06):

Masternodes owners are interested in the preservation of the value of the coin, on the long term, so it’s not a short term boost.

Masternode owners have interests, like everyone else : network users, network developers, … It’s just a balance of influence.

Masternodes have a lot of advantages in term of reliability, scalability, rewarding of holders, low fees, … And many masternode coins are running very well.

---

**MihailoBjelic** (2018-09-06):

Masternodes = centralization.

Ethereum priority/goal is to position Ethereum in the center of the [scalability triangle](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#this-sounds-like-theres-some-kind-of-scalability-trilemma-at-play-what-is-this-trilemma-and-can-we-break-through-it).

---

**Etherbuddy** (2018-09-07):

Masternodes offer the good level of decentralization in the scalability triangle.

When you have 1 node there is centralization. With 10 or 20 supernodes voting (DOS), there is still a high level on centralization.

With thousands of masternodes, you have a good level of decentralization. That’s why masternodes = decentralization.

And with such a number of masternodes, you can implement instantsend (scalability), and the level of security is very good because it’s a technology used by more than 130 coins listed on Coinmarketcap.

Masternodes are even more decentralized than POW coins, because usually on POW there are a few pools which are running the network.

---

**MicahZoltu** (2018-09-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/etherbuddy/48/586_2.png) Etherbuddy:

> the level of security is very good because it’s a technology used by more than 130 coins listed on Coinmarketcap

There is not a strong correlation between “lots of people do it” and “it is good” for any definition of “good” other than “lots of people do it”.

---

**MicahZoltu** (2018-09-07):

The security model for master-node systems is different from the security model for PoW or PoS.  While I do think federated chains and masternode chains have a place, it is a significant change in the security model of the system that should not be undertaken lightly.

In a masternode system (vs PoW/PoS), it is easier for a powerful adversary (e.g., state actor) to gain control of the network by taking over a dominant masternode share.  In many applications this is an acceptable risk, and one could even argue that for ETH/BTC it is an acceptable risk.  However, it isn’t the risk profile that users of Ethereum signed up for so we shouldn’t switch profiles without a great amount of thought/consideration.

We certainly need more than “everyone else is doing it”.

---

**Etherbuddy** (2018-09-07):

A technology widely used without any problem has a good chance to be secure. And the security model of masternodes can be associated with POS, that’s why there are a lot of POS masternode coins.

Concerning the argument that a powerful organization could take control over a dominant masternode share, there couldn’t be a better news for ethereum :

- such an attack would require the attacker to spend billions to buy ethers, which would increase the price of ethers a lot
- such an attack would be pointless, because a fork could be done at any moment in case of misbehavior

By the way, such an attack is not realistic, because states have a lot of financial problems. They have other priorities than spending billions to gain control of a blockchain.

---

**MicahZoltu** (2018-09-07):

As I said, the security model is different, not necessarily worse.  I don’t agree with all of your assertions (like state actors having better things to do than destroy crypto), but I also don’t believe that Masternode systems are inherently bad either.

My recommendation if you want to discuss the pros and cons of Masternode systems vs PoW or PoS systems is to start out by drafting up a security model for each and then comparing them.  Since each has a different set of attack vectors, the best place to start is documenting those vulnerabilities so they can be compared against each other.

