---
source: magicians
topic_id: 1722
title: "ERC-1537: Auditable Storage Passing"
author: johba
date: "2018-10-29"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-1537-auditable-storage-passing/1722
views: 1242
likes: 1
posts_count: 4
---

# ERC-1537: Auditable Storage Passing

## tl;dr

Encapsulating contract storage into a transferable, ownable token allows contracts to migrate across chain with the state that they manage. We think a standard way to pass contract storage through bridges for Plasma and sidechains will allow for more flexible contract development and better user experience.

## Sumary

We propose to extend non-fungible tokens (NFTs) with the ability to store data. This proposal wraps a store of data (eg. partricia tree) into the ERC721 interface. The ownership of the token can now grant access to the storage for writing and provides an audit trail for data updates across chains.

```auto
contract StorageToken is ERC721Token {

  mapping(uint256 => bytes32) public root;

  function readRoot(uint256 _tokenId) public view returns (bytes32) {
    return root[_tokenId];
  }

  function verifiedRead(
    uint256 _tokenId,     // the token holding the storage root
    bytes _key,           // key used to do lookup in storage trie
    bytes _value,         // value expected to be returned
    uint _branchMask,     // position of value in trie
    bytes32[] _siblings   // proof of inclusion
  ) public view returns (bool) {
    require(exists(_tokenId));
    return tree.verifyProof(root[_tokenId], _key, _value, _branchMask, _siblings);
  }

  function writeRoot(uint256 _tokenId, bytes32 _newRoot) public {
    require(msg.sender == ownerOf(_tokenId));
    root[_tokenId] = _newRoot;
  }
}
```

## Replies

**johba** (2018-10-29):

[EIP1537](https://github.com/ethereum/EIPs/issues/1537)

---

**johba** (2018-11-03):

this might proof to be very relevant for efficient membership proofs, insertion and deletion: https://osf.io/8mcnh/

---

**johba** (2018-11-07):

Jan has started some implementation of the CSMT here: https://github.com/parsec-labs/spending-conditions/issues/1

