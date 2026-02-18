---
source: magicians
topic_id: 22336
title: "Add ERC: Token with built-in AMM"
author: evterminal
date: "2024-12-25"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/add-erc-token-with-built-in-amm/22336
views: 231
likes: 2
posts_count: 5
---

# Add ERC: Token with built-in AMM

**See [Add ERC: Token with built-in AMM by Thaoxuanduong · Pull Request #797 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/797) for the most up to date draft**

## Abstract

This Token Standard integrates Automated Market Maker (AMM) functionality directly into

the token smart contract, enabling seamless, gas-efficient token swaps without external

platforms like Uniswap. By embedding liquidity management and trading logic into the token

itself, this standard eliminates the need for approvals, reduces MEV vulnerability, and drastically cuts transaction costs. This standard aim to redefine Ethereum trading with native mechanisms for liquidity provision, slippage protection, and fee management.

## Replies

**Arvolear** (2024-12-25):

Interesting idea! However, I have several concerns and questions here:

#### Token ↔ token swaps

Uniswap does an amazing job here by automatically enabling transitive swaps. I mean, if there are “A <> ETH” and “B <> ETH” pairs, the “A <> B” swap becomes possible as well.

I believe there may be some protocol developed to support this token standard and help with the routing.

#### UniswapV4

We are just a shy of the UniV4 release where basically every token pair lives inside a huge singleton contract. Thanks to [EIP-1153](https://eips.ethereum.org/EIPS/eip-1153) and the redesign, the gas savings proposed in this ERC may not be as significant. (Especially considering the capital efficiency).

#### Oracle

I think it would be a good idea to add some kind of a built-in oracle directly into the token. One of the UnisawapV2 weaknesses was a lack of one.

#### Design questions

- There are several onlyOwner functions in the spec, it will probably be better to exclude them from the standard and let the implementation developers decide whether to add them or not. Definitely, not everybody is willing to support fees.
- What about the biggest AMM issue – impermanent loss? Are LPs going to receive any swap fees?
- How exactly does this AMM approach aid MEV?
- How does the standard account the LP shares? Is a share just a storage variable in a smart contract?

---

**KK779** (2024-12-25):

What a coincidence. I just finished implementing such a thing here: [guano/src/PinusToken.sol at main · kaijuking779/guano · GitHub](https://github.com/kaijuking779/guano/blob/main/src/PinusToken.sol)

I’m not sure I would actually make this an ERC though. Maybe we just need a swap ERC and just make sure it’s easy to extend ERC-20 implementations.

I like that you put the verb in the front for swapping functions unlike UNIv1’s swapping functions.

I originally called my functions the same as yours but I decided to change it to `swapERC20ToNative()`. This way we can use these contracts even on EVM chains that don’t use ETH as their native token. Renaming it to “ERC20” is to better distinguish it from “Native Token”. As for “for” vs “to”, “for” seems better because “to” might refer to recipient/receiver. The “to” I borrowed from UNIv1. I also took out slippage parameters. I feel this should be optional parameters. Sandwich attacks is an issue but I’m not a fan of requiring parameters that may not be necessary for ERC to serve it’s purpose. Perhaps just include it in “Security Considerations”.

I looked at integrating UniV4 but decided to keep things as simple as possible and creating an adapter later if necessary. Thus I took inspiration from UniV1 and updated the methods that made more sense to me. Another key factor for my swap abstraction is it handles Native <> ERC20 not ERC20 <> ERC20 pairs.



      [github.com](https://github.com/kaijuking779/guano/blob/main/src/SwapAbstract.sol)





####



```sol
// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.28;

import "https://github.com/Vectorized/solady/blob/main/src/tokens/ERC20.sol";

import "./ERC223L.sol";

struct Permit2Sig {
    uint deadline;
    uint8 v;
    bytes32 r;
    bytes32 s;
}

/* It's more of an interface just with public functions */
abstract contract SwapAbstract {
    ERC20 public immutable asset;

    constructor(ERC20 asset_){
        asset = asset_;
```

  This file has been truncated. [show original](https://github.com/kaijuking779/guano/blob/main/src/SwapAbstract.sol)










My implementation doesn’t need liquidity management or fee management. Please make these optional. Liquidity management can also get incredibly complex. See ERC-4626 Tokenized Vaults. I recommend not having too many opinions on how it should be implemented in this ERC.

If you decide to add an oracle, I recommend `erc20ToNativePrice(uint erc20sSold) returns (uint nativesBought)` and `nativeToERC20Price(uint nativesSold) returns (uint erc20sBought)`. UNIv1 puts a `get` prefix but considering solidity’s `public` automatically generated get functions, it would be better to keep it consistent. I would prefer an oracle over reserves because how the actual swap rate is calculated could vary greatly. I have tried to simulate an oracle on the front-end using reserves and it’s very easy to make a mistake not to mention being forced to read the  implementation in different protocols (uni vs curve vs balancer).

---

**Lions** (2025-01-14):

Is there any updates with EV Terminal EIP ?

---

**JohnCrunch** (2025-02-08):

Ditto on all. Also, this field is just developing too quickly. I would only use a CLMM at this point. What happens when we see n-th asset MMs? x*y*z…=k, what then? This seems best left out of the platform level.

However… I think your point on MEV is really interesting. MMs solve for marginal liquidity pricing, which is a major issue for blockspace. Perhaps there is some MEV extension framework for flashbots style arbitrage?

