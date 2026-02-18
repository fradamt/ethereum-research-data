---
source: magicians
topic_id: 2469
title: Random critique of EIP-706 (DEVp2p snappy compression)
author: veox
date: "2019-01-18"
category: Magicians > Primordial Soup
tags: [eip, devp2p, compression, eip-706, snappy]
url: https://ethereum-magicians.org/t/random-critique-of-eip-706-devp2p-snappy-compression/2469
views: 1001
likes: 1
posts_count: 3
---

# Random critique of EIP-706 (DEVp2p snappy compression)

Here’s what I’m *guessing* digging into [EIP-706](https://eips.ethereum.org/EIPS/eip-706), mostly after a few days playing with `trinity`.

It was introduced as a means to reduce network load on “full nodes”. No consideration was given to CPU/RAM, because that wasn’t the dire issue to be solved; and it tried to be simple.

It applies compression wholesale, to all messages past DEVp2p’s `Hello`, including to all sub-protocols past DEVp2p, - e.g., when doing sync, peer exchange, or other fully-validating node communication. This produces (substantial) net savings through compressing bulk data. The overhead for `Ping`, `Pong`, and `Disconnect` was not considered, likely because it’s minuscule in comparison to “bulk data” benefits; probably also due to reviewers’ time constraints.

There is no negotiation of compression; it is applied strictly according to advertised DEVp2p version. Consequently, there is no provision to turn compression off. This was not considered, because there were no sub-protocols in widespread use that would be harmed by compression.

---

To address this (general) ungracefulness, I’ve started pondering (vaguely) of opening an EIP, proposing a version 6 of DEVp2p, where compression (or any feature, for that matter) is optional, requires explicit negotiation, and (perhaps?..) applies to sub-protocols’ messages only.

(OTOH, I’m starting to feel like I’m re-inventing [IRC capability negotiation](https://ircv3.net/specs/core/capability-negotiation.html), or something…)

---

My interest got piqued after hearing rumours (FUD, nonsense, apocryphal blasphemy) that “compression will become mandatory”. This might be a non-issue for machines that run “full nodes” these days, but is an additional stress for mobile devices, including IoT.

In fact, for an IoT device, should it want to communicate over some ultra-simple as-of-yet-unwritten Ethereum-native messaging protocol, compression might just be a deal breaker. *If* there is mandatory compression, we’re discouraging this protocol from being written.

## Replies

**atoulme** (2019-01-18):

I just had to do this for my implementation of RLPx (https://github.com/ConsenSys/cava/pull/122/commits/cd35b6f7e9ac3e9f9a4f1b5b691d86a8362a8072 and https://github.com/ConsenSys/cava/pull/122).

It’s a very messy change. Most clients have implemented the change and it does save a lot of traffic.

I expect btw to see the same level of compression with SSZ for Eth 2.0.

I believe compressing network traffic is necessary. Your web browser does a zip compression all the time too.

There is a lot to hate about RLPx - compression is one aspect, but you can also see both sides of the handshake keep egress/ingress MACs updated for every byte in and out.

We also allow only one TCP connection between 2 peers (at least there is a disconnect reason to disconnect if a peer with the same identity is already connected).

I’m not sure about having one more version of DEVp2p. I’m playing with secure scuttlebutt right now to see if we could make it work for Ethereum network communications: https://ssbc.github.io/scuttlebutt-protocol-guide/

---

**veox** (2019-01-19):

> I believe compressing network traffic is necessary. Your web browser does a zip compression all the time too.

I’m not against compression per-se. I do understand the benefits. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

My grumbling is about the way it is “negotiated”. Peers both advertising v5 of DEVp2p *must* use it. Essentially, a protocol feature is “negotiated” implicitly, by advertising a protocol number. This is what I meant by “ungracefulness” in OP.

Should a v6 of DEVp2p be proposed, for whatever reason (say, a change in encryption scheme); *if* it doesn’t also include a provision for “proper” negotiation of compression via messaging, *then* compression becomes mandatory, since all nodes will interpret: `DEVp2p >= 5 ? compress`.

I’m afraid HTTP is not a good example of this, because there, it’s achieved by [“advertising compression tokens”](https://en.wikipedia.org/wiki/HTTP_compression). Not `HTTP/1.2` or something.

If anything, I’m advocating *for* HTTP-style. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

Another concern I haven’t voiced (mainly, because I know next to nothing about) is possible negative impact on Whisper/Swarm or protocols involving “onion routing”, where multiple layers of encryption prevent bandwidth savings of compression-on-top.

> We also allow only one TCP connection between 2 peers (…).

That seems like a sane, safe default to me.

DEVp2p specs [seem to have had a mention of multiplexing](https://ethereum.stackexchange.com/questions/37051/ethereum-network-messaging) in the past - it’s [gone now in its explicit form](https://github.com/ethereum/devp2p/blob/master/devp2p.md), but probably still implied. If, say, one wanted to use both `eth` and `pss` sub-protocols, that should be possible (using one connection): that’s how [Swarm PoC 3](https://blog.ethereum.org/2018/06/21/announcing-swarm-proof-of-concept-release-3/) says to be doing it, at least.

