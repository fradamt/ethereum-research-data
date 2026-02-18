---
source: magicians
topic_id: 15434
title: "ERC-7484: Registry Adapters for Smart Accounts"
author: kopykat
date: "2023-08-14"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7484-registry-adapters-for-smart-accounts/15434
views: 3026
likes: 11
posts_count: 7
---

# ERC-7484: Registry Adapters for Smart Accounts

This EIP proposes a standardised registry adapter for modular smart accounts. The adapter allows the account to query and verify security attestations about a module through an attestation registry. The adapter is responsible for querying the registry and correctly handling the return values.

After having started a dialogue with many of the teams working on modular accounts and/or modules and having received useful feedback on the module registry reference implementation, we have now taken the next step of formalising what we have been working on as a public proposal. The goal of this is increasing the scope and visibility of discussion, receiving more feedback and, ultimately, coming to a consensus about this approach to modular account security.

One major point of discussion that I would like to highlight out of the box is around the tradeoffs of proposing a singleton registry (for more details see the Rationale section of the EIP) and whether this ERC should be more or less restrictive on alternative registries.

Finally, note that this proposal is still in draft and will likely change significantly with input from the community.

https://github.com/ethereum/EIPs/pull/7484

## Replies

**hangleang** (2023-09-20):

Not sure if we can reuse ethereum attestation service: https://easscan.org/ for schema and attestation parts of the architecture, which anyone could attest on-chain and off-chain.

---

**kopykat** (2023-09-20):

Yes, our reference implementation Registry took a lot of inspiration from EAS but made some specific modifications for this use case: [GitHub - rhinestonewtf/registry](https://github.com/rhinestonewtf/registry)

---

**hangleang** (2023-09-21):

Okay, got it. I just saw the mentioned in [FAQ - module registry](https://docs.rhinestone.wtf/registry/faq).

Is there any other way we can leverage EAS and build on top of the existing infrastructure?

---

**kopykat** (2023-09-22):

I’m not sure if there’s much more that could be beneficial. We could directly use the EAS contracts, but this would come with some compromises.

For example, the reference implementation registry has been designed with the idea that attestations are on made a specific module record, which leads to some benefits, such as being able to easily fetch all attestations on a specific module on-chain.

Would love to hear whether you have any ideas for using existing infra even further

---

**hangleang** (2023-10-01):

I’m not sure if this talk is helpful or not to gain insight from [Bankless episode - EAS](https://youtu.be/RsIBqExwsT8?si=GoNtYBrmStD2_jvJ&t=990). In this talk, guests speaker mention about attestation can be done via smart contract, which mean any smart account can be able to do attest on any modules, but not sure whether it supports ERC1271 or not, that you mention in the FAQ.

---

**mdaus** (2025-08-14):

Just found this recently, I think this is a good way to make some consensus for apps, in this case security. EAS are one way to consider but they do not have any reliability in case something goes wrong. I would suggest some stake if some that runs beyond the scope of the intended logic, they will get slashed.

I want to use this as a base concept but want some more feedback if it’s really practical.

