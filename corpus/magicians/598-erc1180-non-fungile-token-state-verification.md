---
source: magicians
topic_id: 598
title: "ERC1180: Non-Fungile Token State Verification"
author: mg6maciej
date: "2018-06-26"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc1180-non-fungile-token-state-verification/598
views: 707
likes: 0
posts_count: 1
---

# ERC1180: Non-Fungile Token State Verification

Hello everybody,

Looking for feedback on this:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1180)












####



        opened 05:47AM - 24 Jun 18 UTC



          closed 06:13AM - 19 Dec 21 UTC



        [![](https://avatars.githubusercontent.com/u/1316369?v=4)
          mg6maciej](https://github.com/mg6maciej)





          stale







Motivation
======

This is to start a discussion on **secure** exchange of NF[…]()Ts, as there are potential problems with front running, where seller can change state of token (and lower its value) before buy transaction is added to blockchain.

Details & Implementation
======

While what we really own is a unique number known as tokenId in a namespace of certain contract, often it's something else that makes us want to own that number. Many tokens have state we look at when buying them, be it a number of won/lost battles by a bot, how many children a token currently has or if a kitty owns some awesome hats or balloons.

Such state can easily change between order fill transaction is sent to miners and mined, so for the benefit of users buying these numbers, it would be good to allow them to specify state they care about and fail order fill tx if their desired state is changed. This is particularly useful for protocols that do not escrow tokens like 0x or wyvern.

As this state can often live outside of the original NFT contract, I propose the following interface:

```solidity
interface StateHashHolder {

    function getStateHash(address nftContractAddr, uint tokenId) external view returns (bytes32);
}
```

The composed hash that is checked against would be a XOR of all hashes:

```solidity
contract StateHashVerifier {

    function calculateStateHash(address nftContractAddr, uint tokenId, StateHashHolder[] holder) public view returns (bytes32 hash) {
        for (uint i = 0; i < holder.length; i++) {
            hash ^= holder[i].getStateHash(nftContractAddr, tokenId);
        }
    }
}
```

This is compatible with currently deployed NFTs, as they could implement `StateHashHolder` via separate contract.

Here is how it could be implemented for CryptoKitties "virginity":

```solidity
interface CryptoKitties {

    function getKitty(uint256 _id) external view returns (
        bool isGestating,
        bool isReady,
        uint256 cooldownIndex,
        uint256 nextActionAt,
        uint256 siringWithId,
        uint256 birthTime,
        uint256 matronId,
        uint256 sireId,
        uint256 generation,
        uint256 genes
    );
}

contract CryptoKittiesStateHash is StateHashHolder {

    function getStateHash(address nftContractAddr, uint tokenId) external view returns (bytes32) {
        if (nftContractAddr != 0x06012c8cf97BEaD5deAe237070F9587f8E7A266d) {
            return 0;
        }
        CryptoKitties cryptoKitties = CryptoKitties(nftContractAddr);
        (,,, uint nextActionAt,,,,,,) = cryptoKitties.getKitty(tokenId);
        // nextActionAt (aka cooldownEndBlock) changes every time you breed a pair of kitties
        return keccak256(abi.encodePacked(nextActionAt));
    }
}
```

Do you see any other use-cases apart from when exchanging NFTs?












Cheers,

Maciej
