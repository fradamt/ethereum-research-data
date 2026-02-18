---
source: magicians
topic_id: 22507
title: "Smart Bidding: Gas Pricing Automation Strategies"
author: sbacha
date: "2025-01-13"
category: EIPs
tags: [wallet, gas, eip]
url: https://ethereum-magicians.org/t/smart-bidding-gas-pricing-automation-strategies/22507
views: 132
likes: 1
posts_count: 2
---

# Smart Bidding: Gas Pricing Automation Strategies

# Smart Bidding: Gas Pricing Automation Strategies

- Slow
- Medium
- Fast

Users Pick Fast, who doesn’t want their transactions (or shipments/packages/etc) delivered **fast**?

The semantics are thus meaningless for users. I am drafting a suggested alternative to the typical gas pricing nomenclature with a different view that captures what gas pricing actually is, **a bidding process**. The idea is to curate high-level *bidding strategies* vis a vie pricing their transaction in relation to a key objective/stated preference.

> These are not just for EOA’s, they are applicable potentially to ‘Agents’ as well

| Strategy Name | Description | Key Parameters | Example Use Cases |
| --- | --- | --- | --- |
| MAX_SPEED | Aim for earliest possible on-chain inclusion, usually referencing top-percentile mempool tips. | - maxFeePerGas (optional fallback)- priorityBuffer (how much above top percentile) | - Rapid DeFi trades- Urgent NFT mint- Liquidation rescue |
| TARGET_CPI | Target a specific cost per inclusion: system attempts to stay below a user-defined maximum fee. | - targetFee (max gwei for priority)- timeTolerance (how many blocks user can wait) | - Casual token transfers- Routine on-chain tasks where speed is less critical |
| MEV_ROI | For MEV searchers seeking a minimum return-on-investment (ROI) on gas costs or priority fees. | - roiThreshold (desired ratio of profit to gas cost)- timeTolerance | - Arbitrage & sandwich attacks- Liquidation bots |
| CENSORSHIP_RESIST | Prefers block builders/relays known to be censorship-resistant, may pay additional premium. | - preferredRelays[] (list of known neutral builders)- feePremium (extra tip if needed) | - Transactions with strong censorship concerns- Tornado Cash or other blacklisted addresses |
| MAX_VALUE | For batching multiple transactions, tries to choose those with the best net payoff. | - budget (overall gas budget)- timeHorizon (deadline for all txs) | - Bulk NFT minting- DeFi strategies spanning multiple interactions |

| Parameter | Type | Associated Strategy(ies) | Description | Example Value |
| --- | --- | --- | --- | --- |
| maxFeePerGas | uint | MAX_SPEED (fallback) | Upper bound for total gas fee (base + priority). Even if the strategy suggests a higher tip, it cannot exceed this. | 200 gwei |
| priorityBuffer | uint | MAX_SPEED | Additional tip to outbid top mempool percentile. | 2 gwei |
| targetFee | uint | TARGET_CPI | Ideal maximum for total transaction fee. The wallet or aggregator tries not to exceed this. | 30 gwei |
| timeTolerance | uint | TARGET_CPI, MEV_ROI | Number of blocks (or seconds) the user can tolerate waiting. If not included by then, fee might be recalculated. | 60 blocks |
| roiThreshold | float | MEV_ROI | Target ratio: (Profit / GasCost) must exceed this to proceed. | 3.0 (i.e., 300%) |
| preferredRelays[] | string | CENSORSHIP_RESIST | List of block builders or relays that do not censor. | ["relayA", "relayB"] |
| feePremium | uint | CENSORSHIP_RESIST | Extra tip beyond normal to incentivize censorship-free builders. | 5 gwei |
| budget | uint | MAX_VALUE | Total gas or ether budget for a set of bundled transactions. | 0.2 ETH |
| timeHorizon | uint | MAX_VALUE | Deadline (in blocks or seconds) by which transactions in the bundle must be completed. | 3600 seconds |

## Example Scenarios Table

> how this might be used in different user scenarios

| Scenario | Chosen Strategy | Parameters | Outcome |
| --- | --- | --- | --- |
| User wants the fastest possible inclusion for a DeFi trade during an NFT mint rush. | MAX_SPEED | - maxFeePerGas: 300 gwei (fallback)- priorityBuffer: 5 gwei | Wallet sets a top-percentile tip + buffer. The user’s tx likely gets into the next block but pays a premium. |
| User only does routine transfers and wants to avoid overpaying, even if it takes a while. | TARGET_CPI | - targetFee: 20 gwei- timeTolerance: 50 blocks | The wallet tries not to exceed 20 gwei priority. If mempool is busy, the user’s tx might wait until fees drop. |
| An MEV searcher running an arbitrage bot wants 300% ROI on gas. | MEV_ROI | - roiThreshold: 3.0 (i.e., 300%)- timeTolerance: 5 blocks | Bot logic checks if (Profit / GasCost) ≥ 3. If yes, it broadcasts with fees to ensure acceptance. If the ratio dips, it aborts. |
| A user is concerned about censorship and is willing to pay a higher tip for a neutral builder. | CENSORSHIP_RESIST | - preferredRelays[]: [“relayA”]- feePremium: 10 gwei | The wallet routes the transaction via relayA if it’s online, adding a 10-gwei premium so the builder is incentivized to include it. |
| A DeFi power-user wants to send multiple transactions to maximize overall value within a fixed budget. | MAX_VALUE | - budget: 0.1 ETH- timeHorizon: 7200 seconds | The wallet looks at possible queued transactions and prioritizes those with the highest net expected value. |

I have not yet created a formal proposal, I am soliciting feedback from everyone and anyone interested.  ![:saluting_face:](https://ethereum-magicians.org/images/emoji/twitter/saluting_face.png?v=15)

## Replies

**ivanmmurcia** (2025-01-16):

Very interesting proposal above all to emphasize the importance of censorship resistant, however, I think it is not for the average person, it would be the job of the wallets and/or developers to abstract this.

