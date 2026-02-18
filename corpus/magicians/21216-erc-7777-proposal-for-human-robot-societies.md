---
source: magicians
topic_id: 21216
title: "ERC-7777: Proposal for Human Robot Societies"
author: Shaohong
date: "2024-09-29"
category: ERCs
tags: [erc, governance, identity, dao, decentralization]
url: https://ethereum-magicians.org/t/erc-7777-proposal-for-human-robot-societies/21216
views: 905
likes: 30
posts_count: 19
---

# ERC-7777: Proposal for Human Robot Societies

> Title: Identity and Governance Interface for Human Robot Societies
> Description: This ERC defines standardized interfaces for managing the identities of humans and robots, establishing and maintaining laws (“rule sets”) that apply to those societies, and standardizing the immigration (“registering”) and emigration (“leaving”) of humans and robots from the rights and responsibilities of those rule sets.
> Author: OpenMind, Jan Liphardt jan@openmind.org, Shaohong Zhong shaohong@openmind.org, Boyuan Chen boyuan@openmind.org, Paige Xu paige@openmind.org
> Status: Draft
> Type: Standards Track
> Category: ERC
> Created: 2024-09-29

The rapid integration of robots into various industries and everyday life presents a unique challenge: how do we efficiently manage interactions between robots and humans in a secure, transparent, and scalable way? Traditional centralized systems often fall short, with issues related to inefficiency, lack of transparency, and limited scalability.

To address this, we propose a new ERC designed to leverage Ethereum’s decentralized infrastructure to facilitate seamless and secure human-robot interactions. By utilizing smart contracts, this ERC aims to provide a verifiable, rule-based ecosystem that ensures security, transparency, and scalability. It could serve as the foundation for managing complex interactions between humans and robots in a decentralized environment, with the potential to set a new standard for the secure and responsible integration of robots into our society.

*We’d love to hear your thoughts on this proposal! We think this ERC could play a key role in shaping the future of decentralized human-robot interactions.*

**Abstract**

This proposal defines two core interfaces: **IUniversalIdentity** and **IUniversalCharter**, providing mechanisms for humans, and robots to establish their identities and to create decentralized communities governed by specific rule sets. The **IUniversalIdentity** interface establishes the fair and equitable treatment of sentient computer architectures other than the human brain, enabling robots to acquire on-chain identities, and thereby interact and transact with humans. The **IUniversalCharter** enables humans and robots to create, join (“register”), maintain (“update”), leave, and terminate self-regulated societies based on predefined rule sets, providing a framework for collaboration and prosperity for mixed societies of humans and robots. These interfaces aim to provide a flexible yet enforceable structure for human-robot interactions in decentralized systems, ensuring efficiency, transparency, and security for all participants.

## Replies

**zzz** (2024-10-02):

This is really interesting! I’m curious what some real-world examples of this would be. For ex, how would this function in industries like healthcare? Smart cities? Manufacturing? Etc.

---

**JamesEBall** (2024-10-03):

Extremely interested to learn more about this, and how it fits in to a broader vision for R2R and R2X communication/messaging

---

**Ddeputy** (2024-10-09):

Hey, congrat on making week in Ethereum news which is how I came across your ERC/git repo.  I’m involved in creating a way for smart contracts and autonomous agents to (prove they) comply with today’s nation state regulations.  Would like to hear your thoughts on how your proposal might be able to integrate off-chain calcs.  Our thesis is there’s simply no way we will re-create all the compliance algos inside blockchain and therefore there’s a need to rely upon web2 apis integrations, potentially adding some fancy “proving” tech to verify they were correctly called/used.  LMK your thoughts and perhaps we can direct connect if  you are attending Devcon?

---

**TangmereCottage** (2024-10-11):

For example, we are now using this to guardrail the behaviour of quadruped robots as they interact with humans and other robots. We write rules into an ERC-7777 complaint contract, and the quadrupeds access this contract and inject those rules into the context of the AI that generates their behavior. A simple example is a rule like “Do not approach humans closer than 50 cm”. This results in a simple, public, and global system where everyone can read what the governing rules are in plain language.

---

**TangmereCottage** (2024-10-11):

Yes, you are right - BTW as you can see there is loads to do.

(1) In terms of `nation state regulations`, a simple bridge could be to mirror nation state regulations in ERC-7777, and robots could certainly voluntarily decide to join that rule set, or be required to as a prerequisite of entering into commercial agreements. That’s easier said than done, due to the complexity of many human rule sets - for example the US IRS tax code changes regularly and is extremely lengthly and complex.

(2) In terms of on-chain, off-chain, and hybrid systems, yes, that needs a lot of thought too. Some rule sets could be private/secret and zk could be used to prove compliance to certain conditions. Please add/edit/change whatever parts of the interface spec you think are missing, or would enhance ERC-7777’s utility.

(3) In terms of the motivating use case, which we are currently using ERC-7777 for, is to store simple rules like Issac Asimov’s **I Robot** governance and behavior rules, for simple *ad hoc* communities of humans and robots that were are currently testing in the SF Bay Area.

---

**TangmereCottage** (2024-10-11):

“**R2R and R2X communication/messaging**” - presumably you mean robot-to-robot and robot-to-human? In terms of any messaging protocol, it’s vital to know with whom you are messaging - that’s a great point. That’s the basis of the internet, for example, where HTTPS allows any two computers to communicate securely (and also establish their identity, at least control of certain crypographic keys). The larger issue is that there is not (yet) a good system for identifying AIs and robots, and as noted by some including Andrew Côté (@Andercot). Trivially, robots and AIs do not have birthdays, fingerprints, or irises, so those will not work from them. One concept for robot identity would be a SHA hash of their model weights, which could also be valuable to give humans trust in any AI they are interacting with. Another concept for robot identity is control of cryptographic keys, just like for wallets today. Please add/edit/fix/markup the ERC-7777 spec to make it as useful as possible for everyone!

---

**Aranna-0572** (2024-10-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shaohong/48/13376_2.png) Shaohong:

> human-robot

Hello, I am Aranna from the DAism team. We are delighted with the ERC-7777 on robot identity. Our team is also working on robot/AI governance initiatives and research. We have the following thoughts regarding your ERC that we hope to discuss with you:

1. We noticed that your rule set may be managed by the owner, which raises questions about centralized vs decentralized management. We would like to know how you assess this aspect. In blockchain, creating a decentralized application requires considering decentralization in the standards as well.
2. Regarding your description of “version,” we would like to understand how the rule set is expanded during upgrades. If V1 upgrades to V2, do the two versions have an inclusion relationship or a parallel relationship in terms of their rule sets?
3. Around the above issues, we would like to know what kind of project you intend to develop with this ERC. I learned some of your ideas through your OpenMind website, which is really cool. However, if it involves blockchain, certain details need to be carefully considered. Additionally, if you are considering making it an open-source project, we could communicate more about this, as we are launching our proposal for incentivizing open-source projects in the blockchain.
Looking forward to your reply : )

---

**Shaohong** (2024-10-13):

Thank you for your interest!

This ERC aims to define the foundational interface for smart contracts that govern human robot interactions in different environments. For example as [@TangmereCottage](/u/tangmerecottage) mentioned, one such rule of interaction for a robot could be to ensure a safe distance from humans. An example where that might be applied is surveillance operations, where robots can be tasked to survey different areas of the plant autonomously. The robots will be bound by the rules defined in their `UniversalIdentity` contracts, which will ensure their safe operation in a transparent and decentralized manner.

Looking ahead, we envision the interface to play a crucial role in managing the integration of robots with Artificial General Intelligence (AGI) or Artificial Super Intelligence (ASI) into our society. In such a scenario, smart contracts can potentially facilitate a verifiable, rule-based ecosystem that ensures security, transparency, and trustlessness, helping to regulate these intelligent robots and smooth the transition to a truly human-robot society.

Would love to hear your thoughts on this!

---

**Shaohong** (2024-10-13):

Thanks for your comment. That is a really good point!

As [@TangmereCottage](/u/tangmerecottage) mentioned, establishing identity is essential for messaging protocols to work. Our interface defines a `UniversalIdentity` contract that can be bound to a robot to establish its on-chain identity and provides a basis for its communication with other agents. The `UniversalCharter` contract can then define the communication protocols between different robots to ensure mutual understanding via the setting of rules. Furthermore, the `UniversalCharter` contracts are designed to be able to work in harmony with each other. We envision the creation of foundational `UniversalCharter` contracts that define basic rules for all robots on-chain (e.g. a communications UniversalCharter contract specifying a messaging protocol that every robot needs to register with to talk to other robots/agents).

---

**Shaohong** (2024-10-13):

Thank you for reaching out, and I’m glad you came across the ERC!

Your point about checking compliance is indeed pertinent, and as [@TangmereCottage](/u/tangmerecottage) said a lot of thoughts and work are required. Our current implementation addresses this by keeping a `complianceStatus` record on-chain, which is updated by a trusted updater responsible for checking and updating the compliance status of a robot-bound `UniversalIdentity` contract. While we allow for the possibility of on-chain checks, the main idea is to offload the actual compliance checks off-chain, because it can be too complex/expensive. The example contract limits the updater to be the owner, but it can be any other trusted, verifiable entity or mechanism. We believe that this system could serve as an efficient solution for compliance checking.

We would love to hear your thoughts!

---

**Shaohong** (2024-10-13):

Hi Aranna, many thanks for reaching out! Your work looks very exciting as well!

1. We agree with your point, and decentralization is a key motivation behind this interface too. In practice, we envision that the UniversalCharter contracts would be managed by decentralized governance systems such as DAOs. To ensure flexibility, this ERC doesn’t lock in any specific form of governance, leaving it up to individual contract developers to decide what works best.
2. This is a great question. In our example implementation, we update the entire rule set, implying a parallel relationship between different versions. This provides more flexibility (e.g. when the V2 rule set removes/modifies from V1)
3. We are currently implementing this to store behavior rules on robot quadrupeds that we are testing in the SF Bay Area. More demos will be released soon and we look forward to continuing the conversation!

---

**JamesEBall** (2024-10-25):

Exactly. I’ve been exploring device identity for robots on decentralized blockchains in a similar way. Just as human identity is closely linked to biometric features, we believe robots could also have a unique, “device-bound” identity, anchored in secure hardware.

In principle, this could be achieved by embedding components like Physical Unclonable Functions (PUFs) into the robot. These PUFs would derive an unalterable private key, making it unique to that robot and providing a tamper-resistant means of identity.

---

**Constantin** (2024-10-31):

Hi guys, nice to read about your ideas and suggestions on the topic of AI agent identity, our interactions with them and AI agent compliance.

After read into the proposal, I’m most curious to your implementation - i.e. why structure the solution in its current form, and what you plan to do with it.

For the UniversalIdentity function, the identity for all subjects on eth is the address, usually there’s no way/no need to identify an on-chain subject as human/robot, thus this new function will be very odd on the protocol level. I believe in 10 years time we will still focusing on helping AI agents to act like human, for the normal “AI agent as human” type of activities, we don’t need to distinguish AI agents on chain.

For the UniversalCharter function, I like the idea, it’s very much like the covenants, so the self-identified AI agent (or human) can participate in multisig or escrow contract in a particular way, very cool thoughts.

If you draft this EIP for the compliance purpose, then the self-identification duty will very much fall on the responsible party (or any party that are afraid to be ruled as responsible party), which would serve as a disclaimer/restriction on AI behavior. But if your AI agent make transactions like human, interact with contracts like human, deposit and withdraw like human, it is human from the blockchain’s pov, this is already the best defense, also sometimes it’s more dangerous to identify potential responsibilities for yourself than let if blend into normal transactions, maybe you should consult lawyers for this particular point.

Also there may be other ways other than adding new eth function, you can build your own dapp for the self-identification and AI agent interaction, for example.

Are you planning to launch any form of product relating to this EIP? Would be very interesting to know!

---

**Constantin** (2024-10-31):

I think the contract here is not necessary, an AI agent controlled address can already freely perform all the interactions you want with address/contracts controlled by another AI agent, and we already have AA stack to help address to communicate with other address.

It will be a pretty terrible idea to build DID like system on top of the current eth address system, that’s just extra burden.

---

**Constantin** (2024-11-01):

After discussing with the author team, I’d like to share some additional thoughts on AI agent related standards, please feel free to comment

AI agents are struggling with web2 regulations and rules, on blockchain they are refrain from the identification as humans, thus I see tremendous potential for blockchain+AI.

There are two distinctive ways to help AI on blockchain, leading to two opposite goals, first is making AI act as human - helping AI to do whatever human is able to do with blockchain, like transactions and interactions, second is making AI act as AI - identify AI as humans using TEE or other technology, thus AI can perform particular actions in better ways, like doing ICOs.

Maybe both goals are achievable but in short term I believe every AI related EIP team should confirm their main goal and which path they are going down.

---

**Ddeputy** (2024-11-01):

I’ve history as both a banking regulatory, a fintech founder, a tax software exec and currently advising governents on on taxation of digital assets while building a web3 compliance startup.  IMHO there’s a couple choices; either a) launch agent and walk away with no “benefical ownership” or (potential for) monetary extraction, or b) don’t do a and be really good at hiding your tracks (go dark), or c) create an artifical person under the law (trust, LLC, corp, recognized dao, etc) for the agent and report benefical ownership as is required under US/ other law as of 2025.  To get a sense of the world I live in here’s an article about a global tax reg being implemented now that requires everyone dox:  [OECD Crypto Tax Reporting Framework challenges Defi | by David Deputy | Medium](https://medium.com/@daviddeputy/oecd-crypto-tax-reporting-framework-challenges-defi-bef10a548c27)  To be clear I don’t believe in dox’ing but existing regs require it.  Without proof that things like ZK DIDs/privacy pools etc, work in practice our ideas aren’t in the overton window of nation state regulators.  Chicken and egg problem, but providing “hooks” for agents to link into complance frameworks would perhaps be a good idea.  Best efforts go a long way when regulators call you out.

---

**futreall** (2024-11-17):

How do you envision addressing the potential ethical dilemmas that might arise when granting robots on-chain identities and equal rights within decentralized societies, especially in cases where their actions might conflict with human interests or societal norms?

---

**donat55** (2024-11-17):

How do the proposed IUniversalIdentity and IUniversalCharter interfaces ensure equitable treatment and secure interactions between humans and robots, and what potential challenges might arise in implementing these standards in decentralized human-robot societies?

