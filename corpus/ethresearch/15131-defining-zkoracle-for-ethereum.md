---
source: ethresearch
topic_id: 15131
title: Defining zkOracle for Ethereum
author: fewwwww
date: "2023-03-25"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/defining-zkoracle-for-ethereum/15131
views: 11171
likes: 34
posts_count: 27
---

# Defining zkOracle for Ethereum

## 0. Background

Currently, there is no unified term for the middleware protocols (The Graph, Gelato Network, Chainlink) used in DApp development, and most people usually categorize them as “Infra.” This term is vague and causes confusion as the underlying layer networks like Ethereum are also Infra.

Therefore, we at Hyper Oracle define the middleware involved in DApp development as “Oracle”. The term “Oracle” has been used to describe certain parts of the blockchain: We expand on its notion and propose the concept and design of a ZK-based Oracle for Ethereum.

More details about zkOracle and its components can be found in our whitepaper: [Hyper Oracle: A Programmable zkOracle Network](https://mirror.xyz/hyperoracleblog.eth/qbefsToFgFxBZBocwlkX-HXbpeUzZiv2UB5CmxcaFTM).

## 1. Framing of Oracles

When people hear the term “oracle,” they often associate it with the price feed oracle, which provides off-chain data to on-chain smart contracts. However, this is just one type of oracle among many.

A straightforward explanation of the Oracle concept, as outlined in this [educational resource](https://chain.link/education/blockchain-oracles), divides it into two main types:

- Input Oracle: delivers off-chain data to on-chain context (ex: Chainlink Price Feeds).
- Output Oracle: delivers on-chain data to off-chain context for advanced computation (ex: The Graph Protocol, Hyper Oracle zkIndexing).

[![截屏2023-02-21 下午3.04.20](https://ethresear.ch/uploads/default/optimized/2X/9/92d36d21b7aae5c40e3f4eaacc397025327fad43_2_690x388.png)截屏2023-02-21 下午3.04.202560×1440 149 KB](https://ethresear.ch/uploads/default/92d36d21b7aae5c40e3f4eaacc397025327fad43)

In the realm of blockchain, the terminology “input” and “output” are used to distinguish between two types of oracles: input oracles and output oracles. In addition, Hyper Oracle is defining the I/O oracle, a specialized type of oracle that integrates both input and output oracles by first following the output oracle’s flow and then the input oracle’s. Each oracle can be further broken down into three components: data source, computation, and output.

- Input Oracle

Data Source: Off-chain data (e.g. CEX price feeds, real-world weather data)
- Computation: Aggregation of off-chain data and “uploading” of data
- Output: On-chain data (equivalent to off-chain data, but stored on-chain)

Output Oracle

- Data Source: On-chain data (e.g. smart contract interactions or events like ERC-20 transfers or ERC-721 minting)
- Computation: Indexing, aggregation, filtering, or other complex computation
- Output: Off-chain data in an organized and easy-to-use form

I/O Oracle

- Combines Input Oracle and Output Oracle with Output flow first, then Input flow.

[![截屏2023-03-14 07.18.42](https://ethresear.ch/uploads/default/optimized/2X/8/88ee180f9e736f929505eefd069bf8696f5804ec_2_690x388.jpeg)截屏2023-03-14 07.18.422560×1440 227 KB](https://ethresear.ch/uploads/default/88ee180f9e736f929505eefd069bf8696f5804ec)

## 2. zkOracle

A zkOracle has advantages over a traditional oracle:

- Providing a unstoppable autonomous network
- Math as the consensus
- Safeguarding the security of the base layer
- A 1-of-N trust model
- Optimal cryptography-native decentralization
- Efficient computing power allocation (ideally no excess wasted)

As a component that processes data, an oracle must ensure both the accuracy and security of computation. It is important to confirm that the output is valid and correct and that the verification process is fast.

[![截屏2023-03-14 07.31.08](https://ethresear.ch/uploads/default/optimized/2X/1/1c048aa885e153d2f016abc1086bd539aff12d40_2_690x388.png)截屏2023-03-14 07.31.082560×1440 113 KB](https://ethresear.ch/uploads/default/1c048aa885e153d2f016abc1086bd539aff12d40)

To achieve a trustless and secure oracle, we need to make it a zkOracle.

Hyper Oracle zkOracle is natively categorized as output zkOracle and I/O zkOracle.

**I. Output zkOracle**

An output zkOracle is an output oracle that uses zk to prove its computation’s validity. An example of this is Hyper Oracle zkIndexing Meta App.

[![截屏2023-03-14 07.32.25](https://ethresear.ch/uploads/default/optimized/2X/6/60551b3eb89cbd4779f1797bbdc95feaa925d7bd_2_690x388.png)截屏2023-03-14 07.32.252560×1440 137 KB](https://ethresear.ch/uploads/default/60551b3eb89cbd4779f1797bbdc95feaa925d7bd)

- Data Source: On-chain Data
 The straightforward solution is to use on-chain data as the source. This data has already been verified and secured by the blockchain. Off-chain data sources cannot efficiently reach the trust level of on-chain data (at least not yet, according to this source). The on-chain data source solution requires zkOracle to act as an output oracle.
- Computation: Execution and ZK Proof Generation
 The solution is to create a zk proof of the computation (typically indexing, aggregation, and filtering…) and enable the step of accessing the data source in a zero knowledge fashion. This adds a layer of validity and trustlessness to the computation. The output will now be accompanied by a zk proof, making the computation and output verifiable.
- Output: Execution Output and On-chain Verifiable zk Proof
 The output of the computation will be both the execution output and a verifiable zk proof. The proof can be easily verified in a smart contract or any other environment. The verification component can confirm the validity of the execution of the zkOracle.

**II. I/O zkOracle (Output + Input)**

An I/O zkOracle is an output oracle and an input oracle both with ZK as computation. An example is Hyper Oracle zkAutomation Meta App.

[![截屏2023-03-14 20.29.17](https://ethresear.ch/uploads/default/optimized/2X/0/085518c92189247a046941b15bfb80688519ea6f_2_690x388.png)截屏2023-03-14 20.29.172560×1440 165 KB](https://ethresear.ch/uploads/default/085518c92189247a046941b15bfb80688519ea6f)

In this case, a zkOracle will function as a combination of two oracles that operates in two stages:

- Data Source: On-chain Data
 The data source for I/O zkOracle is identical to the output zkOracle.
- Computation: Execution and ZK Proof Generation
 The computation of I/O zkOracle includes the output zkOracle (which involves indexing, aggregation, and filtering) as well as the input zkOracle (which involves setting up off-chain computation results as calldata for smart contract calls). The combination of both parts makes it feasible to automate smart contracts with complex off-chain computation.
- Output: On-chain data and On-chain Verifiable zk Proof
 The output for this stage includes on-chain data which is the execution output provided on-chain as calldata, and a verifiable zk proof. This proof is easily verifiable in smart contracts or any other environment. The verification component can confirm the validity of the execution of I/O zkOracle.

**III. Definitions**

Technically, zkOracle is an oracle with verifiable pre-commit computation.

Functionally, zkOracle utilizes zk to ensure the computation integrity of the oracle node for the oracle network’s security, instead of staking and slashing mechanism.

In essence, zkOracle is an oracle that utilizes zk for computation and data access, while also using on-chain data for the data source to secure the oracle in a trustless manner.

**IV. Comparisons**

The advantages of the zkOracle network compared to traditional networks are similar to those of the zk rollup network compared to traditional distributed networks.

1. Security

The trust model of the zkOracle network is 1 of N, meaning the system remains functional as long as at least one node behaves as expected. Securing the network only requires one honest zkOracle node. In contrast, traditional oracle networks typically operate under a trust model of N/2 of large N, or 1 of 1.

[![Vitalik's definition on Trust Models (https://vitalik.ca/general/2020/08/20/trust.html)](https://ethresear.ch/uploads/default/optimized/2X/f/fb55877a18ea5156715a0dd88ac1e5862c316e09_2_564x500.png)Vitalik's definition on Trust Models (https://vitalik.ca/general/2020/08/20/trust.html)640×567 27.9 KB](https://ethresear.ch/uploads/default/fb55877a18ea5156715a0dd88ac1e5862c316e09)

Image Source: Vitalik’s definition on Trust Models (https://vitalik.ca/general/2020/08/20/trust.html)

It’s important to note that traditional oracle networks cannot be fully trusted when there’s only one node (either a data provider or an oracle node). This has significant implications for the following points.

1. Decentralization

The traditional oracle network may be difficult for entry due to its high staking requirement, but the zkOracle network will be more accommodating to nodes as it only requires hardware that can be further optimized through innovative proof systems and other cryptographic designs related to zk technology.

1. Performance

Performance is a crucial factor when it comes to oracle services, especially those that involve output oracles such as indexing protocols. The latency of request and response is highly dependent on the geographical distance between the node and the requester. Although requesters can rely on the results from the entire traditional oracle network, they cannot rely on a single node (that serves fastest), which can have an impact on performance. In contrast, a zkOracle node that is geographically closest and fastest can be trusted to provide better performance due to its computation verifiability.

## 3. zkOracle Network for Ethereum

> zkOracle = zkPoS + zkGraph run in zkWASM

Hyper Oracle is designing a zkOracle network operates solely for the Ethereum blockchain. It retrieves the data from every block of the blockchain as a data source with zkPoS and processes the data using programmable zkGraphs that run on zkWASM, all in a trustless and secure manner.

Here is the zkOracle design for the Ethereum blockchain. This serves as a foundational design for a zkOracle, complete with all of the essential components.

[![截屏2023-03-13 20.15.58](https://ethresear.ch/uploads/default/optimized/2X/1/1f88b8cfa14430bbe06564a6537e03e4ac4712f9_2_690x388.png)截屏2023-03-13 20.15.582560×1440 146 KB](https://ethresear.ch/uploads/default/1f88b8cfa14430bbe06564a6537e03e4ac4712f9)

zkPoS verifies Ethereum consensus with a single zk proof that can be accessed from anywhere. This allows zkOracle to obtain a valid block header as a data source for further processing.

zkWASM (zkVM in the graph) is the runtime of zkGraph, providing the power of zk to any zkGraph in the Hyper Oracle Network. It is similar to the kind of zkEVM used in ZK Rollups.

zkGraph (run in zkWASM) defines customizable and programmable off-chain computation of zkOracle node’s behaviors and Meta Apps. It can be thought of as the smart contract of the Hyper Oracle Network.

## Replies

**htftsy** (2023-03-27):

I think this is a promising direction for trustful data providing for light clients in a trustless environment. Which is the ZK schema that zkOracle is based on, is it Halo2? Also interested strongly in the functionality of zkWASM.

---

**sputnik-meng** (2023-03-27):

This is impressive and attractive! Due to the intensive competition in zkRollup development, it is time to reconsider except for zkRollup Layer2, what can zero-knowledge proof bring to us as a powerful and useful cryptographic primitive. And zkOracle seemingly answers this question.

---

**fewwwww** (2023-03-27):

ZK Rollup definitely inspires a lot of zk usages in blockchain.

Actually, when doing the framing for oracle, I was thinking about calling ZK Rollup as one of the zkOracle.

However,

1. ZK Rollup’s system is more complex.
2. The core part is not about the oracle, but state transition or bridge.
3. If ZK Rollup is zkOracle, then Rollup will have to be one kind of oracle.

To avoid confusion, ZK Rollup is not one category in zkOracle.

---

**fewwwww** (2023-03-27):

Yes. Hyper Oracle zkOracle and zkWASM are all in Halo2 PSE. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

You can watch our talk for more technical details about zkOracle at [here](https://www.youtube.com/watch?v=kHT6uOX3jto).

And you can also read the paper of zkWASM for more details about its functionality and architecture at [here](https://jhc.sjtu.edu.cn/~hongfeifu/manuscriptb.pdf).

---

**htftsy** (2023-03-27):

This is amazing! Thanks a lot for the reply.

PSE Halo2 is efficient and can be verified on chain.

---

**claytonroche** (2023-04-24):

I wanted to flag a section from Vitalik’s Schellingcoin piece for you [@fewwwww](/u/fewwwww) –

> Mining for Schells
>
>
> The interesting part about SchellingCoin is that it can be used for more than just price feeds. SchellingCoin can tell you the temperature in Berlin, the world’s GDP or, most interestingly of all, the result of a computation. Some computations can be efficiently verified; for example, if I wanted a number N such that the last twelve digits of 3N are 737543007707, that’s hard to compute, but if you submit the value then it’s very easy for a contract or mining algorithm to verify it and automatically provide a reward. Other computations, however, cannot be efficiently verified, and most useful computation falls into the latter category. SchellingCoin provides a way of using the network as an actual distributed cloud computing system by copying the work among N parties instead of every computer in the network and rewarding only those who provide the most common result.

I just wanted to confirm for myself – What Vitalik suggests here with computations is what Hyper Oracle can do, but in an optimistic fashion, right?

I had [asked Marlene about this on our Twitter space](https://twitter.com/UMAprotocol/status/1643266879161548800) too, and that’s pretty much what she’d said.

I’m curious what you think the tradeoffs are? I mean, assuming all else is equal, you’d always use a ZK solution over an optimistic one. Maybe the costs could be different, though?

---

**fewwwww** (2023-04-24):

What Vitalik is talking about here could be implemented via Hyper Oracle’s zk, and of course I think in Vitalik’s statement Vitalik would have known that zk might be an implementation path as well. All compute-related steps can be easily migrated to zk.

But since these are non-deterministic off-chain data, we may have to adopt a “consensus” mechanism like "rewarding only those who provide the most common result ". ~~Such a mechanism may be sort of like “optimistic”~~ (edit: it’s actually honest majority that we don’t really want.). Such a mechanism itself may not be removed in this example (due to the data source), but the mechanism’s logic can still be wrapped in zk, allowing for succinct verification of it in external systems. The example here is a potential Input zkOracle.

---

**kladkogex** (2023-04-24):

I think one can probably repurpose ZK EVM to do it.  ZK EVM can not read logs, but if one adds instructions to read logs from blocks, then you can write a Solidity program to read and processes data both from state and logs.

Same with off-site computations - one can treat it as an EVM instance running outside blockchain and  acting on the current state root.

---

**fewwwww** (2023-04-24):

I really like this idea, it is definitely good to unify the tech stack, and also to reuse a lot of the ecosystem work done in zkEVM.

Some side effects on the zkEVM approach is that:

- It needs to implement a lot of new EIPs, and because of the many protocol changes involved, shipping those standards can be very slow.
- In this scenario, the performance of the zkEVM solution may not be better than that of the generic zkVM solution.
- Many of the existing technology stacks and custom applications (oracle, middleware) are not based on Solidity, and these would need to be rebuilt.

In practice, we (Hyper Oracle) choose to use generic zkVM (zkWASM, zkRISCV…) for building zkOracle. At the same time, the recent boom in Nova technology may allow zkVM to be both performant and general.

---

**kladkogex** (2023-04-25):

Hey

Interesting.

Do you think Nova will run faster than existing systems (like Linea from Consensys?)

---

**fewwwww** (2023-04-25):

I personally believe that Nova has great potential as a new ZK stack to provide further performance enhancements for large circuits (especially zkVM).

As compared to Halo2 in the [PSE benchmark](https://github.com/privacy-scaling-explorations/nova-bench), **For large circuits, Nova appears to be faster than Halo2 (KZG)**. However, there is no comparison with Linea’s gnark yet, but I think there are potential enhancements.

However, these would require more specialized cryptographers and circuit engineers to study them in depth. In general, the conceptual implementation of zkOracle can be based on any scheme, be it a zkWASM or zkRISC0, or any zkEVM.

---

**karl-lolme** (2023-04-26):

[@fewwwww](/u/fewwwww) Maybe I’m not understanding the intended use case of this oracle. My question is can the new design provide a ETH-USD oracle price in a more robust fashion than either makerDAO’s reputation-based chronicles protocol or Chainlink or Tellor’s to-be crypto-economic scheme? Thanks

---

**kladkogex** (2023-04-26):

I think this one is for the case where data is on chain and you want to do lots of computation for it

---

**fewwwww** (2023-04-26):

Just like [@kladkogex](/u/kladkogex) explained, the main use cases of zkOracle is output oracle (more like indexing protocol) and i/o oracle (more like automation network). They both have the original data source from on-chain with heavy computation that can only be performed in off-chain context.

The case you mentioned is input oracle case. It’s a little bit tricky if we want to make input oracle into zkOracle. Because data source is originally from off-chain context (USD, asset price in CEX). If data source is not from on-chain, it may be hard to assume that those source data reached consensus. There’s no single truth or consensus for ETH/USD. And zk part in zkOracle and any other case only secures computation, not the original data source.

We can experiment it with several ways:

- Just use something like Uniswap TWAP as on-chain price oracle feed with help of zk in off-chain context for heavy lifting of heavy computation and accessing historical data. So the data source is from on-chain now. But it can only support ETH/USDC, ETH/USDT…, not ETH/USD.
- More complicated mechanism, just like building a stable coin on-chain with zkOracle. Then get the ETH/USD price based on the first approach.

In general, since the data source comes from off-chain, it may need a more complex system to secure the entire process with zk fully input oracle (like Chainlink Price Feeds).

---

**kartin** (2023-04-27):

One standout application for zkOracle is the zk Stable Coin, which allows pledging with any fiat currency through off-chain zkML-level computations.

---

**bsanchez1998** (2023-04-27):

I like how the zkOracle is divided into input and output. Makes me think that to avoid oracle type hacks a network for these oracles should be run and they should have gossip protocol-like checking so that there is less centralization in oracle protocols, because that’s where problems come in. Overall ZKPs do address the limitations of traditional oracle networks and this not only enhances security but optimizes performance. It’s really interesting to see how the zkOracle network utilizes zkPoS and zkGraphs running on zkWASM to make this all happen trustlessly and securely. I’m looking forward to seeing more about this, as I created my own post about ZKPs enabling a novel type of decentralized relay. I think you might find that interesting as well.

---

**fewwwww** (2023-04-27):

For a zk network (including zkOracle), the design of the consensus protocol is very important. It is also different from (or, say better than) the consensus of traditional blockchain networks or oracle networks.

We are looking forward to some new explorations in zk network consensus, such as zk rollup networks.

---

**fewwwww** (2023-09-05):

After further exploration, development, and research into zkOracle, we realized that the core of what we were building was the Ethereum-based “zkOracle protocol”, as well as the “programmable zkOracle protocol”.

A more precise definition of zkOracle is a ZK-based onchain oracle protocol.

For updates on our research and development, see: Hyper Oracle’s [Blog](https://mirror.xyz/hyperoracleblog.eth) and [GitHub](https://github.com/hyperoracle).

---

**fewwwww** (2023-09-05):

For an on-chain zkOracle protocol, there are three primary applications that enhance the computational capabilities of smart contracts:

- Accessing and Computation of Historical Onchain Data:
The zkOracle protocol empowers smart contracts by generating zero-knowledge proofs (such as zkPoS, State Proof, and Event Proof), facilitating access to comprehensive historical onchain data. This functionality enables smart contracts to utilize historical data for further computations within the smart contract or the zkOracle itself.
- Extension of Complex Computational Capabilities:
Conventional smart contracts face inherent limitations within the onchain computing environment, restricting their ability to execute certain functions, including processing large datasets, running complex models, and performing high-precision computations. Conversely, zkOracle transcends these limitations, offering an expansive range of computational possibilities without constraints. This includes the capacity to handle high-intensity computations, such as machine learning tasks.
- Internet Data:
In addition to onchain data sources, zkOracle and smart contracts can seamlessly incorporate internet-based data. Leveraging trustless proving libraries of Transport Layer Security (TLS), zkOracle can collaborate with Proof of HTTPs protocols, opening up diverse avenues for utilizing internet data. The integration of zkOracle with these protocols facilitates access to internet data, thereby unlocking new opportunities for onchain data utilization and computation.

---

**Nafla-hh** (2024-01-03):

Strange choice of word to call that an oracle instead of a coprocessor.

Interesting ideas tho.

If I understand correctly, the idea of the Output zkOracle is to attach proof of correct source and computation when a user retrieves blockchain data. The verifier would need to obtain a trusted block hash from which to start the verification, so it’s similar to running a light client, right ? Are there any tradeoff here with traditional zk light clients like Plumo in terms of proving time/proof size ?

I know Axiom v2 is also using Halo2, any tradeoffs or differences in designs or goals here ?


*(6 more replies not shown)*
