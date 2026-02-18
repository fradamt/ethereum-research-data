---
source: magicians
topic_id: 8924
title: "EIP-5007: EIP-721 Time Extension"
author: 0xanders
date: "2022-04-15"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5007-eip-721-time-extension/8924
views: 2789
likes: 8
posts_count: 10
---

# EIP-5007: EIP-721 Time Extension

---

## eip:
title: ERC-721 Time Extension
description: Add start time and end time to ERC-721 tokens.
author: Anders (), Lance (), Shrug
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2022-04-13
requires: 165, 721

## Abstract

This standard is an extension of ERC-721. It proposes some additional property( `startTime`, `endTime`,`originalTokenId`) to help with the on-chain time management.

## Motivation

Some NFTs have a defined usage period and cannot be used when they are not at a specific time. If you want to make NFT invalid when it is not in use period, or make NFT enabled at a specific time, while the NFT does not contain time information, you often need to actively submit the chain transaction, this process is both cumbersome and a waste of gas.

There are also some NFTs contain time functions, but the naming is different, third-party platforms are difficult to develop based on it.

By introducing (`startTime`, `endTime`) and unifying the naming, it is possible to enable and disable NFT automatically on chain.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY” and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

```solidity
interface ITimeNFT  {

    /// @notice Emitted when the `startTime` or `endTime` of a NFT is changed
    /// @param tokenId  The tokenId of the NFT
    /// @param startTime  The new start time of the NFT
    /// @param endTime  The new end time of the NFT
    event TimeUpdate(uint256 tokenId,uint64 startTime,uint64 endTime);

    /// @notice Get the start time of the NFT
    /// @dev Throws if `tokenId` is not valid NFT
    /// @param tokenId  The tokenId of the NFT
    /// @return The start time of the NFT
    function startTime(uint256 tokenId) external view returns (uint64);

    /// @notice Get the end time of the NFT
    /// @dev Throws if `tokenId` is not valid NFT
    /// @param tokenId  The tokenId of the NFT
    /// @return The end time of the NFT
    function endTime(uint256 tokenId) external view returns (uint64);

    /// @notice Get the token id which this NFT mint from
    /// @dev Throws if `tokenId` is not valid NFT
    /// @param tokenId  The tokenId of the NFT
    /// @return The token id which this NFT mint from
    function originalTokenId(uint256 tokenId) external view returns (uint256);

    /// @notice Check the NFT is valid now
    /// @dev Throws if `tokenId` is not valid NFT
    /// @param tokenId  The tokenId of the NFT
    /// @return The the NFT is valid now
    /// if(startTime  {

    it("test TimeNFT", async () => {
        // Get initial balances of first and second account.
        const Alice = accounts[0];
        const Bob = accounts[1];

        const instance = await TimeNFTDemo.deployed("TimeNFTDemo", "TimeNFTDemo");
        const demo = instance;

        let now = Math.floor(new Date().getTime()/1000);
        let startTime = now ;
        let endTime = now + 10000;
        let newStartTime = startTime + 2000;

        let id1 =  await demo.mint(Alice,start, endTime);
        let isValidNow =   await demo.isValidNow(id1);

        assert.equal(
            isValidNow,
            true,
            "token id1 should be valid now"
        );

        let id2 =  await demo.split(id1,newStartTime, Bob);

        let owner2 = await demo.ownerOf(id2);
        assert.equal(
            owner2,
            Bob ,
            "Owner of NFT 2 should be Bob"
        );

        let id3 =  await demo.mint(Alice,1, 2);
        let isValidNow3 = await demo.isValidNow(id3);

        assert.equal(
            isValidNow3,
            false,
            "token id3 should be not valid now"
        );
    });
});
```

## Reference Implementation

```solidity
pragma solidity 0.8.10;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./ITimeNFT.sol";

contract TimeNFT is ERC721, ITimeNFT  {

    struct TimeNftInfo {
        uint256 originalTokenId;
        uint64 startTime;
        uint64 endTime;
    }

    uint256 private _nextTokenId = 1;

    mapping(uint256 /* tokenId */ => TimeNftInfo) internal _timeNftMapping;

    constructor(string memory name_, string memory symbol_)ERC721(name_, symbol_){
    }

    /// @notice Get the start time of the token
    /// @dev Throws if `tokenId` is not valid token
    /// @param tokenId  The tokenId of the token
    /// @return The start time of the token
    function startTime(uint256 tokenId) public view virtual override returns (uint64) {
        require(_exists(tokenId),"invalid tokenId");
        return _timeNftMapping[tokenId].startTime;
    }

    /// @notice Get the end time of the token
    /// @dev Throws if `tokenId` is not valid token
    /// @param tokenId  The tokenId of the token
    /// @return The end time of the token
    function endTime(uint256 tokenId) public view virtual override returns (uint64) {
        require(_exists(tokenId),"invalid tokenId");
        return _timeNftMapping[tokenId].endTime;
    }

    /// @notice Get the token id which this token mint from
    /// @dev Throws if `tokenId` is not valid token
    /// @param tokenId  The tokenId of the token
    /// @return The token id which this token mint from
    function originalTokenId(uint256 tokenId) public view virtual override  returns (uint256) {
        require(_exists(tokenId),"invalid tokenId");
        return _timeNftMapping[tokenId].originalTokenId;
    }

    /// @notice Check the NFT is valid now
    /// @dev Throws if `tokenId` is not valid token
    /// @param tokenId  The tokenId of the token
    /// @return The the NFT is valid now
    /// if(startTime <= now <= endTime) {return true;} else {return false;}
    function isValidNow(uint256 tokenId) public view virtual override returns (bool) {
        require(_exists(tokenId),"invalid tokenId");
        return uint256(_timeNftMapping[tokenId].startTime) <= block.timestamp
               && block.timestamp <= uint256(_timeNftMapping[tokenId].endTime);
    }

    /// @notice Mint a new token from an old token
    /// @dev Throws if `tokenId` is not valid token
    /// @param originalTokenId_  The token id which the new token mint from
    /// @param newTokenStartTime  The start time of the new token
    /// @param newTokenOwner  The owner of the new token
    /// @return newTokenId The the token id of the new token
    function split(uint256 originalTokenId_, uint64 newTokenStartTime, address newTokenOwner) public virtual override returns(uint256 newTokenId){
        require(_isApprovedOrOwner(_msgSender(), originalTokenId_), "error: caller is not owner nor approved");

        uint64 oldTokenStartTime =  _timeNftMapping[originalTokenId_].startTime;
        uint64 oldTokenEndTime = _timeNftMapping[originalTokenId_].endTime;
        require( oldTokenStartTime < newTokenStartTime  && newTokenStartTime < oldTokenEndTime, "invalid newTokenStartTime");

        _timeNftMapping[originalTokenId_].endTime = newTokenStartTime - 1;
        uint64 newTokenEndTime = oldTokenEndTime;
        emit TimeUpdate(originalTokenId_, oldTokenStartTime ,_timeNftMapping[originalTokenId_].endTime);

        newTokenId = _mintTimeNft(newTokenOwner, originalTokenId_, newTokenStartTime, newTokenEndTime);
    }

    /// @notice Merge two time NFTs into one time NFT
    /// @dev Throws if `firstTokenId` or `secondTokenId` is not valid token
    /// @param firstTokenId   The id of the first token
    /// @param secondTokenId  The id of the second token
    /// @param newTokenOwner  The owner of the new token
    /// @return newTokenId The id of the new token
    function merge(uint256 firstTokenId,uint256 secondTokenId, address newTokenOwner) public virtual override returns(uint256 newTokenId) {
        require(_isApprovedOrOwner(_msgSender(), firstTokenId) &&  _isApprovedOrOwner(_msgSender(), secondTokenId),
          "error: caller is not owner nor approved");

        TimeNftInfo memory firstToken = _timeNftMapping[firstTokenId];
        TimeNftInfo memory secondToken = _timeNftMapping[secondTokenId];

        require(firstToken.originalTokenId == secondToken.originalTokenId
                && firstToken.startTime <= firstToken.endTime
                && (firstToken.endTime + 1) == secondToken.startTime
                && secondToken.startTime <= secondToken.endTime, "invalid tokenId");

        _burn(firstTokenId);
        _burn(secondTokenId);

        newTokenId = _mintTimeNft(newTokenOwner, firstToken.originalTokenId, firstToken.startTime, secondToken.endTime);
    }

    /// @notice mint a new time NFT
    /// @param to_  The owner of the new token
    /// @param originalTokenId_    The token id which the new token mint from
    /// @param startTime_  The start time of the new token
    /// @param endTime_  The end time of the new token
    /// @return newTokenId The id of the new token
    function _mintTimeNft(address to_, uint256 originalTokenId_, uint64 startTime_, uint64 endTime_) internal virtual returns(uint256 newTokenId)  {
        newTokenId = _nextTokenId;
        _nextTokenId++;

        TimeNftInfo storage info = _timeNftMapping[newTokenId];
        info.originalTokenId = originalTokenId_;
        info.startTime = startTime_;
        info.endTime = endTime_;

        _mint(to_, newTokenId);
    }

    /// @notice mint a new original time NFT
    /// @param to_  The owner of the new token
    /// @param startTime_  The start time of the new token
    /// @param endTime_  The end time of the new token
    /// @return newTokenId The id of the new token
    function _mintOriginalToken(address to_, uint64 startTime_, uint64 endTime_) internal virtual returns(uint256 newTokenId) {
        newTokenId = _nextTokenId;
        _nextTokenId++;

        TimeNftInfo storage info = _timeNftMapping[newTokenId];
        info.originalTokenId = newTokenId;
        info.startTime = startTime_;
        info.endTime = endTime_;

        _mint(to_, newTokenId );
    }

    /// @notice burn a time NFT
    /// @param tokenId  The id of the token
    function _burn(uint256 tokenId) internal  virtual override{
        super._burn(tokenId);
        delete _timeNftMapping[tokenId];
    }
}

```

## Security Considerations

Implementors of the `TimeNFT` standard must consider the condition of `merge` function.  The `originalTokenId` of two NFTs should be same and the time of two NFTs should be adjacent.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**SamWilsn** (2022-04-22):

Some non-formatting related points:

- I’d recommend moving the split, merge, and originalTokenId members into one or two optional interfaces (maybe IERC5007Divisible and IERC5007Joinable?)
- Should merge return a value? For symmetry with split, I would assume the intent is to burn the second token, and adjust the first token’s start/end times?

---

**0xanders** (2022-04-26):

Good suggestion, I will change  `split` , `merge` , and `originalTokenId` members into one optional interfaces.

---

**TsBauer** (2022-07-28):

I’ve been thinking about this EIP. In my opinion, it makes sense to standardize the time properties of NFTs. But some questions arose for me.

- What use cases did you have in mind with split, merge and originalTokenId?
- Is this compatible with ERC-1155? If not, would it be compatible without this optional interface which includes split, merge and originalTokenId?

I’d vote even in favor of dropping the optional interface if it’s in the way of ERC-1155 compatibility. I think it’s hard to justify that we would need a similar but different EIP for ERC-1155.

---

**0xanders** (2022-07-28):

- What use cases did you have in mind with split, merge and originalTokenId?

A use case:  doNFT Splitting and Merging: [doNFT Splitting and Merging - Double](https://docs.double.one/concepts/donft-credentials-for-the-right-to-use-at-a-specific-time/donft-splitting-and-merging)

doNFT is DOUBLE NFT, The user with a doNFT has the right to use the original NFT for a specified period of time.

- Is this compatible with ERC-1155? If not, would it be compatible without this optional interface which includes split, merge and originalTokenId?

ERC5007 is not compatible with ERC-1155 now. There is a count param for a specific token id in ERC-1155.

---

**vic** (2023-04-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> split, merge

what’s the convention here usually? Do we lump various ideas into 1 single ERCs?

because the split / merge interface seems to be addressing a very different problem to what a Time extension ERC seeks to address.

or should this be in the sample implementation instead of an extension interface?

---

**SamWilsn** (2023-04-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vic/48/9817_2.png) vic:

> what’s the convention here usually? Do we lump various ideas into 1 single ERCs?

There isn’t a clear-cut answer unfortunately. I tend to recommend splitting into separate proposals if:

- For independent interfaces/ideas: each idea can stand on its own; or
- For dependant interfaces/ideas: it’s more likely that the dependant proposal won’t be implemented.

A good example of the latter point is the `ERC721Metadata` interface. It’s more likely that tokens *will* implement it than not implement it, so I think it was the correct choice to include it in ERC-721.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vic/48/9817_2.png) vic:

> because the split / merge interface seems to be addressing a very different problem to what a Time extension ERC seeks to address.

If split and merge can be implemented without the time extension, then that’s a great indicator that they belong in their own proposal(s).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vic/48/9817_2.png) vic:

> should this be in the sample implementation instead of an extension interface?

The reference implementation should be *as small as possible* so if merge and split are removed from the specification section, they should be removed from the reference implementation as well.

---

**vic** (2023-04-23):

Thanks alot for the clear explanation.

Wish this was clearer in EIP1 too ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

I am in the midst of writing an ERC, and your suggestions come in handy.

---

**MASDXI** (2024-12-13):

Dear [@0xanders](/u/0xanders), [@LanceSnow](/u/lancesnow) and EIP Editor [@SamWilsn](/u/samwilsn)

After writing [ERC-7818](https://ethereum-magicians.org/t/erc-7818-expirable-erc20/21655), I came across this EIP and realized it has many potential use cases. However, there are still areas where improvements can be made to enhance this EIP without breaking its original intention and idea.

I would like to respectfully ask if it would be possible for my teammate [@parametprame](/u/parametprame) and me to take over as co-authors and maintainers of this EIP.

The area I am focusing on and would like to improve

> ## Motivation
>
>
>
> Should mention potential use case for these tokens can be applied to
>
>
> Privileges or Tickets: Ideal for loyalty programs where tokens represent time-limited benefits.
> Authentication: Ensures that invalid tokens cannot be used for accessing products or services.
> Insurance or Warranty: Provides a clear expiration for coverage or guarantees.
> Certificates: Certifies validity within a specific time frame.
>
>
>
> ## Specification
>
>
>
>
> normative should avoid to change

- isTokenValid → MUST retrieve the status of given tokenId return true if the token is still valid otherwise false
- TokenTimeSet → MUST be emitted after setting the startTime and endTime for a given tokenId. The event should be indexed by tokenId.
- ERC5007TransferredInvalidToken → OPTIONAL custom error returns the tokenId, startTime, endTime, and currenTime
- tokenValidityRemaining → OPTIONAL returns the remaining time, in seconds, before the given tokenId becomes invalid and unusable

### Function Behavior

- balanceOf that was inherited from ERC-721 needs to be clarified should return all tokens including invalid or not.
- transferFrom and safeTransferFrom  MUST check if the token is still usable before transferring. If the condition is not met, they MUST revert the transaction.
- startTime and endTime of tokenId, the startTime MUST less than endTime except in the case where both are set to 0. A startTime and endTime of 0 indicates that the tokenId has no time-limited.

## Security Consideration

- Denial of Service
transfer and transferFrom are not restricted by startTime and endTime tokens are  still transferable but may be unusable in the contract that checks the time info of the token

---

**SamWilsn** (2024-12-16):

We cannot transfer ownership of a proposal without the permission of an original author. The correct procedure is to open a pull request changing the author header field on GitGub.

