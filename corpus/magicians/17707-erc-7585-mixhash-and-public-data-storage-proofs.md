---
source: magicians
topic_id: 17707
title: "ERC-7585: MixHash and Public Data Storage Proofs"
author: waterflier
date: "2023-12-28"
category: ERCs
tags: [erc, nft, erc-721, storage]
url: https://ethereum-magicians.org/t/erc-7585-mixhash-and-public-data-storage-proofs/17707
views: 2355
likes: 6
posts_count: 10
---

# ERC-7585: MixHash and Public Data Storage Proofs

## Abstract

This proposal introduces a design for `minimum value selection` storage proofs on Merkle trees. The design consists of two main components:

1. A hashing algorithm termed MixHash, aimed to replace the commonly used Keccak256 and SHA256 algorithms.
2. Public data storage proofs. This enables anyone to present a proof to a public network, verifying their possession of a copy of specific public data marked by MixHash.

Additionally, the proposal discusses the practical implementation of this design in various scenarios and suggests some improvements to the ERC-721 and ERC-1155 standards.

## Motivation

The ERC-721 and ERC-1155 standards are widely used in the NFT  fields. However, the current standards do not provide a mechanism for verifying the existence of public data. This is a major obstacle to the development of many applications, such as decentralized data markets, decentralized data storage, and decentralized data oracles.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### MixHash

MixHash is a Merkle tree root hash value that incorporates data length information. Its structure is as follows:

```plaintext
     +-----------256 bits MixHash-----------+
High |-2-|----62----|----------192----------| Low

2   bits: Hash algorithm selection, where 0b00 represents SHA256, and 0b10 represents Keccak256. (0b01, 0b11 are reserved)
62  bits: File size. Hence, MixHash can support file sizes up to 2^62-1.
192 bits: The lower 192 bits of the Merkel root node value constructed by the designated hash algorithm.

```

Given a file, we can construct a MixHash through the following defined steps:

1. File MUST Split into 1KB chunks. MUST Pad zeros to the end of the last chunk if needed.
2. Calculate the hash for each chunk and the low 128bits is the Merkle Tree leaf value.
3. Construct a Merkle tree , root node hash algorithm is 256bits, other node use low 128bits of the 256bits hash result.
4. Return the combination of hash type, the file size, and the low 192 bits of the Merkle tree root node hash.

MixHash retains a length of 256 bits, so replacing the widely used Keccak256 and SHA256 with MixHash incurs no additional cost. Although including the file length in the upper 62 bits compromises security to some extent, the 192-bit hash length is already sufficient for defending against hash collisions.

The following is the pseudo code for generating Mixhash:

```python
def generateMixHash(blockHeight,hashType,file):
    chunk_hash_array = []
    for chunk in file:
        if len(chunk)  MAX_BLOCK_DISTANCE) {
       revert("proof expired");
    }
    hash_type = getHashType(mixHash);
    merkle_tree_root = getMerkleTreeRootFromPath(m_path,m_leaf_data,hash_type);
    if(low192(merkle_tree_root) != low192(mixHash)) {
       revert("invalid proof");
    }

    nonce = getNonce(blockHeight);
    proof_result = getMerkleTreeRootFromPath(m_path,m_leaf_data.append(nonce),hash_type);
    last_proof_result,last_prover = getProofResult(mixHash, blockHeight);
    if(proof_result = POW_DIFFICULTY) {
        break;
      }
      noise++
    }
    m_path = getMerkleTreePath(chunk_hash_array, min_index);
    return strorage_proof(mixHash, blockHeight, min_index, m_path, min_chunk,noise);
}
```

Applying this mechanism increases the cost of generating storage proofs, which deviates from our initial intent to reduce the widespread effective storage of public data. Moreover, heavily relying on a PoW-based economic model may allow Suppliers with significant advantages in PoW through specialized hardware to disrupt the basic participatory nature of the game, reducing the widespread distribution of public data. Therefore, it is advised not to enable the PoW mechanism unless absolutely necessary.

### Limitations

1. The storage proofs discussed in this paper are not suitable for storing very small files, as small files inherently struggle to defend against external data source attacks.
2. Public data storage proofs do not address the issue of whether the data is genuinely public. Therefore, it is important to verify the public nature of MixHash in specific scenarios (which is often not easy). Allowing Suppliers to submit storage proofs for any MixHash and receive rewards would lead to a situation where Suppliers create data only they possess and exploit this to gain rewards through constructed attacks, ultimately leading to the collapse of the entire ecosystem.

### ERC Extension Suggestion: Tracking High-Value Public Data by MixHash

We can use the existing Ethereum ecosystem to confirm whether a MixHash is public data and track its value. For any contracts related to unstructured data, the `ERCPublicDataOwner` interface can be implemented. This interface determines whether a specific MixHash is associated with the current contract and attempts to return an Owner address corresponding to a MixHash. Additionally, for the existing and widely recognized NFT ecosystem, we suggest that new ERC-721 and ERC-1155 contracts implement a new extension interface `ERC721MixHashVerify`. This interface can explicitly associate an NFT with a MixHash. The specific interface definition is as follows:

```solidity
/// @title ERCPublicDataOwner Standard, query Owner of the specified MixHash
///  Note: the ERC-165 identifier for this interface is .
interface ERCPublicDataOwner {
    /**
        @notice Queries Owner of public data determined by Mixhash
        @param  mixHash    Mixhash you want to query
        @return            If it is an identified public data, return the Owner address, otherwise 0x0 will be returned
    */
    function getPublicDataOwner(bytes32 mixHash) external view returns (address);
}
```

The `ERC721MixHashVerfiy` extension is OPTIONAL for ERC-721 smart contracts or ERC-1155 smart contracts. This extension can help establish a relationship between specified NFT and MixHash.

```solidity
/// @title ERC721MixHashVerfiy Extension, optional extension
///  Note: the ERC-165 identifier for this interface is .
interface ERC721MixHashVerfiy{
    /**
        @notice Is the tokenId of the NFT is the Mixhash?
        @return           True if the tokenId is MixHash, false if not
    */
    function tokenIdIsMixHash() external view returns (bool);

    /**
        @notice Queries NFT's MixHash
        @param  _tokenId  NFT to be querying
        @return           The target NFT corresponds to MixHash, if it is not Mixhash, it returns 0x0
    */
    function tokenDataHash(uint256 _tokenId) external view returns (bytes32);
}
```

## Rationale

Storage proofs (often referred to as space-time proofs) have long been a subject of interest, with numerous implementations and related projects existing.

1. Compared to existing copy proofs based on zero-knowledge proofs, our storage proof is based on “Nash Consensus,” with its core principles being:
a. The public network (on-chain) cannot verify the optimality of a proof but relies on economic game theory. This significantly reduces the costs of construction and verification.
b. Data without value typically lacks game value and is naturally eliminated from the system. There is no commitment to elusive perpetual storage.
2. It can be fully implemented through smart contracts (although the GAS cost of the current reference implementation is somewhat high), separating storage proof from the economic model.
3. For public data, we do not strictly defend against Sybil attacks. A Sybil attack refers to a Supplier using multiple identities to commit to storing multiple copies of data D (e.g., n copies) while actually storing less (like just one copy) but providing n storage proofs, thereby succeeding in the attack. Strictly preventing Sybil attacks essentially means attaching more additional costs to data storage. The core of our storage proof is to increase the probability of the existence of public data copies through a combination of storage proofs and different economic models, rather than needing to strictly define how many copies exist. Therefore, from the perspective of the design of public data storage proofs, we do not need to defend against Sybil attacks.

## Backwards Compatibility

Using HashType allows storage proofs to be compatible with EVM-compatible public blockchain systems, as well as BTC-Like public blockchain systems. In fact, MixHash could become a new cross-chain value anchor: it can track the value of the same data represented by MixHash across different public blockchain networks using different models, achieving the aggregation of cross-chain values. Considering the need for backward compatibility, we have set the default HashType of MixHash to SHA256. Two categories of HashType remain unused, leaving ample room for future expansion.

## Security Considerations

This storage proof revolves around public data. In demonstrating storage proofs, it often involves sending 1KB segments of the data to the public network. Therefore, please do not use the storage proof design presented in this paper for private data.

The design of MixHash can support storage proofs for private files, but this requires some adjustments in the processing of the original data and the construction of the storage proof. A detailed discussion on the design of storage proofs for private files is beyond the scope of this paper. In fact, some of the projects mentioned in the Reference Implementation section use both public data storage proofs and private data storage proofs.

## Test Cases

PublicDataProofDemo includes test cases written using Hardhat.

## Reference Implementation

PublicDataProofDemo   ([GitHub - buckyos/PublicDataProof](https://github.com/buckyos/PublicDataProof))

- A standard reference implementation

DMC public data inscription

- Based on public data storage certification, a complete economic model and gameplay has been designed on ETH network and BTC inscription network

Learn more background and existing attempts

- DMC Main Chain
- CYFS

## Copyright

Copyright and related rights waived via [CC0]

Pull Request URL is the following:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/177)














####


      `master` ← `buckyos:master`




          opened 01:56AM - 28 Dec 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/c/c0c4813267f9dd74720dc8f4bb88675d097b983d.png)
            waterflier](https://github.com/waterflier)



          [+283
            -0](https://github.com/ethereum/ERCs/pull/177/files)







This proposal introduces a design for `minimum value selection` storage proofs o[…](https://github.com/ethereum/ERCs/pull/177)n Merkle trees. The design consists of two main components:

1. A hashing algorithm termed MixHash, aimed to replace the commonly used Keccak256 and SHA256 algorithms.
2. Public data storage proofs. This enables anyone to present a proof to a public network, verifying their possession of a copy of specific public data marked by MixHash.

Additionally, the proposal discusses the practical implementation of this design in various scenarios and suggests some improvements to the ERC-721 and ERC-1155 standards.

## Replies

**abcoathup** (2023-12-28):

You can just include the link to the ERC PR, as the text of the ERC may change.

---

**waterflier** (2023-12-29):

Thank you for your suggestions.

Before posting the topic, I looked at how others have approached similar issues. I aim to include comprehensive content in the topic to facilitate the discussion, allowing participants to avoid jumping between different sections. When there are updates to the ERC TEXT, I will make sure to synchronize them promptly.

---

**waterflier** (2024-01-04):

I did not see your specific question.

The provided content is pseudocode, the basic idea is to continuously find a random number, `noise`, while keeping the `nonce` unchanged. This is done so that the new combination meets both the minimum value requirement and the difficulty criteria.

---

**fulldecent** (2024-01-18):

Could you please make a PR to move this document to “DRAFT” status?

Also I don’t see why it is presumed that this initiative will get the number 7585.

---

**abcoathup** (2024-01-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Could you please make a PR to move this document to “DRAFT” status?

The original PR is draft status and hasn’t been merged yet.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/177)














####


      `master` ← `buckyos:master`




          opened 01:56AM - 28 Dec 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/c/c0c4813267f9dd74720dc8f4bb88675d097b983d.png)
            waterflier](https://github.com/waterflier)



          [+283
            -0](https://github.com/ethereum/ERCs/pull/177/files)







This proposal introduces a design for `minimum value selection` storage proofs o[…](https://github.com/ethereum/ERCs/pull/177)n Merkle trees. The design consists of two main components:

1. A hashing algorithm termed MixHash, aimed to replace the commonly used Keccak256 and SHA256 algorithms.
2. Public data storage proofs. This enables anyone to present a proof to a public network, verifying their possession of a copy of specific public data marked by MixHash.

Additionally, the proposal discusses the practical implementation of this design in various scenarios and suggests some improvements to the ERC-721 and ERC-1155 standards.












![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Also I don’t see why it is presumed that this initiative will get the number 7585.

7585 was the number issued by an ERC editor.

---

**john4real** (2024-07-01):

Can you explain in detail how ERC-7585 secures private data? And if I upload private files in foggie client, how are my files backed up and how are they secured?

---

**waterflier** (2024-07-01):

The core of ERC7585 is how to verify a storage proof on EVM based on the Merkle tree.

Therefore, if it is private data, the original data should be encrypted (the secret key needs to be saved locally), and then the encrypted data should be saved with the provider. Then the storage proof challenge is performed around the encrypted data.

Remember, never save unencrypted private data on the Internet~

---

**john4real** (2024-08-04):

that helps a lot, thanks

---

**fulldecent** (2024-08-27):

So if we’re looking at a file backup scenario, here is an example. On macOS it saves your backups into a sparse bundle disk image. If you specified a password with your backup, then those files are encrypted and safe to upload publicly.

In this use case your only concern is backing up and ensuring the existence of data. And the fact that others could see some small parts of the encrypted data (for the mix proofs) should be of little concern to you.

