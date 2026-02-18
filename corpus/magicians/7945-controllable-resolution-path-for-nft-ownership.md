---
source: magicians
topic_id: 7945
title: Controllable Resolution Path For NFT Ownership
author: cucrisis
date: "2022-01-09"
category: EIPs
tags: [nft, erc-721, erc1155]
url: https://ethereum-magicians.org/t/controllable-resolution-path-for-nft-ownership/7945
views: 670
likes: 0
posts_count: 1
---

# Controllable Resolution Path For NFT Ownership

Current NFT standards such as ERC721, ERC1155 use a mapping of the NFT owner wallet address and the asset `tokenId` to store and resolve representation of ownership. In both ERC721 and ERC1155 when a new instance is minted/created a new record is added to the ownership mapping. To display an NFT knowing the `tokenId` the entry-point to the contract is usually either through a call to `tokenURI` or `uri`, both intended to return a `URI` that leads to the NFT metadata object. In observed NFTs implementations the full `URI` or a `fragment` of it can *sometimes* be controlled by the owner of the collection, but **never by the owner of the NFT instance (token)**. After the NFT instance `URI` is resolved to the metadata object, the scheme most likely contains `pointers` to the location of the NFT instance digital asset object (JPG, PNG, MOV …etc.), mostly in the form of a `URI`. Owners of the digital asset object have no control over the `pointers` value as well, **making it impossible to fully own the asset lifecycle.**

**Problem**

NFT owners have no **control/ownership** of their NFTs digital objects **resolution path**, leading to incomplete ownership representation and potential security risk.

**Potential Solution**

- Metadata reside outside of the contract: NFT standards should include methods that allow assets owners to change the result of tokenURI, uri and equivalent to their own specified value.
- Metadata within the contract: NFT standards should include methods that allow assets owners to change the digital asset media object pointers without affecting the rest of the NFT collection owner resolution path.
Original assets integrity verification: The standard should include function(s) that help validate the authenticity of collection media objects. E.g a function within the collection could return a reference to an object URI or an object itself that help validate all tokenURI, and uri digital objects pointers content authenticity independently if it the location has been changed by its current owner.

```auto
contract OwnableNFT  {
    [...snip...]

    // verify the sender is the owner of the token in the mapping
    modifier onlyNftOwner(uint256 _tokenId) {
        require(NftOwner(_tokenId) == _msgSender(), "Ownable NFT: only token owner can change location");
        _;
    }

     // Change the value of the digital object `pointers`
     function changeURI(uint256 tokenId, string memory newURI) public view onlyNftOwner(tokenId) {
         [...snip...]
     }

    //  Returns assets integrity verification source
     function collectionURI() public view (string memory) {
         [...snip...]
     }

    // Reset URI to default location
    function resetURI(uint256 tokenId, string memory newURI) public view onlyNftOwner(tokenId) {
         [...snip...]
     }
}
```

this way owners can have the digital asset in a location they desire/control, creators can keep a proof of work ownership, and a verification process can be triggered to verify the digital media objects authenticity independently where it resides.
