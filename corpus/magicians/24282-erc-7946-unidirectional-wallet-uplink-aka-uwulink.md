---
source: magicians
topic_id: 24282
title: "ERC-7946: Unidirectional Wallet Uplink aka UWULink"
author: moodysalem
date: "2025-05-20"
category: ERCs
tags: [erc, wallet, qr-codes]
url: https://ethereum-magicians.org/t/erc-7946-unidirectional-wallet-uplink-aka-uwulink/24282
views: 227
likes: 4
posts_count: 6
---

# ERC-7946: Unidirectional Wallet Uplink aka UWULink

Discussion thread for ERC-7946: [add uwulink ERC by moodysalem · Pull Request #1043 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1043/files)

## Replies

**rmeissner** (2025-05-20):

Really like the pattern of the programmable mode. Do you think it would make sense to separate this from the encoding part (protobuf)?

While I am not opposed to Protobuf, I see that the pattern used by the programmable mode could be valuable even in a rpc based world.

---

**SamWilsn** (2025-06-19):

*What’s This?!* **notices you have a new standard** Some non-editorial comments:

I echo [@rmeissner](/u/rmeissner)’s comment that separating this from protobufs might be a good idea, but a different reason. Simply referring to protobufs from an ERC is going to be difficult on an editorial level. They aren’t defined in an RFC (or any other approved document source), and that means the reader cannot get a complete understanding of the specification from the ERC itself. As for why we’re very careful about the external sources we allow, see [markdown-rel-links](https://ethereum.github.io/eipw/markdown-rel-links/). That said, the wire format specification is stored in a [git repository](https://github.com/protocolbuffers/protocolbuffers.github.io/blob/951fee0f8b6470dece55b1792d4ff21bb4549fab/content/programming-guides/encoding.md), so one could follow [EIP-5757](https://eips.ethereum.org/EIPS/eip-5757) and try to get it approved but YMMV.

On another note, I love this idea. This is a huge advancement over [ERC-4804](https://eips.ethereum.org/EIPS/eip-4804) and its decedents.

As I’m sure you’re well aware, browsers, unfortunately, don’t support registering arbitrary schemes in extensions or with [registerProtocolHandler](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler). How would you propose working around that issue?

A particular concern of mine when designing a forward-compatible protocol, is how to handle mandatory new fields in a schema. Say a new version of UWULink comes out, and it introduces an optional field that *MUST* be understood if present or the request should fail. Does this proposal provide such a feature? Should it?

---

**SirSpudlington** (2025-06-25):

Question: Was the acronym created **before** or **after** the full name was created?

---

**moodysalem** (2025-06-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> How would you propose working around that issue?

Good question, I don’t have an answer though. For context, websites can register protocol handlers with the browser using the `web+` prefix as described [here](https://developer.chrome.com/docs/web-platform/best-practices/url-protocol-handler) (e.g. a web based wallet like Coinbase’s smart wallet) and in the extension manifest as described [here](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/protocol_handlers).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Say a new version of UWULink comes out, and it introduces an optional field that MUST be understood if present or the request should fail.

I’d consider that a breaking change to the protocol that we should strive to avoid. I can’t think of a good example where we’d need to do this though.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> Question: Was the acronym created before or after the full name was created?

![:point_right:t4:](https://ethereum-magicians.org/images/emoji/twitter/point_right/4.png?v=12)![:point_left:t4:](https://ethereum-magicians.org/images/emoji/twitter/point_left/4.png?v=12)![:face_holding_back_tears:](https://ethereum-magicians.org/images/emoji/twitter/face_holding_back_tears.png?v=12)

---

**wighawag** (2025-07-05):

Nice proposal, thanks for writing!

Any reason why offchain signature request are not supported?

Would be great to be able to have offchain signature benefit from the one-off flow

Furthermore there is some contrats execution that require such offchain signature to be passed in

I thus see 2 thing missing in the proposal:

- Ability to request offchain signature
- ability to pass in result from one signature request of the list in the next execution/signature requests

