---
source: magicians
topic_id: 12017
title: "Idea: Extending the payable modifier to support multiple tokens beyond ETH"
author: jseam
date: "2022-12-04"
category: Magicians > Primordial Soup
tags: [token, smart-contracts, feedback-wanted]
url: https://ethereum-magicians.org/t/idea-extending-the-payable-modifier-to-support-multiple-tokens-beyond-eth/12017
views: 778
likes: 0
posts_count: 1
---

# Idea: Extending the payable modifier to support multiple tokens beyond ETH

Not sure if this needs to be an EIP but I’ll post the draft of ideas here. It might be better if it is a utility in some library. Would appreciate feedback and discussion around this.

There seems to be a need to create a consistent standard extending the payable modifier. This idea emerged when implementing a ERC1155 contract that needed to accept multiple types of tokens to mint a token. An analogy would be crafting items in Minecraft, where you need 3 x Item A, 1 x Item B, so on to mint an asset.

## Problems with the vanilla payable

Right now, the payable modifier on Ethereum supports only ETH or the network token if on another EVM chain. There is no consistent standard around paying a contract should there be a need to accept other token specifications like ERC20s, ERC721s, ERC1155s, and other future standards. This leads to a lack of consistency around how functions can get called on the UI or other contracts. Paying in ETH is different from paying in an ERC20.

Paying a contract in tokens is also not made explicit like how paying in ETH is like. This is most evident when interacting with contracts directly through libraries like ether.js, web3.js. Wallets like Metamask have a safeguard that makes you confirm transactions first and displaying asset transfers for ERC20s, however, this is not made explicit for ERC721s or ERC1155s. While approval functions were created as safeguards, most users would approve max ERC20, setApprovalForAll on ERC721 and ERC1155s out of convenience. While there would be malicious contracts that would not respect the payment values, this would still help users have agency over the amount transferred in benign contracts.

Beyond the lack of consistency around paying a contract, there’s a lack of a common interface for prices and assets that should be transferred. For example, a NFT mint function will typically check if `msg.value < 0.01 ether` for example. However, there’s no consistent interface around getting the price. This becomes a problem for account abstraction wallet providers which help onboard non-crypto natives. They may offer credit card payments for to abstract transactions. A user can pay directly in USD without buying tokens for gas. However, without the common interface such providers would then have to manually obtain values onchain or implement a complex parser and input the values on their metatransaction relayers.

## Draft of Proposed Implementation

Various abstract contracts for specific asset classes will be implemented that standardizes the transfer of assets. These can be inherited by child contracts. These should be backwards compatible with various smart contracts. However, what will change is how such payable functions be called on the frontends through libraries like ether.js or web3.js.

### Abstract Contracts for PayableERC20, PayableERC721, PayableERC1155

These should be inherited in the child contracts needing multiple payable tokens. Child contracts can then inherit the respective payable contracts for their needs.

```solidity
// SPDX-License-Identifier: AGPL-3.0

pragma solidity >=0.8.0 =0.8.0 =0.8.0 = 0.01 ether, "Insufficient eth");
        require(erc20Address == tempPrice[0].tokenAddress, "Wrong erc20 address");
        require(erc20Amount >= tempPrice[0].amount, "Insufficient erc20");
        require(erc721Address == tempPrice[1].tokenAddress, "Wrong erc721 address");
        require(erc721Id >= 0 , "Insufficient erc721");
        require(erc1155Address == tempPrice[2].tokenAddress, "Wrong erc1155 address");
        require(erc1155Id == tempPrice[2].id, "Wrong erc1155 id");
        require(erc1155Amount >= tempPrice[2].amount, "");
        _safeMint(msg.sender, tokenCount);
    }
}
```

## Backwards Compatibility

The extended payable contracts and IPrice interface are independent additions that could exist on any future contracts created.

## Related EIPs

[EIP-3589: Assemble assets into NFTs (ethereum.org)](https://eips.ethereum.org/EIPS/eip-3589): This is related as the transfer functions for ERC20s, ERC721s, ERC1155s is similar to how the extended payable modifiers should work.

[EIP-5606: Multiverse NFTs](https://eips.ethereum.org/EIPS/eip-5606): The extended payable modifier could also be useful for other EIP implementation that would like to compose multiple assets.
