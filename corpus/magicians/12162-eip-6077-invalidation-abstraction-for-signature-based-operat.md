---
source: magicians
topic_id: 12162
title: "EIP-6077: Invalidation Abstraction for Signature-Based Operations"
author: k06a
date: "2022-12-15"
category: EIPs
tags: [signatures]
url: https://ethereum-magicians.org/t/eip-6077-invalidation-abstraction-for-signature-based-operations/12162
views: 663
likes: 2
posts_count: 3
---

# EIP-6077: Invalidation Abstraction for Signature-Based Operations

History:

- Adding EIP-6077: Add EIP-6077: Invalidation abstraction for signature-based operations powered by EIP-712 by k06a · Pull Request #6077 · ethereum/EIPs · GitHub

## Replies

**xinbenlv** (2022-12-15):

Hi there, thank you for authoring this.

I am drafting [ERC-5453](https://eips.ethereum.org/EIPS/eip-5453) and looking into options for nonce. It seems nonce per signer or nonce per destination contract will be useful. I am yet to better understand how nonce per operation have a strong usecase, can you help ellaborate this rationale?

---

**k06a** (2022-12-17):

[@xinbenlv](/u/xinbenlv) rationale behind nonce per operation is the following: smart contract could have multiple different operations which are not related to each other and some of them could be used non-immediately, for example voting or delegation.

Some existing operations like permit and delegate have nonces per signer, but some future operations could have nonces per signer+beneficiary, since it could be more handy. Or operations could support both ways, it depends on operation.

