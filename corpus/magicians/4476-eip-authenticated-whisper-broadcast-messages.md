---
source: magicians
topic_id: 4476
title: "EIP: Authenticated Whisper Broadcast Messages"
author: rook
date: "2020-08-02"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-authenticated-whisper-broadcast-messages/4476
views: 563
likes: 0
posts_count: 1
---

# EIP: Authenticated Whisper Broadcast Messages

I like the idea of the Whisper Wire protocol, so I extended it to add security features and described a way for smart contracts to emit authenticated broadcast messages:


      [github.com](https://github.com/TheRook/EIPs/blob/master/EIPS/eip-auth-boradcast.md)




####

```md
---
eip:
title: Authenticated Broadcast Messages
author: Michael Brooks
discussions-to:
status: Draft
type:
category (*only required for Standard Track):
created:
requires (*optional):
replaces (*optional):
---

## Simple Summary
This standard builds off of “EIP-627: Whisper Specification” and addresses concerns around whisper messages lacking a method of authenticity. By levering the blockchain as a ground truth an authenticated messaging layer can be built on top of whisper.

## Abstract
By the EIP-627 specification, not all whisper wire messages are created equal.  Each whisper message has an associated proof-of-work that establishes a value of the message. When the network is inundated with messages, then nodes will cull lower-value messages. Anyone can send a message to any publishing channel, and include any information they so choose.

Blockchains are not subject to proof-of-work pre-computation attacks because newly formed blocks must contain information about the previous block.  Authenticated messages take this a step further, and also includes information about a transaction that emitted the message.
```

  This file has been truncated. [show original](https://github.com/TheRook/EIPs/blob/master/EIPS/eip-auth-boradcast.md)








I am very confused by the name choice for the protocol.  I don’t think “whispering” is an accurate name for a global broadcast.  Additionally, I was first drawn to this project because I thought it was written by Whisper Systems, and now I don’t think they are related at all.
