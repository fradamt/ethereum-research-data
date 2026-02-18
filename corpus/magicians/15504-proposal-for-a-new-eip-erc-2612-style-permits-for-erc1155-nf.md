---
source: magicians
topic_id: 15504
title: "Proposal for a new EIP: ERC-2612 style permits for ERC1155 NFTs"
author: emiliolanzalaco
date: "2023-08-20"
category: EIPs
tags: [nft, defi]
url: https://ethereum-magicians.org/t/proposal-for-a-new-eip-erc-2612-style-permits-for-erc1155-nfts/15504
views: 2239
likes: 2
posts_count: 6
---

# Proposal for a new EIP: ERC-2612 style permits for ERC1155 NFTs

**Motivation**

Permits enable a one-transaction transfer flow, removing the approval step. There is a standard for ERC20 Permits [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612) and ERC721 Permits [ERC-4494](https://eips.ethereum.org/EIPS/eip-4494).

ERC1155 is widely adopted; it would make sense to standardise permits for this token type to enable homogeneous support in third-party applications. Further, I’ve seen a few implementations in the wild like t11s’ here: [ERC1155Permit](https://github.com/primitivefinance/rmm-manager/blob/main/contracts/base/ERC1155Permit.sol).

I’ve put together an [example implementation](https://github.com/emi17eal/ERC1155Permit).

You’ll notice a choice to go with `bytes sig` rather than `uint8 v, bytes32 r, bytes32 s`. This decision was discussed in the ERC4494 [thread](https://ethereum-magicians.org/t/eip-4494-extending-erc-2612-style-permits-to-erc-721-nfts/7519/2) and the reasoning is that `bytes sig` supports smart contract signing.

Given that ERC1155s can be fungible, it makes sense that an address permits an operator to transfer their tokens. This flow is more similar to ERC2612 than ERC4494. This means nonces are indexed by address: `nonces(address owner)`.

I’d like to open up this thread for **feedback** on standardising the ERC1155 Permit flow.

## Replies

**dcota** (2023-12-09):

ERC1155 has a limited approval system.

In the original implementation it is out of the box an all-or-nothing type of approval due to `setApprovalForAll`.

Could the permit implementation give more granular control on by the `owner` to the `spender` for certain `id` in a specified `amount`?

```auto
function permit(
      address owner,
      address spender,
      uint256 tokenId,
      uint256 value,
      uint256 deadline,
      uint8 v,
      bytes32 r,
      bytes32 s
  ) external payable override {
```

That would of course require a new mapping. Something like:

```auto
mapping(owner => mapping(tokenId => mapping(spender => amount))) public allowance;
```

---

**calvbore** (2024-01-27):

I’ve been thinking about making this ERC proposal for a while now, and I have a couple things that I think should be considered.

There is an ERC for 1155 approvals by amount, [ERC-5216](https://github.com/ethereum/ercs/blob/master/ERCS/erc-5216.md), and it should probably be a requirement for this ERC.

The nonce should be for both `address owner` and `uint256 tokenId`, so that sending out a permit while another is out there already for a separate tokenId won’t have them interfering and blocking each other.

I’m also wondering if it is worth thinking about adding another `bytes` field to the signature, for some extra arbitrary data in the signature allowing it to be extensible? I have a use case in mind for this, but I’m wondering if anybody else can see a use for it as well?

---

**calvbore** (2024-01-28):

Made the PR for this ERC [here](https://github.com/ethereum/ERCs/pull/223)!

---

**emiliolanzalaco** (2024-02-01):

[@dcota](/u/dcota) and [@calvbore](/u/calvbore) I agree that the ability to approve a granular `amount` is a good extension to ERC1155.

[@calvbore](/u/calvbore) I am in favour of `bytes sig` over `uint8 v, bytes32 r, bytes32 s` for reasons mentioned above.

[@calvbore](/u/calvbore) Thanks for taking the time to open a PR for this. It would be cool collaborate and co-author the EIP.

---

**SamWilsn** (2024-05-16):

> sig is a valid secp256k1, ERC-2098, or ERC-1271 signature from owner of the message

Your proposal doesn’t specify how to tell whether the signature is secp256k1 or one of the other signature forms. It’s fine to leave that up to implementations, but I’d be explicit if that’s what you want.

