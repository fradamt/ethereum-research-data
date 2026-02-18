---
source: magicians
topic_id: 6302
title: How could this huge transaction be executed without paying any Gas?
author: hagen
date: "2021-05-23"
category: Magicians > Primordial Soup
tags: [gas]
url: https://ethereum-magicians.org/t/how-could-this-huge-transaction-be-executed-without-paying-any-gas/6302
views: 1516
likes: 1
posts_count: 2
---

# How could this huge transaction be executed without paying any Gas?

Hi ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Since I have seen this transaction (which was part of a $-25-Mio-Issue on a [DeFi project called xToken](https://thedefiant.io/xtoken-defi-project-hacked-for-over-25m/)) I am thinking about it: [0x7cc7d935d895980cdd905b2a134597fb91004b5d551d6db0fb265e3d9840da22](https://etherscan.io/tx/0x7cc7d935d895980cdd905b2a134597fb91004b5d551d6db0fb265e3d9840da22)

It contains a bunch of expensive transactions through the wide field of DeFi space, but costed itself not a single Wei of Gas. How could that be?

I have seen on Ethercan, that it is called a “private transaction”, which was “bypassing the mempool”.

What are the requirements to submit such an transaction and even to get it into the chain accepted by other miners? It seems to me that the folks behind this transaction were their own miners, but how could they get it broadcasted into the network without the power of a bigger pool? Or was this a coordinated effort by multiple participants across several mining pools?

Thank you in advance for any thoughts that may help me here in order to understand.

## Replies

**esaulpaugh** (2021-05-25):

All you have to do is set the gas price to zero and then mine the transaction or have it mined on your behalf.

