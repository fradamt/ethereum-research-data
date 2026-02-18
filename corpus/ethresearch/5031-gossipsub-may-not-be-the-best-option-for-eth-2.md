---
source: ethresearch
topic_id: 5031
title: Gossipsub may not be the best option for Eth 2
author: jamesray1
date: "2019-02-20"
category: Networking
tags: []
url: https://ethresear.ch/t/gossipsub-may-not-be-the-best-option-for-eth-2/5031
views: 2736
likes: 0
posts_count: 4
---

# Gossipsub may not be the best option for Eth 2

See https://github.com/w3f/messaging/ for an alternative with Whisper v2.0.

For reference, [this is the gossipsub spec](https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/README.md).

Pros:

- see the Protocol requirements section of the above, as well as the Motivation

Cons:

- it’s not specified or implemented yet

## Replies

**MihailoBjelic** (2019-02-21):

What are the advantages of the alternative (W3F’s) approach?

---

**jamesray1** (2019-02-21):

I’ve edited my post with pros and cons and made it a wiki.

---

**jamesray1** (2019-03-10):

Gossipsub has a different purpose to Whisper v 2.0.

Following is a reply from Jeff Burdges of the Web3 Foundation which cleared up misunderstandings on my part:

> We have four unrelated “messaging” projects in the works:
>
>
> There is gossipsub work for libp2p being handled entirely internally at
> Parity. It’s nothing to do with “messaging” in any conventional sense,
> just about replacing p2p broadcasts with a more efficient strategy. You
> should ask the rust-libp2p developers for more information on this.
>
>
> In Polkadot, we have an interchain message passing protocol (ICMP) for
> polkadot that is 100% about blockchains authenticating blocks, and
> nothing to do with normal “messaging”. We also have a more directed
> chunk distribution process used in the availability game for polkadot,
> where nodes must send very different messages to all other nodes, so
> basically the extreme opposite of gossipsup but still all libp2p work.
>
>
> Finally, the w3f/messaging repo you found exists for cordinating our
> work on mix networks. At first blush, mix nets are only for messages
> between two individuals, or from an individual to a blockchain, as they
> do not obviously support group messaging.
>
>
> In fact, we do want to support group messaging in the mixnet, but never
> via gossip of course. As a rule, gossip protocols are never anonymous
> because they cannot provide cryptographic unlinkability.*
>
>
> We’ve encountered problems with adding important functionality, like
> header encryption, to the current best-of-breed group messaging
> cryptography like MLS: https://messaginglayersecurity.rocks
> We’ll therefore focus on the 1-to-1 case this year, as that presents
> enough problems all by itself.

