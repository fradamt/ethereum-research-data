---
source: magicians
topic_id: 2686
title: EIP to cap the ETH spend on gas in one TX
author: ligi
date: "2019-02-19"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/eip-to-cap-the-eth-spend-on-gas-in-one-tx/2686
views: 1022
likes: 3
posts_count: 11
---

# EIP to cap the ETH spend on gas in one TX

Inspired by:

https://github.com/ethereum/go-ethereum/issues/19134

what is the sentiment here about an EIP that limits the amount of ETH spend on gas for one TX?

## Replies

**AlexeyAkhunov** (2019-02-20):

I am very curious to read any suggestions on how such cap would be defined

---

**ligi** (2019-02-20):

perhaps something conservative like:

`if the gas price is more than 100x the maximum gas price from the last block`

---

**Amxx** (2019-02-20):

> Since it is a mistake done by the user, why Ethereum does not provide any payback/refund mechanism?

**Because Ethereum is not a centrally controlled bank.** It’s in Ethereum design (and I believe in everyone’s interest) that no central decision can revert a transaction. The miner can always decide to be nice and refund, but for the community to force him to refund would take a fork.

I believe that rather than questionning the protocol (Ethereum) you should consider questionning the wallet. What application sets the gas price to 0.1eth?

---

**ligi** (2019-02-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Because Ethereum is not a centrally controlled bank. It’s in Ethereum design (and I believe in everyone’s interest) that no central decision can revert a transaction. The miner can always decide to be nice and refund, but for the community to force him to refund would take a fork.

this is not really what is discussed here - I agree refund is not an option - was an idea of the user - and I agree this is not a good idea.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> I believe that rather than questionning the protocol (Ethereum) you should consider questionning the wallet. What application sets the gas price to 0.1eth?

I think it was not a wallet but a programming mistake. There where multiple transactions sending too much fee: https://www.reddit.com/r/ethereum/comments/as7ejb/reminder_be_careful_while_developing_someone_just

Also this account does not look like it was managed by a wallet - it looks like automatic actions.

So I think solving it on the protocol layer is a good option. Not by allowing reverts obviously - but by adding a cap to the ETH that can be spend for gas (as the title of this post).

I think this could improve the UX of Ethereum. This is not the first time this happened - and I think users of ethereum that stepped into this problem did not really like the experience ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**ligi** (2019-02-20):

PS: I think building on top of this EIP: https://github.com/ethereum/EIPs/issues/1559 would make thinks much easier.

So we do not need to care for the sliding window - we could just cap the premium

---

**AtLeastSignificant** (2019-02-20):

Build this into the clients, not the protocol…

---

**ligi** (2019-02-20):

I am not sure if a client was used in this case - might have just been a buggy script

---

**AtLeastSignificant** (2019-02-20):

I’ve seen at least speculation that this was an on-purpose attempt at some kind of ETH laundering.  Possible to not broadcast the transaction and just mine blocks yourself until you’re able to win one that includes it?

---

**xazax310** (2019-03-13):

What about having defined gwei rates? (Slower/Slow/Fast/Fastest) with each one costing a set amount of ethereum?

---

**AtLeastSignificant** (2019-03-25):

Something for clients to implement, not the protocol.

