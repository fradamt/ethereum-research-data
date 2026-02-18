---
source: magicians
topic_id: 16668
title: "ERC-7558: Minimal Lockable Range NFTs"
author: 0xCLARITY
date: "2023-11-16"
category: ERCs
tags: [erc, nft, token, erc-721, soulbound]
url: https://ethereum-magicians.org/t/erc-7558-minimal-lockable-range-nfts/16668
views: 1306
likes: 3
posts_count: 7
---

# ERC-7558: Minimal Lockable Range NFTs

There are various soulbound / lockable proposals for 721-NFTs, like:


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5192)





###



Minimal interface for soulbinding EIP-721 NFTs











      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6982)





###



A gas-efficient approach to lockable ERC-721 tokens










However, none of those proposals have events supporting batch operations to lock/unlock multiple tokens (or an entire contract in a gas efficient way).

So I propose the following interface:

```solidity
// ERC165 interfaceId 0x75587558
interface IERC7558 is IERC5192 {
  /// @notice Emitted when the locking status for a range of tokens is changed to locked.
  event RangeLocked(uint256 _fromTokenId, uint256 _toTokenId);

  /// @notice Emitted when the locking status for a range of tokens is changed to unlocked.
  event RangeUnlocked(uint256 _fromTokenId, uint256 _toTokenId);
}
```

> NOTE: The ERC-165 identifier doesn’t strictly follow ERC-165 calculations, but there is prior art to assigning a custom identifier to avoid conflict or for ERCs that do not include any functions, like ERC-4906.
>
>
> The ERC-165 identifier is thus 0x75587558.

This proposal is completely compatible with ERC-5192, but adds support for token range operations.

This would let you do something like this to mark all the tokens in a contract as locked:

```auto
emit RangeLocked(0, UINT256_MAX)
```

and later if you wanted to allow transfers of a given token collection:

```auto
emit RangeUnlocked(0, UINT256_MAX)
```

I believe this proposal is either more flexible or more gas-efficient than existing soulbound/lockable proposals.

https://github.com/ethereum/ERCs/pull/103

## Replies

**sullof** (2023-11-19):

When working on ERC6982 I thought about batch locked events, but I dismissed it because it is hard to cover most cases. You covered the case when someone locks or unlocks a range. What if I want to unlock all the even tokenIds? What if I have 40 tokenIds that I want to lock/unlock in a single operation?

There are so many cases that can require a batch process and I believe that an ERC focused on batch processes should try to cover all of them.

For this reason, I would change the name of the event from *BatchLocked* to *RangeLocked*, which is  more clear.

Instead of forcing users to implement many overlapping interfaces, it would be better to make an extension. Why not setting it as

```auto
// ERC165 interfaceId 0x75587558
interface IERC_Draft_BATCH_MIN_SBTS is ERC5192 {

  /// @notice Emitted when the locking status for a range of tokens is changed to locked.
  event BatchLocked(uint256 _fromTokenId, uint256 _toTokenId);

  /// @notice Emitted when the locking status for a range of tokens is changed to unlocked.
  event BatchUnlocked(uint256 _fromTokenId, uint256 _toTokenId);

}
```

If not, those who have already implemented ERC5192 will have issues using both interfaces.

In conclusion, I would suggest you change it in

```auto
//
interface ERC7558 is ERC5192 {

  event RangeLocked(uint256 _fromTokenId, uint256 _toTokenId);

  event RangeUnlocked(uint256 _fromTokenId, uint256 _toTokenId);

}
```

or (what I would prefer ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12))

```auto
//
interface ERC7558 is ERC6982 {

  event RangeLocked(uint256 _fromTokenId, uint256 _toTokenId, boolean locked);

}
```

---

**sullof** (2023-11-19):

I would also suggest not to use the word *soulbound*. It refers to a special case of lockable tokens and makes your proposal looking not a general one. Consider that even [@TimDaub](/u/timdaub) tried to remove that from the final name of its proposal, but it was in the final stage and that was not possible.

---

**0xCLARITY** (2023-11-22):

Appreciate the feedback. I updated the proposal name to: “Minimal Lockable Range NFTs”, and updated the naming to `RangeLocked` and `RangeUnlocked`.

I initially used `Batch` for the range events since that is what is used in [ERC-4906](https://eips.ethereum.org/EIPS/eip-4906) - but I agree that `RangeX` is a better descriptor of the behavior.

I’m a little torn on inheriting from 5192 - I thought it might be easier to implement a compatible interface rather than inheriting the inheritance - but after thinking about it more I recognize that can be abstracted away from anyone implementing this.

---

**TimDaub** (2023-11-27):

Just came here to say that I appreciate you building on ERC-5192! If there’s any way I can help, please DM me on TG or other places!

---

**sullof** (2023-12-08):

While I would have appreciated if you where extending ERC6892 since you adopted my suggestion, including the final name of the events, I agree that ERC5192 needs this extension much more.

---

**sullof** (2023-12-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xclarity/48/10935_2.png) 0xCLARITY:

> emit BatchLocked(0, UINT256_MAX)

That is a typo, using the original name.

