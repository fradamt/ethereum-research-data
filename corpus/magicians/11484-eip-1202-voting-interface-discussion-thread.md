---
source: magicians
topic_id: 11484
title: EIP-1202 Voting Interface Discussion Thread
author: xinbenlv
date: "2022-10-27"
category: EIPs
tags: [erc, governance-ercs, erc1202]
url: https://ethereum-magicians.org/t/eip-1202-voting-interface-discussion-thread/11484
views: 2586
likes: 4
posts_count: 7
---

# EIP-1202 Voting Interface Discussion Thread

Starting a discussion thread for EIP-1202. The original discussion occurs on [ERC-1202 Voting Standard · Issue #1202 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1202)

A series of efforts were put forward to support general voting standard.

1. EIP-5247 Proposal Interface and its discussion
2. EIP-5732 Commit Interface and its discussion
3. EIP-5453 Endorsement Interface and its discussion
4. ERC-5805: Voting with delegation

## Roadmap

1. Get the right group of ppl, summarize state of art
2. draft 1st version with 1 prototype
3. run hackathon and grants for more implementations
4. draft 2st version.

## Key Questions

1. What function name and parameter to “vote”
2. What’s a proposal represented

## Participation of discussion

- @bumblefudge

# Reference Projects

- https://goverland.xyz
- https://snapshot.org
- https://tally.xyz
- Governor Bravo of OpenZeppelin
- DAOStar
- Safe (Gnosis Safe)
- MetaGov: Qs: Deliberative Tool Interoperability and Innovation Questions {Shared w/Metagov+} - Google Docs
- https://metagov.slack.com/
- Qs: Deliberative Tool Interoperability and Innovation Questions {Shared w/Metagov+} - Google Docs
- Case study: Snapshot & IPFS | IPFS Docs

## Replies

**xinbenlv** (2024-04-20):

Please comment here if you like to collaborate: authoring, implementing reference implementations, adoptionz

---

**bl2** (2024-07-01):

I am interested in the standardization of voting and look forward to implementing it in a project.

Specifically, the governance I envision involves the following stages (which may require a new EIP):

First, determine the issue,

Second, spontaneously set the motion,

Third, cast votes,

Fourth, make the vote public,

Fifth, generate governance decisions,

Sixth, execute the decision.

In the third step,

We want the voting process and the voting results to be privacy-protected,

Because the voting incentives in the sixth step are related to the specific content of the vote.

The specific implementation process is as follows:

the state data stored on the blockchain is obtained by users using an encrypted passphrase for hashing,

and after the public phase, users can reveal their encrypted passphrase.

I wonder if the requirements for the third step can be reflected in the interface?

---

**xinbenlv** (2024-07-02):

[@bl2](/u/bl2) hi!

There are several ways to enable privacy I can think of.

1. commit reveal, which takes 2 casts, can be batched across many voters
2. optimistic proxy: a trusted party submit the votes on voter’s behalf given a voter-signed commitments from each, voter can submit challenge, in which case the trusted party will reveal the signed commitments pre-image so they can avoid fraud challenge. if they fail to counter challenge, they get slashed.
3. zk-proof-based: use ZKP to prove of correct tally amongst a group of voters while no one’s identity is revealed.

All of these implementations can be supported if we properly design the interface.

---

**bl2** (2024-07-07):

I am unsure whether ZKP is the appropriate model because I want the total number of votes to be hidden, and it is not important whether the voting address is hidden or not. and after the reveal phase, all data should be verifiable.

The first strategy maybe acceptable.

Additionally, we would like each proposal to come with two default functions:

One is the function to execute the proposal itself,

The other is the function to incentivize addresses that participate in the voting (the supporters of the selected proposal need to give fair compensation to the supporters of the failed proposal), and the specific incentives are entirely determined by the voting results.

So, I would like to know if the existing proposal (ERC-5247) can support this idea.

---

**xinbenlv** (2025-10-22):

- Just created a PR to move “Review” status: Update ERC-1202: Move to Review by xinbenlv · Pull Request #1294 · ethereum/ERCs · GitHub
- Also created a telegram working-group, please reply if you like to be added to it.

---

**xinbenlv** (2025-11-15):

# Inviting the ERC-1202 Voting Stakeholders to the Table

As we revisit and expand the ERC-1202 Voting Standard, we don’t want to design it in a vacuum.

On-chain voting already powers DAOs, L2s, prediction markets, identity systems, and a wide range of tooling. If ERC-1202 is going to be useful in practice, it needs to reflect the real constraints and requirements of the people who run these systems every day.

This post outlines the stakeholder categories we plan to invite into the discussion, along with a non-exhaustive list of projects in each category. Every listed stakeholder is someone we hope to either interview, co-design with, or invite as a contributor to the standard.

---

## 1. On-chain voting & governance platforms

These are the primary venues where on-chain (or snapshot-style) votes actually happen today. They are the most direct “users” of any voting standard.

- Tally – end-to-end governance UI and infra for many DAOs (Tally)
- Snapshot – off-chain, signature-based voting that many DAOs rely on for signalling (snapshot.org)
- Aragon – long-standing DAO framework with its own governance modules (aragon.org)

---

## 2. High-governance DAOs & L2 ecosystems

These communities run frequent, high-stakes votes and have already accumulated a lot of hard-won governance experience.

- Uniswap DAO – token governance controlling one of the most systemically important DeFi protocols
- Optimism Collective – bicameral governance (Token House + Citizens’ House) with active experiments in public-goods funding (Nansen)
- Arbitrum DAO – one of the most active L2 governance ecosystems, with large on-chain treasuries and delegation dynamics

---

## 3. Smart-contract voting standards & libraries

These teams maintain the core contracts that many DAOs rely on. We want ERC-1202 to integrate smoothly with, and learn from, their designs.

- OpenZeppelin Contracts – widely used governance and token libraries, de-facto standards for many projects (GitHub)
- Solady – gas-optimized Solidity libraries used across the ecosystem (Cantina)
- Ethereum EIPs Repository – the home of existing ERC governance (ERC-20, ERC-721, ERC-1155, ERC-4337, etc.), and thus the broader “standards author” community

---

## 4. On-chain courts, arbitration & challenge systems

Dispute resolution and fraud-proof / challenge mechanisms are tightly coupled to how we interpret votes and resolve edge cases.

- Kleros – decentralized court system already used for many on-chain disputes (Kleros)
- LexDAO – community of “crypto lawyers” building on-chain dispute-resolution and legal primitives for DAOs (hatsprotocol.xyz)
- Zeitgeist – prediction-market chain that also includes a decentralized court and futarchy-oriented governance features (zeitgeist.pm)

---

## 5. Wallets, smart-account & multisig systems

If voting is going to be safe and usable, it has to work with the key-management systems that people actually use.

- MetaMask – the most widely used self-custodial wallet for Ethereum and EVM chains (MetaMask)
- Coinbase Wallet – a major retail wallet with both self-custodial and exchange-adjacent use cases
- Safe – smart-account / multisig infrastructure securing tens of billions of dollars in assets (app.safe.global)

(For multisig-heavy ecosystems, we also plan to reach out to Solana-native smart-account systems such as [Squads](https://squads.so). ([squads.so](https://squads.so/home-copy?utm_source=chatgpt.com)))

---

## 6. Block explorers & on-chain data indexers

Explorers and indexing protocols are how most people *verify* and *analyze* votes. Standards that are easy to index, filter and visualize will have an outsized impact.

- Etherscan – leading Ethereum block explorer and API provider (Ethereum (ETH) Blockchain Explorer)
- Blockscout – open-source explorer stack used by hundreds of EVM networks (blockscout.com)
- OKLink – multi-chain explorer and Web3 data platform (OKLink)
- The Graph – decentralized indexing protocol powering many governance dashboards (The Graph)

---

## 7. Prediction markets & futarchy experiments

Prediction markets stress-test incentive design, information aggregation and governance in ways that are highly relevant to voting standards.

- Polymarket – currently the most prominent prediction market, with growing institutional interest (Polymarket)
- Augur – one of the earliest decentralized prediction-market protocols (Augur)
- Zeitgeist – a chain purpose-built for prediction markets and futarchy experiments (zeitgeist.pm)

---

## 8. Developer SDKs & wallet-connection infrastructure

Voting is ultimately “just” transactions and signatures—SDKs and wallet-connection layers define how easy (or painful) it is to integrate voting into an app.

- ethers.js – one of the most widely used JavaScript/TypeScript libraries for interacting with Ethereum (docs.ethers.org)
- viem – a modern TypeScript interface to Ethereum that many new stacks are standardizing on (snapshot.org)
- WalletConnect – protocol and infra for connecting wallets and apps across many chains (WalletConnect)
- RainbowKit – a React wallet-connection library built on top of wagmi + viem, widely used in dapps (rainbowkit.com)
- Privy – embedded wallet and authentication infra that powers many consumer crypto apps (Privy)

---

## 9. Identity, reputation & Sybil-resistance

Any serious voting standard needs a story for identity, reputation and Sybil resistance—whether it’s 1-token-1-vote, 1-person-1-vote, or something in between.

- Ethereum Name Service (ENS) – a core identity layer for many users and DAOs (app.ens.domains)
- Gitcoin / Human Passport – Sybil-resistance protocol originally launched as Gitcoin Passport, already integrated with governance tools like Snapshot (passport.human.tech)
- Sismo – privacy-preserving attestation protocol for ZK badges and reputation (Taikai)

---

## 10. Governance tooling, research & standards stewards

Finally, we want to collaborate closely with the people who think full-time about governance, verification and standards.

- LexDAO – bridging legal design and on-chain governance (hatsprotocol.xyz)
- Ethereum Foundation – steward of the core protocol and a key co-ordinator of the EIP / ERC process (ethereum.org)
- Certora – formal-verification tooling for smart contracts, highly relevant for specifying and verifying governance logic (CoinTrust)

We also expect to involve governance researchers, DAO designers, and other ERC authors via the [Ethereum EIPs repository](https://github.com/ethereum/EIPs).

---

## What happens next

Over the coming months we plan to:

1. Run structured interviews with representatives from these stakeholder groups.
2. Publish a series of public notes summarizing requirements, pain points and design proposals.
3. Iterate on ERC-1202 in the open, with concrete reference implementations and test cases informed by real production systems.

If you’re involved with any of the stakeholders listed above—or you see a category we’re missing—and you’d like to participate, we’d love to hear from you.

In later posts we’ll share a more detailed roadmap for ERC-1202 and some concrete technical questions where community input will be especially valuable.

