---
source: magicians
topic_id: 13170
title: "DRAFT ERC: User Owned Social Reputation Profiles"
author: JonValjon
date: "2023-03-05"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/draft-erc-user-owned-social-reputation-profiles/13170
views: 498
likes: 3
posts_count: 3
---

# DRAFT ERC: User Owned Social Reputation Profiles

## Abstract

This proposal defines a system where individuals can own contracts representing their own profile. The owner of a profile can list several authoritative ‘Authorizer’ contracts to their profile, where each authorizer enforces a set of rules about who is allowed to post to the individual’s profile.

Anyone can then post data to a profile by selecting an ‘Authorizer’ from the profile’s list and meeting that contract’s on-chain validation criteria.

An interface for the ‘Profile’ and ‘Authorizer’ contracts allows a rich ecosystem of authoritative entities to moderate content and enforce rules. Ownership of the profile contract  allows the owner complete control over who can post data to their profile and what data remains on their profile while remaining completely decentralized.

To read more about this ERC draft - please visit [EIPs/EIPS/eip-draft-user-owned-social-reputation-profiles.md at master · jonvaljonathan/EIPs · GitHub](https://github.com/jonvaljonathan/EIPs/blob/master/EIPS/eip-draft-user-owned-social-reputation-profiles.md)

## Replies

**Swader** (2023-03-06):

Hi,

excellent, love to see more thinking in this direction. If I am understanding it correctly, this is very similar to what we built with RMRK EIPs, or the Reputational Avatar program presented [here](https://youtu.be/y9GHrMXlyDU).

In a nutshell, we made the NFT 2.0 standards which are backwards compatible with ERC721. They are all documented here: https://evm.rmrk.app

What you would do, is you would mint an NFT for a user, and then put other NFTs inside that NFTs. Those child NFTs are just regular NFTs, just that in this new system any NFT can also own any other. These NFTs - parent, child, or any other level - can also be non-transferable, allowing you to put permissions, reputation, and more into these social profile NFTs.

If we abstract this further, it forms the basis of a much [better data structure for Lens as well](https://twitter.com/bitfalls/status/1632608680930672640?s=20).

Let’s work together on experiments for how to merge any outstanding functionality from your proposal into what is already offered by our EIP? We increase the net usefulness of the ecosystem as a whole and stay backwards compatible with legacy.

For reference: [EIP 6059](https://evm.rmrk.app/rmrk-legos-examples/nestable) will let you put NFTs into other NFTs, and [EIP 6454](https://evm.rmrk.app/general-overview/rmrk-extensions/soulbound) will allow you to lock them inside these NFTs (soulbound 2.0 basically).

---

**JonValjon** (2023-03-07):

[@Swader](/u/swader),

![:man_bowing:](https://ethereum-magicians.org/images/emoji/twitter/man_bowing.png?v=12) Thanks for checking us out and replying with a thoughtful response!

I’ve alerted the other authors. We’re going to review the works you cited.

*Upon the first review and without talking to the other authors*

I think we’ll be backwards compatible as is. I also think both projects are additive to each other. I need to do more homework and consult the team.

Our project intended to be able to compose multiple NFT / ERC / on-chain / off-chain criteria into the Authorizer Contract. So, I think we could use the NFT 2.0 standards as criteria for those contracts to meet the defined conditions.

We want the users to be able to deploy and own their profile contracts so they don’t have to rely on a single protocol to store their identity.

So communities, DAOs, and groups can manage their Authorizer contracts, and members have their profile contracts.

Maybe we could do something interesting together where the Profile and Authorizer contracts are similar to the RMRK EIPs. ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

I’ll do my homework and get back to you!

![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12) I appreciate you,

jvj

