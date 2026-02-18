---
source: magicians
topic_id: 18487
title: "ERC-7611: Sovereign Bridged NFTs"
author: 0xASK
date: "2024-02-05"
category: ERCs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/erc-7611-sovereign-bridged-nfts/18487
views: 1331
likes: 4
posts_count: 3
---

# ERC-7611: Sovereign Bridged NFTs

This is the discussion thread for:

[The ERC-7611 proposal](https://github.com/omni-network/ERCs/blob/master/ERCS/erc-7611.md)

That has an open pull request on Ethereum/RFCs [here](https://github.com/ethereum/ERCs/pull/231).

ERC-7611 proposes an extension to ERC-721 that facilitates seamless migration of NFTs across Ethereum’s rollup ecosystem without forcing NFT communities to cede sovereignty to an interoperability protocol.

NFT communities are currently stuck on the smart contract platform of their original minting. This means that they are isolated to a very small subset of the market on a single rollup, or that their users are forced to pay extremely high gas fees on L1. With all of the innovation happening across the rollup ecosystem it is essential that we establish an open and neutral way for NFT communities to seamlessly expand into the L2 ecosystem and harness the cost savings and innovation happening in these ecosystems.

This is especially important as NFTs have driven some of the most mainstream adoption of Ethereum, so we need to make sure that they are accessible and functional across L2s where a majority of the next wave of users will likely onboard into directly.

Providing sovereignty and security to NFT communities as they expand across the rollup ecosystem is essential, below we enumerate a few questions in particular that we would like to open discussion around to make sure that we establish this standard in a way that best aligns with the community interests:

**Should we abstract out the bridge authorization interfaces from any specific token standard?**

The work in this ERC has been largely inspired by the prior contributions of the Connext team under [ERC-7281](https://github.com/connext/EIPs/blob/master/EIPS/eip-7281.md) which provides the same functionality for ERC-20s. You’ll notice that the bridge authorization interfaces match ERC-7281 exactly — we believe this is the best decision so that as a community when we build tooling to empower NFT communities, that tooling can similarly be used to support token communities and vice versa. However, what about ERC-1155s, ERC-6551s, etc.? Should we launch a new specific standard extending the interfaces of each with the same authorization interfaces or should we instead create one singular interface that can be inherited by any digital asset standard to facilitate secure, sovereign transfers across rollups?

**Should we keep the `mintBatch`  and `burnMatch`  functions?**

We extended the interface to include batching functionality for transfers across smart contract platforms. The logic here is that in general this is a pain point when working with ERC-721s in a single smart contract platform, but the pain for developers goes up even further when migrating ERC-721s across domains. This manifests both in terms of complexity, but also in the form of cost.

I’d like to end on a note thanking the Connext team for their prior work on ERC-7281, it really is fantastic work that empowers token communities to embrace Ethereum’s modular ecosystem in a secure way that preserves sovereignty. We’re proud to be expanding these principles and bringing them to other digital asset standards and looking forward to collaborating with others in the community who wish to promote a future of Ethereum where no proprietary risk or lock in is baked into a future that should remain open, neutral and censorship resistant.

## Replies

**stoicdev0** (2024-02-06):

This is something I’ve been really interested in so expect me to participate a lot on the discussion ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

I understand you are using ERC-7281 as a starting point but I don’t actually see much benefit in all this limit settings which add a lot of overhead. At most I would see useful a way to set `maxSupply` (which could be “unlimited”, i.e `2**256 - 1`).

Can you add a free `bytes data` parameter on `mint` and `burn`? This would allow richer standards to use the bridging functionality too, for instance ERC-5773 which allows NFTs to have multiple assets could use this to pass the data for such assets.

I do like the batch functionality, but having struggled too often with size limits I’m not sure if it’s a good idea, this already has to go on top of 721 and if your contract has other extensions you might run out of space (please don’t suggest diamonds, those are terrible UX ![:grimacing:](https://ethereum-magicians.org/images/emoji/twitter/grimacing.png?v=12)). On top of that, usually lighter standards have more chances or making it through.

With that said, I think the `localSupply` method is absolutely useful and would even include it in the standard.

On the LockBox, for now I just have 2 things.

1. I think only the bridge should be able to call withdraw, if that’s the case please add a @dev comment on it. If that’s not the case, could you explain why?
2. I’m not fan of the name, I would rather have it reflect more it’s use. Something like BridgeLock or CrossChainLock.

Finally (for now), do you have any mock implementation?

---

**0xASK** (2024-03-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> I understand you are using ERC-7281 as a starting point but I don’t actually see much benefit in all this limit settings which add a lot of overhead. At most I would see useful a way to set maxSupply (which could be “unlimited”, i.e 2**256 - 1).

I do think that considering the overhead is worthwhile for any standard like this, however I also do think that it is important that we give NFT issuers some ability to constrain the permissions delegated to any specific interoperability network in this process.

One easy way to get the best of both worlds is just have easy default parameters that projects can opt for when setting this up that set the transfer limits to an unlimited amount so that they can effectively ignore the rate limiting functionality if they do not care to utilize that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> Can you add a free bytes data parameter on mint and burn? This would allow richer standards to use the bridging functionality too, for instance ERC-5773 which allows NFTs to have multiple assets could use this to pass the data for such assets.

Hmm very cool idea! Ya this is one thing that I wanted to lean into with this. A great goal would be to implement something more generalizable so that we didn’t have to create bespoke “x” standards for every single ERC that exists for the “digital asset” standards that we have today.

The additional expressiveness here makes it more functional and would allow us to create a standard that is more widely encompassing / useful to developers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> I do like the batch functionality, but having struggled too often with size limits I’m not sure if it’s a good idea, this already has to go on top of 721 and if your contract has other extensions you might run out of space (please don’t suggest diamonds, those are terrible UX ). On top of that, usually lighter standards have more chances or making it through.

I think this is a totally fair perspective and I am all for minimizing complexity.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> With that said, I think the localSupply method is absolutely useful and would even include it in the standard.

I agree – this strikes me as quite important for the utility on a specific domain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> On the LockBox, for now I just have 2 things
>
>
> I think only the bridge should be able to call withdraw, if that’s the case please add a @dev comment on it. If that’s not the case, could you explain why?

I disagree with this – I think it is important for users to be able to call the lockbox themselves. We should try to empower users as much as possible – one can imagine a scenario where all interoperability networks are removed from the whitelist and in this scenario all funds in the lockbox would become permanently frozen.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> On the LockBox, for now I just have 2 things
>
>
> I’m not fan of the name, I would rather have it reflect more it’s use. Something like BridgeLock or CrossChainLock.

While it is a fair point that these names might be more apt for the specific use case, in this spec I tried to adhere to the original ERC-7281 spec proposed by Connext with the goal of standardizing interfaces so we could create auxiliary tooling to empower developers to utilize all of these “x” standards in the simplest way while also reducing the probability of any implementation errors.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> Finally (for now), do you have any mock implementation?

No – I wanted to first source input from the community (thank you btw!) before moving forward to an initial implementation as I figured it was likely the initial implementation would be modified.

