---
source: magicians
topic_id: 12968
title: Minimalistic ERC721 Approvable Interface
author: sullof
date: "2023-02-18"
category: ERCs
tags: [nft, token, erc721]
url: https://ethereum-magicians.org/t/minimalistic-erc721-approvable-interface/12968
views: 893
likes: 15
posts_count: 9
---

# Minimalistic ERC721 Approvable Interface

Some projects require an interface to indicate whether a token is approvable, but not necessarily transferable. For instance, the Protector Protected Protocol (PPP) allows a Protector to own a protected vault that can contain NFTs, SFTs, and FTs. It’s too risky to allow exchanges to trade these vaults, but the owner of a Protector can still transfer it to other wallets.

In some cases, the owner can decide to trade it on an exchange and make it approvable.

To address this need, I’ve created an interface called IERC721Approvable that covers relevant use cases.

This interface is especially relevant for security tokens that restrict approvability for added protection. It defines several functions:

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

// Author: Francesco Sullo

interface IERC721Approvable {
   // UPDATED on March 16th, 2023

  // Must be emitted when the contract is deployed.
  event DefaultApprovable(bool approvable);

  // Must be emitted any time the status of a tokenId changes.
  event Approvable(uint256 indexed tokenId, bool approvable);

  // Returns true if the token is approvable.
  // It should revert if the token does not exist.
  function approvable(uint256 tokenId) external view returns (bool);

  // A contract implementing this interface should not allow
  // the approval for all. So, any actor validating this interface
  // should assume that the tokens are not approvable for all.

  // An extension of this interface may include info about the
  // approval for all, but it should be considered as a separate
  // feature, not as a replacement of this interface.
}

```

Given the increasing number of security-based NFTs that restrict approvability, I think it might be worthwhile to propose this interface as a standard.

Many people prioritize transferability when it comes to tokens, and I have proposed a minimalistic interface to facilitate this. However, the most critical factor to consider is whether a token is approvable. As the owner of a token, you know whether it is a collectible or soulbound, while exchanges and marketplaces do not have this knowledge. Therefore, before any transfer can take place, approval must be obtained. In my opinion, ensuring a token’s approvability is more important than simply checking its transferability.

What do you think?

## Replies

**sullof** (2023-02-18):

The implementation of PPP (in alpha stage) is at

https://github.com/ndujaLabs/protector-protected-protocol

---

**sullof** (2023-02-19):

I am probably going to create an EIP for it. Before doing it, it would be nice to see what is good, what is bad, if something is missed, etc.

---

**sullof** (2023-02-20):

After some exchange with other devs on other platforms, I realized that the function `makeApprovable` does not need to be part of the interface, since it is irrelevant for whoever checks the support of it. That would reduce the interface to

```auto
interface IERC721Approvable {

  event Approvable(uint256 indexed tokenId, bool approvable);

  function isApprovable(uint256 tokenId) external view returns (bool);

  function defaultApprovable() external pure returns (bool);
}
```

---

**sullof** (2023-02-20):

BTW, with this change, the interfaceId would change to `0xf98e5a0b`.

---

**Bizz** (2023-02-20):

Really important! By making it a standard, it will limit the risk of unintended transaction. Love what I see here!

---

**BUll1sh** (2023-02-20):

As use cases become more and more variable its defenetly beneficial when the processes for approvements become simplified!

---

**sullof** (2023-03-17):

The interface has evolved after the first implementations in a few projects. Now it has changed to

```auto
interface IERC721Approvable {

  event DefaultApprovable(bool approvable);

  event Approvable(uint256 indexed tokenId, bool approvable);

  function approvable(uint256 tokenId) external view returns (bool);

}
```

I updated the first post, to avoid that people read an old version. Thanks for all the feedback.

I have also made a proposal for a similar interface for Lockable ERC721 at



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png)
    [ERC-6982: Default Lockable Proposal](https://ethereum-magicians.org/t/erc721-lockable-proposal-with-default-status/13366) [Tokens](/c/tokens/18)



> Many proposals for lockable ERC721 contracts exist in different phases of development:
>
>
>
>
>
>
> and many others.
> Unfortunately, any of them misses something or is too complicated and add extra functions that do not need to be part of a standard.
> I tried to influence ERC-5192 making many comments and a PR that was closed by @Pandapip1 who suggested I make a new proposal. So, here we are.
> The updated Interface (based on comment and discussions):
> pragma solidity ^0.8.9;
>
> // ERC165 interfaceId 0x6…

---

**sullof** (2023-04-04):

I implemented the interface at


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/ndujaLabs/erc721subordinate/tree/main/contracts)





###



[main/contracts](https://github.com/ndujaLabs/erc721subordinate/tree/main/contracts)



An NFT which is subordinate to a primary NFT. Contribute to ndujaLabs/erc721subordinate development by creating an account on GitHub.

