---
source: magicians
topic_id: 13879
title: "Discussion: Do We Need an EIP for Basic Interface of Multi-Signature Wallet Contract Accounts?"
author: 5cent-AI
date: "2023-04-19"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/discussion-do-we-need-an-eip-for-basic-interface-of-multi-signature-wallet-contract-accounts/13879
views: 468
likes: 4
posts_count: 3
---

# Discussion: Do We Need an EIP for Basic Interface of Multi-Signature Wallet Contract Accounts?

Recently, many wallet projects are preparing to be built on ERC-4337, but many of them seem to be developing their own independent multi-signature wallet contract accounts. There is no common standard for multi-signature wallet contract accounts, which may bring a series of issues such as interoperability, and may affect the large-scale adoption of ERC-4337.

So, do we need an EIP for the basic interface of multi-signature wallet contract accounts? If so, what basic interfaces do we need? We hope more people, especially developers involved in abstract account-related work, can join the discussion.

## Replies

**5cent-AI** (2023-04-19):

Personally, I think we need it. I am doing some research on extending Token standards, and to be compatible with EIP-4337, it requires EIP-1271. However, that alone is not enough. It also needs the following basic interfaces provided by multi-signature wallet contracts:

1.Query the threshold of signers.

2.Query whether a certain address is a valid signer.

---

**skyh24** (2023-04-19):

You can see my thinking about problems on AA, we are still working on it: [aa-research/EIP.md at main · accountjs/aa-research · GitHub](https://github.com/accountjs/aa-research/blob/main/Research/EIP.md)

