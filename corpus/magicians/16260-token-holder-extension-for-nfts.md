---
source: magicians
topic_id: 16260
title: Token Holder Extension for NFTs
author: stoicdev0
date: "2023-10-25"
category: Magicians > Primordial Soup
tags: [nft, token, erc-721, erc-20]
url: https://ethereum-magicians.org/t/token-holder-extension-for-nfts/16260
views: 2230
likes: 3
posts_count: 9
---

# Token Holder Extension for NFTs

## We are proposing a token holder extension for NFTs.

## eip: 7590
title: ERC-20 Holder Extension for NFTs
description: Extension to allow NFTs to receive and transfer ERC-20 tokens.
author: Steven Pineda (@steven2308), Jan Turk ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2024-01-05
requires: 20, 165, 721

## Abstract

This proposal suggests an extension to ERC-721 to enable easy exchange of ERC-20 tokens. By enhancing ERC-721, it allows unique tokens to manage and trade ERC-20 fungible tokens bundled in a single NFT. This is achieved by including methods to pull ERC-20 tokens into the NFT contract to a specific NFT, and transferring them out by the owner of such NFT. A transfer out nonce is included to prevent front-running issues.

## Motivation

In the ever-evolving landscape of blockchain technology and decentralized ecosystems, interoperability between diverse token standards has become a paramount concern. By enhancing ERC-721 functionality, this proposal empowers non-fungible tokens (NFTs) to engage in complex transactions, facilitating the exchange of fungible tokens, unique assets, and multi-class assets within a single protocol.

This ERC introduces new utilities in the following areas:

- Expanded use cases
- Facilitating composite transactions
- Market liquidity and value creation

### Expanded Use Cases

Enabling ERC-721 tokens to handle various token types opens the door to a wide array of innovative use cases. From gaming and digital collectibles to decentralized finance (DeFi) and supply chain management, this extension enhances the potential of NFTs by allowing them to participate in complex, multi-token transactions.

### Facilitating Composite Transactions

With this extension, composite transactions involving both fungible and non-fungible assets become easier. This functionality is particularly valuable for applications requiring intricate transactions, such as gaming ecosystems where in-game assets may include a combination of fungible and unique tokens.

### Market Liquidity and Value Creation

By allowing ERC-721 tokens to hold and trade different types of tokens, it enhances liquidity for markets in all types of tokens.

## Specification

```solidity
interface IERC7590 /*is IERC165, IERC721*/  {
    /**
     * @notice Used to notify listeners that the token received ERC-20 tokens.
     * @param erc20Contract The address of the ERC-20 smart contract
     * @param toTokenId The ID of the token receiving the ERC-20 tokens
     * @param from The address of the account from which the tokens are being transferred
     * @param amount The number of ERC-20 tokens received
     */
    event ReceivedERC20(
        address indexed erc20Contract,
        uint256 indexed toTokenId,
        address indexed from,
        uint256 amount
    );

    /**
     * @notice Used to notify the listeners that the ERC-20 tokens have been transferred.
     * @param erc20Contract The address of the ERC-20 smart contract
     * @param fromTokenId The ID of the token from which the ERC-20 tokens have been transferred
     * @param to The address receiving the ERC-20 tokens
     * @param amount The number of ERC-20 tokens transferred
     */
    event TransferredERC20(
        address indexed erc20Contract,
        uint256 indexed fromTokenId,
        address indexed to,
        uint256 amount
    );

    /**
     * @notice Used to retrieve the given token's specific ERC-20 balance
     * @param erc20Contract The address of the ERC-20 smart contract
     * @param tokenId The ID of the token being checked for ERC-20 balance
     * @return The amount of the specified ERC-20 tokens owned by a given token
     */
    function balanceOfERC20(
        address erc20Contract,
        uint256 tokenId
    ) external view returns (uint256);

    /**
     * @notice Transfer ERC-20 tokens from a specific token.
     * @dev The balance MUST be transferred from this smart contract.
     * @dev MUST increase the transfer-out-nonce for the tokenId
     * @dev MUST revert if the `msg.sender` is not the owner of the NFT or approved to manage it.
     * @param erc20Contract The address of the ERC-20 smart contract
     * @param tokenId The ID of the token to transfer the ERC-20 tokens from
     * @param amount The number of ERC-20 tokens to transfer
     * @param data Additional data with no specified format, to allow for custom logic
     */
    function transferHeldERC20FromToken(
        address erc20Contract,
        uint256 tokenId,
        address to,
        uint256 amount,
        bytes memory data
    ) external;

    /**
     * @notice Transfer ERC-20 tokens to a specific token.
     * @dev The ERC-20 smart contract must have approval for this contract to transfer the ERC-20 tokens.
     * @dev The balance MUST be transferred from the `msg.sender`.
     * @param erc20Contract The address of the ERC-20 smart contract
     * @param tokenId The ID of the token to transfer ERC-20 tokens to
     * @param amount The number of ERC-20 tokens to transfer
     * @param data Additional data with no specified format, to allow for custom logic
     */
    function transferERC20ToToken(
        address erc20Contract,
        uint256 tokenId,
        uint256 amount,
        bytes memory data
    ) external;

    /**
     * @notice Nonce increased every time an ERC20 token is transferred out of a token
     * @param tokenId The ID of the token to check the nonce for
     * @return The nonce of the token
     */
    function erc20TransferOutNonce(
        uint256 tokenId
    ) external view returns (uint256);
}
```

## Rationale

### Pull Mechanism

We propose using a pull mechanism, where the contract transfers the token to itself, instead of receiving it via “safe transfer” for 2 reasons:

1. Customizability with Hooks. By initiating the process this way, smart contract developers have the flexibility to execute specific actions before and after transferring the tokens.
2. Lack of transfer with callback: ERC-20 tokens lack a standardized transfer with callback method, such as the “safeTransfer” on ERC-721, which means there is no reliable way to notify the receiver of a successful transfer, nor to know which is the destination token is.

This has the disadvantage of requiring approval of the token to be transferred before actually transferring it into an NFT.

### Granular vs Generic

We considered 2 ways of presenting the proposal:

1. A granular approach where there is an independent interface for each type of held token.
2. A universal token holder which could also hold and transfer ERC-721 and ERC-1155.

An implementation of the granular version is slightly cheaper in gas, and if you’re using just one or two types, it’s smaller in contract size. The generic version is smaller and has single methods to send or receive, but it also adds some complexity by always requiring Id and amount on transfer methods. Id not being necessary for ERC-20 and amount not being necessary for ERC-721.

We also considered that due to the existence of safe transfer methods on both ERC-721 and ERC-1155, and the commonly used interfaces of `IERC721Receiver` and `IERC1155Receiver`, there is not much need to declare an additional interface to manage such tokens. However, this is not the case for ERC-20, which does not include a method with a callback to notify the receiver of the transfer.

For the aforementioned reasons, we decided to go with a granular approach.

## Backwards Compatibility

No backward compatibility issues found.

## Test Cases

Tests are included in [erc7590.ts](https://eips.ethereum.org/assets/eip-7590/test/erc7590.ts).

To run them in terminal, you can use the following commands:

```auto
cd ../assets/eip-erc7590
npm install
npx hardhat test
```

## Reference Implementation

See [ERC7590Mock.sol](https://eips.ethereum.org/assets/eip-7590/contracts/ERC7590Mock.sol).

## Security Considerations

The same security considerations as with ERC-721 apply: hidden logic may be present in any of the functions, including burn, add resource, accept resource, and more.

Caution is advised when dealing with non-audited contracts.

Implementations MUST use the message sender as from parameter when they are transferring tokens into an NFT. Otherwise, since the current contract needs approval, it could potentially pull the external tokens into a different NFT.

To prevent a seller from front running the sale of an NFT holding ERC-20 tokens to transfer out such tokens before a sale is executed, marketplaces MUST beware of the `erc20TransferOutNonce` and revert if it has changed since listed.

ERC-20 tokens that are transferred directly to the NFT contract will be lost.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**CASABECI** (2023-10-27):

Hello,

How can I help or How can be forward this opportunity?

Thanks a lot for the support.

Kindly regards,

Juan David

---

**stoicdev0** (2023-10-27):

It would be great if you shared your thoughts on Pull vs Push for 721s and 1155s, and on Granular vs Generic.

Also, if you have any suggestions on the proposed methods or events

---

**0xASK** (2024-02-05):

Hey appreciate the post

Can you help me understand the specific pros / cons of the above proposal as you see it in relation to token bound accounts enabled by 6551?

---

**stoicdev0** (2024-02-05):

Sure!

Pros of 6551:

- It is wider, not only meant to accept ERC-20s but other stuff too
- Backwards compatible, works with existing collections.

Pros of 7590:

- It is very simple, focused only a specific funcionality.
- You do not need to care about registries or implementations, just add these methods to your contract.

---

**dievardump** (2024-02-05):

I don’t think it’s needed. 6551 is way more fitted to add balance holding for an NFT, whatever your usecase is.

I would rather see a publicly available implementation of a 6551-compatible contract that allows only to receive and send ERC20s. Public good, retroactive, less open to errors when calculating balances (which your example contract are vulnerable to).

This EIP is too verbose and adds too many functions to a standard (721) that is already too big, while not solving a problem that can’t be solved (in a better way) with existing standards (6551).

It will also be way more costly to use (every time the ERC20 transfer will force update of the contract balance + reads and writes to update nft balance for said token, double work for nothing) and quite complicated to make right (for example you can’t trust amounts passed as parameters, you always need to check balance before and after calling transfer/transferFrom because some ERC20 have tax on transfer, the amount received by recipient is not the same taken out of sender balance etc…), where a TBA account wouldn’t need all this.

---

**stoicdev0** (2024-02-29):

What you mention of 6551 solving this problem better is an opinion. There are use cases where this is just simpler.

Regarding the ERC20s with tax on transfer, this was a great catch, thanks! I have added the needed checks on the example implementation and on security considerations as well.

Edit: I originally mentioned that TBAs could not have on receive logic but they can in deed.

---

**dievardump** (2024-03-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> which would not be possible with TBAs.

onERC721Received? onERC1155Received? onERC1155BatchReceived?

You can put any code in it to execute custom logic on send to, just put your own function to send away from it.

A TBA is a contract, it can do all that.

---

**stoicdev0** (2024-03-08):

Good point, I corrected my previous comment. My point on simplicity stands.

