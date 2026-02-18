---
source: ethresearch
topic_id: 22466
title: "Filler Vaults: A mechanism to deepen cross-chain liquidity via Hyperliquid-style vaults for intent markets"
author: vaibhavchellani
date: "2025-05-26"
category: Applications
tags: [rollup, layer-2]
url: https://ethresear.ch/t/filler-vaults-a-mechanism-to-deepen-cross-chain-liquidity-via-hyperliquid-style-vaults-for-intent-markets/22466
views: 913
likes: 16
posts_count: 9
---

# Filler Vaults: A mechanism to deepen cross-chain liquidity via Hyperliquid-style vaults for intent markets

*Co-authored by [vaibhavchellani](https://x.com/vaibhavchellani) & [letsgetonchain](https://x.com/letsgetonchain)*

## Introduction

Today there is a pretty broad consensus that Ethereum L2 interoperability is intent-based.

Users simply express what they want, for example, “send 100 USDC from Optimism to Arbitrum.” This intent is picked up by incentivised off-chain bots known as fillers/solvers, who deliver the desired outcome while abstracting away the complexities involved.

There are two problematic realities in practice:

- These markets are illiquid leading to bad UX
1252×1236 62.1 KB
- The participation of solver is extremely concentrated posing a risk to liveness and leading to monopolistic pricing dynamics. For example within Across over 60% of volume is cleared by a single filler
1600×466 128 KB
For this system to work efficiently, fillers need two things: Skill and Capital.

Skill isn’t scarce in permissionless systems as talent naturally shows up where incentives exist, as we’ve seen in MEV. But intent fulfillment is not atomic and therefore capital intensive, making capital the real bottleneck.

If we want to scale intent-based interoperability, we must decouple skill and capital, allowing fillers to compete purely on skill, i.e the sophistication of their strategy. This would unlock broader participation, leading to better liveness guarantees, better long-tail coverage, and deeper liquidity across the board. It also democratizes access to filler yield, opening the door for anyone to benefit from participating in the ecosystem. Similarly to how Hyperliquid’s HLP vaults bootstrapped liquidity, we need HLP-style vaults for intent markets.

### Solution: Filler Vaults

We’ve seen this playbook before with Hyperliquid. To attract users, they needed liquidity to ensure attractive perps pricing. They launched a public on-chain vault, where anyone could deposit capital and share in the market making profits. Democratize market making revenue and ensure deep perp liquidity. WIN WIN. This bears the question, could “Filler Vaults”, democratize the upside of filler activity while ensuring deep competitive liquidity through removing capital as a bottleneck?

The challenge, of course, is trust. While anyone could technically create a vault and raise capital, in practice, users chose to trust a trusted authority. In a world of permissionless filler competition, relying on implicit trust and reputation does not lead to the open competitive market we seek.

Instead, we need a way for fillers to access capital in a trust minimized set up. That means: A filler’s strategy must execute exactly as specified in order to tap into a vault’s liquidity and this must be verifiable and enforceable by the vault on-chain.

### How It Could Work

Imagine some off-chain infra layer where filler strategies are hosted. Each strategy listens for intents and decides if and how to fill them. If it determines to fill an intent, the strategy submits a payload to a verifier contract on-chain, which verifies the vault’s configured verification requirements are met.

Forms of verifications could include:

- Running the off-chain infra in a TEE with attestations relayed on-chain
- Quorum-based attestation by trusted authorities
- ZK-proofs of correct execution

Each vault would specify its own trust assumptions. Capital allocators choose which vaults to fund, based on strategy quality and verification guarantees. Capital flows according to market risk preferences.

**[![](https://ethresear.ch/uploads/default/original/3X/7/b/7bbacd76b8a18481c77c1a674b3885ef9160b7e2.png)1104×882 21.6 KB](https://ethresear.ch/uploads/default/7bbacd76b8a18481c77c1a674b3885ef9160b7e2)**

A Practical Example: Filler Vaults Powered by SOCKET

SOCKET offers a powerful middleware stack to build this:

- An EVM based execution environment for asynchronous cross-chain logic
- On-chain contracts to enforce correctness of off-chain computation

[![](https://ethresear.ch/uploads/default/optimized/3X/0/a/0ae9ab07984a6948874db0514fd0c9bc4563a091_2_624x477.png)1466×1120 44.7 KB](https://ethresear.ch/uploads/default/0ae9ab07984a6948874db0514fd0c9bc4563a091)

Here’s how the end to end flow of the intent life cycle could look with SOCKET as the middleware stack and across protocol as the intent and settlement protocol:

1. A filler strategy is deployed on SOCKET middleware paired with an on-chain vault
2. Capital allocators deposit into the vault based on trust assumptions and yield/risk potential
3. An intent is auctioned off by Across Protocol’s SpokePool on Arbitrum
4. The strategy listens to the auction by Across and determines to fill the intent and prepares the corresponding fulfillment payload
5. SOCKETt’s transmitters relay the payload on-chain
6. SOCKET’s on-chain switchboard smart contract (configured by the strategy’s vault to require a zk proof of correct execution) verifies the proof provided along with the payload
7. After successful verification, the payload is forwarded to the vault which fulfills the intent via the Across SpokePool contract on Optimism
8. Across later settles and reimburses the vault including fees

I have built an MVP for this check out the demo here:



The benefits of filler vaults in this trust minized setup is that it unlocks wider filler participation. By decoupling skill from capital and enabling verifiable filler strategies we improve pricing through competition, increase liveness and deepen liquidity.

### The Bigger Vision

This architecture could also unify today’s fragmented filler markets. Currently, each app / wallet runs its own little mini market of intents. A shared middleware layer could consolidate these into a common infrastructure, where fillers deploy their strategies, on chain vaults provide liquidity, and apps/wallets auction off their intents to the full set of existing competing strategies in an open and transparent manner. Auction openness is important as it proves that there is no collusion between the intent protocol and the filler.

It’s also worth noting that the long tail is often poorly served by existing fillers. New intent protocols requiring more custom filler strategies could leverage filler vaults to have their community bootstrap liquidity for a specific filler strategy. Even new chains could seed filler vault capital to encourage inflows and better UX for onboarding users.

## Replies

**rookmate** (2025-05-26):

Really interesting concept. Specially the idea of anyone being able to profit from intent yield hyperliquid like vaults

---

**lancelot-c** (2025-05-26):

Very interesting, this should definitely be implemented at some point.

Unifying the filer market is necessary to truly solve Ethereum L2 interop in an optimal way. I guess bridges like Across & others won’t like the idea because it will decrease their revenue dramatically and push them into irrelevance (basically they will become frontend apps and will only survive with frontend fees)

---

**adachi-440** (2025-05-27):

interesting idea!

I have a few questions about settlement

1. Looking at the diagram, it seems that assets are returned from Arbitrum to Optimism, and the assets used as bridge fees are also returned. In this case, since Across’s LP fee is used, the fee is reduced, and furthermore, the available LP amount on Across may become a limiting factor for the transaction. Receiving the assets on the source chain and using a rebalancing tool like Everclear or a CEX might result in better profitability. (This could potentially be incorporated into the Filler Vault strategy itself.)
2. How do you view protocols that do not execute settlement automatically? For example, intent-based bridges like ERC-7683 or deBridge require the filler to send both the execution and settlement transactions. In that case, there would need to be a mechanism to enforce repayment on the filler, or alternatively, a separate actor that handles settlement requests.

---

**FredCoen** (2025-05-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/adachi-440/48/9828_2.png) adachi-440:

> How do you view protocols that do not execute settlement automatically? For example, intent-based bridges like ERC-7683 or deBridge require the filler to send both the execution and settlement transactions. In that case, there would need to be a mechanism to enforce repayment on the filler, or alternatively, a separate actor that handles settl

Hey [@adachi-440](/u/adachi-440) this is correct, if this was to go to production, the strategy would also manage rebalancing. You would essentially have a vault deployed on each chain the strategy participates in. So you can settle on the source chain and not be charged LP fees. Rebalancing would then be taken care of separately.

Regarding second point, yeah executing the settlement isen’t a problem here, Socket’s infra handles this really well

---

**vaibhavchellani** (2025-05-27):

The mental model here is, this thing allows fillers to become " verifiable scripts" and in these scripts you can write the fulfilment logic, the rebalancing logic and anything else you need.

---

**0xapriori** (2025-07-04):

Great write-up! Two thoughts come to mind (if you are willing to indulge ![:grin:](https://ethresear.ch/images/emoji/facebook_messenger/grin.png?v=12))

- What role do you see filler vaults playing with respect to cross-chain swaps?
- The Ethereum Foundation should consider providing liquidity for this initiative, given their new treasury policy. [It would be a credibility neutral source of liquidity that is not purely profit optimized like the liquidity belonging to the Arbitrum DAO for example].

[@barnabe](/u/barnabe)

---

**Suryansh-23** (2025-07-05):

why only limit this to intent filler vaults, maybe use-cases like using these deep liquidity vaults to perform cross-chain arbitrage could also work.

---

**Game111-cyber** (2025-07-20):

If Filler Vaults require strong on-chain verification mechanisms like ZK proofs or TEEs, how can smaller or newer filler strategies—who may not yet have the technical capacity to integrate such advanced cryptographic guarantees—compete for capital allocation against more established players? Could this recreate a new kind of barrier similar to the capital bottleneck we’re trying to solve?

