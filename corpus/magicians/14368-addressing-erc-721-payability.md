---
source: magicians
topic_id: 14368
title: Addressing ERC-721 Payability
author: sullof
date: "2023-05-21"
category: ERCs
tags: [nft, token, royalties]
url: https://ethereum-magicians.org/t/addressing-erc-721-payability/14368
views: 571
likes: 0
posts_count: 5
---

# Addressing ERC-721 Payability

Recently, I’ve been reflecting upon the various proposals aimed at enabling creators to collect royalties from their Non-Fungible Tokens (NFTs). It seems that none of these solutions sufficiently tackle the problem at hand. My recent discussion with [@0x0ece](/u/0x0ece) led us to some interesting insights, which I would like to share with you.

We conjecture that a more natural and effective solution to address the royalties/fees dilemma would be to make transfers payable. By doing so, the contract can independently collect royalties and fees directly on the blockchain, removing the reliance on marketplaces’ decision to pay off-chain fees or support standards like EIP-2981.

I anticipate some may argue this idea may conflict with the established ERC-721 standard. But let’s clear up this common misconception. Upon scrutinizing the ERC-721 standard more closely (see here: [ERC-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)), it becomes apparent that it indeed defines functions such as transfer, approve, etc. as payable.

It is in fact OpenZeppelin, in a bid to minimize the risk of contracts receiving and potentially losing values, that decided to make these functions non-payable. Here is a related discussion for more context: [Consider supporting payable ERC721's safeTransferFrom, transferFrom, and approve · Issue #1015 · OpenZeppelin/openzeppelin-contracts · GitHub](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/1015)

In my view, OpenZeppelin should have adhered to the original interface while making the underlying contracts non-payable. This would have provided developers the flexibility to extend their interfaces and create a payable version of these functions if they so desired. Regrettably, this isn’t possible currently as non-payable functions cannot be overridden as payable.

Since OpenZeppelin’s implementation of ERC721 is the de-facto standard, as a potential resolution to this issue, I propose the creation of a new interface, say ‘ERC721Payable’, that users would need to implement alongside the original ERC721 interface. The interface could be as follows:

```auto
interface ERC721Payable {
  function withdrawEther(uint256 amount, address beneficiary) external;
}
```

I’m eager to hear your thoughts on this proposition. Can this serve as a robust solution to the royalties/fees problem in the NFT space? How can we refine this further?

Thank you for your time and your feedback.

## Replies

**sullof** (2023-05-21):

Of course, the contract would need more functionalities to manage royalties and fee (for example, it should know the price of the NFT), but everything starts from having payable transfer functions.

---

**sprice** (2023-05-21):

Creators and marketplaces have seem to found themselves in a bind with regards to royalties which is unfortunate. I believe it’s important that creators are able to earn royalties.

I’m excited to see this but to be candid am skeptical there is a solution.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> By doing so, the contract can independently collect royalties and fees directly on the blockchain

How does the ERC-721 contract know the value involved in the purchase transaction from within a marketplace contract?

And what do you propose happens when I transfer an NFT I own from one wallet of mine to another wallet of mine? And does that need to be sybil resistant?

---

**sprice** (2023-05-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> but everything starts from having payable transfer functions.

100%. It would be great if the destination is possible and payable transfer functions are one step. I believe it’s important that the rest of the steps are well understood before laying the first stone.

---

**sullof** (2023-05-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sprice/48/9532_2.png) sprice:

> How does the ERC-721 contract know the value involved in the purchase transaction from within a marketplace contract?

I didn’t think deeply to a solution but a possible way to go is that when the safeTransferFrom is called with a proposed msg.value, the contract activates an oracle that confirms that the value is reasonable for the market price of the asset and executes the actual transfer. If the value is not aligned, the contract returns the funds to the original caller, keeping just the cost for the gas.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sprice/48/9532_2.png) sprice:

> And what do you propose happens when I transfer an NFT I own from one wallet of mine to another wallet of mine? And does that need to be sybil resistant?

I would say that the transfer can apply a fee only if the caller is an operator. If it is the actual owner, fees and royalties are not applied. Someone for sure will try to exploit this, but it looks to me like a reasonable limitation.

