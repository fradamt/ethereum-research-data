---
source: magicians
topic_id: 9905
title: "Idea: Bundle NFT with ERC20 tokens for intrinsic value"
author: westofpluto
date: "2022-07-11"
category: ERCs
tags: [nft, token]
url: https://ethereum-magicians.org/t/idea-bundle-nft-with-erc20-tokens-for-intrinsic-value/9905
views: 487
likes: 1
posts_count: 3
---

# Idea: Bundle NFT with ERC20 tokens for intrinsic value

This is my first post/suggestion here, but it is an idea that I have been thinking of for a week or two - an idea that, if not yet proposed, might work towards providing NFTs with more intrinsic value, thereby rejuvenating the market for them. Please let me know what you all think.

As we are all seeing from the collapse in prices for NFTs on OpenSea and other markets, consumers are realizing that the current NFT standard ERC-721 just gives you ownership of something like an easily replicable JPEG stored offchain, i.e., something that has no intrinsic value, just perceived value. Furthermore, recent US regulatory guidance has suggested that many/most crypto tokens are likely to be treated as commodities. If that is to be a reasonable analogy, we should realize that commodities generally have intrinsic value: oil is used for energy, wheat is used for food, gold is used for jewelry and ornamentation, etc. In particular, gold and silver are fungible elements but become non-fungible with intrinsic value when a specific set of gold or silver is collected and fabricated into jewelry or ornamentation. The resulting product is non-fungible but has intrinsic value from the previously fungible quantity of gold/silver that was used to create it.

Suppose we wanted to provide a way for NFTs to have intrinsic value. One way would be to have NFTs be able to bundle/lock-up a specific amount of (say) ETH (or other token) into an internal “vault” that is locked together with the NFT. The NFT can be transferred/sold to another wallet, and the internal vault with the locked ETH is transferred with it. Potential buyers could query the NFT contract to verify the intrinsic value of tokens locked together with the NFT. Any wallet that holds this NFT with its internal vault of ETH would NOT be able to sell the locked ETH/tokens separately from the NFT, without calling a function on the NFT contract to unbundle the ETH/tokens from the NFT - an action that would allow future buyers to also see that the NFT no longer has the locked intrinsic value.

My guess is that to create this, a more advanced ERC for NFTs would be required, i.e., a contract that inherits from ERC721 but adds more capabilities/restrictions. It may also be the case that the locked fungible tokens would have to adhere to a standard that derives from ERC20 but also adds more restrictions. Perhaps one has to wrap an ERC20 token into a new ERCXXX token that uses a contract that inherits from ERC20 but is linked to a specific NFT and cannot be transferred/traded unless it does so with the NFT.

Such a feature would boost the luxury/vanity NFT market. The same people who buy $50K gold/diamond Rolex watches (even though your iPhone tells time just as well) might be more interested in buying and showing off NFT’s if their NFT’s had verifiable intrinsic value. This approach probably opens up numerous other applications (e.g. in the financial sector) that I have not thought of yet.

Thoughts/comments? Or is this already proposed somewhere and I missed it?

## Replies

**Pandapip1** (2022-07-11):

Unfortunately, this will not work.

If one can simply *withdraw* the ether or other comparable asset from the NFT if one owns it, then if the NFT alone is worth $X, then either the seller will withdraw the ETH (say it’s worth $Y) and sell the NFT for $X, netting $X+$Y. If the seller sells the NFT without withdrawing the ETH, then it will sell for $X+$Y (as that would be the value that the seller would get out of it).

If the ETH is simply *burnt*, then no new standard is needed. Simply transfer an amount of ETH or ERC20 token to the NFT’s smart contract address. What if the smart contract doesn’t have a payable function? Then use the “create a smart contract that instantly self-destructs” technique. However, the value this will create for the burner will *always* be lower than the amount burned.

Great idea, though!

---

**westofpluto** (2022-07-11):

Hi and thanks for the response.

I’m not sure why you say “this will not work.” The first example you give shows it works perfectly as designed. The second example (burning the ETH) adds no intrinsic value to the NFT, so it is exactly the sort of situation the proposed idea is meant to avoid. The second example shows exactly why the idea is needed.

Let’s look at the first example and use the analogy of a piece of gold jewelry. Gold itself is a fungible commodity but a specific quantity of gold used to make a specific piece of jewelry essentially locks the gold into a non-fungible item (a specific piece of jewelry). A seller can sell this non-fungible piece of jewelry for ($X+$Y) where $X is the worth of the jewelry item without the gold and $Y is the value of the gold (the intrinsic value. Or the seller could replace the gold in the jewelry with very cheap gold colored material with no intrinsic value and sell the jewelry item for $X. Or the seller could buy the gold jewelry item for $X+$Y and then extract the gold and sell that for $Y and sell the jewelry item to someone else for $X. Assuming the value of the jewelry itself is always $X regardless of how much gold is in it (not a very good assumption), then yes there is no advantage or disadvantage in price to keeping the items bundled or unbundling them. But that isn’t the point! The point is that bundling a piece of jewelry (or an NFT) with intrinsic value provides higher commercial appeal to the item. In your terms the $X of a piece of jewelry or NFT is going to be much higher if the NFT has higher intrinsic value. The values of X and Y are definitely not independent.

Right now the $X value (the perceived value) of the vast majority of NFT’s is basically zero. That is the problem - most people have no interest in spending any money on a JPEG that anyone can copy. Because there is no intrinsic value, the perceived value is now going to zero. By adding intrinsic value, the perceived value also goes up.

Think of it this way: you see a necklace at a store but discover the material is cheap gold plated and the stone is cubic zirconia. The materials are worth a few dollars at most. You might pay $$20 for that to give to your daughter. So the perceived value is slightly less than $20. Compare that to a gorgeous diamond necklace where the stone is 2 carats and the material is gold. The intrinsic value might be $10K but it is likely that the the necklace would sell for quite a bit more than this. In other words, the value of the necklace by itself, not considering materials is quite a bit more than an extra $20.

In other words X (the perceived value) = function of Y (the intrinsic value). As Y gets bigger, so does X.

Do you have some other reason why you think this wouldn’t work?

