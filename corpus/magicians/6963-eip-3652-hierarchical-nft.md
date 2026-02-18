---
source: magicians
topic_id: 6963
title: "EIP-3652: Hierarchical NFT"
author: k06a
date: "2021-08-27"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-3652-hierarchical-nft/6963
views: 2652
likes: 8
posts_count: 22
---

# EIP-3652: Hierarchical NFT

EIP: [[WIP] EIP-3652: Introduce hierarchical NFT by k06a · Pull Request #3652 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/3652)

## Replies

**k06a** (2021-08-27):

We could use `CREATE2` to deploy proxies with `salt=tokenId`, this would allow to have same `tokenId` dimension of 32 bytes.

---

**Swader** (2021-08-28):

Just FYI we’re actively working on this and have recently launched our prototype of nestable, equippable, multi-resource NFTs at kanaria.rmrk.app - each bird is an NFT which can hold other NFTs and visually reacts to them by changing the render when they are equipped in specific slots, and each NFT can have specific alternative resources for different rendering (e.g. first 100 birds, owners can switch resource priority). This makes for interesting mechanics described [here](https://url.rmrk.app/rmrkcc). We’ll be building an EVM version of these RMRK standards in the coming months.

---

**k06a** (2021-08-30):

Updated example: [GitHub - 1inch/ERC3652](https://github.com/k06a/ERC3652)

Extracted `ERC3652Deployer` to a allow any existing ERC721 to have lazy ownership feature. Lazy means proxy contract could be deployed on demand of managing owned assets.

---

**sullof** (2023-05-01):

I am surprised that this conversation is not very alive because the proposal is very interesting and powerful. [@k06a](/u/k06a), I wonder if you guys have dropped it out or are working on an alternative. Any update?

---

**k06a** (2023-05-02):

Thx, we had some implementation, but I believe nowadays it could be even better: [GitHub - 1inch/ERC3652](https://github.com/1inch/ERC3652)

---

**k06a** (2023-05-02):

Would love to have someone ready to try this protocol out. Deprecation of SELFDESTRUCT would allow to use DELEGATECALL safely within proxy contracts

---

**sullof** (2023-05-03):

I am studying it to understand if it makes sense in a project on which I am working on. If so, I may implement it. One issue is the cost. I must find a way to keep the new deployed contract small enough to avoid excessive costs for the deployer. I was thinking of mixing it with [Diamonds](https://eips.ethereum.org/EIPS/eip-2535) so that the facets are deployed separately and are common. Another alternative is to use a registry to handle external contracts that manage the storage, etc.

But I am still not sure about it. Anyway, I will keep you posted.

---

**stoicdev0** (2023-05-03):

This EIP is closed but for anyone interested on hierarchical NFTs, there’s already: [ERC-6059: Parent-Governed Nestable Non-Fungible Tokens](https://eips.ethereum.org/EIPS/eip-6059), it allows multiple level of nesting an parent-child relationships can be created among any NFT collection implementing the interface.

---

**sullof** (2023-05-03):

I took a look at that and it defines a much more complex and structured scenario.

Also, I think that defining EIP-3652 as “Hierarchical NFT” is reducing its scope.

For example, I am considering to use it to create on-chain wallets associated to single NFTs, so that the owner of the NFT is the only one able to manage the wallet.

---

**stoicdev0** (2023-05-04):

Sounds a lot like what 6551 is doing, might wanna check.

---

**sullof** (2023-05-04):

I didn’t know that. Thanks for pointing out to it

---

**k06a** (2023-05-08):

[@stoicdev0](/u/stoicdev0) I saw bunch of hierarchical NFT EIP, they all struggle with non-compatibility with existing predeployed NFTs and it’s too complex in general which makes no sense to use it.

---

**k06a** (2023-05-08):

We could make proxies super cheap to deploy, moreover they could be deployed on demand.

---

**sullof** (2023-05-08):

ERC6551 is supposed to deploy very small contracts and being fully compatible with existing tokens too.

I would bet that they have seen your ERC and started their work from there.

---

**stoicdev0** (2023-05-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/k06a/48/1421_2.png) k06a:

> it’s too complex in general which makes no sense to use it.

This seems very short minded. If you want something which is specialized in Nesting NFTs, where can easily move through parents/children and have multiple levels, you can either deploy new contracts or wrap you existing one and use 6059. Several projects already do. If a contract owned by an NFT being able to receive NFTs is enough, then you go with 6551.

---

**sullof** (2023-05-11):

I would be careful in defining something short minded.

[@k06a](/u/k06a) motivation is very close to 6551’s authors one.

Also, the two protocols are very similar. 6551 just came much later than 3652, replicating the same approach.

---

**stoicdev0** (2023-05-12):

You’re right, apologies for the wording.

If they want to replicate the functionality with a simple interface, my only argument against is that it makes adoption harder when several EIPs address similar problems. I would just not discard other proposals because they seem “too complex”.

---

**k06a** (2023-05-15):

Upgraded proxy implementation with EVM bytecode for the best gas efficiency:



      [github.com](https://github.com/1inch/ERC3652/blob/master/contracts/ERC3652.sol)





####



```sol
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/Create2.sol";

contract ERC3652 {
    uint256 public constant PROXY_CODE_TOKEN_ADDRESS_BYTE_OFFSET = 77;
    uint256 public constant PROXY_CODE_TOKEN_ID_BYTE_OFFSET = 47;

    bytes public constant PROXY_CODE =
        // Universal constructor (11 bytes length)
        // codecopy(0, 0, codesize())
        hex"38"    // codesize
        hex"5f"    // push0
        hex"5f"    // push0
        hex"39"    // codecopy
        // return(13, sub(codesize(), 13))
        hex"60_0b" // push1 13
        hex"38"    // codesize
```

  This file has been truncated. [show original](https://github.com/1inch/ERC3652/blob/master/contracts/ERC3652.sol)










But delegatecall means proxy could be destroyed by SELFDESTRUCT intentionally or non-intentionally. But upcoming Ethereum hard fork Dencun gonna change SELFDESTRUCT opcode behavior to non-delete smart contract.

---

**sullof** (2023-05-16):

In this new implementation, to transfer, for example, an ERC721 from the proxied account to some address address, someone should just implement a `transferNft` function inside `TokenTransferDelegatee`, right?

---

**sullof** (2023-05-16):

In theory, a malicious TokenTransferDelegatee could implement the transfer function to execute code in the caller contract, included a self-destruct. Does it make sense?


*(1 more replies not shown)*
