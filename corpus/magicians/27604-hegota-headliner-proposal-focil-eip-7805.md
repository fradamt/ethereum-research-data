---
source: magicians
topic_id: 27604
title: "Hegotá Headliner Proposal: FOCIL, EIP-7805"
author: soispoke
date: "2026-01-27"
category: Magicians > Primordial Soup
tags: [hegota, headliner-proposal]
url: https://ethereum-magicians.org/t/hegota-headliner-proposal-focil-eip-7805/27604
views: 310
likes: 9
posts_count: 2
---

# Hegotá Headliner Proposal: FOCIL, EIP-7805

*Thanks to [Jihoon](https://x.com/jih2nn),[Julian](https://x.com/_julianma), [Nixo](https://x.com/nixorokish) and [Caspar](https://x.com/casparschwa) for their feedback and comments.*

### Summary (ELI5)

**FOCIL** as specified in [EIP-7805](https://eips.ethereum.org/EIPS/eip-7805) stands for **FO**rk **C**hoice–enforced **I**nclusion **L**ists, which is currently considered for inclusion (CFI) in the **Hegotá** fork. It significantly improves transaction inclusion guarantees by enabling multiple validators to participate in block building.

#### Champions: ,

### Detailed Justification

#### Why does it matter?

***Primary benefit: Censorship resistance***

FOCIL guarantees that any protocol-valid transaction gets included onchain within a bounded timeframe. By limiting the ability of centralized intermediaries to arbitrarily filter transactions, it preserves fair and equal access to blockspace, ensuring Ethereum remains the most credibly neutral venue to transact onchain.

***Secondary benefit: Safe scaling***

As Ethereum scales (e.g., gas limit increases) and moves toward zkEVMs, it increasingly relies on sophisticated provers and builders. FOCIL prevents these specialized actors from selectively excluding public transactions, effectively decoupling censorship resistance from the centralization of block production.

#### Why now?

A solution to mitigate censorship risks from builder market centralization is long overdue. The builder market is inherently prone to centralization due to MEV and [private order flow](https://dune.com/dataalways/private-order-flow), and vertical integration across builders, relays, and searchers continues to increase.

Ethereum should provide a protocol-level guarantee of fast, reliable inclusion for [all valid transactions according to protocol rules](https://ethresear.ch/t/uncrowdable-inclusion-lists-the-tension-between-chain-neutrality-preconfirmations-and-proposer-commitments/19372), rather than leaving inclusion subject to external preferences. Without FOCIL, this core Ethereum value is not actually guaranteed, leaving the protocol vulnerable to mass censorship events.

### Stakeholder Impact

**For validators**, FOCIL is a meaningful step towards enabling them to contribute to preserving CR without having to be a local builder and sacrifice MEV rewards.

**For users and applications**, shipping FOCIL means:

- Institutions can trust that competitors can’t quietly bribe or pressure a handful of service providers to delay their transactions from landing onchain. It reduces counterparty risk.
- L2s can shorten their withdrawal windows, offering smoother UX and stronger interoperability. That means faster exits and lower costs for cross-chain swaps.
- Everyday users buying ETH with stablecoins get the same protocol-level inclusion guarantees as large funds rebalancing their portfolios. A good example is borrowers on lending protocols, who need to get their transactions included without fear of being blocked from topping up collateral to avoid liquidation.

And the list goes on, as a wide range of users and applications benefit from strong transaction inclusion guarantees.

### Tradeoffs and limitations

FOCIL is broadly accepted as the best design to improve inclusion guarantees for censored transactions. Most of the pushback against [shipping FOCIL in Glamsterdam](https://ethereum-magicians.org/t/focil-readiness-for-hegota/27245#p-65864-what-is-eip-7805-status-today-4) concerned prioritization and fork scope.

That said, FOCIL does come with some tradeoffs and design choices:

- Protocol complexity: FOCIL adds a new role/duty and related deadlines within a slot, and inclusion lists will consume bandwidth (128 KiB in total).
- No support for blobs: FOCIL doesn’t support blob transactions.
There is active, ongoing work on solutions to improve inclusion guarantees for blobs (i.e., using blobpool tickets). We consider this a high priority, but given the different properties between regular transactions and blobs (especially on determining their availability), we think blob CR should be addressed as an independent EIP, shipped in a subsequent fork.
- No support for MEV transactions: Including a transaction via FOCIL means it becomes public, making it ill-suited for MEV-carrying transactions.
In-protocol censorship resistance for MEV transactions could be achieved using encrypted mempools (e.g., EIP-8105, Sealed transactions). FOCIL is a strong primitive that could easily be built upon to support encrypted mempools in the future, but given their complexity, we think it should be proposed as a separate EIP.
- Not much censorship happening on the network recently: Today very few transactions are censored by dominant builders and relays.
However, this was not always the case, and it can change suddenly and unpredictably. Our view is that Ethereum should be designed to be robust and resilient for decades to come and proactively preventing large-scale censorship through reliable inclusion guarantees, rather than being caught off guard and having to react.
- Bypassability: Censoring proposers and builders can bypass FOCIL by missing a slot or producing a full block filled with arbitrary transactions.
However, this comes at the expense of proposer rewards and exponentially increasing base fees, respectively. Ongoing work on missed slot penalties or fallback proposers also aims to address this gap.

### Technical Readiness

FOCIL demonstrates [a high level of technical readiness](https://github.com/jihoonsong/focil-for-implementors/wiki/FOCIL-for-Implementors). FOCIL specifications have been reviewed, and 8 out of 11 clients have implemented FOCIL prototypes, 2 of which were developed by community members. Both specifications and prototypes are ready to be rebased onto Glamsterdam once available.

### Security & Open Questions

FOCIL ([EIP-7805](https://eips.ethereum.org/EIPS/eip-7805)) includes clear mitigation strategies for key security risks such as consensus liveness, IL equivocation, and fork-choice related changes, all detailed in the EIP. The design is also compatible with Native AA ([EIP-7701](https://eips.ethereum.org/EIPS/eip-7701)) and other proposals including BALs ([EIP-7928](https://eips.ethereum.org/EIPS/eip-7928)) and ePBS ([EIP-7732](https://eips.ethereum.org/EIPS/eip-7732)).

## Replies

**lex-node** (2026-01-27):

simply here to say I strongly agree with all of the above and support FOCIL to headline **Hegotá !!!**

