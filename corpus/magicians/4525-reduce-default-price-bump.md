---
source: magicians
topic_id: 4525
title: Reduce default price bump
author: yahgwai
date: "2020-08-20"
category: EIPs
tags: [gas]
url: https://ethereum-magicians.org/t/reduce-default-price-bump/4525
views: 736
likes: 1
posts_count: 1
---

# Reduce default price bump

An ethereum transaction can be replaced on the network as long as the gas price is increased by at least a minimum amount: the pricebump. This minimum amount stops client endlessly replacing transactions, and causing extra work for nodes, without significantly increasing the price they pay to do so.

Recently gas prices have increased dramatically, such that the minimum amount accounts to a significant absolute value. This is a proposal to reduce the default setting for this minimum amount from ~10% to ~1% to allow more price bumping.

### Current default settings in major clients

- Open Ethereum 12.5%
- Geth 10% (see --txpool.pricebump)
- Nethermind - ? - couldnt find it

### Rationale

Currently users and applications estimate gas prices by using common estimators such as EthGasStation. They often choose high gas prices as volatility in the gas price market can mean that a lower price can have a high variance on mining time - if the market is moving upwards a transaction estimated to take 5 minutes can end up taking hours, or be dropped completely.

One solution to this is to replace the transaction on the network by bumping the price, however the current minimum settings can often cause an individual bump to overshoot and overpay the market price. Having a more fine grained control over the price bump can allow the users to more closely track the market price without risking overpaying by so large an amount.

Another positive effect of this method is that by always starting below the network price and slowly bidding up a downward pressure is placed on the gas price market, lowering gas prices for all participants.

### Downsides

Lowering this threshold value could lead to a lot more replacements on the network. Front runners and arbitrageurs would benefit from having more fine grained control which could place a heavier burden on the network.
