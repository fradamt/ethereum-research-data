---
source: ethresearch
topic_id: 20107
title: "Commit-Boost: Proposer Platform to Safely Make Commitments"
author: DrewVanderWerff
date: "2024-07-19"
category: Proof-of-Stake
tags: [preconfirmations, proposer-builder-separation]
url: https://ethresear.ch/t/commit-boost-proposer-platform-to-safely-make-commitments/20107
views: 2703
likes: 12
posts_count: 1
---

# Commit-Boost: Proposer Platform to Safely Make Commitments

*The following post is an introduction to some and an update to others on a community effort called [Commit-Boost](https://x.com/Commit_Boost). Much of this has already been discussed in various public domains / presentations / documentation. Thank you to all the countless teams that already have contributed / committed to contributing to this effort including researchers, validators, builders, relays, client teams, consulting firms, teams building commitment protocols, L2s, restaking platforms, shared sequencers, wallets, and countless others. Please reach out if you would like to contribute to this effort for Ethereum.*

[![Commit-Boost](https://ethresear.ch/uploads/default/optimized/3X/a/d/adc1d52f519c3c2bb0d61cd00f9c796e249eba81_2_408x375.png)Commit-Boost782×717 59.8 KB](https://ethresear.ch/uploads/default/adc1d52f519c3c2bb0d61cd00f9c796e249eba81)

**TL;DR**

- Due to the risks developing for Ethereum, core development, and its validator set, a group of teams / individuals are working on developing a public good called Commit-Boost
- Commit-Boost is an open-source public good that is fully compatible with MEV-Boost but acts as a light-weight validator platform to safely make commitments
- Specifically, Commit-Boost is a new Ethereum validator sidecar that is focused on standardizing the last mile of communication between validators and proposer commitment protocols
- Commit-Boost has been designed with safety and modularity at its core, with the goal of not limiting the market downstream including stakeholders, flows, proposer commitments, enforcement mechanisms, etc.
- While we should always be skeptical of out-of-protocol solutions that directly impact infrastructure this close to the Ethereum protocol layer, if we are going to rely on these solutions, we believe they should be developed, sustained, and governed in a way that encompasses many of the views previously voiced by the community. We have tried to embrace this and strive to model Commit-Boost after it

**Background**

- Proposer commitments have been an important part of Ethereum’s history. Today, we already see the power of commitments where over 90% of validators give up their autonomy and make a wholesale commitment that outsources block building to a sophisticated actor called a block builder
- However, most are starting to agree on a common denominator: in the future, beacon proposers will face a broader set of options of what they may “commit" to–be it inclusions lists or preconfs or other types of commitments such as long-dated blockspace futures–compared to just an external or local payload they see today
- A post from Barnabe captures this well; during block construction, the validator “…creates the specs, or the template, by which the resulting block must be created, and the builders engaged by the proposer are tasked with delivering the block according to its specifications”
- While this all seems great, the challenge is that many teams building commitments are creating new sidecars driving fragmentation and risks for Ethereum
- For Ethereum, there are going to be significant challenges and increased risks during upgrades if there are a handful of sidecars that validators are running
- For validators, these risks potentially take us to a world where proposers will need to make decisions on which teams to “bet on” and which sidecars they will need to run to participate in what those teams are offering
- For homestakers, this is difficult and they likely will be unable to participate in more than one of these commitments
- For sophisticated actors, this increases the attack vector and operational complexity as more and more sidecars are required to be run
- Another side effect of this is validators are somewhat locked into using a specific sidecar due to limited operational capacity and the switching costs of running a different sidecar (i.e., vendor lock-in). The higher the switching costs, the more embedded network effects could become if these sidecars only support certain downstream actors / proposer commitment protocols
- This also could create a dynamic where core out-of-protocol infrastructure supporting Ethereum which should be a public good, starts being used for monetization, distribution, or other purposes
- Due to these dynamics, various teams and individuals across the community are driving the development and testing of open-source / public good software called Commit-Boost. This effort includes researchers, validators, builders, relays, client teams, consulting firms, protocols building commitments, L2s, restaking platforms, and countless others across the community

**Commit-Boost Overview**

Commit-Boost is a community-driven, open-source project developing an unopinionated validator platform to enable safe interactions with commitments. Some of its features include:

- Unification: Core devs will be able to interact and work with one standard during Ethereum forks / upgrades / when and if things go wrong
- Backward compatibility + more: Commit-Boost is not only backward compatible with MEV-Boost, but will improve the life of validators who only run MEV-Boost through increased reporting, telemetry / other off-the-shelf tools validators can employ
- Opt-in without running more sidecars: Commit-Boost will allow proposers who want to opt into other commitments do so without having to run multiple sidecars
- Robust support: Commit-Boost the software is supported by a not-for-profit entity. This team will be focused on security and robustness through policies and procedures with follow-the-sun type models where there is support 24/7 if / when things go wrong. This team will also be focused on testing and adjustments needed during hard forks and have a team to interact with to help during adoption, improvements, and sustainment
- Not VC-backed public good: This team and effort will not be VC-backed. There is no monetization plan. The entity will not be able to sell itself and will not start any monetizable side businesses

**Robustness, Sustainability, and Security**

- Commit-Boost is being developed as a fully open-source project with contributions from teams across the Ethereum tech stack including from validators, client teams, relays, builders, consulting firms, researchers, and many others. This effort with input and support from these teams will help develop a robust product integrating many perspectives
- Commit-Boost will go through code reviews and audits once fully developed
- As noted below, there also will be a full-time team that helps maintain and upgrade the software with their core focus on 100% uptime and when there are bugs, robust processes to quickly address and fix
- The software stack is also built with the validator at the core and includes off-the-shelf tools for monitoring as well as reducing and proactively addressing any risks that may arise
- Last, this public good software will have minimal, but critical open governance around future upgrades with input across the Ethereum

**Team Supporting / Governance of Commit-Boost Software**

- Entity supporting the software: Not-for-profit entity
- Multiple-person team: Multiple devs that focus on transparency, sustainment / development, and research with an initial focus around Commit-Boost the software
- Transparency: Open-source repo and governance calls (see below)
- Sustainment / Development: 24/7 follow-the-sun coverage and highly engaged with client teams around upgrades / early in getting testnet support
- Research: Helping with open-source research across Ethereum
- Governance: This is still a WIP, but at a minimum will run a Commit-Boost, ACD-like calls (first one coming soon) to engage with stakeholders and drive consensus on upgrades / help coordinate around hard forks. A credibly neutral community member will lead these calls / this process that has experience with running governance processes over critical software within the Ethereum community
- Funding: All grants

**Where Will the Grants Come From**

The team is in the process of applying for grants from across the ecosystem. We are initially applying to a few organizations across the community that are supporting grants across research organizations and firms focused on PBS and staking. If teams are interested in providing a grant, feel free to comment below / reach out.

**Technical Roadmap**

Commit-Boost is currently in the MVP phase with [testing](http://holesky.beaconcha.in/slot/2022891) underway in Holesky with multiple validators. This includes the full functionality of a PBS Module implementing MEV-Boost with additional telemetry and metrics collection. We are continuing the development and feature set of Commit-Boost targeting production-ready software and audits kicking off at the end of Q3. More details are in the Commit-Boost [repo](https://github.com/Commit-Boost/commit-boost-client/issues) and we are keen to get feedback / engage with the community around these.

Some near-term high-level highlights from the roadmap include:

- Optimized and functional MEV-Boost module including multiple metrics for reporting and extensions such as configurable timing for get_header / get_payload calls
- Pre-made dashboards on Grafana for all core services
- Improved reliability and integrations for incident response
- R&D / spec signing mechanism to fit as many validator set-ups as possible
- Expanding modularity and optionality (i.e., supporting different types of signatures and modules)

**Commit-Boost Design Principles**

- Built for validators: Platform that not only can help validators today (i.e., can improve the lives of validators even if they just run an MEV-Boost module) but allows validators to be ready for the market of tomorrow (i.e., preconfs, inclusion lists, etc)
- Neutrality: No opinions, the platform will be proposer commitment agnostic, relay agnostic, transaction flow agnostic, etc. The goal is to build a platform that doesn’t limit the design space downstream while reducing risks of fragmentation for validators and Ethereum
- Unified: Validators run one core sidecar with the ability to opt into many different commitments
- Safety: Open-source code developed with input by the community with community reviews / audits
- Reduce risks: Modularized and transparency are core to reducing risk / overhead for the proposer to manage commitments and their broader operational processes
- Values aligned: Public good with no plans for monetization. We will continuously ask ourselves: would Vitalik run Commit-Boost and can this be designed in a way to increase the decentralization of Ethereum block construction

**From the Perspective of the Proposer**

More details on what it takes to run Commit-Boost as a node operator can be found [here](https://commit-boost.github.io/commit-boost-client/get_started/overview). Please note that this has not been finalized and over the next few weeks we will be making updates (see roadmap / milestones above).

- Run a single sidecar with support for MEV-Boost and other proposer commitments protocols, such as precons / other commitments
- Out-of-the-box support for metrics reporting and dashboards to have clear insight around what is happening in your validator seen through dashboards such as Grafana
- Plug-in system to add custom modules, i.e., receive a notification on Telegram if a relay fails to deliver a block
- Standardized way to provide a signature to opt into a commitment
- Creates constraints / condition sets and pass these constraints downstream

**From the Perspective of the Proposer Commitment Protocol / Module Creator**

More details on what it takes to build a module / metrics can be found [here](https://commit-boost.github.io/commit-boost-client/category/developing). Please note that this has not been finalized and over the next few weeks we will finalize moving parts that impact module creators (see roadmap / milestones above).

- A modular platform to develop and distribute proposer commitments protocols
- A single API to interact with validators
- Support for hard-forks and new protocol requirements

**Architecture of Commit-Boost**

More details can be found in the Commit-Boost [documentation](https://commit-boost.github.io/commit-boost-client/). However, below is a schematic of Commit-Boost. This proposed architecture allows proposers to run one sidecar, but still retain the ability to opt into a network of proposer commitment modules. More specifically, with this middleware, the proposer will only need to (in the case of delegation / light weight commitments) run one sidecar and limit their responsibilities to only selecting which module / proposer commitment protocol they would like to subscribe to.

It is important to note that the below depiction contains just a few examples of proposer commitment modules that can run on Commit-Boost. The design space for modules is completely open / not gated by the Commit-Boost software and proposers will be responsible for opting into the commitments they wish to subscribe to (i.e., a proposer is responsible for which modules they will subscribe to).

**Terminology**

- Proposer: entity, staking pool NoOp, or DVT cluster with the right to propose the next block
- Commitment: a constraint or condition that the proposer choses and agrees to via a signature
- Key Manager: some proposers use key managers or remote signers as part of their proposer / validator duties. Please note, that Commit-Boost is being designed in a way where it does not require validators to run key managers and working on solutions for monolithic set-ups
- Consensus Client: for example, Lighthouse or Teku (see here for more details)
- Commitment Modules: community-built modules allowing proposers to make commitment, including some of the logic of the proposer commitment protocol
- Signer API: The signer API is one of the core components around Commit-Boost. This is used to provide signatures from the proposer to the proposer commitment protocol. This is still in the design but proxy signatures will be used in nearly all cases (there are some outlier cases). For more details on the API please see here. For an example of how to communicate with the Signer API, please see here

[![Schematic](https://ethresear.ch/uploads/default/optimized/3X/c/a/ca4fdf7f738261cf46b1505dc56198da182592dc_2_690x411.png)Schematic865×516 44 KB](https://ethresear.ch/uploads/default/ca4fdf7f738261cf46b1505dc56198da182592dc)

Using this as a middleware instead of direct modification to the consensus client or running a sidecar per commitment will allow for each component to be sustained independently and will provide for cross proposer commitment compatibility. This will also allow for a bit of time for the market to play out, but via a public good, standardize the last mile of communication to help address the risks (discussed in the background section above) developing. Once the market does play out, and the community is able to observe some dynamics (the good and the bad), we can and should push for CL changes.

**Resources**

- Commit-Boost Repo
- Commit-Boost documentation
- List of presentations
- Original post on ETH Research, read more here
- First presentation to the community can be found here
- Second presentation at zuBerlin can be found here
- zuBerlin Devnet notion can be found here
- Mev-Boost Community call here
- Espresso / One Balance Sequencing day here (this will be updated when the link is ready)
- Gattaca MEV Day here (this will be updated when the link is ready)
