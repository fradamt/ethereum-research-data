---
source: magicians
topic_id: 25979
title: "ERC-8060: IERC721Value — Embedding native ETH inside ERC-721 tokens"
author: ten-io-meta
date: "2025-10-26"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8060-ierc721value-embedding-native-eth-inside-erc-721-tokens/25979
views: 197
likes: 1
posts_count: 8
---

# ERC-8060: IERC721Value — Embedding native ETH inside ERC-721 tokens

### Hello everyone

This is an early-stage concept I’ve been developing called **[TEN.IO](http://TEN.IO)**, which proposes a way for ERC-721 tokens to embed native ETH value directly within their logic.

I’m sharing it here to open a technical discussion about its potential **standardization** and implications for Ethereum’s cultural and economic layers.

---

###  Overview

The idea extends the current ERC-721 standard by introducing an interface called **`IERC721Value`**.

Each NFT can hold a verifiable **ETH balance within the contract itself**, not through wrapping or delegation.

The embedded value is transparent, withdrawable (via `burn()`), and fully on-chain — linking artistic, cultural, or symbolic data with **real ETH collateral**.

This enables new forms of digital assets that act as **reservoirs of ETH-backed culture**, where each fragment of art or code carries intrinsic, measurable value.

---

###  Interface draft (simplified)

```auto
interface IERC721Value is IERC721 {
    function valueOf(uint256 tokenId) external view returns (uint256);
    function mint(address to) external payable returns (uint256 tokenId);
    function burn(uint256 tokenId) external returns (uint256 refunded);
}
```

---

###  Use cases

- Art and media fragments that embed verifiable ETH reserves
- NFTs representing cultural or educational works with intrinsic liquidity
- Tokenized archives where each asset holds its own collateral
- Long-term storage of symbolic value directly on-chain

---

###  Key difference

Unlike ERC-20 or wrapped models, the ETH never leaves the NFT contract.

The token itself **is the vault** — an autonomous unit of value and meaning.

---

###  Motivation

This proposal aims to **bridge Ethereum’s financial layer with its cultural layer**, giving each creative output measurable economic weight without intermediaries.

---

###  Next steps

I’d love to hear thoughts on:

- Possible integration paths with ERC-721 extensions
- Security considerations for ETH holding per token
- Whether this could evolve into a formal ERC standard

---

###  Full reference

**Test implementation (Sepolia):**

Deployed and verified as part of the [TEN.IO](http://TEN.IO) system.

**IPFS video demonstration:**

![:movie_camera:](https://ethereum-magicians.org/images/emoji/twitter/movie_camera.png?v=15) https://ipfs.io/ipfs/bafybeifyzmymkdjkovo25z4kglt6bglcmy5ajpjpw5qjvhctnkcquwi4la

---

###  Summary

> ERC-721 tokens capable of holding native ETH —
> transforming NFTs from representations of value into containers of value.

---

###  Author

**[TEN.IO](http://TEN.IO)**

`@ten_io_meta` on X

**ENS:** tenio.eth

**Website:** https://tenio.eth.limo

---

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15) **Category:** `Magicians › Primordial Soup`

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15) **Tags:** `ERC721, ETH, NFT, protocol, value`

## Replies

**ten-io-meta** (2025-10-27):

Open for community feedback.

Looking forward to hearing thoughts from other ERC authors and protocol engineers.

---

**mikelxc** (2025-11-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mikelxc/48/15479_2.png)
    [ERC-7978: Non Fungible Account Tokens](https://ethereum-magicians.org/t/erc-7978-non-fungible-account-tokens/24612/3) [ERCs](/c/ercs/57)



> ERC-6551: NFT ↔ account binding stored in a registry contract; NFT metadata unchanged.
> NFAT: NFT metadata directly names the wallet address; validator enforces “current NFT holder == wallet signer”; wallet is tradable anywhere ERC-721 is supported.
> The philosophy is to make the wallet address part of the NFT’s identity; use a minimal validator so the NFT is the key. Instead of relying on a central registry coordinates the mapping and NFT point to an account;

I had an earlier proposal of taking this a step further and turn an NFT into a smart wallet

---

**ten-io-meta** (2025-11-03):

Thanks for the recent discussion about ERC-6551 and ERC-7978 — both are great references.

Just to clarify, ERC-8060 goes one step further: it allows **native ETH to be embedded directly inside an ERC-721 token**, so the NFT itself can hold and release real ETH value without needing a separate registry or external account abstraction.

In that sense, it turns the NFT into a **self-contained smart wallet**.

I’d really appreciate any feedback on interoperability with 6551 or 7978, or suggestions for maintaining ERC-721 compliance while embedding value.

---

**ten-io-meta** (2025-11-04):

Thanks for the reference — the concept of NFTs acting as smart wallets is indeed an interesting direction.

In fact, ERC-8060 starts exactly from that premise: by embedding native ETH directly inside the token, the NFT itself *becomes* the wallet, maintaining its own balance without relying on an external account or wrapper contract.

The goal is to simplify the abstraction layer — merging value (ETH) and identity (NFT) into a single on-chain entity.

---

**ten-io-meta** (2025-11-08):

**Update — Value clarification + live implementation**

Quick clarification regarding value units inside the current implementation:

- Fragment 0 (El Umbral) mints at 0.012 ETH
and keeps 0.010 ETH embedded as native collateral.
- Future fragments (songs / chapters) will follow the structure of
mint 0.12 ETH → hold 0.10 ETH as collateral,
but the current early fragment uses a lower value since it acts as the “entry threshold” of the system.

Website (ENS): https://tenio.eth.limo

The goal remains the same:

> The NFT itself becomes the vault — a self-contained unit of value + meaning.

Happy to receive feedback on:

- compatibility with existing ERC-721 extensions,
- security trade-offs holding ETH per token,
- whether embedding native ETH should evolve into a formal ERC.

---

**ten-io-meta** (2025-11-13):

Hi everyone ![:waving_hand:](https://ethereum-magicians.org/images/emoji/twitter/waving_hand.png?v=15)

Just a quick follow-up — the ERC-8060 PR (#1315) has passed all checks and is now waiting for editorial assignment.

The reference implementation is already live on Sepolia and Mainnet, following the same structure used in https://tenio.eth.limo (mint 0.012 ETH → holds 0.010 ETH as native collateral).

Would appreciate any thoughts or feedback on how native ETH embedding compares to related discussions like ERC-6551 or ERC-6909.

Thanks for keeping the standards process alive and open ![:folded_hands:](https://ethereum-magicians.org/images/emoji/twitter/folded_hands.png?v=15)

---

**ten-io-meta** (2025-12-15):

Hi everyone

I just wanted to add a brief clarification for context, since ERC-8060 is sometimes discussed alongside proposals that define supply behavior.

**ERC-8060 is intentionally scoped to value localization, not supply semantics.** Its only invariant is that value lives in a single, self-contained ERC-721 state — the token itself acts as the vault.

ERC-8060 does **not** define how supply behaves over time. It does not specify minting rules, burn finality, caps, or whether total supply can ever increase after a burn. Those concerns are explicitly out of scope for this proposal.

Supply semantics are addressed separately in **ERC-8098**, which defines a strictly non-increasing total supply invariant for fungible assets.

In [TEN.IO](http://TEN.IO), both ERCs are used together but remain **orthogonal**:

• **ERC-8060 answers where value lives**

• **ERC-8098 answers how value can cease to exist at the protocol level**

I’m sharing this only to avoid semantic overlap — not to couple the proposals. Each ERC stands independently and can be evaluated on its own merits.

Thanks for taking the time to review.

