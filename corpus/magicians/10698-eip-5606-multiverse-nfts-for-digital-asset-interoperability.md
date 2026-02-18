---
source: magicians
topic_id: 10698
title: "EIP-5606: Multiverse NFTs for digital asset interoperability"
author: gaurangtorvekar
date: "2022-09-06"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5606-multiverse-nfts-for-digital-asset-interoperability/10698
views: 3144
likes: 7
posts_count: 8
---

# EIP-5606: Multiverse NFTs for digital asset interoperability

This specification defines a minimal interface to create a multiverse NFT standard for digital assets such as wearables and in-game items that, in turn, index the delegate NFTs on each platform where this asset exists. These platforms could be metaverses, play-to-earn games or NFT marketplaces. This proposal depends on and extends EIP-721 and EIP-1155.

The ERC specification defines an interface, which acts as an abstract layer on top of existing NFTs that we call a ‘Multiverse NFT’. A multiverse NFT indexes a digital asset and tracks its various incarnations across different metaverse platforms, games and such. We call the individual representations of this digital asset on the various platforms ‘delegate NFTs’. The standard also allows for the ‘bundling’ and ‘unbundling’ of these delegate NFTs within the multiverse NFT so holders can trade them individually or as a bundle.

status: Draft

type: Standards Track

category: ERC

[Link to the PR](https://github.com/ethereum/EIPs/pull/5606)

[Explanatory Blog](https://gaurangtorvekar.medium.com/proxy-nfts-soulbond-nfts-for-a-digital-asset-6f59922aab55)

## Replies

**SamWilsn** (2022-09-20):

Might be worth looking into [EIP-4955: Vendor Specific Metadata Extension for Non-Fungible Tokens](https://eips.ethereum.org/EIPS/eip-4955). Not exactly the same, but seems related.

---

**gaurangtorvekar** (2022-09-21):

Thanks for that! This is quite relevant, it is trying to solve a similar use case, and the NFTs implementing our standard - “Multiverse NFTs” - can use this metadata schema.

While EIP-4955 only deals with a few new schema entries for NFT metadata, our EIP encompasses a new NFT standard, which allows the ownership of the child NFTs on the various metaverses through bundling and unbundling! Hence, it goes beyond the EIP-4955 and adds much more functionality to the implementation.

---

**poojaranjan** (2022-11-01):

[EIP-5606: Multiverse NFTs with Gaurang Torvekar](https://youtu.be/PajykC_RV9Q)

  [![image](https://i.ytimg.com/vi/PajykC_RV9Q/hqdefault.jpg)](https://www.youtube.com/watch?v=PajykC_RV9Q)

---

**jcbdev** (2022-11-23):

I just had a look through the EIP and the stock implementation.  I really like the idea but I think there are potentially a few avenues for abuse currently

This relies on the honesty of the “bundler” and/or the current owner such that when it comes to trading the bundles as there is no protection for the purchaser on bad actions performed by the current owner.  My primary scenario I am thinking of is bait and switch - where the bundle is listed for sale but when it comes to transfer the bundle is unbundled and then rebundled with different items using the same multiverseTokenID before transfer.  Maybe there is and I missed it when I read through the contract?

The other scenario is using a bundle to trojan horse a forgery/fake on one platform through by bundling it with some genuine versions of the item on other platforms.

Just my initial thoughts.

---

**gaurangtorvekar** (2022-11-24):

Thanks for your feedback. We have considered this issue and we have already addressed by introducing the `initBundle` functionality.

I would like to point you to this section in the EIP documentation -

> Any dapp implementing this standard would initialise a bundle by calling the function initBundle . This mints a new multiverse NFT and assigns it to msg.sender. While creating a bundle, the delegate token contract addresses and the token IDs are set during the initialisation and cannot be changed after that. This avoids unintended edge cases where non-related NFTs could be bundled together by mistake.

I am assuming this safeguard can resolve the issue that you mentioned…

---

**jcbdev** (2022-11-24):

Thanks for the quick reply. I didn’t notice that part so thanks.

It doesn’t fully solve it in it’s current form.  In the stock implementation the initBundle function is public and unsecured so any person can initialise their own bundle (Obviously a dApp could secure this in their particular implementation but they would need to remember to do that).

But the most important issue is still the ability to sell the bundles and to unbundle all NFTs at any time with no purchase or transfer protections for buyer.

A bad party could list the bundle for sale on a marketplace and just prior to transfer of the bundle they could unbundle all the items. This would leave the purchaser receiving an empty bundle without the NFTs they thought they were buying.

Perhaps transfer should be blocked whilst some items are currently unbundled? Or perhaps a way to lock the bundle for sale temporarily removing the current owners ability to unbundle until the next transfer?

---

**gaurangtorvekar** (2022-11-25):

> It doesn’t fully solve it in it’s current form. In the stock implementation the initBundle function is public and unsecured so any person can initialise their own bundle (Obviously a dApp could secure this in their particular implementation but they would need to remember to do that).

While writing the EIP, we define an interface, and the implementation can vary from one use case to another. Each DAPP or marketplace could define the internal logic and the safeguards when implementing this EIP. Also, the purpose of the `initBundle` function is to publicly initialize a bundle and define it beforehand so that it deters these kinds of malicious users in the first place ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=12)

> A bad party could list the bundle for sale on a marketplace and just prior to transfer of the bundle they could unbundle all the items. This would leave the purchaser receiving an empty bundle without the NFTs they thought they were buying.
>
>
> Perhaps transfer should be blocked whilst some items are currently unbundled? Or perhaps a way to lock the bundle for sale temporarily removing the current owners ability to unbundle until the next transfer?

I believe the problem has already been resolved by existing marketplaces out there - firstly, marketplaces can show the status of the delegates in real-time and the buyers can make sure that the delegate NFTs are really present in this contract before buying. Secondly, “atomicMatch” as defined in [Wyvern protocol](https://wyvernprotocol.com/docs/protocol-components) is exactly meant for this purpose - to ensure the safety of both the seller and the buyer.

In any case, if Wyvern and atomic match is not used, then this issue can plague any sort of buying transaction even for normal NFTs.

