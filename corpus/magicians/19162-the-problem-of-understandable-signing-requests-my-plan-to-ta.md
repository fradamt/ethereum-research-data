---
source: magicians
topic_id: 19162
title: The problem of understandable signing requests — My plan to tackle it
author: h4l
date: "2024-03-11"
category: Web > User Experience
tags: [eip-712, attestation, a11y]
url: https://ethereum-magicians.org/t/the-problem-of-understandable-signing-requests-my-plan-to-tackle-it/19162
views: 503
likes: 1
posts_count: 1
---

# The problem of understandable signing requests — My plan to tackle it

For many years it’s been a challenge to present users with signature/transaction requests in a way that they can understand. Web3 users are commonly presented with incomprehensible hex strings or JSON data by their wallets, and asked for consent. Users can’t give informed consent to requests they cannot understand, which hurts usability, accessibility and security.

I’m keen to work towards rectifying this situation, and I’d like to share an overview of what I’m thinking and planning; **it’d be great to hear any thoughts/feedback people have, and if anyone else is working on overlapping things**.

I wasn’t around at the time, but it seems like there was quite a bit of activity around 2017/18 on this issue, but it seems to have tailed off in recent years (with some exceptions!). The general perception I get from people is that poor User Experience (UX) is a problem that will be solved naturally over time as Wallets generally improve.

My core belief here is that it’s a mistake to think that Wallets will be able to present easily understandable requests to users by improving their UX in isolation. This is because the fundamental problem is that EIP-712 signature and transaction requests are not self-describing — the data a Wallet receives from an App is not rich enough for a Wallet to decode it into a human-understandable form, regardless of how fantastic the Wallet’s UI/UX is.

Wallets rely on out-of-band information to generate understandable representations of requests. For example, [Ledger maintains a repository of custom JSON metadata](https://github.com/LedgerHQ/ledger-asset-dapps) for this purpose.

What we’re missing missing is:

1. A way to describe the effect of a transaction or data signature in a way that a User can understand.
2. A way to look up descriptions for transaction or data-signing requests, in a way that cannot be manipulated by an attacker.

If Wallets had both of these, they could receive an unknown, untrusted request from a App, securely look up a trustworthy description method, and use it to present an accurate, understandable description to allow their user to provide informed consent on the use of their digital property.

---

**My Plan**

I think this problem is too large to go from 0 to 1 with an up-front design. I know there have been quite a few efforts to spec out designs in this area. I’m planning to take an iterative approach.

I’m planning to focus initially on EIP-712 typed-data signatures, and later tackle general transactions with knowledge/experience gained. (I think that data signatures should be smaller problem than transactions, and transaction simulation helps already in a way that it doesn’t with off-chain signatures (that can be used later). And the two should have a lot of overlap.)

I will start by building a data signing testbed/playground WebApp, which I can iterate on to implement and assess data signing request explanation methods in a practical setting.

My vision for this testbed is a webapp in the same vein as tools like https://jsfiddle.net/, https://jwt.io/ and https://playground.sourcify.dev/. It will provide a UI to paste an ERC-712 data signature request, received from a Wallet or App. Initially, the tool will only display unambiguous facts that can be determined by introspecting from the message itself (amount: 34, spender: `0x....`), without additional subjective interpretation (“Allow example.eth to withdraw 34 tokens …”).

I’ll then use the playground to iterate on designs and implementations of description methods, to come up with an approach that can produce accurate, understandable descriptions, without being too difficult to define. I’m trying to avoid making this post too long, so I won’t go into specifics, but I envisage this will be the combination of:

1. A data format that encodes a higher-level description of the data to be signed
2. A UI that can present the data format from 1. to a user in a sensible way
3. A method of generating 1. from the signature request (the EIP-712 data).

This could be a combination of a static, approved program, and dynamic, untrusted data provided by an App. E.g. if the to-be-signed data contains a hash, the App might provide the un-hashed data for the approved program to encode into 1., to demonstrate the origin of the hash.

This is part 1 of the two missing pieces I mentioned above. At this point you could imagine being able to paste in EIP-712 data from a set of known, pre-defined domains, and have them be described, along with identifying features like the domain, message and overall hash.

Part 2 is a means of discovering and trusting these description methods, so that

Wallets from different providers can share the same descriptions, and expand the

set of descriptions over time. There are lots of ways to go about this, but I feel like this should probably be something that doesn’t require on-chain support at the contract level. Any system needs to support existing contracts,

and the multi-chain nature of the world means that we need to support both contracts with instances on multiple chains, and ultimately transactions that bridge multiple chains. I can imagine a two-sided system working here, where developers publish description methods (either for their smart contracts, or for their DApps at a higher level), and Wallet providers add these methods to allowlists. I can imagine [EAS](https://attest.sh/) being one good building block to implement such a system.

A Wallet could show a user that an operation was recognised by X, Y, Z other well-known providers, even if it wasn’t part of the Wallet’s own allowlist. Users could opt to trust additional lists beyond the default, to avoid their Wallet provider censoring/gatekeeping Apps.

So much like Part 1, I’ll then use the playground to iterate on approaches to this, ending up with a way of dynamically discovering trusted description methods in the playground App.

Thanks for reading!
