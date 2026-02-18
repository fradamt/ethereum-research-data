---
source: magicians
topic_id: 23336
title: "EIP-####: GitChain"
author: etan-status
date: "2025-04-01"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-gitchain/23336
views: 143
likes: 3
posts_count: 9
---

# EIP-####: GitChain

Discussion topic for GitChain EIP:

- Add EIP: GitChain by etan-status · Pull Request #9579 · ethereum/EIPs · GitHub
- EthPandaOps support

## Replies

**etan-status** (2025-04-01):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9579#discussion_r2022774531)














#### Review by
         -


      `master` ← `etan-status:gc-init`







This solves MEV!












Yes, ordering transactions by issue number ensures that transactions cannot be frontrun.

---

**etan-status** (2025-04-01):

This also removes all security issues and operational challenges involved with validator key management, including support infrastructure such as the generic validator request bus, and the entire engine API interaction. There is no concept of INVALID payloads.

---

**etan-status** (2025-04-01):

Wallets also no longer need to use a16z/helios to verify JSON-RPC responses. They can simply check the GitHub TLS signature and immediately know that the response is correct, immediately! No more 12s delay to wait for the sync committee signature, or 24s with ePBS, or 36s if state root computation is delayed… It’s all obsolete!

---

**etan-status** (2025-04-01):

4444 is also included:

- For history, simply checkout the repository with a max --depth
- For state, use Git sparse checkout to only checkout the accounts that are of interest.

The response can be validated by checking the GitHub TLS signature. No Merkle proofs etc are needed, every subpage can be verified using TLS.

It is up to GitHub to switch to PQ signature schemes for TLS in time. Notably, it does not add complexity to the blockchain, it just continues to work as is.

---

**etan-status** (2025-04-01):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9579#issuecomment-2769627971)














#### Comment by
         -


      `master` ← `etan-status:gc-init`







This is a fantastic alternative to the Beam Chain! I like it much more












Yes, this proposal does not require experimental zk crypto or crazy protocols. It is straight-forward to audit, based on established tooling.

---

**bbusa** (2025-04-01):

EthPandaOps [supports](https://ethpandaops.io/posts/april-fools/) this EIP

---

**etan-status** (2025-04-02):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9579#discussion_r2023776819)














#### Review by
         -


      `master` ← `etan-status:gc-init`







This ensures we are censorship resistant legally 👍












It’s a good point. GitHub is available globally, including regions that have more restrictive Internet access. GitChain is also auditable, the sequential indexing makes it obvious if a transaction suddenly disappears, as it leaves a gap in the issue numbering.

---

**etan-status** (2025-04-02):

With the proposed timeline, do we have to propose it for inclusion in Fusaka? [@timbeiko](/u/timbeiko)

