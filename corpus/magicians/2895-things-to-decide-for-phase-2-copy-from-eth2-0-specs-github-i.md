---
source: magicians
topic_id: 2895
title: Things to decide for phase 2 (copy from eth2.0-specs github issues)
author: vbuterin
date: "2019-03-11"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/things-to-decide-for-phase-2-copy-from-eth2-0-specs-github-issues/2895
views: 1158
likes: 6
posts_count: 1
---

# Things to decide for phase 2 (copy from eth2.0-specs github issues)

- Virtual machine

Decide definitely doing EWASM (default)?
- What does the FFI look like?
- How is code serialized? Doing any fancy AST merklization?

**Cross-shard message structure**.

- Here is a possible design with some details: https://ethresear.ch/t/phase-2-pre-spec-cross-shard-mechanics/4970
- Mechanics: cross-shard messages, contract yanking
- Decide we’re not doing layer 1 synchronous cross-shard calls and leaving it to layer 2 (default) or do something else?

**Contract storage structure**

- Linear code, linear storage, max combined size 12kb (to fit a yank into a single block) ?

**Contract addressing**

- Default approach: CREATE2 for everything
- Possible alternative: optional sequential addresses for contract creation (rationale: with much smaller addresses, using libraries may be much more efficient)

**Access lists**

- Total (must specify all addresses) vs partial (can specify prefixes) vs none at all

**Account abstraction model**

- https://ethresear.ch/t/tradeoffs-in-account-abstraction-proposals/263
- https://ethresear.ch/t/maximally-simple-account-abstraction-without-gas-refunds/5007
- Major tradeoff: do we abstract nonces or not? That is, do we keep in-protocol nonce-checking of transactions or do we leave that to the contract code?

Rationale for abstraction: simpler protocol; also prevents complexities arising from interaction between multiple users attempting withdrawal from one contract at the same time, where N-1 of them must resend with a higher nonce, also removes need to worry about replay prevention in the hibernation/waking cases in-protocol
- Rationale for non-abstraction: potential for more guarantees for network peers; preserves invariant that any given txhash appears only once in a chain

**Gas cost model**

- Computation
- Data
- Access: charge per Merkle branch, don’t charge if the Merkle branch has already been used in that block?
- Adopt fee market reform proposal from https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838 ?

**Storage fees**

- https://ethresear.ch/t/a-minimal-state-execution-proposal/4445
- https://ethresear.ch/t/state-fees-formerly-state-rent-pre-eip-proposal-version-3/4996
- Hibernation and waking: https://ethresear.ch/t/cross-shard-receipt-and-hibernation-waking-anti-double-spending/4748 (referenced in https://ethresear.ch/t/phase-2-pre-spec-cross-shard-mechanics/4970)
- Decide on fixed fee?

Note: even with a fixed fee, there is an implied cap on the storage size of each shard because of gas limits (at least, this is if we charge a gas cost that scales linearly with TTL extension)

What is the above missing?
