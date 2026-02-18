---
source: magicians
topic_id: 853
title: "RC: Shout Message Hub"
author: trigun0x2
date: "2018-07-23"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/rc-shout-message-hub/853
views: 1225
likes: 2
posts_count: 3
---

# RC: Shout Message Hub

Hello everyone,

I’m here to propose what I believe should be a primitive in the Ethereum ecosystem. Please note this is an still in ideation phase and I’d love constructive feedback from other smart people like yourselves.

Shout: a proposal for an open standard for smart contract to user notifications.

You can read the description here: [Google Doc](https://docs.google.com/document/d/1VlVkRWS2m1sQ3pUQP85rHGB0nKSE02RPUdgABGLqfVY)

Tldr: smart contract message send a message to the Shout smart contract. Off-chain services can poll from the smart contract for messages.

Here are my main areas of concern/discussion:

1. Events vs Storage
I chose to persist message so services like MetaMask do not have to replay previous blocks.
2. When to delete messages?
3. How can current smart contracts adapt to this standard?
4. Message schema: How can a smart contract pass dynamic data to the Shout contract?
5. Does this even belong as an EIP?

## Replies

**boris** (2018-07-24):

Might be useful to look at [@expede](/u/expede) ‘s ERC  1066 as being related. In fact, you might support the message format in shout [ERC-1066: Ethereum Status Codes (ESC)](https://ethereum-magicians.org/t/erc-1066-ethereum-status-codes-esc/283)

Recent presentation here [Lightning Talk: Ethereum Status Codes ERC 1066](https://ethereum-magicians.org/t/lightning-talk-ethereum-status-codes-erc-1066/770)

ERCs for standardization “above” the token level are totally appropriate.

Welcome, thanks for contributing!

---

**trigun0x2** (2018-07-24):

Thanks a lot! ERC-1066 is something I’d love to incorporate into the contract! I’ve reached out to [@expede](/u/expede) to get her opinions on the idea.

