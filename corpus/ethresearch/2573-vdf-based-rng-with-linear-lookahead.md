---
source: ethresearch
topic_id: 2573
title: VDF-based RNG with linear lookahead
author: JustinDrake
date: "2018-07-16"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/vdf-based-rng-with-linear-lookahead/2573
views: 5119
likes: 4
posts_count: 3
---

# VDF-based RNG with linear lookahead

**TLDR**: We present a VDF difficulty scheme that significantly reduces the RNG lookahead, i.e. the amount of time random numbers are made public before they are used.

**Context**

In [a previous post](https://ethresear.ch/t/verifiable-delay-functions-and-attacks/2365) Vitalik exposed a DoS attack on a naive VDF-based RNG where an attacker, assumed to have a hardware advantage up to A_{max}, can ramp up the VDF difficulty and then under-perform (e.g. by going offline). This would cause the randomness beacon to pause for an extended period of time, hence stalling the beacon chain and shards.

One way to address the DoS vector is to have a lookahead quadratic in A_{max}, as presented in Vitalik’s post. In this post we achieve a lookahead linear in A_{max} with a difficulty scheme strengthened against DoS attacks.

**Construction**

Notice that when an attacker ramps up the VDF difficulty versus the capabilities of honest players and then under-performs he is revealing two pieces of information:

1. an upper bound on the VDF speed of honest players
2. a lower bound on the VDF speed of the attacker

Let’s call the range between these two bounds the “DoS zone” and let:

- s_i be the fastest observed VDF speed in epoch i
- t_i be the target VDF speed (the difficulty) in epoch i
- s_{max} be the historically fastest observed VDF speed prior to epoch i

The difficulty adjustment works as follows:

- If s_i \le t_i then set t_{i+1} = \max\{s_i, s_{max}/A_{max}\}. That is, downward difficulty adjustments are maximally steep up to the safe minimum s_{max}/A_{max}.
- If s_i > t_i and s_{max} > t_i then set t_{i+1} = t_i * c where c is the smallest constant that safely accounts for organic improvements to VDF speeds. That is, upward difficulty adjustments in the DoS zone are slow.
- If s_i > t_i and s_{max} = t_i then set t_{i+1} = s_i. That is, upward difficulty adjustments outside the DoS zone are maximally steep.

**Discussion**

By setting the lookahead to be linear in A_{max} the attacker can do a large DoS attack, but only rarely. For example if the lookahead is set to the expected VDF computation time, A_{max}=10, and c is set to target a maximum of 2x VDF speedup in 1 year then DoS attacks only become viable once per few years.

## Replies

**djrtwo** (2018-07-16):

So the purpose of these difficulty adjustments is so after an attack, the difficulty can only grow at the organic c constant until we reach the previous attack difficulty, at which point the difficulty adjusts in lock step with s_i?

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> an upper bound on the VDF speed of honest players

We only get this piece of information on the round *after* the attacker has disappeared.

In the case where s_i \le t_i and max\{s_i, s_{max}/A_{max}\} == s_{max}/A_{max}, this scenario likely occurs when an attacker turns off their VDF, but honest players were not previously online/calculating for that round (thus the slow s_i). This is likely to happen due to the monopolistic nature of the VDF game especially in the case of a strong attacker. In this scenario we will see a longer than expected s_i while honest players fire up their VDF calculations.

Assuming a_max, what is the expected worst case that an attacker can stall the VDF calculation and thus the progression of the beacon chain?

Is it worth having a fallback to pure RANDAO in the case of the rare attack to keep the chain live?

---

**JustinDrake** (2018-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> So the purpose of these difficulty adjustments is so after an attack, the difficulty can only grow at the organic cc constant until we reach the previous attack difficulty, at which point the difficulty adjusts in lock step with s_i?

Right.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> We only get this piece of information on the round after the attacker has disappeared.

Right.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> In the case where s_i \le t_i and max\{s_i,s_{max}/A_{max}\}==s_{max}/A_{max}

In theory this scenario should not happen by definition of A_{max}. I included the s_{max}/A_{max} part as “security in depth” to cater for exceptional scenarios like the one you suggest.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> we will see a longer than expected s_i while honest players fire up their VDF calculations

Right, this is one possible exceptional scenario. I don’t think it’s likely to happen (even with a strong attacker) because it suffices for a single non-lazy honest player to operate a baseline-speed VDF backup. I expect the Foundation and other entities (including myself) to operate baseline-speed VDF backups.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Assuming A_{max}, what is the expected worst case that an attacker can stall the VDF calculation and thus the progression of the beacon chain?

There are three parameters that come into play. My best-guess conservative parameters are D = 1 minute (where D is the attacker’s largest reveal period), A_{max} = 10, and the lookahead equal to D * A_{max}. With this setup the worst case delay is D * A_{max} * A_{max} - 2 * D * A_{max} = 80 minutes.

With publicly-available VDF ASICs (we are considering having the Foundation sponsor the development of a VDF ASIC) I’m hoping we can bring A_{max} down to something like 5, where the worst case delay would be 15 minutes.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Is it worth having a fallback to pure RANDAO in the case of the rare attack to keep the chain live?

I don’t think it’s worth the added complexity (and the grinding vector) ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

