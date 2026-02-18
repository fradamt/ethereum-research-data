---
source: magicians
topic_id: 19506
title: "Proposal for a New ERC: Token Transfer Validation"
author: nathanglb
date: "2024-04-02"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/proposal-for-a-new-erc-token-transfer-validation/19506
views: 657
likes: 5
posts_count: 4
---

# Proposal for a New ERC: Token Transfer Validation

ERC20/ERC721/ERC1155 are all token standards that have existed for many years.  The battle over creator royalties has been ongoing for some time now, and Limit Break has built an extension to these standards that allow creators to put custom controls in place for transfers.  The extension, known as Creator Token Standards (or ERC721C) is quickly becoming the standard of record for creators that wish to enforce royalties on their collections, or perhaps to build other cool gamified features for tokens.

To date, Magic Eden and OpenSea marketplaces have recently adopted use of ERC721C standards for creator earnings/royalty enforcement.  There are many creators who want to adopt ERC721C, so now seems to be an appropriate time to start formalizing an ERC that standardizes this extension to the core token standards for creators who wish to use it.

## Replies

**ryley-o** (2024-04-09):

I agree that formalizing the standard would be very appropriate, as the current name of ERC721C is misleading. The extension created by Limit Break did not go through the ERC review process, and the extension fundamentally changes the ownership model of the tokens on those contracts (single token owner now becomes joint ownership between entity controlling the transfer validation logic and token owner).

Giving the community a peer-reviewed ERC that includes all risks and highlights different changes is important and will provide a place for consumer education.

I would also encourage this community to consider options beyond the current Limit Break implementation, as I personally do not feel comfortable with the long-term security implications of admin-controlled whitelists on my tokens.

---

**LB-mitch** (2024-04-09):

It’s important to note that the LB implementation of the creator token standards only requires that a contract have a transfer validator - this can come in any form such as a whitelist, blacklist, authorizer model, and more.

Limit Break does provide a canonical validator, but this can be changed at any time.

---

**ryley-o** (2024-04-09):

Good call - an important distinction and updated my post above to indicate joint ownership between the entity controlling the transfer validation logic and token owner. Because the transfer validation is configurable, the entity controlling that configuration could be a contract owner, or a hard-coded allowlist owner, etc.

