---
source: magicians
topic_id: 14494
title: "EIP: Social Recovery Interface"
author: odysseus0
date: "2023-05-30"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/eip-social-recovery-interface/14494
views: 1997
likes: 5
posts_count: 7
---

# EIP: Social Recovery Interface

I would like to share with you a new ERC proposal that aims to standardize the interface for social recovery processes within smart contract accounts:

https://github.com/ethereum/EIPs/pull/7093

The main idea of this proposal is to separate the identity verification and policy verification procedures from the recovery process, allowing users to customize their recovery policies and choose different types of guardians, such as friends, family members, NFTs, SBTs, or even off-chain identities. The proposal also supports multiple recovery mechanisms and eliminates single points of failure.

I believe this proposal can benefit the Ethereum community by providing a common standard for social recovery processes, enabling interoperability and composability among different smart contract accounts and applications.

I would appreciate your feedback and suggestions on this proposal. Please let me know what you think about the design, implementation, security, and usability aspects of this standard. Thank you for your time and attention.

## Replies

**bumblefudge** (2024-04-02):

this is super interesting! do you know if anyone has implemented this and benchmarked/studied it on a testnet or anything?

---

**Amxx** (2025-03-05):

This ERC contains invalid solidity code (public functions in interfaces, missing location for non-value args, typos for types and variables …) that shoukld be fixed.

Additionally, it requires `IRecoveryAccount` to provide EIP-712 related getters. I’d suggest removing them in favor of ERC-5267.

---

**Amxx** (2025-03-05):

I would also suggest to prefix all interfaces with the ERC number to avoid any confusion with other ERCs

- IPermissionVerifier → IERC7093PermissionVerifier
- IRecoveryPolicyVerifier → IERC7093RecoveryPolicyVerifier
- IRecoveryAccount → IERC7093RecoveryAccount

---

**Amxx** (2025-03-05):

The ERC mentions

```auto
EXECUTE_RECOVERY_TYPEHASH = keccak256("StartRecovery(address configIndex, bytes newOwners, uint256 nonce)")
```

Usually, the name of the variable should match the name of the typed data struct. So it should either be `START_RECOVERY_TYPEHASH` or `"ExecuteRecovery(address ...`

---

**Amxx** (2025-03-05):

I’m currious why the `getRecoveryStatus(address policyVerifier)` is taking an address as a parameter.

- can multiple recovery happen in parallele for the same account (using different configIndex) ?
- can multiple RecoveryConfigArg (configIndex) use the same policyVerifier ?

Overall, this ERC feels way under-specified.

---

**Amxx** (2025-03-05):

- In struct ThresholdConfig, lockPeriod is using a signed value (int48). I guess this is a mistake.
- In IPermissionVerifier, should the isValidPermission functions be view ? Is there any reason for them to be non-payable ?

