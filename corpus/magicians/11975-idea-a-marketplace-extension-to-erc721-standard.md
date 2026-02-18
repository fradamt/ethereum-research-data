---
source: magicians
topic_id: 11975
title: "Idea: A marketplace extension to ERC721 standard"
author: lambdalf-dev
date: "2022-12-01"
category: ERCs
tags: [nft, token, erc-721]
url: https://ethereum-magicians.org/t/idea-a-marketplace-extension-to-erc721-standard/11975
views: 1600
likes: 11
posts_count: 21
---

# Idea: A marketplace extension to ERC721 standard

**“Not your marketplace, not your royalties”**

OpenSea’s latest code snippet gives them the ability to entirely control which platform your NFTs can (or cannot) be traded on.

We propose to add basic marketplace functionality to the ERC721  standard to allow projects creators to gain back that control.

It includes:

~ a method to list an item for sale or update an existing listing, whether private sale (only to a specific address) or public (to anyone),

~ a method to delist an item that has previously been listed,

~ a method to purchase a listed item,

~ a method to view all items listed for sale, and

~ a method to view a specific listing.

This interface could also be adapted for ERC1155 standard, but might require adjustments

Edit:

This proposal is both compliant with OpenSea’s snippet and safe from it as it doesn’t need to make usage of the `transfer()`, `safeTransfer()`, and `approve()` functions.

This way, if OpenSea suddenly decided to completely block all other marketplaces, your internal marketplace can still operate.

## Replies

**offgridgecko** (2022-12-01):

Thank you Lambdalf for posting this.

---

**offgridgecko** (2022-12-01):

Would also add to this that the code as presented is compliant with the new snippet from opensea for their listing function, but collection-only marketplaces will not be affected if OpenSea were to choose to do something nefarious, because (and why) this code doesn’t affect approval and transferFrom protocols.

It therefore also leaves the devteam/founders to decide what kind of secure control they wish to implement over those functions to increase security of their collections and specify which marketplaces can/should be aloud to carry out 3rd party trading.

---

**lambdalf-dev** (2022-12-01):

right, I’ll update the initial post to reflect it better

---

**MilkyTaste** (2022-12-01):

Nice that this standard would work in tandem with [EIP-2981: NFT Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981)

Can the interfaces support sales in currencies other than ETH? e.g. I imagine a lot of projects would want to use their own utility token for sales.

---

**Pandapip1** (2022-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/milkytaste/48/7946_2.png) MilkyTaste:

> I imagine a lot of projects would want to use their own utility token for sales.

It wouldn’t be too hard for the purchase function to call uniswap and swap the ether for the correct number of tokens, and send back the excess.

---

**lambdalf-dev** (2022-12-01):

Yes, the interface doesn’t really care about the currency used, so if you want to use a different currency than the default chain token, make sure you add the address of the currency contract in your code, and use appropriate transfer on those tokens

---

**johnamcconnell** (2022-12-02):

Will the listing and delisting functionality be the same as an Opensea or anywhere else, meaning you have to sign and also pay gas in order to switch it on and off? I assume yes but I am asking just in case you might have did some wizardry where its simpler (and cheaper)

---

**MilkyTaste** (2022-12-02):

This implies the sale price is always pegged to ETH which they may not want. e.g. you might want to peg to USDC

---

**MilkyTaste** (2022-12-02):

This wouldn’t support multiple tokens when using the interface. Would we be able to sell one token for $APE and another for $ETH? for example

---

**MilkyTaste** (2022-12-02):

Think it would be valuable to include a deadline/expiry when listing an item for sale.

Sorry for multiple posts, I didn’t see the quote reply feature…

---

**Pandapip1** (2022-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/milkytaste/48/7946_2.png) MilkyTaste:

> This implies the sale price is always pegged to ETH which they may not want. e.g. you might want to peg to USDC

No, it doesn’t. Here is how it could work:

1. I send 0.1 ETH to buy an NFT
2. The marketplace calls uniswap to transform (for example) 0.0008 ETH into 1 USDC, leaving 0.0992 ETH.
3. That 1 USDC gets sent to the NFT’s owner.
4. The NFT is transferred.
5. The remaining 0.0992 ETH gets sent back to the original caller.

---

**offgridgecko** (2022-12-02):

To be clear, currently the purchase function is “payable” and thus is expecting an eth amount in our example code. However this is only the default listed idea. It could easily be modified with the same interface to allow payment via ERC20 token.

Other “purchase” functions can be added as needed to suit the intended functionality of your smart contract.

---

**offgridgecko** (2022-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> esn’t. Here is how it could work:
>
>
> I send 0.1 ETH to buy an NFT
> The marketplace calls uniswap to transform (for example) 0.0008 ETH into 1 USDC, leaving 0.0992 ETH.
> That 1 USDC gets sent to the NFT’s owner.
> The NFT is transferred.
> The remaining 0.0992 ETH gets sent back to the original caller.

I’m not writing that part, lol. Hate interfacing with swap contracts, but this is totally doable. Great idea as an optional upgrade. Maybe something like this can be added to our example code on GIT when we are ready, or a fork could be made.

---

**offgridgecko** (2022-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/johnamcconnell/48/7948_2.png) johnamcconnell:

> u have to sign and also pay gas in order to switch it on and off? I assume yes but I am asking just in case you might have did some wizardry where its simpler (and cheaper)

Gas is a thing, it’s always there, but there is no “setApprovalForAll()” required as you are interacting with the SC directly. The list and delist functions by themselves are quite small and easily manageable, gas costs should be minimal. Also listing again kills the previous listing, so if you want to change price or set so one wallet address only can purchase, it’s the same call to change the existing listing.

---

**lambdalf-dev** (2022-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/milkytaste/48/7946_2.png) MilkyTaste:

> Think it would be valuable to include a deadline/expiry when listing an item for sale.
>
>
> Sorry for multiple posts, I didn’t see the quote reply feature…

You’re good, discussion needs to be open and I’ve been doing some twitterspaces to discuss these issues.

I considered expiration, and agree it could be valuable, but left it out for simplicity. There is really nothing stopping someone from adding it to the base code that we are using for this standard. You would simply need to add some checks to the buy function as well as the data being pulled to your front end.

---

**1-om** (2023-01-09):

Cryptopunks, that precede the ERC721 standard itself, seem to have this idea in right direction, incorporating this model. Have a look at [cryptopunks/CryptoPunksMarket.sol at master · larvalabs/cryptopunks · GitHub](https://github.com/larvalabs/cryptopunks/blob/master/contracts/CryptoPunksMarket.sol)

However, this extension does not solve the royalty issue. It is correct that “if the sale is not on the in-built marketplace, then royalty is not guaranteed” but this does not ensure that sale is only via inbuilt marketplace.

---

**Pandapip1** (2023-01-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/1-om/48/7024_2.png) 1-om:

> However, this extension does not solve the royalty issue. It is correct that “if the sale is not on the in-built marketplace, then royalty is not guaranteed” but this does not ensure that sale is only via inbuilt marketplace.

That can be done via off-chain means (such as legal agreements).

---

**lambdalf-dev** (2023-01-12):

it doesn’t solve the entirety of the royalty issues, as long as you allow any marketplace to operate sales for you, but if you couple that with blocking transfer from 3rd parties, for example, then only your contract can handle sales, ensuring that all royalties are paid.

---

**5cent-AI** (2023-01-17):

If the NFT project is willing, it can set up a blacklist function to prevent NFT from being traded on all intermediary trading markets that do not charge copyright taxes.

On the other hand, I am also considering the rationality of copyright tax. IMHO, the copyright tax charged by many NFTs is too high, but it does not bring enough benefits to NFT holders.

In addition, we have also considered some new copyright tax schemes to adapt to different categories of NFT.

https://mirror.xyz/5660.eth/ymqq1CB7ALJYZe5StLeqo11jl6VBH9ztbhqpFQNTK_E

But I’m sorry that I haven’t translated it into English yet, so I have to suggest you use Google Translate or DeepL to read it.

---

**5cent-AI** (2023-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png)

      [Final: EIP-6105: No Intermediary NFT Trading Protocol With Mandatory and More Diverse Royalty Schemes](https://ethereum-magicians.org/t/no-intermediary-nft-trading-protocol/12171) [EIPs](/c/eips/5)




> No Intermediary NFT Trading Protocol With More Diverse Royalty Schemes
> Abstract
> Add a marketplace functionality to ERC-721 to enable non-fungible token trading without relying on an intermediary trading platform. At the same time, implement a mandatory, more diverse royalty scheme.
> Motivation
> Most current NFT trading relies on an NFT trading platform acting as an intermediary, which has the following problems:
>
> Security concerns arise from authorization via the setApprovalForAll function. The…

Here is some content, also can be used as a reference

