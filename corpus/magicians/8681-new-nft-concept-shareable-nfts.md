---
source: magicians
topic_id: 8681
title: "New NFT concept: shareable NFTs"
author: qqmato
date: "2022-03-22"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/new-nft-concept-shareable-nfts/8681
views: 3243
likes: 4
posts_count: 7
---

# New NFT concept: shareable NFTs

Hey there,

We are considering developing a new NFT standard - shareable NFTs.

### Motivation

Regular NFTs often represent real-world objects that can change the owner in a regular way (person A gives the object to person B) and transferring of NFT reflects this action.

Shareable NFTs are intended to represent a virtual world object that can be shared between persons - e.g. a song, blog article, digital art or contribution to a open source project. These virtual world objects cannot be “moved” or “transfered” the same way as real world objects (therefore regular transferable NFTs don’t properly reflect their nature), but these types of items can be shared/copied - here we suggest shareable NFTs to represent these items and their natural behavior.

### Sharing mechanics

We envision two possible types of NFT sharing: open and permissioned sharing.

#### Open sharing

With open sharing a shareable NFT can be shared by anyone - this is suitable for NFTs representing publicly available items and the act of sharing can serve as an endorsement of the item.

#### Permissioned sharing

In this case only the original holder of the NFT could share it with someone else. This can cover use-cases such as acknowledging others that helped you receive a badge or recognition NFT.

We are also considering making these shareable NFTs non-transferable.

### Questions

Do you think these would be meaningful use-cases? Do you have any thoughts on the implementation?

## Replies

**anjimkofy** (2022-04-15):

The current NFT only allows the owner to enjoy, if it is music, the NFT is a record, tape.

When we simulate a scene, Mike Jackon released a “Heal THE WORLD”, casting 10 NFTs to sell, 10 NFT owners can listen “HEAL THE WORLD”, because rare and because of Mike Jackson’s works, inevitable Very value. But this is not in line with reality, because everyone can listen to music, should not be just 10 people’s power. In order to meet the reality, let more people hear “HEAL THE WORLD”, then need to release more NFT, when NFT is more than a certain degree, not a NFT will be valuable, because their content is the same, Then there is alternative. Map to reality, my music disc is the same, we can do exchange, I believe that most people don’t mind, because digital collection does not have depreciation and wear aging. And each NFT content is the same, repeated issuance not only waste resources, but also let NFT lose each of them is unique.

And the shared NFT is perfectly solved. NFT is a disc record, then shared NFT is streaming media music. This is not only applicable in music fields, but also novels, film and so on, there are too many imagination space!

And you can share NFT to solve the current copyright issue, and different music software is deployed without the copyright of the music artist, causing users to download a variety of music software. When the music artist passes the NFT direct connection, it will need a platform to connect to both sides. Because the platform is only responsible for providing NFT sharing, do not own NFT, this NFT is still in the music artist, so the platform will not form monopoly.

Regarding its business value, you can get a payment for a payment for life by consumer collection, or the actual situation chooses a lifetime enjoy, or subscribe. In order to avoid a wallet payment, public key can be used, and the mortgage can be used. There must be a certain number of valuable loops on the wallet. When the private key is disclosed, it will be done to transfer the loop, in order to avoid the loss of the money. There should be no one will be willing to open the key (of course there is a problem here: there is already a fraud that is intended to reveal the private key, so that there are many valuable Currency, there is no original coin as GAS, when you should Address payment, native parties will be transferred immediately by contract)

The above solution is not perfect, but I have to admit that the shared NFT is very cool, it is supplemented with the existing NFT.

---

**triddlelover69** (2022-05-17):

I think the idea of shareable NFTs is an interesting way to expand the market for digital assets. There are a lot of ways this could be done and I think it would be cool if we could start seeing some of them in action soon.

---

**yaruno** (2022-05-20):

Hi everyone, and thank you for your encouraging comments!

We’ve made with [@qqmato](/u/qqmato) a draft EIP about shareable NFTs. You can find it from here [Shareable NFT eip draft by yaruno · Pull Request #5023 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5023). Sharing is an interesting concept as it can be thought and perceived in different ways as well as it can be implemented in various ways. For example, when we talk about sharing we can think about it is as digital copying, giving a copy of a digital resource while retaining a version by ourselves. Sharing can also be fractional, though it may be interesting how that could be doable with indivisible tokens, or sharing could be about giving rights to use a certain resource.

Depending on are we sharing the pie, growing the pie or splicing the pie the different implementations of sharing would benefit from an abstraction level higher definition e.g. EIP-5023 that defines an interface which elaborates that shareable tokens should have a method of Share and an event of Share defining what was shared and to whom.

---

**high_byte** (2022-05-22):

this sounds like a subset of owning shares in an NFT where the shares are equal. ERC20 tokens better represent shares.

I would imagine it be useful to share NFTs if say the NFT represent ownership of a house, then shared ownership could be implemented by a contact owning the ownership NFT and distributing $HOME tokens that represent shared of said NFT. of course the drawback is the NFT is held by a contact, but perhaps this idea could be expanded.

---

**nilo** (2022-10-19):

I recently became curious about NFT music. I want to know how to make and share NFT music. Of course, I read on the site Zcoino which is about NFT and Obeato which is about music, but I want to know if anyone has any experience with this.

---

**yaruno** (2022-11-16):

Hi all!

Circling back to this thread as our use case of sNFTs is live! To inspire you all and to demonstrate an actual use case of these types of tokens you can check our platform at https://talkoapp.io/ and check out the about page of our reasoning for this new token type.

If you have any questions about the sNFTs, our EIP or the use case I’d be happy to answer them.

Best,

Yaruno

