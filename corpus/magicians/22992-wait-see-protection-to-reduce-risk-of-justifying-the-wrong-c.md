---
source: magicians
topic_id: 22992
title: Wait & see protection to reduce risk of justifying the wrong chain
author: mxs
date: "2025-02-26"
category: Magicians > Primordial Soup
tags: [consensus-layer]
url: https://ethereum-magicians.org/t/wait-see-protection-to-reduce-risk-of-justifying-the-wrong-chain/22992
views: 156
likes: 4
posts_count: 1
---

# Wait & see protection to reduce risk of justifying the wrong chain

# Wait and see

*Thanks to [ralexstokes](https://ethereum-magicians.org/u/ralexstokes) & [ManuNLP](https://ethereum-magicians.org/u/ManuNLP/) for reviews & feedback.*

This post describes an approach to minimize the risk during Ethereum upgrades to avoid the Pectra/Holesky scenario where the wrong chain was justified due to a bug present in 3 implementations of execution clients.

It does not imply changes to the specs or the Ethereum protocol, but it requires all beacon nodes to play this game. A parallel to this approach would be the Doppelgänger protection, which isn’t bullet-proof but somewhat easy to implement and can save the day.

## Overview

At the transition moment of the fork, beacons enter a wait-and-see mode where they arbitrarily mute 40% of their validators: muted validators continue to propose blocks but do not attest. Knowing 40% of the network is not attesting, observe what the 60% voting ones are doing and act depending on it.

### Smooth upgrade

If the 60% agree on the same view, the beacon unmutes its validators and the chain finalizes. 40% of the validators lose 1 attestation during this process.

![Screenshot 2025-02-25 at 09.52.47](https://hackmd.io/_uploads/HypPr_i5yx.png)

### Upgrade with bugs

If the 60% don’t agree on the same chain, the beacon continues in muted mode for 40% of its validators and waits for manual clarification. In this mode, the validators won’t cast a vote for a source higher than the one of the fork, because they don’t see 2/3 of the network vote on something (40% is down). The two sides are stuck.

Network enters inactivity leak but there is time for client teams to investigate what is going on and provide a fix. Once the fix lands, the bogus clients are upgraded and agree on the same view.

![Screenshot 2025-02-25 at 10.25.04](https://hackmd.io/_uploads/rJeW6Osc1x.png)

They key point is that, as long as a consensus client doesn’t see 2/3 of the network voting on the same target, its source vote will stay at a stuck position. When the network upgrades in the right fork, it will be able to see a target with 2/3 and increase its source vote. There is no surrounding involved so no slashing.

![Screenshot 2025-02-25 at 10.02.11](https://hackmd.io/_uploads/ByGiP_ickg.png)

## Examples

Assuming a coordinated bug on 80% of the network (3/4), beacon knows 40% is randomly down, on the 60% up statistically it sees:

- 3/4 vote for 1 thing (~45% of the network), side A,
- 1/4 the other (~15% of the network), side B.

Bug is identifed on side A and fixed, everyone upgrades and moves to side B, beacons see 60% agree on the same target there, accept to vote on it as you see it the same, 2/3 is reached and the network continues.

## Downsides

- It only works during specific periods where a beacon “knows 40% of validators is randomly down”, it won’t prevent such bugs during normal operations,
- It costs some attestation misses (likely 1-2 or so if it everything goes fine, but it’s ridiculously small compared to the risks),
- An attacker not playing by the rules can lure the network into believing there is 60% agreement, this would defeat this protection: this is not a bullet-proof protection, and is more to prevent bug scenarios.
