---
source: magicians
topic_id: 20392
title: "ERC-7734: Decentralized Identity Verification (DID)"
author: 64anushka
date: "2024-06-26"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7734-decentralized-identity-verification-did/20392
views: 715
likes: 3
posts_count: 3
---

# ERC-7734: Decentralized Identity Verification (DID)

**Introduction**: Hi everyone, I would like to discuss EIP, which proposes a standard for decentralized identity verification on the Ethereum blockchain.

**Motivation**: Centralized identity verification methods are often cumbersome, prone to data breaches, and do not give users control over their identity data. This proposal aims to provide a secure, privacy-preserving method for identity verification that can be used by decentralized applications (dApps).

**Abstract**: This proposal introduces a standard for decentralized identity verification (DID) on the Ethereum blockchain. The standard aims to provide a secure, privacy-preserving method for identity verification that can be used by decentralized applications (dApps).

**Specification**:

// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IDecentralizedIdentity {

struct Identity {

address userAddress;

bytes32 identityHash;

bytes32[2] verificationHashes;

bool isVerified;

uint256 timestamp;

}

```
event IdentityCreated(address indexed userAddress, bytes32 identityHash, uint256 timestamp);
event IdentityVerified(address indexed userAddress, bytes32[2] verificationHashes, uint256 timestamp);
event IdentityRevoked(address indexed userAddress, uint256 timestamp);

function createIdentity(bytes32 identityHash) external;
function verifyIdentity(bytes32[2] calldata verificationHashes) external;
function revokeIdentity() external;
function getIdentity(address userAddress) external view returns (Identity memory);
```

}

**Rationale**: The design leverages cryptographic hashes to represent identity information, ensuring that sensitive data is not stored directly on the blockchain. The use of verification hashes allows for flexible identity verification mechanisms, and the inclusion of events ensures transparency and traceability.

**Security Considerations**: Ensure that identity and verification hashes are generated using a secure hashing algorithm to prevent collisions and ensure the integrity of the identity data. Users have control over their identity data, which reduces the risk of unauthorized access and ensures privacy.

**Feedback Request**: I would love to hear your thoughts on the proposed standard, especially regarding the hashing methods used for identity verification and any potential improvements to the current design.

**Conclusion**: Thank you for taking the time to review this proposal. I look forward to your feedback and suggestions.

## Replies

**abcoathup** (2024-06-27):

I am not aware of an ERC-64.  ERC numbers are issued sequentially by editors/associates, you don’t get to pick your own.

I assume that you want to create an ERC, please create a PR in the ERCs repo when ready, an ERC number will be manually assigned.

---

**64anushka** (2024-07-02):

Adding the PR link:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/517)














####


      `master` ← `64anushka:patch-1`




          opened 08:54AM - 02 Jul 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/e/e178ad035d7e7cad89b15564cbbbcd1b0f37693e.jpeg)
            64anushka](https://github.com/64anushka)



          [+194
            -0](https://github.com/ethereum/ERCs/pull/517/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/517)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

