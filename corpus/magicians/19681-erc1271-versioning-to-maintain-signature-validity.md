---
source: magicians
topic_id: 19681
title: ERC1271 versioning to maintain signature validity
author: kylekaplan
date: "2024-04-16"
category: Magicians > Primordial Soup
tags: [account-abstraction, signatures, erc-1271]
url: https://ethereum-magicians.org/t/erc1271-versioning-to-maintain-signature-validity/19681
views: 920
likes: 3
posts_count: 2
---

# ERC1271 versioning to maintain signature validity

## Intro

Off-chain ERC1271 Signatures are not guaranteed to be valid in the future, because the `isValidSignature` function can be changed.

## Problem

This creates a problem for any application that would like to use signatures to prove validity of statements and also support smart accounts.

Simple example of signers changing causing the validity of a signature to change:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/c/cdc07f04996e7a9905e86afae5b4b3d85da3a4fa_2_690x297.jpeg)image1898×818 148 KB](https://ethereum-magicians.org/uploads/default/cdc07f04996e7a9905e86afae5b4b3d85da3a4fa)

From [Peter Robinson’s Ethereum Engineering Group presentation](https://www.youtube.com/watch?v=p_UG1x53TWc)

## Proposal

#### Standard way of updating isValidSignature function

I propose we create a standard way for updating the `isValidSignature` function so that we can keep track of previous versions.

One possible solution is to store in state previous ERC1271 verifiers and timestamps, which can be updated by calling an `updateIsValidSignature` function. Then a `wasValidSignature` function can be called and reference previous verifiers, when determining if a signature was valid.

The way state is stored can be external to this standard, but could look something like this:

### State:

```auto
// create a VerifierStruct which includes a timestamp and ERC1271 verifier
// keep an array of VerifierStructs that updateIsValidSignature will push to

struct VerifierStruct {
  timestamp: uint64;
  verifier: ERC1271; // ERC1271 contract address
}

VerifierStruct[] public verifiers = [];
```

OR

```auto
// Keep a mapping of timestamps and ERC1271 verifiers that updateIsValidSignature will add to

mapping(uint64 => ERC1271) public verifiers;
```

### Functions:

```auto
updateIsValidSignature:
@dev pushes to the array a new contract address with a current timestamp
@param _contract An ERC1271 contract address
function updateIsValidSignature(address _contract) external;
```

```auto
wasValidSignature:
@dev looks up which contract to use based on timestamp, and calls appropriate function
@return The bytes4 magic value 0x1626ba7e when function passes
@param _timestamp Timestamp to check for
@param _hash Hash of the data to be signed
@param _signature Signature byte array associated with _hash
@param _data arbitrary extra data used for verification
function wasValidSignature(
    unit64 _timestamp,
    bytes32 _hash,
    bytes memory _signature,
    bytes _data
) public view returns(bytes4);
```

### Events:

```auto
event ERC1271CheckerUpdated(address indexed newChecker)
```

---

I would love feedback and suggestions on this and other possible solutions for this problem. Thanks [@sina](/u/sina) for your help on this design so far.

## Replies

**sina** (2024-05-28):

Gm, we have a draft for a standard proposal @ [[EXTERNAL] DRAFT-EIP-1271T - HackMD](https://hackmd.io/XY84l1BcSPKSGl0Y8FtFPA), would love feedback from anyone interested ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12)

