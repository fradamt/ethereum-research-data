---
source: ethresearch
topic_id: 21640
title: Fabric - Fabric to Accelerate Based Rollup Infrastructure & Connectivity
author: DrewVanderWerff
date: "2025-01-30"
category: Layer 2
tags: [based-sequencing]
url: https://ethresear.ch/t/fabric-fabric-to-accelerate-based-rollup-infrastructure-connectivity/21640
views: 1353
likes: 30
posts_count: 6
---

# Fabric - Fabric to Accelerate Based Rollup Infrastructure & Connectivity

*Over the last few weeks many teams and individuals across Ethereum provided feedback and input on this idea and post. Some of these teams were able to reflect their support in the recent [Sequencing Call](https://x.com/drakefjustin/status/1882861787491778998) hosted by Justin Drake, but this support stretches beyond those teams. We also want to note that [Fabric](https://x.com/fabric_ethereum) is a continuation of many efforts and is a Schelling point to help coordinate and accelerate the benefits of based sequencing.*

*Personal Note: Since last year I have been focused on an effort called [Commit-Boost](https://github.com/Commit-Boost). Fabric in no way is a shift away from [Commit-Boost](https://x.com/Commit_Boost), rather leaning in unlocking more resources to help push Ethereum forward.*

[![Fabric](https://ethresear.ch/uploads/default/optimized/3X/d/9/d9c6c64630565ce0deb1dfef40be09589186b5f6_2_497x500.jpeg)Fabric850×855 89.2 KB](https://ethresear.ch/uploads/default/d9c6c64630565ce0deb1dfef40be09589186b5f6)

### TL;DR

- The Ethereum rollup ecosystem has experienced remarkable growth, with multiple L2s driving scalability, innovation, and adoption. Years of progress have provided the community with valuable insights into design trade-offs and opportunities for collaboration.
- Over the past year, based rollup research and development contributions and efforts have progressed significantly with the goal of offering an alternative way to sequence rollups that aims to inherit as much of Ethereum’s core properties—liveness, decentralization, and censorship resistance—as possible, while helping address fragmentation within the L2 ecosystem, improving UX, and enabling new forms of composability with the L1.
- With two based rollups (Taiko, Facet) now live in production and several preconfirmation (preconf) protocols in development/testing on Holesky, we believe based rollups have matured to a point where the community has a clearer understanding of design trade-offs and a path forward. Conversations with over a dozen teams indicate strong support for a coordinated effort around based rollups to:

> Align on minimal standards that the community can agree they will collectively adopt.
> Ship a minimal viable reference implementation of a based rollup stack that prioritizes simplicity, legibility, and trustlessness.
> Collaborate with existing rollup stacks to support these standards.

- To support this vision, teams across Ethereum propose “Fabric” (Fabric to Accelerate Based Rollup Infrastructure & Connectivity)—a community effort to continue accelerating coordination and to collectively agree on standards to help drive the based rollup ecosystem forward. Fabric in practice will be a minimal collection of common components required by based rollups and aims to become a Schelling point for rollup developers to build on and build towards.
- This initiative is stitching together work started last year by Justin Drake and other contributors across the Ethereum ecosystem and it will not progress without their continued collective efforts. Early progress has been made through based preconfs, focusing on public goods such as standardizing how validators make proposer commitments, creating API specs for building preconf-compliant blocks and introducing a universal registry contract to back proposer commitments with collateral.
- Fabric is building off of the efforts of many teams, but as a community-driven effort, we welcome feedback and encourage active participation from across the Ethereum ecosystem to push this forward.

### Background

The Ethereum ecosystem has been experiencing rapid growth, with multiple L2s flourishing and bringing in users and applications at an accelerated pace. This growth has driven scalability, user adoption, and innovation, showcasing the strength and diversity of Ethereum’s developer and user communities. Along with this, based rollup efforts emerged as a solution to help address L2 ecosystem fragmentation. Following an [ETH Research post](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016) nearly two years ago and a [year-long push](https://www.youtube.com/playlist?list=PLJqWcTqh_zKHDFarAcF29QfdMlUpReZrR) throughout 2024, there is now general consensus among an ever-growing part of Ethereum that we should pursue the development of based rollups ([timeline](https://docs.spire.dev/spire-overview/based-resources) of based rollup talks and developments).

There is a vast diversity of based rollups and based rollup stacks being built (these are just the ones we’re aware of), each innovating in its own ways. They all share the challenge of re-implementing common infrastructure, such as modifications to the PBS pipeline, highlighting the importance of collaboration and standardization within the based ecosystem.

[![Based Ecosystem as of Sequencing Call 16 - Justin Drake](https://ethresear.ch/uploads/default/optimized/3X/f/4/f4a5b10de31fb87b691fd1808f7b12f42dcb03c9_2_690x214.jpeg)Based Ecosystem as of Sequencing Call 16 - Justin Drake1920×596 81.8 KB](https://ethresear.ch/uploads/default/f4a5b10de31fb87b691fd1808f7b12f42dcb03c9)

*We want to note that the “How It Is Going” is does not capture all the teams looking to support or be based.*

### Proposal

We propose Fabric, an effort to coordinate and standardize various components needed for based rollups. The goal is to coordinate, help build, shepherd adoption, and then sustain a collection of common standards and components that anyone can use or develop towards in their own based or non-based rollup stack. As part of the effort, we will encourage and help develop reference implementations for anyone to deploy a based rollup or use as a guide to adapt and evolve their stack.

### Design principles

- Open-source/Open Development: Everything will be developed in the open and released under open-source licenses (MIT/Apache-2.0).
- Limit Stack Lock-In: We aim to develop the minimal components necessary to integrate with a variety of existing rollups ensuring they are not purpose-built for any single stack.
- Modularity: Fabric will establish a minimal set of standards that rollup developers can adopt to expedite the creation of based rollups while leaving room for competition, such as developers creating custom stacks or SDKs.
- Governance Minimized: This effort will not be venture-backed, and there are no plans to launch a token or monetize. It is a public good and will involve contributions from teams across the Ethereum ecosystem.

### Fabric from the perspective of the Ethereum Community

- There is growing sentiment within the Ethereum community that based rollups are a valuable approach for Ethereum’s scalability and decentralization goals. Fabric aims to facilitate this progress more efficiently by coordinating efforts, driving adoption, and sustaining public goods.
- Based rollups often operate with fewer trust assumptions than classical rollups since they leverage the Ethereum validator set for security, making this effort well-suited to function as a public good.

### Fabric from the perspective of rollup/rollup providers

- Projects can contribute to common based rollup infrastructure without bearing the full burden of development, sharing resources and efforts with the Ethereum community.
- Teams can either leverage the reference implementations or develop customized stacks for their specific offerings (e.g., replace the VM or proving system). This reduces the developer resources required while contributing to the positive-sum based ecosystem.
- L2 teams can take advantage of a balanced positioning, where they can contribute to public goods while also continuing to offer customized solutions, helping establish a healthy relationship between “public” and “private” efforts.

### Supporting/Governance of Fabric

- Entity Supporting Coordination and Development: Many teams and individuals across Ethereum will be critical to the success of this effort. However, a core team already helping drive the development of Commit-Boost, API standards, and universal registry contract can be leveraged as a point of coordination, shepherding, and development.
- Transparency: Development will be in the open and everything will be open-sourced.
- Sustainment/Development: Full-time committed team developing standards and supporting Fabric on a continued basis with input from teams across Ethereum.
- Funding: Only through grants provided by teams across the Ethereum ecosystem.

### Overview of Fabric

Fabric is designed to facilitate the adoption of based sequencing by providing the tools necessary to decentralize rollup sequencers and efficiently interface with Ethereum validators. Rather than being a monolithic stack, Fabric offers a minimal set of modular components built on a set of standards that rollups can use to transition towards being based. This helps ensure rollups have a path to adopt based sequencing efficiently while maintaining flexibility to innovate and observe the based rollup infrastructure mature.

Based rollups exist on a spectrum of decentralization, and Fabric seeks to avoid imposing rigid design choices. For example, this can range from a straightforward “total anarchy mode,” where anyone can propose the next block, to more structured models that restrict proposers to those providing preconfs—credible commitments about transaction inclusion and execution that enhance the user experience.

As part of this effort, Fabric will include open-source reference implementations for components that are not yet built or are built but need modifications, ensuring developers have a clear starting point for adoption.

We view this effort as an *initial* foundation and are eager to collaborate across the ecosystem to refine and advance its development. Fabric *tentatively* includes:

L1 components for based block construction:

- Commitments API: Enables consumers to request and verify preconfs (needs coordination across preconf teams which will build on the Constraints API efforts).
- Constraints API: Ensures proposers build L1/L2 blocks that satisfy preconfs (in development).
- Universal Registry Contract: Allows proposers to register and be discovered (in development).

L2 components for based sequencing:

- Proposing Layer: Multiple components needed to make rollup contracts aware of based preconfers (needs development and coordination across teams).
- Sequencing Layer: Multiple components to delegate L2 proposing rights, price transactions, and distribute fees i.e., to proposers/gateways/PGF/etc (needs development and coordination across teams and in particular coordination and thoughts around PGF—see Vitalik’s recent talk here).
- Blob Sharing: Optimizes shared blob space across rollups (needs development and coordination across teams).
- Shared Bridging: Enables shared settlement helping interoperability (needs development and coordination across teams).

Fabric is unopinionated on the VM or proof system so the following layers are left open for custom implementations:

- Derivation Layer: Facilitates L2 state reconstruction using an L1 node (exists in multiple rollup stacks, but needs to be standardized/developed across different stacks).
- Execution Layer: The goal is to support multiple virtual machines (needs development and coordination to potentially support different EVM implementations).
- Settlement Layer: Accommodates diverse proving systems (needs coordination and development around the proving system i.e., validity/fraud/multi-proof).

[![Fabric Overview](https://ethresear.ch/uploads/default/optimized/3X/a/a/aa05b89e4d1c588c8b928edf04fbe83e028ed562_2_637x500.png)Fabric Overview856×671 363 KB](https://ethresear.ch/uploads/default/aa05b89e4d1c588c8b928edf04fbe83e028ed562)

**Near-Term Roadmap**

We have already begun work at the proposer/PBS pipeline level and are now focused on expanding efforts to cover the full scope. In the coming days, weeks, and months we plan to help drive consensus and coordination around the Fabric’s design, secure funding to support development, and hire developers to accelerate progress. Collaboration with the community will be a key focus, ensuring that specifications are refined and aligned with broader ecosystem needs. We expect to have a more detailed plan, finalize specs, and start shipping components of the stack within the next few days to weeks.

### FAQ:

Why take this approach for Fabric?

- We aim to standardize based sequencing, which doesn’t fit neatly into a single “rollup stack.” For example, efficient based sequencing (such as with preconfs) involves components that impact the L1 block production supply chain which is out of scope of a rollup stack. Fabric aims to deliver a complete set of tools—such as standards, APIs, contracts, and other essential components—required to reduce frictions with choosing to go based. Some of these components are public goods that require coordination and sustained development.

Does this compete with L2s already being developed and flourishing or based rollup efforts already underway?

- No, Fabric does not compete with existing L2s or based rollup efforts. Instead, it seeks to identify common infrastructure, standardize it, and sustain it as public goods. Rather than compete, Fabric aims to reduce development friction for upcoming based rollups and existing rollups to become based.

Given the significant resources invested, why hasn’t a coordinated effort like this emerged earlier for L2s? What lessons can we apply now to ensure the success of this initiative?

- When L2 teams first began building, they faced the challenge of pioneering new technologies without the benefit of established frameworks or insights into the long-term implications of their design choices. Each team had to operate independently and innovate from the ground up. Now, in 2025, the ecosystem has matured significantly. The community has a clearer understanding of best practices, trade-offs, and the impact of various implementations. This perspective allows us to rethink the process and design an approach that is more aligned with Ethereum’s core principles from the outset.

Is this just another standards working group?

- This effort is about coordinating with stakeholders to agree and align on standards and then ship the necessary components. This will require cross-team discussions and coordination to develop minimum viable implementations.

Is the team developing this plan to launch their own rollup?

- No, the team will not launch its own rollup. The focus is on developing and maintaining minimal open-source components that serve the Ethereum ecosystem as a whole. Any reference implementation stacks are solely meant to be references for the community and ideally are developed by various rollup teams.

Will the team launch a token or monetize?

- No, the Fabric initiative will not launch a token or engage in monetization. The effort is designed to be governance-minimized with no venture backing or business model, ensuring it remains a public good for the Ethereum community.

Is Fabric finalized?

- No, Fabric is still under development. While the team has begun work on key components and initial conversations with various teams, the exhaustive list of components and their designs has not yet been finalized. We are working with the community to identify, define, and refine the specs, and we expect to ship parts of Fabric in the coming weeks to months. Please reach out if you’re interested in helping!

**Conclusion:**

We are excited to continue this effort, promote collaboration, and advance the coordination and development of Ethereum’s ecosystem. If you would like to help, please [reach out](https://x.com/Commit_Boost).

## Replies

**GregTheGreek** (2025-01-30):

Awesome work!

I would love to see more research put into fee markets:

- Blobs should realistically have different priorities based on the type of rollup. I’d assume based/native rollups should have priority and potential discounts for being so tightly coupled to the validators.
- What does sequencer revenue mean, and ensuring that rollups who are bringing the edge/onboarding/orderflow of users are properly reimbursed.

---

**cankisagun** (2025-02-01):

Love the initiative.

I am curious how a shared bridge and a custom settlement layer will work together though. Different proof systems have different risks, having a shared bridge where you bear the risk of another proof is not acceptable to me. Let me know if I’m missing something

I feel the biggest value add of based rollups is synchronous composability. For that to provide value we need to better understand how preconfs pricing is going to work. I think this is the most underexplored area.

As t1, we would be happy to contribute

---

**kustrun** (2025-02-04):

Appreciate [@DrewVanderWerff](/u/drewvanderwerff) for starting and leading the **FABRIC** initiative. ![:raised_hands:](https://ethresear.ch/images/emoji/facebook_messenger/raised_hands.png?v=12) I believe its goals are well-defined and will make it easier for others to understand and seamlessly build their own based rollups. The timing is right, as there are now sufficient examples to establish clear standards.

What excites me the most is the **standardization** - it provides clear guidelines while still allowing plenty of room for experimentation.

You may already be aware, but a group of developers and researchers has formed around **Blob Sharing**. Right now, discussions are mostly focused on **Blob Aggregation**, but it’s clear this is just an intermediate step - essentially a pre-phase of based sequencing - toward building **shared blobs by based sequencers**.

---

**jtremback** (2025-02-04):

Is this working towards synchronous interoperability- i.e. contract calls between rollups?

---

**DrewVanderWerff** (2025-02-05):

Yes, generally Fabric is looking to help accelerate based sequencing which is aimed to help (along with other improvements) to get this!

