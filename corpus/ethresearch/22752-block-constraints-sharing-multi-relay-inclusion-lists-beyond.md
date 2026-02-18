---
source: ethresearch
topic_id: 22752
title: "Block Constraints Sharing: Multi-Relay Inclusion Lists & beyond"
author: remosm
date: "2025-07-16"
category: Proof-of-Stake > Block proposer
tags: [mev, proposer-builder-separation, censorship-resistance]
url: https://ethresear.ch/t/block-constraints-sharing-multi-relay-inclusion-lists-beyond/22752
views: 232
likes: 3
posts_count: 1
---

# Block Constraints Sharing: Multi-Relay Inclusion Lists & beyond

Co-authored by [Michael](https://x.com/mostlyblocks), with [Kubi](https://x.com/kubimensah) and [George](https://x.com/gd_gattaca) from [Gattaca](https://x.com/gattacahq). Special thanks to [Alex](https://x.com/alextes), [Max](https://x.com/0xKuDeTa), and [Jason](https://x.com/jasnoodle) for the discussions and suggestions. Feedback is not necessarily an endorsement.

### Introduction

This post introduces Multi-Relay Inclusion Lists (mrIL), a way for relays to converge on a single shared inclusion list with minimal overhead. This increases Ethereum’s censorship resistance by reducing the discretion any individual relay may exercise over the contents of the inclusion list.

Relays are incentivized to opt-into the design as it reduces the marginal cost a builder incurs when delivering blocks to individual relays with diverging rILs. This reflects as a higher likelihood of receiving builder blocks, and allows relays with low market share to stay competitive.

The proposed protocol can be trivially extended to converge on a shared list of any signed proposer commitments, minimizing the slashing risk of such commitments (like preconfirmations) by allowing each relay to enforce block compliance in a more informed way.

This improves the risk adjusted return from proposer commitments, which may result in additional proposer opt-in, and ultimately may reduce the risk margin charged to users.

This article is an extension to our previous work on [relay inclusion lists](https://ethresear.ch/t/relay-inclusion-lists/22218), and complementary to [relay block merging](https://ethresear.ch/t/relay-block-merging-boosting-value-censorship-resistance/22592). Together, these components increase block value, and provide additional censorship resistance for mempool- and private- transactions respectively.

### Implementation and Transaction Flow

As relays are incentivized to converge on a shared inclusion list, a lean implementation without multi-round communication is possible:

1. Each relay r_i builds a local inclusion list L_i for the current slot and exposes it at the get_local_il() endpoint.
2. Relays pull L_1,...,L_n from peers and for each transaction t observed count the number of lists it appears in:

f(t) = \#\{j \in \{1,\dots,n\} \mid t\in L_j\}

1. Each relay constructs a candidate shared list S_i by sorting transactions into it in descending frequency order up to the maximum byte size. Ties are broken lexicographically via the transaction hash.

\text{Order: }t_1,\dots,t_n \text{ sorted by } f(t) \text{ descending, then hash}(t) \\ S_i = \{t_1, \dots, t_k\} \text{ where } k = \max\{j : \sum_{m=1}^j \text{bytes}(t_m) \leq 8\text{KB}\}

1. Each relay exposes its proposed shared inclusion list S_i via a get_shared_il() endpoint.
2. Relays poll peers and settle on the modal shared inclusion list S. Ties are broken by maximizing inclusion list byte size, with lexicographical sorting via the inclusion list hash as a fallback key.

S = \text{most frequent } S' \text{ among } \{S_1, \dots, S_n\} \\ \text{Tie-breaking: Maximize } \sum_{t \in S'} \text{bytes}(t), \text{ then hash}(S')

### Application and Incentives

This protocol allows the shared inclusion list to be derived without explicit consensus. As relays seek to maximize the number of competitive blocks they receive, they are incentivized to converge on a shared inclusion list in order to minimize the marginal cost a builder incurs when submitting a block.

The discretion any individual relay holds over the shared inclusion list is limited to an inclusion vote, put another way, individual relays cannot censor the content of the shared inclusion list beyond failing to adopt it.

The failure mode of the protocol corresponds to a case where relays fail to converge on a shared inclusion list. This should be precluded by the deterministic tie breaking procedure described in step 5. The worst case corresponds to each relay holding a different local inclusion list, which is equivalent to the base case in the existing local inclusion list implementation. In such an instance, builders would exercise discretion over whether to build for a union of inclusion lists, or deliver to specific relays only.

In contrast to designs like multiple concurrent proposers, the relays build standard-sized lists locally and truncation is performed over transaction frequency to ensure uniform application of the inclusion rule. This ensures that a full-sized shared inclusion list can be built even if individual relays were to fail to deliver a local list.

In summary, a basic protocol is sufficient for relays to converge on a shared inclusion list as this is collectively favorable. There is no excess value to be gained from building a competing local list (for example, a leaner list); in this case, the relay would be better served by opting out of rILs altogether.

### A Simple Extension: Shared Proposer Commitments

The mechanism can be extended to allows relays to share proposer commitments. Specifically, each relay would publicize the signed proposer constraints on-file, which may then be mirrored by peers. This reduces the risk of a slashing event for the proposer; relays sharing proposer constraints improve the proposer’s risk-adjusted return.

In practice, this can be efficiently accomplished through the following sequential steps:

1. Each relay r_i fetches proposer commitments from the proposer or designated gateway as per the standard procedure defined in the Fabric standard.
2. Each relay composes an array of the SignedCommitment objects it has observed and exposes it via a get_proposer_commitments() endpoint.
3. Relays poll peers and add any newly observed SignedCommitment to their block constraint verification process, if these are appropriately signed.

This procedure is incentive-compatible as relays continue to compete on latency during the slot auction, while reducing the slashing risk surface proposers and builders are exposed to. For this reason, proposers and builders are likely to express a preference for relays sharing proposer commitments.

Ultimately, this leads to a better risk-adjusted return from proposer commitments, which may reduce the risk premium charged to users, making Ethereum’s service offering more competitive.

### Future Directions

In the future, relays may elect to extend block constraints sharing into a more binding consensus implementation. This approach could be used to increase mrIL efficiency by minimizing builder overhead, and as a way of distributing the value generated by relay block merging more objectively.

The design may also be extended in scope to increase the value generated by relay block merging, by allowing relays to share transactions eligible for merging with each other.
