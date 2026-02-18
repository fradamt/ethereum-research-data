---
source: ethresearch
topic_id: 4052
title: Plasma Nano - A Plasma Cash Extension For Nano And Fractional Payment Processing
author: boneyard93501
date: "2018-11-01"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-nano-a-plasma-cash-extension-for-nano-and-fractional-payment-processing/4052
views: 1824
likes: 0
posts_count: 1
---

# Plasma Nano - A Plasma Cash Extension For Nano And Fractional Payment Processing

The [Dock protocol](https://dock.io/protocol) affords data owners the opportunity to take centralized control of their data by incentivizing sharing among data creators and data consumers via data owners’ consent. In many respects, Ethereum’s eco-system provides a perfect platform to back Dock’s protocol and Dock initially opted to [design and implement](https://medium.com/dock/moving-towards-scalability-docks-plasma-cash-poc-f8ce26966dc6?) the Plasma Cash reference model.

However, the gas costs associated with the life-cycle as well the non-fungible nature of the ERC721 token very quickly posed a barrier to process nano-payments. To wit, utilizing the (somewhat) optimized, still maturing Dock Plasma Cash contracts as an evaluation base, the minimum entry cost for a participant, entirely ignoring the data cost component, for a single ERC721 token is its mint cost of a minimum of USD 0.155 (225,012 gas). Similarly, the minimum exit cost for one ERC721 token with proof-chain length one, again ignoring the actual payment component expressed in DOCK token, is USD 0.317. Clearly, the gas costs amortized over one, or even a small number of,  transactions per ERC721 instance, each “worth” very little, results in anything but a cost-effective solution under the best of circumstances, i.e., long running one-to-one exchange reciprocity among fixed pairs of actors, leave alone in the dominant share pattern of many-to-few data consumers/producers.

Entry and exit gas costs even for Ethereum’s L2 solutions are still too high to make nano and fractionalized payment processing viable as the per-transaction cost floor massively exceeds “paywall” pricing by one or more orders of magnitude. Since a large volume of nano-payments in the cent, and possibly sub-cent, range are a critical aspect of the Dock solution, we created an extension to Plasma Cash: meet *Plasma Nano*.

Dock’s Plasma Nano addresses the crux of the nano-payment problem by spreading the (invariant) gas costs over a much larger number of transactions than what the (indivisible) ERC 721 token would ordinarily allow. In a nutshell, Plasma Nano introduces a (virtual) token, the CSC (cent sub-cent), at the L2 layer for which the allocation calculation is based on both the DOCK (ERC 20) value at entry, a fractionalization base, and the payload price. By pegging the CSC allocation relative to these fiat-driven parameters, which is somewhat akin to swaps, we can significantly increase the number of nano-payment transactions a participant can execute thereby reducing the per-transaction gas cost allocation. Moreover, this approach allows us to decouple the CSC from individual ERC 721 bindings and introduce the concept of fractional ownership in ERC 721 token pools. The latter concept is critical to allow more timely ERC 721 exits by the receiving parties. As a corollary, Plasma Nano results in much, much shorter transfer proof chains further limiting exit costs. It may be worth noting that this is not a probabilistic but deterministic solution. Moreover, since the tuning of Plasma Nano is primarily parameter-based, we see this solution easily applicable to other paywall-type exchange solution operating with nano-amounts, such as (streaming) IoT data exchanges.

To put Plasma Nano in perspective utilizing the gas cost parameters outlined above, a data consumer entering with, say, the DOCK equivalent of USD 2.00 + entry gas, some USD 2.155 in total, a fractional base parameter of 0.001, and a CSC allocation parameter of 1, can now consume 200 data packages priced at USD 0.01 at a per transaction cost of USD 0.010775. Assuming we split gas costs into distinctly allocated components, a producer bearing the entire exit costs of one ERC 721 token ends up with a little over USD 1.60 for 200 shares (assuming the ERC 721 token was used only once and all fees including two updates to the mainnet are born by the data producer) for a $0.008 net transaction receipt. Of course, tuning the CSC allocation parameter via the ERC 721 denomination parameter can further decrease the per-transaction (gas) cost.

We are working to realize this solution in relatively short order; the first iteration of the ERC 721 contract modifications are in place and work on the settlement engine, including pool smoothing and allocation algorithms has also begun and we plan on having a testnet implementation in place by the end of November.

Since the discrete “clunkiness” inherent in the ERC 721-based Plasma Nano approach outlined above hasn’t been entirely lost on us, we already started to work on a revised protocol, think debit card rather than gift card, to further reduce per-transaction costs and reduced the slightly larger than ideal trustlesness gap introduced. This should provide an even more timely, smoothed-out exit process while still not requiring co-operative, online presence(s).

A (white) paper addressing some of the more detailed aspects of Plasma Nano, such as the impact of token burn, is also in the works.

cheers.
