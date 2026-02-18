---
source: ethresearch
topic_id: 21050
title: Transport privacy exploration of the Validator-Relayer Builder API
author: QYu
date: "2024-11-20"
category: Privacy
tags: [mev, p2p, proposer-builder-separation]
url: https://ethresear.ch/t/transport-privacy-exploration-of-the-validator-relayer-builder-api/21050
views: 483
likes: 3
posts_count: 1
---

# Transport privacy exploration of the Validator-Relayer Builder API

# Transport privacy exploration of the Validator-Relayer Builder API

*Special thanks to [@Nero_eth](/u/nero_eth) and [@liobaheimbach](/u/liobaheimbach)*

## Abstract

The availability of metadata from the networking layer of Ethereum, particularly in Proposer-Builder Separation (PBS)-enabled environments poses real and immediate privacy risks. Among other concerns, it allows and incentivizes adversaries to target and interfere with block production processes to prevent certain transactions or even entire blocks from being processed. Our experiment, “Metaclear,” investigates how transport-level privacy leaks at validator-relay interfaces allow targeted disruption via metadata analysis and low-cost network-layer attacks. We implemented a transport metadata harvesting pipeline of the full MEV architecture stack to link validators’ public keys to the IP address of their consensus client as well as that of the mev-boost software and executed attacks in a lab setting to demonstrate the practical applications of this work. We found that once de-anonymized, block proposers became vulnerable to network attacks aimed at interfering with future block proposals. We also identified scenarios where different parties besides proposers can be attacked when transport privacy is unprotected. Through this experiment, we want to i) challenge the trust assumptions in MEV infrastructure such as relayers, ii) advocate researchers and engineers to integrate network-level metadata privacy protocols into the design of enshrined PBS, and iii) expand the scope of MEV considerations to include transport-layer metadata.

## Table of contents

[Abstract](#p-51319-abstract-2)

[1. Introduction](#h-1-introduction-4)

[1.1. MEV Relay in PBS](#p-51319-h-11-mev-relay-in-pbs-5)

[1.1.1 Definition of terms](#p-51319-h-111-definition-of-terms-6)

[1.2. Privacy issues in Relays](#p-51319-h-12-privacy-issues-in-relays-7)

[1.3. Randomness generation by validators](#p-51319-h-13-randomness-generation-by-validators-8)

[1.4. Contributions](#p-51319-h-14-contributions-9)

[2. Methodology](#p-51319-h-2-methodology-10)

[2.1. Metadata collection in Relay HTTP calls](#p-51319-h-21-metadata-collection-in-relay-http-calls-11)

[2.2. Attestation data collection](#p-51319-h-22-attestation-data-collection-12)

[2.3. De-anonymization](#p-51319-h-23-de-anonymization-13)

[2.4. Simulation of network attacks](#p-51319-h-24-simulation-of-network-attacks-14)

[3. Setup and environment](#p-51319-h-3-setup-and-environment-15)

[3.1. Architecture](#p-51319-h-31-architecture-16)

[3.2. Environment and test parameters](#p-51319-h-32-environment-and-test-parameters-17)

[4. Results](#p-51319-h-4-results-18)

[4.1. Linking public key and IP addresses of validators](#p-51319-h-41-linking-public-key-and-ip-addresses-of-validators-19)

[4.2. Identifying victim validators](#p-51319-h-42-identifying-victim-validators-20)

[4.3. Viable network attacks](#p-51319-h-43-viable-network-attacks-21)

[5. Discussion: Further Attack scenarios and Network Consequences](#p-51319-h-5-discussion-further-attack-scenarios-and-network-consequences-22)

[5.1. Network topology can be mapped using Relay metadata](#p-51319-h-51-network-topology-can-be-mapped-using-relay-metadata-23)

[5.2. Solo stakers are more vulnerable to attack](#p-51319-h-52-solo-stakers-are-more-vulnerable-to-attack-24)

[5.3. RANDAO can be exploited and manipulated](#p-51319-h-53-randao-can-be-exploited-and-manipulated-25)

[5.4. Blobs can be disrupted](#p-51319-h-54-blobs-can-be-disrupted-26)

[5.5. Recently bootstrapped, sparsely connected beacon nodes are more vulnerable to “covert flash attacks”](#p-51319-h-55-recently-bootstrapped-sparsely-connected-beacon-nodes-are-more-vulnerable-to-covert-flash-attacks-27)

[5.6. Selectively attack multi-block MEV](#p-51319-h-56-selectively-attack-multi-block-mev-28)

[5.7. Malicious Relay can more easily conduct a metadata-based attack without leaving traces](#p-51319-h-57-malicious-relay-can-more-easily-conduct-a-metadata-based-attack-without-leaving-traces-29)

[5.8. Decentralizing Relays makes attacks more likely, not less](#p-51319-h-58-decentralizing-relays-makes-attacks-more-likely-not-less-30)

[5.9. Valuable metadata can make Relay a victim](#p-51319-h-59-valuable-metadata-can-make-relay-a-victim-31)

[5.10. Builders can be made to underperform](#p-51319-h-510-builders-can-be-made-to-underperform-32)

[5.11. A new class of MEV?](#p-51319-h-511-a-new-class-of-mev-33)

[6. Limitations](#p-51319-h-6-limitations-34)

[7. Future research](#p-51319-h-7-future-research-35)

[Bibliography](#p-51319-bibliography-36)

## 1. Introduction

One standard definition of Maximal Extractable Value (MEV) defines MEV as “the maximum value that can be extracted from block production […] by including, excluding, and changing the order of transactions in a block [[1]](https://ethereum.org/en/developers/docs/mev/).” However, these are not the only actions which can be taken by network participants to disrupt or extract value. Indeed, the current focus on mempool data – comprising pending transactions [[2]](https://assets.ey.com/content/dam/ey-sites/ey-com/en_us/topics/financial-services/ey-an-introduction-to-maximal-extractable-value-on-ethereum.pdf) – provides a limited perspective and overlooks other potentially valuable sources of data that could be exploited for extracting value.

One such underexplored source is the data collected from the networking layer that underpins blockchain systems. For a distributed network to function properly, various subprotocols coordinate states among nodes, such as the broadcasting of mempool transactions and the gossiping of attestations. We [[3]](https://medium.com/hoprnet/proof-of-stake-validator-sniping-research-8670c4a88a1c) and other researchers [[4]](https://doi.org/10.48550/arXiv.2409.04366) have previously shown how data harvesting from these low-level communication protocols and collecting relevant metadata can be a source of valuable information, for example by linking validator public keys to their IP address. Once parties involved in block production have been de-anonymized, adversaries can target them, interfering with their block production processes and potentially excluding expected transactions from a block or entire blocks altogether.

This risk becomes even more pronounced in a Proposer-Builder Separation (PBS) - enabled environment, where the introduction of builders – responsible for constructing blocks – adds complexity to the communication protocol. When validators connect to a block-building service that contains a trusted party in the middle to moderate block delivery, the trusted party processes privileged information including validator metadata. When validators connect to a decentralized network of builders, their metadata is exposed to more parties. With more metadata to observe, the potential for privacy leakage increases, creating opportunities for MEV disruption and perhaps extraction. However, the potential for MEV extraction in PBS has not been thoroughly explored [[5]](https://ethereum.org/en/roadmap/pbs/).

This experiment, named “Metaclear”, seeks to assess the feasibility of these attacks by examining transport-level privacy in the context of PBS in a practical manner and in a controlled lab environment, with a specific focus on privacy leaks at the interfaces between validators and relays. “Metaclear” reveals how metadata can de-anonymize stakeholders involved in block creation and demonstrates potential methods for exploiting these vulnerabilities to disrupt block production and extract additional value which falls outside the traditional definition of MEV.

### 1.1. MEV Relay in PBS

The PBS scheme was introduced as part of Ethereum’s transition to Proof-of-Stake (PoS), aiming to bifurcate block production into two distinct roles: block builders, responsible for collecting and ordering transactions, and proposers, tasked with proposing new validated blocks. While the design and specifications have been discussed since 2018 [[6]](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725), consensus on the design of enshrined PBS (ePBS) or in-protocol PBS (IP-PBS) has not yet been reached. Various proposals for ePBS, such as two-slot PBS [[7]](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980), single-slot PBS [[8]](https://ethresear.ch/t/single-slot-pbs-using-attesters-as-distributed-availability-oracle/11877), Protocol-Enforced Proposer Commitment (PEPC) [[9]](https://ethresear.ch/t/unbundling-pbs-towards-protocol-enforced-proposer-commitments-pepc/13879), and Payload-timeliness committee (PTC) [[10]](https://ethresear.ch/t/payload-timeliness-committee-ptc-an-epbs-design/16054), emphasize different assumptions about the desired degree of decentralization, economic incentives, and appropriate positioning on the spectrum of censorship resistance.

Currently, the most widely adopted implementation by block proposers, based on slot share [[11]](https://mevboost.pics/mevboost.pics), is an out-of-protocol PBS called MEV-Boost. MEV-Boost is a market-driven block-building platform developed by Flashbots [[12]](https://boost.flashbots.net/). In a nutshell, MEV-Boost requires at least one trusted centralized middleman called “Relay”, which sits in between block builders and Ethereum validators and which prevents validators from extracting value from builders and also prevents builders from withholding information from validators. Validators run an instance of MEV-Boost alongside their client software so that when they are selected as a block proposer, MEV-Boost requests block-building information from the Relay. Block contents are fed by block builders at the beginning of a slot. The Relay implements the latest Builder API specification [[13]](https://ethereum.github.io/builder-specs/).

[![Figure 1 Architecture of MEV-Boost, an implementation of PBS by Flashbots](https://ethresear.ch/uploads/default/optimized/3X/2/0/2006f08ea6e79bd49ec7ec94bb2e09928889e963_2_690x188.png)Figure 1 Architecture of MEV-Boost, an implementation of PBS by Flashbots1498×410 220 KB](https://ethresear.ch/uploads/default/2006f08ea6e79bd49ec7ec94bb2e09928889e963)

***Figure 1** Architecture of MEV-Boost, an implementation of PBS by Flashbots [[14]](https://github.com/flashbots/mev-boost)*

#### 1.1.1 Definition of terms

The terms “proposer” and “builder” can carry different meanings depending on the context in which they are discussed.

In the Ethereum Proof of Stake context, the term “proposer” refers to one of the main duties of validators. When a validator is randomly chosen for a specific slot, their responsibility is to propose a new block containing transactions for that slot. The term “builder” refers to the block builders who are responsible for creating blocks of transactions and offering them to the block proposer for each slot [[5]](https://ethereum.org/en/roadmap/pbs/). For example, MEV-Boost (from the mev-boost instance running along the beacon client to the entire marketplace with block builders and searchers) is considered a “builder” within PBS implementations [[14]](https://github.com/flashbots/mev-boost).

In the context of MEV-Boost as one PBS implementation with a block-building marketplace, “MEV Boost” has three major components (see Figure 1 for its architecture): Builder, Relay, and mev-boost. Here, “Builder” refers to block builders who provide the ordered payload of a full block considering MEV extraction and reward distribution. “mev-boost” in blue in Figure 1 refers to the narrow sense of mev-boost, a sidecar middleware run by validators, which provides access to the “MEV-Boost” marketplace.

When considering the “Relay” component of MEV-Boost, “builder” has the same meaning as in the MEV-Boost context, referring to block builders external to MEV-Boost. Here, builders call the Relay HTTP API [[15]](https://flashbots.github.io/relay-specs/). “Proposers” are validators with mev-boost middleware. Relays implement the Ethereum Builder API specs [[13]](https://ethereum.github.io/builder-specs/) to handle API calls from mev-boost middleware.

Since our research is focused on the architecture of MEV-Boost, for clarity we will use the same terminology as defined for the Relay component.

### 1.2. Privacy issues in Relays

Relays play a special role in current PBS, because they protect searchers and builders from proposers who may try to steal the value of bundles and blocks via, e.g., unbundling. Relays also provide validity checks on transactions with an EVM execution client [[16]](https://ethresear.ch/t/relays-in-a-post-epbs-world/16278). However, the centralized and intermediary nature of Relays requires both validators and builders to trust Relays in two different ways: first, that the data delivered by the Relays is accurate, and second that the Relays themselves will not actively attack the validators or builders. Indeed, facets of Relay design such as payload sharing and value spoofing [[17]](https://collective.flashbots.net/t/post-mortem-for-a-relay-vulnerability-leading-to-proposers-falling-back-to-local-block-production-nov-10-2022/727) have been exploited in the past [[18]](https://github.com/flashbots/mev-boost/blob/4035cb3c8c8f9b0118a0170049203f0167c604a0/docs/audit-20220620.md).

These trust assumptions are well known, and countermeasures are already implemented such as signatures and mechanisms against known unbundling attacks which would prevent relays from allowing arbitrary insertion or deletion of transactions from a bundle [[19](https://collective.flashbots.net/t/post-mortem-april-3rd-2023-mev-boost-relay-incident-and-related-timing-issue/1540), [20](https://blog.sigmaprime.io/mev-unbundling-rpc.html)]. However, the true extent of the trust assumptions is much broader, and less explored. Relays possess the advantage of collecting metadata of validators and builders. Metadata leaks via HTTP calls can reveal information about nodes’ IP address and location within the networking layer [[21](https://doi.org/10.1007/11767831_1), [22](https://doi.org/10.1145/384268.378789)]. By correlating data collected on the consensus layer and more, nodes can be identified with relative ease and thus become a target of attacks on the networking layer. Proposals such as Block Negotiation Layer (BNL) [[23]](https://ethresear.ch/t/realigning-block-building-incentives-and-responsibilities-block-negotiation-layer/16666) intend to improve network security by modifying the Relay mechanism with the proposer’s intent. However, despite the strong demand for protecting validator privacy and even an explicit desire to separate on-chain addresses from IP addresses [[24]](https://ethresear.ch/t/mev-boost-merge-ready-flashbots-architecture/11177), the issue of metadata privacy leaks at the transport layer remains unaddressed, leaving a significant gap in proposer security. In fact, the original MEV Boost architecture explicitly mentioned that “communication between MEV-Boost and relays […] must protect validator privacy by not associating validator key and IP address” [[24]](https://ethresear.ch/t/mev-boost-merge-ready-flashbots-architecture/11177). Yet, no technical solutions were implemented to protect validator privacy.

### 1.3. Randomness generation by validators

Randomness plays an important role in selecting block proposers in Ethereum [[25]](https://eth2book.info/capella/part2/building_blocks/randomness/). The RANDAO value is designed to be unpredictable to the other validators as other validators cannot predict a proposer’s entropy contribution without knowing their private keys. However, a proposer’s contribution to the randomness calculation can be influenced by a malicious proposer choosing between broadcasting or withholding a block [[26]](http://arxiv.org/abs/2409.19883), or by accidentally missed proposals due to network conditions [[27]](https://eips.ethereum.org/EIPS/eip-4399).

But there is a third scenario we would like to highlight: block proposers can be purposefully disrupted by third parties to ensure they miss their proposal slot. This scenario is feasible thanks to the transport-layer privacy leaks outlined above.

### 1.4. Contributions

In our work we i) showcase the feasibility of metadata collection by privileged Relays in a sandbox environment, ii) identify the true trust assumptions surrounding Relays and demonstrate how Relays can de-anonymize validators and conduct attacks without leaving traces, iii) construct a sandbox environment to conduct attacks on the network layer and demonstrate the negative consequences of such attacks on block production, iv) outline attack scenarios on other components, v) discuss possible ways to target these attacks to extract value, as a potential new class of MEV and vi) suggest changes in protocol to prevent and mitigate the effects of these metadata leaks, particularly on solo stakers.

## 2. Methodology

In order to gather metadata from the HTTP calls utilized in MEV-Boost-Relay, we first identified all relevant HTTP calls used by the Relay. After that, we made changes to the Relay source code to allow for metadata collection. We then set up a sandbox Ethereum testnet using the Kurtosis “ethereum-package” from EthPandaOps [[28]](https://ethpandaops.io/posts/kurtosis-deep-dive/) to test the new setup. The sandbox environment[[1]](#footnote-51319-1) includes services such as consensus clients, execution clients, validators, MEV flood simulator, transaction and blob spammer, beacon metrics gazer, beacon explorer, networking tools and containers, and Grafana dashboards. Using the metadata collected from the HTTP calls, as well as additional data about validators, we compiled a dashboard to reveal the identities of validators and to highlight important information that was subsequently used to conduct network attacks within the sandbox environment.

### 2.1. Metadata collection in Relay HTTP calls

Focusing on the most popular MEV-Boost-Relay implementation[[2]](#footnote-51319-2), validators and block builders communicate with Relays via RESTful HTTP APIs [[29]](https://flashbots.notion.site/Relay-API-Documentation-5fb0819366954962bc02e81cb33840f5#854339c909a042d0bbca6e8f8069674e). Specifically, MEV-Boost communicates with the Builder API (Proposer API) [[13](https://ethereum.github.io/builder-specs/), [14](https://github.com/flashbots/mev-boost)], while block builders interact with the Relay API [[15]](https://flashbots.github.io/relay-specs/). The Relay, in turn, communicates with its beacon client through the Beacon API [[30]](https://github.com/ethereum/beacon-APIs). We extended the sequence diagram of MEV-Boost [[14]](https://github.com/flashbots/mev-boost) to provide an overview of HTTP calls within the Relay, as illustrated in Figure 2.

[![Figure 2 Sequence diagram of MEV Relay, extracted from source code flashbots/mev-boost-relay.](https://ethresear.ch/uploads/default/optimized/3X/0/6/06c27e25dff33c837d6e8c19662954850d0a737d_2_640x500.png)Figure 2 Sequence diagram of MEV Relay, extracted from source code flashbots/mev-boost-relay.1080×843 50 KB](https://ethresear.ch/uploads/default/06c27e25dff33c837d6e8c19662954850d0a737d)

***Figure 2** Sequence diagram of MEV Relay, extracted from source code flashbots/mev-boost-relay [[31]](https://github.com/flashbots/mev-boost-relay). See a zoomable version [here](https://kroki.io/mermaid/svg/eNqtVk1v2zAMvfdX6NLD0Ba5B0MPRbHuVBTLsGshy0wsRJY8UU6afz9KllX5K-5huTSlKOqRfI8Mwt8WtIBnyQ-W1zeMPg23TgrZcO2YMBpBY4uTkxpO74Ux6CYnFhS_4Lz5vQBOMSeHhTLi-F60UpVg8Sac_5ZOwZb98vfYDuwJbLDf3kYbOh9BH1jbhINX44AZcosQtt3fzg97r-7s4fHxLke0ZQdwu4sWO8ddTDc_f6ALD33YgSu5YePLtBb9BTSgXA8d_b4c94exx52ooGwVrAbPnWdf-DaMj22BwsoCmDPUsYsyvGTcOTK1DpBxXbIKyAYn0K5LThnTsFc4M1Smo8da3amQ8IcrWXJnLPqn2oa-Aztqc9bslI6G0ZZ6Mwo3SHMFyps1jUGwz62TlN7eWEoxovnS46MAg7dBlz2DM3iBnlMOJ-ltP_MfUTm5EIakR8_6g0QHNr0RnJNDyhuXXAMIKw-VY2afxBRREBNkDQSkbu7Z98JuHgmt3JPM5EGTICxEs6cGUkhgUrPnp5xkvmYZ4BE-Os2S7yv21A2HpXINJ8h29P-ocIGhbwTblFJwpS6ptcNreami7QVc1jvPj7YRpvZjqImtR3aSvJtRY8r5xCdI5wKv8obRhEBQIByQIEmIHfQEYplNZy5dR2xFN7i_n4S6nD4Nglo6UvVTeGaQeP4yV1coVIIwJfEDuZbuwmgOieN1EqGsW8WdNDpjVRwOjppYyPKaFEiQP2k6wRUJDF0CbgX7AWxKk5ZVRnx23ojWmf0-mCIyCsQKOveYMNrCfLRACelYpYpjdbPCiFGt58b0SEEpiaHzZ_8z31jp3pHV3FEjkMFHE9i0fLPjW5dk3AVT6d5lVLsGqy9y5u6bz1wFYaOAvf8s4cEgymYqAn-D-DuhwKg2bxnY2cxkSdvLV6VfcWhaK-Aqa_KgSxulaQslsQp9vMIvr4OkXBqXJXz0suiH7lgYUQMD6vgp53rqVVQ32vHArbpslPe1_sceJoeIrQuxJNqUSWEpV8Gp875BmrZ7uNe1aG9NHex-oCiW_cgbrcq0KYdcnm_X_-Ly0maZeekfwzrOyw).*

Below is a summary of relevant HTTP calls:

Proposer APIs called by mev-boost implemented in the Relay

| Path | Endpoint name |
| --- | --- |
| GET /eth/v1/builder/status | getStatus |
| POST /eth/v1/builder/validators | registerValidator |
| GET /eth/v1/builder/header/{slot}/{parent_hash} | getHeader |
| POST /eth/v1/builder/blinded_blocks | getPayload |
| (equivalent to POST /eth/v1/builder/blinded_blocks | submitBlindedBlock) |

Relay API called by block builders implemented in the Relay

| Path | Endpoint name |
| --- | --- |
| GET /relay/v1/builder/validators | builderGetValidators |
| POST /relay/v1/builder/blocks | submitNewBlock |

Selected BeaconAPIs used by the Relay:

| Path | Endpoint name |
| --- | --- |
| GET /eth/v1/events | subscribeToEvents |
| GET /eth/v1/beacon/states/{state_id}/validators | getStateValidators |
| GET /eth/v1/node/syncing | getSyncStatus |
| GET /eth/v1/validator/duties/proposer/{epoch} | getProposerDuties |
| POST /eth/v1/beacon/blocks | publishBlock |
| POST /eth/v2/beacon/blocks | publishBlock |
| GET /eth/v1/beacon/genesis | getGenesis |
| GET /eth/v1/config/fork_schedule | getForkSchedule |
| GET /eth/v1/beacon/headers | getBeaconHeader |
| GET /eth/v1/beacon/headers/{block_id} | getBeaconHeaderAt |
| GET /eth/v1/config/spec | getSpec |
| GET /eth/v1/beacon/states/{state_id}/randao | getRandao |
| GET eth/v1/beacon/states/{state_id}/withdrawals | getWithdrawals |

Our experiment focuses on extracting metadata, particularly the IP addresses and client types, from the `X-Forwarded-For` and `X-Real-IP` headers within the source code[[3]](#footnote-51319-3).

### 2.2. Attestation data collection

Our team at HOPR previously conducted research on “validator sniping” [[3]](https://medium.com/hoprnet/proof-of-stake-validator-sniping-research-8670c4a88a1c), which involved linking validators’ IP addresses with their public keys collected from validator attestations. In this experiment, we expanded our modifications to beacon clients to include aggregated attestations as an additional data source for inferring the most likely IP address of a validator.

We calculated the percentage of occurrences for each validator’s public key and peer ID pair. For each validator public key, we identified the pair with the highest occurrence percentage as the most probable match. This allowed us to link the validator’s IP address with their public key.

Each consensus client may serve multiple validators. To locate a validator with their consensus client’s public-facing IP address, we first established the link between validators’ public keys and the peer ID used in the networking layer of consensus clients from collected attestations. We then listed the percentage of occurrences of a certain peer ID paired with a specific pub key from received attestations, and. We calculated the percentage of occurrences for each validator’s public key and peer ID pair. For each validator public key, we identified the pair with the highest occurrence percentage as the most probable match. We further associated the obtained public key and peer ID pairs with nodes’ multi-addresses, as the link between peer ID and multi-addresses is created when establishing connections in the libp2p protocol.

### 2.3. De-anonymization

We started by matching the IP addresses we gathered from HTTP calls with the public keys that validators provided during the registerValidator call. This helped us connect validator public keys with their corresponding MEV-Boost IP address.

Next, we used validator attestations to link the most likely validator public key with their Beacon Client IP address.

Finally, by combining these connections, we were able to acquire both the MEV-Boost and Beacon Client (or consensus client) IP addresses for each validator. With this information, we could estimate the location of a validator, as these processes necessitate low latency and are therefore likely to be situated in close geographic proximity.

### 2.4. Simulation of network attacks

To conduct production-level network attacks on production servers in the real world, a significant amount of resources is required. We have simplified the test to demonstrate the technical viability of network attacks. As more than 90% of denial of service (DoS) attacks use TCP and TCP SYN flooding is the most commonly used attack [[32]](https://doi.org/10.1109/INFCOM.2002.1019404), we started the network attacks with a raw ICMP and TCP flood. We used the “syn_flood” service to simulate a network adversary, sending out an ICMP ping flood and TCP SYN flood using ‘iputils-ping’ and ‘hping3’ respectively to beacon client, validator clients, and mev-boost instances. To analyze the impact on memory and network performance, the changes were inspected using the Kubernetes dashboard, as shown in Figure 4 and onwards.

For a more efficient simulation of network attacks, the Attacknet [[33]](https://github.com/crytic/attacknet) developed by Trail of Bits was utilized to execute memory attacks, bandwidth attacks, and clock skew attacks.

## 3. Setup and environment

The simulation environment is an Ethereum testnet in a sandbox based on the Kurtosis Ethereum package developed by EthPandaOps. It has been modified for specific data collection and analysis purposes. Key modifications are given in the architecture breakdown. The source code can be found at hoprnet/metaclear-ethereum-package[[4]](#footnote-51319-4).

### 3.1. Architecture

We modified the implementation of various components used in MEV-Boost to collect relevant data and metadata, as highlighted in yellow in Figure 3.

[![Figure 3 Testing architecture, adapted from MEV-Boost Relay architecture diagram 34](https://ethresear.ch/uploads/default/optimized/3X/4/4/442ec3279ca2ec69e1fd48edefe0c2a5a57b8464_2_690x388.png)Figure 3 Testing architecture, adapted from MEV-Boost Relay architecture diagram 34960×540 63.6 KB](https://ethresear.ch/uploads/default/442ec3279ca2ec69e1fd48edefe0c2a5a57b8464)

***Figure 3** Testing architecture, adapted from MEV-Boost Relay architecture diagram [[34]](https://flashbots.notion.site/Running-MEV-Boost-Relay-at-scale-4040ccd5186c425d9a860cbb29bbfe09). The system (circled in dark blue) is divided into three main sections: Proposer, Relay, and Block Builders. Components highlighted in yellow indicate the “metaclear-” forked versions of the original implementation, where modifications have been introduced to collect data and metadata. Components filled with blue are services for testing system behaviors under network attacks.*

**Proposer Section:**

- Beacon Node: Lighthouse client that manages consensus and coordinates the actions of validators. Here it has been enhanced with “metaclear” modifications to extract public keys from attestation and aggregated attestations, as well as the mapping of public keys and multi-address from the networking layer. The docker image that it runs is `hoprnet/metaclear-lighthouse`[5].
- MEV-Boost: A middleware used by validators to interact with the MEV-Boost marketplace.
- Execution Node: Geth client running `ethereum/client-go:latest`, which is the execution environment where transactions are processed.
- Validators: 64 validators per proposer instance. It manages the duties of an Eth2.0 validator, including proposing and attesting to blocks.

**Relay Section:**

- Services: The main service of the metaclear MEV-Boost Relay is where HTTP calls are handled. The single instance of housekeeper coordinates sync between beacon, db, and APIs. The website displays data from the datastore. The major modifications are as follows.

API: Handles all the external facing calls of proposer APIs and block builder APIs. Metadata is collected from the HTTP headers.
- Housekeeper: As it updates known validators and proposer duties, it’s modified to store those data persistently.

Clients: A local beacon and an execution client to gain knowledge on validator activity and simulate blocks submitted from block builders. It uses the same modified image as nodes in the Prosper sections.
Data store: Data management component of the metaclear MEV-Boost Relay. It consists of an in-memory cache, Redis, and Postgres database. Here below are the major modifications.

- Postgres: Two new tables are created to collect HTTP header metadata, proposer duties, and RANDO values.

**Block Builders Section:**

- Block builder (MEV-Flood): Deploys mock Uniswap contracts and builds bundles on those mock Uniswap transactions. These entities are responsible for constructing blocks that are optimized for MEV extraction. In this architecture, one block builder instance is shown interacting with the Relay. The “flashbots/mev-flood” package is used to create mock MEV bundles.

**Network tools:**

- Syn_flood: A dedicated service used to SYN flood targets, where it runs a containerized `hping3` TCP/IP packet assembler.
- Tools such as `iputils-ping` and `tcpdump` are installed in the services, along with beacon client instances and mev-boost instances.
- AttackNet and Chaos-mesh: Tools used for injecting faults and simulating network attacks on the system. We created three types of test suites[6]: “memory-stress” for memory exhaustion, “network-bandwidth” for saturated bandwidth, and “clock-skew” for synchronization disruption.

### 3.2. Environment and test parameters

All the images are run in minikube with docker as VM driver

- Minikube v1.33.1 on Darwin 14.6.1 (arm64) with memory of 4GB
- Kubernetes v1.30.0 on Docker 26.1.1
- Kurtosis engine 1.1.0

MEV flood generates bundles every 15 seconds. The interval between slots is reduced to 6 seconds from the standard 12s for faster testing. The number of consensus layer (CL) clients varies between 2 to 3 in different testing scenarios. Each CL instance contains 64 validator public keys.

In the TCP SYN flood, 15000 packets are sent from random IP sources to the observed IP address and port. In the memory stress chaos test, the test plan has three scenarios, targeting one validator client (“vc-1-geth-lighthouse”), one mev-boost instance (“mev-boost-2-lighthouse-geth”), and one beacon client (“cl-3-lighthouse-geth”). Each belongs to a different beacon instance. For each scenario, 50 workers stress 10 MB/worker for a total of 10 minutes.

## 4. Results

We compiled a Grafana dashboard to collect and visualize metrics from the metaclear experiment and visualize how a malicious Relay could identify validators with attestations from beacon clients and metadata from HTTP requests.

### 4.1. Linking public key and IP addresses of validators

Public keys of validators can be linked with their IP addresses from two datastreams. One datastream is validator attestation. The link between validator public key to their consensus layer (CL) client peer IDs can be probabilistically established by observing aggregated and non-aggregated attestations, as shown in Figure 4(b). As peer IDs in CL can be translated into multiaddress and thus IP addresses, as shown in Figure 4(a), links between validator public keys with IP addresses can be obtained via CL peer IDs, as in Figure 4(c).

[![Figure 4a) displays information from an unmodified Lighthouse implementation, including the link between peer ID and IP address, the current beacon epoch, and the current head slot.](https://ethresear.ch/uploads/default/optimized/3X/b/c/bced7b1320231fc0916d3d6224dd817b7fc51674_2_690x222.jpeg)Figure 4a) displays information from an unmodified Lighthouse implementation, including the link between peer ID and IP address, the current beacon epoch, and the current head slot.1920×620 57.3 KB](https://ethresear.ch/uploads/default/bced7b1320231fc0916d3d6224dd817b7fc51674)

[![Figure 4b) features a table that calculates the correlation between public keys and peer IDs derived from attestations. Higher percentages in this table indicate a stronger probability of the peer ID being associated with the corresponding public key.](https://ethresear.ch/uploads/default/optimized/3X/2/4/24afebff2692297daa070d33cd2d059d3198a0b0_2_690x448.jpeg)Figure 4b) features a table that calculates the correlation between public keys and peer IDs derived from attestations. Higher percentages in this table indicate a stronger probability of the peer ID being associated with the corresponding public key.1920×1249 219 KB](https://ethresear.ch/uploads/default/24afebff2692297daa070d33cd2d059d3198a0b0)

[![Figure 4c) uses the most probable associations between public keys and peer IDs to establish a mapping between the public key and the IP address of the validators' consensus layer (CL) client.](https://ethresear.ch/uploads/default/optimized/3X/5/f/5f90b02eefc47810aa54e63130bf9e9cd3781580_2_690x267.jpeg)Figure 4c) uses the most probable associations between public keys and peer IDs to establish a mapping between the public key and the IP address of the validators' consensus layer (CL) client.1920×744 111 KB](https://ethresear.ch/uploads/default/5f90b02eefc47810aa54e63130bf9e9cd3781580)

***Figure 4** Grafana dashboard for MEV-Boost-Relay and their beacon nodes, labelled as a), b), and c) from top to bottom. Figure 4a) displays information from an unmodified Lighthouse implementation, including the link between peer ID and IP address, the current beacon epoch, and the current head slot. Figure 4b) features a table that calculates the correlation between public keys and peer IDs derived from attestations. Higher percentages in this table indicate a stronger probability of the peer ID being associated with the corresponding public key. Figure 4c) uses the most probable associations between public keys and peer IDs to establish a mapping between the public key and the IP address of the validators’ consensus layer (CL) client.*

The other datastream is the HTTP API calls requested to MEV Relays.

Figure 5 shows the Metaclear Relay dashboard, which displays how the MEV-Boost Relay can track the IP address of mev-boost instances of validators through the ‘registerValidator’ HTTP call, which occurs at the outset of launching the mev-boost instance. It’s important to note that multiple relays can be assigned to mev-boost, allowing the IP address to be shared with all the provided MEV-Boost Relays.

Additionally, it monitors the frequency (per second) of each HTTP call to detect the submission pattern of block builders. The green line, representing the ‘POST /eth/v1/builder/blinded_blocks’ endpoint, reflects the rate of block builders delivering blocks. Moreover, the MEV-Boost Relay gathers the IP addresses of block builders.

[![Figure 5 Metaclear Relay dashboard displays the association between the validator’s public key, their peer ID, and the IP:port of their mev-boost instance at the launch of the mev-boost.](https://ethresear.ch/uploads/default/optimized/3X/2/6/265c87a1d4dc52b8948f0d0556840c6a83195fd0_2_690x297.jpeg)Figure 5 Metaclear Relay dashboard displays the association between the validator’s public key, their peer ID, and the IP:port of their mev-boost instance at the launch of the mev-boost.1600×689 179 KB](https://ethresear.ch/uploads/default/265c87a1d4dc52b8948f0d0556840c6a83195fd0)

***Figure 5** Metaclear Relay dashboard displays the association between the validator’s public key, their peer ID, and the IP:port of their mev-boost instance at the launch of the mev-boost. It also monitors the rate (per second, average over 1 minute) of each HTTP call to identify the submission pattern of block builders.*

### 4.2. Identifying victim validators

The Metaclear Relay dashboard also extracts the proposers of the next epoch, as shown in Figure 6. As proposers are unique once selected for a slot in a given epoch, they are the most obvious choice of victims for network-layer attacks after being deanonymized. However, we will outline possible attacks on other parties in the network later. Those proposers are computed by RANDAO [[25]](https://eth2book.info/capella/part2/building_blocks/randomness/).

[![Figure 6 Metaclear Relay dashboard displays validators selected as proposers of the next epoch](https://ethresear.ch/uploads/default/optimized/3X/2/e/2e6e743461c5aa1039422f2bef6668a33e3371f2_2_690x314.jpeg)Figure 6 Metaclear Relay dashboard displays validators selected as proposers of the next epoch1920×876 170 KB](https://ethresear.ch/uploads/default/2e6e743461c5aa1039422f2bef6668a33e3371f2)

***Figure 6** Metaclear Relay dashboard displays validators selected as proposers of the next epoch and historical RANDAO values.*

### 4.3. Viable network attacks

We conducted a memory stress attack on three different clients around 15:13 one validator client (“vc-1-geth-lighthouse”), one mev-boost instance (“mev-boost-2-lighthouse-geth”), and one beacon client (“cl-3-lighthouse-geth”), each belonging to a different beacon instance as shown in Figure 7.

The attack caused the respective clients to become overwhelmed. As a result, the validator client and the beacon client stopped producing blocks and processing slots. As shown in Figure 7, the block production metric came to a halt for client number 3 (green line in Figure 7), where the consensus client was under attack. Block production stopped for client number 1 (blue line in Figure 7), where the validator stopped functioning. Block production continued as usual for client number 2 (yellow line in Figure 7), where mev-boost was under attack. However, blocks were produced only locally but not from mev-boost, as shown in Figure 8.

[![Figure 7 Number of successfully produced blocks around the time of the attack.](https://ethresear.ch/uploads/default/optimized/3X/b/8/b889772db4e922230d02b5c3ff9c5f1b2192534b_2_690x396.png)Figure 7 Number of successfully produced blocks around the time of the attack.1574×904 53.3 KB](https://ethresear.ch/uploads/default/b889772db4e922230d02b5c3ff9c5f1b2192534b)

***Figure 7** Number of successfully produced blocks around the time of the attack. Instances number 1 (blue) and 3 (green), where the validator client and beacon client were under attack respectively, stopped producing slots.  Instance number 2 (yellow), where the mev-boost was under attack, could still produce blocks locally.*

Figure 8 shows the number of blocks constructed by the block builder instance and subsequently sent to proposers via the metaclear Relay instance. After the attack (after the dotted line), no blocks were delivered through the relay. This is due to instances 1 and 3 being unable to fulfill their proposer duties. Even though instance 2 was still able to propose blocks, they could not be proposed via the Relay because its MEV-boost functionality was not operational.

[![Figure 8* Rate per minute of slots containing blocks built by the block builder and delivered to proposers via meta-clear Relay.](https://ethresear.ch/uploads/default/optimized/3X/5/4/544b07dc01aac7bfc5d8feb6a3bcbb9e711ba661_2_690x322.png)Figure 8* Rate per minute of slots containing blocks built by the block builder and delivered to proposers via meta-clear Relay.1600×748 92.3 KB](https://ethresear.ch/uploads/default/544b07dc01aac7bfc5d8feb6a3bcbb9e711ba661)

***Figure 8** Rate per minute of slots containing blocks built by the block builder and delivered to proposers via meta-clear Relay.*

By observing the HTTP endpoint request rate in Figure 9, it is clear that block builders kept posting blocks to the Relay (continuous red and orange lines). However, the request rate of other endpoints (other lines) dropped to 0, indicating they were not called.

[![Figure 9 Metaclear-Relay HTTP endpoint request rate (per minute) around the attack time](https://ethresear.ch/uploads/default/optimized/3X/a/5/a589596cf251feca4cef8a6cca127d71f3a674f0_2_690x408.png)Figure 9 Metaclear-Relay HTTP endpoint request rate (per minute) around the attack time1600×948 190 KB](https://ethresear.ch/uploads/default/a589596cf251feca4cef8a6cca127d71f3a674f0)

***Figure 9** Metaclear-Relay HTTP endpoint request rate (per minute) around the attack time*

The block explorer gives us a more intuitive overview of slot production status, as seen in Figure 10. All slots were successfully proposed before the attack. After the attack, the only block proposer was client number 2, while clients 1 and 3 missed their slots.

[![Figure 10 Explorer of block production before (left) and after (right) the attack.](https://ethresear.ch/uploads/default/optimized/3X/4/2/426d035252b87d4abd3e38bdfe6e2a6dfa8a70d5_2_690x410.jpeg)Figure 10 Explorer of block production before (left) and after (right) the attack.1920×1141 176 KB](https://ethresear.ch/uploads/default/426d035252b87d4abd3e38bdfe6e2a6dfa8a70d5)

***Figure 10** Explorer of block production before (left) and after (right) the attack.*

## 5. Discussion: Further Attack scenarios and Network Consequences

Our Metaclear experiment focused on demonstrating the practicality of identifying and disrupting block proposers using leaked metadata. However, it is feasible that similar approaches to deanonymizing actors in the network could enable other attacks against other actors, including the Relay itself. The following sections outline briefly how the same metadata could be used to probabilistically identify the roles of different nodes and the kinds of attacks which could be conducted as a result, along with possible broader consequences for the entire network.

### 5.1. Network topology can be mapped using Relay metadata

The MEV-Boost Relay has access to ample metadata to provide an advantage in mapping the network topological and geographical distribution of validators and builders. Validators rely on MEV-Boost instances to produce blocks with higher returns. This incentivizes the deployment of mev-boost and beacon nodes in a network configuration that reduces latency, likely in the same geographical area. By cross-checking the IP addresses of mev-boost collected from ‘registerValidator’ calls with the beacon IP addresses correlated from observing attestations, the MEV-Boost Relay can map out the topology and location of validators more reliably.

By grouping validators by IP addresses, Relayers can use IP ranges to infer the network topology. For example, home stakers can be identified by residential IP addresses and they would likely experience higher latency due to multiple network layers before reaching the device. Cloud-hosted validators can easily be identified by finding providers from IP address registries. Staking pools generally exhibit a dense concentration of validators per IP address, which implies that they apply some network security rules similar to other nodes in the same pool. These are just some of the examples of inferences which might be drawn, with differing levels of confidence. Determining the nature of a particular validator’s hardware and relationship to other validators opens up the possibility of more nuanced targeted attacks.

### 5.2. Solo stakers are more vulnerable to attack

For reasons of security, decentralization and fairness, it is generally considered desirable for solo stakers to comprise a significant proportion of validators [[35]](https://cointelegraph.com/news/vitalik-buterin-advocates-lowering-solo-staking-eth), although there is debate about the extent to which stakers with less powerful hardware should be supported. However, even well-equipped solo stakers are disproportionately vulnerable to the attacks outlined in our research. They are generally easier to identify [[36]](https://blog.rated.network/blog/solo-stakers), easier to attack, and would be less likely to notice that they have been attacked.

Solo stakers and home stakers generally do not have ample resources for Distributed Denial of Service (DDoS) protection, such as alternative fallback IP addresses. Due to the usage of consumer-grade hardware, physical limitations on memory and computation power, as well as the bandwidth on the router and switches, solo stakers are more exposed to DDoS attacks. Additionally, DDoS attacks against a single home staker can be targeted extremely well; the attack only needs to be effective for a few seconds to cause a slot to be missed, making such attacks cheap to execute and hard to detect. Attackers can identify solo stakers via attestations alone, but the extra data collected from Relayer would make the validator de-anonymization more efficient.

Since a DDoS attack can mimic the effects of other non-malicious errors, it is not always possible to identify when an attack has occurred. Solo stakers propose fewer blocks than other classes of proposer, and are much less likely to have robust hardware setups. Therefore, it will be harder for them to gather data to prove an attack, and they may be more likely to ascribe other causes such as a faulty setup or poor connection.

Attacking solo validators during block proposals can provide significant advantages to professional validators. These entities typically have the resources and expertise to carry out such attacks efficiently and profitably, aiming to repeatedly disrupt the reward-earning potential of solo stakers. Over time, this strategy can force solo validators to leave the network after repeatedly failing to produce blocks, allowing professional validators to capture a larger market share and exert greater control over block production.

The disproportionate effects of these attacks on solo stakers could harm attempts to encourage them to join and remain in the network.

### 5.3. RANDAO can be exploited and manipulated

RANDAO is the random number generator used by Ethereum in various parts of its consensus mechanism, including determining which validators will be selected to propose upcoming blocks. RANDAO values generated in a particular epoch are used to assign duties in two epochs’ time, allowing chosen validators enough time to prepare for their roles. This delay presents an opportunity for malicious actors, however: by observing when a victim is selected as proposer by the RANDAO, the attacker has a time advantage of one epoch to prepare a DDoS attack (although this will change if secret leader elections are implemented) [[37]](https://ethereum.org/en/roadmap/secret-leader-election/).

But it is possible to more actively interfere with RANDAO to manipulate future outcomes. Missing a slot, either deliberately or through unresponsiveness or delay, does not introduce entropy in the next RANDAO calculation and thus gains potentially multiple slots for free without increasing its stake fraction. Researchers have already identified the possibility of choosing to forego block rewards in exchange for generating a favourable RANDAO result in two epochs’ time [[38]](https://ethresear.ch/t/selfish-mixing-and-randao-manipulation/16081). Our research suggests a further possibility: proposers could be deliberately targeted by competing proposers to miss their block in order to achieve the same result.

This could be part of a single attack to benefit from a known high-value upcoming event in a particular epoch, or part of a more concerted effort to accelerate the k-tailed RANDAO takeover [[26](http://arxiv.org/abs/2409.19883), [36](https://blog.rated.network/blog/solo-stakers)].

### 5.4. Blobs can be disrupted

By occupying network bandwidth, a validator may fail to send their attestation to data availability sampling (DAS) in time, which affects the result of attestation on blob data [[39]](https://ethresear.ch/t/das-fork-choice/19578). Additionally, a node could selectively respond to sampling requests while selectively providing malicious responses to data requests by other nodes. This could be made feasible by identifying nodes uniquely based on their IP address as outlined above.

### 5.5. Recently bootstrapped, sparsely connected beacon nodes are more vulnerable to “covert flash attacks”

The higher the number of validators per beacon node, and the more sparse that beacon’s connections to the rest of the network, the more vulnerable it is to a “covert flash attack” [[40]](https://arxiv.org/abs/2007.02754). A covert flash attack happens when the sybils of an attacker connect to the victim and behave properly long enough to build up scores in GossipSub protocol before executing a coordinated eclipse attack when the victim needs to propose a block. Such a covert flash attack executed at the time when a validator proposes a block could be considered a new type of MEV, if as a result the attacker is able to extract the value which the attacked proposer would have otherwise claimed for themselves.

### 5.6. Selectively attack multi-block MEV

Even in the narrow definition, MEV is not always confined to individual blocks. It is possible to extract MEV across multiple neighbouring blocks, known as multi-block MEV (MMEV), by having two or more consecutive block proposers collude and jointly create blocks in a row [[41]](https://doi.org/10.1109/ICBC54727.2022.9805499). This is already known to be a high risk MEV tactic, but the disruptive attacks shown in our research increase this risk further. If a block proposer comes under attack and cannot produce the block at a given slot, this missing block will affect the MMEV, often with significant losses. For example, several proposers might collude to extract MMEV by manipulating on-chain time-weighted average price (TWAP) oracles. If a colluding proposer is attacked and fails to produce the promised block, the TWAP will not be manipulated, not only losing the MMEV but potentially resulting in a significant loss for MEV searchers. In an advanced attack scenario, the attacker would control the slot immediately after the targeted proposer. In this case, the attacker would be able to place a backrun order to exploit the original MMEV searcher.

Alternatively, MMEV could be de-risked by taking out other proposers. If, for example, a large validator controls slots 5 and 8 in an epoch, they could disrupt the nodes of proposers responsible for slots 6 and 7 in order to launch a multi block MEV strategy. This is especially viable if the proposers of slots 6 and 7 have been identified as home stakers which can likely be taken out successfully by cheap and highly targeted attacks.

### 5.7. Malicious Relay can more easily conduct a metadata-based attack without leaving traces

Despite Relays being monitored on the reliability of block delivery, there is no measure in place to prevent them from leaking metadata on validators. When such metadata leaks are exploited by network attacks to kick out block proposers, they leave no definitive trace that would incriminate them. As outlined above, in operation, validators, especially solo stakers who get to produce blocks at a lower frequency than professional node operators, cannot differentiate a purposeful attack from poor network conditions.

### 5.8. Decentralizing Relays makes attacks more likely, not less

It can be tempting to view issues like the ones outlined in this research as “teething troubles” which will be resolved once the network becomes more decentralized. But decentralization is unlikely to resolve the issue of high trust assumptions in Relays. In fact, it may make it worse: although validators may want to connect to multiple relays for more bids from more block builders and/or more reliable receipt of externally built blocks, connecting to multiple relays would leak their metadata to more parties in the network, each a potential attacker. It would also make it even harder to identify who the attacker was.

### 5.9. Valuable metadata can make Relay a victim

Much of the foregoing has focused on an untrustworthy Relay as an attacker, but Relays themselves are also exposed to attack. As a result of reducing latency, Relay, e.g. ultrasound relay, actively disabled Cloudflare service to gain 10 ms of latency advantage [[42]](https://www.youtube.com/watch?v=fWRboyGk_lc); although it eliminates the time for round-trip traffic routing in Cloudflare’s network, it also exposes Relay to DDoS attacks. As the validator registration information is publicly available via the Relay’s Data API, attackers can scrape the latest registration data via public endpoints to obtain all the relays that a given validator connects to. Attackers can then prepare DDoS attacks on a validator that will soon become a block proposer, with a maximum of one epoch time ahead. Ideally, this validator only connects to one Relay, so that the target for a DDoS attack is minimal. When Relay fails to deliver a block in time, the victim proposer would need to build a block using only the local mempool and thus lose their MEV profit.

It would be even more beneficial for attackers to attack Relay in the window right after the proposer broadcasts the signed header but before the payload gets published. This would not only damage the reputation of the proposer but also push down the stable operation rate of Relay, gradually making block builders and validators abandon their service. If the attacker happened to be a competitor of Relay, they might attract alienated validators to their service, increasing revenues and getting access to even more valuable metadata.

### 5.10. Builders can be made to underperform

Last but not least, block builders also expose their IP addresses to Relays. A malicious attacker could target builders connected to profitable searchers, in the hope that those searchers would move from the now underperforming builders to other block builders.

### 5.11.  A new class of MEV?

Although the standard definition of MEV restricts itself to actions taken when constructing blocks, we would argue that many of the targeted attacks shown to be possible via this research also qualify as MEV. Metadata can be used to deanonymize other players in the cutthroat MEV game, identify their role in the network and target them with disrupt DDoS attacks which prevent them from extracting MEV they would otherwise expect. In addition to harming competitors, attackers can take advantage of favourable slot ordering to claim this MEV for themselves. Particularly resourceful (in every sense of the words) attackers could even manipulate RANDAO to engineer these favourable slot positions, rather than waiting for circumstances to align.

One key difference: the fairness and ethics of MEV extraction as usually defined is subject to much debate. However, the attacks identified in our research seem unambiguously negative for the health and security of the network. Smooth and reliable block production is a fundamental part of blockchain utility. Incentives to disrupt the block production process and even manipulate RANDAO generation can only be bad for all parties in the long run.

Not all of these attacks seem equally feasible or likely, and this is far from an exhaustive list of possible disruptive actions, but we hope this illustrates the broader point that failures in transport level metadata privacy leave all parties exposed. Even more concerning, many of these attacks can be carried out with no evidence of who the perpetrator is.

In general, all parties engaged in capturing MEV under the standard definition benefit from minimizing latency in the MEV pipeline [[43]](https://frontier.tech/exploration-of-mev-latencies). Some argue that the co-location of builders with relay and relay with validators may become a driver for a more distributed MEV infrastructure [[42]](https://www.youtube.com/watch?v=fWRboyGk_lc). However, a distributed MEV infrastructure does not necessarily translate into a more distributed Ethereum network, hence there’s no direct contribution to a more robust Ethereum network. Due to the risk of leaking metadata privacy, bootstrapping a rather isolated node makes it susceptible to networking-level attacks before it establishes a stable and truthful connection with the rest of the Ethereum network. Therefore, protecting metadata privacy is particularly important to a more distributed Ethereum network with more sparsely-connected nodes.

To mitigate these risks, a promising approach involves integrating network-level metadata privacy protection protocols directly into the networking layer of Ethereum clients when designing PBS specifications. An effective protocol should be easily integrable with the Ethereum protocol, provide out-of-the-box transport layer anonymity for REST-JSON Builder API calls, maintain low latency to ensure that necessary communications can be completed within a slot time, and avoid any centralized points of failure that could become vulnerabilities for privacy leaks. Additionally, generalizing Ethereum’s peer-to-peer networking protocols to support an overlay of metadata-private protocols, such as a mixnet, would further enhance privacy protections across the network. These solutions are already viable and could be implemented to significantly bolster the security of Ethereum’s infrastructure against potential MEV exploits.

Privacy-critical API calls such as `registerValidators` are one-time requests which are not time-critical. Using metadata-private protocols to protect such API calls are given. However, protecting one single endpoint does not prevent metadata leaks because the link between validator public keys and IP addresses can be derived from other endpoints. Partial protection is no protection.

Granted that any overhead on the p2p networking layer would introduce additional latency, which is generally undesirable in MEV games, networking-level privacy protection makes the (re-)distribution of MEV fairer and enhances the resilience of the entire network by protecting solo stakers from network attacks.

While the community seems to be focusing on faster commitment, i.e., single slot finality, single slot secret leader election, should we leave some space for a fair and secure environment for solo stakers and home stakers, and consider a reasonably longer slot time and eventually a longer epoch time, such that large majority of transactions can still be gossiped through the network, even from one sparsely connected node to another sparsely connected node. When there’s sufficient time for transactions to be propagated across the network, the speed of propagation becomes less important as the information asymmetry eventually gets canceled out.

## 6. Limitations

While the “Metaclear” experiment effectively demonstrates the potential for network disruption and potential new kinds of MEV extraction through metadata analysis, it has limitations. The simulated memory exhaustion attack is not practically feasible in most real-world deployments due to robust resource allocations. Attacks such as botnet-driven DDoS could achieve the same or better results, but these are hard to test ethically. Such botnets are readily available and inexpensive at a cost of 200$/day [[44]](https://www.statista.com/statistics/1350155/selling-price-malware-ddos-attacks-dark-web/), which could make MEV extraction highly profitable: based on the average profit of 0.025 ETH/block at time of writing, up to $450,000 a day of value in total MEV is available.

Additionally, technical challenges prevented the simulation of network bandwidth and clock skew attacks, which are also known to exacerbate privacy leaks and disrupt block production. Despite these constraints, “Metaclear” highlights significant risks and underscores the need for stronger countermeasures.

## 7. Future research

Our current version of Metaclear ran in a contained environment with a limited number of proposers, relays, and block builders. We also assumed that validators had participated in the network for long periods and had gathered sufficient data to derive networking information on other parties.

We would like to extend the experiment to:

- Run in a more realistic environment
- Explore the possibilities for attacks when parties are more distributed yet still co-located and hold more computational resources.
- Build a Proof-of-Concept (PoC) that integrates network-level metadata privacy protection protocol solutions like uHTTP [45].
- Carry out experiments of network bandwidth attack when validators send attestations to blob in data availability sampling (DAS).

We also hope to further explore questions such as:

- How effectively can we de-anonymize validators and builders in the real world?
- How much additional latency can the MEV-Boost design tolerate while remaining fair?
- How do we quantify the fairness of the distributed Ethereum network?
- Are the attacks we have identified a new class of MEV, an extension of existing MEV, or something else?
- How large an anonymity set can be obtained when applying network-level metadata privacy protection protocol solutions like uHTTP [45]?

## Bibliography

[1]	“Maximal extractable value (MEV) | [ethereum.org](http://ethereum.org).” Accessed: Oct. 09, 2024. [Online]. Available: [Maximal extractable value (MEV) | ethereum.org](https://ethereum.org/en/developers/docs/mev/)

[2]	G. Damalas and P. Ambrus, “An introduction to maximal extractable value on Ethereum,” Mar. 2023. [Online]. Available: [https://assets.ey.com/content/dam/ey-sites/ey-com/en\_us/topics/financial-services/ey-an-introduction-to-maximal-extractable-value-on-ethereum.pdf](https://assets.ey.com/content/dam/ey-sites/ey-com/en%5C_us/topics/financial-services/ey-an-introduction-to-maximal-extractable-value-on-ethereum.pdf)

[3]	S. Bürgel and L. Pohanka, “Proof-of-Stake Validator Sniping Research,” HOPR. [Online]. Available: https://medium.com/hoprnet/proof-of-stake-validator-sniping-research-8670c4a88a1c

[4]	L. Heimbach, Y. Vonlanthen, J. Villacis, L. Kiffer, and R. Wattenhofer, “Deanonymizing Ethereum Validators: The P2P Network Has a Privacy Issue,” Sep. 06, 2024, *arXiv*: arXiv:2409.04366. doi: 10.48550/arXiv.2409.04366.

[5]	Ethereum Foundation, “Ethereum Roadmap: PBS and MEV,” [ethereum.org](http://ethereum.org). [Online]. Available: [Proposer-builder separation | ethereum.org](https://ethereum.org/en/roadmap/pbs/)

[6]	V. Buterin, “Proposer/block builder separation-friendly fee market designs - Economics,” Ethereum Research. [Online]. Available: [Proposer/block builder separation-friendly fee market designs](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725)

[7]	V. Buterin, “Two-slot proposer/builder separation - Proof-of-Stake,” Ethereum Research. [Online]. Available: [Two-slot proposer/builder separation](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980)

[8]	V. Buterin, “Single-slot PBS using attesters as distributed availability oracle - Proof-of-Stake,” Ethereum Research. [Online]. Available: [Single-slot PBS using attesters as distributed availability oracle](https://ethresear.ch/t/single-slot-pbs-using-attesters-as-distributed-availability-oracle/11877)

[9]	B. Monnot, “Unbundling PBS: Towards protocol-enforced proposer commitments (PEPC) - Economics,” Ethereum Research. [Online]. Available: [Unbundling PBS: Towards protocol-enforced proposer commitments (PEPC)](https://ethresear.ch/t/unbundling-pbs-towards-protocol-enforced-proposer-commitments-pepc/13879)

[10]	M. Neuder, “Payload-timeliness committee (PTC) – an ePBS design - Proof-of-Stake,” Ethereum Research. [Online]. Available: [Payload-timeliness committee (PTC) – an ePBS design](https://ethresear.ch/t/payload-timeliness-committee-ptc-an-epbs-design/16054)

[11]	T. Wahrstätter, “MEV-Boost Dashboard,” mevboost.pics. [Online]. Available: https://mevboost.pics/mevboost.pics

[12]	Flashbots Ltd, “MEV-Boost in a Nutshell,” MEV-Boost in a Nutshell. [Online]. Available: https://boost.flashbots.net/

[13]	Ethereum Foundation, “Builder-API.” [Online]. Available: [Builder-API](https://ethereum.github.io/builder-specs/)

[14]	*Flashbot/MEV-Boost*. Go. Flashbots. [Online]. Available: [GitHub - flashbots/mev-boost: MEV-Boost allows Ethereum validators to source high-MEV blocks from a competitive builder marketplace](https://github.com/flashbots/mev-boost)

[15]	Flashbots Ltd, “Relay-API.” [Online]. Available: [Relay-API](https://flashbots.github.io/relay-specs/)

[16]	M. Neuder, “Relays in a post-ePBS world - Proof-of-Stake,” Ethereum Research. [Online]. Available: [Relays in a post-ePBS world](https://ethresear.ch/t/relays-in-a-post-epbs-world/16278)

[17]	C. Hager, “Post-mortem for a relay vulnerability leading to proposers falling back to local block production (Nov. 10, 2022) - Relays,” Nov. 2022. [Online]. Available: [Post-mortem for a relay vulnerability leading to proposers falling back to local block production (Nov. 10, 2022) - Relays - The Flashbots Collective](https://collective.flashbots.net/t/post-mortem-for-a-relay-vulnerability-leading-to-proposers-falling-back-to-local-block-production-nov-10-2022/727)

[18]	lotusbumi, “MEV-Boost Security Assessment (audit),” Jun. 2022. [Online]. Available: [mev-boost/docs/audit-20220620.md at 4035cb3c8c8f9b0118a0170049203f0167c604a0 · flashbots/mev-boost · GitHub](https://github.com/flashbots/mev-boost/blob/4035cb3c8c8f9b0118a0170049203f0167c604a0/docs/audit-20220620.md)

[19]	R. Miller, “Post mortem: April 3rd, 2023 mev-boost relay incident and related timing issue - The Flashbots Ship,” Apr. 2023. [Online]. Available: [Post mortem: April 3rd, 2023 mev-boost relay incident and related timing issue - The Flashbots Ship - The Flashbots Collective](https://collective.flashbots.net/t/post-mortem-april-3rd-2023-mev-boost-relay-incident-and-related-timing-issue/1540)

[20]	M. Sproul, “Unbundling attacks on MEV relays using RPC,” 12:00:00+10:00. [Online]. Available: [Unbundling attacks on MEV relays using RPC](https://blog.sigmaprime.io/mev-unbundling-rpc.html)

[21]	G. D. Bissias, M. Liberatore, D. Jensen, and B. N. Levine, “Privacy Vulnerabilities in Encrypted HTTP Streams,” in *Privacy Enhancing Technologies*, G. Danezis and D. Martin, Eds., Berlin, Heidelberg: Springer, 2006, pp. 1–11. doi: 10.1007/11767831_1.

[22]	F. D. Smith, F. H. Campos, K. Jeffay, and D. Ott, “What TCP/IP Protocol Headers Can Tell Us About the Web,” *ACM SIGMETRICS Perform. Eval. Rev.*, vol. 29, no. 1, pp. 245–256, Jun. 2001, doi: 384268.378789.

[23]	Ł. Miłkowski, “Realigning block building incentives and responsibilities - Block Negotiation Layer - Proof-of-Stake / Block proposer,” Ethereum Research. [Online]. Available: [Realigning block building incentives and responsibilities - Block Negotiation Layer](https://ethresear.ch/t/realigning-block-building-incentives-and-responsibilities-block-negotiation-layer/16666)

[24]	S. Gosselin, “MEV-Boost: Merge ready Flashbots Architecture - The Merge,” Ethereum Research. [Online]. Available: [MEV-Boost: Merge ready Flashbots Architecture](https://ethresear.ch/t/mev-boost-merge-ready-flashbots-architecture/11177)

[25]	B. Edgington, *Upgrading Ethereum | 2.9.2 Randomness*. 2023. [Online]. Available: [Upgrading Ethereum | 2.9.3 Randomness](https://eth2book.info/capella/part2/building%5C_blocks/randomness/)

[26]	K. Alpturer and S. M. Weinberg, “Optimal RANDAO Manipulation in Ethereum,” Sep. 29, 2024, *arXiv*: arXiv:2409.19883. [Online]. Available: [[2409.19883] Optimal RANDAO Manipulation in Ethereum](http://arxiv.org/abs/2409.19883)

[27]	M. Kalinin and D. Ryan, “EIP-4399: Supplant DIFFICULTY opcode with PREVRANDAO,” Ethereum Improvement Proposals. [Online]. Available: [EIP-4399: Supplant DIFFICULTY opcode with PREVRANDAO](https://eips.ethereum.org/EIPS/eip-4399)

[28]	B. Busa and P. Jayanthi, “Kurtosis: A Deep Dive to Local Devnets.” [Online]. Available: [Kurtosis: A Deep Dive to Local Devnets | ethPandaOps](https://ethpandaops.io/posts/kurtosis-deep-dive/)

[29]	Flashbots Ltd, “Relay API Documentation.” [Online]. Available: [Notion](https://flashbots.notion.site/Relay-API-Documentation-5fb0819366954962bc02e81cb33840f5%5C#854339c909a042d0bbca6e8f8069674e)

[30]	Ethereum Foundation, *ethereum/beacon-APIs*. (Oct. 09, 2024). HTML. ethereum. [Online]. Available: [GitHub - ethereum/beacon-APIs: Collection of RESTful APIs provided by Ethereum Beacon nodes](https://github.com/ethereum/beacon-APIs)

[31]	*flashbots/mev-boost-relay*. (Apr. 03, 2024). Go. Flashbots. [Online]. Available: [GitHub - flashbots/mev-boost-relay: MEV-Boost Relay for Ethereum proposer/builder separation (PBS)](https://github.com/flashbots/mev-boost-relay)

[32]	H. Wang, D. Zhang, and K. G. Shin, “Detecting SYN flooding attacks,” in *Proceedings.Twenty-First Annual Joint Conference of the IEEE Computer and Communications Societies*, Jun. 2002, pp. 1530–1539. doi: 10.1109/INFCOM.2002.1019404.

[33]	“crytic/attacknet: Tool and testing methodology for subjecting blockchain devnets to simulated network and side channel attacks.” [Online]. Available: [GitHub - crytic/attacknet: Tool and testing methodology for subjecting blockchain devnets to simulated network and side channel attacks](https://github.com/crytic/attacknet)

[34]	Flashbots Ltd, “Running MEV-Boost-Relay at scale.” [Online]. Available: [Notion](https://flashbots.notion.site/Running-MEV-Boost-Relay-at-scale-4040ccd5186c425d9a860cbb29bbfe09)

[35]	“Vitalik Buterin supports lowering Ethereum solo staking requirement,” Cointelegraph. Accessed: Oct. 14, 2024. [Online]. Available: [Vitalik Buterin supports lowering Ethereum solo staking requirement](https://cointelegraph.com/news/vitalik-buterin-advocates-lowering-solo-staking-eth)

[36]	“Solo stakers: The backbone of Ethereum,” Rated blog. [Online]. Available: [Solo stakers: The backbone of Ethereum — Rated blog](https://blog.rated.network/blog/solo-stakers)

[37]	Ethereum Foundation, “Secret leader election,” [ethereum.org](http://ethereum.org). [Online]. Available: [Secret leader election | ethereum.org](https://ethereum.org/en/roadmap/secret-leader-election/)

[38]	T. Wahrstätter, “Selfish Mixing and RANDAO Manipulation - Consensus,” Ethereum Research. [Online]. Available: [Selfish Mixing and RANDAO Manipulation](https://ethresear.ch/t/selfish-mixing-and-randao-manipulation/16081)

[39]	F. Damato, L. Zanolini, and R. Saltini, “DAS fork-choice - Consensus,” Ethereum Research. [Online]. Available: [DAS fork-choice](https://ethresear.ch/t/das-fork-choice/19578)

[40]	D. Vyzovitis, Y. Napora, D. McCormick, D. Dias, and Y. Psaras, “GossipSub: Attack-Resilient Message Propagation in the Filecoin and ETH2.0 Networks,” 2019.  [[2007.02754] GossipSub: Attack-Resilient Message Propagation in the Filecoin and ETH2.0 Networks](https://arxiv.org/abs/2007.02754)

[41]	T. Mackinga, T. Nadahalli, and R. Wattenhofer, “TWAP Oracle Attacks: Easier Done than Said?,” in *2022 IEEE International Conference on Blockchain and Cryptocurrency (ICBC)*, May 2022, pp. 1–8. doi: 10.1109/ICBC54727.2022.9805499.

[42]	Bell Curve, *Shining A Light On MEV  | Tarun Chitra, Justin Drake*, (Apr. 05, 2023). [Online Video]. Available: [https://www.youtube.com/watch?v=fWRboyGk\_lc](https://www.youtube.com/watch?v=fWRboyGk%5C_lc)

[43]	0xTaker and Frontier Research, “Exploration of MEV Latencies,” Exploration of MEV Latencies. [Online]. Available: [Exploration of MEV Latencies](https://frontier.tech/exploration-of-mev-latencies)

[44]	“Dark web price of malware/DDoS services 2023,” Statista. [Online]. Available: [Dark web price of malware/DDoS services 2023| Statista](https://www.statista.com/statistics/1350155/selling-price-malware-ddos-attacks-dark-web/)

[45]	*u(nlinked)HTTP-lib*. (Oct. 03, 2024). TypeScript. HOPR. [Online]. Available: [uHTTP-lib/ONBOARDING.md at fe38143e0b23ee7d81f8d8941f044261de74f320 · hoprnet/uHTTP-lib · GitHub](https://github.com/hoprnet/uHTTP-lib/blob/fe38143e0b23ee7d81f8d8941f044261de74f320/ONBOARDING.md)

1. Source code of metaclear-ethereum package GitHub - hoprnet/metaclear-ethereum-package: A Kurtosis package that deploys a private, portable, and modular Ethereum devnet ↩︎
2. Checking the source code within the Github repos of top Relays in https://www.relayscan.io/ indicates that they are variants of Flashbots’ MEV-Relay ↩︎
3. Source code of metadata handling in metaclear-mev-relay https://github.com/hoprnet/metaclear-mev-relay/blob/a96c4b6e9df7e7788a308bd10e3efe0ea3b6316d/services/api/service.go\#L1003-L1042 ↩︎
4. Source code of metaclear-ethereum package GitHub - hoprnet/metaclear-ethereum-package: A Kurtosis package that deploys a private, portable, and modular Ethereum devnet ↩︎
5. Source code of metaclear-lighthouse GitHub - hoprnet/metaclear-lighthouse: Ethereum consensus client in Rust ↩︎
6. Source code of metaclear-attacknet GitHub - hoprnet/metaclear-attacknet: Tool and testing methodology for subjecting blockchain devnets to simulated network and side channel attacks ↩︎
