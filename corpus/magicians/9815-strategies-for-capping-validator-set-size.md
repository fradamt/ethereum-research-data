---
source: magicians
topic_id: 9815
title: Strategies for capping validator set size
author: vbuterin
date: "2022-07-01"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/strategies-for-capping-validator-set-size/9815
views: 829
likes: 2
posts_count: 5
---

# Strategies for capping validator set size

Thread to talk about validator size capping strategies, including this doc:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/3/32f2c2579dd4c41c2ec5bf2227cb15da0bb80b26.png)

      [HackMD](https://notes.ethereum.org/@vbuterin/validator_set_size_capping)



    ![](https://ethereum-magicians.org/uploads/default/original/2X/6/6b9ddfd2b1913bf8d957f5433175f046d3da78dc.png)

###



This document is incorporated into https://notes.ethereum.org/@vbuterin/single_slot_finality










And any other ideas.

## Replies

**kladkogex** (2022-07-01):

An interesting idea is to require validators to maintain replacement price (if a new validator wants to join she would pay this price to the old validator)

Then validators would be taxed on the replacement price.

---

**vshvsh** (2022-07-03):

I think that the number of entities participating in Ethereum consensus is much, much lower than 400k (and much lower than 26 thousands, implied by the estimate of 15 validators/staker), and will be much lower for the foreseeable future. I would be very surprised if the actual number of entities operating consensus nodes of the beacon chain is over 2 or 3 thousand. The consensus algorithm, with some changes, can accommodate everyone who actually operates nodes hundreds of times over.

Thus, option 1 is entirely unnecessary. Making subcommittees from this amount isn’t needed. Option 2, in any shape, will lead to shifting out hobbyist validators, either through direct economic mechanisms or via indirect ones (e.g. just being better at timing validator entries/exists, or circumventing the native mechanism entirely to create a validator medallion market). If that’s not the desired effect, it should not be considered. I think that in general any change to a consensus protocol that makes operators’ time harder will result in professional operators dealing with it easily and unprofessional ones just finding a simpler hobby and moving on with their lives.

Option 3 is not defined very well (e.g. it’s not clear if consensus “power” and rewards are scaled with validator balance), but if there’s any solution here, it lies in scaling consensus participation power + rewards linearly with the stake of a validator. If the rewards are not scaled, small stakers will end up outpriced. If the power is not scaled, the change will result in lower security.

---

**kladkogex** (2022-07-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vshvsh/48/6493_2.png) vshvsh:

> I think that the number of entities participating in Ethereum consensus is much, much lower than 400k (and much lower than 26 thousands, implied by the estimate of 15 validators/staker), and will be much lower for the foreseeable future.

More than 50% is now controlled by three enities Coinbase, Binance and Lido

---

**vshvsh** (2022-07-07):

Lido is not one staking entity. There’s 28 node operators that validate chain under Lido’s umbrella.

