---
source: magicians
topic_id: 8075
title: "EIP-721 vs. EIP-3074 / smart contract wallets: What will happen?"
author: axic
date: "2022-01-22"
category: EIPs > EIPs core
tags: [erc-721, account-abstraction, eip-3074]
url: https://ethereum-magicians.org/t/eip-721-vs-eip-3074-smart-contract-wallets-what-will-happen/8075
views: 1749
likes: 6
posts_count: 7
---

# EIP-721 vs. EIP-3074 / smart contract wallets: What will happen?

[EIP-721](https://eips.ethereum.org/EIPS/eip-721) has two functions for transfering ownership. The simple one is `transferFrom`:

```solidity
    /// @notice Transfer ownership of an NFT -- THE CALLER IS RESPONSIBLE
    ///  TO CONFIRM THAT `_to` IS CAPABLE OF RECEIVING NFTS OR ELSE
    ///  THEY MAY BE PERMANENTLY LOST
    /// @dev Throws unless `msg.sender` is the current owner, an authorized
    ///  operator, or the approved address for this NFT. Throws if `_from` is
    ///  not the current owner. Throws if `_to` is the zero address. Throws if
    ///  `_tokenId` is not a valid NFT.
    /// @param _from The current owner of the NFT
    /// @param _to The new owner
    /// @param _tokenId The NFT to transfer
    function transferFrom(address _from, address _to, uint256 _tokenId) external payable;
```

As expected, this just changes the associated owner.

However `safeTransferFrom` is a bit more tricky:

```solidity
    /// @notice Transfers the ownership of an NFT from one address to another address
    /// @dev Throws unless `msg.sender` is the current owner, an authorized
    ///  operator, or the approved address for this NFT. Throws if `_from` is
    ///  not the current owner. Throws if `_to` is the zero address. Throws if
    ///  `_tokenId` is not a valid NFT. When transfer is complete, this function
    ///  checks if `_to` is a smart contract (code size > 0). If so, it calls
    ///  `onERC721Received` on `_to` and throws if the return value is not
    ///  `bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"))`.
    /// @param _from The current owner of the NFT
    /// @param _to The new owner
    /// @param _tokenId The NFT to transfer
    /// @param data Additional data with no specified format, sent in call to `_to`
    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data) external payable;
```

The important part here is:

> When transfer is complete, this function checks if _to is a smart contract (code size > 0). If so, it calls onERC721Received on _to and throws if the return value is not bytes4(keccak256("onERC721Received(address,address,uint256,bytes)")).

This means a contract must opt-in, as opposed to opt-out, into receiving EIP-721 compatible tokens.

---

Once an EOA authorizes a contract with [EIP-3074](https://ethereum-magicians.org/t/eip-3074-auth-and-authcall-opcodes/4880), there are two ways such an address can interact with others:

1. As an EOA
2. Through a contract wallet

In both cases `msg.sender.code.length == 0`, but in the second case the safe transfer should check for `onERC721Received`. Happy side effect: EIP-3074 compatible contract wallets do not need to implement it.

Account Abstraction and [Smart Contract Wallet](https://ethereum-magicians.org/t/validation-focused-smart-contract-wallets/6603) solutions however are a bit more drastic, as some versions of them propose a *default* bytecode for EOAs. These default bytecodes are rather basic and do not deal with application layer standards. It would be weird just specifically supporting `onERC721Received` in them. This means they won’t be able to receive NFTs via “safe transfers”, and if every EOA has such an assumed code, then none of them can interact that way.

It is important to note that there is the “unsafe” `transferFrom` function for unchecked transfers, but various NFTs interpret the standard differently, and tooling / apps may have additional restrictions (such as only supporting “safe transfers”).

I do not have any proposal(s), only a discussion starter ![:grimacing:](https://ethereum-magicians.org/images/emoji/twitter/grimacing.png?v=12)

## Replies

**hrkrshnn** (2022-01-22):

Had a private conversation with [@axic](/u/axic) about following, but posting here anyway.

An EOA can authorize multiple contracts. So even when they receive the NFT, how can one say which contract it should do the `onERC721Received` check?

However, assuming that an EOA can delegate itself to a single contract, it is interesting if EVM allows obtaining this contract, and an EIP712 implementation doing the `onERC721Received` check on the contract instead of the EOA. With this, EOAs can prevent an ERC721 `safeTransfer` / `safeTransferFrom` / `safeMint` to its account. This is not a problem that needs to be solved, but makes an interesting design question.

---

**axic** (2022-01-22):

I wonder what is the reason 721 has this check though? Is it

1. for avoiding that tokens get locked up in contracts which can’t do anything with it?
2. or an attempt to avoid reentrancy attacks?

---

**MicahZoltu** (2022-01-23):

It is the former (1).

---

**Amxx** (2022-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> but in the second case the safe transfer should check for onERC721Received

I disagree with that.

AFAIK, the role of this check is to avoid sending ERC721 tokens to smart contract that would not support them, which would lock them indefinitely. If the msg.sender is an EOA, regardless of wether it operates directly, or using an EIP3074 forwarder, it ultimately has the possibility of recovering the NFT, either using a native transaction, or using another EIP3074 forwarder. There is IMO no risk of locking an NFT.

Am I missing something ?

---

**MicahZoltu** (2022-01-23):

I am of the opinion that the safe transfer check is a poor design.  I understand the desire to try to protect everyone from everything, but when those protections come with costs you must weigh the cost against the benefit.  In this case, the cost is extra gas and an incompatibility with a bunch of things including generalized contract wallets and upgrades like 3074.

Personally, I don’t think anyone should be using the safe transfer unless they are working in a closed system where there is a very strong expectation/requirement that the receiver implements the necessary functions.

---

**PhABC** (2022-01-24):

These callbacks are not just to avoid sending tokens to contract not supporting them.

Imo the main benefit is that it allows users to deposit/send tokens to contracts without the need to approve contracts, the latter being a security risk. Also means gas is cheaper and UX is better since you only have 1 tx instead of two.

