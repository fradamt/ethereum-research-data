---
source: ethresearch
topic_id: 595
title: Telegram Sharding
author: kladkogex
date: "2018-01-12"
category: Sharding
tags: []
url: https://ethresear.ch/t/telegram-sharding/595
views: 7917
likes: 16
posts_count: 20
---

# Telegram Sharding

Below is a link to Telegram whitepaper …

Does anyone understand how is this supposed to work ?)) They claim it to be infinitely fast and infinitely good ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=9)

https://drive.google.com/file/d/1ucUeKg_NiR8RxNAonb8Q55jZha03WC0O/view

Some quotations:

Because taking cryptocurrencies mainstream in 2018 would not be possible using the

existing blockchain platforms,4 Telegram co-founder Dr. Nikolai Durov set out to find

a novel solution to meet the speed and scalability required for mass adoption.

At the core of the platform is the TON Blockchain — a scalable and flexible blockchain architecture  that consists of a master chain and up to 2^92 accompanying blockchains.

TON blockchains can  automatically split and merge to accommodate changes in load. This means that new blocks are always generated quickly and the absence of long queues helps keep transaction costs low, even if some of the services using the platform become massively popular.

TON blockchains use smart routing mechanisms to ensure that transactions between any two blockchains will always be processed swiftly, regardless of the size of the system. The time needed to pass information between TON blockchains grows logarithmically with their number, so scaling to even millions of chains will allow them all to communicate at top speed.

TON can «grow» new valid blocks on top of any blocks that were proven to be incorrect to

avoid unnecessary forks. This self-healing mechanism saves resources and guarantees that valid transactions will not be discarded due to unrelated errors.

TON uses a Proof-of-Stake approach in which processing nodes («validators») deposit stakes to guarantee their dependability and reach consensus through a variant of the Byzantine Fault Tolerant protocol. This allows TON to focus the computing power of its nodes on handling transactions and smart contracts, further increasing speed and efficiency.

## Replies

**rumkin** (2018-01-13):

Centralised systems has no such problem with sharding. So they just will use telegram servers ![:laughing:](https://ethresear.ch/images/emoji/facebook_messenger/laughing.png?v=9)

---

**kladkogex** (2018-01-13):

2^92 is one shard per gram of the Planet Earth …  Nowhere to hide! Someone needs to stop Dr. Nikolai Durov! ![:clown_face:](https://ethresear.ch/images/emoji/facebook_messenger/clown_face.png?v=9)

---

**ltfschoen** (2018-01-13):

The leaked link you shared is their “TON Primer”, which it says in fineprint on page 3 is just a “General Overview” of the proposed technology and its uses.

It mentions in the fineprint that there is another document called the “TON Technical Whitepaper”, which compares  blockchains and describes in detail the “TON Protocol” and other Components such as the “TON Blockchain” and the “TON Infinite Sharding Paradigm”.

Has the “TON Technical Whitepaper” also been leaked? If so, where may we obtain a copy of it to help us understand how it works?

---

**kladkogex** (2018-01-13):

I do not know - I only found the primer - if you find the whitepaper please post …

---

**ltfschoen** (2018-01-13):

According to this Bitcoin Magazine article the “TON Technical Whitepaper” is 132 pages in length: https://bitcoinmagazine.com/articles/telegrams-privacy-focused-user-base-could-be-ton-blockchains-killer-app/

---

**smartass111** (2018-01-17):

Guys, here is the 132 TON techical whitepaper, if someone missed


      [dropbox.com](https://www.dropbox.com/s/dul8l7wxsygritr/TON.pdf?dl=0)


    https://www.dropbox.com/s/dul8l7wxsygritr/TON.pdf?dl=0

###








cheers

---

**djrtwo** (2018-01-18):

The font is big and the margins are huge, but damn! Might this be the longest blockchain whitepaper to date?

Holler if anyone finds anything of note in this stack of pages…

---

**kladkogex** (2018-01-18):

The paper kind of shows that  the incredible Mr. Durov never took an undergraduate course in cryptography

For example, what is this hillarius statement supposed to mean ?)

[![Screenshot from 2018-01-18 19-16-31](https://ethresear.ch/uploads/default/optimized/1X/f8c3338ce8b338c01311ce733a40df5602493449_2_690x280.png)Screenshot from 2018-01-18 19-16-311131×459 142 KB](https://ethresear.ch/uploads/default/f8c3338ce8b338c01311ce733a40df5602493449)

[![Screenshot from 2018-01-18 19-24-19](https://ethresear.ch/uploads/default/optimized/1X/cf59c75950ecc83e425310f7ae622b59b988a1bd_2_690x401.jpg)Screenshot from 2018-01-18 19-24-191123×654 205 KB](https://ethresear.ch/uploads/default/cf59c75950ecc83e425310f7ae622b59b988a1bd)

Mr. Durov needs to read  about birthday paradox, his formulas make no sense, and also why so much obsession about numbers ?)) Why 10^{-18} ?  May because it is a billion of  billions and Mr. Durov thinks it is a really really big number ?))

> Fixing an incorrectblock generates “ripples” that are ultimately propagated towards the recent blocks of all affected shardchains; these changes are reflected in new“vertical” masterchain blocks as well

Seem to be lots of ripples - this essentially breaks all existing mathematical proofs of bllockchain security so it is a totally unchartered territory ruled by the genius of Mr. Durov ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

> Most systems would achieve this by “rolling back” to the last block before the invalid one in this shard chain and the last blocks unaffected by messages propagated from the invalid block in each of the other shard chains, and creating a new fork from these blocks. This approach has the disadvantage that a large number of otherwise correct and committed transactions are suddenly rolled back, and it is unclear whether they will be included later at all

Which “most systems”?  Who would design a crazy system that “suddenly rolls back” committed transactions?))

> TVM offers support for bit strings and byte strings

If it supports bit strings isnt it automatically supposed to support byte strings, because a byte string is also a bit string ?)))

> Once a validator obtains enough chunks to reconstruct the block candidate from them, it signs a confirmation receipt and propagates it through its neighbors to the whole of the group. Then its neighbors stop sending new chunks to it, but may continue to send the(original) signatures of these chunks, believing that this node can generate the subsequent chunks by applying the Reed–Solomon or fountain code by itself(having all data necessary), combine them with signatures, and propagate to its neighbors that are not yet ready

This is like the worst BFT  protocol ever created )  How can neighbors “believe”  in something - are they some kind of live creatures ? Or Mr Durov wants to put a human on each node ?))

How can neighbors know which other neighbors are ready and which are not ready? And then ready for what ?) He never explains what should they be ready for.

---

**ldct** (2018-01-22):

2.2.9 (with the caveats after) looks perfectly fine to me - what’s wrong with it?

---

**kladkogex** (2018-01-23):

I can not say whats wrong about it  since I dont understand it,  the entire paper is written in a random random style  ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) And since I am a really nice kind guy and usually try hard to understand things, I can conclude that the paper is badly written, and, therefore, the author is  mediocre, since talented people write good papers ) And then since he is a mediocre guy,  the entire statement Telegram makes about superiority of their things is really a sick, sick thing.

When people really invent something new, they are usually able to explain this in simple, clear terms. Einstein’s  thesis was just two pages, he got a Nobel Prize for it ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**kladkogex** (2018-02-21):

More on Telegram Tech

[telegram tech](https://tokeneconomy.co/a-ton-of-crap-b1e264c36802)

---

**kladkogex** (2018-03-05):

[and more](https://www.forbes.com/sites/jasonbloomberg/2018/02/17/telegram-ico-scam-among-cryptocurrency-scams/#6b0a641b1cf0)

---

**Futurizt** (2018-03-24):

Those are not technical comments by any means. It would be interesting to actually know what community thinks about the proposed solution (or lack of )…

---

**dpyro** (2018-04-07):

`s = {0...255}`. The entire thing falls apart when you realize its a hash function on a *single* byte. It’s almost guaranteed there will be at least one collision when you map a single byte to single byte (check out the Birthday Paradox if this doesn’t make sense to you).

I think the author says you can fix that by extending the output of the hash function to be `k`-bits long to produce a collision chance of `2^-k`. At that point you might as well make the hash function `f(x) -> x` since its operating on a single byte and produces a *larger* output than input in a deterministic fashion. (8) is not a useful conclusion because it doesn’t ask for the probability that `Hash(s)` will clash with `Hash(s')` but if it will clash with just one certain `Hash(s')`.

---

**ldct** (2018-04-07):

The domain of the function HASH in that picture is Bytes*, not Bytes

---

**zhuvikin** (2018-06-26):

As far as I can see there is a proposal to use trustless payment channels. The idea is to create “money pools” and let users to make transactions without use of blockchain every time.

[![Note](https://ethresear.ch/uploads/default/optimized/2X/d/d235b5f6d5e9584841e334619e25687adbe904ad_2_647x500.png)Note929×717 113 KB](https://ethresear.ch/uploads/default/d235b5f6d5e9584841e334619e25687adbe904ad)

---

**zhuvikin** (2018-06-26):

Seems this is the way to speed up payments processing in addition to multi-blockchain technique

---

**kladkogex** (2018-06-26):

“This is usually achieved with the aid of signatures”

Hilarious to see these  guys raising billions of dollars  on something they do not have a slightest spec for ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**daniejjimenez** (2019-05-29):

I do not understand how there can be a project like this with so many ‘loopholes’ … more recent projects like FLETA Blockchain have already achieved with sharding parallel and multichains to solve the scalability with 15k TPS

