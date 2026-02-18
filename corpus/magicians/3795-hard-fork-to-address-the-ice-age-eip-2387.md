---
source: magicians
topic_id: 3795
title: Hard Fork to Address the Ice Age (EIP-2387)
author: MadeofTin
date: "2019-11-22"
category: EIPs > EIPs Meta
tags: []
url: https://ethereum-magicians.org/t/hard-fork-to-address-the-ice-age-eip-2387/3795
views: 6996
likes: 11
posts_count: 9
---

# Hard Fork to Address the Ice Age (EIP-2387)

This is the central discussion place for a proposal to have a Hard fork shortly after Istanbul to address the Ice.

The proposed EIP is to rewind the Ice Age 4 million blocks and include a commitment to address issues with the Ice Age during that time.

Ice Age Delay EIP: [EIP-2384 - Difficulty Bomb Delay by econoar · Pull Request #2384 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2384)

Hard-fork Meta: [Hard fork proposal to address the Ice age by MadeofTin · Pull Request #2387 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2387)

## Replies

**tjayrush** (2019-11-23):

Copy from Gitter:

Where does the number to delay the hard fork of 4,000,000 come from? My understanding of the reason for the bomb was to avoid a situation like in Bitcoin where ten people control when to fork. Here’s the scenario — all you’all decide (for whatever reason) that there should be no more changes forever. And whomever has the GitHub permissions to change the code are convinced as well. The rest of the community would then have no recourse. If you think this can’t happen–look at Bitcoin. Forcing ourselves to deliver a fork every so often, even if there are no substantive changes, forces the community to repeatedly come back into agreement…and it give whatever portion of the community that wants to a chance to fork off. A better way to remove the ‘pain’ of the ice age would be to better manage it and make sure it gets modeled better (so we know when it’s going to hit) and include it in forks as a regular course.

**Correction:** The 4,000,000 would be in addition to the 5,000,000 from previous forks (3,000,000 for Byzantium and an additional 2,000,000 for Constantinople). So the subtraction from the ‘real’ block number to the ‘fake’ block number would be 9,000,000. This will reset the fork ‘period’ to zero ((9069000 - 9000000 = 69000) % 100000) = 0

Another way to do this, which would be much more obvious would be to simply subtract the FORK_BLOCK_NUMBER from the ‘real’ block to arrive at ‘fake’ block number. This would reset the bomb to zero each time.

I think there’s a lot of confusion related to hash rate. The bomb, once it starts going off, totally dominates the difficulty calc.

The reason the bomb is going off earlier this time is because we only set it back to period 22 ((7280000 - 5000000) % 1000000) = 22, whereas in Byzantium we set it back to period 13 ((4370000 - 3000000)  % 100000) = 13. Our goal should be to set the period back to 0.

The difficulty calc comes in two parts, A and B. A is designed to offset any change in hash rate by responding oppositely with higher or lower difficulty. Part A tends to hover at 14 seconds.

Part B (the bomb) grows exponentially based only on the period it’s in, and the period is dependent only on block number. The bomb totally dominates once it starts showing up. The non-bomb component (A – i.e. hash rate/difficulty) hovers.

A much more likely explanation for why the bomb is happening earlier than expected is because 2^22 is a lot larger than 2^13, and N months after the Byzantium fork we were in period 13 + X, whereas now we are in period 22 + X. (Where X is the number of periods the chain advances in N months.)

If we choose bomb_reset_subtraction = ISTANBUL_FORK_BLOCK we would make the period == 0 and fully diffuse the bomb.

---

**shemnon** (2019-11-23):

Why block 9mm?  4mm past the current fake block number?

(1) we didn’t want to put the fake block in the future.  There was concern that some implementations may wind up using negative block numbers for calculations and was viewed as an unneeded risk.  So that’s why it’s not larger.

(2) we wanted to kick it down a long way.  This gives us the room for either the bomb to meet or see measurable progress on one of the goals that advocates have stated (which is to encourage us to move off of Proof of Work to Proof of Stake) or for us to have a less pressured discussion to remove the bomb entirely.  There are reasonable arguments on both sides of the “remove” debate and achieving consensus on removal would not happen inside of a week.  So that’s one reason it was as large as was reasonable.

As far as timeframe I estimate that gives us until Q2 or Q3 of 2021 before we can measure the impact again. The future of the difficulty bomb is something that we should have at least one panel discussion on at Devcon 6, and possibly EthCC and other large ethereum conferences (but those are IMHO the two tentpoles).  A 2-3mm block delay would put “the bomb is about to explode” pressure on such a panel as there is an outside chance we could measure the impact by then.  I don’t know if we can have a good discussion about the purpose of the bomb and whether or not it is filling that purpose when the mechanism is demanding action.

---

**tjayrush** (2019-11-23):

[![Difficulty%20Periods](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c062112045b08e14ec7b05b1325cad5d2811c653_2_690x402.jpeg)Difficulty%20Periods3406×1986 613 KB](https://ethereum-magicians.org/uploads/default/c062112045b08e14ec7b05b1325cad5d2811c653)

If you only subtract 4,000,000 from the current block number (9,000,000) you will make the ‘fake block’ 5,000,000 which would be period 50 – which is way, way past where the bomb is now. The thing that matters is the period. The goal should always be to reset the period to zero.

---

**veox** (2019-11-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> If you only subtract 4,000,000 from the current block number

[EIP-2384](https://eips.ethereum.org/EIPS/eip-2384) proposes to push it 4 million **from Constantinople** (highlights mine):

> Starting with ???_FORK_BLKNUM the client will calculate the difficulty based on a fake block number suggesting to the client that the difficulty bomb is adjusting 9 million blocks later than the Homestead fork, which is also 7 million blocks later than the Byzantium fork and 4 million blocks later than the Constantinople fork.

---

It’s also probably OT in this thread (for the hard-fork meta), and should go to [the one on the delay](https://ethereum-magicians.org/t/eip-2384-difficulty-bomb-delay/3793).

---

**tjayrush** (2019-11-24):

In this article, I argue that hash rate has nothing to do with why the bomb seems to be going off earlier this time than the last time. I argue that we didn’t set the `period` back far enough last time. I also argue that the only thing that really matters is the `bomb` part of the calc, and that the non-bomb part not only doesn’t affect the slowing blocks but that it actually helps the chain get back to faster blocks each time a bomblet explodes. Finally, I argue that if one always sets the `period` back to the same value (0), then the bomb would be perfectly predictable since it’s a function of `fake block` number only. It’s all explained here: https://medium.com/@tjayrush/its-not-that-difficult-33a428c3c2c3. I’d really appreciate discussion.

---

**axic** (2019-11-25):

I’ve asked this on Gitter, just copying here for reference: Why is there a need for a new hard fork name and not just stick the agreed naming scheme? i.e. make this part of Istanbul or Berlin.

These two reasons came up:

- For some reason news outlets already reported about Berlin and “what’s included in it” (despite the EIP-centric process)
- “Emergency” hard forks had two-word names (with the exception of Petersburg)

And [copying this from the PR](https://github.com/ethereum/EIPs/pull/2387#discussion_r349774488): Suggest “Muir Glacier” ([see here](https://en.wikipedia.org/wiki/Muir_Glacier)) which has retreated significantly. Or any other similar glacier ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**fulldecent** (2019-12-01):

As a matter of procedure, I argue that EIP-2387 should be remove from Last Call and without further consideration.

EIP-2387 depends on EIP-2384 with the latter being in Last Call status.

Because the EIP dependee is not in final status the EIP dependor should not be eligible for Last Call consideration.

That is all.

---

**fulldecent** (2019-12-01):

This recommendation is implemented at https://github.com/ethereum/EIPs/pull/2413

