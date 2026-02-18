---
source: magicians
topic_id: 8655
title: NFT Commission Standard
author: StEvUgnIn
date: "2022-03-19"
category: EIPs
tags: [nft, erc-721, erc1155, eip2981]
url: https://ethereum-magicians.org/t/nft-commission-standard/8655
views: 648
likes: 1
posts_count: 1
---

# NFT Commission Standard

This discussion concerns the need for developing a standard for accessing to commission on-chain based on the work done with EIP-2981.

Royalty on Non Fungible Token (NFT) is described in the ERC standard EIP-2981 which is related to

`tokenId` and `salePrice`.

On decentralized NFT marketplaces, Royalty is respectively paid by the buyer and allows the artist to keep earning a fixed percentage on every next transaction.

Commision contrarily to royalty is paid to the Token operator only on the first sale.

There is currently no standard to describe given commission on-chain. The need for commission is based on the scenario that artists required technical expertise (e.g., refered as Token operator in `EIP-721`) to tokenize their artwork. Token operator would like to earn commission from the first transaction (e.g., sale, auction and mint) without directly accessing the artist wallet but to provide a public access that they need the commission in agreement with the artist must be sent directly to them.

```nohighlight
///
/// @dev Interface for the NFT Commission Standard
///
interface NFTCommission is ERC165 {
    /// ERC165 bytes to add to interface array - set in parent contract
    /// implementing this standard
    ///
    /// bytes4(keccak256("commissionInfo(uint256,uint256)")) ==
    /// bytes4 private constant _INTERFACE_ID_NFTCommission = ;
    /// _registerInterface(_INTERFACE_ID_NFTCommission);

    /// @notice Called with the sale price to determine how much commission
    //          is owed and to whom.
    /// @param _tokenId - the NFT asset queried for commission information
    /// @param _salePrice - the sale price of the NFT asset specified by _tokenId
    /// @return receiver - address of who should be sent the commission payment
    /// @return commissionAmount - the commission payment amount for _salePrice
    function commissionInfo(
        uint256 tokenId,
        uint256 salePrice
    ) external view returns (
        address receiver,
        uint256 commissionAmount
    );
}
```
