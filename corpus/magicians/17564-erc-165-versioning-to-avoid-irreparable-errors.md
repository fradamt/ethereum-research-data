---
source: magicians
topic_id: 17564
title: ERC-165 Versioning To Avoid Irreparable Errors
author: sullof
date: "2023-12-21"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-165-versioning-to-avoid-irreparable-errors/17564
views: 528
likes: 0
posts_count: 1
---

# ERC-165 Versioning To Avoid Irreparable Errors

I’d like to highlight an issue with the current method of supporting ERC-165 interfaces, which focuses solely on the Final version and disregards any intermediate versions.

When a promising new proposal emerges, many projects adopt it, even if it’s in the Review phase or sometimes even a Draft. This is due to the expectation that the proposal will eventually be finalized without significant changes. A case in point is ERC-6551, which, although still in the Review stage, has been implemented by numerous projects. A concern arises when such a proposal undergoes modifications before finalization, leading to a different interface ID. This makes it impossible to verify if a smart contract supports the intended interface.

Those who adopted the initial version might end up aligned with an incorrect interface ID, potentially leading to irreparable errors. Introducing some form of versioning could resolve this by enabling the verification of the specific interface version supported, thus ensuring accurate information retrieval.

Several possible solutions exist for this issue. A straightforward approach would be to include the previous version in the final specification. For instance, the final interface could retain the name IERCxxx, while the earlier version could be named IERCxxxv1.

Alternatively, a new ERC could be introduced, such as:

```auto
interface IERCzzz {
  // returns the version for a specific interface
  function interfaceVersion(bytes4 interfaceId) external view returns (uint256) {}
}
```

In this case, when a standard supports more versions, we could verify if it supports both IERCxxx and IERCzzz and call `interfaceVersion`. This would enable determination of which version of the interface is supported. It’s important that ERCxxx lists the versions it supports.

A potential challenge arises when the first version of the interface is the only one, thereby lacking explicit versioning. To address this, we could assume that, by default, the version is 0.0.1. Hence, the function would return 0.0.1 in such cases. Under this system, if there are no changes throughout the development process, the final version (1.0.0) would be considered equivalent to 0.0.1. However, if there are changes during development, each intermediate version would be assigned a unique number to reflect those alterations.

Regarding the `interfaceVersion` function, using uint256 as the result type is indeed more efficient for handling within a smart contract. The versioning could be straightforward, where a version like 1.2.3 would be encoded as 1002003. Alternatively, each part of the version (MAJOR.MINOR.PATCH) could be considered as a bytes8 segment and encoded as:

```python
uint semver = MAJOR << 16 | MINOR << 8 | PATCH;
```

What are your thoughts on these suggestions?
