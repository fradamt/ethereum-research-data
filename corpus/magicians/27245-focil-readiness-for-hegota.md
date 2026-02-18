---
source: magicians
topic_id: 27245
title: FOCIL Readiness for Hegotá
author: jihoonsong
date: "2025-12-19"
category: Magicians
tags: [hegota]
url: https://ethereum-magicians.org/t/focil-readiness-for-hegota/27245
views: 378
likes: 7
posts_count: 2
---

# FOCIL Readiness for Hegotá

by [Thomas Thiery](https://x.com/soispoke) and [Jihoon Song](https://x.com/jih2nn), December 20th 2025

*Thanks to [Nixo](https://x.com/nixorokish) for valuable feedback and comments on this post.*

### What is FOCIL?

**FOCIL** stands for **FO**rk **C**hoice–enforced **I**nclusion **L**ists and is described in [EIP-7805](https://eips.ethereum.org/EIPS/eip-7805), which is currently considered for inclusion (CFI) in the **Hegotá** fork. It significantly improves inclusion guarantees for Ethereum transactions by enabling multiple validators to participate in block building.

### Why does it matter?

FOCIL strengthens Ethereum’s censorship resistance and credible neutrality by ensuring that *any transaction valid under the protocol is included onchain* in a timely manner.

By constraining the ability of centralized, trusted intermediaries to arbitrarily filter transactions, FOCIL preserves fair and equal access to high-quality blockspace and ensures Ethereum remains the most reliable venue to transact onchain.

### Who is it for?

FOCIL is crucial **for the future of the Ethereum protocol**. It allows us to safely start scaling to gigagas per second using zkEVMs, by letting sophisticated provers and builders go [beast mode](https://blog.ethereum.org/2025/07/31/lean-ethereum) while keeping them in check and making it extremely difficult to arbitrarily exclude public transactions.

**For users and applications**, shipping FOCIL means:

- Institutions can trust that competitors can’t quietly bribe or pressure a handful of service providers to stop their transactions from landing onchain.
- L2s can shorten their withdrawal windows, offering smoother UX and stronger interoperability. That means faster exits, cheaper bridging, and lower costs for cross-chain swaps.
- Stablecoin issuers and tokenized assets gain reliable, predictable inclusion across geographies and market conditions.
- Everyday users buying ETH with stablecoins get the same protocol-level inclusion guarantees as large funds rebalancing their portfolios.
- Borrowers on lending protocols can get critical transactions included when it matters most, without fearing someone can block them from topping up collateral to avoid liquidation.

And the list goes on: from onchain games to payments apps and social protocols, a wide range of users and applications benefit from stronger, more reliable inclusion guarantees.

### What is EIP-7805 status today?

FOCIL was [considered for inclusion (CFI) in Glamsterdam](https://forkcast.org/calls/acdc/162#t=5024) and had strong support from both the community and core devs. The community rallied behind the feature that represents Ethereum core values, posting forkcast EIP tier lists on social media or taking the time to share preferences on [public forums like ethereum-magicians](https://ethereum-magicians.org/t/soliciting-stakeholder-feedback-on-glamsterdam-headliners/24885/2).

Ultimately, it was left out of Glamsterdam to keep the testing scope manageable given new objectives to achieve a 6-month fork cadence, not due to any technical concerns. As we outlined the scope of Glamsterdam, we are now turning to the headliner-selection phase for the next fork, Hegotá. Given the [continued support](https://x.com/soispoke/status/1989023520240574555), FOCIL has been preemptively **CFI’d as a headliner for Hegotá**.

### How ready is it?

FOCIL demonstrates a high level of readiness. FOCIL [specifications](https://github.com/jihoonsong/focil-for-implementors/wiki/FOCIL-for-Implementors#specifications) have been reviewed and [8 out of 11 clients](https://github.com/jihoonsong/focil-for-implementors/wiki/FOCIL-for-Implementors#client-implementations) have implemented FOCIL prototypes, 2 of which were developed by [community](https://hackmd.io/@pellekrab/SyIkHIweWl) [members](https://hackmd.io/sy_M9JNcTTCiPcdeuVAM3A). Both [specifications](https://github.com/ethereum/consensus-specs/pull/4714) and [prototypes](https://hackmd.io/@jihoonsong/rJX-fxADxl) are ready to rebase onto Glamsterdam once available.

## Replies

**abcoathup** (2026-01-08):

## FOCIL opposers

Is there a list of the [core dev](https://forkcast.org/calls/acdc/170?chat=00:40:36) and [non core dev](https://x.com/ameensol/status/1958781727767412816) opposers points?

How have these points been rebutted?

## Timeline

Can Hegotá with FOCIL as a headliner be delivered in 2026?

Assuming latest mainnet date is December 9 then testnet release(s) would be required by October 3 (at the latest).  [ACD Planning Sandbox - Forkcast](https://forkcast.org/schedule/)

How much development and testing can be done in parallel with Glamsterdam?

## Resources

- https://meetfocil.eth.limo/
- https://censorship.pics/
- https://x.com/VitalikButerin/status/2008174642066845778

