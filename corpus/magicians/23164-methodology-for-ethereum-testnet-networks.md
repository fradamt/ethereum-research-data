---
source: magicians
topic_id: 23164
title: Methodology for Ethereum (testnet) Networks
author: alonmuroch
date: "2025-03-16"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/methodology-for-ethereum-testnet-networks/23164
views: 346
likes: 10
posts_count: 6
---

# Methodology for Ethereum (testnet) Networks

The recent failed forks on Sepolia and Holesky left Ethereum app developers without a stable, finalizing testnet, effectively halting most development progress for nearly three weeks. This disruption underscored a critical issue: the lack of reliable testnet infrastructure for developers.

With the Ethereum Foundation’s [leadership transition](https://www.coindesk.com/tech/2025/03/01/ethereum-foundation-picks-new-co-executive-directors-following-leadership-reshuffle), there is now a renewed focus on app developers. This shift presents an opportunity to reassess the goals and priorities of Ethereum’s testnets to better support the broader development community.

SSV.Network, like many other projects, was heavily reliant on Holesky. The network instability significantly delayed our development, reinforcing the need for more dependable testing environments. Frustrated by the situation, I tweeted the following:

**[![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcammU3Yi_s5dyJYfR9mGpPqereMPH_eccvIpp4Yzfx6UrBmp6oSLbbZhRWZkdhSscRnELIufcT-gNBlHiTZpDFso75-9pZ-0dmRs8rlFCA0cxcjz9Lj95bg37Z9Cptye541j6SMg?key=Xz1CRapOotEVX7ifihcNdDFI)](https://x.com/AmMuroch/status/1897647440301318570)**

Moving forward, the Ethereum community must prioritize testnet stability to ensure continuous innovation and prevent future bottlenecks in protocol and application development.

# What Are Testnets For?

“A testnet is an encapsulation of some Ethereum fork, with next to zero cost of testing and experimentation”

And boy did we have a lot of them… 26 to be exact (see table below)

Despite their differences, all testnets share common traits:

- Critical dependencies – Developers rely on them for QA testing, transaction validation, contract interactions, and more.
- Operational overhead – Running nodes, coordinating upgrades, and maintaining tooling introduce significant costs and complexity.
- Finite lifespan – Unlike mainnet, all testnets are eventually deprecated, forcing migrations and disrupting workflows.

Historically, some testnets enjoyed longer lifespans (Ropsten, Kovan, Rinkeby, Goerli), but recent years have brought instability, introducing frequent changes to testing environments. While no testnet has ever been designated as “everlasting,” the consequences of their deprecation are far from trivial—especially for app developers with limited DevOps and cloud resources.

**The Need for a Persistent Testnet**

We tend to accept that mainnet is the only stable network, but that assumption is flawed when building consumer-facing applications. Developers need a testnet that mirrors mainnet as closely as possible.

As dApp complexity grows, so does dependency on external services. Expecting developers to self-replicate critical Ethereum infrastructure (e.g., ENS, Etherscan, builders/relays) for local testing is neither practical nor scalable.

**Case Studies: Why Stability Matters**

1. Dex Aggregator
A DEX aggregator relies on multiple on-chain services like oracles, DEX pools, and bridges, which are difficult to replicate. While open-source contracts can be redeployed, the effort and cost involved are prohibitive.
2. Staking Service
Staking services must interact with third-party components such as relays, builders, and deposit contracts. These dependencies are nearly impossible to replicate in a local test environment.

**Testnet Successions**

| Terminated Testnet | Successor | Reason for Transition |
| --- | --- | --- |
| Morden (July 2015 – Nov 2016) | Ropsten (Nov 2016) | Morden was deprecated due to accumulated junk data and client consensus issues. Ropsten replaced it as the primary PoW testnet. |
| Ropsten (Nov 2016 – Dec 2022) | Sepolia (Oct 2021 – Active) | Ropsten was transitioned to PoS during Merge testing, then deprecated in favor of Sepolia, which is lighter and easier to maintain. |
| Kovan (March 2017 – 2021) | Sepolia (Oct 2021 – Active) | Kovan was a PoA testnet maintained by OpenEthereum (Parity), which was deprecated. Sepolia became the main Ethereum execution-layer testnet. |
| Rinkeby (April 2017 – Q3 2023) | Sepolia (Oct 2021 – Active) | Rinkeby did not undergo The Merge, so it was deprecated. Sepolia took over as the main lightweight testnet. |
| Goerli (Jan 2019 – Active, planned EOL 2024) | Holesky (Sep 2023 – Active) | Goerli faced issues with test-ETH supply and staking limitations. Holesky was launched as a large-scale staking testnet to replace it. |
| Prater (June 2021 – Aug 2022) | Merged with Goerli (Aug 2022) | Prater was an Ethereum 2.0 beacon chain testnet. It was merged into Goerli to simulate The Merge. |
| Pyrmont (Nov 2020 – Q4 2021) | Prater (June 2021 – Aug 2022) | Pyrmont was an early staking testnet, but Prater replaced it as the long-term beacon chain testnet. |
| Kiln (Feb 2022 – Sep 2022) | No direct successor (transition to Merge) | Kiln was the final Merge testnet. It was decommissioned after The Merge successfully went live on mainnet. |
| Shandong (Oct 2022 – Jan 2023) | Shanghai Public Testnets (Zhejiang, etc.) | Shandong was an early testnet for Shanghai/EOF, but EOF was postponed, so it was replaced by final Shanghai testnets. |
| Zhejiang (Feb 2023 – April 2023) | Mainnet Shanghai Upgrade | Zhejiang was a short-lived testnet to simulate ETH withdrawals. Once Shanghai went live, it was deprecated. |

# In A Perfect World

To solve the issues outlined above, we need to rethink what a testnet should be. A perfect testnet for app developers should embody the following key properties:

#### 1. Continuity: A Testnet That Lasts

A truly effective testnet must be long-lasting—ideally indefinite—evolving alongside the Ethereum mainnet. It should serve as a permanent point of reference for developers, ensuring stability in testing environments.

Continuity enables the broader developer community to build an entire ecosystem around it, including:

- Tooling (e.g., monitoring, debugging, and deployment frameworks)
- Faucets (ensuring easy access to test ETH)
- Builders & Relays (for a realistic block-building environment)
- Explorers (to track test transactions just like on mainnet)
- Interoperable dApps (for seamless integration testing)

#### 2. Isomorphism: A True Mainnet Replica

The ideal testnet should mirror mainnet as closely as possible. This means:

- Protocol stability – The testnet should not fail due to forks, misconfigurations, or protocol changes.
- Identical properties – Everything from gas mechanics to validator behavior should be an accurate reflection of mainnet, except for the use of “funny money” instead of real ETH.
- Full-feature parity – It must support the same infrastructure services as mainnet, ensuring realistic testing conditions.

#### 3. Accessibility: Open & Scalable for Developers

Past testnets have often suffered from artificial scarcity—whether through limited access to test ETH, restricted validator sets, or bureaucratic hurdles. This led to instability, slow adoption, and even premature deprecation.

A developer-friendly testnet should be:

- Permissionless – Anyone should be able to access it and spin up validators if needed.
- Scalable – Designed to handle high transaction volumes and large-scale app testing.
- Easy to onboard – With simple mechanisms for obtaining test ETH and deploying smart contracts at scale.

# Methodology for Ethereum Networks

To address the current issues with Ethereum testnets, we propose a structured testnet methodology that categorizes networks based on their purpose, stability, and governance. This approach ensures continuity, isomorphism, and accessibility while providing dedicated environments for different use cases.

### 1. Mainnet (Ethereum Main Network)

Purpose: The primary Ethereum network for production use.

- Ever-lasting – The final, canonical Ethereum chain.
- Minimal risk tolerance – Any protocol change must be fully vetted and proven.
- The ultimate point of reference – All testnets should align with its behavior.

Why it matters:

- Ensures a secure and stable environment for users and dApps.
- Provides a source of truth for developers and researchers.
- Maintains Ethereum’s economic and security integrity.

### 2. aTestnet (App Developer Testnet)

Purpose: A stable, long-term testnet designed specifically for app developers.

- Ever-lasting – A permanent testnet that remains operational indefinitely.
- Minimal risk tolerance – Only perfectly vetted changes are introduced.
- Forks with or after mainnet – Maintains high parity with the main Ethereum chain.
- Similar ETH supply as mainnet – Mimics real-world economic conditions.
- Community faucets – Provides open access to test ETH for developers.

Why it matters:

- Ensures uninterrupted testing for dApps, wallets, and smart contracts.
- Supports a full ecosystem of tooling, explorers, relays, and infrastructure.
- Eliminates sudden deprecations that disrupt developer workflows.

### 3. ceTestnet (Consensus + Execution Testnet for Core Developers)

Purpose: A structured environment for testing protocol upgrades before mainnet deployment.

- Forks before mainnet – A successful fork here means a mainnet upgrade is imminent.
- Could be terminated – Exists only as needed for upgrade validation.
- Validator set controlled by the Ethereum Foundation and partners – Ensures structured testing and reliability.

Why it matters:

- Serves as a proving ground for protocol upgrades before they go live.
- Allows Ethereum core developers to test and validate changes under realistic conditions.
- Reduces risks by ensuring only battle-tested forks reach mainnet.

### 4. uceTestnet (Unstable Consensus + Execution Testnet)

Purpose: An experimental testnet for early-stage consensus and execution changes.

- Forks before ceTestnet – The first testing environment for new protocol changes.
- Unstable by design – Encourages experimentation and rapid iteration.
- Easier to experiment with – No long-term support guarantees.
- Validator set controlled by the Ethereum Foundation – Managed for structured chaos.

Why it matters:

- Serves as Ethereum’s sandbox for bleeding-edge research.
- Allows core developers to test radical changes without breaking stable testnets.
- Reduces failure risks before upgrades reach ceTestnet or mainnet.

### 5. dsTestnet (Domain-Specific Testnets)

Purpose: Custom testnets for non-canonical Ethereum forks and niche use cases.

- Unstable by design – Built for targeted experimentation.
- Supports domain-specific Ethereum adaptations – Used for specific research, such as rollup testing, execution sharding, or staking experiments.
- Validator set controlled by the Ethereum Foundation – Ensures controlled experimentation.

Why it matters:

- Enables custom Ethereum forks to test innovations without impacting global testnets.
- Supports specialized research in scalability, security, and execution environments.
- Prevents fragmentation of core testnets by offloading experimental work.

# Conclusion: A Testnet Framework That Works for Everyone

By implementing this methodology, Ethereum can provide:

- App developers with a stable, long-term testing environment (aTestnet).
- Core developers with structured, risk-tolerant testnets for protocol upgrades (ceTestnet and uceTestnet).
- Domain-specific innovators with dedicated experimental spaces (dsTestnet).

This structured approach ensures Ethereum remains developer-friendly while maintaining high security, stability, and innovation velocity.

The next step is rallying the community around this vision and pushing for implementation.

# Past & Present Testnets

| Name | Launch Date | Termination Date | Duration | Purpose | Consensus Mechanism | Type | Special Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Olympic | Early 2015 | Jul-15 | 6 months | Final pre-launch testnet (stress test for Frontier release) | PoW | Public Testnet | Ethereum 0.9, incentivized stress test |
| Morden | Jul-15 | Nov-16 | 16 months | First long-lived testnet | PoW | Public Testnet | Replaced due to consensus issues, continued as Morden Classic for ETC |
| Ropsten | Nov-16 | Dec-22 | 6 years | Final Ethereum PoW testnet, later merged to PoS | PoW ‚Üí PoS | Public Testnet | DoS attack in 2017, transitioned to PoS before deprecation |
| Kovan | Mar-17 | 2021 | 4 years | Parity PoA testnet, aimed at stability for dApps | PoA (Aura) | Public Testnet | Only supported by OpenEthereum, not Geth |
| Rinkeby | Apr-17 | Q3 2023 | 6 years | Geth PoA testnet | PoA (Clique) | Public Testnet | Did not undergo The Merge |
| Goerli | Jan-19 | Q1 2024 | 5 Years | Cross-client PoA testnet, later transitioned to PoS | PoA ‚Üí PoS | Public Testnet | Merged with Prater Beacon Chain for Merge testing |
| Sepolia | Oct-21 | Active | Ongoing | Main post-Merge testnet | PoW ‚Üí PoS | Public Testnet | Minimal cross-client execution layer testnet |
| Holesky | Sep-23 | Active | Ongoing | Largest Ethereum testnet, replacing Goerli | PoS | Public Testnet | 10√ó mainnet validators, resolves Goerli‚Äôs test-ETH issues |
| Schlesi | Apr-20 | May-20 | 1 month | First multi-client Beacon Chain testnet | PoS (Beacon) | Beacon Chain Testnet | Tested Eth2 clients for Phase 0 |
| Witti | May-20 | Jun-20 | 1 month | Second Beacon Chain testnet | PoS (Beacon) | Beacon Chain Testnet | Expanded client diversity |
| Altona | Jun-20 | Aug-20 | 2 months | Limited multi-client testnet before Medalla | PoS (Beacon) | Beacon Chain Testnet | Early Eth2 validator coordination |
| Medalla | Aug-20 | Dec-20 | 4 months | Final Beacon Chain testnet before mainnet | PoS (Beacon) | Beacon Chain Testnet | Time sync bug caused network halt |
| Spadina | Sep-20 | Oct-20 | 3 days | Dress rehearsal for Eth2 launch | PoS (Beacon) | Beacon Chain Testnet | Failed due to low validator participation |
| Zinken | Oct-20 | Oct-20 | 1 week | Second genesis rehearsal | PoS (Beacon) | Beacon Chain Testnet | Final pre-launch rehearsal before Beacon Chain mainnet |
| Pyrmont | Nov-20 | Q4 2021 | 1 year | Public staking testnet post-Eth2 launch | PoS (Beacon) | Beacon Chain Testnet | Large-scale staking testnet |
| Prater | Jun-21 | Aug-22 | 1 year | Successor to Pyrmont, merged with Goerli | PoS (Beacon) | Beacon Chain Testnet | Used for The Merge testing |
| YOLO v1 | Jun-20 | Jun-20 | 1 month | Early Berlin upgrade testnet | PoW | Ephemeral Devnet | Crashed due to disk usage issues |
| YOLO v2 | Oct-20 | Late 2020 | 1 month | Berlin upgrade EIP testing | PoW | Ephemeral Devnet | Follow-up after YOLO v1 crash |
| YOLO v3 | Feb-21 | Q1 2021 | 2 months | Final Berlin upgrade testing | PoW | Ephemeral Devnet | Concluded Berlin test cycle |
| Aleut | Apr-21 | May-21 | 1 month | First London upgrade testnet | PoW | Ephemeral Devnet | Tested EIP-1559 fee market changes |
| Baikal | May-21 | Late May 2021 | 2 weeks | Second London upgrade testnet | PoW | Ephemeral Devnet | Ensured client compatibility |
| Calaveras | May-21 | Jun-21 | 1 month | Final London upgrade testnet | PoW | Ephemeral Devnet | EIP-1559, 3198, 3529, 3541 tested |
| Kintsugi | Dec-21 | Q1 2022 | 3 months | First Merge testnet | Hybrid (PoW ‚Üí PoS) | Ephemeral Devnet | Exposed client bugs, leading to Kiln |
| Kiln | Feb-22 | Sep-22 | 7 months | Final Merge testnet | Hybrid (PoW ‚Üí PoS) | Ephemeral Devnet | Successfully simulated The Merge |
| Shandong | Oct-22 | Jan-23 | 3 months | Experimental pre-Shanghai testnet | PoS | Ephemeral Devnet | Ran EOF and PUSH0 EIPs, later removed |
| Zhejiang | Feb-23 | Apr-23 | 2 months | Staked ETH withdrawals (Shanghai/Capella) | PoS | Ephemeral Devnet | Allowed early withdrawal testing |

## Replies

**yuting** (2025-03-18):

The finalization issues caused by Sepolia and Holesky are really terrifying. The current situation is akin to everyone on Earth sharing a single computer, with some doing homework, some playing games, some writing documents, and others learning how to disassemble computers—haha. I strongly support the design and maintenance of multiple purpose-built testnets; this definitely isolates risks effectively. From the perspective of feasibility in implementation, I’m thinking about how to design an economic mechanism that ensures people can organically organize themselves to maintain these multiple testnets. Some may want to test for three months while others may wish to test for a year; it seems quite challenging without an economic mechanism. Suddenly, I thought that all Ethereum testnets are actually PoS blockchains—could we utilize SSV bapp (based application) to implement a Testnet as a Service? This would allow rapid generation of on-demand testnets on bapp, with SSV bapp operators taking on the validation services for multiple testnets and enabling different risk levels as needed. This way, there’s no need for dynamic organization of validators specifically, reducing many coordination difficulties.

---

**parithosh** (2025-03-18):

Thank you so much for the detailed post! I agree that this sort of comprehensive framing has been missing for a while, we might need to work on how we message the testnets.

IMO we do need atleast 3 specific networks:

1. App dev: this would be sepolia, its stable, has uptime similar to mainnet and easy to get funds
2. Staking: this used to be holesky and would now become hoodi. This is meant to be large (mainnet sized), but we try to keep it as stable as possible for staking setups
3. Chaos network: this is where core devs can test taking the network down, non finality, bump gas limits and so on

I think anything on top of these 3 types of network basically adds a lot of co-ordination overhead for what might be unclear gains - some such as 5.dsTestnet do tend to be done via devnets, they just aren’t widely announced and hence lack of recognition of them.

I think one item i might want to push back on is ever-lasting - I think this might be detrimental as the protocol evolves and the testnet stack we support needs to evolve with it. E.g, The parameters chosen on Goerli were fine for 2019, but the testing needs of 2022 forced us to replace it. I imagine the same with future upgrades (beamchain/etc) needing us to relaunch networks setup in a way to facilitate that version of the network.

However I do agree that our testnets might need to be more risk averse, ideally we only break them if we can’t avoid it.

---

**alonmuroch** (2025-03-23):

Thank you for the feedback!

I think the challenge here is to re-define those testnets according to what i’ve written in the original post. For example Sepolia forked first which contradicts the notion of a stable (risk free) app dev net.

If we can re-define those testnets to be that it will be an easy and big win to the community.

Why should an app testnet be any different than mainnet in that regard? If mainnet goes through forks it can go as well. The notion of an ever-lasting testnet is to ingrain stability into our tests, not just our mainnet.

Think of integration testing which depends on other dApps, without stability (current status), developers find themselves re-deploying entire dApps just for simple integration testing…

---

**timbeiko** (2025-03-25):

+1 to what Pari said.

I’d also add that we have had cases of `dsTestnets` in the past. Pretty much every devnet is one of those ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)  Sometimes there’s value in getting community input so we polish them a bit, like with [Mekong](https://blog.ethereum.org/2024/11/07/introducing-mekong-testnet) or [Kintsugi](https://blog.ethereum.org/2021/12/20/kintsugi-merge-testnet). More recently, Ithaca also had [experimental devnets](https://ithaca.xyz/updates/exp-0003).

That said, maybe we do need to formalize both the terminology and fork ordering. One challenge with the latter is that sometimes forks affect more things at the application layer, and other times they affect the consensus layer. This can affect how we want to order things. Additionally, how close we are to deprecating a testnet may also play a role, as it can be lower stakes to first deploy to that testnet. One thing we could consider is to always include at least one successful shadow fork before forking an application-facing testnet.

---

**alonmuroch** (2025-03-26):

Thank you for your comments!

I agree we don’t need more testnets, the overhead is too much. But we can, as you’ve suggested, better define the existing ones to suite what app devs “need”.

The 2 points i’m bullish about are:

- Stability - let’s try to treat the app dev testnet as similarly as possible to mainnet
- Longevity - let’s try, in a perfect world, to never terminate that testnet. Probably impossible but i think setting that as a goal is important

Making those 2 points as formal and public as possible will be a huge improvement!

