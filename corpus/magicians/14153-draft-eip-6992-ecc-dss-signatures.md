---
source: magicians
topic_id: 14153
title: "Draft EIP-6992: ECC DSS signatures"
author: JKinc
date: "2023-05-05"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/draft-eip-6992-ecc-dss-signatures/14153
views: 872
likes: 5
posts_count: 13
---

# Draft EIP-6992: ECC DSS signatures

## Read Me

This is EIP used to be for HTTP requests and was renamed to ECC DSS signatures on the 16/05/2023. All comments under this are still valid as this EIP is work in progress.

## Abstract

This EIP allows for smart contracts to verify DSS signatures.

## Motivation

This EIP allows for check signatures which should allow for an smoother transition from web2 to web3. While it might seem counter-intuitive to defeat the “true decentralization” of ethereum it should prove to have some major advantages like polling external data sources or creating random data while verifing data authenticity.

## Specification

### Opcode

Opcode: 0xa5

Gas cost: 15000 (minimum)

Inputs:

- Body (string): A selection of data.
- Signature (bytes): The signature of the data
- PublicKey (string): An ECC P-256 public key in PEM format

Output:

- Verified (bool): True if the data is correctly signed.

Description:

This Opcode must encode the data to bytes using utf-8 and then must hash the Body field with the SHA256. Then, the node should verify against the ECC P-256 public key which should be used to verify the signature against the data using the fips-186-3 DSS signing algorithm .

Stack Transition:

(before) [Body, Signature, PublicKey]

(after)  [… Verified]

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

## Rationale

TBD

## Backwards Compatibility

No backward compatibility issues found.

## Test Cases

Opcode : 0xa5

(before) [“Hello World”, 0x1234567890, “[validpublickey]”]

(after)  [… , true]

In this sense the server should have made a DNS query to the subdomain “_domainkey.example.com”.

## Reference Implementation

Example solidity contract for verification

```auto
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.18;

contract Example {
    function randomNumber(string calldata data, bytes calldata hash) public {
        if (!verifySignature(data, hash, "validkey")) {
            revert();
        } else {
            // Very secret code here
        }
    }

    function verifySignature(string calldata data, bytes calldata hash, string memory key) private returns (bool) {
        // Dummy function to emulate opcode
        return true;
    }
}

```

## Security Considerations

Needs discussion.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**JKinc** (2023-05-05):

The PR for anyone interested : [Add EIP: HTTP requests by JKincorperated · Pull Request #6992 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6992)

---

**SamWilsn** (2023-05-07):

If the web server intentionally fails validation after a block is proposed, wouldn’t that cause the block proposer to be slashed through no fault of their own?

---

**JKinc** (2023-05-07):

Yes, you are right… I will rewrite this EIP to prevent this. Please check the PR on GitHub to see the revised version.

---

**SamWilsn** (2023-05-07):

If the opcode returns `(502, "")` for a validator and `(200, "some body")` for the block proposer, the resulting state roots will be different for the validator and block proposer.

---

I think the only way to solve this is to pass the body from the server into the EVM through calldata when the transaction is created, with a proof (perhaps using DNSSEC) that the data was signed by the domain owner.

---

**JKinc** (2023-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I think the only way to solve this is to pass the body from the server into the EVM through calldata when the transaction is created, with a proof (perhaps using DNSSEC) that the data was signed by the domain owner.

This is exactly what I was attempting but based in the EVM, having the transaction show the request would be generally better. I will rewrite it.

---

**JKinc** (2023-05-07):

Fixed, now the Opcode is just for verification purposes and the data should be sent to the smart contract via calldata.

---

**SamWilsn** (2023-05-08):

[ERC-3668](https://eips.ethereum.org/EIPS/eip-3668) was recently brought to my attention on Twitter. It wouldn’t require a consensus change and seems to allow similar functionality. Have you seen it before?

---

**JKinc** (2023-05-08):

I have just read though it, It appears to be somewhat similar. However, ERC-3668 does not appear to have any truly verifiable means to get the data. I like the saying “verify don’t trust” and this should provide  the means to verify by the DNS records and DNSSEC.

---

**mathewmeconry** (2023-05-16):

How do you handle the problem of changing keys on DNS?

A TX is not verifiable after some time because the key has changed in the TXT record and the verification fails.

Also, this opens up some attack vectors where I would send a TX and respond to the first DNS query with the key (block proposer) and to all others (attesters) with another key or with no response at all, thus failing the block.

---

**JKinc** (2023-05-16):

Fixed, it was too much of a headache trying to actually fix DNS queries. Now, data must be passed to the contract either on creation or later and the opcode just implements a quick version of verifying these as doing it in pure solidity would be really inefficient.

---

**mathewmeconry** (2023-05-16):

What is then now the difference to only using an EOA to sign the data and verify it with `ecrecover`?

Also, would it make more sense to it being a precompile instead of an opcode like `ecrecover` if it cannot be accomplished with the already built-in cryptographic schemes?

---

**JKinc** (2023-05-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mathewmeconry/48/9502_2.png) mathewmeconry:

> Also, would it make more sense to it being a precompile instead of an opcode

I just finished changing the specs so it is a precompile, as before I started this I had no idea what a precompiled contract was, after 30 minutes of intense googling, I have adjusted the EIP accordingly.

