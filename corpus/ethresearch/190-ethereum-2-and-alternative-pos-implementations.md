---
source: ethresearch
topic_id: 190
title: Ethereum 2 and alternative POS implementations
author: Lars
date: "2017-11-03"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/ethereum-2-and-alternative-pos-implementations/190
views: 2543
likes: 2
posts_count: 8
---

# Ethereum 2 and alternative POS implementations

Now that the plans for Ethereum 2 has been announced, would that make it possible to experiment with both Vitalik’s and Vlad’s implementation?

## Replies

**jamesray1** (2017-11-13):

Reading Ethereum 2 makes me confused. Do you have a reference for the announcement? What do you mean by “Vitalik’s and Vlad’s implementation”? Please be more specific and give references, otherwise it’s hard to understand where you are coming from and what you are asking. I was under the impression that Ethereum 1.0 and 2.0 were used initially, but was later replaced with Frontier, Homestead, Metropolis (and consequently the sub-phases of Byzantium and Constantinople) and Serenity.

---

**Lars** (2017-11-14):

Ethereum 2 was announced on the first day of Devcon3 by Vitalik. It is a plan on how to manage conflict between need for frequent hardforks and the high costs and risks with hardforks.

In short, if I understood it correctly, it is by using something similar to sidechains. It will be possible to create these without having to hardfork the main chain every time. Please see vide clip from DevCon3 for more details. I am not sure if there is a specific clip for this yet, otherwise you will find it as the last presentation on the first day.

---

**yhirai** (2017-11-14):

You can watch the announcement here: https://www.youtube.com/watch?v=Yo9o5nDTAAQ&feature=youtu.be&t=7h55m35s

---

**jamesray1** (2017-11-15):

OK I will watch it. I had going through DEVCON on the to do list but I thought that focusing on Serenity was more important, but I will at least skim through to find parts that look most important for development of the core protocol. My understanding according to comments from Vlad on Twitter was that side channels weren’t worth it compared to sharding.

---

**Lars** (2017-11-15):

The Ethereum 2 design will allow sharding be developed in parallel, before the POS.

---

**jamesray1** (2017-11-15):

OK I just watched the talk. The talk highlighted that there are lots of good ideas being developed, and the validator manager contract on a sidechain of N shards looks like it’s well worth further development, as well as other future developments such as tight coupling (which I remember was originally presented earlier on sharding). The need to have deep changes is indeed critical for not only for rapid research and development, but also for quickly fixing vulnerabilities that are detected on operating software, as there have been the need to make such changes urgently in the event of vulnerabilities (e.g. DAO and [Parity multisig wallets in July and this month](https://paritytech.io/blog/security-is-a-process-a-postmortem-on-the-parity-multi-sig-library-self-destruct.html)).

---

**AFDudley** (2017-12-26):

Yes. That’s what’s happening now:

Vitalik’s https://github.com/ethereum/casper

Vlad’s https://github.com/ethereum/cbc-casper

