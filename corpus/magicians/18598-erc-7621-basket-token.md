---
source: magicians
topic_id: 18598
title: "ERC-7621: Basket Token"
author: CalMC
date: "2024-02-11"
category: ERCs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/erc-7621-basket-token/18598
views: 4036
likes: 3
posts_count: 4
---

# ERC-7621: Basket Token

Hi Magicians,

We would like to propose the following new ERC token standard for discussion: The ERC-7621 (BTS or Basket Token Standard).

Please find PR of draft submission here: [Add ERC: Basket Token by AlvaraProtocol · Pull Request #251 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/251)

This proposed standard allows for the implementation of multi-asset tokenized funds. It provides basic functionality for anyone to deploy unique, non-fungible BTS tokens that can contain an unlimited number of underlying ERC20 tokens, allowing rebalancing and accepting additional stakeholders, issuing unique BTS LP tokens whenever a contribution is made.

The deployer receives a BTS token representative of their ownership of the fund, as well as LP tokens representative of their percentage share of the fund (100% at time of deployment but changing as other wallets contribute/withdraw). Whenever a contribution is made to a BTS, ETH (or equivalent) is used to purchase the underlying ERC20 tokens at the current weighting and BTS LP tokens are minted and distributed to the contributor’s wallet (representative of their share of the fund); when a withdrawal is made from a BTS, the underlying ERC20 tokens are sold for ETH (or equivalent), BTS LP tokens are burned and ETH returned to the redeemer’s wallet.

The BTS has a rebalance function, which allows for a BTS owner to change the percentage share of the fund that each asset makes up. Assets can also be removed entirely or added through this function, after a BTS has already been minted.

By leveraging the ERC721 standard as a representative token of ownership when minting the BTS, the tokenized fund can also be fully manageable and transferable on-chain.

The motivation is to provide infrastructure that will enable the on-chain creation and management of asset-backed investment funds.

## Replies

**lockheart** (2024-02-22):

I can’t really see how this EIP provides innovation beyond other EIPs which are more general, like 6551 [ERC-6551: Non-fungible Token Bound Accounts](https://ethereum-magicians.org/t/erc-6551-non-fungible-token-bound-accounts/13030)

Can you perhaps expand on what the innovation is?   E.g. TokenSets is already an application that does the similar wrapping of multiple assets into ERC20 tokens.

---

**CalMC** (2024-02-23):

The ERC-7621 is unique from other ERCs as each time a contribution is made, unique ERC-20 LP tokens are minted. And conversely, when a withdrawal is made, the LP tokens are burned. Unlike other solutions, the 7621 LPs are fully transferable, therefore solving the scalability issue. The 7621 also has a rebalance function which can be set to execute automatically, or can be done manually.

The 6551 implementation provides a wallet for 721, allowing users to hold assets within an NFT but not allowing third party participation or the provision of LP tokens denoting stake in a wallet.

There are several protocols that provide solutions for on-chain funds, with varying degrees of centralization or gate-keeping of decentralization. The ERC-7621 is base layer DeFi infrastructure. The standard’s implementation layer will be where the security considerations you’ve mentioned will be addressed. For example, as 7621 LPs are transferable ERC-20 tokens, they can be used as governance tokens for fully decentralized management of 7621 tokens. A manager could then make proposals to their DAO to substitute or rebalance the underlying tokens.

If the 7621 didn’t allow for full discretionary management as well as DAO-managed funds, then it would not be base-layer infrastructure and would be attempting to gate-keep decentralization. It would also never attract mass adoption as much of the TradFi fund market operates under full discretionary management.

---

**catiga** (2024-04-14):

Hi, could I invite you to review and discuss my topic, [ERC2510: Embedding Perpetual Value and Liquidity in Tokens](https://ethereum-magicians.org/t/erc2510-embedding-perpetual-value-and-liquidity-in-tokens/19577)

Looking forward to your suggestions.

