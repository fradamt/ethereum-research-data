---
source: magicians
topic_id: 14256
title: Automatic Transaction Representation
author: Pandapip1
date: "2023-05-12"
category: EIPs
tags: [wallet, ux, ui]
url: https://ethereum-magicians.org/t/automatic-transaction-representation/14256
views: 1076
likes: 0
posts_count: 7
---

# Automatic Transaction Representation

https://github.com/ethereum/EIPs/pull/7023

## Replies

**Weixiao-Tiao** (2023-08-24):

Would it be better to be categorized like EIP-712 ([EIP-712: Typed structured data hashing and signing](https://eips.ethereum.org/EIPS/eip-712)), as Standards Track: Interface but not ERC?

---

**Pandapip1** (2023-09-01):

I thought so as well, but the majority of other editors disagreed.

---

**SamWilsn** (2023-09-21):

> If the transaction originates from an embedded frame (e.g. an iframe or webview), the wallet MUST […] add a warning that the request may not be trustworthy

This seems too strict. If the wallet can determine the embedded frame is safe (maybe same domain, or similar rules), it shouldn’t have to display the warning. I’d change this to a SHOULD?

---

**SamWilsn** (2023-09-21):

> If the request references a contract that doesn’t have verified source code […]

This is a huge centralization risk. If every wallet implementing this proposal has to somehow implement contract source validation, they either need to include an entire IPFS client and a dozen solidity compilers, or rely on a centralized provider like etherscan.

---

**Pandapip1** (2023-10-16):

Somehow only just now got the notifications?! I have updated the EIP.

---

**SamWilsn** (2023-10-24):

For the contract source and audit requirements, how do you handle differences in execution between simulation in the wallet and what actually happens on chain?

A verified source contract can pretty easily call into a non-verified contract, and an incorrect “verified” stamp is worse than no stamp at all.

