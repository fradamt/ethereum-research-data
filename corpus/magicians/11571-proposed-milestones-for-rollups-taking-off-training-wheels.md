---
source: magicians
topic_id: 11571
title: Proposed milestones for rollups taking off training wheels
author: vbuterin
date: "2022-11-02"
category: Magicians > Primordial Soup
tags: [rollups, decentralization]
url: https://ethereum-magicians.org/t/proposed-milestones-for-rollups-taking-off-training-wheels/11571
views: 55932
likes: 104
posts_count: 14
---

# Proposed milestones for rollups taking off training wheels

There are currently a large number of (optimistic and ZK) rollup projects, at various stages of development. One pattern that is common to almost all of them is the use of temporary **training wheels**: while a project’s tech is still immature, the project launches early anyway to allow the ecosystem to start forming, but instead of relying fully on its fraud proofs or ZK proofs, there is some kind of multisig that has the ability to force a particular outcome in case there are bugs in the code.

L2beat’s risk analysis page shows a large amount of stats about various rollups, including the status of their training wheels:


      ![](https://l2beat.com/static/icon.c58a8403.svg)

      [L2BEAT](https://l2beat.com/scaling/risk/)



    ![](https://l2beat.com/static/meta-images/scaling/risk-analysis/opengraph-image.d12777e4.png)

###



Understand the risks of Ethereum scaling solutions using L2BEAT’s assessments.










However, as of today this information is not well-standardized, making it difficult for users to understand what specific trust model a particular rollup is using. Rollup teams may even have the incentive to keep quiet about their present-day trust model, focusing the discussion instead on the fully-trustless tomorrow.

This post proposes a simple milestone-based schema to help us categorize rollups into three different stages, depending on how heavily they rely on their training wheels. This is intended to achieve a few goals:

1. Make it easier for users to identify the extent to which a particular rollup depends on “trust in a specific group of humans” vs “trust in code”
2. Help motivate rollup projects to improve on their trust models, reducing the risk that trust minimization gets deprioritized because it is “less visible” than eg. flashy UX improvements
3. Give the ecosystem some precise milestones to coordinate around and celebrate, letting us say when “The Surge” is half-complete or fully complete, paralleling “The Merge”

This schema is NOT intended to imply a moral judgement that movement to maximum trust in code as quickly as possible is the only correct course of action. **Rollups absolutely should have a clear roadmap to taking off training wheels, but they should take training wheels off only when they are ready**.

## The Schema

### Stage 0: full training wheels

Requirements:

- The project should call itself a rollup.
- All rollup transactions should go on-chain.
- There should exist a “rollup full node”: an independently runnable software package that can read the L1 chain, extract and the rollup chain, and compute the current state of the rollup chain. If it disagrees with a rollup state root posted into the contract, it should give an alarm.
- There should be machinery that allows users to either post rollup transactions or at least ensure a withdrawal of their assets with no cooperation from the operator. That is, the operator cannot freeze or steal users’ assets by censoring users; their only possible tool for doing so must be to post a false state root.
- It’s okay if the on-chain mechanism for posting new state roots is simply a multisig, with no active fraud proof or validity proof whatsoever.

### Stage 1: limited training wheels

Requirements:

- There must be a running fraud proof or validity proof scheme, which has the practical authority to accept or reject which state roots get accepted by the rollup contract.
- There can exist a multisig-based override mechanism (“security council”) that can override the fraud proof or validity proof system’s outputs and post state roots, to be used in case the proof system code is bugged. However:

The multisig must be 6 of 8 or stricter (that is, >= 8 participants AND >= 75% threshold)
- At least a quorum-blocking group (that is, enough participants to prevent the multisig from acting) must be outside the organization that is running the rollup.

There can exist an upgrade mechanism, but if it has a lower threshold than the multisig, upgrades must have a mandatory activation delay of at least 7 days or the maximum length of the fraud proof game, whichever is longer. The goal of this rule is to ensure that the upgrade mechanism cannot be used to intervene in real-time disputes.

### Stage 2: no training wheels

Requirements:

- In the event that code does not have bugs, there must not be any group of actors that can, even unanimously, post a state root other than the output of the code

This somewhat awkward phrasing (“IF the code does not have bugs, THEN no one can override it”) is meant to permit use of security councils in ways that are clearly limited to adjudicating undeniable bugs, such as the following:

- The rollup uses two or more independent implementations of its state transition function (eg. two distinct fraud provers, two distinct validity provers, or one of each), and the security council can adjudicate only if they disagree - which would only happen if there is a bug
- If someone submits a transaction or series of transactions that contains two valid proofs for two distinct state roots after processing the same data (ie. “the prover disagrees with itself”), control temporarily turns over to the security council
- If no valid proof is submitted for >= 7 days (ie. “the prover is stuck”), control temporarily turns over to the security council
- Upgrades are allowed, but must have a delay of >= 30 days

## Replies

**jessepollak** (2022-11-03):

Thank you for documenting this proposed framework. Agree that it would be very useful to have a defined framework for rollup classification as they progress through various stages of training wheels.

From the Coinbase perspective, this would be a valuable resources for presenting our users with a standardized risk assessment as they interact and move assets across different rollups. We would be excited to collaborate on fleshing this out and making this a resource that can be standardized across the broader ecosystem.

As currently specified, this seems like a reasonable v0 that we can expand on. One additional requirement I might suggest would be to encode something about the fraud proof or validity proof mechanism being available in such a way (e.g open source) that it can be reviewed by 3rd parties.

---

**smartcontracts** (2022-11-03):

Like [@jessepollak](/u/jessepollak) said, I think this is a good v0 proposal that would benefit the entire rollup ecosystem. As more and more assets are held in rollups, it’s becoming increasingly important for users to have a clear understanding of the security model of the system they’re using. A standardized security framework is going to be a key part of this.

My primary feedback is that there are “nice to haves” that aren’t necessarily covered by a framework like this that can have a real impact on the overall security of the network. For example, the ability to easily preview and upgrade and understand its implications can be the deciding factor between a bug slipping through and a secure system. Of course, that’s not *strictly* required but, like I said, it’s a nice to have that has a real impact.

IMO a good v1 version of a framework like this looks sort of like a tech/skill tree. You have specific key requirements that are necessary for advancement to the next stage but you can also unlock bonus items that give you “points” but aren’t requirements for advancement. You might be able to extend this model by assigning points *and* required features such that the requirement for advancement is X number of points and some set of necessary features. Assigning points also reflects the relative value of different features (especially non-critical features) and can help teams prioritize their work.

I’d really like to see comments on this proposal from other rollup teams so we can start to build consensus. Generally, the sooner the better with a framework like this. Rollup risk is only increasing and this is a critical first step in pushing rollups towards *real* security.

---

**frangio** (2022-11-03):

Are permissioned fraud/validity proof schemes considered Stage 1 in this proposal?

---

**vbuterin** (2022-11-03):

I would say yes, as long as any of the members of the security council can initiate the proof. That would be a 1-of-8 trust model, a higher trust-minimization bar than the 3-of-8 assumption already inherent in the multisig.

---

**ittaiab** (2022-11-05):

An upgrade delay of 7 or 30 days is a safety vs liveness trade off that favors safety by forcing a liveness delay - this sounds reasonable  But what if there is an urgent need to upgrade quickly? Say a zero day attack or a bug that may enable an attacker to drain funds in a few days? Recall the DAO fork (upgrade) had some urgency. Perhaps a higher level committee (or social consensus?) should allow faster upgrades. One way is via an on chain governance mechanism driven by eth validators or other (more specific) stake holders…

---

**vbuterin** (2022-11-06):

> But what if there is an urgent need to upgrade quickly? Say a zero day attack or a bug that may enable an attacker to drain funds in a few days?

Then we’re screwed, and that is a risk that we have to take. This is an unavoidable tradeoff: if we want the system to be secure against 51% attacks on the governance layer, then we have to sacrifice the ability of benign 51% collusions in governance to fix broken code.

Ideas around combining multiple proof systems and only turning on governance when they disagree (the reasoning being that it’s very unlikely they would all be bugged in the same direction) is the best that I can come up with to get the best of both worlds here.

---

**robioreefeco** (2022-11-07):

is there an official rollup emoji for community members? ![:newspaper_roll:](https://ethereum-magicians.org/images/emoji/twitter/newspaper_roll.png?v=12) or ![:cyclone:](https://ethereum-magicians.org/images/emoji/twitter/cyclone.png?v=12) could be great ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**elistark** (2022-11-10):

Jumping in to comment that StarkNet is following a different approach, one that doesn’t quite follow these 3 steps. On one hand, we have the main security technology - validity proofs - turned on from the get go, we’ve never submitted a state update to StarkNet without having a STARK proof for it (same holds for all StarkEx systems). So that maps to somewhere between Step 1 and 2 (currently our upgrade period is less than 30 days, so not Step 2). On the other hand, we have decided to deploy decentralized operation at the sequencer+prover level at the very end. Roughly, the steps we’re taking are thus:

1. Functionality - i.e., having the basic structure of the system, accounts, format, state, fees, etc. This has been completed (well, there’s Cairo 1.0 and regenesis but it’s a soft one, meaning the system is already functional)
2. Performance - this is where we’re at now, and it means increasing TPS.
3. Decentralization - having decentralized everything - provers, sequencers, etc.

The main reason we followed this path is to move fast. Easier to solve functionality and performance when the operators are not yet decentralized.

---

**krzkaczor** (2022-11-14):

Kris from L2BEAT team here.

I love the proposal. One of the things we struggle with in L2BEAT is explaining difficult technical terms to non-tech-savvy users. [The risk framework](https://l2beat.com/scaling/risk/) is great, but it’s full of technical jargon. A precise categorization would definitely help us explain risks to users in an easier to comprehend way.

To give folks some idea, with the current framework:

- Stage 0 rollups: Optimism (missing FPs),
- Stage 1 rollups: Arbitrum (FPs are behind a whitelist) + with small adjustments to msig structure zkSync v1 and dYdX could be listed here,
- Stage 2 rollups: Fuel v1,

Here’s a (very) quick mockup of how we could present such info to the user:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b550fba84b0577d00f20e093618c010da1c99686_2_690x185.png)image2300×618 197 KB](https://ethereum-magicians.org/uploads/default/b550fba84b0577d00f20e093618c010da1c99686)

**Few points:**

- IMO naming should indicate that “Stage 2” is final and desired. Maybe instead of naming stages with numbers, we should use tiers like “Tier A - Fully secured by Ethereum”, “Tier B - Limited security“, “Tier C - Under construction”
- In Stage 0, “rollup full node” for zk rollups might not meet this criteria as often zk rollups don’t push all tx on chain but only state diffs.

---

**vbuterin** (2022-12-08):

> Here’s a (very) quick mockup of how we could present such info to the user:

That looks great to me! It would definitely be much clearer to newbies than the current risk framework, which has excellent info but doesn’t really help users understand which properties are more important.

Though perhaps rename “stage” to something clearer like “security level”. And happy to accept alternate namings, tier etc.

> In Stage 0, “rollup full node” for zk rollups might not meet this criteria as often zk rollups don’t push all tx on chain but only state diffs.

Ooh, good point. I guess there are a few paths to take:

1. Accept that for rollups that only publish state diffs, a “full node” would just play the state diffs to compute the current state
2. The rollup must offer a ZK-SNARK verifier that attempts to verify that there are valid transactions that created the transitions, though it’s ok if it’s not “plugged in” and these SNARKs are only published with a delay
3. Make the decision that rollups that only publish state diffs are “not rollups” until they get to stage 1

I’m inclined to lean toward (1) particularly if we brand “stage 0” as “under construction”, because then users would understand that that’s what stage 0 means and it has very few guarantees. But something like (2) could work too. Maybe survey the ZK-EVM teams on this to get their views?

---

**Bartek** (2023-01-31):

Hey all, Bartek from l2beat here. We are in the process of finalizing the implementation of the ranking which will be released soon. We are hoping for one last final feedback - please check out l2beat forum post and consider providing your feedback


      ![](https://europe1.discourse-cdn.com/flex017/uploads/l2beat/optimized/1X/f797c2a34c68dab95d03786717fdee5ea664e06e_2_32x32.png)

      [L2BEAT – 31 Jan 23](https://forum.l2beat.com/t/rollup-maturity-ranking-proposal-call-for-final-feedback/119)



    ![image](https://europe1.discourse-cdn.com/flex017/uploads/l2beat/original/1X/8fc23bf2d7a6581a9e488d0ecdb3ac74d7c61668.png)



###





          Methodology &amp; Framework






After numerous discussions with the whole l2beat team we have decided to have another round of community feedback before finally releasing our implementation of a “rollup maturity ranking” which is our interpretation of what has been proposed by...



    Reading time: 7 mins 🕑
      Likes: 20 ❤











As a teaser, we are still trying to decide if we should go with a simple, linear ranking as proposed by Vitalik, or it is better having slightly more complicated (but hopefully still easy to understand) more multi-faceted maturity ranking that could look like the following mockup.

Have your say ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

[![image](https://ethereum-magicians.org/uploads/default/original/2X/c/cdef887caca5a85f94bb8fd0d2bdc64151f3b97c.png)image438×420 44.5 KB](https://ethereum-magicians.org/uploads/default/cdef887caca5a85f94bb8fd0d2bdc64151f3b97c)

---

**KevinLiu** (2024-01-10):

**The Path to Decentralization**

By Kevin Liu, [Metis](https://www.metis.io/) Co-Founder and [ZKM](https://www.zkm.io/) CEO

In the evolving landscape of blockchain technology, the concept of decentralization has emerged as a guiding principle, especially for Ethereum, where decentralization is the key differential factor and advantage compared with other blockchain ecosystems. However, the problem remains the same now as it did going back to Ethereum’s first baby steps: How do we get there?

As in this post, Vitalik proposed milestones that Ethereum rollups would need to take to achieve full functionalities and true decentralization. By making it through these stages, rollups would shed their training wheels and meet the most challenging of the three sides of the Blockchain Trilemma.

Vitalik’s proposal did a great job of outlining the What: rollups should become fully functional and technically decentralized. However, decentralization is not just on the technology side, it is a complicated architecture we need to build, so How, exactly, do rollups reach that elusive Decentralization goal?

Having co-founded Metis and then leading a project that’s building infrastructure to enable hybrid rollup technology (ZKM), it’s that How which keeps me up at night.

# Stages of Decentralization: A Strategic Blueprint

The journey to full decentralization unfolds in four stages.

## Stage 0: Cold Start - Laying the Foundation for Decentralization

Stage 0, the “Cold Start,” initiates the blockchain project and focuses on establishing robust infrastructure. Similar to a heavy construction phase, a core team takes a central role in development and management. While encouraging general community participation, challenges arise in wielding control during this heavy construction phase.

In Stage 0’s complexities, community involvement is integral. While the core team leads heavy construction, projects encourage community participation with activities such as voting and token delegation. The problem is that these activities offer only a superficial sense of decentralization within limited parameters.

To truly advance decentralization, strategic community engagement is crucial. Beyond token-based voting, it’s important to foster genuine community ownership through transparent communication, education, and collaboration. Building a community truly invested in the project’s success lays the groundwork for meaningful decentralization.

Stage 0 Tldr;

- Objective: Lay the groundwork for the business.
- Key Focus: Establish a solid foundation for future development and decentralization efforts.
- Approach: Concentrate on efficiency and execution by building your team, while giving the community a feeling of ownership, if not yet literal ownership.

## Stage 1: Infrastructure Decentralization - Unleashing the Power of Utility Tokens

Utility tokens play a dual role in Stage 1. Beyond transactional utility, they become instruments of network security and decentralization. True contributors use utility tokens for staking, mining, voting, and governance, actively shaping the project’s trajectory.

### Empowering True Contributors: A Collaborative Construction Approach

Stage 1 heralds an era where infrastructure construction and operation are no longer exclusive to a central authority. True contributors, actively fostering network growth, gain tools and incentives for critical processes. This democratization aligns with decentralization principles and nurtures collective ownership.

Recognizing the significance of infrastructure decentralization is paramount. As the network infrastructure becomes more decentralized, it becomes more resilient, adaptive, and capable of withstanding the challenges that may arise in the dynamic landscape of blockchain technology.

By removing single points of control, leveraging the power of utility tokens, and empowering true contributors, blockchain projects set the stage for a more robust and participatory ecosystem. This evolution is not an isolated accomplishment but a strategic stepping stone towards a decentralized future.

Stage 1 Tldr;

- Objective: Remove technical single points of control.
- Key Focus: Distribute control and ownership of essential components, utilizing utility tokens to secure the network.
- Approach: Enable true contributors to participate in infrastructure construction and operation, fostering a more resilient and censorship-resistant network.

## Stage 2: Revenue Sharing - Aligning Interests for Sustainable Growth

Many blockchain projects and ecosystems struggle to handle the diverging goals of short-term token holders vs. long-term stakeholders (such as the core team and key contributors). Short-term token holders prioritize immediate price movements, seeking quick returns, while long-term stakeholders want to build a sustainable future.

### Shifting Mindsets: From Airdrop Farming to Ecosystem Participation

The key to resolving these conflicts lies in transforming community members’ mindset. Moving beyond the tendency to join an ecosystem solely for airdrop farming, participants must embrace a more active role in the growth of the ecosystem. This shift entails an understanding that rewards are earned through active participation rather than passive speculation.

### Metis: Decentralizing Sequencers through Revenue Sharing

An illustrative example of this transformative approach is Metis’ decision to decentralize its sequencer. Metis adopts a model of revenue sharing with all node operators, creating a system where token holders can stake their assets to earn revenue and mining rewards. This approach establishes a direct correlation between community participation, staking to secure the network, and the overall value of the Metis network.

### Ecosystem Growth and Stakeholder Benefits

The beauty of this model is its self-reinforcing nature. More active nodes and increased community participation lead to higher levels of staking, enhancing the network’s security. As the Metis ecosystem expands, attracting more dApps and builders, the overall value of the network grows. Consequently, all stakeholders, whether short-term or long-term, benefit from the prosperity of the ecosystem.

### Aligned Interests: A Prerequisite for Sustainable Development

Stage 2 focuses on aligning the interests of all parties involved in the ecosystem. By incentivizing active participation and contribution over passive speculation, blockchain projects can foster a community that is genuinely invested in the long-term success of the network. The shift from short-term gains to a collective vision of sustained growth ensures that the interests of all stakeholders are harmonized, creating a foundation for sustainable development.

Revenue sharing is not just a mechanism for distributing rewards; it is a transformative force that reshapes community dynamics and aligns the interests of diverse stakeholders. As exemplified by Metis, this approach sets the stage for a decentralized ecosystem where every participant is not just a beneficiary but an active contributor to the shared success of the project.

Stage 2 Tldr;

- Objective: Align the interests of short-term token holders and long-term builders.
- Key Focus: Introduce revenue-sharing mechanisms to incentivize active community participation.
- Approach: Shift the community mindset from short-term gains to active participation in ecosystem growth, exemplified by models like Metis, where revenue-sharing encourages collaboration and contribution.

## Stage 3: Full Governance - Navigating Complexities with Dual-Layered Governance

The end goal in this whole journey is to establish a comprehensive governance structure that harmonizes the interests of the broader community, small token holders, and key stakeholders. While token amount-based voting power can risk being dominated by large holders, a more nuanced approach is required. The solution lies in drawing inspiration from modern political structures, to create a dual-layered governance system that ensures inclusivity and balances the influence of various stakeholders.

### Addressing the Giant Whale Conundrum

The challenge at this stage is twofold: empowering small token holders to impact ecosystem decisions, and preventing the undue influence of huge token holders. A traditional one-layered governance structure, solely based on token amounts, might inadvertently favor the whales, overshadowing the voices of smaller contributors and community members.

### The Dual-Layered Governance Model at Metis: Commons and Eco Nodes

Metis’ dual-layered governance model comprises Commons and Eco Nodes. The Commons, akin to a decentralized autonomous organization (DAO), is where every community member can create, join, and form interest groups. Commons work like the House in most Western political structures. Within Commons, small token holders pool their voting power, staking collectively into the governance platform, thereby amplifying their influence. This collective power allows smaller token holders to have a more substantial say in decision-making processes, counterbalancing the influence of giant whales.

### The Commons as the First Layer of Governance: A Democratic Forum

Within the Commons, members can submit proposals, engage in debates, and collectively decide on matters that impact the ecosystem. This dynamic and inclusive space ensures that even small token holders can actively participate and contribute to the governance of the project. The proposals approved by the Commons then proceed to the second layer of governance.

### The Eco Nodes as the Second Layer: Guardians of Long-Term Interests

The Eco Nodes form the upper layer of governance; they consist of core builders, contributors, and stakeholders deeply invested in the long-term success and growth of the ecosystem. The Eco Nodes work like the Senate in most Western political structures. Unlike the Commons, Eco Nodes hold a dual responsibility – validating proposals and taking decisive action. Their voting power is not solely determined by token amounts; rather, it is intricately adjusted based on Reputation Power. Reputation Power is earned through past contributions, creating a more meritocratic system.

### Striking a Balance and Ensuring Accountability

The dual-layered governance model maintains a delicate balance by enabling small token holders to collectively influence decisions, while the Eco Nodes act as gatekeepers, scrutinizing proposals for rationality and long-term viability. The system is designed to be adaptable, allowing Commons to grow into Eco Nodes when certain criteria are met, while Eco Nodes can be subject to slashing in case of malicious behavior. This checks-and-balances approach ensures accountability and promotes a dynamic and responsive governance structure.

By leveraging the power of collective influence within Commons and incorporating the wisdom and experience of Eco Nodes, Metis aims to ensure a fair and transparent representation of all stakeholders. This innovative governance structure shows a commitment to true decentralization and community empowerment.

Stage 3 Tldr;

- Objective: Build the right structure for different types of stakeholders.
- Key Focus: Create a dual-layered governance model to balance the influence of various stakeholders, including small token holders and key contributors.
- Approach: Establish a Commons layer for community engagement and proposal approval, and an Eco Nodes layer for validation and decision-making, ensuring a fair and accountable governance structure.

# Summary

The time has come to move from general discussion of milestone scaling to concrete, unique steps on the path to decentralization. Becoming the first Optimistic Rollup to decentralize its sequencer and share the revenue is one such step. Another is a dual-layered governance structure that aligns the interests of a blockchain project’s core team with that of its token holder community.

By following steps like these, we can navigate the seemingly conflicting goals of decentralization and growth harmoniously. I can’t wait to see the fresh ideas that other blockchain projects put forth on their own journey.

---

**jawshuafisher** (2025-02-08):

And thank you for sharing at Base Camp, very helpful!

