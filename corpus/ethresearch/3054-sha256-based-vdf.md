---
source: ethresearch
topic_id: 3054
title: SHA256-based VDF
author: MihailoBjelic
date: "2018-08-22"
category: Sharding
tags: []
url: https://ethresear.ch/t/sha256-based-vdf/3054
views: 6222
likes: 5
posts_count: 11
---

# SHA256-based VDF

I’ve been exploring VDFs lately.

Noticed that Solana’s VDF is basically a recursive SHA256. A brief explanation of the model:

https://medium.com/solana-labs/proof-of-history-a-clock-for-blockchain-cf47a61a9274

The rationale is: " …thanks to Bitcoin there has been significant research in making this cryptographic hash function fast. This function is impossible to speed up by using a larger die area, like a Look Up Table, or unrolling it without impact to clock speed. Both Intel and AMD are releasing consumer chips that can do a full round of SHA256 in 1.75 cycles. Because of this, we have pretty good certainty that a custom ASIC will not be 100x faster, let alone 1000x, and most likey will be within 30% of what is available to the network. We can construct protocols that exploit this bound and only allow an attacker a very limited, easily detected and shortlived oportunity for a denial of service attack."

Any thoughts on this? Would it be worth considering for the Ethereum beacon chain? Thanks.

## Replies

**vbuterin** (2018-08-23):

How do they prove the result to clients that don’t have these magic chips built in?

Arithmetic is also something that there’s been huge research on speeding up, so I still think [MIMC+STARK](https://vitalik.ca/general/2018/07/21/starks_part_3.html) is better.

---

**JustinDrake** (2018-08-23):

Thanks for highlighting Solana ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) We do want to use a VDF for [Ethereum 2.0 randomness](https://docs.google.com/presentation/d/13OAGL42yzOvQUKvJJ0EBsAAne25yA7sv9RC8FfPhtyo/edit#slide=id.p). Verifying hash chains in parallel does not readily work for us (unless we use a [cryptoeconomic VDF](https://ethresear.ch/t/a-scheme-for-cryptoeconomic-vdfs-based-on-proto-vdfs/2741)) for a few reasons:

1. Low latency: Verification must be low latency to reduce the randomness lookahead and prevent DoS attacks.
2. Light clients: Verification of VDF outputs must be doable by light clients with limitted parallelism (e.g. an entry-level DigitalOcean instance).
3. Full nodes: Full nodes (including validators) should ideally not require “exotic” hardware such as GPUs for verification.

It is possible Solana could benefit from moving to [Sloth](https://eprint.iacr.org/2015/366.pdf) (or better, [Sloth++](https://eprint.iacr.org/2018/601.pdf)) instead of SHA256. My [favourite VDF](https://eprint.iacr.org/2018/623.pdf) is by Benjamin Wesolowski, specifically the instantiation in RSA groups. I am currently looking into the viability of building a commodity ASIC for it to minimise the speed advantage an attacker may get. Filecoin and Chia are two other projects looking into VDF ASICs.

---

**MihailoBjelic** (2018-08-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How do they prove the result to clients that don’t have these magic chips built in?

They state that the output can be verified in parallel on clients’ GPUs: “Each recorded slice can be verified from start to finish on separate cores in 1/(number of cores) time it took to generate. So a modern day GPU with 4000 cores can verify a second in 0.25 milliseconds.”

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Arithmetic is also something that there’s been huge research on speeding up, so I still think MIMC+STARK  is better.

You might be right. I generally love everything STARK-related. Thanks for the link, haven’t look into MIMC yet, but it was on my reading list already.

---

**aeyakovenko** (2018-08-23):

thanks for mentioning the project!  I am happy to answer any questions, please poke holes ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**aeyakovenko** (2018-08-23):

I guess we dont see GPUs all that exotic, since you can purchase them everywhere.  We are using GPUs for just about everything, ed255 ecdsa, and hopefully soon contract execution.  You get the cheapest cores per dollar on GPUs.

---

**JustinDrake** (2018-08-23):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/a/3bc359/48.png) aeyakovenko:

> we dont see GPUs all that exotic

My main concern is that GPUs exclude light clients, and cloud providers such as DigitalOcean.

**Edit**: It looks like DigitalOcean [will support GPUs](https://blog.digitalocean.com/2018-whats-shipping-next-on-digitalocean/) at some point.

---

**garious** (2018-08-23):

If no GPU handy and okay with longer startup and finality times, 2 or more CPU cores will suffice. Here’s the code: https://github.com/solana-labs/solana/blob/v0.7.2/src/ledger.rs#L421. Tests down below.

---

**aeyakovenko** (2018-08-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Light clients : Verification of VDF outputs must be doable by light clients with limitted parallelism (e.g. an entry-level DigitalOcean instance).

oof, you expect these digital ocean clients to be custodians of keys?

---

**MihailoBjelic** (2018-08-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Verifying hash chains in parallel does not readily work for us (unless we use a cryptoeconomic VDF) for a few reasons

Thanks for clarifying. IMHO, points 1 and 2 are valid, point 3 not so much (GPUs are more or less widely available).

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> It is possible Solana could benefit from moving to Sloth  (or better, Sloth++ ) instead of SHA256. My favourite VDF is by Benjamin Wesolowski, specifically the instantiation in RSA groups.

Thanks for the links, added to the reading list.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> I am currently looking into the viability of building a commodity ASIC for it to minimise the speed advantage an attacker may get. Filecoin and Chia are two other projects looking into VDF ASICs.

ASICs are my biggest concern regarding VDFs, and the main reason why I’m more inclined towards threshold cryptography when it comes to randomness. The plan to start the production of commodity VDF AISCs is really ambitious and challenging, and honestly I wonder if it’s realistic at all… I might be wrong, of course, hardware is not my thing after all…

---

**MihailoBjelic** (2018-08-23):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/a/3bc359/48.png) aeyakovenko:

> thanks for mentioning the project! I am happy to answer any questions, please poke holes

No problem, I’m glad to see you here. You guys are really experienced as far as I can see (especially with hardware/low level), and it seems to me like there’s a lot of substance to your project (which is not always the case with newer crypto projects ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12)). Having that in mind, I hope you will communicate and join efforts with [@JustinDrake](/u/justindrake) and others from Ethereum/Filecoin/Chia, I’m sure all projects will benefit.

