---
source: magicians
topic_id: 12722
title: Security implications of storing a user's signature publicly
author: elmariachi
date: "2023-01-27"
category: Uncategorized
tags: [signatures]
url: https://ethereum-magicians.org/t/security-implications-of-storing-a-users-signature-publicly/12722
views: 527
likes: 2
posts_count: 1
---

# Security implications of storing a user's signature publicly

Many of us are requesting or using user signatures for various reasons, e.g. to log them in (siwe), to prove they understood terms and conditions, to have another party grant them access to something (erc20 permits) etc.

Question is: how safe is it, depending on the individual usecase, to store these signatures on a public storage layer, e.g. ipfs, along with the message the user has signed?

My instant answer is the obvious one: it’s safe since you cannot derive the private key from a message and a signature. It actually must be safe to do so, since eth transactions are nothing more than signed messages, payload and sig are public.

For more specific usecases, e.g accepting the terms of a certain action (an individual “yes I want to mint exactly this NFT#17 on this contract” signoff) I think one at least should take replay attack vectors into account, adding the chain id and ideally a unique domain to the message payload. A verifier must make sure that all signed parameters match the expected context it’s verifying for (notably the chain id so you can’t reuse a signature for a replay on another chain)

I’m still wondering if some of you have an example where it at first seems pretty safe to store a signature publicly but you found an attack that let a malicious party use the signature in a way that wasn’t intended. Reusing Siwe signatures just enters my mind, they can actually be used to login the user into several systems if they accept or forget to check its nonce or domain.

Happy to hear your opinions!

Oh, and more technically: atm we’re talking about Ecdsa signatures that rely on trapdoors that are safe on current hardware but potentially can be reversed using Shor’s algorithm on quantum hardware. Are there signature schemes or key exchanges that potentially already are considered quantum safe and allow saving / using the signature on the long term?
