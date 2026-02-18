---
source: magicians
topic_id: 14526
title: "EIP-7099: Off-chain Checks"
author: civia-code
date: "2023-06-01"
category: EIPs
tags: [erc, gas]
url: https://ethereum-magicians.org/t/eip-7099-off-chain-checks/14526
views: 505
likes: 2
posts_count: 4
---

# EIP-7099: Off-chain Checks

Low cost distribution of ERC-20 tokens with off-chain check writing and batched or bundled mint.

PR: [Add EIP: Offchain Checks by civia-code · Pull Request #7099 · ethereum/EIPs (github.com)](https://github.com/ethereum/EIPs/pull/7099)

## Replies

**teamdesider** (2023-06-01):

This is very useful for creating blockchain games. Besides ERC20, is it compatible with ERC1155? Also, I would like to know if it’s possible to destroy Checks before they have been minted on the chain. It would be great if it can provide such flexibility.

---

**civia-code** (2023-06-01):

Yes, we are indeed considering the off-chain SBT checks protocol, and we have taken reference from the implementation of ERC-1155. We believe that this protocol is highly valuable in the domain of SBT distribution.

---

**civia-code** (2023-06-01):

Sure, users simply need to invoke the contract with a zero amount check to invalidate certain checks that originally have a specific amount. Similar to the regular process, this operation requires consecutive IDs and a valid signature.

