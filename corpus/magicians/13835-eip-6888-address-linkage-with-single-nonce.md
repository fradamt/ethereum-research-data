---
source: magicians
topic_id: 13835
title: "EIP-6888: Address Linkage with Single Nonce"
author: hiddenintheworld
date: "2023-04-15"
category: EIPs
tags: [account-abstraction]
url: https://ethereum-magicians.org/t/eip-6888-address-linkage-with-single-nonce/13835
views: 711
likes: 2
posts_count: 3
---

# EIP-6888: Address Linkage with Single Nonce

EIP: 6888

Title: Address Linkage with Single Nonce

Author: sunrize.eth, hiddenintheworld.eth

Status: Draft

Type: Standards Track

Category: ERC

Created: [2023-04-16]

## Simple Summary

This EIP proposes a standard for linking Ethereum addresses using a simple smart contract that maps public addresses. The contract uses signed messages and a single nonce value to establish and revoke linkages between two addresses. This standard can be utilized for notification and wallet control modules, and it is fully on-chain.

## Abstract

This standard proposes the use of a “Linkage” contract that allows an Ethereum address (owner) to link to another address (servant) using signed messages and a single nonce value. The linkage can be created or revoked using the owner’s or the servant’s signed message, which increases the nonce value for the servant’s address.

This standard can be utilized for fully on-chain notification and wallet control modules that require a secure and reliable solution. The use of signed messages and a single nonce value ensures that all transactions are recorded on the blockchain and cannot be manipulated or tampered with off-chain.

## Specification

Definitions

`ownerOf`: A mapping of address to address, representing the linkage between a servant address and its owner address.

`nonces`: A mapping of address to uint256, representing the nonce value for each servant address.

## Smart contract implementation

Here is the full code:

```auto
pragma solidity ^0.8.0;

contract Linkage {
    mapping(address => address) public ownerOf;
    mapping(address => uint256) public nonces;

    function createLinkage(address servant, address owner, bytes memory signatureServant, bytes memory signatureOwner) public {
        require(ownerOf[servant] == address(0), "Linkage already exists for servant");

        bytes32 messageServant = keccak256(abi.encodePacked(owner, uint256(1), nonces[servant]));
        bytes32 messageOwner = keccak256(abi.encodePacked(servant, uint256(0)));

        require(recoverSigner(messageServant, signatureServant) == servant, "Invalid signatureServant");
        require(recoverSigner(messageOwner, signatureOwner) == owner, "Invalid signatureOwner");

        ownerOf[servant] = owner;
        nonces[servant]++;
    }

    function revokeLinkage(address servant, address owner, bytes memory signature) public {
        require(ownerOf[servant] == owner, "Linkage does not exist or is already revoked");

        bytes32 messageServant = keccak256(abi.encodePacked(owner, uint256(3), nonces[servant]));
        bytes32 messageOwner = keccak256(abi.encodePacked(servant, uint256(2)));

        address signer = recoverSigner(messageServant, signature);
        if (signer != servant) {
            signer = recoverSigner(messageOwner, signature);
            require(signer == owner, "Invalid signature");
        }

        ownerOf[servant] = address(0);
        nonces[servant]++;
    }

    function recoverSigner(bytes32 _hash, bytes memory _signature) internal pure returns (address) {
        bytes32 r;
        bytes32 s;
        uint8 v;

        if (_signature.length != 65) {
            return (address(0));
        }

        assembly {
            r := mload(add(_signature, 32))
            s := mload(add(_signature, 64))
            v := byte(0, mload(add(_signature, 96)))
        }

        if (v < 27) {
            v += 27;
        }

        if (v != 27 && v != 28) {
            return (address(0));
        } else {
            return ecrecover(keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", _hash)), v, r, s);
        }
    }
}
```

## Methods

`createLinkage(address servant, address owner, bytes memory signatureServant, bytes memory signatureOwner)`

This function creates a linkage between the servant and owner addresses. The linkage is established only when the provided signatures of both parties are valid. The function increases the nonce value for the servant address.

`revokeLinkage(address servant, address owner, bytes memory signature)`

This function revokes the linkage between the servant and owner addresses. The function requires a valid signature from either the servant or the owner. The function increases the nonce value for the servant address.

`recoverSigner(bytes32 _hash, bytes memory _signature) internal pure returns (address)`

This internal function recovers the signer’s address from a given message hash and its corresponding signature.

## Rationale

This standard was created to address the issue of open-source wallets like Metamask, which do not allow the use of private keys for encryption and decryption. By creating a simple smart contract that maps public addresses, users can link their addresses and utilize the contract for notification and wallet control modules. The use of signed messages and a single nonce value ensures security against replay attacks.

## Backwards Compatibility

The proposed contract is not directly compatible with existing Ethereum token standards such as ERC20, ERC721, and ERC1155. However, it can be utilized alongside them or integrated into a new token standard with additional functionalities.

## Security Considerations

The security of this standard relies on the uniqueness of the signed messages. Each signed message must include the source and target addresses to prevent replay attacks. The nonce for the servant address ensures that once a linkage is created or revoked, the same transaction cannot be used again.

## Copyright

Copyright and related rights waived via CC0.

(NOTE: The EIP number and creation date will be provided when you submit the EIP to the Ethereum Improvement Proposals repository.)

---

## Replies

**jhfnetboy** (2023-04-18):

Thanks for this good idea to maintain a linkage between the two addresses.

I have some questions:

1. Could you give scenarios to explain what time we should create or revoke a linkage?
If we create one linkage and never revoke it, what will happen?
What factors influence the removal of this linkage? a timer? a trigger?
2. Based on the linkage we create, what can I do?
Does the owner’s address receive some tokes, and will the servant’s address be notified? like, subscribe to an event?
or should we add more functions to this contract to implement more features through this linkage?

glad to talk about this.

---

**hiddenintheworld** (2023-04-23):

1. A scenario could be if you want to have an address(0xabc) that someone else owns, you ask them for permission to link the address, then on another smart contract you can execute orders based on linkage, if there is no linkage, on the smart contract then since the address(0xabc) does not belong to you, you cannot execute orders on behalf of that address.
2. You can simply by creating an SDK, or some API to write/read from this smart contract. This smart contract is already optimized and there could be improvements where multiple parties could be linked to each other.

