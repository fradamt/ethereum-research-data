---
source: magicians
topic_id: 13677
title: Yield-bearing token Converters
author: LeoPapais
date: "2023-04-04"
category: Magicians > Primordial Soup
tags: [token]
url: https://ethereum-magicians.org/t/yield-bearing-token-converters/13677
views: 405
likes: 0
posts_count: 1
---

# Yield-bearing token Converters

Hello Fellowship!

I’m working with yield-bearing tokens, and some implementation details are making my life harder, so I’d like to propose a standard if there’s nothing else out there that solves this issue. These tokens can accrue value through time, but this accrual can be represented as *rebasing tokens* or as *exchange rate tokens*.

**Definitions:**

- asset: This unit measures the pool’s value. At time t, the pool has a total value of TotalAsset(t) assets.
- shares: A unit that represents ownership of the pool. At time t, there are TotalShares(t) shares in total. One user u has sharesOf[u], and only a new transfer changes this value.
- exchange rate: At time t, the exchange rate ExchangeRate(t) is simply how many assets each shares is worth ExchangeRate(t) = TotalAsset(t) / TotalShares(t)
- rebasing tokens: the tokens that implements their balanceOf method as sharesOf[u] * ConvertionRate(t). That means the return value from balanceOf can change even without a transfer to/from the user u.
- exchange rate tokens: the tokens that implement their balanceOf method as just sharesOf[u], so the return value from this method is constant if no shares are transferred to/from the user u. They use the ExchangeRate(t) method upon withdrawal/burn of the shares of a user.

**Examples:**

- rebasing tokens: stETH from Lido.
- exchange rate tokens: cTokens from Compound.

Contracts that integrate with **rebasing tokens** tend to break with **exchange rate tokens** and vice-versa, and that’s where a converter from one type to another becomes handy. While this is relatively simple, I think the community would benefit from the added safety that a standardized and audited reference implementation would bring.

While I did find a reliable and safe converter from **rebasing token** to **exchange rate token** on 0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0 (wstETH contract on mainnet), I couldn’t find the other way around (from exchange rate token to rebasing token).

Do you think that’s something worth opening an EIP for?
