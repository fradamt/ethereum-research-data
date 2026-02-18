---
source: ethresearch
topic_id: 2854
title: Proof of stake without a cryptocurrency, but with an "index-fund"-token as collateral
author: josojo
date: "2018-08-08"
category: Economics
tags: []
url: https://ethresear.ch/t/proof-of-stake-without-a-cryptocurrency-but-with-an-index-fund-token-as-collateral/2854
views: 1472
likes: 2
posts_count: 3
---

# Proof of stake without a cryptocurrency, but with an "index-fund"-token as collateral

**Introduction:**

Gold, most cryptocurrencies and other assets like arts are quite frequently being criticized for being a bad investment, as they are only a collectible and their value is only derived from scarcity. Compared to stocks, they do not “work for the investor” and they do not generate dividends. While stocks appreciate and depreciate with the growth or decline of the underlining economy, gold and other assets appreciated and depreciate in value only by social adaption consensus and/or social network effects.

We, the ethereum community,  have built something awesome: a decentralized world computer. We used a cryptocurrency, crypto fuel for it. I would like to discuss whether we could build the same decentralized world computer without any cryptocurrency, but using a decentralized index-fund token as collateral.

**World computer with POS and without a cryptocurrency:**

Imagine we would create a **decentralized index fond (DIF100)** on ethereum, which would hold the top 100 most valuable ICO’s (like the Nasdaque100). This DIF100 could be a smart contract that holds these top 100 ICO coins and issues DIF100-tokens representing an ownership in all the top 100 tokens.

Now, these DIF100-tokens could be used for staking and for paying transaction fees on the decentralized world computer instead of Ether. Everything would be quite the same, with the only difference that the token supply cannot be inflated, proof of stake validators could only be paid with transactions fees.

**Advantages:**

- Collateral tokens (DIF100-tokens) for staking have an inherent value
(Ether has also an inherent value, as it is used to pay for computation fees. But the dividends from the DIF100 might a high multiple of the transaction fees collected)
- “higher security”, as the valuation of the DIF100 might become higher than the market cap of Ether
- If the DIF100 would contain reliable companies, volatility might be lower as it is for Ether.
- (Decentralized computers run on a crypto-currency have a coupling between the security provided and the fees charged, as a fee model maximizing the total fees collected will boost the value of the token and therefore the POS-stakes. This might not be the optimal fee structure for a decentralized computer.)

**Disadvantages:**

- Forks are getting much harder to manage
- If the companies require KYC, validators would be known
- No issuance of new tokens is possible
- Governing the DIF100 might be challenging

**Comment**

By no means, this post is meant as a criticism of the current ethereum model. I think that ethereum has a sound economic model, as it is the currency required to run any computation on this great trust-machine. I am just wondering, whether another model might be even better.

## Replies

**coolpikmin** (2018-08-09):

The moment you issue DIF100 token, wouldn’t that be going back to square one? Sure the underlying assets are spread out (semi-decentralized across 100 tokens?), but I don’t see how buying that token would be different from buying ether to stake. Owning 10% of DIF100 and owning 10% of ether would both mean you have 10% voting power.

Also, this opens up additional unknown attack vectors. For example, a malicious actor staked and gets paid in DIF100, and if this same actor owned one of the assets underlying DIF100, she could artificially inflate her own project token (cause market cap manipulation is for now possible), inflating her DIF100 token right before she changes it to a stablecoin.

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> “higher security”, as the valuation of the DIF100 might become higher than the market cap of Ether

I’m fine with speculating my own money, but I don’t want speculation to be an integral part of Ethereum’s security.

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> Governing the DIF100 might be challenging

Oh yeah, absolutely. It’ll be governance hell.

This made me wonder though if it’s possible to create a service for other ERC20 token holders to participate in main chain staking. They just click a button, and although their ERC20 tokens are left intact, using a combination of DEX or loans, behind the scenes they start staking in Ether. Not exactly your idea of creating a decentralized asset for staking, but floating an alternative ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**josojo** (2018-08-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/coolpikmin/48/2542_2.png) coolpikmin:

> The moment you issue DIF100 token, wouldn’t that be going back to square one? Sure the underlying assets are spread out (semi-decentralized across 100 tokens?), but I don’t see how buying that token would be different from buying ether to stake. Owning 10% of DIF100 and owning 10% of ether would both mean you have 10% voting power.

Yes, it would be quite the same. The only difference is that the asset type is a different one and hence, we are getting different properties.

![](https://ethresear.ch/user_avatar/ethresear.ch/coolpikmin/48/2542_2.png) coolpikmin:

> Also, this opens up additional unknown attack vectors. For example, a malicious actor staked and gets paid in DIF100, and if this same actor owned one of the assets underlying DIF100, she could artificially inflate her own project token (cause market cap manipulation is for now possible), inflating her DIF100 token right before she changes it to a stablecoin.

Yes, one would choose only tokens for the DIF100, which are not inflatable. And probably, they should also have some other constraints, which are enforced on a smart contract level.

![](https://ethresear.ch/user_avatar/ethresear.ch/coolpikmin/48/2542_2.png) coolpikmin:

> “higher security”, as the valuation of the DIF100 might become higher than the market cap of Ether

I’m fine with speculating my own money, but I don’t want speculation to be an integral part of Ethereum’s security.

The main claim of my post is that owning Ether is a higher speculation risk that owning tokens of an index fond.

