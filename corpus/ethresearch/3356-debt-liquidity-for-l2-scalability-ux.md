---
source: ethresearch
topic_id: 3356
title: Debt & Liquidity for L2 Scalability UX
author: eva
date: "2018-09-13"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/debt-liquidity-for-l2-scalability-ux/3356
views: 5293
likes: 12
posts_count: 13
---

# Debt & Liquidity for L2 Scalability UX

Thanks to Kelvin Fichter, vi and conversations with Dharma, Connext, Bounties Network and Spankchain.

---

Research on blockchain scaling is all very exciting, but implementations of scalability solutions like payment channels, Plasma or sidechains must also facilitate *acceptable user experience*; otherwise blockchains risk being scaled for an adoption that never occurs.

Although decentralized technology provides users with greater opportunities, user acquisition/conversion from centralized, incumbent platforms will only occur if user experience is comparable, if not better. Thus, we must bridge the gap between cryptographically secure and economically incentivized mechanisms, and the *reasonable* expectations and payment behaviors of users.

## L2 Capital Requirements

Many emerging mechanisms rely on some kind of collateralization or capital lock-up that can be slashed in the case of malicious activity. This disincentivization makes sense to mitigate bad behavior of operators, network validators and users but also poses threats to usability. Frankly, any kind of lock-up for basic functions can impede user experience.

For Plasma implementations, a few examples of lock-up or capital-induced  “events” include:

- Deposits into Plasma contract
- Transactions between UTXOs on Plasma chain
- Exit bonding or piggyback bonding (collateralizing the attestation of chain exits / withdrawals,
re: More Viable Plasma)
- Plasma chain withdrawals

While depositing into a Plasma contract is adequate UX parallel with digital wallet top-up or prepaid payment models; “bonding” or lengthy withdrawal periods are not and can create significant psychological costs.

When a user wants to exit or withdraw from the Plasma chain (e.g., if the chain goes bad or to transfer funds to another Plasma or sidechain), they must bond themselves (provide a small collateral), that acts as a disincentive for bad behavior (such as attempting to exit or withdraw an invalid UTXO).

Current estimates of Plasma withdrawals are ~7-14 days, as funds go through a sort of “escrow” when being exited from a Plasma chain to the rootchain. This escrow is conditional on a successful challenge period, where the transaction is deemed valid if no conflicting proof is provided.

If the user is good (valid transaction), they will have their bonds returned and their funds withdrawn, yet psychological costs prevail. We can alleviate these costs by introducing liquidity or debt providers that “buy” user bonds or [fast withdrawals](https://ethresear.ch/t/enabling-fast-withdrawals-for-faulty-plasma-chains/2909)), by providing the funds required and earning interest on the service. *Caveat: who pays for the interest? Depending on the design, the operator, watcher, wallet provider or user could pay. For example, the Plasma smart contract could presupose lending, so a user’s fast withdrawal could be their UTXO withdrawal value minus interest.

## Plasma Debt

There are three potential debt options that vary in their trust models:

**1. Trustless:** lender for bonds or fast withdrawals downloads the Plasma chain and lends necessary funds *only if* the exit / withdrawal is valid.

**2. Semi-Trusted / Cryptoeconomically Incentivized:** lender relies on a third-party “attester” to download the Plasma chain. To ensure the attester doesn’t grief the lender, they would also have to bond themselves for their attestation.

The value of the attester’s bond would have to equal the value of the Plasma bond or fast withdrawal, however this could require a lot of capital depending on the size of the exit / withdrawal. So perhaps more likely, the attester would put up a bond smaller than the Plasma transaction, but would require an underwriter to assess the risk of the transaction and minimize the lender’s potential loss of funds.

*Note: the attester, Plasma operator, watchers, users and the overall chain consensus mechanism would **all** need to be underwritten.*

**3. Fully-Trusted:** lender sits on the rootchain and requires an underwriter to assess the risk of the transaction. Lender assumes full risk but trusts the underwriter, Plasma operator, watchers and users.

##

Only the trustless option is secure for lenders, as loans won’t be issued unless the transactions are confirmed to be valid. Semi-trusted and fully-trusted models would require underwriters but still wouldn’t 100% guarantee loan repayment.

A Plasma debt mechanism could ensure that users never have to understand the concept of “bonding” and they can receive their withdrawals as quickly as possible, limited by the rate of rootchain finality. Lenders don’t have to be traditional debt providers but could be Plasma operators, watchers, wallets or service providers. Alternatively yet more aggressively, if a user *fully collateralizes* their exit / withdrawal, a bond wouldn’t be necessary and fast withdrawal would be guaranteed.

## Other L2 Liquidity Considerations

In addition, payment channel, Plasma or sidechain implementers may require liquidity or debt solutions to facilitate exchange and acceptance of multiple currencies, to enable interoperability.

*Payment Channels*

- Liquidity or exchange for multi-currency payments in a state channel or channel hub
- Collateralization instead of HTLCs to secure funds in a payment channel hub

*Plasma / Sidechains*

- In-Plasma / sidechain liquidity or exchange for multi-currency payments
- Liquidity or exchange on rootchain, linked to Plasma or sidechain contract

These can be executed by L2 implementers developing their own in-house exchange mechanisms (e.g., state channel / hub exchange, Plasma or sidechain exchange like OMG Network DEX) or integration with on-chain liquidity, exchange or debt relayers.

## Conclusion

We must remember that with everyday users, decentralization vs. centralization is a competition for attention, based on convenience, usability and benefits of products/services - not necessarily the underlying technology or the ideologies behind it. New classes of debt and liquidity mechanisms may become tools to create acceptable user experiences across layers of blockchain infrastructure.

## Replies

**jdkanani** (2018-09-13):

Nice.

We have already started working on a faster exit by wrapping exit UTXO into NFT. With that, an operator  (in our case, Matic Network) will underwrite and the user can put NFT as collateral in Dharma or sell on 0x.

---

**jepidoptera** (2018-09-13):

Probably the most logical entity to provide trustless exit collateralization would the operator, who already has all the information required and a natural incentive to make it work… is there any potential issue with that?

---

**eva** (2018-09-14):

The main constraint is the significant amount of capital that would be required. Not all operators (e.g. merchants, network providers) will be in a position to front capital, so selling the receivables to disparate lenders may be more likely (see [factoring](https://en.m.wikipedia.org/wiki/Factoring_(finance)))

---

**Dikud** (2018-09-14):

Интересные мысли, Ева. Фактически, это инженерная ошибка в самой экономической конструкции.

Думаю, что на больших массах пользователей подобные сложности быстро проявлятся и будут устранены.

---

**gakonst** (2018-09-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/eva/48/2187_2.png) eva:

> Current estimates of Plasma withdrawals are ~7-14 days, as funds go through a sort of “escrow” when being exited from a Plasma chain to the rootchain.

This is based on the first implementations that set the dispute period to be 7/14 days.

I don’t believe there is a ‘correct’ choice for how long the dispute period should be.

As for the bonds, I’d imagine that a good Plasma UI would be also connected to a lending protocol (maybe [dharma.io](http://dharma.io) for example). That way, when you start an exit, you can automatically have the bond lended to you, and when your exit is finalized, you’d pay back the bond (plus whatever interest the lending deal involved).

![](https://ethresear.ch/user_avatar/ethresear.ch/eva/48/2187_2.png) eva:

> There are three potential debt options that vary in their trust models:

I believe that only the trustless option will be used in practice, as you say. The most likely parties to be the lenders are the ‘full nodes’.

![](https://ethresear.ch/user_avatar/ethresear.ch/eva/48/2187_2.png) eva:

> In addition, payment channel, Plasma or sidechain implementers may require liquidity or debt solutions to facilitate exchange and acceptance of multiple currencies, to enable interoperability.

Why?

![](https://ethresear.ch/user_avatar/ethresear.ch/eva/48/2187_2.png) eva:

> Collateralization instead of HTLCs to secure funds in a payment channel hub

@jcp was talking about something similar to this, could you elaborate / point to relevant literature?

---

**ldct** (2018-09-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> Collateralization instead of HTLCs to secure funds in a payment channel hub

@jcp was talking about something similar to this, could you elaborate / point to relevant literature?

Yeah, do you mean under-collateralization in a payment channel network? All trustless payment channel networks have basically the same collateral requirements IMO (assuming constant locktime)

---

**eva** (2018-09-15):

Theoretically, instead of HTLCs the hub in a channel network of Alice, hub and Bob, could collateralize or “bond” themselves equal or greater to the value flowing through the channel network, to ensure that Bob receives the funds.

Practically this would require a lot of capital and may be unrealistic (similar to the above idea of fully collateralizing a Plasma exit/withdrawal) although implementations with wealthy hub / users could be possible.

cc [@gakonst](/u/gakonst)

---

**ldct** (2018-09-15):

What properties distinguish fully collateralized hubs from HTLC-based payment channel networks?

---

**kfichter** (2018-09-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/j/4bbf92/48.png) jdkanani:

> We have already started working on a faster exit by wrapping exit UTXO into NFT. With that, an operator (in our case, Matic Network) will underwrite and the user can put NFT as collateral in Dharma or sell on 0x.

Does this make use of something similar to [Simple Fast Withdrawals](https://ethresear.ch/t/simple-fast-withdrawals/2128)?

---

**jdkanani** (2018-09-16):

> Does this make use of something similar to Simple Fast Withdrawals?

Yes. We are wrapping into NFT, so that current (liquidity) protocols can use it instead of fixing on price while exit.

---

**tasd** (2018-09-17):

I think this is an important topic, as I see still some handwaving around usability problems.  Also, it is helpful to consider specific use cases or classes of applications, and state those assumptions when discussing solutions; what works well for a large, multi-node POS network (like OMG) may be quite different from what works for a smaller single operator POA network that’s designed for one application.

For exit bonds, I wonder if it would be workable for the user to pre-fund their exit bond when they make an initial deposit into the plasma chain.  The root chain smart contract would hold the bond on their behalf until they want to exit.  If they really want to spend all of their funds including the bond, then perhaps they have to acknowledge a warning in the UI before they can do that.  This solves the “What do you mean I have to pay to get my money out?!” problem, and could be simpler than trying to arrange a loan.  I’m not sure what the implementation details would look like.

Of course pre-funded exit bonds would not work if the user never made an initial deposit, and they only received funds.

---

**eva** (2018-09-18):

For one, no need to estimate time to expiry as full collateralization could theoretically keep the channel open indefinitely, or until Bob wants his funds in which case the collateral could be slashed.

