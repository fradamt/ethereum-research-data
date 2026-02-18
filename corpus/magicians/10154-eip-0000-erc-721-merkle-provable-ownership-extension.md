---
source: magicians
topic_id: 10154
title: EIP-0000 ERC-721 Merkle-Provable Ownership Extension
author: Nerolation
date: "2022-07-28"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-0000-erc-721-merkle-provable-ownership-extension/10154
views: 1018
likes: 2
posts_count: 3
---

# EIP-0000 ERC-721 Merkle-Provable Ownership Extension

**EDIT: Based on received feedback, I altered the design:**

Find the new repo here:

https://github.com/Nerolation/EIP-ERC721-zk-SNARK-Extension

and the related disussion (before submitting a pull request):

https://ethresear.ch/t/erc721-extension-for-zk-snarks/13237

**The following is deprecated:**

This is an ERC721 extension to store ownership information in a merkle tree.

https://github.com/Nerolation/EIP0000

It enables the use of **private merkle-proofs (zk-SNARKs)** for ownership verification.

The idea was inspired by the [Souldbound token](https://vitalik.ca/general/2022/01/26/soulbound.html) article of Vitalik.

**How it works**

When minting and transfering tokens, there is a commitment *c* created for the recipient that consists of a users address and the respective tokenID. This *c*  is then written to a leaf in the merkle tree.

For prooving ownership, a user must demonstrate the ability to reproduce any *c* in the merkle tree. For that, the user must have access to an address *a*, which, when being hashed together with a tokenId *tid* (*c = h(a, tid)*), is present in the merkle tree. Prooving access to an address can be done by signing a message.

**Using zk-SNARKs, the owner can verify to be included in the merkle tree without pointing to the exact location in the tree.** This allows for private ownership proofs.

When a user transfers, the respective entry in the merkle tree is nullified ( *c* ==> True ). Same happens when tokens are burned.

Pros:

- Private Ownership proofs
- Logic handled by underlying ERC721 (no Stealth addresses)

Cons:

- Comes with fixed and limited nr of owners/transfers (depending on size of merkle tree)
- Inceasing gas costs for all users
- Once owner, always owner (see note below)

I initially thought about implementing it for ERC-4973 (Account-bound Tokens) or ERC-5114 (Soulbound Badge), but came to the conclusion that it would only make sense for ERC-721, at the time.

NOTE: Since there is no `nullifier` (some secret noise to the commitment) incorporated in the commitment hash, users who once had the token can always proof ownership. I consider this a bug, not a feature, but might also depend on the usecase. By using a `nullifier`, leafs can be marked as “spent”, however, it eventually requires users to transfer nullifiers off-chain, for doing transfers.  So, as you can see, still some thoughts required on this.

Check out the [Tornado Cash docs](https://docs.tornado.cash/general/how-does-tornado.cash-work) for some background.

You’ll find some really good explanations there.

I really appreciate receiving feedback!

## Replies

**themandalore** (2022-08-02):

super cool stuff.  I think the question is what are some use cases? Proving you own an ape when you’re embarrassed about which one?  And you use the nova contracts from tornado cash to make it transferrable too right?

---

**Nerolation** (2022-08-02):

Thanks for your feedback!

I’m currently pivoting from the proposed implementation, because I think that including a merkle tree on-chain adds computation loads that are not needed. Instead, I try to implement something like barryWhiteHat implemented [here](https://github.com/barryWhiteHat/roll_up_token).

Have a look at this, it’s a great resource. Basically, I now strictly implement what Vitalik sketched in a short [section](https://vitalik.ca/general/2022/01/26/soulbound.html) on zk-SNARKable SoulBound Tokens.

What I got from “Soul-bound” token discussions (as of now), transferability will still exists, therefore, I’m now thinking of a transfer function that also takes a commitment, that can be used for the zk ownership proof.

It would look somethin like this:

```auto
function _transfer(
        address to,
        uint256 tokenId,
        bytes calldata proof,
        bytes calldata input,
        bytes32 commitment
    ) internal virtual
```

> I think the question is what are some use cases?

Usecase could be to proof (privately) that you visited ETHAmsterdam and get an additional sticker at ETHBogota. More industrial usecases are proving vaccination status without revealing identity.

As I interpreted from Vitalik’s explanation, stealth addresses are required for the final implementation.

I’m currently working on finishing the implementation and will then update this thread (a few more days required).

