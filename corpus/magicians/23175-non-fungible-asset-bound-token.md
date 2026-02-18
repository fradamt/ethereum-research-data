---
source: magicians
topic_id: 23175
title: Non-Fungible Asset Bound Token
author: NickZCZ
date: "2025-03-18"
category: ERCs
tags: [nft, token]
url: https://ethereum-magicians.org/t/non-fungible-asset-bound-token/23175
views: 134
likes: 4
posts_count: 4
---

# Non-Fungible Asset Bound Token

With the rise of numerous digital collectibles and the idea of digital identity, entities must create a second collection when the first one can no longer support the evolution of an idea, or rather simply a new idea overall.

What we see happening repeatedly is the creation of a secondary smart contract, often a secondary collection, that does little for the first. If anything, a negative impact on the first collection can be recorded as the creator must split his attention in 2 when creating a secondary smart contract and collection. Oftentimes, this leads to holders of a collection selling the genesis tokens / their assets on the market, in an attempt to get a more sought-after asset within collection 2. The result is liquidity being pulled from the 1st collection, and allocated into the second, rarely benefiting the first collection in any way.

In a different setting, we can observe the issuance of IDs happening in every nation, such as a passport, state ID, or social security number. These documents can be used to not only identify oneself but also to link individuals to their healthcare insurance, driver’s licenses, bank accounts. registered voting and so on. If we are to see the creation of a universal digital identification, to the linking of initiatives such as the European Blockchain Services Infrastructure (EBSI), the idea that each of these documents should not be linked or connected can result in major issues. For example, a smart contract is made for each of these, minting a token for each. If a user decides to switch wallets, they must pay close attention to sending all of these tokens so as to not get lost. The concept of an on-chain identity is not a farfetched idea, but requiring the individual to migrate all issued tokens from various identities can be catastrophic with human error always being a concern.

ABTs, also known as Asset Bound Tokens, are a token standard that binds one token to another token by linking it. This means if the primary token gets moved, all of the linked token information will update, essentially moving with it without the act of the token actually moving. The token standard can be viewed as a live repository, updating in accordance with the primary token while remaining independent with its own set of information. Therefore, whether it’s a secondary collection intended to complement the first, or healthcare issued to an ID, the sma

## Replies

**SamWilsn** (2025-04-15):

You may want to include a section on [ERC-165](https://eips.ethereum.org/EIPS/eip-165) so that the contract’s users can determine what interfaces are supported.

Might also be a good idea to define some events to be emitted when tokens are created/destroyed/linked. Even if those functions aren’t defined in the standard itself, those operations will still happen and external observers should be able to subscribe to those events.

---

**NarcisCRO** (2025-05-01):

While it’s true that authoritarian regimes could misuse this kind of technology, I believe that any well-intentioned tool can be twisted for the wrong purpose. What we’re aiming for with ABTs is to define a standard that allows linking one or more assets to a primary asset in a secure and flexible way.

For example, if you ever suspect your wallet is compromised, instead of manually transferring each asset one by one, you could just move the primary asset. If that primary is an ERC-6809, even better—it simplifies the whole process significantly and secures it in the same time.

---

**SamWilsn** (2025-05-13):

Have you seen [ERC-5114: Soulbound Badge](https://eips.ethereum.org/EIPS/eip-5114)? It proposes a somewhat similar idea of binding a token to another token.

