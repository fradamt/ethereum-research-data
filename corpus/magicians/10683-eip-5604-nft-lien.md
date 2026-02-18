---
source: magicians
topic_id: 10683
title: "EIP-5604: NFT Lien"
author: xinbenlv
date: "2022-09-06"
category: EIPs
tags: [erc, erc-721, collateralization]
url: https://ethereum-magicians.org/t/eip-5604-nft-lien/10683
views: 3969
likes: 18
posts_count: 14
---

# EIP-5604: NFT Lien

Hi all, we are proposing a standard for “lien” of NFT, mimicking the property lien [Lien - Wikipedia](https://en.wikipedia.org/wiki/Lien). Please comment here

See the EIP draft [Add EIP-5604: NFT Lien by xinbenlv · Pull Request #5604 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5604/files)

## Replies

**xinbenlv** (2022-09-06):

A draft of the EIP is published at [EIP-5604](https://eips.ethereum.org/EIPS/eip-5604). We also look forward to contributions and co-authors. Let me know if you are interested. I personally think it’s an important financial vehicle.

---

**AlexQin** (2022-09-07):

Hello xinben, just saw your post. I love this idea, actually we are building a business model upon this idea, would love to cooperate with you and dig into that. ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=12)

---

**xinbenlv** (2022-09-08):

Glad to hear. Happy to collaborate!

---

**AlexQin** (2022-09-08):

If we can establish the standard of lien on NFT, the debtor don’t need to transfer the ownership of the collateral to the creditor, which solves the question of trust and low capital utilization rate due to over collateralized. Moreover, the debtor can still use or benefit from the collateral while borrowing against the NFT.

Meanwhile, a lien secures the loan and vests the creditor with the right to realize the value of collateral by acquiring or selling the collateral if the debtor fail to repay the loans.

The proposed standard may sound like the concept of non-possessory contractual lien under Common Law I would say.

---

**beyondandl1** (2022-09-20):

Great Idear! We really need it.

---

**allen** (2022-09-24):

Hi [@xinbenlv](/u/xinbenlv) , I am very interested in your proposal. Actually, we have implemented similar functionality in our project [Ubiloan](https://ubiloan.io). Now I re-wrote a reference implementation based on your interface. You can check the code in [Github](https://github.com/allenzhou-ubiloan/erc-5604).

**Reference Implementation**

```auto
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.0;

import "openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";

import "./IERC5604.sol";

/// @author Allen Zhou
abstract contract ERC5604 is ERC721, IERC5604 {

    // Mapping from token ID to lien holder address.
    mapping(unit256 => address) private _tokenLienHolders;

    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(bytes4 interfaceId) public view virtual override(IERC165, ERC721) returns (bool) {
        return interfaceId == type(IERC5604).interfaceId || super.supportsInterface(interfaceId);
    }

    /**
     * @dev See {IERC5604-addLienHolder}.
     */
    function addLienHolder(uint256 tokenId, address holder, bytes calldata extraParams) public virtual override(IERC165, ERC721) {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC5604: caller is not token owner or approved");
        require(_tokenLienHolders[tokenId] == address(0), "ERC5604: token lien holder existed");
        require(holder != address(0), "ERC5604: add lien to address(0)");

        _tokenLienHolders[tokenId] = holder;

        emit OnLienPlaced(tokenId, holder, extraParams);
    }

    /**
     * @dev See {IERC5604-removeLienHolder}.
     */
    function removeLienHolder(uint256 tokenId, address holder, bytes calldata extraParams) public virtual override(IERC165, ERC721) {
        require(_tokenLienHolders[tokenId] == _msgSender(), "ERC5604: caller is not token lien holder");

        delete _tokenLienHolders[tokenId];

        emit OnLienRemoved(tokenId, holder, extraParams);
    }

    /**
     * @dev See {IERC5604-hasLien}.
     */
    function hasLien(uint256 tokenId, address holder, bytes calldata extraParams) public view virtual override returns (bool) {
        return _lienHolderOf(tokenId) == holder;
    }

    /**
     * @dev Returns the lien holder of the `tokenId`. Does NOT revert if token doesn't exist.
     */
    function _lienHolderOf(uint256 tokenId) internal view virtual returns (address) {
        return _tokenLienHolders[tokenId];
    }

    /**
     * @dev See {IERC721-transferFrom}.
     */
    function transferFrom(
        address from,
        address to,
        uint256 tokenId
    ) public virtual override {
        //solhint-disable-next-line max-line-length
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not token owner or approved");

        require(_tokenLienHolders[tokenId] == _msgSender() || _tokenLienHolders[tokenId] == address(0), "ERC5604: caller is not token lien holder");

        _transfer(from, to, tokenId);
    }

    /**
     * @dev See {IERC721-safeTransferFrom}.
     */
    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId,
        bytes memory data
    ) public virtual override {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not token owner or approved");

        require(_tokenLienHolders[tokenId] == _msgSender() || _tokenLienHolders[tokenId] == address(0), "ERC5604: caller is not token lien holder");

        _safeTransfer(from, to, tokenId, data);
    }
}
```

---

**xinbenlv** (2022-09-28):

This is wonderful. I can see the implementation very well implemented. Do you have any other comments about the EIP and how it can be improved? I wonder if you would be interested in co-authoring this EIP with me?

---

**allen** (2022-09-29):

Of course, we’ve been trying to provide a better way for NFT Lending Protocol. We can refine this technical solution so that it can pass the rigorous testing of industrial practice directly and share it with the community ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**allen** (2022-09-29):

Look forward to collaborating with you and other interested community members!!

---

**wisdant** (2023-01-30):

[@xinbenlv](/u/xinbenlv) This is very cool! I see great GameFi and RWA use cases and would love to partner on this.

I feel the example for why separate functions are used for add and remove can be strengthened. “the token holder shall be able to add someone else as a lien holder but the lien holder of that token” seems incomplete.

Have you considered hasOtherLiens(…) for a lien holder to check if it is the last lien?  In some lending cases to increase credit for the backed asset, the lender already knows the lien that they have put on the asset. They also like to know if there are other liens placed against the asset.

The comment says “amount of debt” shall be its own EIP. Do you have a draft for that? I feel these two might have to go hand-in-hand or go out as one EIP.

---

**xinbenlv** (2023-01-30):

That’s good point. [@allen](/u/allen) WDYT?

---

**ispolin69** (2023-01-31):

I think it’s worth considering for us

---

**tbergmueller** (2023-10-23):

I had recommended this in ERC-6956 as a Lien mechanism, but since your proposal’s status is stagnant [I had to remove the link in order to proceed to Review](https://github.com/ethereum/EIPs/pull/7903). Please ping me in case this proposal moves forward.

