---
source: ethresearch
topic_id: 11379
title: Constructions for a private collective treasury?
author: bgits
date: "2021-11-30"
category: Privacy
tags: []
url: https://ethresear.ch/t/constructions-for-a-private-collective-treasury/11379
views: 2430
likes: 3
posts_count: 3
---

# Constructions for a private collective treasury?

[Constitution DAO](https://www.constitutiondao.com/) has gathered some mindshare around a collective that came together to try and bid on a copy of the U.S. Constitution. One of the flaws was that the treasury value of the DAO was entirely transparent and that would allow any other bidder to know the max bid of the DAO and outbid them.

What type of construction would allow such a DAO to maintain a private treasury and participate in an auction?

## Replies

**SebastianElvis** (2021-11-30):

This is a really promising research direction, yet challenging. The straightforward way of hiding the balance of a smart contract account may not work, as the balance of an account is always known on the blockchain.

An alternative is to make the treasury non-custodial: everyone locks its donated coins in his own account while telling the manager the amount, and the donated coins are transferred to the treasury account only when certain events are triggered (e.g., the bid is successful). The technical challenges include 1) how to hide the amount of donated coins on-chain, 2) how can the manager verify the amount claimed by the donators, and 3) how to trigger the events.

---

**Cais** (2021-12-01):

hah – impeccable timing as it almost feels like a planted question given we’ve been seeking a review of our [whitepaper](https://ethresear.ch/t/introducing-obscuro-a-new-decentralised-layer-2-rollup-protocol-with-data-confidentiality/11353). Luckily, [@bgits](/u/bgits), you’ve been around these forums for a while, so definitely not a planted question! ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=10)

This is an approach Constitution DAO could have taken using Obscuro:

Create a contract that holds the funds on Obscuro, inflows/outflows, and the total balance would be known to nobody, all hidden away in encrypted rollups on Ethereum and inside secure TEEs.

Users would commit funds into the contract using encrypted transactions, indistinguishable from other transactions happening on the network.

The contract would have a function; let’s call it “doYouBid()”; which the auction house (or the party executing the auction) would need to be explicitly authorised at the outset to call using their key only in a predefined interval.

During the auction, the auctioneer would call this function at every step, passing in the next bid amount, e.g. doYouBid(13,000,000), doYouBid(14,000,000), etc. The function would only ever respond yes to the limit of its available funds (or some preconfigured limit that is also hidden).

After the auction, the auction house can claim the funds from the contract.

The other bidders cannot know the maximum amount locked in the DAO and thus have no advantage.

