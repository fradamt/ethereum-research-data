---
source: magicians
topic_id: 13321
title: "EIP-X: Batched Transfers for ERC721"
author: collect9
date: "2023-03-15"
category: EIPs
tags: [erc, nft, erc-721, gas]
url: https://ethereum-magicians.org/t/eip-x-batched-transfers-for-erc721/13321
views: 1097
likes: 2
posts_count: 3
---

# EIP-X: Batched Transfers for ERC721

| eip | title | author | discussions-to | status | type | category | created | requires |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X | Safe Batched Transfers | Arthur Suszko (@collect9) | Eth Magicians | Draft | Standards Track | ERC | 2023-03-14 | 721 |

## Simple Summary

An extension of the ERC721 standard that provides safe batch transfer functions. Another similar ERC already exists ([ERC1412 [1]](https://github.com/ethereum/EIPs/issues/1412)), but feels incomplete. This EIP expands on what ERC1412 did but with additional efficiency improvements and capabilities.

## Abstract

Smart contracts are not efficiently mutable; thus they must be future proofed as much as possible prior to deployment. The ERC721 extension presented in the EIP accomplishes some of that future-proofing, by standardizing a way to transfer multiple ERC721 tokens requiring multiple transactions. Current methods, such as delegating batch transfer to an operator approved proxy contract, use more gas than is necessary. The benchmarks presented demonstrate the savings of native batch transfer capability, versus that of an operator approved proxy contract. Even more savings are realized when calling the contract direct.

## Motivation

We have witnessed Ethereum gas fees sustain 100+ GWEI. Such fees make transferring many NFTs between two wallets too expensive to perform. Often, operator approved proxy contracts are used to facilitate NFT batch transfers, effectively reducing the transfer cost per token.

Contrary to popular belief, delegation of batch transfers to proxy contracts is not nearly as efficient as an ERC721 contract being able to natively batch transfer itself; the benchmarks of this EIP below show a 24-32% reduction in safe transfer costs from a proxy contract for batches sized 10-100. Additionally, individual users may perform batch transfer without the overhead of a proxy contract, further increasing the gas savings to 28-35% for batched sized 10-100. Such reduction in gas usage would go a long way in reducing promoting the health of the network by lowering its demand load and thus gas fees.

## Specification

#### The Interface

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/* @dev Note: Interface for EIP-XXXX
 */
interface IERCXXXX {
    // Only one emit event needed per TransferBatch
    event TransferBatch(address indexed from, address indexed to, uint256[] tokenIds);

    // Batch transfer from
    function safeTransferBatchFrom(address from, address to, uint256[] calldata tokenIds) external;

    // Batch transfer from (bytes memory data ERC721 spec version)
    function safeTransferBatchFrom(address from, address to, uint256[] calldata tokenIds, bytes memory data) external;

    // Batch transfer from to batch
    function safeBatchTransferBatchFrom(address from, address[] calldata to, uint256[][] calldata tokenIds) external;

    // Batch transfer from to batch (bytes memory data ERC721 spec version)
    function safeBatchTransferBatchFrom(address from, address[] calldata to, uint256[][] calldata tokenIds, bytes[] memory data) external;
}
```

#### Additional

```auto
/**
* @dev See {IERC165-supportsInterface}.
*/
function supportsInterface(bytes4 interfaceId)
    public view
    override(IERC165, ERC721)
    returns (bool) {
        return interfaceId == type(IERCXXXX).interfaceId || super.supportsInterface(interfaceId);
}
```

#### Implementation Examples

```auto
error InputSizesMisMatch();
error NonERC721Receiver();

/**
 * @dev See {IERCXXXX-safeTransferBatchFrom}.
 */
function safeTransferBatchFrom(address from, address to, uint256[] calldata tokenIds)
public virtual override {
    _transferBatch(from, to, tokenIds);
    // Only need to check the first token when going to same address
    if (!_checkOnERC721Received(from, to, tokenIds[0], "")) {
        revert NonERC721Receiver();
    }
}

/**
 * @dev See {IERCXXXX-safeBatchTransferBatchFrom}.
 */
function safeBatchTransferBatchFrom(address from, address[] calldata to, uint256[][] calldata tokenIds)
public virtual override {
    uint256 _batchSize = tokenIds.length;
    if (to.length != _batchSize) {
        revert InputSizesMisMatch();
    }
    for (uint256 i; i<_batchSize;) {
        safeTransferBatchFrom(from, to[i], tokenIds[i]);
        unchecked {++i;}
    }
}
```

## Test Cases

Two ERC721 contracts are benchmarked within the Remix VM: one with the extension - referred to as the test contract, and another without - the control contract, which the base ERC721 standard contract. Both contracts are called from an approved operator proxy contract. The transaction gas costs and reductions in costs are as follows:

| Transfer Batch Size | Proxy to Control Gas Cost | Proxy to Test Gas Cost | Direct to Test Gas Cost | Proxy Reduction | Direct Reduction |
| --- | --- | --- | --- | --- | --- |
| 1 | 52332 | 50730 | 46921 | 3.1% | 10.3% |
| 2 | 65302 | 59397 | 55582 | 9.0% | 14.9% |
| 5 | 104212 | 85398 | 81565 | 18.1% | 21.7% |
| 10 | 169062 | 128733 | 124870 | 23.9% | 26.1% |
| 100 | 1336362 | 908808 | 868302 | 32.0% | 35.0% |

#### Test Code

##### Base ERC721 Derived Contract

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

/**
* @dev Original ERC721 without any extensions.
*/
contract OriginalTokenContract is ERC721 {
    constructor() ERC721("Original NFTs", "ONFTs") {
        for (uint256 i; i<144;) {
            _mint(_msgSender(), i);
            unchecked {++i;}
        }
    }
}
```

##### ERCXXXX ERC721 Derived Contract

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./erc721-EIPXXXX.sol"; // ERC721 with IERCXXXX implemented

/**
* @dev Updated ERC721 with EIP extension.
*/
contract UpdatedTokenContract is ERC721 {
    constructor() ERC721("EIP NFTs", "ENFTs") {
        for (uint256 i; i<144;) {
            _mint(_msgSender(), i);
            unchecked {++i;}
        }
    }
}
```

##### Proxy Contract

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "./interfaces/IERCXXXX.sol";

/**
* @dev This a proxy contract that one would build to
* achieve batching of the original ERC721 contract.
* Note: While a proxy contract is no longer needed
* with the EIP extension, we still include it here for
* benchmark purposes as other dApps will act as a
* proxy anyway, thus benchmarks are taken from the proxy.
*/
contract Proxy {

    address public immutable contractTokenOriginal;
    address public immutable contractTokenUpdated;

    constructor(address _contractTokenOriginal, address _contractTokenUpdated) {
        contractTokenOriginal = _contractTokenOriginal;
        contractTokenUpdated = _contractTokenUpdated;
    }

    /**
     * @dev Batched transfer from the original ERC721 contract.
     */
    function safeTransfer(address from, address to, uint256[] calldata tokenIds)
    public {
        uint256 _batchSize = tokenIds.length;
        for (uint256 i; i<_batchSize;) {
            IERC721(contractTokenOriginal).safeTransferFrom(from, to, tokenIds[i]);
            unchecked {++i;}
        }
    }

    /**
     * @dev Batched transfer from the updated ERC721 contract.
     */
    function safeTransferBatch(address from, address to, uint256[] calldata tokenIds)
    public {
        IERCXXXX(contractTokenUpdated).safeTransferBatchFrom(from, to, tokenIds);
    }
}
```

## Rationale

Benchmarks show the EIP extended contract sees immediate gas savings over the control contract with just a batch of two tokens. The test contract exceeds gas savings of over ~4000 gas units per token over larger transfers (>10 tokens). A batch of 100 tokens were tested to save ~4300 gas units per token, suggesting a plateau around this number.

If this were to become widely adopted, the cumulative gas savings of batched transfers could be massive.

Such batching also introduces the capability for a proxy contract to batch transfer to a batch of addresses, as implemented by `safeBatchTransferBatchFrom(...)`. For users interacting directly with the ERC721 contract, such a capability opens up the new possibilities such as being able to more cheaply gift NFTs to multiple addresses at once, without the overhead of a  proxy contract.

## Backwards Compatibility

To take full advantage of batching, the following *MUST* be done:

1. Only a single event, event TransferBatch(...) MUST be emitted to summarizes all token transfers per batch to address.
2. Token owner balances MUST only be updated one time per batch.
3. _checkOnERC721Received() MUST only be called one time per batch to address.

Thus, the original private `_transfer()` function is not suitable for batched transfer, as it performs event emissions and balance update for every transfer. To maintain backwards compatibility, the ERC *SHOULD* include a new private `_transferBatch()` function. However, it is highly *RECOMMENDED* to update the original `_transfer()` so that duplicate code does not need to be inlined within internal `_transferBatch()`.

A new internal `_transferBatch()` function cannot be written into the extension by itself as it tries to read from storage that is marked as private in the ERC721 contract. Thus, to maintain full backwards compatibility, it would be *REQUIRED* for `_transferBatch()` to be hard coded into the ERC721 base contract. Alternatively, state variables this EIP reads from *MAY* be changed to internal.

## Copyright

Copyright and related rights waived via CC0

## Citations

[1] [ERC1412: Batch Transfers For Non-Fungible Tokens · Issue #1412 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1412)

## Replies

**abcoathup** (2023-03-16):

Welcome ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

Suggest reading: [Guidelines on How to write EIP. Do's and Don'ts including examples | by Anett | The Fellowship of Ethereum Magicians | Medium](https://medium.com/ethereum-magicians/guide-on-how-to-write-perfect-eip-70488ad70bec)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/collect9/48/8876_2.png) collect9:

> I have no idea how the EIP numbering is done. Did I do this right?

EIP editors assign an EIP number (generally the PR number, but the decision is with the editors) (from: [EIP-1: EIP Purpose and Guidelines](https://eips.ethereum.org/EIPS/eip-1#eip-numbers))

---

**collect9** (2023-03-16):

Thank you! I’ve removed the EIP wherever it shows up and have replaced it with EIP-X.

