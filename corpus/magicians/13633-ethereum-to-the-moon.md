---
source: magicians
topic_id: 13633
title: Ethereum to the Moon!
author: Pandapip1
date: "2023-04-01"
category: EIPs > EIPs core
tags: [correctly-tagged, no-reason-not-to-do, really-good-proposal]
url: https://ethereum-magicians.org/t/ethereum-to-the-moon/13633
views: 2194
likes: 8
posts_count: 15
---

# Ethereum to the Moon!

Edit,  since this was hidden by community flags: this is a valid EIP and I am actively pursuing it. This is not off-topic (despite the punny name)! Thank you for your understanding.

It is impossible for Ethereum to literally “go to the moon” due to a limitation in the protocol: the block length. Should validators attempt to validate on the surface of the moon, they would find that the ~1.25 second communication delay (caused by the speed of light) is might cause issues with synchronization, considering the 12-second timer between blocks. The validators would find themselves slashed on the terrestrial chain, and validating their own fork.

## Replies

**xtools-at** (2023-04-01):

happy april fools’ day ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12) the problem would be even graver for EVM-compatible chains with shorter blocktimes, 2s is quite common ![:grimacing:](https://ethereum-magicians.org/images/emoji/twitter/grimacing.png?v=12)

does speed of light really require 1.25s to get from earth to the moon though, sounds a bit too much ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12) too lazy to do the maths though ![:stuck_out_tongue_winking_eye:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue_winking_eye.png?v=12)

---

**JamesB** (2023-04-03):

Bitcoin wouldn’t have any problem with that block length ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=12) just need to add an EVM to it so it’s a bit more useful …

---

**xtools-at** (2023-04-04):

bitcoin cash (of all things ![:roll_eyes:](https://ethereum-magicians.org/images/emoji/twitter/roll_eyes.png?v=12)) has a EVM-compatible L2, would have loved that for BTC too

---

**Pandapip1** (2023-04-04):

Yes, it does, meaning that it takes ~2.5s for a round trip.

The distance is $384400 km=384400000 m$, and the speed of light is $299792458 \frac{m}{s}$, so the time is: $\frac{384400000 m}{299792458 \frac{m}{s}}=1.2822203819 s$

---

**Pandapip1** (2023-04-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamesb/48/6370_2.png) JamesB:

> Bitcoin wouldn’t have any problem with that block length  just need to add an EVM to it so it’s a bit more useful …

Bitcoin already has a long block length.

---

**Pandapip1** (2023-04-04):

It’s worth noting that this is both a “joke” proposal and one I’m legitimately interested in pursuing. I feel like there are many good reasons to increase the block length.

---

**5cent-AI** (2023-04-04):

I think quantum communication can solve this problem ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

---

**Pandapip1** (2023-04-04):

Nope, it can’t! You can’t communicate faster than the speed of causality, not even with entangled particles!



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Superluminal_communication)





###

Superluminal communication is a hypothetical process in which information is conveyed at faster-than-light speeds. The current scientific consensus is that faster-than-light communication is not possible, and to date it has not been achieved in any experiment.
 Superluminal communication other than possibly through wormholes is likely impossible because, in a Lorentz-invariant theory, it could be used to transmit information into the past. This complicates causality, but no theoretical arguments...

---

**5cent-AI** (2023-04-04):

How about we try to build layer2 on the moon?

---

**5cent-AI** (2023-04-04):

If we achieve interstellar travel, the communication delay will become longer. Increasing the block length cannot completely solve the latency problem.

---

**JamesB** (2023-04-05):

Yeah, exactly ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) wouldn’t be any issues blocklength-wise adding a 3s round trip - unless that extended round trip + the inevitable modem comms ping interferes with the client initialisation/sync. Wonder what timezone the moonbase would be using? UTC? That’s a whole other source of pain for future devs!

---

**imkharn** (2023-04-08):

Lets scale up the problem to its theoretical limits:

Suppose an infinite plane with evenly distributed nodes spaced 1km apart. Design a consensus mechanism that allows multiple light cone consensus silos to communicate.

The best part is that humanity will for sure face a similar problem some day (assuming no extinction, and causality is limited by C)

---

**alijasin** (2023-04-12):

I must admit that I was one of the persons who submitted a report to this post. Did not think this was a half-way serious issue and I apologize.

Would it make sense to name the EIP to something like “Ethereum to the Moon and Back!” to indicate that it is not just a meme, but also that it relates to the round trip time?

---

**Pandapip1** (2023-04-18):

I’ll consider it. Also, don’t worry about the report. No harm, no foul.

