---
source: magicians
topic_id: 14502
title: Clustered NFT for sub-collections
author: sullof
date: "2023-05-30"
category: Magicians > Primordial Soup
tags: [nft, token, erc-721, sub-collections]
url: https://ethereum-magicians.org/t/clustered-nft-for-sub-collections/14502
views: 882
likes: 7
posts_count: 14
---

# Clustered NFT for sub-collections

For many developers eager to explore the NFT space, a significant barrier to entry is the substantial cost associated with deploying an NFT contract on the Ethereum blockchain. In periods of bullish market activity, deploying an ERC721 contract can cost thousands of dollars, which prevents many creators from realizing their unique collections.

While marketplaces like OpenSea have addressed this issue with the implementation of lazy-minting on their own collections, this is merely a workaround and not an optimal solution. A more comprehensive approach would be the deployment of a smart contract capable of managing multiple sub-collections, each with their unique name, symbol, tokenURI, and ownership. This not only allows for individual ownership, which enables token minting and royalty collection from marketplaces, but also allows the clusters to maintain their unique identity.

Additionally, this approach supports the creation of NFTs with a pure utility purpose that require an affiliation program. This interface also elegantly addresses the challenge of creating new collections within a family of NFTs, simplifying management and maintaining a clear hierarchy and organization.

I propose the following interface as a potential solution to these challenges:

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

// Authors: Francesco Sullo

/**
 * @title IClusteredERC721
 * @dev IClusteredERC721 interface allows managing clusters or sub-collections of ERC721 tokens within a single contract
    ERC165 InterfaceId = 0x8a7bc8c2
 */
interface IClusteredERC721 {
  /**
   * @dev Emitted when a new cluster is added
   */
  event ClusterAdded(uint256 indexed clusterId, string name, string symbol, string baseTokenURI, uint256 size, address owner);

  /**
   * @dev Emitted when ownership of a cluster is transferred
   */
  event ClusterOwnershipTransferred(uint256 indexed clusterId, address indexed previousOwner, address indexed newOwner);

  /**
   * @notice Gets the id of the cluster to which a token belongs
   * @param tokenId ID of the token
   * @return uint256 ID of the cluster to which the token belongs
   */
  function clusterOf(uint256 tokenId) external view returns (uint256);

  /**
   * @notice Gets the name of a cluster
   * @param clusterId ID of the cluster
   * @return string Name of the cluster
   */
  function nameOf(uint256 clusterId) external view returns (string memory);

  /**
   * @notice Gets the symbol of a cluster
   * @param clusterId ID of the cluster
   * @return string Symbol of the cluster
   */
  function symbolOf(uint256 clusterId) external view returns (string memory);

  /**
   * @notice Gets the range of token IDs that are included in a specific cluster
   * @param clusterId ID of the cluster
   * @return (uint256, uint256) Start and end of the token ID range
   */
  function rangeOf(uint256 clusterId) external view returns (uint256, uint256);

  /**
   * @notice Gets the owner of a cluster
   * @param clusterId ID of the cluster
   * @return address Owner of the cluster
   */
  function clusterOwner(uint256 clusterId) external view returns (address);

  /**
   * @notice Gets how many clusters have been added
   * @return uint256 Total number of clusters
   */
  function clustersCount() external view returns (uint256);

  /**
   * @notice Adds a new cluster
   * @dev The ClusterAdded event MUST be emitted upon successful execution
   * @param name Name of the cluster
   * @param symbol Symbol of the cluster
   * @param baseTokenURI Base Token URI of the cluster
   * @param size Size of the cluster (number of tokens)
   * @param clusterOwner Address of the cluster owner
   */
  function addCluster(
    string memory name,
    string memory symbol,
    string memory baseTokenURI,
    uint256 size,
    address clusterOwner
  ) external;

  /**
   * @notice Transfers ownership of a cluster
   * @dev The ClusterOwnershipTransferred event MUST be emitted upon successful execution
   * @param clusterId ID of the cluster
   * @param newOwner Address of the new owner
   */
  function transferClusterOwnership(uint256 clusterId, address newOwner) external;

  /**
   * @notice Gets the normalized token ID for a token
   * @dev The normalized token ID is the token ID within the cluster, starting from 1
   * @param tokenId ID of the token
   * @return uint256 Normalized token ID
   */
  function normalizedTokenId(uint256 tokenId) external view returns (uint256);
}

```

The interface is changing over time, based on comments and suggestions. To see latest version, refer to the PR at [Add EIP: Clustered ERC-721 by sullof · Pull Request #7108 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7108/files)

## Replies

**abcoathup** (2023-05-31):

## Deployment Cost

Devs/creators should deploy NFTs to Layer 2 if cost is an issue.

OpenSea supports Layer 2s such as Optimism & Arbitrum (One & Nova).

The Dencun upgrade with EIP4844 is going to lower the cost of Layer 2 transactions by an order of magnitude.

Onchain SVG NFTs and composable SVG NFTs are much more viable on Layer 2.

NFT marketplaces have already created their own internal mechanisms for identifying NFT collections in a single marketplace contract.  Without support of a large NFT marketplace, I am not convinced that this would get any adoption.

# NFT families

Having the ability to group NFT’s into a family sounds interesting, and something that could be worth exploring more.  An onchain mechanism to group NFTs together and show the relationship other than just the owner of the contract.

---

**sullof** (2023-05-31):

Creating collections on Layer 2 solutions, in theory, sounds like a good solution. However, in practice, it presents a significant challenge for ordinary users. The transition to Layer 2 can be cumbersome due to the necessary conversion of native tokens and other factors. This friction is why Layer 2 solutions are primarily used by DeFi projects and users, where the benefits outweigh the complexity.

Marketplaces each have their own strategies. For instance, if I create a collection on OpenSea and you buy a token, nobody can track what you do with that token outside of OpenSea. These custom solutions often result in centralization.

I believe that clustered NFTs could be a solution to many of these problems. I started pondering this issue while working on a protocol for purely utility-based NFTs. We found ourselves in need of a feature similar to clustered NFTs. Instead of creating a basic, customized version just for our needs, I decided it might be beneficial to generalize the concept, thereby addressing a broader range of issues.

---

**sullof** (2023-05-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> Having the ability to group NFT’s into a family sounds interesting, and something that could be worth exploring more. An onchain mechanism to group NFTs together and show the relationship other than just the owner of the contract.

A use case that is very common is that a game deploys a smart contract for a collection of in-game assets. Let’s say that initially is a collection of avatars. Later, the game adds a collection of lands. And later, castles. In the current system, the game will deploy three different smart contracts. Using a clustered NFT, that game can deploy a single contract and managing the three collections as completely independent. We would definitely use that in Byte City and Mobland if there is support from the community for this proposal or something similar.

---

**SanLeo461** (2023-05-31):

What kind of gas savings does this approach gain over something more simple or minimal such as an EIP-897 DelegateProxy?

Should consider not only deployment costs, but user costs for overhead of loading and working with these clusters vs the overhead a proxy implementation causes.

Seems like a lot of extra work for implementers and marketplaces to adopt this standard, when a more simple and universally compatible solution may exist.

---

**sullof** (2023-05-31):

I think that there are many different scenarios. In some case, using a proxy is a perfect solution, in other cases it may not be ideal. For example, if you are building assets for a game, you would have many advantages in deploying a single contract with all the logic and create new collections on that single contract.

I think that the marketplace example is not really important since, as I specified, they have their own solution for it, which works, however, only with their own created collections.

---

**sullof** (2023-05-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sanleo461/48/8998_2.png) SanLeo461:

> Seems like a lot of extra work for implementers and marketplaces to adopt this standard, when a more simple and universally compatible solution may exist.

I envision some well-audited clusters, maybe with specific features (lockable, on-chain attributes for games, etc.) that people can use to create their own collection.

Some other clusters will be used by specific project to optimize the management of their infrastructure.

In Cruna we will have a CrunaVault (which is technically an NFT) which will support affiliation. With a clustered NFT, the affiliate can mint its own range of tokens without affecting the rest of the tokens, and without risks of adding security issues if/when deploying a slightly different contract.

---

**SanLeo461** (2023-06-01):

The idea of user-based collections in games makes a lot more sense to me.

Some more feedback on the specification then, I think that since NFTs are often dynamic nowadays (especially with the points you made about metadata), it might make sense to either include Metadata change events, or an extension interface to allow these events to occur.

I think also the ownership specification should be made agnostic over the ownership implementation, that is, each cluster contract can have its own method of transferring ownership as long as the correct events are emitted on transfer. e.g. both the OpenZeppelin Ownable & Ownable2Step methods of transferring ownership (or even something like an ownership lock contract) should all be compliant.

---

**sullof** (2023-06-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sanleo461/48/8998_2.png) SanLeo461:

> The idea of user-based collections in games makes a lot more sense to me.

Thanks for pointing out.

When I wrote the clustered NFT for Cruna I didn’t think to the cost of deploying many ERC721 as a relevant feature. Later, when I extended the idea to a generic protocol, I considered that as an important factor and I started from it. But I think that there can be many other use cases that are more relevant and hard to solve with just using ERC721.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sanleo461/48/8998_2.png) SanLeo461:

> I think also the ownership specification should be made agnostic

What do you mean exactly? The interface specifies the function `transferClusterOwnership` just to be sure that an event is emitted when that changes. But the implementer can add more functions.

In suspect that in many implementations, the cluster owner will be the owner of the contract and they may ignore the parameter `clusterOwner_` in the addCluster function.

I will investigate more possible use-cases and add them to the ERC. BTW, I opened a PR for it at

https://github.com/ethereum/EIPs/pull/7108/files

---

**sullof** (2023-06-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sanleo461/48/8998_2.png) SanLeo461:

> I think also the ownership specification should be made agnostic over the ownership implementation, that is, each cluster contract can have its own method of transferring ownership as long as the correct events are emitted on transfer

I think you are right. The way the ownership is changed is irrelevant in the context of the interface specification. I removed that function, but will leave the event.



      [github.com](https://github.com/ethereum/EIPs/blob/35904d5cff7cce5cab2b827ada616aecc53ce441/EIPS/eip-7108.md)





####



```md
---
eip: 7108
title: Clustered ERC-721
description: Extend ERC-721 to allow for clusters of NFTs ad sub-collections
author: Francesco Sullo (@sullof)
discussions-to: https://ethereum-magicians.org/t/clustered-nft-for-sub-collections/14502
status: Draft
type: Standards Track
category: ERC
created: 2023-05-30
requires: 165, 721
---

## Abstract

A standard interface for contracts that manage clusters or sub-collections of [ERC-721](./eip-721) tokens within a single contract.

This EIP introduces a new standard interface for Ethereum contracts that manage multiple clusters or sub-collections of [ERC-721](./eip-721) tokens within a single contract. This allows the tokens to be grouped together in a way that maintains each group's distinct identity and metadata.

## Specification
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/35904d5cff7cce5cab2b827ada616aecc53ce441/EIPS/eip-7108.md)

---

**sullof** (2023-06-10):

Working on an advanced implementation inside Cruna protocol, I realized that in the current proposal there is no direct way to know how many tokens a wallet owns within a sub-collection. This could be solved adding a function like

```auto
  function balanceOfWithin(
    address owner,
    uint clusterId
  ) external view
    returns(uint);
```

But that can be implemented only if the token is enumerable. So, I may add a second interface like

```auto
interface ERC7108Enumerable {

  /**
   * @notice Retrieves the balance of tokens a wallet owns within a specific cluster
   * @dev The balance is the number of tokens owned by the caller within the specified cluster.
      Note that due to potential computational complexity, this function could be gas-intensive,
      and therefore should primarily be called from dApps rather than included in smart contract
      business logic. To avoid risks, this function could be implemented as 'external' so that
      the smart contract cannot call it internally.
   * @param tokenOwner the owner of the tokens
   * @param clusterId ID of the cluster
   * @return uint256 Balance of tokens within the cluster
   */
  function balanceOfWithin(address owner, uint clusterId) external view returns(uint);
}
```

What do you think?

---

**sullof** (2023-06-11):

I’ve made some updates to the proposal. In my view, there are instances where the `balanceOfWithin` function proves to be crucial. However, my uncertainty lies in whether its implementation should be mandated for every ERC7108 contract. If we decide to enforce it, this would require all clustered NFTs to possess some form of enumerability. This could potentially be a necessary step, but for the time being, I’ve decided to designate it as an extension.

---

**sullof** (2023-06-14):

I also added

```auto
  /**
   * @notice Gets the owner of a tokenId within a cluster
   * @param normalizedTokenId_ The normalized ID of the token
   * @param clusterId ID of the cluster
   * @return the address of the owner of the token, if it exists
   */
  function ownerOfWithin(uint256 normalizedTokenId_, uint256 clusterId) external view returns (address);
```

---

**sullof** (2023-06-27):

I am thinking of removing the `addCluster` function from the specification, leaving its implementation to the dev. In fact, there can be many possible ways to do so. As long as it emits the ClusterAdded event, it should be fine. Any thought about it?

