---
source: ethresearch
topic_id: 14150
title: Zero fee Ethereum architecture
author: Michael2Crypt
date: "2022-11-09"
category: Architecture
tags: [zk-roll-up]
url: https://ethresear.ch/t/zero-fee-ethereum-architecture/14150
views: 2129
likes: 0
posts_count: 5
---

# Zero fee Ethereum architecture

There are currently approximately 450 000 Ethereum validators.

They could be used for additional tasks, for example validating not only L1 Ethereum, but also L2 and L3 “Official Ethereum Rollups” :

[![architecture](https://ethresear.ch/uploads/default/optimized/2X/d/d288c946b4fba70346a03aee61d1e32173da1fa1_2_681x500.jpeg)architecture800×587 79.4 KB](https://ethresear.ch/uploads/default/d288c946b4fba70346a03aee61d1e32173da1fa1)

Each of the 450 000 Ethereum validators could be randomly assigned to one L2 Official Ethereum Rollup and one L3 Official Ethereum Rollup.

The security level would be better than current “unofficial” rollups, because if some validators don’t fulfill their L2 and L3 tasks, they could face a ban or a slash.

Each layer would have its own role :

- L1 Ethereum would be dedicated to “important” transactions requiring maximum security, just like it is currently.
- L2 Official Ethereum Rollups would provide reduced fees, in exchange for a slightly lower security. For example, some artists could choose one of the 64 L2 Official Ethereum Rollups to mint their valuable NFT with reduced fees.
- L3 Official Ethereum Rollups could offer zero fee transactions, in exchange for a slightly lower security. It could be used for gaming token, or for fan tokens enabling each influencer to create a micro-economy, by selling or giving away fan tokens. These use cases require massive microtransactions with zero fee.

Zero fee would be reachable on L3 Official Ethereum Rollups, because the maintenance cost would be very low :

- the cost of development would be shared between the 4 096 L3 Official Ethereum Rollups, because it is the same software.
- the cost of validation would be very low, because validation on L2 and L3 Official Ethereum Rollups would just be a side task, an additional task assigned to Ethereum validators.
- the cost of storage could be limited if anti-spam measures are implemented to limit the number of transactions. For example, on the L3 client, looking an ad could be required every few microtransactions. And since microtransactions are not very valuable, there would be no need to store the history of each L3 rollup on thousands of computers.

More, these ads could provide long term resources to the Ethereum foundation.

Online ads are a major source of revenue for organizations whose wealth rely on information, like Meta, Google, Tiktok, …

Online ads running on the L3 client and offering zero fee transactions could become a major source of revenue for the Ethereum foundation.

## Replies

**cybertelx** (2022-11-11):

here are my thoughts:

- having 64 + 4096 different rollups all considered “official” would break composability and introduce a lot of fragmentation, without granting a lot of benefits (AliceDEX is on rollup 3619, but my Ether is all on rollup 1447 and the MuchWowDogeInu2.0Moon token is only deployed on rollup 1104! what do i do???)
- on L2, computation is cheap but calldata is as expensive as on mainnet due to data availability requirements, so moving to L3 wouldnt really do much for that. validiums would grant you the power you desire at the cost of decentralization (i believe proto-danksharding/EIP-4844 will blur the line between rollup & validium)
- about the ads on the L3 client: how do we enforce this in FOSS software? what if a community project builds a client that doesn’t have ads in it? how do we check? how do we prove it without adding more centralization into the mix

---

**Michael2Crypt** (2022-11-11):

Hi,

> having 64 + 4096 different rollups all considered “official” would break composability and introduce a lot of fragmentation, without granting a lot of benefits (AliceDEX is on rollup 3619, but my Ether is all on rollup 1447 and the MuchWowDogeInu2.0Moon token is only deployed on rollup 1104! what do i do???)

- There are a lot of benefits : the proposed model makes Ethereum very scalable, enabling thousands of transactions per second without compromising decentralization and security. Rollups are a very good solution because they enable fractal scalability, while keeping potentially strong decentralization and security.

[![rollups](https://ethresear.ch/uploads/default/original/2X/8/815a2f2580253906634f9b7c77989f54f3e5e1e8.jpeg)rollups708×352 16.7 KB](https://ethresear.ch/uploads/default/815a2f2580253906634f9b7c77989f54f3e5e1e8)

- Yes, the proposal introduces fragmentation, just like sharding. The fact is that a monolithic blockchain is too heavy. It needs to be fragmented. Fragmenting in 64 + 4096 different rollups seem to be a lot, but it means that L3 rollup chains will be lighter, enabling them to be stored easily on an average computer, on event a smartphone.
- This fragmentation may be reversed in the future, if technical solutions emerge to store easily much more data than currently. Reorganizing a large amount of data is possible.
- Transfering Ethers and tokens from a rollup to another is a common issue of the rollup technology, as the ethereum website explains : “Bridges … With the proliferation of L1 blockchains and L2 scaling solutions … the need for communication and asset movement across chains has become an essential part of network infrastructure.”
- Regarding security, the ethereum website explains : “Security – Who verifies the system? Bridges secured by external validators are typically less secure than bridges that are locally or natively secured by the blockchain’s validators.” The proposed solution of official L2 and L3 Ethereum rollups is one of the safest, because bridges could be natively secured by the blockchain’s validators.

> on L2, computation is cheap but calldata is as expensive as on mainnet due to data availability requirements, so moving to L3 wouldnt really do much for that. validiums would grant you the power you desire at the cost of decentralization (i believe proto-danksharding/EIP-4844 will blur the line between rollup & validium)

- regarding the cost of calldata, some projects are implementing calldata compression to save on fees.
- EIP-4844 may be useful. It is claimed that “EIP-4844 is to reduce gas fees on the network, especially for the rollup solutions” . In this case, the cost of transaction on L2 Rollups may be so low that zero fee transactions may be offered to users. In this case, L3 official Ethereum rollups may be useless.
- I agree that validiums are not a good option, I prefer rollups because they are more secure and resistant to censorship

> about the ads on the L3 client: how do we enforce this in FOSS software? what if a community project builds a client that doesn’t have ads in it? how do we check? how do we prove it without adding more centralization into the mix

- a huge milestone is to make gas fee so low that a transaction can be covered by watching an ad. It means a cost of a few cents per transaction. At this point, the access to the Ethereum network can be free for most users.
- this is the way many video games and apps like Instagram, Google and Twitter work : their use is free, but users watch an ad from time to time. Most users, especially young users, can’t or don’t want to pay. They want to download an app, use it for free, and get an experience they like.
- once gas fee is very low, around a few cents, technical solutions will emerge. Nothing has to be enforced. The ad can remain on the client side, without involving projects.
- for example, some Ethereum wallet apps may wire a few cents in Ethers once users download the app and create a wallet on a L3 Official rollup. There may be an ad tab inside the app, where users could watch ads and receive a few cents in Ethers each time, enough to make a few transactions for free, like sending gaming, NFT or fan tokens, …
- if there is an official Ethereum wallet app, partnerships could be made with well chosen digital advertising companies, giving them access to the ad tab of the wallet app. It could become a long term source of revenue for the Ethereum foundation.

---

**cybertelx** (2022-11-11):

ty for the quick response,

> Yes, the proposal introduces fragmentation, just like sharding.

atm the ethereum proposed way of sharding is just danksharding (data storage sharding), afaik we aren’t sharding the execution layer any time soon so no fragmentation as it would ruin the UX

> The fact is that a monolithic blockchain is too heavy. It needs to be fragmented. Fragmenting in 64 + 4096 different rollups seem to be a lot, but it means that L3 rollup chains will be lighter, enabling them to be stored easily on an average computer, on event a smartphone.

i believe proposer/builder separation will make things better so validators/proposers won’t need to store a load of data, rather itll just accept bids from builders, plus light clients are being championed which are meant for mainstream users. not everyone needs to run a full node

> This fragmentation may be reversed in the future, if technical solutions emerge to store easily much more data than currently. Reorganizing a large amount of data is possible.

perhaps ether balances could be merged, but how about tokens? what if there are multiple instances of the token on different rollups? how about different create2’d instances of the same contract with the same address on different rollups with different state?

> (this is my quote) on L2, computation is cheap but calldata is as expensive as on mainnet due to data availability requirements, so moving to L3 wouldnt really do much for that. validiums would grant you the power you desire at the cost of decentralization (i believe proto-danksharding/EIP-4844 will blur the line between rollup & validium)

you havent addressed that L3 is pretty much useless over L2 when trying to optimize gas fees, check out https://vitalik.ca/general/2022/09/17/layer_3.html by vitalik buterin

---

**Michael2Crypt** (2022-11-12):

> “you havent addressed that L3 is pretty much useless over L2 when trying to optimize gas fees, check out What kind of layer 3s make sense? by vitalik buterin”

[The article explains](https://vitalik.ca/general/2022/09/17/layer_3.html)  : “*If we can build a layer 2 protocol that anchors into layer 1 for security and adds scalability on top, then surely we can scale even more by building a layer 3 protocol that anchors into layer 2 for security and adds even more scalability on top of that ?*“

But some problems may occur : “*There’s always something in the design that’s just not stackable, and can only give you a scalability boost once - limits to data availability, reliance on L1 bandwidth for emergency withdrawals, or many other issues.*”

Yet, **the article confirms that you can scale computation with SNARK** : “*SNARKs, can scale almost without limit; you really can just keep making “a SNARK of many SNARKs” to scale even more computation down to a single proof.*”

Regarding computation, the proposed model of L2 and L3 Official rollups is therefore possible, with a Zk-Rollup implementation.

The problem of data availability is more complex, as the article explains : “*Data is different. Rollups use a collection of compression tricks to reduce the amount of data that a transaction needs to store on-chain: … About 8x compression in all cases. But rollups still need to make data available on-chain in a medium that users are guaranteed to be able to access and verify*”

There are solutions to increase data availability in a context of rollups on top of rollups.

An [article on Coinmarketcap](https://coinmarketcap.com/alexandria/article/what-is-eip-4844-a-quick-guide-for-beginners) about EIP-4844 explains : “*it has been proposed that the data can be stored elsewhere in a way that it is easily accessible like several applications/protocols that provide that service.*”

To increase data availability, a solution would be to store data elsewhere, not only on the compressed blockchain. Blockchain is basically a security measure intended to secure transactions, so they cannot be modified.

But the data could also be available elsewhere.

**L1, L2 and L3 blockchains could have a buffer for data availability**. In this buffer, there would be a list of all the addresses of the blockchain with their balances in real time, and a list of the characteristic of the smart contracts implemented on the chain. These buffers should have enough information to validate new transactions without having to do expensive calldatas on the blockchain, at least most of the time.

If the buffer is too big, it could be sharded between nodes operating on the same blockchain.

Being uncompressed and easily accessible, the buffer would solve the problem of data availability.

> atm the ethereum proposed way of sharding is just danksharding (data storage sharding), afaik we aren’t sharding the execution layer any time soon so no fragmentation as it would ruin the UX

Rollups can be seen as a way to shard the execution layer. Some rollups are popular, and this fragmentation doesn’t ruin the UX.

Regarding data sharding, there is a consensus that it is necessary, because the monolithic L1 chain is too heavy.

But :

- there are several ways to shard data. I would prefer a temporal sharding of data. Validators should have the option to store only a random period of the blockchain history (if they store more, they are more rewarded). Storing only a part of the blockchain would not be a problem for data availability with the proposal of buffer.
- sharding data doesn’t mean sharding the execution of the L1 chain. If the L1 chain is divided into different shards working in parallel, security breaches may occur, with risks of double spending attempts,  looping problems, contradictory instructions …
- an interesting post about sharding and parallelization comes to the same conclusion : “Rollups + data-availability sharding are substantially less complicated than most sharding proposals.”
- as the post explains, a major argument in favor of rollups is that “a single honest party” is required, enabling to push “heavy-duty execution” on rollups
- the proposed model of L2 and L3 official Ethereum rollups could come along with buffers to increase data availability, and a sharding of data, preferably a temporal sharding.

> “i believe proposer/builder separation will make things better so validators/proposers won’t need to store a load of data, rather it ll just accept bids from builders, plus light clients are being championed which are meant for mainstream users. not everyone needs to run a full node”

Yes I agree that validators shouldn’t be required to store a lot of data. Once data is sharded, one way or another, it will be possible to run lighter clients.

> “perhaps ether balances could be merged, but how about tokens? what if there are multiple instances of the token on different rollups? how about different create2’d instances of the same contract with the same address on different rollups with different state?”

In the case, very hypothetical, where a fragmentation of data should be reversed, it’s possible to add an identification linked to the original shard.

It’s also possible to identify different contracts with the same address on different shards.

More, if there are official L2 and L3 rollups, it may be possible to shard the addresses. For example, a certain range of addresses could be assigned to L3 rollup n°1, another range to L3 rollup n° 2, …

As a conclusion, L1 Ethereum runs about 1 million transaction per day. Instagram and Facebook have  around 1,5 billion daily users. In case Ethereum is to become as popular, with zero fee transactions, there may be around 200 million daily users, who would process an average of 3 daily transactions (utility token, gaming token, fan token, NFT, …). It means the Ethereum ecosystem should be able to handle 600 million to 1 billion transaction a day.

This is a   **x1000 factor** compared to the current situation. It may be possible to reach such scalability with L2 Rollups, or other L2 solutions, but models with L3 rollups should also be considered.

A benefit of L3 rollups is that they write Zero-Knowledge Proofs on L2 rollups, which is much cheaper than putting Zero-Knowledge Proofs on the L1 chain. So the use of **L3 is more in line with the goal of zero fee transactions**.

