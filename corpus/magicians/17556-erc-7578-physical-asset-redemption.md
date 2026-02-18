---
source: magicians
topic_id: 17556
title: ERC-7578 Physical Asset Redemption
author: Vidor
date: "2023-12-21"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7578-physical-asset-redemption/17556
views: 2315
likes: 10
posts_count: 12
---

# ERC-7578 Physical Asset Redemption

Discussion for [ERC-7578 Physical Asset Redemption](https://eips.ethereum.org/EIPS/eip-7578)

The Physical Asset Redemption Standard (the “Standard”) is an extension of [ERC-721](https://www.odwebp.svc.ms/eip-721.md). The proposed standard implements additional functionality and information pertaining to the NFT’s underlying physical asset by capturing information that enables the holder of physical asset backed NFTs to verify authenticity and redeem the underlying physical assets. The Standard is primarily aimed at providing transparency by disclosing details of involved parties and provides opportunity to define and make easily available relevant legal relationship between NFT holder and the holder of the respective underlying physical asset.

## Replies

**tadaa** (2024-04-11):

With the tokenization of real-world assets and in particular physical assets, there is a demand for transparency on the token level for (prospective) token holders to retrieve specific information about the underlying physical asset a NFT is referring to. The primary aim is to provide the token holders with the basic information that enables them to legally enforce a redemption of the physical asset in the real world in cases where the NFT shall represent the physical asset. The accessible information on the token level also allows for a prospective token buyer to conduct instant due diligence on the token and underlying physical asset.

---

**Vidor** (2024-04-22):

Absolutely, transparency and data integrity are paramount in tokenizing physical assets, ensuring trust and credibility in the digital representation of real world items. Token issuers are required to provide accurate and comprehensive data during the minting stage, laying the foundation for transparency and empowering token holders to make informed investment decisions.

Moreover, if any changes occur to the underlying data after minting or during the lifecyle of the digital asset, it’s crucial that the existing token be burned, and a new token be created. This process ensures that the token’s representation of the physical asset remains accurate and up-to-date, preventing any potential confusion or discrepancy between the token and its corresponding physical asset.

With blockchain technology, supporting the storage of the data technically isn’t challenging. It’s more about cultivating trust between token issuers and holders, which also acts as a safeguard against misinformation and manipulation, thereby enhancing the reliability and authenticity of tokenized assets in the digital realm.

---

**gabrielstoica** (2024-05-07):

We certainly need a standardized way to synchronize and define the underlying physical asset’s properties, especially when talking about RWA.

Here are a few improvements I’m suggesting after reviewing the proposal:

- Update the Properties struct documentation and rename the legalOwner param to assetHolder to match the struct definition;
- Remove the tokenId parameter within the Properties struct as all tokens IDs will point to their respective properties structure using a dedicated mapping(uint256 => Properties) public properties; mapping; By doing so, both PropertiesSet and PropertiesRemoved events can be updated to index the tokenId, like this:

```auto
   /**
     * @notice Emitted when properties are set
     * @param tokenId The ID of the token
     * @param properties The properties of the token
     */
    event PropertiesSet(uint256 indexed tokenId, Properties properties);

   /**
     * @notice Emitted when properties are removed
     * @param tokenId The ID of the token
     * @param properties The properties of the token
     */
    event PropertiesRemoved(uint256 indexed tokenId, Properties properties);
```

- The properties() method could be updated by removing the tokenId from the return fields and by renaming the input parameter from id to tokenId to match the method’s documentation; the second suggestion should also be applied to the setProperties() method;
- Consider making the properties mapping private in the implementation and create a getProperties() getter to be consistent with the setProperties() method;

On top of that I’m considering the best way to maintain backward compatibility with the OpenZeppelin ERC721 versioning. In the new `v5.0.0` release it will not be possible to override the `_safeMint()` and `_burn()` methods using the proposed approach. Perhaps the standard should also include an example implementation for any smart contract using the `v5.0.0` version where one would override the `_update()` method to check the `to` and `from` addresses, i.e.:

```auto
function _update(address to, uint256 tokenId, address auth) internal override returns (address) {
        address from = _ownerOf(tokenId);
        if (to == address(0)) {
            _removeProperties(tokenId);
        } else if (from == address(0)) {
          require(properties[tokenId].tokenId > 0, "Properties not initialized");
        }

        return super._update(to, tokenId, auth);
    }
```

---

**Vidor** (2024-05-09):

Great! Thanks we appreciate the feedback and will definitely get the draft updated with these suggestions!

---

**Vidor** (2024-05-10):

[@gabrielstoica](/u/gabrielstoica) Changes are merged and live [Physical Asset Redemption | Ethereum Improvement Proposals](https://ercs.ethereum.org/ERCS/erc-7578)

---

**SamWilsn** (2024-06-25):

I’d recommend not defining `setProperties` in the standard. Functions that are only meant to be called by “a trusted externally owned account (EOA) or contract” don’t need to be part of the standard because there’s no interoperability.

ERC-20 is a great example of this. `mint` and `burn` are very common functions, but aren’t part of ERC-20 because there aren’t any parties that need to coordinate on minting and burning. The person who deployed the contract knows exactly how to call `mint` and `burn`, and other users aren’t even allowed to call them.

By defining `setProperties` in the standard, you limit the functionality of implementations who might not even want to allow changing properties after the contract is deployed.

---

**gabrielstoica** (2024-07-01):

Hey [@SamWilsn](/u/samwilsn)!

Thanks for your feedback!

Indeed, the `setProperties` method restricts the standard interoperability as some people would want to make it internal and just call it at the deployment time. Therefore, I’ve removed it from the interface and added a small note on the “Rationale” on how and when the ERC-7578 properties should be set:

> When a token is minted, its properties SHOULD be initialized beforehand. By not initializing a token’s properties before minting, one risks that the asset’s provenance represented by the token cannot be established.

Thank you once again, and we look forward to any further feedback that can improve the standard, as we’ve requested to move it to the review stage.

---

**SamWilsn** (2024-07-01):

You should keep requirements (defined with the uppercase keywords like “SHOULD”) in the specification section. Otherwise, that change looks good!

---

**Vidor** (2024-07-01):

Thanks [@SamWilsn](/u/samwilsn) , you’re right that we shouldn’t limit the functionality of properties. We’ve have agreed to remove setting properties from the standard.

---

**Vidor** (2024-07-01):

Thanks again for the quick feedback!

---

**gabrielstoica** (2025-01-04):

This ERC has been moved to Last Call. We’d appreciate any feedback until it’s moved to Final.

