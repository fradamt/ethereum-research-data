---
source: ethresearch
topic_id: 20039
title: L2 Asset Interoperability via Two-way Canonical Bridges
author: wdai
date: "2024-07-10"
category: Layer 2
tags: []
url: https://ethresear.ch/t/l2-asset-interoperability-via-two-way-canonical-bridges/20039
views: 6446
likes: 11
posts_count: 8
---

# L2 Asset Interoperability via Two-way Canonical Bridges

## Motivation

One key problem with the L2 scaling solutions is that assets natively minted on L2s can only be used on the L2 of issuance but it cannot be bridged back to L1 or other L2s, without utilizing external bridges. This creates fragmentation. At the time of writing, there is already half as much natively-minted assets ($12b) on Eth L2s compared to canonical bridged assets ($24b), according to L2Beat.

Shared settlement layers only solve this problem for L2s using the same shared settlement layer. The ecosystem remain fragmented once more shared settlement layer show up.

We propose **two-way canonical bridges** as a solution, where L2-minted assets can be **reverse-canonically bridged** to L1. It is simply an ERC-1155-like interface that an L2 settlement contracts adopt, plus additional precompiles added to the L2 execution environment.

## Two-way Canonical Bridges

Below is a highlevel description of two-way canonical bridging.

- The L2 settlement contract becomes the ledger of record for all native assets issued on it (that have been reverse-canonically-bridged). The settlement contract (on L1) shall implement the ERC-1155 interface, where the asset id field denotes the L2 asset address.
- To send an L2-native asset to an L1 address, the L2 users simply send the asset to a prespecified system address, which shall results in the L2 settlement contract on L1 issuing ERC-1155 tokens to itself. Next, L2->L1 call mechanisms can be utilized to move the newly-issued asset to any desired destination. This is done within the same L2 transaction.
- To send a reverse-canonically-wrapped asset back to its L2 of origin, a special burnAndDeposit function on the L2 settlement contract can be called.
- Since the L2 settlement contract is an ERC-1155 contract, L1 EOAs and other L2s can simply hold assets or wrap them as normal. This requires the L2 canonical bridge to support wrapping of ERC-1155 assets.
- In normal usage, it is expected that the only holders of the ERC-1155 tokens issued by an L2 settlement contract are other L2 settlement contracts. This means that the state overhead on L1 is small.

Additional consideration:

- The safety of an asset is maintained without additional trust assumptions because the L2 settlement contract acts as the ledger of record for all outstanding assets (those owned by other L1 addresses).
- It is assumed that any assets that is reverse-canonically-bridged to L1 addresses is done at the risk of the user initiating the bridging.
- In practice, end-users can utilize fast liquidity bridges while crosschain liquidity providers utilize the two-way canonical bridges to rebalance.
- This mechanism can extend to L3s on L2s. An asset issued on an L3 can be reverse canonically-bridged to L2 and then reverse canonically-bridged back to L1. We’d need the 1155 ids on the settlement contract to be able to represent the 1155 asset id on L2 alongside with the asset address–this can be done via hashing for example.

### Acknowledgements

Thanks to Shumo Chu for review and comments.

## Replies

**Joxess** (2024-07-11):

Hey [@wdai](/u/wdai), I have been very interested in these topics.

Conceptually, any general-purpose Layer 2 should be able to provide a secure messaging layer that allows bridge native L2 assets to L1; follow the exact procedure as we secure bridging L1 assets into L2. For example, the OP Stack address this possibility, and it would be as straightforward as it is today for L1 token bridging: anyone can create a token representation that follows the required interface (commonly via a factory) and then make a deposit into the bridge contract on the origin chain. The underlying message-passing protocol will ensure that the message arrives and is valid. These mechanisms may vary depending on how the L2s implement their respective canonical bridges, but in principle, if the security model can be assumed, then both directions could be equivalent.

Importantly, I believe a key aspect of bridged tokens, including this case, is how the token is implemented and managed in each chain where it isn’t native to meet the expected use cases and fulfill the owner’s requirements. We can distinguish two major groups (intermediates can still exist):

- Classic bridged tokens: When the token is sent to another domain, the issuer/owner will not have any rights over the new representations. This is ideal if the user wants full ownership, provided that the backing is guaranteed, or when the token does not have a “responsible” party. The security model of each representation will solely depend on the security model implemented by the domain.
- Sovereign tokens: The issuer/owner wants to have full control of its implementation. A generalized solution for this is, for example, xERC20, where any issuer can be set, and it is not limited to third-party bridges; canonical or any other method can also work. Others decide to build their own infrastructure, such as Circle.

So, I believe that regardless of the issuer/owner’s choice (which is a critical decision), these current models ensure that a token can move into any domain and that 1:1 transfers are always achieved with any security model. I think many pain points include UX aspects such as times, user actions, and end implementations. I would love to know your thoughts and ideas to achieve better interoperability flows and more elegant token issuing mechanisms.

---

**SebastienGllmt** (2024-07-13):

This is conceptually similar to what we’ve been calling *inverse projections* for sovereign rollups built with Paima Engine. We have fairly extensive docs on the concept as well as an existing Solidity contract for it that we use in production for the app-chain for our game Tarochi: docs.paimastudios [.] com/home/PRCs/prc-5 (sorry for breaking the link - I can’t post URLs here)

---

**donnoh** (2024-07-14):

This is already implemented in all major L2s

---

**MicahZoltu** (2024-07-15):

Nitpick: There are currently no L2s (inherits security from L1), so while this statement is technically true (because `0 * 100% = 0`), it hints at something that may not mean what the reader thinks.  ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12)

---

**wdai** (2024-07-15):

I like your classification on Classic bridged tokens vs. Sovereign tokens. It is clear that Sovereign token issuers will need to take control of the issuing contracts on different chains that they support. My post is strictly about classic bridge tokens and is more of a call-to-arms for the community to come up with better canonical bridge standards so the ecosystem gets less fragmented as more non-sovereign tokens gets minted on L2s.

---

**Joxess** (2024-07-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/wdai/48/8617_2.png) wdai:

> I like your classification on Classic bridged tokens vs. Sovereign tokens.

Thanks!

![](https://ethresear.ch/user_avatar/ethresear.ch/wdai/48/8617_2.png) wdai:

> My post is strictly about classic bridge tokens and is more of a call-to-arms for the community to come up with better canonical bridge standards so the ecosystem gets less fragmented as more non-sovereign tokens gets minted on L2s.

I fully agree with that. I believe the OP Stack `StandardBridge` is a good reference for how to bridge outside of the L2, although its current usage might be limited due to the withdrawal time period. Other L2s should aim to implement similar features. The `OptimismMintableERC20` is also an excellent interface for how the bridge contract can gain the ability to mint and burn assets; many teams have adopted similar interfaces.

However, I still believe the discussion about token interoperability should go further and raise more awareness among token issuers about setting their end goals for their tokens and planning accordingly to become properly interoperable. When a token is moved to a new chain, we need to be clear about what we want to bridge, and generally, there are two reasons:

1. Its monetary value
2. Its utility (export (1) for free)

For (1), there is nothing better than how canonical bridges operate today, as they only mint vanilla representations (e.g. WBTC, LUSD, etc.) and their value is the only thing that matters. But for (2), it is sometimes desirable to port additional properties such as protocol minting rights, voting and delegations (e.g. NEXT, MAI, etc.) or whatever. Since these may require maintenance over time, it would be preferable for the token to remain sovereign and optionally leverage existing bridge security models. There is no uniform solution for (2) and I suspect it will become an increasingly demanding case. I believe xERC20 is one possible candidate.

I am happy to continue discussions like this from a holistic perspective. Through Wonderland we have been contributing to the token bridging vertical for a while (xERC20 and OP Stack token bridging).

---

**Joxess** (2024-11-01):

Recently, we published **ERC-7802**, which contributes in that direction. We would love to receive feedback and discuss any ideas around it.

