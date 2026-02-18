---
source: magicians
topic_id: 12171
title: "Final: EIP-6105: No Intermediary NFT Trading Protocol With Mandatory and More Diverse Royalty Schemes"
author: 5cent-AI
date: "2022-12-16"
category: EIPs
tags: [nft, token, trading]
url: https://ethereum-magicians.org/t/final-eip-6105-no-intermediary-nft-trading-protocol-with-mandatory-and-more-diverse-royalty-schemes/12171
views: 4012
likes: 7
posts_count: 19
---

# Final: EIP-6105: No Intermediary NFT Trading Protocol With Mandatory and More Diverse Royalty Schemes

No Intermediary NFT Trading Protocol With More Diverse Royalty Schemes

## Abstract

Add a marketplace functionality to ERC-721 to enable non-fungible token trading without relying on an intermediary trading platform. At the same time, implement a mandatory, more diverse royalty scheme.

## Motivation

Most current NFT trading relies on an NFT trading platform acting as an intermediary, which has the following problems:

1. Security concerns arise from authorization via the setApprovalForAll function. The permissions granted to NFT trading platforms expose unnecessary risks. Should a problem occur with the trading platform contract, it would result in significant losses to the industry as a whole. Additionally, if a user has authorized the trading platform to handle their NFTs, it allows a phishing scam to trick the user into signing a message that allows the scammer to place an order at a low price on the NFT trading platform and designate themselves as the recipient. This can be difficult for ordinary users to guard against.
2. High trading costs are a significant issue. On one hand, as the number of trading platforms increases, the liquidity of NFTs becomes dispersed. If a user needs to make a deal quickly, they must authorize and place orders on multiple platforms, which increases the risk exposure and requires additional gas expenditures for each authorization. For example, taking BAYC as an example, with a total supply of 10,000 and over 6,000 current holders, the average number of BAYC held by each holder is less than 2. While setApprovalForAll saves on gas expenditure for pending orders on a single platform, authorizing multiple platforms results in an overall increase in gas expenditures for users. On the other hand, trading service fees charged by trading platforms must also be considered as a cost of trading, which are often much higher than the required gas expenditures for authorization.
3. Aggregators provide a solution by aggregating liquidity, but the decision-making process is centralized. Furthermore, as order information on trading platforms is off-chain, the aggregator’s efficiency in obtaining data is affected by the frequency of the trading platform’s API and, at times, trading platforms may suspend the distribution of APIs and limit their frequency.
4. The project parties’ royalty income is dependent on centralized decision-making by NFT trading platforms. Some trading platforms implement optional royalty without the consent of project parties, which is a violation of their interests.
5. NFT trading platforms are not resistant to censorship. Some platforms have delisted a number of NFTs and the formulation and implementation of delisting rules are centralized and not transparent enough. In the past, some NFT trading platforms have failed and wrongly delisted certain NFTs, leading to market panic.

## Solution

In short, the NFT trading function is directly written into the NFT’s own contract, and the royalty distribution mechanism is set. In this way, we have no intermediary, safer, 0 service fee, with network-wide liquidity and meet the project party of the copyright tax revenue, anti-censorship NFT trading protocol.

### Mechanism Design

It includes:

~ a method to list an item for sale or update an existing listing, whether private sale (only to a specific address) or public (to anyone),

~ a method to delist an item that has previously been listed,

~ a method to purchase a listed item while royalties are automatically distributed

~ a method to view a specific listing.

Optional: Collection Offer Extention and Item Offer Extention

This interface could also be adapted for ERC1155 standard, but might require adjustments

Note: Compatibility with [EIP6147](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6147.md) can be considered in the future. NFT can only be traded without `guard`

## Other - Optional Blocklist

Some viewpoints suggest that tokens should be prevented from trading on intermediary markets that do not comply with royalty schemes, but this standard only provides a functionality for non-intermediary NFT trading and does not offer a standardized interface to prevent tokens from trading on these markets. If deemed necessary to better protect the interests of the project team and community, they may consider adding a blocklist to their implementation contracts to prevent NFTs from being traded on platforms that do not comply with the project’s royalty scheme.

If community members support it, they may also block these platforms that charge higher service fees.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6105.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6105.md)



```md
---
eip: 6105
category: ERC
status: Moved
---

This file was moved to https://github.com/ethereum/ercs/blob/master/ERCS/erc-6105.md
```












    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png)

      [Better and More Diverse Royalty Schemes](https://ethereum-magicians.org/t/better-and-more-diverse-royalty-schemes/13070)




> Better and More Diverse Royalty Schemes
> Abstract
> By using modern tax theory, various royalty schemes are proposed to better fit the diversity of NFTs and industry development. Through research, most of the royalty schemes can be implemented without any improvements to EIP2981.
> Royalty Scheme
> We replace the _salePrice in EIP2981 with the taxablePrice.
> That is, the expression of
> function royaltyInfo( uint256 _tokenId, uint256 _salePrice ) external view returns ( address receiver, uint256 royalt…

## Replies

**5cent-AI** (2022-12-16):

I think the trading market of CryptoPunks is worth referring to.

https://etherscan.io/address/0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb#code

---

**5cent-AI** (2022-12-23):

https://news.artnet.com/market/nft-marketplace-opensea-delisting-cuban-artists-us-sanctions-2235440

OpenSea is delisting Cuban artist and collector accounts from its platform.Everyone has the right to enjoy the convenience brought by NFT. This is one of the reasons we need `No Intermediary NFT Trading Protocol`

---

**5cent-AI** (2023-02-09):

Here are some previous discussions for reference.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lambdalf-dev/48/7940_2.png)
    [Idea: A marketplace extension to ERC721 standard](https://ethereum-magicians.org/t/idea-a-marketplace-extension-to-erc721-standard/11975) [Tokens](/c/tokens/18)



> “Not your marketplace, not your royalties”
> OpenSea’s latest code snippet gives them the ability to entirely control which platform your NFTs can (or cannot) be traded on.
> We propose to add basic marketplace functionality to the ERC721  standard to allow projects creators to gain back that control.
> It includes:
> ~ a method to list an item for sale or update an existing listing, whether private sale (only to a specific address) or public (to anyone),
> ~ a method to delist an item that has previ…

Since lambdalf-dev doesn’t have much time lately, it’s best to discuss EIP6105 here to keep track of the latest progress.

---

**5cent-AI** (2023-02-17):

**“Not your marketplace, not your royalties”**

This is reflected in the recent royalty strategies adopted by Blur and OpenSea in the competition

---

**william1293** (2023-02-27):

The new royalty scheme, especially the value-added royalty, sounds good. I would appreciate further explanation.

---

**zt1991666** (2023-02-27):

agree with you!

it is annoying to trade in a series of marketplaces for NFT holders, and it is unreasonable that the marketplace decides how much royalty the creator can get.

---

**5cent-AI** (2023-02-27):

There is a discussion of more diverse royalty schemes here：



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png)

      [Better and More Diverse Royalty Schemes](https://ethereum-magicians.org/t/better-and-more-diverse-royalty-schemes/13070)




> Better and More Diverse Royalty Schemes
> Abstract
> By using modern tax theory, various royalty schemes are proposed to better fit the diversity of NFTs and industry development. Through research, most of the royalty schemes can be implemented without any improvements to EIP2981.
> Royalty Scheme
> We replace the _salePrice in EIP2981 with the taxablePrice.
> That is, the expression of
> function royaltyInfo( uint256 _tokenId, uint256 _salePrice ) external view returns ( address receiver, uint256 royalt…

---

**Alex-Klasma** (2023-02-27):

It seems that as long as you implement a ERC721.transfer function it will be impossible to enforce royalties. Yes it’s true that you can block other marketplaces smart contracts, but eventually marketplaces will spring up that automatically generate new smart contracts (perhaps per-trade) to get around these blocks.

Then what, you block autogenerated smart contracts by comparing ext_code_hash(address) with a “blacklist” of bad code hashes that don’t respect royalties? Then the autogenerated smart contracts start adding randomization in order to get around these sort of hash blocking schemes. Etc.

The only way to truly enforce royalties is to remove the ERC721.transfer function. Make a new transfer function that requires ETH to be sent in the other direction of the transfer, and then tax that. In order to prevent 0ETH or dust amts being sent in the other direction, you could pull the “floor price” from this NFT collection (from Chainlink or other) and enforce that the ETH amount is at least some fraction of this floor price.

But do we really want that? Perhaps we should look beyond royalties if they aren’t really possible to enforce without really cumbersome changes or arms-race style blocklists.

---

**5cent-AI** (2023-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-klasma/48/7919_2.png) Alex-Klasma:

> It seems that as long as you implement a ERC721.transfer function it will be impossible to enforce royalties. Yes it’s true that you can block other marketplaces smart contracts, but eventually marketplaces will spring up that automatically generate new smart contracts (perhaps per-trade) to get around these blocks.

We must consider compatibility issues. Removing the transfer function will bring more inconvenience. Even if we do so, traders can still complete deals privately and transfer NFTs online at extremely low prices.

However, I don’t think we should assume that everyone is unethical. I believe that most people are willing to pay royalties while themselves benefiting from NFT.

Therefore, designing standards from the perspective of increasing the “cost of illegal activities” is more appropriate.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-klasma/48/7919_2.png) Alex-Klasma:

> Then what, you block autogenerated smart contracts by comparing ext_code_hash(address) with a “blacklist” of bad code hashes that don’t respect royalties? Then the autogenerated smart contracts start adding randomization in order to get around these sort of hash blocking schemes. Etc.

Doing so would significantly increase the gas cost for traders and also increase their exposure to risk. You can think of it as increasing the “cost of illegal activities.”

For an intermediary trading market, if it does not follow the royalty scheme, it may lose its users instead of gaining more users as a result. If we achieve this goal, the number of “violators” in the market will be greatly reduced.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-klasma/48/7919_2.png) Alex-Klasma:

> The only way to truly enforce royalties is to remove the ERC721.transfer function. Make a new transfer function that requires ETH to be sent in the other direction of the transfer, and then tax that. In order to prevent 0ETH or dust amts being sent in the other direction, you could pull the “floor price” from this NFT collection (from Chainlink or other) and enforce that the ETH amount is at least some fraction of this floor price.

In addition to NFT trading, there are also financial scenarios such as NFT lending, NFT renting, etc. NFTs have a lot of utility. The method mentioned above would limit the value of NFTs only to NFT trading, which may not be appropriate.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-klasma/48/7919_2.png) Alex-Klasma:

> we should look beyond royalties

I completely agree with that view. As you said, there is no perfect royalty solution. NFTs should have greater value and more room for imagination. Even with a royalty scheme, we can make some changes to adapt to the development of NFTs. Here are some studies on the new royalty scheme.We have already reserved scalability for this in the interface.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png)

      [Better and More Diverse Royalty Schemes](https://ethereum-magicians.org/t/better-and-more-diverse-royalty-schemes/13070)




> Better and More Diverse Royalty Schemes
> Abstract
> By using modern tax theory, various royalty schemes are proposed to better fit the diversity of NFTs and industry development. Through research, most of the royalty schemes can be implemented without any improvements to EIP2981.
> Royalty Scheme
> We replace the _salePrice in EIP2981 with the taxablePrice.
> That is, the expression of
> function royaltyInfo( uint256 _tokenId, uint256 _salePrice ) external view returns ( address receiver, uint256 royalt…

But regardless, we must consider protecting the interests of creators and holders. Without them, innovation will no longer occur in the NFT space.

Although we are discussing the royalty issue, I would like to add some thoughts on EIP-6105. The benefits of implementing it are not limited to enforcing royalty payments (it doesn’t even provide a standard method for setting blocklists, haha). It provides a more secure, decentralized, censorship-resistant, and zero-service-fee way of trading NFTs.

---

**dievardump** (2023-02-28):

About the EIP:

Putting the marketplace stuff in the contract is how most contracts did it at the beginning(following punks) and it became very quickly obvious that is was a bad idea.

- any wrong implementation or bug was impossible to fix and can lead to a dead collection
- managing a marketplace is complicated and is actually problematic in some countries ( need trade license etc…)
- on-chain listing are quite expensive.
- an integrated marketplace never answers to the users needs: Bulk listing, bulk buying, bulk cancelling, auctions, cheap to buy, sell, edit, cancel etc…
- separation of concerns
- erc721 is already a big contract by itself

You need a market contract that can evolve with the rest. Which is why you can’t really EIP marketplaces behaviors: the space is going to evolve. An interface that allows payment in erc20 is ok, but why not erc1155? Or another 721?

We want cheap to use. We want auctions. We want bulk actions. We want off-chain order books. We want…

This EIP would not answer the needs of the space, and might probably just do the opposite: lock us in one non-evolving scheme.

Note: seeing the idea of Blocklist in an EIP proposal really hurts.

About the royalties:

You can’t enforce them. You can’t block operators to interact with your contracts if they want to.

Blocklist, blocking transfers, etc… Can only hurt the space on the long run.

As creators, we need to accept that we lost the battle, at least on ethereum, and need to find new ways of doing things, not try to lock us, and our collectors /users, in the old ones.

---

**5cent-AI** (2023-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> any wrong implementation or bug was impossible to fix and can lead to a dead collection

This is exactly why we need to submit an eip.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> managing a marketplace is complicated and is actually problematic in some countries ( need trade license etc…)

If we are to discuss this issue within the legal framework of certain countries, then the current intermediary trading markets may not even be able to obtain local licenses. This is clearly not a problem that can be solved by technology alone. It may also go against the original intention of censorship resistance.

Furthermore, in most countries, not complying with project royalty schemes is actually illegal.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> on-chain listing are quite expensive

I believe that we should consider the overall cost. If we include the service fees paid in other trading markets in the transaction costs, we will find that the overall trading costs in other markets have been more expensive in the past. Additionally, if this EIP is applied to a Layer 2, then cost will not be an issue.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> an integrated marketplace never answers to the users needs: Bulk listing, bulk buying, bulk cancelling, auctions, cheap to buy, sell, edit, cancel etc…

This EIP aims to provide basic but flexible trading market functionality.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> Note: seeing the idea of Blocklist in an EIP proposal really hurts.

This EIP does not actually provide a standard blacklist function, but I personally believe that this is a power that developers could have. This power is to protect their interests from being harmed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> As creators, we need to accept that we lost the battle, at least on ethereum, and need to find new ways of doing things, not try to lock us, and our collectors /users, in the old ones.

We should consider what better changes Ethereum and the community can bring to the world. We should also think about what attracts creators to join. For creators, if smart contracts cannot better protect their interests, then the bright future of blockchain is no different from the bad past they have faced. We also have no reason to convince more creators to join us.

This industry needs more innovation, but the interests of everyone should be considered. Without the support of the honest and upright, innovation will not happen or may go in a bad direction.

---

**dievardump** (2023-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> This is exactly why we need to submit an eip.

Well… no. EIP is about giving an Interface, not implementing it. That’s why ERC2981 can do all the kind of royalties you mention: because the interface is flexible and the implementation is let to the implementers.

We have seen with the first ERC721A and other implementations of Enumerable using loops, people will do really bad code if they only have an interface.

Everyone will want to make their own implementation because they think other people’s code s**k or is not optimized and we will end up with code that leads to bug, front-running attacks, etc…

Fun fact: your proposal `function buyItem(uint256 tokenId) external payable;` is actually vulnerable to front-running attacks.

Someone can list an item from 0.1, watch the pool, and when they see a user calls `buyItem(tokenId)` they can front-run and up the price to 10eth if the user has enough in their wallet.

You **fulfill a given order** in a marketplace, you don’t just “buy an id”

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> Additionally, if this EIP is applied to a Layer 2, then cost will not be an issue.

Yes on a layer 2, but the EIP is for all E based contracts and for the moment, ETH is still the preferred one (and by far in term of valuable collectible/art). You yourself use “ETH” instead of “current chain native token” in your EIP comments

And even that, Layer 2 today are “cheaper” but nothing says they will always stay like this.

As long as the fees are paid with a token that has a price that can vary (which is the case for almost all of them, except Gnosis chain), there is nothing that says it will always stay cheap.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> This EIP aims to provide basic but flexible trading market functionality.

Not seeing any flexibility here. It’s expensive and hard to use. And it’s really basic yes. No bulk actions, no way to cancel absolutely all orders is a no go in the current state of our space. That’s how people trade.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> For creators, if smart contracts cannot better protect their interests, then the bright future of blockchain is no different from the bad past they have faced. We also have no reason to convince more creators to join us.

We need to incentivize creators and find solutions/alternatives, but what you propose here can not do that as it has been said and proven enough times that it is not really possible to do that with the current state of the chain and definitely not the way you propose: nor with an integrated marketplace (because not flexible, cheap or featured enough), nor with any kind of blocklist.

If a company  that makes $23m per months in fees wasn’t able to make a blocklist work, not sure who will.

Spreading the idea it can work is either lie to creators, or giving them false hopes.

Creators adapt. We’ve always been. If you tell us “it’s technically not possible” we try new things, we find new ways, we innovate.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> We should consider what better changes Ethereum and the community can bring to the world.

Bringing permissioned stuff like this is not what I would consider a “better change”.

---

**5cent-AI** (2023-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> Fun fact: your proposal function buyItem(uint256 tokenId) external payable; is actually vulnerable to front-running attacks.
> Someone can list an item from 0.1, watch the pool, and when they see a user calls buyItem(tokenId) they can front-run and up the price to 10eth if the user has enough in their wallet.

Thank you very much for your feedback. If there is such a problem, we can include it in `Security Considerations` or resolve it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> No bulk actions, no way to cancel absolutely all orders is a no go in the current state of our space. That’s how people trade.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> For example, taking BAYC as an example, with a total supply of 10,000 and over 6,000 current holders

You may often perform bulk actions and cancel absolutely all orders. However, for **most** NFT holders, they are not necessary functions as they do not hold a large quantity of NFTs.

As you mentioned, “ERC721 is already a big contract by itself,” so we cannot implement all functions in one contract. If you do require the aforementioned functions, you can implement them in other contracts such as aggregators, which does not conflict with the implementation of the EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> We need to incentivize creators and find solutions/alternatives

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> Creators adapt. We’ve always been.

In fact, a better royalty system was one of the ways we could incentivize creators to the crypto world. Now, you’re saying we should make them adapt to a situation without royalties, which is strange. Creators can have more choices, but the power of choice is in their hands. We just have been trying to provide them with more and better choices.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> Bringing permissioned stuff like this is not what I would consider a “better change”.

If you have an issue with the word “permission”,  then it cannot explain the fact that in both ERC20 and ERC721, only with our “permission” can someone transfer tokens from our account.

What we should distinguish is what is a good permission and what is a bad permission. Rather than thinking that permissions are bad. Good permissions are those that better protect the interests of participants.

It is still worth emphasizing that the blocklist is **optional**. This means that creators can decide for themselves, and it is not shameful for us to recognize that they have this power, nor can we prevent them from exercising it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> we try new things, we find new ways, we innovate

I hope more people will join. It will definitely bring about “better change”. ![:handshake:](https://ethereum-magicians.org/images/emoji/twitter/handshake.png?v=12)

---

**dievardump** (2023-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> we can include it in Security Considerations or resolve it.

You shouldn’t include this kind of vulnerabilities in security considerations. You should change the interface so the vulnerability does not exist. Especially one as big as that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> ERC721, only with our “permission” can someone transfer tokens from our account.

The approval is given by the NFT owner so they can interact with any protocol or even manage their assets from several wallets. It facilitates interoperability.

The blocklist is managed by the creator/contract owner, which is de facto biased by their own believes/interest, to block operators (which can include owner of the NFTs).

The first one is a delegation of rights by the rightful owner of the NFT, the second is a blockage by someone who shouldn’t have much rights on the NFT (at least not about transfers) once it’s not own by themselves.

It’s dangerous and yes it’s mentioned as optional, but the problem is that it is mentioned at all. Especially since it can not work.

---

**5cent-AI** (2023-03-01):

We’ll resolve it **and** mention it in the `Security Considerations`.

You think blocklist may not be desirable, but many creators have told that they need it. That’s why `optional blocklist` appears in the `Rationale`.

Our value preference should not influence the decision of creators, because we are not creators. They need it, they adopt it. They don’t need it, they don’t adopt it. This is the true meaning of “optional”. And whether it is effective should be judged by the creators.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> The blocklist is managed by the creator/contract owner, which is de facto biased by their own believes/interest, to block operators (which can include owner of the NFTs).

The style, pricing strategy, roadmap, and other aspects of NFT also reflect the interests and believes of creators and communities. We may choose not to purchase the NFTs that do not align with our interests and believes, but we should defend others’ rights to have their own interests and believes.

In addition, this issue can also be addressed through multi-signature.

---

**0x0** (2023-03-02):

### Mandatory, but more diverse royalty scheme

Mandatory royalty can only be realized by writing the NFT trading function into its own contract.

Meanwhile, a choice of A or B is better than a choice of have or nothing. By introducing the parameter `benchmarkPrice` in the `listItem` function, the `_salePrice` in the `royaltyInfo(uint256 _tokenId, uint256 _salePrice)` function in the ERC-2981 interface can be changed to `taxablePrice`, making the ERC-2981 royalty scheme more diverse. Here are several examples of royalty schemes:

`(address royaltyRecipient, uint256 royalties) = royaltyInfo(tokenId, taxablePrice)`

1. Value-added Royalty (VAR, royalties are only charged on the part of the seller’s profit）: taxablePrice=max(salePrice- historicalPrice, 0)
2. Sale Royalty (SR): taxablePrice=salePrice
3. Capped Royalty(CR): taxablePrice=min(salePrice, constant)
4. Quantitative Royalty(QR, each token trading pays a fixed royalties): taxablePrice= constant

---

**5cent-AI** (2023-03-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> Fun fact: your proposal function buyItem(uint256 tokenId) external payable; is actually vulnerable to front-running attacks.

`function buyItem(uint256 tokenId, uint256 salePrice, address supportedToken)`

Front-running attacks can be prevented by checking the `salePrice` and `supportedToken`.

---

**william1293** (2023-04-05):

These royalty schemes sound very interesting. Place visible ward.

