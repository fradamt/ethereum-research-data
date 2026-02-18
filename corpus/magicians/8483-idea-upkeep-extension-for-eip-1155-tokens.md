---
source: magicians
topic_id: 8483
title: "[IDEA] Upkeep Extension for EIP-1155 Tokens"
author: Pandapip1
date: "2022-03-02"
category: Magicians > Primordial Soup
tags: [nft]
url: https://ethereum-magicians.org/t/idea-upkeep-extension-for-eip-1155-tokens/8483
views: 776
likes: 1
posts_count: 5
---

# [IDEA] Upkeep Extension for EIP-1155 Tokens

Currently, all existing token standards have no upkeep cost. This ERC would provide an extension to ERC1155 that introduces an upkeep cost (that can be paid in any number of ways - potentially even more NFTs!). If it isn’t paid, ownership of the token will change to a particular address. This could allow for a greater commission for creating NFTs, or fun concepts such as a “pet” that needs “food.”

## Replies

**Bschuster3434** (2022-03-02):

That’s an interesting idea. Perhaps it can be revoked if the maintenance isn’t paid, kind of like a forfeiture. Or if someone else pays the maintenance it can be owned by them.

I can see a loan structure working like that.

---

**Pandapip1** (2022-03-04):

> Perhaps it can be revoked if the maintenance isn’t paid

I was thinking that it could just be sent to the null address if it is to be burned, or the contract owner if it is to be re-sold.

This could be implemented by having the balanceOf function take the latest block’s timestamp (or number) into account.

---

**ravachol70** (2022-03-08):

That’s not dissimilar to basic demurrage. I fully support this concept; in fact, I think the principle should apply to the base token, i.e. ETH itself.

---

**mukas** (2022-04-12):

What a simple yet interesting idea!

And what if we expand it and make the maintenance of the token or asset can be between several?

For example, the purchase of a property between partners or sharing an account on an online content platform such as Spotify or Netflix…

Greetings

