---
source: magicians
topic_id: 9027
title: Standards for a consent token
author: EricForgy
date: "2022-04-23"
category: Magicians > Primordial Soup
tags: [token]
url: https://ethereum-magicians.org/t/standards-for-a-consent-token/9027
views: 1135
likes: 7
posts_count: 5
---

# Standards for a consent token

Hi everyone,

I did a cursory search and didn’t find a discussion on this topic, but if I missed anything, references would be appreciated ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=15)

I was inspired by Evin’s ETHDenver talk:

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/2/2369703a432790b91e4b05f343927c8bc930fe7d.jpeg)](https://www.youtube.com/watch?v=EZ_Bb6j87mg)

I’ve been busy working on something else, but this has been running in the back of my head since ETHDenver.

ERC-20, ERC-721 and ERC-1155 all contain some form of approval in order to allow the transfer of tokens out of an owner’s account.

After listening to Evin’s talk, I was wondering if a new “Consent” standard might make sense.

Consent would be dual to approval. In a consent model, you would need to give consent before anyone can transfer a token to you. The idea is that a token transfer can, in some circumstances, be a form of harassment. I think this is more of an issue for women and under-represented demographics. I know I had never even thought of this problem that some people face until Evin’s talk. I think a consent standard would make sense and am curious what others might think.

I’d be happy to help draft a more formal proposal if there was interest.

Take care,

Eric

## Replies

**mukas** (2022-04-23):

I think it’s a good idea!

It solves a problem that at least has happened to me and my acquaintances, which is having the wallet full of a lot of advertising or misleading tokens in which if you try to claim them they crack you, so it seems like a good idea to me.

Greetings

---

**ra-phael** (2022-04-25):

Yes!

This notion of requiring consent is part of my proposal for non-transferable ERC1238 tokens: [EIP-1238: Non-Transferable Tokens](https://ethereum-magicians.org/t/eip-1238-non-transferable-tokens/9044)

For an EOA, the issuer would ask for a signature from the recipient which could be displayed in a nice way, using EIP-712. It’s one small extra step affecting UX but a reasonable price to pay to avoid harm to someone’s reputation.

---

**streamerd** (2022-06-12):

Hey [@EricForgy](/u/ericforgy)  and [@ra-phael](/u/ra-phael) , I was also thinking of the same one, part of the standard.

Also would like to see that development in multi-signature wallets, so incoming transactions can be collectively approved/rejected before them landing to the account.

haven’t yet finished reading them all however, would u consider also elaborate and contemplate further on this aspect on your proposals as well?

maybe in terms of account types, along with the various asset type ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

in case there are works in progress around this, and as well for collaboration, please let me know.

I’d start another EIP, but would join another work group if such efforts already placed somewhere else rn.

---

**TimDaub** (2022-06-13):

In EIP-4973, we’re also working on a `function mintWithPermit` that shall allow collecting the consent of both the `from` and `to` accounts via signatures. We’re exploring how EIP-712 can help us with that and [@ra-phael](/u/ra-phael)’s [ERC1238Approval](https://erc1238.notion.site/ERC1238-Approval-43b7967b27ff4119ab15b4279f0fa61c) has been helpful. More details here in the “Right to Mint” section: [Addressing the most common misconceptions about Account-bound tokens](https://timdaub.github.io/2022/05/30/addressing-the-most-common-misconceptions-about-account-bound-tokens/#right-to-mint)

