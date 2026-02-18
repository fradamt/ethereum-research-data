---
source: magicians
topic_id: 13092
title: "Wallet PSA: Beacon Chain Withdrawal Address Balance Updates"
author: timbeiko
date: "2023-02-28"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/wallet-psa-beacon-chain-withdrawal-address-balance-updates/13092
views: 678
likes: 4
posts_count: 1
---

# Wallet PSA: Beacon Chain Withdrawal Address Balance Updates

Cross-posting from [Twitter](https://twitter.com/TimBeiko/status/1630693566023598085), to reach folks here as well:

> Shapella PSA for wallet devs: beacon chain withdrawals don’t create a transaction on the EL. This means that if you’re scanning incoming txns to an address to update its balance, you won’t process withdrawal balance updates

> We saw this bug on MetaMask during the Sepolia fork, but others probably have the same issue. Here’s a bug report for them: [Bug]: ETH balance not updating after Beacon Chain Withdrawals · Issue #17936 · MetaMask/metamask-extension · GitHub

> Withdrawals are processed similarly to PoW emission: they are added to the addresses’ balance “behind the scenes”, at the end of block execution. See the State Transition section here: EIP-4895: Beacon chain push withdrawals as operations

> If you want to run your own validator to test this, you can do so on Zhejiang: https://zhejiang.ethpandaops.io Alternatively, you can track the Sepolia validators and their periodic withdrawals. Goerli date fork isn’t set yet, but we’ll likely do so on ACDE this Thursday.
