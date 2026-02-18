---
source: magicians
topic_id: 12052
title: "FINAL EIP-6147: Guard of NFT/SBT, an Extension of ERC-721"
author: 5cent-AI
date: "2022-12-07"
category: EIPs
tags: [nft, final]
url: https://ethereum-magicians.org/t/final-eip-6147-guard-of-nft-sbt-an-extension-of-erc-721/12052
views: 3175
likes: 2
posts_count: 12
---

# FINAL EIP-6147: Guard of NFT/SBT, an Extension of ERC-721

**Title**: Guard of NFT/SBT, an Extension of ERC-721

**Description**: A new management role with an expiration date of NFT/SBT is defined, achieving the separation of transfer right and holding right.

**Author**: [5660.eth](https://twitter.com/web3saltman),Wizard Wang

**Requirements**: 165, 721

**Created**: 2022-12-07

## Abstract

This standard is an extension of ERC-721. It separates the holding right and transfer right of non-fungible tokens (NFTs) and Soulbound Tokens (SBTs) and defines a new role, `guard` with `expires`. The flexibility of the `guard` setting enables the design of NFT anti-theft, NFT lending, NFT leasing, SBT, etc.

## Motivation

NFTs are assets that have both use and financial value.

Many cases of NFT theft currently exist, and current NFT anti-theft schemes, such as transferring NFTs to cold wallets, make NFTs inconvenient to be used.

In current NFT lending, the NFT owner needs to transfer the NFT to the NFT lending contract, and the NFT owner no longer has the right to use the NFT while he or she has obtained the loan. In the real world, for example, if a person takes out a mortgage on his own house, he still has the right to use that house.

For SBT, the current mainstream view is that an SBT is not transferable, which makes an SBT bound to an Ether address. However, when the private key of the user address is leaked or lost, retrieving SBT will become a complicated task and there is no corresponding specification. The SBTs essentially realizes the separation of NFT holding right and transfer right. When the wallet where SBT is located is stolen or unavailable, SBT should be able to be recoverable.

In addition, SBTs still need to be managed in use. For example, if a university issues diploma SBTs to its graduates, and if the university later finds that a graduate has committed academic misconduct or jeopardized the reputation of the university, it should have the ability to retrieve the diploma SBT.

## The standard has more than the following use cases:

SBTs. The SBTs issuer can assign a uniform role of `guard` to the SBTs before they are minted, so that the SBTs cannot be transferred by the corresponding holders and can be managed by the SBTs issuer through the `guard`.

NFT anti-theft. If an NFT holder sets a `guard` address of an NFT as his or her own cold wallet address, the NFT can still be used by the NFT holder, but the risk of theft is greatly reduced.

NFT lending. The borrower sets the `guard` of his or her own NFT as the lender’s address, the borrower still has the right to use the NFT while obtaining the loan, but at the same time cannot transfer or sell the NFT. If the borrower defaults on the loan, the lender can transfer and sell the NFT.

Additionally, by setting an `expires` for the `guard`, the scalability of the protocol is further enhanced, as demonstrated in the following examples:

More flexible NFT issuance. During NFT minting, discounts can be offered for NFTs that are locked for a certain period of time, without affecting the NFTs’ usability.

More secure NFT management. Even if the `guard` address becomes inaccessible due to lost private keys, the `owner` can still retrieve the NFT after the `guard` has expired.

Valid SBTs. Some SBTs have a period of use. More effective management can be achieved through `guard` and `expires`.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6147.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6147.md)



```md
---
eip: 6147
category: ERC
status: Moved
---

This file was moved to https://github.com/ethereum/ercs/blob/master/ERCS/erc-6147.md
```

## Replies

**5cent-AI** (2022-12-08):

```auto
mapping(uint256 => address) private token_guard_map;
```

=>

```auto
mapping(uint256 => address) internal token_guard_map;
```

---

**5cent-AI** (2022-12-17):

update

` require(_isApprovedOrOwner(_msgSender(), tokenId),"ERC721QS: caller is not owner nor approved")`

Both the owner and the operator can set up guards to be more compatible with subsequent application protocols and application scenarios

add

```auto
 ///@dev When burning, delete `token_guard_map[tokenId]`
    function _burn(uint256 tokenId) internal virtual override {
        address guard=guardOf(tokenId);
        super._burn(tokenId);
        delete token_guard_map[tokenId];
        emit UpdateGuardLog(tokenId, address(0), guard);
    }
```

When burning, delete  the `guard`.

---

**SamWilsn** (2023-02-07):

As part of our process to encourage peer review, we assign a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@ThunderDeliverer](/u/thunderdeliverer)! Please note that this review **is NOT required** to move your EIP through the process. When you—the authors—feel ready, just open a pull request.

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@ThunderDeliverer](/u/thunderdeliverer) please take a look through [EIP-6147](https://eips.ethereum.org/EIPS/eip-6147) and comment here with any feedback or questions. Thanks!

---

**5cent-AI** (2023-02-18):

We have discussed for six months and finally decided to define a new management role with a time limit. The introduction of `expires` for `guard` is very significant.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> Additionally, by setting an expires for the guard, the scalability of the protocol is further enhanced, as demonstrated in the following examples:
>
>
> More flexible NFT issuance. During NFT minting, discounts can be offered for NFTs that are locked for a certain period of time, without affecting the NFTs’ usability.
>
>
> More secure NFT management. Even if the guard address becomes inaccessible due to lost private keys, the owner can still retrieve the NFT after the guard has expired.
>
>
> Valid SBTs. Some SBTs have a period of use. More effective management can be achieved through guard and expires.

---

**zt1991666** (2023-02-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> For SBT, the current mainstream view is that an SBT is not transferable, which makes an SBT bound to an Ether address. However, when the private key of the user address is leaked or lost, retrieving SBT will become a complicated task and there is no corresponding specification. The SBTs essentially realizes the separation of NFT holding right and transfer right. When the wallet where SBT is located is stolen or unavailable, SBT should be able to be recoverable.

it is hard to define a address was been stolen

---

**zt1991666** (2023-02-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> NFT anti-theft. If an NFT holder sets a guard address of an NFT as his or her own cold wallet address, the NFT can still be used by the NFT holder, but the risk of theft is greatly reduced.

Is this address write in the contract ?

---

**5cent-AI** (2023-02-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zt1991666/48/8630_2.png) zt1991666:

> it is hard to define a address was been stolen

If an address is stolen, the SBT holder should report it to the SBT issuer for judgment.

---

**5cent-AI** (2023-02-19):

If an address is stolen, the SBT holder should report it to the SBT issuer for judgment.

---

**5cent-AI** (2023-02-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zt1991666/48/8630_2.png) zt1991666:

> Is this address write in the contract ?

Yes, for example, you can set the address of “guard” as a cold wallet address to prevent theft.

---

**william1293** (2023-02-22):

Recoverable, manageable, and valid SBT is an amazing idea.

---

**5cent-AI** (2023-02-23):

Yes, I think we should make deeper considerations and improvements on what SBT is and how to manage SBT, including exploring underlying protocols.

