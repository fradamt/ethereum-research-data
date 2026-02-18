---
source: ethresearch
topic_id: 23862
title: "ENS with IBAN Resolvers: Unify settlment layer of DeFi and TradFi"
author: Citrullin
date: "2026-01-16"
category: Layer 2
tags: []
url: https://ethresear.ch/t/ens-with-iban-resolvers-unify-settlment-layer-of-defi-and-tradfi/23862
views: 212
likes: 4
posts_count: 3
---

# ENS with IBAN Resolvers: Unify settlment layer of DeFi and TradFi

The Ethereum ecosystem has successfully bridged the gap from TradFi to DeFi through regulated on-ramps and stablecoins like EURe.

Sending money from your IBAN account directly into your wallet works like a breathe. The reverse direction on the other hand doesn’t work as seemless.

Settling from a web3 wallet directly into arbitrary IBAN account remains fragmented, often requiring calling APIs or manual off-ramping.

This extension to ENS attaches verifiable virtual IBANs (vIBANs) to ENS domains.

By implementing a hierarchical resolver system, we can enable wallets to treat an IBAN as a first-class routing identifier on chain.

Supporting either direct on-chain p2p settlement or automated fallback to regulated SEPA proxies.

By leveraging the structured and hierarchical nature of IBANs (Country Code → Bank Code → BBAN), we can build a decentralized directory within ENS to automate this flow.

## ENS Text Record Schema

Two new text records for ENS domains:

`viban`: A standard-compliant IBAN string (e.g., EE471000001020145685).

`accepted`: A comma-separated list of preferred assets and chains (e.g., eure@gnosis, usdc@base, eth@taiko).

## Hierarchical Resolver Architecture

The system routes queries through specialized resolvers:

**Global Resolver**: resolver maintained by a DAO that parses the country.

**Country Resolver**: A DAO or Consortium maintained contract that parses the country and bank code. Routes to a bank-specific resolver.

**Bank Resolver**: Maintained by the institution. it validates the BBAN and resolves it to a wallet address and ENS domain.

**Fallback**: If no on-chain route is found (NOROUTE), the system triggers an off-chain proxy.

## Verification and Security

To prevent spoofing, the system implements a verification model.

1. On-Chain Query: The wallet fetches the recipient’s ENS record and the viban claim.
2. Signature Match: Verification of an EIP-712 signed message proving the wallet owner controls the claimed IBAN

```c
struct IBANClaim {
  string viban;
  address wallet;
}
```
3. Bank Confirmation: The claim is matched against the data held by the bank resolver.

## The “Burn and Proxy” Fallback Flow

When a destination IBAN is unresolvable on-chain, the system defaults to a regulated gateway:

1. Rejection: The resolver returns NOROUTE.
2. Intent: The wallet generates a transaction to a designated Burn Address (redemption contract).
3. Off-Chain Execution: A regulated proxy (e.g., Monerium) handles the SEPA credit transfer to the legacy IBAN.
4. Transparency: The gateway provides real-time swap rates if the sent asset (e.g., USDC) differs from the bank’s requirement (e.g., EUR).

## Discussion

This model abstracts chain and liquidity selection, prioritizing low-cost L2s and based rollups (with [Sync Composability](https://ethresear.ch/t/solving-ethereum-s-fragmentation-problem-with-sync-composability/23814)) for cross-chain efficiency. Yet, some question remain.

- How can this model works while maintaining privacy?
- What is the optimal governance for the Root Resolver and Country Resolvers to ensure neutrality? (Bank Consortium?)

Future expansion could extend this beyond SEPA to UK Faster Payments, eYuan, and multi-currency vIBANs.

By treating the IBAN as an extension of identity within the ENS ecosystem, we can create a unified financial space where the boundaries between TradFi and DeFi are transparent.

## Replies

**CPerezz** (2026-01-29):

I like the idea. But doesn’t it feel “wrong” to also expose your IBAN onchain by having it stored in ENS? This is no longer leaking your address and funds, it’s also publicly linking it to your IBAN (and possibly identity as IBANs are widely available “hacked” in data breaches).

Unsure if there’s any mechanism or way to avoid this. The rest looks indeed cool!

---

**Citrullin** (2026-01-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> I like the idea. But doesn’t it feel “wrong” to also expose your IBAN onchain by having it stored in ENS?

You are absolutely right, it would. Personally, I don’t see a huge issue with that.

Personal preferences aside, the properties that make Blockchains, especially Smart Contract ones, so powerful is the transparency.

A lot would be helped if TradFi would be all public and accountable.

Any way, I see the point that some may want to hide their drug purchases, sex toys and whatnot.

Aztec has an interesting compromise in terms of balancing the privacy paradox.

Meaning the interest of society to trace transactions (Money Laundering, Terror financing, Human trafficking etc.) vs. the individuals interest to use their money in a private matter.

It’s an interesting approach and something in that direction might be possible.

Private Resolvers with reveal keys. Idk, something to think about.

If I would do this, I would go with transparent version first, find the issues with etc. and think privacy more of an afterthought.

At that point it becomes also a larger issue for the system. (Wealth distribution, trust collapse etc.). So, you should cover that on that level too, since those are essentially the side-effects that will occur if you don’t. You end just designing a system that will inherently destroy itself if you don’t.

Any way, if you have an idea here. Feel free. Might be simple enough to add reasonable privacy.

How about calling it web3 IBAN?

