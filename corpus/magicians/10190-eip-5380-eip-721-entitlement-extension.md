---
source: magicians
topic_id: 10190
title: "EIP-5380: EIP-721 Entitlement Extension"
author: Pandapip1
date: "2022-07-31"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5380-eip-721-entitlement-extension/10190
views: 2558
likes: 1
posts_count: 9
---

# EIP-5380: EIP-721 Entitlement Extension

https://github.com/ethereum/EIPs/pull/5380

## Replies

**Pandapip1** (2022-08-02):

Originally from this comment but now a completely different proposal: [EIP4907: ERC-721 User And Expires Extension - #17 by TimDaub](https://ethereum-magicians.org/t/eip4907-erc-721-user-and-expires-extension/8572/17)

---

**SamWilsn** (2022-09-02):

Why use the zero address as the owner for `EntitlementChanged`? Seems like you’d have two possible representations for the owner (the zero address, and their own address). Do they mean different things?

What are the fields of that event supposed to represent (specifically `contract`)?

---

How is the `reason` argument supposed to be used? If it’s important, should it be logged? If it isn’t, should it be removed from the interface?

---

**Pandapip1** (2022-09-02):

> Why use the zero address as the owner for EntitlementChanged? Seems like you’d have two possible representations for the owner (the zero address, and their own address). Do they mean different things?

The default value of `address` is `address(0)`. In order to save gas, setting `address(0)` to mean the current user means that contracts can just return the user’s address if the entitlement is set to `address(0)`. This ends up being a not insignificant saving over a large user base.

---

**Pandapip1** (2022-09-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> What are the fields of that event supposed to represent (specifically contract)?

`contract` represents the contract address of the EIP-721 token.

---

**Pandapip1** (2022-09-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> How is the reason argument supposed to be used? If it’s important, should it be logged? If it isn’t, should it be removed from the interface?

That was a suggestion by [@xinbenlv](/u/xinbenlv). I would be happy to remove it, and I do think that it should be logged if kept.

---

**SamWilsn** (2022-09-02):

I’m not sure I follow, but that isn’t particularly important. This is good content for the rationale section, as I’m sure you know ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**xinbenlv** (2022-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> How is the reason argument supposed to be used? If it’s important, should it be logged? If it isn’t, should it be removed from the interface?

One example of the use of extraParams is that in GovernorBravo

```auto
function castVoteWithReason(uint proposalId, uint8 support, string calldata reason)
```

When I am designing the EIP-5453 (Endorsemen) it turns out to me having the ability to give extraParams makes future extension more available.

Obviously this is my author peer-review comment, please feel free to make your own authorship judgement, Pandapip1

---

**Pandapip1** (2022-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> When I am designing the EIP-5453 (Endorsemen) it turns out to me having the ability to give extraParams makes future extension more available.

Why couldn’t an EIP just extend this EIP and have an additional implementation that has an additional function signature?

