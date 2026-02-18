---
source: magicians
topic_id: 5535
title: An opt-in off-chain protocol to pre-validate transactions
author: rubi
date: "2021-03-10"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/an-opt-in-off-chain-protocol-to-pre-validate-transactions/5535
views: 618
likes: 0
posts_count: 1
---

# An opt-in off-chain protocol to pre-validate transactions

This is just about wallets UX. Check-sums are nice, but at the end of the day, a lot of people “make a small transaction, just to see it’s working”, before making a really huge one. A lot can go somewhat wrong on the first transaction between two wallets (picking the wrong network, an unsophisticated malware changing the address on clipboard, copying the wrong address on the first place, etc.)

It could be nice if this is replaced by some off-chain protocol that publish the transaction as a notification on the other end, so the person(s) doing it can validate, before submitting.

I’m not getting into implementations details because it doesn’t matter. I’d love to hear community  opinion ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

Of course it’s optional, may be turned off by default.
