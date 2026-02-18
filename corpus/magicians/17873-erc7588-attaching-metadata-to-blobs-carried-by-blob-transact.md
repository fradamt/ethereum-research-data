---
source: magicians
topic_id: 17873
title: "ERC7588: Attaching metadata to blobs carried by blob transactions"
author: gavfu
date: "2024-01-05"
category: EIPs
tags: [rollups, sharding, eip-4844]
url: https://ethereum-magicians.org/t/erc7588-attaching-metadata-to-blobs-carried-by-blob-transactions/17873
views: 2000
likes: 6
posts_count: 8
---

# ERC7588: Attaching metadata to blobs carried by blob transactions

## Abstract

This EIP proposes a standard for attaching metadata to blobs carried by shard blob transactions, as introduced by EIP-4844. The metadata is a JSON object that conforms to a predefined schema and is encoded in hexadecimal with UTF-8 character encoding. The metadata is put in the `data` field of the blob transaction.

## Motivation

EIP-4844 defines a new type of transaction, called “blob transaction”, which contains a list of blobs and their KZG commitments and proofs. Blob transactions are designed to be used by rollups to post their layer 2 transaction data to Ethereum layer 1.

Typically, rollups keep track of their own posted blob transactions, download blobs and decode their layer 2 transaction data from blobs on demand. However, some third party solutions, such as Portal Network, blobscan, etc., may also index all the blobs ever posted to Ethereum and provide querying services of them. It would greatly improve the visibility and auditability of blobs if we could attach some metadata to the blobs, such as `originator`, `description`, `content_type`, etc.

Moreover, some `dStorage` projects may use blob transactions to post user data to Ethereum, sync and permanently store the blobs off-chain for future retrieval. Attaching metadata to blobs would also inspire novel applications, such as inscriptions, etc.

## Specification

### Metadata JSON Schema

The metadata is a JSON object that conforms to the following schema:

```json
{
    "title": "Blobs Metadata",
    "type": "object",
    "properties": {
        "originator": {
            "type": "string",
            "description": "Identifies the originator of the carried blobs"
        },
        "description": {
            "type": "string",
            "description": "Describes the contents of the blobs"
        },
        "content_type": {
            "type": "string",
            "description": "Describes the mime type of the blobs"
        },
        "extras": {
            "type": "string",
            "description": "Dynamic extra information of the blobs"
        },
        "blobs": {
            "type": "array",
            "items": {
                "description": {
                    "type": "string",
                    "description": "Describes the content of the i'th blob"
                },
                "content_type": {
                    "type": "string",
                    "description": "Describes the mime type of the i'th blob"
                },
                "extras": {
                    "type": "string",
                    "description": "Dynamic extra information of the i'th blob"
                },
            }
        }
    }
}
```

### Metadata Encoding

The metadata JSON object should be converted to hexadecimal with UTF-8 character encoding, and put in the `data` field of the blob transaction.

## Rationale

The rationale for this EIP is to provide a standard way for attaching metadata to blobs carried by blob transactions, which can enhance the auditability and usability of blob transactions. The metadata can be used by various applications and services that post or index blob transactions, such as rollups, `dStorage` projects, blobscan, etc. The metadata can also provide additional context and information about the blobs, such as their `originator`, `description`, `content type`, etc.

The metadata is encoded in hexadecimal with UTF-8 character encoding, and put in the `data` field of the blob transaction, to follow the convention of regular transactions. The metadata is a JSON object that conforms to a predefined schema, to ensure the consistency and validity of the metadata format. The schema defines the properties of the metadata, such as `originator`, `description`, `content_type`, `extras`, and `blobs`. The `originator` property identifies the originator of the carried blobs, which can be a rollup, a `dStorage` project, or any other entity that uses blob transactions. The `description` property describes the contents of the blobs, which can be a summary, a title, a tag, or any other relevant information. The `content_type` property describes the mime type of the blobs, which can be used to determine how to decode and interpret the blobs. The `extras` property provides dynamic extra information of the blobs, which can be used to store any additional data that is not covered by the other properties. The `blobs` property is an array that contains the metadata of each individual blob in the blob transaction. Each element in the array is an object that has the same properties as the metadata object, except for the `originator` property, which is omitted. The `blobs` property allows for specifying the metadata of each blob separately, which can be useful for cases where the blobs have different contents or types.

# Backwards Compatibility

This EIP is backward compatible with EIP-4844, as it does not modify the structure or functionality of blob transactions, but only adds an optional metadata field to them.

## Security Considerations

This EIP does not introduce any new security risks or vulnerabilities, as the metadata is only an informational field that does not affect the execution or validity of blob transactions. However, users and applications should be aware of the following potential issues:

- The metadata is not verified or enforced by the consensus layer, and therefore it may not be accurate or trustworthy. Users and applications should not rely on the metadata for critical or sensitive operations, and should always verify the contents and sources of the blobs themselves.
- The metadata may contain malicious or harmful data, such as spam, phishing, malware, etc. Users and applications should not blindly trust or execute the metadata, and should always scan and sanitize the metadata before using it.
- The metadata may increase the gas cost of blob transactions, as more data is included in the data field. Users and applications should balance the benefits and costs of using the metadata, and should optimize the size and format of the metadata to reduce the gas cost.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**Mani-T** (2024-01-05):

Good thought. This offers beneficial enhancements for handling blockchain data.

---

**abcoathup** (2024-01-05):

Renamed title to assigned ERC number.

---

**0xBreadguy** (2024-03-09):

Hey [@abcoathup](/u/abcoathup) - thinking on this, I wonder if it would be reasonable to add an element to denote blob reconstruction/composibility.

We have `extras` to play with, but as blobs become used for various `dStorage` projects I’d have to imagine we’d want to have standardized elements to denote:

- Completeness
- References to other blobs for incomplete blobs

Imagine a scenario where something as large as a library is being uploaded across several blobs. To be functional, each blob would have to have a reference, creating a trail of sorts, to be able to rebuild the library in full.

---

**SamWilsn** (2024-05-06):

How does the contract get any relevant arguments if the `data` field is completely filled with metadata?

---

**gavfu** (2024-05-09):

In most scenarios, blob transactions are primarily used to post blobs, and the `data` field remains unused. Therefore, placing the metadata JSON in the `data` field is a straightforward approach.

However, if a blob transaction also invokes smart contract functions, the `data` field becomes occupied. In such cases, this EIP proposal does not directly apply. Instead, an alternative solution is needed. One possibility is to create a separate smart contract (either precompiled or commonly used, such as multicall3) specifically designed to track metadata. Users can then include the metadata as smart contract function call arguments within that contract.

---

**gavfu** (2024-05-09):

BTW, I’ve created a project demonstrating how to send an EIP-4844 blob transaction to Sepolia with this metadata extension:

https://github.com/gavfu/exp-blobtx

As an example, you could check this blob tx on Sepolia:

https://sepolia.etherscan.io/tx/0xc177b7159aba6372bbf296cd7711793324abea797289cf75e72fbd514bd6ce31

---

**gavfu** (2024-05-09):

And the metadata could be directly viewed on etherscan:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5e9d16f5a7c2e316e2b84ba8f0c5d64eb9a5fc0f_2_690x255.png)image2714×1004 324 KB](https://ethereum-magicians.org/uploads/default/5e9d16f5a7c2e316e2b84ba8f0c5d64eb9a5fc0f)

