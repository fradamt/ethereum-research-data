---
source: magicians
topic_id: 14759
title: "ERC-7204: Contract wallet management token"
author: wenzhenxiang
date: "2023-06-20"
category: ERCs
tags: [erc, wallet]
url: https://ethereum-magicians.org/t/erc-7204-contract-wallet-management-token/14759
views: 1362
likes: 0
posts_count: 1
---

# ERC-7204: Contract wallet management token

A proposal to manage fungible tokens by the user’s smart contract wallet, which provides a new way to manage assets, utilizes the programmability of the smart contract wallet, and also provides more playability.

EOA wallet has no state and code storage, and the smart contract wallet is different.

AA is a direction of the smart contract wallet, which works around abstract accounts.

The smart contract wallet allows the user’s own account to have state and code, bringing programmability to the wallet. We think there are more directions to expand. For example, token asset management, functional expansion of token transactions, etc.

The proposal aims to achieve the following goals:

1. Assets are allocated and managed by the wallet itself, such as approve and allowance, which are configured by the user’s contract wallet, rather than controlled by the token asset contract, to avoid some existing ERC-20 contract risks.
2. Add the simpletokenTransfer function, the transaction initiated by the non-smart wallet itself or  will verify the allowance amount
3. Add simpletokenApprove, simpletokenAllowance, simpletokenApproveForAll, simpletokenIsApproveForAll functions. The user wallet itself supports approve and provides approve
for single token assets and all token assets( simpletoken is forward compatible with ERC-20).
4. user wallet can choose batch approve and batch transfer.
5. Users can choose to add hook function before and after their simpletokenTransfer to increase the user’s more playability
6. The user can choose to implement the simpletokenReceive function
