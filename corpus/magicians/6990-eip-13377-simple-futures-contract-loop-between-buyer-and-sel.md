---
source: magicians
topic_id: 6990
title: "EIP-13377: Simple futures contract \"loop\" between buyer and seller for digital products"
author: M8loss
date: "2021-09-01"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/eip-13377-simple-futures-contract-loop-between-buyer-and-seller-for-digital-products/6990
views: 687
likes: 0
posts_count: 1
---

# EIP-13377: Simple futures contract "loop" between buyer and seller for digital products

**Abstract: EIP-13377:** A futures contract “future loop” between buyer and seller ensures price security when buying, for example, a digital tattoo motif. The “loop” of the transaction is only fully executed when the processing time of around 1-2 weeks or freely definable has been completed. The time of the order (transaction execution) up to the completion or handover of the product (transaction confirmation), with a suitable correction between the fiat price and the ether value, is located.

**Motivation:** In trading, we would say “futures” are for professionals, but in principle they are a “futures contract” with the oldest financial instrument there is. This is because farmers were able to sell their crops in advance and then had a certain degree of planning security. As already mentioned, futures contracts are standardized and therefore very transparent. Each contract stipulates which goods must be delivered when and at what price.

**Implementation:** This mechanism would have to be built into the interface of, for example Ledger or MetaMask???

**Example:** Let us assume that a digital artist would like to secure works of art by means of an appointment transfer to his cover-up in order to secure prices. He intends to hedge EUR 50. How could such a contract look like ??? At the beginning, as with all “derivatives”, we need the base value. This is derived from the underlying basic product, the tattoo template. In addition, it must be stipulated in the contract which delivery quantity and templates the “future” includes. If the futures contract contains an amount of 100 EUR and 2 tattoo templates, the digital artist must sell 2 futures to the buyer in order to achieve the desired price hedging. There must be no minimal price change in this appointment transfer. When closing, the execution date must be recorded. This could be set to two weeks for the tattoo template, for example.

You can also look at the [german forum](https://m8loss.xyz/forums/topic/eip-13377-einfacher-future-kontrakt-zwischen-kaeufer-und-verkaeufer/), for german discussion.

If there is already some kind of this idea or is technically feasible, I apologize.

Best regards,

M8loss
