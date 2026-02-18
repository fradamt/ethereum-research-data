---
source: magicians
topic_id: 9054
title: Should the stake value of 32ETH be static?
author: rkapka
date: "2022-04-26"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/should-the-stake-value-of-32eth-be-static/9054
views: 1409
likes: 3
posts_count: 2
---

# Should the stake value of 32ETH be static?

On December 1st 2020, the launch date of the Beacon Chain, the price of 1ETH was $582.44. This means that becoming a solo validator cost $18638.08. Right now the price sits at $2,861.09, which requires $91,554.88 to participate in the proof of stake mechanism. What’s the point of making it possible to run the blockchain on consumer hardware when nobody will do it at home anyway because they will be a part of a validator pool? Of course you can still run a node altruistically, but I doubt there are many such cases. What if the price of ETH reaches $10,000? $50,000?

I would like to understand why keeping the value at 32ETH is a good idea for the system.

## Replies

**timbeiko** (2022-04-26):

The value is set based on how much overhead we can tolerate in the beacon chain. If the amount is lower, there are more cross-validator messages sent on the network. See [here](https://notes.ethereum.org/@vbuterin/serenity_design_rationale#Why-32-ETH-validator-sizes) for an explainer.

Agreed we should keep trying to lower it, and some research efforts, such as [Single Slot Finality](https://ethereum-magicians.org/t/discussion-thread-for-single-slot-finality/8917) might help here.

