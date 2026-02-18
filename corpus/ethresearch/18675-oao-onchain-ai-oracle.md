---
source: ethresearch
topic_id: 18675
title: "OAO: Onchain AI Oracle"
author: fewwwww
date: "2024-02-14"
category: Layer 2 > Optimisitic Rollup
tags: []
url: https://ethresear.ch/t/oao-onchain-ai-oracle/18675
views: 1805
likes: 7
posts_count: 2
---

# OAO: Onchain AI Oracle

## TL;DR

- Today we are launching OAO, an onchain AI oracle, complementary to our zkOracle offering. The OAO is powered by opML (optimistic machine learning) on Ethereum and brings ML models onchain.
- Currently, OAO supports LlaMA 2 and Stable Diffusion. Users can use these onchain models onchain.
- The future of onchain machine learning is optimistic with opML.

## 0. opML: Optimistic Machine Learning

### a) Onchain ML

Machine Learning and Artificial Intelligence, the trendiest and most talked-about computing paradigms today, have led to an acceleration of innovation.

Implementing ML or AI onchain can give machine learning computation the advantages of current onchain computing, including:

- Fairness
- Verifiability
- Computational Validity
- Transparency

However, the convergence of AI x Crypto is facing challenges. Taking Ethereum as an example, running ML/AI model inference on the blockchain faces the following challenges:

- Network resource: In order to ensure decentralization, it is not reasonable to have all nodes running complex ML computations in 12 seconds.
- Computation limitation: Ethereum’s EVM is a domain-specific language for smart contracts, and does not take into account ML and AI-related computational adaptations.

### b)

Some pioneers are trying to implement onchain ML using zkML. The idea is to generate a cryptographic proof for ML computations that is succinct enough to be verified on the blockchain.

However, this approach is not really practical given the restraints of current computing power, here are some examples:

- The zkML framework EZKL takes around 80 minutes to generate a proof of a 1M-nanoGPT model.
- According to Modulus Labs, zkML has >>1000 times overhead than pure computation, with the latest report being 1000 times.
- According to EZKL’s benchmark, the average proving time of RISC Zero is of 173 seconds for Random Forest Classification.

In the blockchain field, there is another commonly used form of proof: the fault/fraud proof, that is commonly deployed in optimistic rollups, and that can be serve as a more practical solution to realize onchain ML.

As [the inventor of opML](https://ethresear.ch/t/opml-optimistic-machine-learning-on-blockchain/16234) and [the first open source implementation](https://github.com/hyperoracle/opml), we are thrilled to see the growing adoption of opML. opML can [run Stable Diffusion and LLaMA 2 directly on Ethereum](https://www.hyperoracle.io/app/opml/sd). You can find the latest and most complete information about opML in the [whitepaper](https://arxiv.org/abs/2401.17555).

Compared to zkML or other onchain ML methods, **opML is all you need**.

[![zkML can run some small ML models onchain” & ”opML can run any ML model onchain”](https://ethresear.ch/uploads/default/optimized/2X/d/d1c2419d53f447441c2def1df1bbba9fdaa22834_2_690x387.png)zkML can run some small ML models onchain” & ”opML can run any ML model onchain”1876×1054 29.4 KB](https://ethresear.ch/uploads/default/d1c2419d53f447441c2def1df1bbba9fdaa22834)

[![Comparison between opML and zkML](https://ethresear.ch/uploads/default/original/2X/f/f6cea93b2062a5f7e13ba725e7320fb9eeebe67b.png)Comparison between opML and zkML1115×479 33.6 KB](https://ethresear.ch/uploads/default/f6cea93b2062a5f7e13ba725e7320fb9eeebe67b)

Comparison between opML and zkML

## 1. OAO: Onchain AI Oracle

### a) Introduction

We are thrilled to announce the deployment of opML on the Ethereum network.

[OAO](https://www.ora.io/app/opml/sd), with opML at its core, allows anyone to use onchain ML inference on the blockchain.

[![OAO](https://ethresear.ch/uploads/default/optimized/2X/a/ac81db5637c1a99e8b34b8454051d622d63c52f0_2_689x351.png)OAO1237×630 383 KB](https://ethresear.ch/uploads/default/ac81db5637c1a99e8b34b8454051d622d63c52f0)

OAO is a set of smart contracts including:

- opML contract, for fault proofs and challenges to ensure ML is onchain and verifiable
- AIOracle contract, for connecting the opML node with onchain callers to process ML request and introducing any ML model
- User contract, to initiate and receive AI results from OAO. This can be any contract customized by developers

### b) Architecture and Workflow

The specific architecture of the OAO is as follows. The user’s contract can initiate an AI request by calling the OAO, the OAO will publish the request to the opML node for processing, and then the OAO will return the AI result to the user.

[![Untitled (6)](https://ethresear.ch/uploads/default/optimized/2X/6/607e99be7e74da694bf80872bf5d2af172e69939_2_690x316.png)Untitled (6)1328×610 82.3 KB](https://ethresear.ch/uploads/default/607e99be7e74da694bf80872bf5d2af172e69939)

In terms of workflow, we need to break down the explanation into two parts.

Usage process:

1. The user contract sends the AI request to the OAO on chain, by calling the requestCallback function on the OAO contract.
2. Each AI request will initiate an opML request.
3. The OAO will emit a requestCallback event which will be collected by the opML node.
4. The opML node will run the AI inference, and then upload the result onchain.
 Challenge process:

The challenge window starts right after step 4 in the previous section.
5. During the challenge period, the opML validators (or anyone) will be able to check the result and challenge it if the submitted result is incorrect.
6. If the submitted result is successfully challenged by one of the validators, the submitted result will be updated onchain.
7. After the challenge period, the submitted result onchain is finalized (results can not be mutated).

When the result is uploaded or updated onchain, the provided result in opML will be dispatched to the user’s smart contract via its specific callback function.

Here’s the annotated detailed workflow:

[![Untitled (7)](https://ethresear.ch/uploads/default/optimized/2X/9/99809b2b16e4232413248ce8add404351b6ee416_2_690x346.png)Untitled (7)1170×587 91.6 KB](https://ethresear.ch/uploads/default/99809b2b16e4232413248ce8add404351b6ee416)

### c) Deployment and Usage

Here are the OAO contracts deployed onchain:

- AIOracle: Address: 0xb880D47D...1E2D4349d | Etherscan Sepolia
- Prompt (example user contract attached to AIOracle): Address: 0x5d696300...eA7Aef1a2 | Etherscan Sepolia

Currently, you can use the onchain ML model by initiating an onchain transaction by interacting with the prompt contract. We have uploaded two models to the OAO: LlaMA 2 (LLM model) and Stable Diffusion (Image Generation Model).

**Interact on [ora.io](http://ora.io)**

You can directly interact with OAO at: https://www.ora.io/app/opml/sd.

**Interact on Etherscan**

Here’s the usage guide if you want to play with it directly on Etherscan. You can also check out the [video guide](https://www.youtube.com/watch?v=zuhKVbTDqag) with all the steps:

1. Initiate AI calculation
 Go to the write contract tab, set modelId as 0 (LlaMA 2), and enter your prompt in human-readable text.
 screenshot1382×396 26.4 KB
2. See AI result
 Go to the read contract tab, set modelId as 0 (LlaMA 2), and enter your previous prompt.
 截屏2024-01-24 上午7.01.271382×574 39.2 KB

## 2. The future of onchain machine learning is optimistic.

### Partners and Use Cases

At this stage, we are experimenting with OAO and opML together with several projects:

- 7007.studio: The next generation marketplace to secure and govern AI models.
- MyShell: A decentralized and comprehensive platform for discovering, creating, and staking AI-native apps.
- Space Runners: A design tool built for fashion designers, powered by Stable Diffusion.

We are actively exploring the following use cases and directions:

- AIGC NFT (ERC-7007), 7007 Studio won the Story Protocol Hackathon
- zkKYC using facial recognition based on ML
- Onchain AI Games (e.g. Dungeon and Dragons)
- Prediction Market with ML
- Content Authenticity (deepfake verifier)
- Compliant programmable privacy
- Prompt Marketplace
- Reputation/Credit Scoring

### Future of Onchain ML

With an OAO, anyone and any contract can experience the magic of onchain ML. An OAO is decentralized and verifiable with the help of opML and its optimistic mechanism.

For our OAO, we’ll onboard more ML models. With our opML framework, you can Bing Your Own Model. Anyone is welcome to integrate with the OAO. And we have many more exciting releases coming in the future!

Optimistic machine learning will be the future of onchain machine learning. The future of onchain machine learning is optimistic!

## Replies

**0xemperor** (2024-02-16):

Extremely Interesting work!

Do you have any benchmarks or idea for how long it takes to generate a fraudproof in case a dispute is raised? Just curious how long it takes for the disputed “difference” in the layer to be found, does it change if the layer is deeper in the network than earlier?

