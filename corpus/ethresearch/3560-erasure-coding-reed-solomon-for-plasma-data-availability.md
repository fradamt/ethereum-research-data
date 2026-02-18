---
source: ethresearch
topic_id: 3560
title: Erasure coding (Reed-Solomon) for Plasma data availability
author: MihailoBjelic
date: "2018-09-26"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/erasure-coding-reed-solomon-for-plasma-data-availability/3560
views: 4124
likes: 11
posts_count: 11
---

# Erasure coding (Reed-Solomon) for Plasma data availability

I’m writing this posts for two reasons:

1. I feel like erasure coding is not discussed enough as a data availability solution for Plasma implementations
2. Yesterday, @vbuterin and @musalbas published a paper which proposes an interesting data availability scheme based on Reed-Solomon erasure coding. Their blockchain model uses SMTs (the state is represented as a key-value map), so it can support both UTXO and account-based chains.

I know erasure coding gives probabilistic data availability guarantees, but those can be **really** high, as shown in the section 5.6 of the paper. Why Plasma folks are not considering this more often? Is it hard to implement? Something else?

Two main challenges of Plasma are ensuring correct transaction execution (preventing incorrect/malicious transactions) and ensuring data availability. It seems like SNARKs/STARKs should take care of the former in future, and erasure coding might be an elegant solution for the later (most implementations currently require users to download whole chains, which is quite a burden)?

Hope this can start a constructive discussion.

https://arxiv.org/pdf/1809.09044.pdf

## Replies

**vbuterin** (2018-09-26):

So basically a Plasma MVP architecture where clients use erasure coding-based data availability sampling in place of downloading the full data?

Sounds very reasonable to me!

---

**MihailoBjelic** (2018-09-26):

Exactly. I guess it could also be used for never, EVM-like Plasma proposals, like [Plasma Snapp](https://ethresear.ch/t/plasma-snapp-fully-verified-plasma-chain/3391), [Quark-gluon Plasma](https://ethresear.ch/t/quark-gluon-plasma-verified-plasma-chain-without-confirmation-signatures/3453) and [Plasma EVM 2.0](https://ethresear.ch/t/plasma-evm-2-0-state-enforceable-construction/3025) (they even had to make changes to their original design because it couldn’t guarantee data availability). Basically, in any implementation which so far required users to download the whole chain…

---

**shamatar** (2018-09-26):

SPV is always on a table in Plasma implementers discussion, it’s a very important part of the UX, although the “data availability” problem should be separated and clarified:

- Block withholding - in this case a Plasma operator (or a set of operators) commits to the new state or a new block header on-chain, but never publishes a block in full. So it’s never available in the network, even if every relaying node is honest
- Dishonest full nodes - in this case a paper linked above helps to propagate a valid (and fully available somewhere) data to as many participants as possible and give proper guarantees for SPV

---

**MihailoBjelic** (2018-09-27):

Thanks for the comment, [@shamatar](/u/shamatar).

![](https://ethresear.ch/user_avatar/ethresear.ch/shamatar/48/670_2.png) shamatar:

> SPV is always on a table in Plasma implementers discussion

I’m aware SPV is being mentioned quite often, but I haven’t heard erasure-coding being discussed (I haven’t listen all the implementers calls yet, though).

![](https://ethresear.ch/user_avatar/ethresear.ch/shamatar/48/670_2.png) shamatar:

> the “data availability” problem should be separated and clarified

I think erasure coding could help in both cases you described. We can have two erasure coding-based sampling processes happening simultaneously - one that is checking only the last few blocks, and the other checking the whole chain. Somebody can correct me if I’m wrong, but I believe this way the light Plasma clients can have a really high guarantees that all the data is constantly available, without ever having to download a single block! Now we can imagine Raspberry Pi and IoT devices as light Plasma clients.

---

**MaxC** (2018-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I think erasure coding could help in both cases. We can have two erasure coding-based sampling happening simultaneously - one that is checking only the last few blocks, and the other checking the whole chain. Somebody can correct me if I’m wrong, but I believe this way the light Plasma clients can have a really high guarantees that all the data is constantly available, without ever having to download a single block!  Now we can imagine Raspberry Pi and IoT devices as light Plasma clients.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> might

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I think erasure coding could help in both cases you described. We can have two erasure coding-based sampling processes happening simultaneously - one that is checking only the last few blocks, and the other checking the whole chain. Somebody can correct me if I’m wrong, but I believe this way the light Plasma clients can have a really high guarantees that all the data is constantly available, without ever having to download a single block!  Now we can imagine Raspberry Pi and IoT devices as light Plasma clients.

Say the whole blockchain is a gigabyte. You’d need enough clients querying the erasure code for the whole block-chain. If you updated the erasure code every day, you’d have to  have the clients sample gigabytes worth of data every day.  Not sure how feasible that is.

---

**gloine** (2018-09-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I think erasure coding could help in both cases you described.

Hi Mihailo,

I am not sure how erasure coding can help block withholding case. If the block had never been available on the network (intentionally), how could we sample from the data?

Thanks,

Jaehyung

---

**MihailoBjelic** (2018-09-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> You’d need enough clients querying the erasure code for the whole block-chain.

I didn’t really get this, please expand?

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> If you updated the erasure code every day, you’d have to have the clients sample gigabytes worth of data every day. Not sure how feasible that is.

In the worst case, sampling of the whole chain can been done only as a part of the first boot-up (sync) of a light client. Then we can increase the frequency from that, depending on the resources each client is willing/able to invest. Speaking of that, I don’t really know how resource(bandwidth/CPU/memory)-intensive this sampling is? If you have any knowledge/experience/data on this, can you please share? Thanks!

![](https://ethresear.ch/user_avatar/ethresear.ch/gloine/48/1830_2.png) gloine:

> If the block had never been available on the network (intentionally), how could we sample from the data?

We can not, that’s exactly how we’ll see the data is missing (or I am the one missing something)?

---

**gloine** (2018-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> We can not, that’s exactly how we’ll see the data is missing (or I am the one missing something  )?

Then is the following claim true? Erasure coding cannot resolve data availability issues caused by block withholding (but may resolve issues from dishonest full nodes).

---

**MihailoBjelic** (2018-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/gloine/48/1830_2.png) gloine:

> Erasure coding cannot resolve data availability issues caused by block withholding (but may resolve issues from dishonest full nodes).

As I’ve said, my understanding is that it help in both cases, and I’we explained why (if you do the sampling and you can’t fetch some data, you know that data is unavailable?). It would be great if someone who is experienced with erasure coding could weigh in on this.

---

**MaxC** (2018-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> In the worst case, sampling of the whole chain can been done only as a part of the first boot-up (sync) of a light client. Then we can increase the frequency from that, depending on the resources each client is willing/able to invest. Speaking of that, I don’t really know how resource(bandwidth/CPU/memory)-intensive this sampling is? If you have any knowledge/experience/data on this, can you please share? Thanks!
>
>
>  gloine:

If the person who created the block could not

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> If you updated the erasure code every day, you’d have to have the clients sample gigabytes worth of data every day. Not sure how feasible that is.

The creator of the erasure code could respond to requests on the network for pieces of the erasure code, making it seem that more data is available than the sampling scheme would suggest. Eg You sampled 3 pieces and the block creator returns the 3 pieces, but the rest of the block is unavailable.

The two ways to circumvent this would be (1) to ensure that the operator cannot respond to requests for pieces of the erasure code- difficult if the operator has a lot of sybil identities on the network; (2) have enough light clients sampling that something like half the erasure code is sampled by the light clients. Even then you run into the issue that some light clients can be fooled into accepting a block as available when it is not - and you have to  add some extra privacy features.  It’s all detailed here: [A note on data availability and erasure coding · ethereum/research Wiki · GitHub](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding)

