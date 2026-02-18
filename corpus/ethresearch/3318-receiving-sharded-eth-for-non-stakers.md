---
source: ethresearch
topic_id: 3318
title: Receiving sharded ETH for non stakers
author: schone
date: "2018-09-11"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/receiving-sharded-eth-for-non-stakers/3318
views: 1063
likes: 0
posts_count: 4
---

# Receiving sharded ETH for non stakers

I read that initially the transition from the “old” (ETH 1.0) mainchain, will include a one way contract that burns ETH and credits a staker with Beacon-ETH which will trickle subsequently to a block on a shard crediting you the amount.

What happens to accounts who don’t hold enough ETH to stake, how will their ETH find it’s way to the sharded blocks? And on what time scale and operational procedure?

## Replies

**djrtwo** (2018-09-12):

There will be a system level contract that allows for validator registration to the beacon chain. After the validator logs out, the ETH can be withdrawn to the shard chains. This will not be a bi-directional transfer (at least until the existing EVM chain is rolled into the eth2.0 landscape somehow).

As for non-staked ETH that wants to move into the eth2.0 landscape, we can similarly construct another eth1.0 system level contract that allows for a directional deposit into eth2.0. The mechanism would be similar but would be destined for a shard chain instead of for validation.

This is not currently spec’d, but can and probably should be specified as an EIP sometime after the initial beacon chain launch.

---

**schone** (2018-09-12):

Do I understand the vision correctly thinking that once sharding is complete there will be no POW mainchain anymore? The beacon chain will be the main chain.

---

**djrtwo** (2018-09-12):

Yes, the intention is to eventually roll the EVM chain in as a PoS shard or a contract on a shard. This is will only happen once the rest of the eth2.0 sharding protocol is built out and stable.

