---
source: ethresearch
topic_id: 22327
title: "Auto-Rollover Perpetuals (ARP): A Novel Funding-Free Synthetic Perpetual Futures Design for Decentralized Exchanges"
author: dev-clober
date: "2025-05-13"
category: Applications
tags: []
url: https://ethresear.ch/t/auto-rollover-perpetuals-arp-a-novel-funding-free-synthetic-perpetual-futures-design-for-decentralized-exchanges/22327
views: 317
likes: 0
posts_count: 3
---

# Auto-Rollover Perpetuals (ARP): A Novel Funding-Free Synthetic Perpetual Futures Design for Decentralized Exchanges

## 1. Background and Motivation

Perpetual futures have become exceptionally engaging trading products due to their ability to offer high leverage, resulting in significant user engagement and trading volumes. Recently, the rise of high-performance blockchain platforms has facilitated the emergence of fully on-chain order books, bringing increased attention to order book-based perpetual decentralized exchanges (DEXs).

However, traditional perpetual futures rely on periodic funding rate payments to maintain their peg to spot prices. Implementing such periodic funding payments entirely on-chain is costly, computationally intensive, and fundamentally unscalable.

In response to these challenges, we introduce Auto-Rollover Perpetuals (ARP), specifically designed to offer a scalable and economically sustainable perpetual futures mechanism tailored for decentralized on-chain environments without relying on funding rates.

## 2. Core Idea of ARP

ARP replaces traditional periodic funding payments with a novel combination of automatic futures contract rollovers and a Force-Settlement mechanism. At its core, ARP functions as a synthetic perpetual futures contract, structured as expiring futures contracts that automatically roll over, thereby offering traders continuous exposure without manual interventions or periodic funding payments.

The key innovation in ARP is the Force-Settlement mechanism, allowing participants to settle positions directly against the underlying spot price at predetermined intervals (e.g., monthly). If the futures price deviates significantly from the spot price as settlement approaches, market participants can opt to exit their positions at the nominal spot value through Force-Settlement.

The existence of the Force-Settlement mechanism naturally discourages trading at prices significantly deviating from the spot price as the settlement date nears, assuming sufficient market liquidity. Traders opting into Force-Settlement must pay a premium fee (for example, 15 basis points), further reducing incentives for unnecessary settlements. Although Force-Settlement may initially appear unfavorable from a trading experience perspective, its true strength lies in its mere existence, inherently ensuring effective price pegging and making actual settlements rare. Additionally, even traditional funding-based perpetuals occasionally enforce position closures under extreme market conditions, making the potential execution of Force-Settlement in exceptional circumstances a reasonable and transparent trade-off for overall market stability.

## 3. Technical Details

ARP leverages Collateralized Debt Positions (CDPs) as the foundational infrastructure for synthetic asset creation. Users deposit USDC to mint cUSD at a 1:1 ratio, which is then utilized to issue and trade synthetic perpetual futures assets (e.g., synthetic BTC or ETH).

- Long Positions: Users deposit cUSD into a dedicated smart contract account, enabling additional leveraged cUSD issuance restricted within the platform. For instance, a user depositing 10,000 cUSD can issue an additional 90,000 cUSD for internal use, creating a total leveraged position of 100,000 cUSD used to purchase synthetic assets, establishing leveraged long exposure.
- Short Positions: Users deposit cUSD as collateral to directly issue synthetic assets, which are then immediately sold into the market to establish short exposure. For example, a user depositing 10,000 cUSD can mint synthetic assets equivalent to that value, directly creating a short position.

**Force-Settlement Mechanism:**

At the end of each settlement period (for example, monthly), traders can opt-in for Force-Settlement, matching positions with counterparties based on a trusted oracle’s spot price. Traders choosing this option pay a premium fee to discourage unnecessary settlements. Arbitrageurs anticipate and capitalize on potential price deviations, proactively driving the perpetual futures prices toward spot prices, maintaining market stability without frequent actual settlements.

**Liquidation and Last Resort Force-Settlement:**

Positions exceeding predefined Loan-to-Value (LTV) thresholds are subject to liquidation. Liquidations involve selling the collateral at a discounted rate compared to the index price to recover the outstanding debt. Profits from liquidation activities are accumulated in the Insurance Fund. In rare cases where liquidation fails and the Insurance Fund is depleted, the protocol initiates a “last resort” Force-Settlement. This emergency measure forcibly settles outstanding positions against randomly selected counterparties at a further discounted price, ensuring the protocol’s overall solvency and integrity.

**ARP Market-Making Vault:**

The Market-Making Vault is an additional mechanism designed to allow users, regardless of their market-making expertise, to passively provide liquidity to synthetic asset markets. By depositing assets into the MM Vault, users enable market-making operations through short position CDPs and long position smart contract accounts with conservative leverage. This facilitates initial liquidity bootstrapping and ongoing market stability. While the MM Vault prioritizes handling Force-Settlement requests, it does not hold special privileges or core dependencies within the ARP system. Over the long term, as market participation grows, professional market-making firms and diverse market participants are expected to further enhance market depth and liquidity independently from the MM Vault. Managed by professional market makers, the vault dynamically adjusts spreads and liquidity based on market conditions, adhering strictly to predefined risk management practices encoded within smart contracts.

## 4. Benefits and Composability

ARP eliminates the scalability constraints and economic inefficiencies associated with traditional periodic funding rate payments. As high-performance chains increasingly adopt fully on-chain order books, ARP offers a scalable, cost-effective, and economically sustainable solution for perpetual futures trading.

Additionally, ARP-generated synthetic assets can be wrapped into fungible ERC20 tokens, substantially enhancing composability and utility across the broader DeFi ecosystem. This ERC20 compatibility enables synthetic assets to seamlessly integrate with and be freely utilized across various external DeFi platforms, significantly broadening their practical applications and user base.

## 5. Future Research Directions

Determining the optimal level of capital required in the liquidity ecosystem, including both MM Vaults and external liquidity providers, as well as in the Insurance Fund, to sustain effective market liquidity without relying on Force-Settlement remains an open research area. Under the assumption of effective pegging, it is unlikely that all participants on one side of the market would simultaneously seek to close their positions at settlement. Therefore, maintaining liquidity equivalent to a certain percentage of the total open positions, similar to partial reserves, should suffice. Identifying the precise percentage will require empirical data gathered through actual operation and continuous monitoring.

## Replies

**killroy192** (2025-05-15):

Thanks for sharing this idea. Could you please clarify who the counterparty is for the leveraged position? Is it an OTC-like deal or peer-to-pool?

Considering that force-settlement should happen during huge market imbalances, how does the system protect counterparties that do not want their position to be closed (and impermanent loss to be converted into settled loss)?

---

**dev-clober** (2025-05-26):

[@killroy192](/u/killroy192)

1. The leveraged position arises not when the synthetic asset is issued, but when it is traded in the market. That trade could occur OTC, through an on-chain order book (peer-to-peer), or via an AMM (peer-to-pool). In that sense, the counterparty model is independent of the ARP mechanism itself. That being said, ARP is designed under the assumption that these synthetic assets will primarily be traded via on-chain order books.
2. If a force-settlement must occur, then by design, counterparties on the other side are inevitably exposed to the risk of having their positions forcibly closed. This is part of the trade-off required to maintain solvency during extreme market imbalances. That said, at the operational level, the system can prioritize which positions to settle in a more reasonable way. For example, counterparties may be selected based on heuristics such as highest LTV, largest unrealized profit, or largest position size. This helps minimize disruption and spread the impact more fairly.

