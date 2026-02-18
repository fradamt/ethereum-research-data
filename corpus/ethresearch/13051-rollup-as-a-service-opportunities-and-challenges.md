---
source: ethresearch
topic_id: 13051
title: "Rollup as a Service: Opportunities and Challenges"
author: nanfengpo
date: "2022-07-13"
category: Layer 2
tags: []
url: https://ethresear.ch/t/rollup-as-a-service-opportunities-and-challenges/13051
views: 16445
likes: 9
posts_count: 5
---

# Rollup as a Service: Opportunities and Challenges

TLDR: This article discusses the opportunities and challenges in building “Rollup as a Service” for Web3 applications.

# RaaS Opportunities, From Multi-chain to Multi-rollup

Cosmos and Polkadot adopt the multi-chain structure for their scaling solutions. Their blockchain SDK, Tendermint and Substrate, are applied by many projects to customize blockchains. These blockchains use cross-chain protocols like [Cosmos IBC](https://ibc.cosmos.network/), [Polkadot XCM](https://wiki.polkadot.network/docs/learn-crosschain), and [bridges](https://wiki.polkadot.network/docs/learn-bridges) to interact with each other. However, such protocols are difficult to guarantee high security, which leads to frequent exploit events. As a result, cross-chain protocols did not work as expected, resulting in relative independence between blockchains.

[![cosmospolkadot](https://ethresear.ch/uploads/default/optimized/2X/e/efb50713f798d15585b6323deb3e1873bf0a8e49_2_690x259.jpeg)cosmospolkadot1381×520 143 KB](https://ethresear.ch/uploads/default/efb50713f798d15585b6323deb3e1873bf0a8e49)

*From https://v1.cosmos.network/intro* *and* *[Getting Started - Polkadot Wiki](https://wiki.polkadot.network/docs/getting-started)*

Later, a more secure scaling technology called rollup emerged. Rollup compresses Layer 2 transactions into a “batch”, uploads it to Layer 1, and proves the validity of state transition on Layer 1 through Fraud Proof (Optimistic-rollup) or Validity Proof (ZK-rollup). Since data availability and state validity are verified on Layer 1, rollup obtains the same level of security as Layer 1, ensuring that assets can be safely transferred between Layer 1 and Layer 2.

So far, many rollup projects such as Arbitrum, Optimism, ZkSync, and StarkNet have already been in use. In addition to these universal rollups, there also came up some **application-specific rollups,** including [StarkEx rollup SDK](https://starkware.co/starkex/)-based dYdX (order book DEX) and DeversiFi (AMM DEX), etc. Although the rollup technology is not yet fully developed, and few teams have mastered it, there is still strong demand for this technology on the market.

[![](https://ethresear.ch/uploads/default/optimized/2X/0/09141676d6f9401f63798182e660d3347912e157_2_586x500.png)1001×854 158 KB](https://ethresear.ch/uploads/default/09141676d6f9401f63798182e660d3347912e157)

*Universal and application-specific rollups listed at https://l2beat.com/*

Rollup provides a standalone execution environment with high TPS, low gas, and access to all assets from Layer 1, which helps applications on the blockchain scale from DeFi to more general fields like games and social networks. We expect rollup will gradually become a sort of service provided to **Web3 applications**, i.e., **Rollup as a Service (Raas)**. Some projects are now heading in this direction. Ethereum’s [rollup-centric roadmap](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698) and StarkNet’s [Layer 3 architecture](https://medium.com/starkware/fractal-scaling-from-l2-to-l3-7fe238ecfb4f) both demonstrate an application-specific multi-rollup future.

[![](https://ethresear.ch/uploads/default/optimized/2X/b/b9dcab53ebf4116ef98e6260e9af36cb78db8e76_2_690x414.png)700×421 128 KB](https://ethresear.ch/uploads/default/b9dcab53ebf4116ef98e6260e9af36cb78db8e76)

*StarkNet’s architecture described in* *https://medium.com/p/7fe238ecfb4f* *, where Layer3 are multiple application-specific rollups.*

# Challenges in Building RaaS

Rollup still faces the following challenges in providing RaaS.

## Engineering

First of all, let’s talk about the **rollup SDK**. One can deploy some configuration and launch rollups quickly based on an SDK. The open-source rollups are better choices for SDK development to avoid reinventing the wheel. For Optimistic-rollups, both Arbitrum and Optimism are open-source. From L2beat, we can see that both Metis and Boba are developed on Optimism’s code base. In contrast, ZK-rollups are not very open-source. ZkSync releases complete code for [v1](https://github.com/matter-labs/zksync) but merely the [contract](https://github.com/matter-labs/v2-testnet-contracts) code for v2 (zkEVM enabled). StarkEx releases only the [contract](https://github.com/starkware-libs/starkex-contracts) code and provides other modules to third parties through a closed source. StartNet provides code solely in [Cairo](https://github.com/starkware-libs/cairo-lang).

Though Optimistic-rollups have more mature codebases and better support for EVM, the inherent characteristics of fraud-proof leave them far behind ZK-rollups in terms of finality and security. A ZK-rollup Layer 2 transaction is finalized immediately after being proved on Layer 1, while an Optimistic-rollup Layer 2 transaction requires several days before the finalization due to the challenge period. On the other hand, Optimistic-rollups need more assumptions for security: at least 1-out-of-N honest operators for fraud-proof submission and a censorship-resistant Layer 1 for fraud-proof acceptance.

In sum, we can quickly build an Optimistic-rollup SDK right now based on the existing open-source code, but **a ZK-rollup SDK seems more attractive in the long run**. Of course, in addition to the codebase issue, a design of ZKVM, i.e., ZKP-provable smart contracts, is also in urgent need. Currently, a variety of ZKVM solutions are under development. The methods of each solution are still not unified.

[![](https://ethresear.ch/uploads/default/optimized/2X/1/191f91fb22fb14d4b175aaa0ad42ebf9bc18aafe_2_690x348.png)1321×668 112 KB](https://ethresear.ch/uploads/default/191f91fb22fb14d4b175aaa0ad42ebf9bc18aafe)

*A comparison of ZKVMs by Ye Zhang’s talk "* *[An overview of zkEVM](https://drive.google.com/file/d/1SyOXq8CtoEOKplw0KxazAL_YySdpsP62/view)* *"*

## Performance

As mentioned, batched transactions are required to send to Layer 1 in a rollup, so the **TPS** of the rollup is limited by Layer 1’s storage space, aka the [Data Availability](https://hackmd.io/@vbuterin/sharding_proposal#Why-is-data-availability-important-and-why-is-it-hard-to-solve) (DA) problem. Ethereum has proposed a series of Layer 1 storage scaling solutions, including EIP-4488, Proto-Danksharding, and the full Danksharding (currently [seeking proposals](https://github.com/ethereum/requests-for-proposals/blob/e8eed947a35d966027f47dfdd6c556089228642d/open-rfps/das.md)). Besides the scaling for Layer 1, many projects like Celestia and Polygon Avail are also attempting to expand the storage capacity for Layer 2. However, these solutions’ security and ease of use still need further examination.

[![](https://ethresear.ch/uploads/default/optimized/2X/b/b90da11588ef8619fd7f6c9e5fd627a6cd3658b7_2_690x222.png)761×245 19.2 KB](https://ethresear.ch/uploads/default/b90da11588ef8619fd7f6c9e5fd627a6cd3658b7)

*How the block size will be increased by EIP-4488 and Proto-danksharding in Vitalik’s "* *[Proto-Danksharding FAQ](https://notes.ethereum.org/@vbuterin/proto_danksharding_faq)* *"*

In terms of ZK-rollup, the **TPS** is additionally limited by ZKP calculation speed. Paradigm and 6block have different hardware choices on GPU, FPGA, and ASIC to accelerate the calculation. In addition, 6block compares several software architectures for ZKP distributed computing, including mining pool, proof aggregation, and DIZK. [ZPrize](https://www.zprize.io/), an upcoming competition, also incentivizes developers to find valuable solutions to accelerating ZKP calculation.

Ensuring the high availability of the rollup service is another critical issue. Current rollups on the market are almost centralized, i.e., only specific operators can submit batches and proofs to Layer 1. This is a vulnerable design since the SPOF (single point of failure) will easily lead to service unavailability. Arbitrum has suffered hours of downtime on several occasions due to [software bugs](https://medium.com/offchainlabs/arbitrum-one-outage-report-d365b24d49c) and [hardware failures](https://offchain.medium.com/todays-arbitrum-sequencer-downtime-what-happened-6382a3066fbc). Many projects are working on decentralizing rollups to avoid SPOF, including [zkSync](https://docs.zksync.io/userdocs/decentralization.html), [StarkNet](https://community.starknet.io/t/starknet-decentralization-tendermint-based-suggestion/998), [Polygon Hermes](https://ethresear.ch/t/proof-of-efficiency-a-new-consensus-mechanism-for-zk-rollups/11988), [PoVP](https://ethresear.ch/t/a-design-of-decentralized-zk-rollups-based-on-eip-4844/12434), and [taikocha.in](http://taikocha.in/).

## Economics

**A good economic model** is under consideration for RaaS. For now, the profits of service providers mainly come from the transaction fee gap between Layer 1 and Layer 2, i.e., charging fees from Layer 2 as the revenue and paying fees to Layer 1 as the costs. Optimism has issued its [governance token](https://community.optimism.io/docs/governance/), but it’s still not a good way to maintain a sustainable income.

[![](https://ethresear.ch/uploads/default/original/2X/b/bef13fe92d843dec865c1e937cf9d8f4d1c86eff.png)615×498 26.7 KB](https://ethresear.ch/uploads/default/bef13fe92d843dec865c1e937cf9d8f4d1c86eff)

*Rollups and their fees listed on* *https://l2fees.info/*

Most of the existing rollups are third-party services built on the blockchain, so their primary income is merely from the transaction fee. However, we can get out of this mindset and regard rollups as **native services** the blockchain provides. Like Cosmos’ and Polkadot’s design, the whole system contains one blockchain and multiple rollups attached to the blockchain, forming a decentralized network with infinite scalability. In this way, the network can reward both Layer 1 blockchain validators and Layer 2 rollup operators with the same native token. This idea is similar to “[enshrined rollups](https://twitter.com/epolynya/status/1511623759786307586)” proposed by Polynya and is worth further research.

## Functionality

Like the cross-chain protocols in Cosmos and Polkadot, a **cross-rollup** **protocol** is necessary when multiple rollups are deployed on one blockchain. Users can also withdraw their assets from Layer 1 and deposit them to another rollup, but the process requires additional fees on Layer 1 and more operation steps. Some third-party [cross-rollup bridges](https://newsletter.banklesshq.com/p/how-to-hop-between-chains) leverage liquidity pools to help users transfer between rollups instantly, but these bridges are as vulnerable to exploits as cross-chain bridges.

[![](https://ethresear.ch/uploads/default/original/2X/1/1fbc0d587575f1b2501374699957060c125d15d9.png)581×331 6.74 KB](https://ethresear.ch/uploads/default/1fbc0d587575f1b2501374699957060c125d15d9)

*A future blockchain architecture described by Vitalik in "* *[Endgame](https://vitalik.ca/general/2021/12/06/endgame.html)* *", with multiple rollups and cross-rollup bridges among them*

Ideally, the blockchain should provide a **native cross-rollup bridge** maintained by its validators for security. Moreover, such a bridge should preferably support synchronous message calls from one rollup to another, i.e., a user on one rollup can directly call the contract on another. This will maximize user experience in a multi-rollup architecture. The underlying technology is complicated, but we look forward to its emergence.

# Conclusion

This article describes RaaS, i.e., providing rollup services to DApps. Apparently, blockchain will usher in a multi-rollup future for Web3. Anyone can quickly launch their rollup with an SDK and run applications on the rollup with high performance and low costs. After discussing all the possible challenges faced by RaaS, we finally came up with the idea of **native rollups**, which will help the blockchain reward rollup validators with its native token and provide a cross-rollup bridge maintained by its validators. We plan to study it further carefully and elaborate on it in future articles.

## Replies

**shakeib98** (2022-11-13):

After reading the post I have one thought that Rollmint (Celestia’s SDK for rollup) is similar to this? Would you agree on it?

---

**nanfengpo** (2022-11-16):

Yes, there are some similarities, for example we both provide an SDK to help users build rollup quickly, but the platform where Native Rollup is mentioned in this article is more focused on a fully functional chain rather than just a DA layer, which would include things that celestia does not, such as unified consensus, a unified economic model, and **native** cross-rollup communication

---

**madhavg** (2023-01-17):

yo was curious where does fuel vm fit into the landscape?

---

**neelsomani** (2023-01-30):

Heads up that this is what we’re building at Eclipse: https://twitter.com/EclipseFND

We don’t offer a rollup SDK at this point but might add one in the future as the customizations we support become more sophisticated.

