---
source: magicians
topic_id: 10402
title: "Idea: Forced NFT Royalties"
author: osaka-toni-thomas
date: "2022-08-16"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/idea-forced-nft-royalties/10402
views: 866
likes: 0
posts_count: 2
---

# Idea: Forced NFT Royalties

Currently NFT royalties can not be enforced. Implementing royalties is optional for marketplaces.

I’m preparing a proposal for a novel mechanism which would enable compulsory royalties on NFT sales. Based on standardising the “Harberger tax” on ERC721.

I want to gauge community feedback

**Motivation:**

Royalties on NFT sales are currently optional. Marketplaces can choose whether or not they honour royalties. EIP-2981 created a common standard for recommending royalty information but has no way to enforce it.

This is leading to marketplaces not honouring royalties, which removes the incentives for NFT creators and communities to build value for their holders. Requiring the trust of marketplaces to implement royalties goes against the trustless nature of decentralisation.

**Proposed Solution**

A new standard would work as follows:

- Owners are able to set a sale price for the specific token on the ERC721 Contract
- Anyone is able to buy() the token at the listed price
- This is the only mechanism by which tokens can be transferred

**Solution Explanation**

In order for the owner to transfer a token, they must set a sale price they are willing to sell. This forces the transfer to take place in the ERC721 contract, meaning that the royalty split can be determined by the contract itself. If a marketplace tried to wrap the contract and transfer for a low price to circumvent royalties, the token could be sniped by someone else for that low price.

*Note: The implementation of `buy()` would need to check that `sell()` is not in the same transaction.*

```auto
interface IERCX {

     /**
     * @notice Function for the owner to set the automatic sell price for the token
     * @param amount to sell the token for
     **/
    function sell( uint256 amount ) external;

     /**
     * @notice Function to buy the token at the given price
     **/
    function buy() payable external;

     /**
     * @notice Function to get the current price to buy
     * @returns price to buy the token for
     **/
    function price() external view returns ( uint256 price );
}
```

**Questions for the community**

- Should the basic sale mechanism be standardised ERC721 contracts?
- What problems do you foresee with this model?

## Replies

**zapaz** (2022-08-18):

Hi [@osaka-toni-thomas](/u/osaka-toni-thomas),

Interesting proposal !   As at [Kredeum](https://www.kredeum.com) we are currently developing an AutoMarket ERC721 component, that allows what you describe, with some additionnal features.

Draft code there : https://github.com/Kredeum/OpenNFTs/blob/main/contracts/templates/OpenAutoMarket.sol

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/osaka-toni-thomas/48/6845_2.png) osaka-toni-thomas:

> Questions for the community
>
>
> Should the basic sale mechanism be standardised ERC721 contracts?

Not sure for Sell and Buy , as Mint and Burn are already not standardized

whereas Price(), i.e. getting NFT Price, could be standardized, as an extension of ERC2981

To enforce payment, this should (has to ?) be done via transferFrom functions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/osaka-toni-thomas/48/6845_2.png) osaka-toni-thomas:

> What problems do you foresee with this model?

How to enforce payments via standardisation ? you have to read the smarcontract to be sure of that!

Your can broaden the scope of your proposal : it can also be applied to all use cases with no royalties, to enforce NFT payment.

You could also include in your spec the minting price (and some events)

zapaz

