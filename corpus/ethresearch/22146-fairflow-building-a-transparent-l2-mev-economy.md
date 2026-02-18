---
source: ethresearch
topic_id: 22146
title: "FairFlow: Building a Transparent L2 MEV Economy"
author: kosunghun317
date: "2025-04-14"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/fairflow-building-a-transparent-l2-mev-economy/22146
views: 448
likes: 4
posts_count: 2
---

# FairFlow: Building a Transparent L2 MEV Economy

# FairFlow: Building a Transparent L2 MEV Economy

**About the Author**

The author, [Ko Sunghun](https://x.com/wycfwycf), is a researcher at Radius. The author thanks [Tariz](https://x.com/Hyunxukee), [AJ Park](https://x.com/ZeroKnight_eth), and Chanyang Ju from [Radius](https://x.com/radius_xyz) for their feedback and helpful comments.

**TL;DR**

- We reviewed existing sequencing policies used by L2s and explained how out-of-protocol players recently adopted new strategies to game the policy.
- We suggested FairFlow, a tweaked version of TimeBoost, as an alternative that may prevent such activities and eventually enable L2s to internalize more revenue.

*This is a cross-posted version of [a blog post](https://hackmd.io/@kosunghun317/BJ3GNEBAye).*

# Introduction

Layer 2 networks (L2s) provide low transaction fees and faster execution times, playing a vital role in maintaining the Ethereum ecosystem as a leading player in the blockchain industry. The economic growth of L2s not only drives the adoption of the Ethereum network but also attracts even more users. However, at present, there is no clear source of revenue at the protocol level for newly launched L2s beyond transaction fee income. As low fees are a key factor in their adoption, L2s cannot simply increase costs to achieve profitability. Consequently, capturing Miner Extractable Value (MEV) without compromising user experience, such as through capturing backrun revenue, has become a significant challenge. Various sequencing strategies have been proposed and implemented, but recent reports indicate that certain types of opportunities can be exploited, allowing some to game the system and capture a substantial portion of MEV without sharing it. In this post, we will thoroughly examine these phenomena and previous attempts and propose an alternative sequencing policy designed to mitigate such tactics and internalize more revenue, ultimately promoting the economic growth of L2s.

## Existing Sequencing Policies

### Block Auction

Block Auction is the method used on Ethereum L1. It relies on the fact that there is no in-protocol rule for ordering transactions, and any valid transaction can be included in a block. External experts compete for the right to build the entire block, and the winner is given complete control over the block building.

### Priority Ordering

In [Priority Ordering](https://www.paradigm.xyz/2024/06/priority-is-all-you-need), valid transactions are greedily sequenced in descending order based on `priorityFeePerGas`. This simple approach works well in most cases, and is the default setting of OP Stack chains. Under priority ordering the profit-seeking players (searchers) are willing to pay higher fees to secure positions at the top of the block. In contrast, regular users, who are less sensitive to transaction orders and waiting time, can still include their transactions even with lower fees.

### FCFS

First-Come, First-Served (FCFS) processes transactions in the chronological order they are received. Although this approach appears intuitive and fair (and is preferred by regular users), it suffers from significant drawbacks. The intense competition among searchers results in spamming the network, which wastes blockspace. Moreover, the efforts of searchers for lower latency are invested in out-of-protocol infrastructures (e.g., colocation), and protocol earns nothing from it.

### TimeBoost

Proposed in 2023, [TimeBoost](https://arxiv.org/pdf/2306.02179) is built on FCFS but adds an option to boost the transaction’s submission time based on an attached bid. This mechanism incentivizes time-sensitive participants, such as searchers, to pay more and thus works as an additional source of revenue for rollup. In the Arbitrum’s implementation, the winner of a periodic auction enjoys delay-free inclusion for the next minute, while transactions from the rest incur a 200 ms delay.

### Secure Block Building (SBB)

[SBB](https://docs.theradius.xyz/overview/secure-block-building-sbb), proposed by Radius, allows the L2 sequencer to capture backrunning profits without compromising the user experience (UX). First, a user’s transaction is quickly confirmed (in bundle units) by the L2 sequencer, and once confirmed, that bundle is forwarded to the searcher. Then, the searcher creates a backrunning transaction based on the received bundle, and this newly created transaction is included at the bottom of the L2 block. Throughout this process, an encrypted mempool is employed, that is, the user’s transaction is transmitted to the L2 sequencer in an encrypted form to guard against malicious manipulation, while the searcher uses the decrypted information upon receipt to identify backrunning opportunities efficiently.

## Evolving Searcher Activities

Despite the sequencing policies, which aim to receive more fees from those who find more value from (faster) inclusion, searchers can avoid paying high fees and capture the value for specific opportunities. The two below are among such tactics.

### Blind Backrunning

Blind backrunning is a form of atomic arbitrage that identifies swap opportunities amid transaction execution. This strategy is feasible primarily on blockchains with low gas fees. Bots employing blind backrunning flood the network with transactions from numerous accounts, each set with different (e.g., priority fee) configurations. On chains with priority ordering (e.g., Base) or FCFS rule (e.g., Arbitrum), this tactic allows bots to backrun nearly every transaction. Such behavior not only siphons value away from the protocol but also makes it harder for the protocol (L2 in this case) to internalize transaction revenue fully. Moreover, since many of these transactions end up reverting (recently, the revert ratio has declined, but this does not necessarily mean the blind backrunning activity has decreased; see [here](https://blockworks.co/analytics/base/base-onchain-activity)), the blockspace is wasted just for checking the price of DEX pools multiple times.

### Private Order Flow

Private order flow on L1 has been criticized for [accelerating centralization](https://arxiv.org/abs/2305.19150). In L2, it is still problematic but the reason is slightly different; it undermines the protocol’s revenue internalization. Entities with private order flow can create “pseudo” bundles that capture nearly all the revenue from backrunning. All of sequencing mechanisms described above are vulnerable to this vector. For example, under priority ordering policy, a searcher can set its transaction’s `priorityFeePerGas` just 1 wei lower than that of the targeted user transaction, nearly guaranteeing that its transaction will be positioned immediately after the user transaction. Similarly, in FCFS or its variants, sending multiple transactions with minimal delay almost guarantees a backrunning opportunity (it was how [Polygon Fastlane guaranteed bundling](https://fastlane-labs.gitbook.io/polygon-fastlane/what-is-polygon-fastlane/component-diagram)).

Moreover, most deals between searchers and dApps (or wallets) are made off-chain, and there is no standardized marketplace for order flow. Such opaque and non-transparent market landscape of private order flow causes informational asymmetries between sellers (transaction originators) and buyers (searchers), causing inefficiencies.

## Previous Attempts

While the context may vary slightly, there were multiple attempts to tackle similar problems.

### Speed Bumps

In traditional finance (TradFi), exchanges often adopt [asymmetric speed bumps](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3221990) to disincentivize quote sniping and increase liquidity. Since this policy targets only a particular type of order (quote sniping market order), the situation resembles our case. We do not want to introduce too complicated a mechanism or ad-hoc policy; we want to disincentivize the blind backrunning and the induced waste of blockspace.

### Local Fee Markets

In Solana and [several other chains](https://docs.sui.io/guides/developer/advanced/local-fee-markets), local fee markets are suggested and adopted so that interacting with only specific contracts or storage that is frequently touched becomes expensive, while other transactions remain cheap. Again, this policy may work well for L2s to prevent or disincentivize blind backrunning. However, it risks the degradation of UX for transactions that include the transfer of several popular ERC-20 tokens and will be [hard to implement](https://www.helius.dev/blog/solana-local-fee-markets) appropriately.

### SEC Order Competition Rules

The SEC recently proposed [the order competition rule](https://www.sec.gov/rules-regulations/2022/12/order-competition-rule) called Proposed Rule 615 to solve the problem with private order flow. Their primary rationale was that by forcing the auction for the right of routing each order, they might assure the investor of a better execution than the status quo. Although it did not result in implementation, it is notable that holding an auction for each order or transaction is a viable option.

# Introducing FairFlow

In this section, we present a variant of TimeBoost called FairFlow, which seeks to capture revenue from backrunning opportunities that current sequencing methods overlook, without compromising user experience. It achieves such goal by enshrining a marketplace for backrunning that anyone can participate in. By combining elements of a Dutch auction with TimeBoost, FairFlow incentivizes searchers to engage and compete within this designated market instead of relying on third-party OFA protocols. We believe that FairFlow can assist Layer 2 solutions in reclaiming value from backrunning more effectively and reducing blockspace waste.

## Goals

Below are the objectives we aim to achieve with FairFlow:

**Establishing a Permissionless Marketplace for Backrunning Opportunities**

We aspire to create a marketplace that fosters healthy competition among searchers and facilitates price discovery for each backrunning opportunity. Our ultimate goal is to enhance the overall efficiency and transparency of order flow markets, and making it a dominant strategy to send transaction directly to FairFlow for users.

**User Protection**

We strive to minimize the risks associated with sandwich and front-running attacks, and waste of blockspace induced by spam transactions. Our aim is to create an environment where L2 users can transact safely and conveniently, without significant delays or additional costs.

**Building a sustainable L2 economy**

By internalizing backrunning revenue at the protocol level, we support L2 in developing a stable revenue structure. This approach is expected to foster a virtuous cycle that contributes to the growth of the entire Ethereum ecosystem.

## How it works

As mentioned, FairFlow is essentially a variation of Arbitrum’s TimeBoost, and its sequencing policy can be largely divided in three steps:

1. When the sequencer receives a user transaction, it initiates a Dutch auction for the right to backrun that transaction. Searchers who want to backrun the user transaction send an EIP-712 signature for the bid and backrunning transaction to the auctioneer (sequencer). Note that the user may attach the bid for herself (self-bid).
2. When the reserve price becomes less than or equal to one of the submitted bids, the auction is closed, and the user transaction and backrunning transaction (if any) are bundled together then added to the BundleList.
3. At each block creation, bundles are selected from the BundleList—up to the gas limit—and included in the block for sequential execution in an FCFS manner (i.e., the older bundle is executed earlier).

In short, to achieve aforementioned goals, we adopted TimeBoost’s mechanism with simple tweak: enabling *anyone* to boost user’s transaction by bidding on behalf of user, and in exchange she receives a right to backrun the user transaction. In the following section we explain the rationale behind of such design, and how it will eventually disincentivize spamming blind backrunning trials and enable L2s to earn more revenue.

## Analysis

### Rationale

- Single Public Market
Every transaction is disclosed to subscribers before its inclusion, establishing this market as a dominant and aggregative platform for order flow. This approach reduces fragmentation and enhances price discovery.
- Dutch Auction
By implementing an off-chain auction system, we can limit spam transactions to a maximum of one per user transaction. Additionally, the nature of a Dutch auction allows the protocol to effectively capture revenue, even in the presence of third-party On-chain Frontrunning Alternatives (OFA) protocols. If a searcher obtains information about an incoming transaction, they must pay a high price; otherwise, that information will be shared with others, preventing them from effectively exploiting the situation without adequate compensation.
Furthermore, even if an external third-party protocol manages to bundle transactions, such as by utilizing a signature-based off-chain auction that renders the user’s intent and the searcher’s operations inseparable, they will generally incur more delays. This is because the searcher who wins the auction to fulfill the user’s intent will have reduced budget resources (having paid to win the OFA), thereby limiting their ability to bid sufficiently to boost the transaction. As a result, for time-sensitive activities like NFT minting or purchasing newly launched memecoins, using such a platform may not prove to be the most optimal choice.

### Expected Results

We primarily anticipate two key outcomes:

- Reduction in spam and waste of blockspace: By limiting the occurrence of blind backrunning trials to a maximum of one per user transaction, even in scenarios with multiple entities attempting blind backrunning, we expect a significant decrease in wasted blockspace.
- Enhancement of internalized revenue and market efficiency: Rather than having order flow distributed across fragmented and opaque markets, all transactions will be facilitated within a single market featuring numerous competitive bidders. This consolidation will improve the efficiency and price discovery of order flow, ultimately boosting the revenue for the protocol and its aligned partners.

### Limitations

- We note that under current version the transaction originators (wallets and dApps) cannot earn revenue, and blindly setting kickback policy would further distort the dynamics (revenue sharing may result in lowering the reserve price for searchers). While we do not discuss in kickback or revenue sharing in this post, it seems like manually whitelisting addresses (e.g., multisig treasury of aligned dApps) for revenue sharing is a correct policy in general.
- Additionally, while it is generally unwise economically, sandwich attacks or frontrunning are theoretically feasible by outbidding a user transaction immediately upon receipt and discerning the user’s intent. However, it is important to note that even if such an attack is possible, the attacker faces significant risks, as their own attacking transaction would also be broadcast to other searchers and backrunnable.
- It is hard to set the parameters correctly. For FairFlow to work as intended and not hinder user experience, the auction period should be neither too long nor too short. If it is too long, average users will experience a too long delay. If it is too short, no searcher will adequately value the backrunning opportunities and choose to spam or ignore them. Moreover, the reserve price curve should properly decay to capture the full value adequately. While we do not provide exact numbers in this post, we mention general points to be considered in the later section.

# Technical Description

This section describes the mechanism and overall system in greater detail.

## Glossary

- Sequencer: The L2 entity responsible for receiving user transactions, initiating the backrunning auction, and managing the ordering of transactions for block inclusion.
- User: The end-user or dApp that submits a transaction for inclusion in L2 block.
- Searcher(s): Entities (bots or operators) that monitor pending transactions, participate in auctions, and submit backrunning transactions.
- Executor: The L2 entity that aggregates and executes transactions in each block. While it does not need to be a different entity from Sequencer, to help understanding in this article we divided them in two.
- UserTx: The original transaction submitted by the user.
- Auctioneer Contract: a smart contract that maintains balance of each bidder and settles payment for each auction.
- Bid: A submission from a searcher or advanced user, in the form of an EIP-712 signature, indicating their willingness to backrun a given transaction for a specified fee.
- BackrunTx: The backrunning transaction submitted by a searcher as part of their bid.
- BundleList: The ordered queue that stores finalized bundles (each comprising a UserTx and, if applicable, a winning BackrunTx) waiting for inclusion in the block.
- Auction Parameters: These parameters determine the shape of the reserve price curve for a Dutch auction. While the needed parameters can vary across the base curve (linear, reciprocal, exponential, …), this article introduces the following:

max_period: The maximum period the auctioneer will wait for the bid, i.e., the maximum possible auction duration.
- min_price: Minimum price that the auctioneer wants to receive. If no bid exceeds or equals this value, the auction will be resolved with no winner after the max_period passes.
- decay_rate:  The rate of decrease of reserve price.

## Lifecycle of Transaction

[![Untitled-2025-01-17-2335](https://ethresear.ch/uploads/default/optimized/3X/9/e/9ee7c48dc267c1e0cc16d0012f88af5aa54490b4_2_690x178.png)Untitled-2025-01-17-23354298×1110 641 KB](https://ethresear.ch/uploads/default/9ee7c48dc267c1e0cc16d0012f88af5aa54490b4)

Under FairFlow, a user’s transaction undergoes the following procedure:

1. Submission:
A User submits a transaction (UserTx) to the Sequencer, and optionally a Bid for Dutch auction.
2. Auction Initiation:
Upon receiving a new UserTx, the Sequencer initiates a Dutch auction for the right to backrun the transaction.
3. Notification:
The Sequencer forwards the UserTx details to Searcher(s) who subscribed to the user transactions with FF_newPendingTransactions API.
4. Bidding:
Searcher(s) analyze the pending transaction for backrunning opportunities. If an opportunity is identified, a searcher submits a Bid and a BackrunTx using the FF_submitBackrunTxAndBid API.
5. Auction Resolution:
The Sequencer waits until the reserve price (determined by a decaying reserve price curve) falls below one of the submitted valid bids. At that point, the auction closes, and a winning bid is determined. (Note: There may be no winner if no searcher is interested.)
6. Bundling:
The resulting bundle (containing the original UserTx and, if applicable, the winning BackrunTx) is added to the BundleList.
7. Preconfirmation:
An order commitment is issued to the user, ensuring the transaction will be executed in a predetermined order.
8. Block Inclusion:
Just before block creation, the Sequencer selects the oldest bundles from the BundleList (up to the gas limit) and delivers them to Executor via the FF_requestBundleList API.
9. Block Construction:
The Executor constructs a block by sequentially executing transactions within the received bundles, and publish it.

## Backrunning Auction

In this section, we explain the auction itself with a greater depth.

### Reserve Price Curve

The shape and parameters of the reserve price curve are crucial. Improper settings can lead to negligible value capture while inducing excessive delay. We propose two curve models:

#### Linear Decaying Curve

[![image (2)](https://ethresear.ch/uploads/default/optimized/3X/2/5/25724259179b74b0306976acde5b9dd5f997e255_2_690x441.png)image (2)855×547 26.8 KB](https://ethresear.ch/uploads/default/25724259179b74b0306976acde5b9dd5f997e255)

Linear decaying curve is a simple and intuitive model that decreases the reserve price at a constant rate:

`reserve_price(t) = min_price + decay_rate × (max_period - t)`.

While it may fail to capture the full value in case of outliers, many protocols have adopted such a curve due to its simplicity. Such protocols include:

- 1inch Fusion: 1inch Fusion adopted a partially linear curve configurable by the user.
- UniswapX: Similarly to 1inch Fusion, UniswapX sells the right to fill the user order to “fillers” in Dutch auction format, with a linear curve configurable by the user.
- Other examples include, but are not limited to, DAI’s liquidation auction, Opyn’s crab strategy vault’s rebalancing auction, etc.

#### Reciprocal Decaying Curve

[![image (3)](https://ethresear.ch/uploads/default/optimized/3X/5/e/5e7e40efde30170612f83d1241c757a855e32809_2_690x441.png)image (3)855×547 53.4 KB](https://ethresear.ch/uploads/default/5e7e40efde30170612f83d1241c757a855e32809)

This model uses the inverse of a function that was initially suggested in [the original TimeBoost paper](https://arxiv.org/abs/2306.02179), referred to as the simplest form of delaying function:

`reserve_price(t) = min_price + decay_rate × (max_period / t - 1)`.

Provided that searchers’ latency is low enough, it can capture most of the value in almost every case.

#### Setting Parameters and Trade-Offs

While each L2 can freely select the curve and parameters, some general recommendations exist for setting parameters.

- The maximum period should not be too long, as it may damage the user experience. We recommend that the period be set under 1 second, which is more than enough for most searchers who target users’ transactions for backrunning arbitrage opportunities. Several other platforms and trials are also adopting around 100ms-500ms auction period.
- The curve should not decay too much at earlier periods. Due to the physical limit, some latencies cannot be avoided, and only a handful of players can bid at that time, which leads to value leakage. Thus, at the very beginning, the price should be set higher than the expected value, and it is recommended to adopt either a reciprocal curve or a linear curve with kink at earlier periods.
- It is recommended that the parameters be iteratively adjusted so that most of the resolution can occur within the middle of the auction rather than at the beginning or the end.
- Another metric to consider is the gap between the bid and the reserve price at the moment of bid reception. Most searchers will minimize the time gap between bid submission and auction resolution to avoid volatility. If the gap is too big, the curve may decay too fast and fail to capture the full value.

### Bid Settlement

Searchers or advanced users submit their bids with a `BackrunTx` using an EIP-712 signature. The `Auctioneer Contract` on each L2 processes these submissions. The auction is resolved once the decaying reserve price falls below one of the submitted bids. An auctioneer account owned by `Sequencer` will send the settlement transaction, which will deduct the bidder’s balance in `Auctioneer Contract`. Note that the settlement may not be synchronous to the execution of the bundle. Also, while `Sequencer` may not need to simulate execution and track the entire state of chain, it will track the balance of bidders at vault and will only accept the bid such that lastly reported balance is greater than certain threshold multiple of submitted bid. This is to prevent insolvency. Monad implemented [a similar system](https://docs.monad.xyz/monad-arch/consensus/asynchronous-execution#balance-validation-at-time-of-consensus) to provide both fast inclusion while preventing spamming from low balance accounts.

## Specifications

In this section, we provide sequence diagrams and specifications to further clarify the structure and how each entity interacts.

### User ↔️ Sequencer

[![mermaid-diagram-2025-04-12-203839](https://ethresear.ch/uploads/default/optimized/3X/6/c/6c2a8859c4606d6a73fb4cbb87050d2fc8d86d8e_2_690x473.png)mermaid-diagram-2025-04-12-2038392319×1590 177 KB](https://ethresear.ch/uploads/default/6c2a8859c4606d6a73fb4cbb87050d2fc8d86d8e)

`eth_sendRawTransaction`: Standard transaction submission.

`FF_sendRawTransactionAndBid`: submission for advanced users that includes an optional self-bid. Through self-bidding, users can accelerate their transactions.

### Searcher ↔️ Sequencer

[![mermaid-diagram-2025-04-12-203803](https://ethresear.ch/uploads/default/optimized/3X/4/1/41abef6aa85adb08c64c1ddc42a2cec22f0bb23b_2_690x473.png)mermaid-diagram-2025-04-12-2038032319×1590 184 KB](https://ethresear.ch/uploads/default/41abef6aa85adb08c64c1ddc42a2cec22f0bb23b)

`FF_newPendingTransactions`: Allows searchers to subscribe and receive notifications about new pending `UserTx` submissions.

`FF_submitBackrunTxAndBid`: Enables searchers to submit an EIP-712 signed bid along with the `BackrunTx`.

`FF_newBundleAdded`: This allows searchers to subscribe and receive notifications about newly added bundles to simulate and guess the most recent state of the chain.

### Executor ↔️ Sequencer

[![mermaid-diagram-2025-04-12-203536](https://ethresear.ch/uploads/default/optimized/3X/8/5/85e6f88d612efcd4c00e7ce4f9817413a58d3a75_2_690x473.png)mermaid-diagram-2025-04-12-2035362319×1590 163 KB](https://ethresear.ch/uploads/default/85e6f88d612efcd4c00e7ce4f9817413a58d3a75)

`FF_requestBundleList`: The executor uses this endpoint to retrieve the finalized bundles (`UserTx` + `BackrunTx`) for block construction.

# Conclusion

Through this post, we have examined existing sequencing policies and how recently developed strategies are exploiting these policies, ultimately degrading user experience and hindering protocols from effectively internalizing revenue. In response, we propose FairFlow, which establishes a single public auction market, allowing all participants to bid fairly for backrunning opportunities. Our design specifically implements a protocol-level auction for each transaction and implicitly introduces additional delays for transactions that contain privately extracted MEV outside the protocol. This mechanism not only incentivizes market participants to engage in the public auction but also enables L2s and searchers to internalize MEV from backrunning opportunities more efficiently, addressing inefficiencies arising from private order flow markets and spam transactions. We provide detailed APIs and sequence diagrams to further elucidate the implementation. We hope this design will be helpful and sound enough for upcoming (or existing) L2s to adopt.

## About Radius

[Radius](https://www.theradius.xyz/) is dedicated to advancing Ethereum’s L2 ecosystem with fair and transparent MEV capture. Our protocol-level backrunning infrastructure supports the sustainability and profitability of L2s, contributing to our vision of Ethereum’s growth as a leading platform.

Our research on FairFlow explores potential approaches to L2 challenges. If you’re interested in learning more about our research or products like [Secure Block Building (SBB)](https://docs.theradius.xyz/overview/secure-block-building-sbb) or [Lighthouse](https://docs.theradius.xyz/overview/lighthouse), we’d love to [connect](https://www.theradius.xyz/contact). Together, we can help L2s generate stable revenue, attract users, and strengthen the Ethereum ecosystem.

## Replies

**0xJermo** (2025-04-20):

1. If an auction mechanism were to be implemented prior to the user transaction, would this not introduce additional latency, thereby making the private transaction flow a more efficient alternative?
2. How easy is the transition from a FCFS/Timeboost model to FairFlow?
3. Is there an estimate of the MEV savings that an end user might end up saving when using FairFlow compared to Timeboost?

