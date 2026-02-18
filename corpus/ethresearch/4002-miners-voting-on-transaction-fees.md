---
source: ethresearch
topic_id: 4002
title: Miners voting on transaction fees?
author: nullchinchilla
date: "2018-10-29"
category: Economics
tags: []
url: https://ethresear.ch/t/miners-voting-on-transaction-fees/4002
views: 1888
likes: 4
posts_count: 4
---

# Miners voting on transaction fees?

I realize there’s been a lot of discussion over the best way to charge transaction fees, but if I don’t think anybody has proposed a system where the gas price is the same for all transactions in a block, and miners upvote/downvote the gas price by small increments rather than the gas limit. All transactions with that much fees goes through, otherwise it’s immediately rejected by the network, and there is no long-lasting mempool of transactions with too-low fees.

It seems like this would make fees a lot more stable, and users would be able to know for sure whether or not their transaction will get through. Users sending transactions with low fees will also not take up space in the mempool: currently those transactions could actually incur *higher* costs to miners since they have to be kept around for so long and might never be included in a block. When congestion happens, miners would upvote the gas price higher and higher; people unable to bear the price will simply wait a while before trying to send their transaction, rather than sending their transaction to have it languish in a mempool for hours.

Such a system, especially if miners’ income comes mostly from transaction fees, would definitely cause higher fees, but that’s not necessarily a bad thing as it incentivizes people to run validators. Under the current system, if blocks aren’t full validators basically can’t make any money out of transaction fees, and the incentive is to quit being a validator, until the number of validators is small enough that the small amount of transaction fees can cover their total cost. Under my proposal, the validators as a whole would act as a monopolistic cartel and raise fees towards the revenue-maximizing point, above which people start quitting using Ethereum because the fees are too high and the total amount of fees drops.

Nobody proposing this system probably means it absolutely sucks, though. Perhaps a miner cartel deciding fees would lead to ridiculously high fees?

## Replies

**musalbas** (2018-10-30):

IMO allowing market participants to collectively fix the price of a good or service is a bad idea, because it eliminates competition and incentives to be more efficient. Imagine if for example, airlines collectively vote that a flight from London to Paris must cost at least $X, because that’s their average price. If a challenger airline came along and discovers a new way to make flights much cheaper, then they wouldn’t be able to pass those savings to consumers, and there wouldn’t be as much pressure for those other airlines to be more efficient either, because they’ll still get customers and be profitable. The same applies with mining and transaction processing.

---

**nullchinchilla** (2018-10-30):

The problem is that the transaction fee “market” isn’t really a competitive market between validators. Validators can’t compete for transactions, and every transaction accepted by one validator is a burden on all validators. A more efficient-than-usual validator is unable to offer lower transaction fees to users unless *all* validators are more efficient, so the validator set already behaves like a cartel regardless of the way fees are set. In the old model, this just means that validators can’t ever charge fees high enough to cover their costs, and everybody loses money.

Also, currently the gas limit is already collectively decided, which punishes miners who discover efficient ways of processing huge blocks.

---

**nullchinchilla** (2018-11-02):

I’ve been thinking about this problem a bit more, and it seems like even in the existing system validators can informally fix the price of gas by voting down the gas limit until congestion occurs, or even by simply forming a 51% cartel that refuses to accept transactions with less gas than the fixed price or mine on top of / vote for blocks that include cheaper transactions. With enough incentive I don’t see any reason why this wouldn’t happen, as Ethereum miners already coordinate things like the gas limit fairly efficiently.

I am increasingly suspecting that in any system where validators earn most of their revenue through transaction fees and coordination costs between validators aren’t extremely high, miner cartels raising transaction fees is going to happen. Validator cartels probably have a lower social cost than a “tragedy of the commons” scenario where there isn’t enough demand for auction-based transaction fees to cover miner costs anyway, so perhaps a voted-on parameter deciding transaction fees might not be as bad as it sounds, as it gives a “legitimate” channel for monopoly pricing.

But again, the fact that [@vbuterin](/u/vbuterin) never mentioned it his [quite comprehensive paper](https://ethresear.ch/t/draft-position-paper-on-resource-pricing) on transaction fee pricing systems probably means it’s garbage. I’d really like a rigorous breakdown of *why* though.

