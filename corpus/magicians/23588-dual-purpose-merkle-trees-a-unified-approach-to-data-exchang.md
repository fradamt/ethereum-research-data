---
source: magicians
topic_id: 23588
title: "Dual-Purpose Merkle Trees: A Unified Approach to Data Exchange and Selective Disclosure Proofs"
author: luke
date: "2025-04-17"
category: Web
tags: []
url: https://ethereum-magicians.org/t/dual-purpose-merkle-trees-a-unified-approach-to-data-exchange-and-selective-disclosure-proofs/23588
views: 214
likes: 1
posts_count: 9
---

# Dual-Purpose Merkle Trees: A Unified Approach to Data Exchange and Selective Disclosure Proofs

Hello Ethereum Magicians community,

I’d like to share an approach I’m developing for Merkle trees that serves a dual purpose: both complete data exchange and selective disclosure proofs in a single structure. This design is particularly relevant for Ethereum Attestation Service (EAS) implementations and other onchain attestation scenarios.

## The Dual-Purpose Pattern

Rather than creating separate structures for data storage and proof verification, my approach uses a single Merkle tree that can:

1. Exchange Data: Share complete or partial data between systems (API-to-API exchange)
2. Create Selective Disclosure Proofs: Allow end users to reveal only specific parts when sharing with third parties
3. Verify Against Onchain Attestations: Match the root hash against attestations stored on the blockchain

The key insight is that all these use cases can be served by the same data structure with appropriate serialization policies.

## Application to EAS and Onchain Attestations

This pattern is especially valuable in the context of Ethereum Attestation Service and other attestation frameworks, where:

1. Issuers create attestations with a Merkle root of the complete data
2. Users receive the complete Merkle tree with all data
3. Verifiers accept selective disclosure proofs derived from the original tree
4. Everyone can verify against the same onchain attestation

## Key Design Choice: Data-Agnostic Leaves

A distinctive design decision in this implementation is that each leaf can contain arbitrary data without a predefined schema or structure. Unlike systems that require specific field names at the leaf level, this approach:

1. Treats Data as Opaque Values: The Merkle tree doesn’t dictate what’s in each leaf - it could be a JSON object, a single value, or any other data format
2. Uses Content Type for Context: The format is defined by the content type, not by the tree structure
3. Separates Content from Structure: The tree structure focuses on cryptographic relationships, not data semantics

This design creates exceptional flexibility, where:

```auto
// A leaf's data could be a simple JSON key-value pair
Leaf 1: { "fullName": "John Doe" }

// Or a more complex nested object
Leaf 2: { "address": { "street": "123 Main St", "city": "Anytown" } }

// Or even non-JSON data
Leaf 3:
```

The benefit of this approach is that developers can organize data in whatever way makes sense for their application. While I typically use one JSON key-value pair per leaf for maximum selective disclosure flexibility, the implementation doesn’t enforce this pattern - it’s a choice left to the application.

## Implementation Details

My implementation includes several key features:

```csharp
// Create a Merkle tree with all user data
var tree = new MerkleTree();
var userData = new Dictionary
{
    { "fullName", "John Doe" },
    { "dob", "1990-01-15" },
    { "passport", "AB123456" },
    { "address", "123 Main St, Anytown" },
    { "ssn", "123-45-6789" }
};

// Add all fields with automatic per-leaf random salts
tree.AddJsonLeaves(userData);
tree.RecomputeSha256Root();

// The root hash can be stored onchain as an attestation
Hex rootHash = tree.Root;

// OPTION 1: Complete data exchange (API-to-API)
string completeJson = tree.ToJson(); // Contains all fields

// OPTION 2: Selective disclosure (for any scenario)
Predicate hideSSN = leaf =>
    leaf.TryReadText(out string text) && text.Contains("ssn");
string proofWithoutSSN = tree.ToJson(hideSSN);
```

When the tree is serialized for selective disclosure, it includes:

- All metadata needed for verification
- Full data for disclosed fields
- Only hashes for private fields

### The Role of Content Type

A distinctive feature of this implementation is the `contentType` field for each leaf, which:

1. Ensures Data Integrity: Specifies how the data should be interpreted and processed
2. Supports Multiple Formats: Handles JSON, plain text, binary data, or hex-encoded content
3. Standardizes Encoding: Uses MIME types with charset and encoding information (e.g., “application/json; charset=utf-8; encoding=hex”)
4. Enables Smart Processing: Allows verifiers to properly decode and use the data without guesswork

For example, the content type `application/json; charset=utf-8; encoding=hex` tells us:

- The data is a JSON object
- It’s UTF-8 encoded text
- It’s represented in hexadecimal format in the tree

This approach creates a self-describing data structure that can be safely exchanged between different systems while preserving the original data format and semantics.

### Example JSON Output

Here’s what a selective disclosure structure looks like in JSON (with document number redacted):

```json
{
  "leaves": [
    {
      "data": "0x7b22646f63756d656e7454797065223a2270617373706f7274227d",
      "salt": "0x3d29e942cc77a7e77dad43bfbcbd5be3",
      "hash": "0xe77007d7627eb3eb334a556343a8ef0b5c9582061195441b2d9e18b32501897f",
      "contentType": "application/json; charset=utf-8; encoding=hex"
    },
    {
      "hash": "0xf4d2c8036badd107e396d4f05c7c6fc174957e4d2107cc3f4aa805f92deeeb63"
    },
    {
      "data": "0x7b22697373756544617465223a22323032302d30312d3031227d",
      "salt": "0x24c29488605b00e641326f6100284241",
      "hash": "0x1b3bccc577633c54c0aead00bae2d7ddb8a25fd93e4ac2e2e0b36b9d154f30b9",
      "contentType": "application/json; charset=utf-8; encoding=hex"
    },
    {
      "data": "0x7b2265787069727944617465223a22323033302d30312d3031227d",
      "salt": "0x5d3cd91a0211ed1deb5988a58066cacd",
      "hash": "0xce04b9b0455d7b1ac202f0981429000c9f9c06665b64d6d02ee1299a0502b121",
      "contentType": "application/json; charset=utf-8; encoding=hex"
    },
    {
      "data": "0x7b2269737375696e67436f756e747279223a22556e69746564204b696e67646f6d227d",
      "salt": "0xc59f9924118917267ebc7e6bb69ec354",
      "hash": "0xf06f970de5b098300a7731b9c419fc007fdfcd85d476bc28bb5356d15aff2bbc",
      "contentType": "application/json; charset=utf-8; encoding=hex"
    }
  ],
  "root": "0x1316fc0f3d76988cb4f660bdf97fff70df7bf90a5ff342ffc3baa09ed3c280e5",
  "metadata": {
    "hashAlgorithm": "sha256",
    "version": "1.0"
  }
}
```

In this example, you can see:

1. The document number leaf (second position) has only its hash preserved
2. All other leaves include their full data, salt, and content type
3. The root hash allows verification against the original attestation
4. Each leaf has its own unique random salt
5. The data in each leaf is a hex-encoded JSON object (in this case, each with a single key-value pair)
6. The structure allows for any data format, as specified by the content type

## Real-World Flows

### Identity Verification Flow

1. Issuance: An identity provider creates a Merkle tree with all user data, stores the root hash onchain as an attestation, and gives the user the complete tree
2. Selective Disclosure: The user creates a proof revealing identity information without sensitive data like SSN
3. Verification: A third-party (like a KYC service) verifies the proof against the onchain attestation

### API-to-API Exchange Flow

1. Selective Data Exchange: Two services exchange a data structure with only the necessary fields (e.g., a KYC service might omit certain sensitive fields even in API-to-API communication)
2. Verification: The receiving service verifies the root hash against the onchain attestation
3. Further Filtering: The receiving service can apply additional filtering when sharing with other parties

## Security Considerations

I’ve implemented several security features:

- Each leaf has its own cryptographically secure random salt (16 bytes/128 bits)
- Correlation attacks are prevented as identical data produces different hashes
- JSON serialization supports both complete and selective disclosure modes

## Looking for Feedback

I’d appreciate the community’s thoughts on:

1. How this pattern could integrate with existing EAS implementations and standards
2. Whether having a unified structure for both complete data and selective disclosure makes sense
3. Additional use cases where this approach could be valuable
4. Security considerations we should address

This approach aims to simplify the developer experience while maintaining security, providing a seamless path from data sharing to selective disclosure without requiring separate data structures.

My implementation is available in [our open-source repository](https://github.com/lukepuplett/evoq-blockchain), with detailed documentation on both the complete data exchange and selective disclosure capabilities.

Looking forward to your insights!

---

Originally drafted version in Evoq.Blockchain repo where you’ll also find the C# MerkleTree implementation.



      [github.com/lukepuplett/evoq-blockchain](https://github.com/lukepuplett/evoq-blockchain/blob/master/docs/merkle/selective-disclosure.md)





####

  [master](https://github.com/lukepuplett/evoq-blockchain/blob/master/docs/merkle/selective-disclosure.md)



```md
# Selective Disclosure in Merkle Trees

## A Privacy-Preserving Approach to Verification

Merkle trees are a powerful cryptographic data structure that allows efficient and secure verification of content within a larger dataset. However, traditional Merkle proof implementations focus on proving the inclusion of specific leaves without addressing a critical need in many real-world applications: **selective disclosure**.

This document explores our implementation of selective disclosure in Merkle trees - an approach that allows revealing only specific leaves while maintaining the cryptographic verifiability of the entire tree.

## The Challenge

Consider a digital passport or identification document stored as a Merkle tree where each leaf represents a different piece of personal information:

- Document number
- Name
- Date of birth
- Address
- Biometric data
- Nationality

In many verification scenarios, you need to prove only specific attributes (like age or nationality) without revealing other sensitive information (like your address or full document number).
```

  This file has been truncated. [show original](https://github.com/lukepuplett/evoq-blockchain/blob/master/docs/merkle/selective-disclosure.md)

## Replies

**luke** (2025-04-17):

Note - what’s not in the proposed JSON document is the locator for the attestation. The recipient of the document would ideally be able to read all the information needed to resolve the attestation on whatever chain and compare the hashes.

---

**luke** (2025-04-19):

**Security** - Today I started wondering whether, by omitting the intermediate hashes, it would be easier to manipulate the hashes to arrive at the root hash?

In other words, is a conventional proof with intermediate left/right hashes designed in such a way to mitigate this?

Would love some thoughts on this.

Thanks

---

**luke** (2025-05-23):

Looking at prior art in JWS, JSON Web Signature, they use a header object. So my ‘metadata’ object would instead become:

```auto
"header": {
  "alg": "SHA256",
  "type": "MerkleTree+1.0"
}
```

The ‘alg’ being a hashing algorithm is communicated by the fact that it does not have a signature algorithm prefix like RS256.

---

**luke** (2025-05-23):

A signed, attested, selective reveal Merkle proof might look like this when downloaded with the idea of sharing it or uploading it:

```auto
{
    "header": {
        "alg": "ES256K-KECCAK256",
        "typ": "JWS"
    },
    "payload": {
        "merkleTree": {
            "header": {
                "alg": "SHA256",
                "typ": "MerkleTree+1.0"
            },
            "leaves": [
                {
                    "data": "0x7b22646f63756d656e7454797065223a2270617373706f7274227d",
                    "salt": "0x3d29e942cc77a7e77dad43bfbcbd5be3",
                    "hash": "0xe77007d7627eb3eb334a556343a8ef0b5c9582061195441b2d9e18b32501897f",
                    "contentType": "application/json; charset=utf-8; encoding=hex"
                },
                {
                    "hash": "0xf4d2c8036badd107e396d4f05c7c6fc174957e4d2107cc3f4aa805f92deeeb63"
                },
                {
                    "data": "0x7b22697373756544617465223a22323032302d30312d3031227d",
                    "salt": "0x24c29488605b00e641326f6100284241",
                    "hash": "0x1b3bccc577633c54c0aead00bae2d7ddb8a25fd93e4ac2e2e0b36b9d154f30b9",
                    "contentType": "application/json; charset=utf-8; encoding=hex"
                },
                {
                    "data": "0x7b2265787069727944617465223a22323033302d30312d3031227d",
                    "salt": "0x5d3cd91a0211ed1deb5988a58066cacd",
                    "hash": "0xce04b9b0455d7b1ac202f0981429000c9f9c06665b64d6d02ee1299a0502b121",
                    "contentType": "application/json; charset=utf-8; encoding=hex"
                },
                {
                    "data": "0x7b2269737375696e67436f756e747279223a22556e69746564204b696e67646f6d227d",
                    "salt": "0xc59f9924118917267ebc7e6bb69ec354",
                    "hash": "0xf06f970de5b098300a7731b9c419fc007fdfcd85d476bc28bb5356d15aff2bbc",
                    "contentType": "application/json; charset=utf-8; encoding=hex"
                }
            ],
            "root": "0x1316fc0f3d76988cb4f660bdf97fff70df7bf90a5ff342ffc3baa09ed3c280e5"
        },
        "attestation": {
            "eas": {
                "network": "base-sepolia",
                "attestationUid": "0x27e082fcad517db4b28039a1f89d76381905f6f8605be7537008deb002f585ef",
                "from": "0x0000000000000000000000000000000000000000",
                "to": "0x0000000000000000000000000000000000000000",
                "schema": {
                    "schemaUid": "0x0000000000000000000000000000000000000000000000000000000000000000",
                    "name": "PrivateData"
                }
            }
        },
        "timestamp": "2025-05-23T12:00:00Z"
    },
    "signature": "0x0000000000000000000000000000000000000000000000000000000000000000"
}
```

Signing it would be another layer of security, so a checker can quickly spot a fake proof before bothering to check the attestation. It also signs the date, should a checker want a recent proof to perhaps prove they are not in possession of a stolen proof.

The checker could potentially ask for a nonce to be included in the proof. This could happen between websites, where one site reaches out to another for a proof to be made.

The end user could paste a URL into a website wanting proof of age, and the website then gets the URL and tacks on a nonce or just checks the timestamp is less than a few seconds old. It would have the added reassurance of SSL.

The idea is that someone who has had their ID verified and attested can simply paste a URL into websites to buy beer, weapons and financial services.

---

**luke** (2025-06-03):

**Note** - The signed JWT envelope version does not allow a technical end user to manually open the file and redact leaf data and salts in order to make their own selective reveal proof, since it would invalidate the signature. This could be done with a text editor or even a tool for nontechnical folks.

It depends whether the signed JWT envelope version is especially beneficial, vs. the desirability of self-selected proofs.

One big reason for self-selected proofs is that the user would no longer rely on the availability or payment to the original proving service (my Zipwire app) to generate proofs revealing different data. This is quite important.

Possibly both designs might work. A consumer/reading such a proof could be written to specifically want the signed version, or it could accept the dis-enveloped object (or ignore it).

---

**luke** (2025-06-05):

A nice feature of this design is the ability to paste it directly into an LLM and have it:

1. decode the hashed text values
2. write code to check the root
3. future - MCP check the attested hash

Currently has mixed results. Cursor worked well. ChatGPT canvas needed a gentle nudge to get it to not try and do something with the salts, but it worked!

That makes it highly portable and usable.

---

**luke** (2025-06-11):

I’ve reworked the signed JSON around the JOSE JWS standard, which is related to the JWT standard (where JWT is compact, dot-delimited form).

```json
        {
          "payload": "eyJtZXJrbGVUcmVlIjp7ImxlYXZlcyI6W3siZGF0YSI6IjB4N2IyMjc0NjU3Mzc0MjIzYTIyNzY2MTZjNzU2NTIyN2QiLCJzYWx0IjoiMHhhN2UxMGYwYjk2YjU0YzlmNDJiZTQ3NzI1N2JmNWRiNyIsImhhc2giOiIweGZmNzY4NzE2NTE1M2Q5YmVlYzcxZWYxODcwZWE3YThhNDQyMmQ3ZDQwMjU2YmI2YTAwODMzODhkZmRkNWQyN2UiLCJjb250ZW50VHlwZSI6ImFwcGxpY2F0aW9uL2pzb247IGNoYXJzZXQ9dXRmLTgifV0sInJvb3QiOiIweGZmNzY4NzE2NTE1M2Q5YmVlYzcxZWYxODcwZWE3YThhNDQyMmQ3ZDQwMjU2YmI2YTAwODMzODhkZmRkNWQyN2UiLCJoZWFkZXIiOnsiYWxnIjoiU0hBMjU2IiwidHlwIjoiTWVya2xlVHJlZVx1MDAyQjIuMCJ9fSwiYXR0ZXN0YXRpb24iOnsiZWFzIjp7Im5ldHdvcmsiOiJiYXNlLXNlcG9saWEiLCJhdHRlc3RhdGlvblVpZCI6IjB4YWJjZGVmMTIzNDU2Nzg5MGFiY2RlZjEyMzQ1Njc4OTBhYmNkZWYxMjM0NTY3ODkwYWJjZGVmMTIzNDU2Nzg5MCIsImZyb20iOiIweDEyMzQ1Njc4OTBBYmNkRUYxMjM0NTY3ODkwYUJjZGVmMTIzNDU2NzgiLCJ0byI6IjB4ZkVEQ0JBMDk4NzY1NDMyMUZlRGNiQTA5ODc2NTQzMjFmZWRDQkEwOSIsInNjaGVtYSI6eyJzY2hlbWFVaWQiOiIweDEyMzQ1Njc4OTBhYmNkZWYxMjM0NTY3ODkwYWJjZGVmMTIzNDU2Nzg5MGFiY2RlZjEyMzQ1Njc4OTBhYmNkZWYiLCJuYW1lIjoiUHJpdmF0ZURhdGEifX19LCJ0aW1lc3RhbXAiOiIyMDI1LTA2LTExVDEyOjI0OjAwLjE0MjI0M1oifQ",
          "signatures": [
            {
              "signature": "AJwjiXdpQ246AiQL2ThlruB9TPo1jW85ISo1u5eCDn0ujkVr9RgA/FDOK3MKRXGhN2\u002BvQjqqms0r4LxQ/NiQzRs=",
              "protected": "eyJhbGciOiJFUzI1NksiLCJ0eXAiOiJKV1QiLCJjdHkiOiJhcHBsaWNhdGlvbi9hdHRlc3RlZC1tZXJrbGUtZXhjaGFuZ2VcdTAwMkJqc29uIn0"
            }
          ]
        }
```

A suitable smart LLM can take this as-in and comprehend it. It can read the base64url-encoded data and knows what’s inside before even decoding.

(try it)

Decoding yields the Merkle ‘tree’ leaves and root, inside its envelope which contains the attestation.

Part of that decoding allows the LLM to decode the contents of the Merkle leaf data (in the same response!).

It can write a Python script to check the root hash integrity, and I suspect with the appropriate MCP service, it could reach out to EAS and check the attestation.

The JWS is signed using `ES256K` (Ethereum raw signing) but I’ve not asked the LLM to code a checker for this.

I have a theory that LLMs will be able to think in code soon, i.e. execute code either as part of CoT or from the emergence of ‘neural pathways’ which work like strictly logical program execution.

So I reckon it won’t be long before you could throw such a file at an LLM and it’ll infer what it is and verify it all.

-

Anyway, the point of all this is to design a portable, verifiable data format which is familiar to non-web3 developers.

Apps that create or hold sensitive records or rich events can break the record into pieces and put them into leaves of a Merkle tree, attest the root hash, then allow their users to create a select-reveal proof.

The proof could be a downloadable/uploadable JSON file, or a URL to the JSON.

---

**luke** (2025-06-11):

Am looking into a design for the inner envelope with a `nonce` sibling to the `timestamp`.

Also considering if/how a proof could be delegated to some other actor to present, like a bot.

Note that by using the JWS design, it is simple to make a JWT to present in a header. So you have a select-reveal verifiable data exchange format in a web token. I’ll need to check and make sure I ain’t breaking any JWT rules with my payload.

