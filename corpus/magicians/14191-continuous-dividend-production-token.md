---
source: magicians
topic_id: 14191
title: Continuous Dividend Production Token
author: internetmoneydev
date: "2023-05-09"
category: EIPs
tags: [eip, interfaces, proposal]
url: https://ethereum-magicians.org/t/continuous-dividend-production-token/14191
views: 1733
likes: 59
posts_count: 13
---

# Continuous Dividend Production Token

It seems that the discussion has stalled on dividend-producing tokens so we are going to shepherd it.

This post is to centralize interest in standards regarding dividend production for holders of a token to push it into a standards track and reduce complexity for dividend production token implementations.

There has been superficial interest in defining dividend-producing tokens in the past, specifically [1726](https://github.com/ethereum/EIPs/issues/1726) for native tokens and [2222](https://github.com/ethereum/EIPs/issues/2222) for erc20s as dividends. However, these efforts seem to have failed or stalled out. There have been many other implementations that have simply launched and have run into a variety of issues/limitations with their implementation that are only apparent afterward. There have also been pushes for royalty payments, however, they have mostly centralized around NFTs and not around arbitrary divisions of cash flow in addition to holding an erc20/721/777 or any other token underlying the accounting and shares defining distributions as formalized by 4626 using vaults. One of the most isolated versions is from @roger-wu, however, it never seemed to go beyond a [github repo](https://github.com/Roger-Wu/erc1726-dividend-paying-token/blob/master/contracts/DividendPayingToken.sol) at least not in the EIP process, and at this point, it should be rewritten to take advantage of recent solidity updates.

While dividends for tokens may be small when spread across a total supply, depending on the token being distributed, defining this standard at the token level seems appropriate since other features can be built on top of this baseline standard such as staking (eip4626) to concentrate dividends and reward behavior which is beneficial for the addresses holding the token. Not only will some token implementations wish to produce cash flow to all holders to discourage custodial-based (see celsius, ftx) or other behaviors, but this is how legacy finance works currently, and if we wish to take a conservative approach to replace an entire financial system, it may be prudent to require fewer steps and less abstraction.

We think that it would be worthwhile to define a distribution mechanism on the token level - to remove any feature complexity such as staking and allow each feature to simply be a gate that mints new tokens. Then all of the accounting can exist as a token and include every level that may be relevant to projects that wish to incorporate dividends. This is already an emergent phenomenon, so it would be best to be able to build off of previous work and standardize a protocol instead of fragmenting implementations.

We are on [step 1](https://eips.ethereum.org/EIPS/eip-1#shepherding-an-eip) of this process and want to know if this is worth pursuing! Please post your reactions / best arguments for and against.

## Replies

**BrotherKDG** (2023-05-09):

Hello Fellow Magicians!

My name is KG and I am the founder of the ecosystem from which this token standard necessity is derived.

Our goal with the creation of this accounting method was twofold:

1. To make the user experience for income yielding tokens simpler than the standard accounting methods used (most commonly staking).
2. To remove the time restrictions that usually come with locking up tokens. In the case of the proposed standard, there is no minimum or maximum time that dividends sent to this contract are subject to.

The two above statements make this standard, fluid and easy to interact with.

In our case, we utlize the above standard as such:

-The core of our technology is an EVM wallet. In our wallet, we have an in-app swap feature (DEX Aggregator) that charges fees when users utilize this feature.

- Those fees are paid by the user in the form of native coin (relevant to each chain).
- 100% of those fees are sent to the above contract (in our case T.I.M.E. Dividend; TIME)
- Then holders of TIME can interact with dividends as stated in the above standard proposition (as frequently as they choose, with no time constraints - outside of block speeds), and without staking or locking up their TIME.

We feel that this standard is an important innovation for the Ethereum ecosystem as it allows additional flexibility and diversity for protocols that wish to be yield bearing. It also allows for the evolution model of a “Decentralized Company” as ANY protocol (even multiple protocols pointing to a single contract) can point yield/revenue/dividends to this contract and holders of the contracts token will be the recipients of the rewards.

What is Ethereum, if not innovative and all considering? This standard aims to add further contribution to that ethos.

You can learn more about us at https://internetmoney.io

---

**Cateater9000** (2023-05-09):

I think this is a great idea thank you for what your team has done to better the crypto space its brains like the IM team that change the world!

---

**toos_pooky** (2023-05-09):

Brilliant. Would be a huge step forward and would definitely incentivize self custody and longer holders periods. It’s a beautiful layer to add to the world of crypto.

---

**Whalecome** (2023-05-09):

Crypto at it’s best! Can’t wait for this ride to the top​:rocket:![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)

---

**Loungey** (2023-05-09):

Action toward new standards.

---

**Waves** (2023-05-09):

Love internet money wallet, it’s has the potential of been one of the best crypto currency wallet.

---

**EW1** (2023-05-10):

I love the simplicity of design with yield, while upholding the core principles of DeFi. This changes how the new person to crypto can get exposed to smart contracts that are easy to understand and benefit from. Please dive deeper into this.

---

**psi931** (2023-05-10):

Such a novel concept and quite frankly the reason crypto was invented, to eliminate the middleman. Love your work and look forward to making the Internet Money wallet my only wallet! Bring on the dividends!

---

**Bhau** (2023-05-10):

I support the idea of developing such a distribution mechanism as it can facilitate the onboarding of new users to web3. Once optimized, such a standard could be broadly applied across a variety of tokens and chains. Parameters, of course, would be decided by respective governances.

---

**charlesirie** (2023-05-10):

Great project…everyday crypto wallet ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=12)

---

**sergeifocusnik** (2023-05-12):

Internet Money is best wallet but need translate in other languages…

---

**Koru** (2023-10-11):

Great idea and now a working product ![:vulcan_salute:](https://ethereum-magicians.org/images/emoji/twitter/vulcan_salute.png?v=12)

