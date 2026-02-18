---
source: magicians
topic_id: 11625
title: "Idea: Buy and Sell Limited Token (Feedback Appreciated)"
author: cvensand
date: "2022-11-05"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/idea-buy-and-sell-limited-token-feedback-appreciated/11625
views: 740
likes: 2
posts_count: 4
---

# Idea: Buy and Sell Limited Token (Feedback Appreciated)

Hi Ethereum Community! I wanted to get feedback on an idea for a new ERC token standard. The idea is to create a token that is limited to only being sold and bought on-chain and not allowed to be directly transferred between addresses.

**TLDR**

After exploring different token standards like [ERC-721](https://eips.ethereum.org/EIPS/eip-721), [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155) and [ERC-2981](https://eips.ethereum.org/EIPS/eip-2981) I could not find a suitable standard to guarantee that if an NFT token is resold the creator receives a portion of the resale value. [ERC-2981](https://eips.ethereum.org/EIPS/eip-2981) offers a standardized way to retrieve royalty payment information, however it does not provide a way to enforce this payment. Creating a new token standard that records sale price on-chain and limits the token to only being sold and bought would enable royalty payments to be collected without 3rd party involvement.

**Motivation:**

Digital marketplaces like the [Steam Community Market](https://steamcommunity.com/market/) are a great way for players to exchange in-game items and allow the developer (Valve in this case) to receive a portion of the resale. Having this marketplace provides a large amount of value to the players because they can trade with each other and value to the developer because they can use the fees as a way to continue developing the game.

However, these traditional centralized marketplaces have multiple problems.

1. You need to trust in a central 3rd party (Valve in my example)
2. You cannot take your money out of the marketplace after it has been deposited
3. Players use blackmarket trading sites to avoid resale fees

Current token standards allow organizations to create marketplaces that remove problems 1 and 2, but problem 3 is still unavoidable. By allowing addresses to freely transfer tokens we cannot assume the intention of a token transfer. The transfer could have been initiated for numerous reasons other than the sale of a token allowing bad actors to handle payments off-chain. This makes it impossible to collect resale fees without 3rd party involvement.

If it were possible to record sale price on-chain and remove the ability to directly transfer tokens, it would be possible to avoid problem 3. Every token sale could be handled by a smart contract that would properly distribute funds to the intended parties. If someone tried to sell their token for much less than what it was worth, potentially handling funds off-chain for the sale, they would not be able guarantee that the person they were working with could purchase the item. Anyone listening to the chain would be able to fill the order.

**Reference Implementation v0.1**

```auto
/// Emitted when the sell function is called
/// @param _from The address of the token owner
/// @param _tokenId The token type being transferred
/// @param _price The price offered to sell the token
event Sell(address indexed _from, uint256 _tokenId, uint256 _price);

/// Emitted when the buy function is called
/// @param _from The address of the token owner
/// @param _tokenId The token type being transferred
/// @param _price The price the token was sold for
event Buy(address indexed _from, uint256 _tokenId, uint256 _price);

/// Modifies the token to be for sale and sets the price
function sell(address indexed _seller, uint256 _tokenId, uint256 _price);

/// Transfers token to buyer, pays seller and modifies the token to not be for sale
function buy(address indexed _buyer, uint256 _tokenId, uint256 _price) external payable;

/// Returns if the token is for sale
function forSale() public view returns (bool)

/// Returns the price needed to buy the token
function price() public view returns (uint256)

/// Returns the token that can be used for payment
function acceptablePayment() public view returns (uint256 tokenId)

/// Returns the last price the token was sold for
function lastPrice() public view returns (uint256)

/// Finds the owner of the token
function ownerOf() external view returns (address);
```

[ERC-721](https://eips.ethereum.org/EIPS/eip-721) was referenced when creating this example.

**Outstanding thoughts:**

It seems like we would have to enforce what token the creator accepts as payment before it is minted. If we do not, then it would be easy to create a new ERC-20 token with no value and use it as payment for a sale.

**Next Steps:**

Thank you [@ChrisWong](/u/chriswong) for writing such a nice idea document that I could use as a template.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chriswong/48/7417_2.png)
    [Idea: P2P SoulBound Token (Call For A Better Name!)](https://ethereum-magicians.org/t/idea-p2p-soulbound-token-call-for-a-better-name/11262) [Primordial Soup](/c/magicians/primordial-soup/9)



> Hi Eth Magicians, I wanted to share some thoughts on a new pattern regarding ERC1155, or NFT that is 1.) non-transferrable (a.k.a soul bound) and can only be minted with signatures from all agreed addresses.
> TLDR
> Using ERC-1155 as a social footprint to represent interaction among a small set of addresses. When all participant agrees on such action, and provide the signatures; A mint can be initialised. Once minted, these tokens would be burnable, but not transferable.
> Motivation:
> Social inte…

## Replies

**magicintern** (2022-11-07):

Thank you for the detailed writeup this is my first attempt at asking questions to clarify things before I assume anything. Hopefully, this can translate into some good contributions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cvensand/48/7672_2.png) cvensand:

> Creating a new token standard that records the sale price on-chain and limits the token to only being sold and bought would enable royalty payments to be collected without 3rd party involvement.

So as an average user of NFTs, I can perform two of the following things:

1. I can sell it on the secondary market
2. Transfer it between my wallets for other reasons

For point 2, I don’t suppose there’s a way we can verify whether the transfer that happened was as part of a sale or not (if they don’t use marketplace and custom exchange contracts)

If those are the two events we’re trying to state and allow later if we need to know if it was a sale or transfer, can these two methods be combined under one name (it represents the same thing - a sale happened)

```auto
event Sell(address indexed _from, uint256 _tokenId, uint256 _price);
event Buy(address indexed _from, uint256 _tokenId, uint256 _price);
```

```auto
/// Emitted when a sale happens (bought or sold)
event Sale(address indexed _from, uint256 _tokenId, uint256 _price);
/// Transfer event that we already have in erc721
event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);
```

Not sure if this is the correct way to think about it.

---

**cvensand** (2022-11-10):

Hello! With this new token you would not be able to directly transfer it between wallets, so point 2 would not be possible.

You would be able to transfer this token indirectly by calling the `sell()` function. This function would change the `forSale` variable to `True` which would allow anyone on the network to call the `buy()` function to buy the token.

---

**magicintern** (2022-11-10):

Thank you for details

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cvensand/48/7672_2.png) cvensand:

> The idea is to create a token that is limited to only being sold and bought on-chain and not allowed to be directly transferred between addresses.

I should’ve reread this, but I get the point.

