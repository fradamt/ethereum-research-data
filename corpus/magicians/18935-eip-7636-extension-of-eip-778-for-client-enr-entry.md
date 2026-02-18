---
source: magicians
topic_id: 18935
title: "EIP-7636: Extension of EIP-778 for \"client\" ENR Entry"
author: JKinc
date: "2024-02-25"
category: EIPs > EIPs networking
tags: [networking]
url: https://ethereum-magicians.org/t/eip-7636-extension-of-eip-778-for-client-enr-entry/18935
views: 2081
likes: 4
posts_count: 7
---

# EIP-7636: Extension of EIP-778 for "client" ENR Entry

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7636.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7636.md)



```md
---
eip: 7636
title: Extension of EIP-778 for "client" ENR Entry
description: Add additional ENR entry to specify client information such as name and version number.
author: James Kempton (@SirSpudlington)
discussions-to: https://ethereum-magicians.org/t/eip7636-extension-of-eip-778-for-client-enr-entry/18935
status: Withdrawn
type: Standards Track
category: Networking
created: 2024-02-25
requires: 778
withdrawal-reason: Lack of use and conflicts with some client developers regarding its practicality
---

## Abstract

The Ethereum network consists of nodes running various client implementations. Each client has its own set of features, optimizations, and unique behaviors. Introducing a standardized way to identify client software and its version in the ENR allows for more effective network analysis, compatibility checks, and troubleshooting. This EIP proposes the addition of a "client" field to the ENR.

## Motivation

```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7636.md)











      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7636)





###



Add additional ENR entry to specify client information such as name and version number.










## Abstract

The Ethereum network consists of nodes running various client implementations. Each client has its own set of features, optimizations, and unique behaviors. Introducing a standardized way to identify client software and its version in the ENR allows for more effective network analysis, compatibility checks, and troubleshooting. This EIP proposes the addition of a “client” field to the ENR.

## Motivation

Understanding the landscape of client software in the Ethereum network is crucial for developers, nodes, and network health assessment. Currently, there is no standardized method for nodes to announce their software identity and version, which can lead to compatibility issues or difficulty in diagnosing network-wide problems. Adding this to the ENR allows clients to audit network health only using discv5, and additionally track discv5 adoption across different services.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

The “client” entry is proposed to be added to the ENR following the specifications in [EIP-778](https://eips.ethereum.org/EIPS/eip-778). This entry is OPTIONAL and can be omitted by clients that choose not to disclose such information. The key for this entry is `"client"`.

All elements MUST be encoded as a string using the ASCII standard as described in [RFC 20](https://www.rfc-editor.org/rfc/rfc20).

The value for this entry MUST be an RLP list:

```auto
[ClientName, Version, (BuildVersion)]
```

- ClientName: A string identifier for the client software. It SHOULD be concise, free of spaces, and representative of the client application.
- Version: A string representing the version of the client software in a human-readable format. It is RECOMMENDED to follow semantic versioning.
- BuildVersion: An OPTIONAL string representing the build or commit version of the client software. This can be used to identify specific builds or development versions.

## Rationale

One key was chosen over using many keys to make efficient use of space. The use of one string, however, does not align with other EIPs of similar purpose and as such the RLP list was decided as the best encoding.

## Backwards Compatibility

This EIP is fully backwards compatible as it extends the ENR specification by adding an optional entry. Existing implementations that do not recognize the “client” entry will ignore it without any adverse effects on ENR processing or network behavior.

## Test Cases

A node running Geth version 1.10.0 on the mainnet might have an ENR `client` entry like:

```auto
["Geth", "1.10.0"]
```

A node running an experimental build of Nethermind might include:

```auto
["Nethermind", "1.9.53", "7fcb567"]
```

and an ENR of

```auto
enr:-MO4QBn4OF-y-dqULg4WOIlc8gQAt-arldNFe0_YQ4HNX28jDtg41xjDyKfCXGfZaPN97I-MCfogeK91TyqmWTpb0_AChmNsaWVudNqKTmV0aGVybWluZIYxLjkuNTOHN2ZjYjU2N4JpZIJ2NIJpcIR_AAABg2lwNpAAAAAAAAAAAAAAAAAAAAABiXNlY3AyNTZrMaECn-TTdCwfZP4XgJyq8Lxoj-SgEoIFgDLVBEUqQk4HnAqDdWRwgiMshHVkcDaCIyw
```

which can be decoded to yield normal data such as `seq`, `siqnature`, `id` and `secp256k1`. Additionally, it would yield the client value of `["0x4e65746865726d696e64","0x312e392e3533","0x37666362353637"]` or `["Nethermind", "1.9.53", "7fcb567"]`

## Security Considerations

Introducing identifiable client information could potentially be used for targeted attacks against specific versions or builds known to have vulnerabilities. It is crucial for clients implementing this EIP to consider the implications of disclosing their identity and version. Users or operators should have the ability to opt-out or anonymize this information if desired.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**Nerolation** (2024-04-23):

The disadvantage of “revealing” that kind of data is the fact that an attacker could use that info to better plan and execute certain kind of attacks. Not saying I’m against that proposal (I’m for it but maybe an even simpler approach would do it), but if I had to steelman the opposite opinion, I’d say it increases the practicality of attacking the network or individual nodes.

---

**JKinc** (2024-04-25):

I do agree that in an extreme case it could be used to exploit client specific vulnerabilities, however RLPx shows client information similar to this as part of the protocol.

---

**sbacha** (2024-05-27):

This EIP should additionally make explicit in the “Security Considerations” section that this information is self reported: it is not verifiable and should not be relied upon.

---

**JKinc** (2024-05-27):

Good idea, I should have specified it even though I thought people should already know that user specified data is not reliable, but with the magic Ethereum is doing now some might believe that it is reliable. I have updated it accordingly.

---

**wemeetagain** (2025-06-02):

Cool EIP.

I would recommend updating the encoding to be more compact.

As I argued in [another ENR-related thread](https://github.com/ethereum/consensus-specs/pull/3644#issuecomment-2064204258) ENR space is precious and limited (the spec limits an ENR to 300 bytes) and we should do what we can to make good use of the space.

The current encoding will spend a lot of that space. Much more than is necessary.

In your two examples:

```auto
["Geth", "1.10.0"]
```

- spends ~6.5% of available space

```auto
["Nethermind", "1.9.53", "7fcb567"]
```

- spends ~11% of available space

I don’t think we need to go crazy with squeezing every bit out of the encoding, but something more conservative would go a long way.

I would recommend something like:

- shorten the key to cl (saves ~1% of available space)
- cap client identifier to 2 bytes (saves 1-3% of available space)
- use rlp numbers for version (saves ~1% of available space)
- cap build identifier to 3 bytes (saves ~1% of available space)

Using these encoding rules, this field will only spend a max of ~4.5% of available space

The examples would then look like:

```auto
["gt", 1, 10, 0]
```

- spends ~2.5% of available space

```auto
["nt", 1, 9, 53, 0x7fcb56]
```

- spends ~4.5% of available space

---

**SirSpudlington** (2025-06-02):

This EIP is now final, so while this may be a better scheme changing cannot be done at this stage.

I have collected some information on the effects of this EIP and the data can be seen below (this is after both lighthouse and Grandine haved supported EIP-7636 for some time):

| description | value |
| --- | --- |
| Current size of (seen) DHT | 398,297 bytes |
| DHT size increase due to EIP-7636 | 32,259 bytes (8.81%) |
| Average size of ENR | 140 bytes |
| Max size of ENR | 253 bytes |
| Average size of client entry | 18 bytes |

