---
source: magicians
topic_id: 24733
title: "IERC721 Retroactive approvals: disabling approvals before time"
author: sebasky-eth
date: "2025-07-04"
category: Magicians > Primordial Soup
tags: [nft, token, erc-721, token-approval]
url: https://ethereum-magicians.org/t/ierc721-retroactive-approvals-disabling-approvals-before-time/24733
views: 50
likes: 0
posts_count: 1
---

# IERC721 Retroactive approvals: disabling approvals before time

**Upgrade to IERC721 approval system**

([content-finance-contracts/src/token/erc721/IERC721RetroactiveApprovals.sol at master · sebasky-eth/content-finance-contracts · GitHub](https://github.com/sebasky-eth/content-finance-contracts/blob/master/src/token/erc721/IERC721RetroactiveApprovals.sol))

*IERC721RetroactiveApprovals* adds extra dimension to approvals: time. Every approval saves information about date, which are compared with *retroactiveDate* to decide its validity.

**It could work in three ways:**

**A) Adaptation to current system**

retroactiveDate cannot go to future. So if dApp call for approval, it will work as expected

**B) Silent Freedom**

*retroactiveDate* can go to future.

**C) Loud Freedom**

*retroactiveDate* can go to future. But calling *approve* or *setApprovalForAll*, if *retroactiveDate* is futuristic, must revert.

**Gas cost**

It could be minimalized in bitfield implementation of ERC721.

Supply data could contain *retroactiveDate*.

Token owner data could contain date for token approval.

But operator approval date need to be read during transfer, if necessary.

**Code**:

```auto
interface IERC721RetroactiveApprovals is IERC721 {
  event RetroactiveApproval(address indexed owner, uint256 retroactiveDate);

  function retroactiveDate(address owner) external view returns (uint256);

  function approvalDate(address owner, address operator) external view returns (uint256 date);
  function tokenApprovalDate(uint256 tokenId) external view returns (uint256 date);

  function disableAllApprovalsBefore(uint256 retroactiveDate) external;
  function disableAllApprovals() external;
  ///acts like: disableAllApprovalsBefore(block.timestamp + 1)
}
```
