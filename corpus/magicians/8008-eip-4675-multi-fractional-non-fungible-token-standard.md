---
source: magicians
topic_id: 8008
title: "EIP-4675: Multi-Fractional Non-Fungible Token Standard"
author: DavidKim
date: "2022-01-16"
category: EIPs
tags: [erc, nft, token]
url: https://ethereum-magicians.org/t/eip-4675-multi-fractional-non-fungible-token-standard/8008
views: 3348
likes: 1
posts_count: 6
---

# EIP-4675: Multi-Fractional Non-Fungible Token Standard

Hi everyone, this is the discussions issue to discuss the newly propose EIP regarding Multi-Fractional Non-Fungible Token Standard.

[EIP-4675](https://github.com/ethereum/EIPs/pull/4675)

This EIP was proposed to minimize redundant bytecode on the Ethereum blockchain by not having to deploy ERC-20 contract every time when fractionalizing an NFT.

EIP-4675 is similar to the ERC-1155 token regarding `_id` distinguishing each token type, but different since each `_id` represents a distinct NFT.

By calling `setParentNFT()` the contract verifies the ownership of NFT and adds a new token type.

This is the reference implementation with a full-coverage test.

[Implementation](https://github.com/PowerStream3604/multi-fnft)

Please, share your thoughts freely.

Thank you.

## Replies

**SamWilsn** (2022-01-24):

Is there a front-running concern with `setParentNFT`?

For example, I send `CoolNft #442` to the `MFNFT` contract, then I call `setParentNFT(CoolNft, 442, 100)`.

Before my transaction is included, some third party calls `setParentNFT(CoolNft, 442, 1)`.

---

Would it make more sense to write this EIP as a direct extension of [EIP-1155](https://eips.ethereum.org/EIPS/eip-1155)?

```auto
interface MFNFT is IERC1155 {
    /**
        @notice Sets the NFT as a new type token
        @dev The contract itself should verify if the ownership of NFT is belongs to this contract itself with the `_parentNFTContractAddress` & `_parentNFTTokenId` before adding the token.
        MUST revert if the same NFT is already registered.
        MUST revert if `_parentNFTContractAddress` is address zero.
        MUST revert if `_parentNFTContractAddress` is not ERC-721 compatible.
        MUST revert if this contract itself is not the owner of the NFT.
        MUST revert on any other error.
        MUST emit `TokenAddition` event to reflect the token type addition.
        @param _parentNFTContractAddress    NFT contract address
        @param _parentNFTTokenId            NFT tokenID
        @param _totalSupply                 Total token supply
    */
    function setParentNFT(address _parentNFTContractAddress, uint256 _parentNFTTokenId, uint256 _totalSupply) external;

    /**
        @notice Get the bool value which represents whether the NFT is already registered and fractionalized by this contract.
        @param _parentNFTContractAddress    NFT contract address
        @param _parentNFTTokenId            NFT tokenID
        @return                             The bool value representing the whether the NFT is already registered.
    */
    function isRegistered(address _parentNFTContractAddress, uint256 _parentNFTTokenId) external view returns (bool);
}
```

---

**DavidKim** (2022-01-25):

That’s a good point. To prevent front-running issue the reference implementation includes `onlyAdmin()` modifier to only let the **admin** call the `setParentNFT()`. I also agree that notifying developers to consider front-running issues is a must!

The only point of sameness with ERC-1155 is that this token standard uses `_id` to distinguish different token types. This token standard includes NFT ownership verification and many other features to receive and fractionalize the NFT.

So, I considered it better to be a separate token standard.

---

**SamWilsn** (2022-01-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidkim/48/13667_2.png) DavidKim:

> That’s a good point. To prevent front-running issue the reference implementation includes onlyAdmin() modifier to only let the admin call the setParentNFT(). I also agree that notifying developers to consider front-running issues is a must!

Interesting. I assumed the owner who deposited the NFT would initially receive all of the fractionalized tokens and get to set the `totalSupply`, not an admin.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidkim/48/13667_2.png) DavidKim:

> The only point of sameness with ERC-1155 is that this token standard uses _id to distinguish different token types. This token standard includes NFT ownership verification and many other features to receive and fractionalize the NFT.

I’m not sure what you mean exactly. Doesn’t the MFNFT also inherit all the functions for transferring, querying balance, etc?

---

**julesl23** (2022-01-26):

In my opinion just have an extension to ERC-1155 as suggested by [@SamWilsn](/u/samwilsn)

The simpler, the more chance for adoption. There’s a whole bunch of duplication to ERC-1155 anyway, like the transfer functions and balances of multi tokens etc.

---

**DavidKim** (2022-02-13):

1. In the case of the reference implementation, only admin has the right to fractionalize the token.
However, it would definitely depend on the implementation. We could also open the possibilities for projects to implement it by handling transfer & fractionalization in an atomic transaction. (all possibilities are open).
2. Yeah(also for ERC-20), but I think that it would be worth mentioning the other capabilities of NFT fractionalization on top of ERC-1155.

