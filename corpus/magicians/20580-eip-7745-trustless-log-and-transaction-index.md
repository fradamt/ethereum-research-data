---
source: magicians
topic_id: 20580
title: "EIP-7745: Trustless log and transaction index"
author: zsfelfoldi
date: "2024-07-17"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7745-trustless-log-and-transaction-index/20580
views: 678
likes: 9
posts_count: 15
---

# EIP-7745: Trustless log and transaction index

Discussion topic for EIP-7745

https://github.com/ethereum/EIPs/pull/8740



      [github.com/zsfelfoldi/EIPs](https://github.com/zsfelfoldi/EIPs/blob/new-log-filter/EIPS/eip-7745.md)





####

  [new-log-filter](https://github.com/zsfelfoldi/EIPs/blob/new-log-filter/EIPS/eip-7745.md)



```md
---
eip: 7745
title: Two dimensional log filter data structure
description: An efficient and light client friendly replacement for block header bloom filters
author: Zsolt Felföldi (@zsfelfoldi)
discussions-to: https://ethereum-magicians.org/t/eip-7745-two-dimensional-log-filter-data-structure/20580
status: Draft
type: Standards Track
category: Core
created: 2024-07-17
---

## Abstract

Replace the fixed 2048 bit log event bloom filters in block headers with a new data structure that can adapt to the changing number of events per block and consistently guarantee a sufficiently low false positive ratio. Unlike the per-block bloom filters, the proposed structure allows searching for specific events by accessing only a small portion of the entire dataset which can also be proven with a Merkle proof, making the search both efficient and light client friendly.

As an additional benefit, the new structure provides more precise position information on the potential hits (block number and transaction index) allowing the searcher to only look up a single receipt for each potential hit.

## Motivation

```

  This file has been truncated. [show original](https://github.com/zsfelfoldi/EIPs/blob/new-log-filter/EIPS/eip-7745.md)










An efficient and light client friendly replacement for bloom filters. This EIP proposes a new data structure that adds a moderate amount of consensus data that is optional to store long term, has limited processing and memory requirements and allows searching for log events with 2-3 orders of magnitude less bandwidth than what bloom filters allowed back when they were not rendered useless by over-utilization. It also inherently adapts to changing block utilization and maintains a constantly low average false positive ratio.

## Replies

**wjmelements** (2024-07-17):

Why `SHA2` instead of `SHA3`?

---

**zsfelfoldi** (2024-07-18):

Because log_filter_tree uses SSZ merkleization which uses SHA2. I’m not sure whether and when the existing EL structures will be converted to SSZ but for this purpose a binary tree is absolutely the logical choice, Merkle multiproofs are nice and easy with SSZ hash trees, so I think that sticking with the old hexary MPT format would be really impractical. And if we use an existing format with existing tooling then I don’t see a reason to complicate that by not using the hash function it was specified with.

---

**sbacha** (2025-01-10):

Will there be a test net support for this? Very interested in using this

---

**etan-status** (2025-03-24):

Have split the ProgressiveByteList to its own EIP: [Add EIP: SSZ ProgressiveByteList by etan-status · Pull Request #9523 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9523)

---

**frangio** (2025-06-28):

Have any “explainer” articles or videos been published about this EIP?

---

**greg7mdp** (2025-07-02):

See the mp4 here: [Releases · etan-status/purified-web3 · GitHub](https://github.com/etan-status/purified-web3/releases)

---

**sbacha** (2025-07-18):

> This PR is #1 of a 3-part series that implements the new log index intended to replace core/bloombits. Replaces #30370
>
>
> This part implements the new data structure, the log index generator and the search logic. This PR has most of the complexity but it does not affect any existing code yet so maybe it is easier to review separately.
>
>
> FilterMaps data structure explanation: gist.github.com/zsfelfoldi/a60795f9da7ae6422f28c7a34e02a07e
>
>
> Log index generator code overview: gist.github.com/zsfelfoldi/97105dff0b1a4f5ed557924a24b9b9e7
>
>
> Search pattern matcher code overview: gist.github.com/zsfelfoldi/5981735641c956afb18065e84f8aff34
>
>
> Note that the possibility of a tree hashing scheme and remote proof protocol are mentioned in the documents above but they are not exactly specified yet. These specs are WIP and will be finalized after the local log indexer/filter code is finalized and merged.



      [github.com/ethereum/go-ethereum](https://github.com/ethereum/go-ethereum/pull/31079)














####


      `master` ← `zsfelfoldi:log-filter-1d`




          opened 08:55AM - 27 Jan 25 UTC



          [![](https://avatars.githubusercontent.com/u/9884311?v=4)
            zsfelfoldi](https://github.com/zsfelfoldi)



          [+4825
            -0](https://github.com/ethereum/go-ethereum/pull/31079/files)







This PR is #1 of a 3-part series that implements the new log index intended to r[…](https://github.com/ethereum/go-ethereum/pull/31079)eplace core/bloombits.
Replaces https://github.com/ethereum/go-ethereum/pull/30370

This part implements the new data structure, the log index generator and the search logic. This PR has most of the complexity but it does not affect any existing code yet so maybe it is easier to review separately.

FilterMaps data structure explanation:
https://gist.github.com/zsfelfoldi/a60795f9da7ae6422f28c7a34e02a07e

Log index generator code overview:
https://gist.github.com/zsfelfoldi/97105dff0b1a4f5ed557924a24b9b9e7

Search pattern matcher code overview:
https://gist.github.com/zsfelfoldi/5981735641c956afb18065e84f8aff34

Note that the possibility of a tree hashing scheme and remote proof protocol are mentioned in the documents above but they are not exactly specified yet. These specs are WIP and will be finalized after the local log indexer/filter code is finalized and merged.

---

**etan-status** (2025-11-05):

Made an explainer on [Event logs - Pureth](https://pureth.guide/event-logs/) and an EPF fellow actually managed to prototype a subset of it.

The EIP is quite challenging to implement in other clients (database format, deep reorgs etc), and the proof format has not yet been validated against purifiers (Helios / Nimbus) and L2s. A network protocol for syncing would also be needed. Further, the tree structure could benefit from a bump to the latest ProgressiveList (EIP-7916).

Given these challenges, I think this is one of the EIPs that needs more time. It would be interesting to collect feedback from other clients who implemented accelerated log indices, and also have a concrete answer to syncing and proving. There’s also the EIP-7792 alternative (based on [IVC for scalable trust-free Ethereum logs - HackMD](https://notes.ethereum.org/@vbuterin/parallel_post_state_roots)) of storing the commitment in an external zk-proven system, rather than having every node maintain it.

As this EIP uses SSZ, a good first step would be ensuring that all EL teams have production grade SSZ libraries (as a priority for G*). This has been repeatedly used in the past as an excuse to delay SSZ based proposals. Once that happens, would re-consider this EIP for H* (which would also provide enough time to address the open questions).

---

**zsfelfoldi** (2025-12-03):

Now that the EIP is in PFI status for Amsterdam and next ACDE is coming up, I updated the EIP and also published an initial draft of an EELS implementation:


      ![image](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7745)





###



An efficient, light client and DHT friendly replacement for block header bloom filters












      [github.com/ethereum/execution-specs](https://github.com/ethereum/execution-specs/pull/1832)














####


      `forks/amsterdam` ← `zsfelfoldi:eip-7745`




          opened 03:30AM - 02 Dec 25 UTC



          [![](https://avatars.githubusercontent.com/u/9884311?v=4)
            zsfelfoldi](https://github.com/zsfelfoldi)



          [+845
            -9](https://github.com/ethereum/execution-specs/pull/1832/files)







## 🗒️ Description

This PR implements EIP-7745 in the Amsterdam fork.
https:/[…](https://github.com/ethereum/execution-specs/pull/1832)/eips.ethereum.org/EIPS/eip-7745

Note that this PR is still WIP and exists only in order to publicly track progress. Basic tox linter tests pass but still has some errors.

## 🔗 Related Issues or PRs

N/A.

## ✅ Checklist

- [ ] All: Ran fast `tox` checks to avoid unnecessary CI fails, see also [Code Standards](https://eest.ethereum.org/main/getting_started/code_standards/) and [Enabling Pre-commit Checks](https://eest.ethereum.org/main/dev/precommit/):
    ```console
    uvx tox -e static
    ```
- [ ] All: PR title adheres to the [repo standard](https://eest.ethereum.org/main/getting_started/contributing/?h=contri#commit-messages-issue-and-pr-titles) - it will be used as the squash commit message and should start `type(scope):`.
- [ ] All: Considered adding an entry to [CHANGELOG.md](/ethereum/execution-spec-tests/blob/main/docs/CHANGELOG.md).
- [ ] All: Considered updating the online docs in the [./docs/](/ethereum/execution-spec-tests/blob/main/docs/) directory.
- [ ] All: Set appropriate labels for the changes (only maintainers can apply labels).
- [ ] Tests: Ran `mkdocs serve` locally and verified the auto-generated docs for new tests in the [Test Case Reference](https://eest.ethereum.org/main/tests/) are correctly formatted.
- [ ] Tests: For PRs implementing a missed test case, update the [post-mortem document](/ethereum/execution-spec-tests/blob/main/docs/writing_tests/post_mortems.md) to add an entry the list.
- [ ] Ported Tests: All converted JSON/YML tests from [ethereum/tests](/ethereum/tests) or [tests/static](/ethereum/execution-spec-tests/blob/main/tests/static) have been assigned `@ported_from` marker.

#### Cute Animal Picture

![Put a link to a cute animal picture inside the parenthesis-->]()

---

**RazorClient** (2025-12-09):

Yes

we are working on Nimbus for the implementation of the minimised(the log index and filtermap) and also the extended version with the publishing and verifying the proof part.

This is also a broader effort to support EIP-7919 testing and inclusion.

We would want to deliver the entire package with the proofs tho as that is quite benifical to the trust minimised user.

An estimated timeline would be end jan or feb

---

**zsfelfoldi** (2025-12-16):

I updated EIP-7745 with specs for the log index proof format and the required wire protocol extension for log index state initialization:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7745.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7745.md)



```md
---
eip: 7745
title: Trustless log and transaction index
description: An efficient, light client and DHT friendly replacement for block header bloom filters
author: Zsolt Felföldi (@zsfelfoldi)
discussions-to: https://ethereum-magicians.org/t/eip-7745-two-dimensional-log-filter-data-structure/20580
status: Draft
type: Standards Track
category: Core
created: 2024-07-17
requires: 7916
---

## Abstract

Replace the fixed 2048 bit log event bloom filters with a new lookup index data structure that can adapt to the changing number of events per block and consistently guarantee a sufficiently low false positive ratio, allowing efficient trustless proofs of log event queries, canonical block hash and transaction hash lookups.

The proposed structure maps all index entries (log events, transaction and block markers) onto a global linear index space and hashes them into a binary Merkle tree based on that index. It also contains a _filter map_ for every fixed length section of the index space. These are two dimensional sparse bit maps that provide an efficient probabilistic method for looking up indexed values or query patterns of values, yielding potential matches in the form of exact positions in the linear index space. Unlike the per-block bloom filters, they allow searching for specific events by accessing only a small portion of the entire dataset which can also be proven with a Merkle proof, making the search both efficient and light client friendly.

The proposed structure can be efficiently used both for local search and for remote proof generation/verification, thereby simplifying implementation of provers and verifiers. It also allows validators that are not interested in either searching or proving logs to generate the index root hash by maintaining a minimal index state with a relatively small (hard capped) size.
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7745.md)












      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/assets/eip-7745/log_index_proof_format.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/assets/eip-7745/log_index_proof_format.md)



```md
## EIP-7745 log index proof format

A log index proof is a Merkle multiproof that fully or partially proves the contents of certain filter map rows and index entries. The proof format specified here can be used to prove the results of log queries, transaction and block hash lookups, and also to initialize the log index state. The root hash of any proof can be calculated and validated against the expected log index root regardless of its contents but the required contents (the proven subset of filter rows and index entries) depend on the use case. These use cases and their conditions for proof validity are detailed in separate documents.

The general format of a log index proof is defined as follows:

```
class LogIndexProof(Container):
    filter_rows: FilterRows
    index_entries: IndexEntries
    next_index: uint64
    proof_nodes: List[Bytes32]
```

The filter map and index entry data included in the proof uses a more compact encoding than the binary Merkle tree leaves but their contents can be translated into a known set of tree leaves. The `proof_nodes` list provides additional tree node contents required to calculate the log index root and validate it against the one found in the relevant block header.

Note that the position and order of the proof nodes is not specified in the proof but can be determined based on the set of known leaves. Also note that the `next_index` pointer of the log index is always supplied with the proof and its leaf node is always considered known.

### Filter map row encoding

```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/assets/eip-7745/log_index_proof_format.md)












      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/assets/eip-7745/wire_protocol_extension.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/assets/eip-7745/wire_protocol_extension.md)



```md
## EIP-7745 wire protocol extension

This document specifies the extensions to the [Ethereum Wire Protocol](https://github.com/ethereum/devp2p/blob/master/caps/eth.md) required to initialize the log index.

### Proposed new messages

#### GetLogIndexProof (0x12)

`[request-id: P, referenceBlockHash: B_32, proofType: P, proofSubset: P]`

Require peer to return a __LogIndexProof__ message containing a log index proof that proves the specified subset of the specified type of initialization data from the log index tree belonging to the specified _reference block_.

Note that all clients are expected to be able to serve log index proofs using either the current finalized block or the previous one as _reference block_. Also note that the initialization data served by this protocol are split into a limited number of pre-defined subsets so that proofs can be pre-generated for each potential _reference block_. This, together with the limited size of each individual response, makes it easy to ensure that serving this data will not be an excessive burden on the clients.

#### LogIndexProof (0x13)

`[request-id: P, log_index_proof]`

This is the response to __GetLogIndexProof__, providing the RLP encoded log index proof of the requested partial initialization data. See the [log index proof format](log_index_proof_format.md) specification.

```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/assets/eip-7745/wire_protocol_extension.md)

---

**ADMlN** (2026-01-09):

Has someone estimated how much less efficient a variant of this EIP would be if it provided cryptographic collision-resistance? It is stated that bloom filters are practically useless now because of high false-positive rates, and now the suggestion is to replace it with something where it is already known that collisions can be mined?

---

**zsfelfoldi** (2026-01-09):

Collision resistance is proportional to the amount of data added to the filter maps per entry (determined by MAP_WIDTH); right now this is 24 bits so it takes 2^24 attempts to generate a false positive. Achieving 256 bits of collision resistance would increase filter map data size by roughly 10x, affecting both the database size of full nodes and the length of trustless proofs. The general design would still hold up and retain its other advantages (like the in-memory maintainable log index state) while losing a significant performance edge (that is admittedly due to its probabilistic nature).

It should be noted though that the old bloom filter did not become useless because of deliberate collision attacks, in fact I do not know about any such attacks actually happening. False positives increased because of random collisions, because of the filter not being able to adapt to the changing number of entries per block (which the new design is very good at, always having constant map density). Also, as noted in the EIP, it is mostly just the block builders who could realistically carry out such an attack.

---

**zsfelfoldi** (2026-01-09):

One possible way to kind of have the best of both worlds would be to create two filter maps trees per epoch, one having just the short column indices (3 bytes per entry) that work well enough for non-attack scenarios, and another one with extended indices (32 bytes per entry). This way the provers could still create efficient proofs and only revert to the extended data if an excessive amount of false positives is detected. It would still be a significant extra storage cost for provers and approximately double CPU costs for processing the index (though mostly just hashing, which is parallelizable). I’d say this is a low priority issue at this point but there is a solution if needed.

