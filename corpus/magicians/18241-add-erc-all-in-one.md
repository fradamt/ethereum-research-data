---
source: magicians
topic_id: 18241
title: "Add ERC: All in one"
author: cleberlucas
date: "2024-01-20"
category: ERCs
tags: [erc, new-erc, all-in-one, allinone, newerc]
url: https://ethereum-magicians.org/t/add-erc-all-in-one/18241
views: 573
likes: 0
posts_count: 1
---

# Add ERC: All in one

## Abstract

The idea involves creating an ERC contract to store the metadata of any contract in just one contract, facilitating the extension of external contracts, since the data will not be stored in them but rather in the ERC contract.

## Motivation

I was working on my thesis, which focuses on storing academic articles on the blockchain. My work has a generic structure that doesn’t guarantee other entities will use the same framework, as their business models may differ in the presentation of articles. Therefore, I developed a contract that stores data in a unified manner, enabling other contracts to store data with any type of structure or extend the existing structure.

## Specification

The following data defines the ERC.

## ERCXLog

### Events:

### MetaDataSended

```solidity
event MetaDataSended(bytes32 token)
```

### MetaDataCleaned

```solidity
event MetaDataCleaned(bytes32 token)
```

### SenderSigned

```solidity
event SenderSigned(address sender)
```

### SignatureTransferred

```solidity
event SignatureTransferred(address sender)
```

## ERCXRules

### Modifiers:

### OnlySenderSigned

```solidity
modifier OnlySenderSigned(struct ERCXStorageModel.Interconnection _interconnection)
```

### IsNotMetadataEmpty

```solidity
modifier IsNotMetadataEmpty(bytes metadata)
```

### IsNotSignedEmpty

```solidity
modifier IsNotSignedEmpty()
```

### IsNotSenderSigned

```solidity
modifier IsNotSenderSigned(struct ERCXStorageModel.Interconnection _interconnection)
```

### IsNotSignatureUsed

```solidity
modifier IsNotSignatureUsed(struct ERCXStorageModel.Interconnection _interconnection)
```

### IsNotMetadataSended

```solidity
modifier IsNotMetadataSended(struct ERCXStorageModel.Data _data, bytes32 token)
```

### IsMetadataSended

```solidity
modifier IsMetadataSended(struct ERCXStorageModel.Data _data, bytes32 token)
```

### IsMetadataSendedBySender

```solidity
modifier IsMetadataSendedBySender(struct ERCXStorageModel.Data _data, bytes32 token)
```

## IERCXSignature

---

### Functions:

### SIGNATURE

```solidity
function SIGNATURE() external pure returns (string signature)
```

## IERCXInterconnection

### Functions:

### Initialize

```solidity
function Initialize() external payable
```

### TransferSignature

```solidity
function TransferSignature(address newSender) external payable
```

## IERCXInteract

### Functions:

### SendMetaData

```solidity
function SendMetaData(bytes metadata) external payable
```

### CleanMetaData

```solidity
function CleanMetaData(bytes32 token) external payable
```

## IERCXSearch

### Functions:

### Tokens

```solidity
function Tokens(string signature) external view returns (bytes32[] tokens)
```

### Signature

```solidity
function Signature(bytes32 token) external view returns (string signature)
```

### MetaData

```solidity
function MetaData(bytes32 token) external view returns (bytes metadata)
```

### Senders

```solidity
function Senders() external view returns (address[] senders)
```

### Signature

```solidity
function Signature(address sender) external view returns (string signature)
```

### Sender

```solidity
function Sender(string signature) external view returns (address sender)
```

## Rationale

This approach ensures a standardized and operational way of storing metadata for any contracts. By centralizing the storage of metadata in the ERC contract, the system becomes more modular and adaptable to different business models. Overall, this design promotes flexibility, reusability, and ease of maintenance for external contracts.

## Security Considerations

The security of `TransferSignature()` must come from the external contract.

The external contract must inherit the `IERCXSignature`  interface. This ensures that only the single-signature contract can change your stored data.
