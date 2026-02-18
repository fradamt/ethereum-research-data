---
source: magicians
topic_id: 22138
title: "EIP-7834: Separate Metadata Section for EOF"
author: kuzdogan
date: "2024-12-09"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7834-separate-metadata-section-for-eof/22138
views: 202
likes: 6
posts_count: 8
---

# EIP-7834: Separate Metadata Section for EOF

Discussion topic for [EIP-7834](https://github.com/ethereum/EIPs/pull/9100)

#### Update Log

- 2024-12-06: initial draft Add EIP: Separate Metadata Section for EOF by kuzdogan · Pull Request #9100 · ethereum/EIPs · GitHub

#### External Reviews

None as of 2024-12-09.

#### Outstanding Issues

None as of 2024-12-09.

## Summary

This EIP proposes a separate section for contract metadata in the EOF. Initially discussed at [EOF Implementers Call #62 · Issue #1192 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1192).

Solidity appends contract metadata in the runtime bytecode in legacy bytecode (see [playground.sourcify.dev](https://playground.sourcify.dev)). The current practice already makes it difficult to locate these in nested contracts and [makes source-code verification difficult](https://docs.sourcify.dev/blog/finding-auxdatas-in-bytecode/).

The tentative practice in EOF for any “metadata” in the Solidity compiler is to add it in the beginning of the `data_section`. However, changes to the size of `data_section` do affect the contract’s `code` by shifting `DATALOADN` offsets. This makes it impossible to verify two identical contracts with different metadata sizes.

Solidity’s default metadata is just one current example. Other kinds of metadata might be needed by any tooling or contract developer in the future. It is good practice to have a separate section for  contract metadata that is unreachable by the code, and any changes to its size do not affect the actual code.

## Replies

**charles-cooper** (2024-12-17):

Discussed this somewhat offline in the discord and on an EOF call, and wanted to point out that it increases EVM complexity without any in-protocol benefit. Metadata can be implemented using other in-EVM approaches. For example, in Vyper, metadata about the runtime code lives in the initcode. This serves two purposes: it makes it unreachable from runtime code, and also reduces runtime code size (which is both expensive and subject to the EIP-170 hard limit).

[@kuzdogan](/u/kuzdogan) pointed out that that might be inconvenient for off-chain tooling to index, so another approach would be issuing an event (like `log VyperMetadata(metadata_bytes)`) at the time of contract creation for indexers to consume. This is slightly more expensive than the initcode approach, but still cheaper than storing in runtime code, and also achieves the unreachability goal as logs also exist as a a kind of metadata within the EVM which is unreadable from EVM code. The point is that there are in-EVM approaches which work today for this, so the goals of this EIP can be achieved without burning a new section kind.

---

**shemnon** (2024-12-17):

With the EIP-7834 section we can still use the vyper approach to metadata.  The initcode container is the container that has the metadata section, and the deployed contracts do not have the metadata section.  Then users can go back through chain history to look at the contract creation to get the metadata.  Whether compilers attach metadata to the initcode container or the runtime container is a choice the compiler will make.

I do think there is net-positive protocol benefit to this section.  Right now we don’t have any place to associate with code data that is not accessible durring execution and can be used for whatever purpose that the code producer wants.  The first pass would be for compilers to store their validation information, but I also see that regulated L2s may need to attach “legends” to their contracts that regulators may want for their own purposes.  If we continue to drop these into the execution-accessible data section then we make the math more complex as to where to go for extra aux-data, and it makes it possible to create aux-data that could “mask” the metadata.

In it’s current form, where it is a segment of the EOF code that is ignored at runtime and treated as opaque, it frees up a lot more design space further down the supply chain.

---

**manuelwedler** (2024-12-20):

In reference to the alternative approach [@charles-cooper](/u/charles-cooper) pointed out:

In my opinion, it is important to attach the metadata to the runtime bytecode. Both other approaches, putting the metadata in the initcode and in an event, require indexing the chain if you want to access the metadata. This is inconvenient for tooling and verifiers, but, much more importantly, it is also inconvenient and not always feasible for users.

Users need to have easy access to the metadata or integrity hash. If they download the source code from a service like Sourcify, they should be able to verify themselves that the source they downloaded is correct. For this, they need the metadata or integrity hash. If it is not in the runtime code, users who don’t index the chain themselves would have to depend on external services. So, attaching the metadata to the runtime code is also a matter of enabling users not to have to trust third parties.

---

**kuzdogan** (2024-12-24):

> it increases EVM complexity without any in-protocol benefit

I disagree with the above point. Having one less section might seem less complexity on the protocol, however, this basically pushes the complexity to the application layer and tooling. Any convention to store metadata in the `data_section` requires coordinated approaches across compilers and tooling on how to decode this section, and again, this directly affects contract’s code.

The whole point of the EOF upgrade is to bring structure to code and this EIP helps achieve that by handling a missing use case. It also provides a larger design space for anyone to do whatever they want in the `metadata_section` without affecting the rest of the code.

One can say that EOF makes things more “complex” too. Maybe, but for good reasons to make other parts of the Ethereum stack simpler.

> an event (like log VyperMetadata(metadata_bytes))

I don’t fully understand how this would be done. Do you mean the compiler my default adds a `LOG` to the contract code. Is there a possibility this gets in conflict with user defined logs? And potentially someone else can emit the same log with a different integrity value?

Logs option might be worth considering for this specific use case too. My feeling is still it’s worth keeping the contract’s metadata closer to it’s actual code. And also even if we go full logs route for compiler metadata, I feel there are still use cases that we don’t know yet that would use the `metadata_section` and benefit from having that section that’s isolated from the code and data.

---

**pdobacz** (2025-02-20):

I’d like to make visible an interaction with EOF’s current idea to support counterfactual deployments, which is basically the [TXCREATE design](https://eips.ethereum.org/EIPS/eip-7873).

`TXCREATE` generates the new address with a `keccak256(sender+salt)` scheme (no initcode hash!). We celebrated an added benefit of this, which is that it excludes the EIP-7834 metadata section from address hashing. This is good, because the metadata shouldn’t usually impact the address. However, the counterfactual deployments support is based on the factory contract including the `initcode_hash` in the `salt` and then also `TXCREATE` uses the same `initcode_hash` to lookup the initcontainer. But that `initcode_hash` right now would **include** the metadata contents, because it’s just hashing of the opaque bytes of the initcontainer.

If we do not do anything (I don’t yet have any ideas what we could do) the reality will be that the user would have a choice:

1. Have factory use initcontainer_hash in the salt and not include any metadata - making the new_address deterministic and the deployment counterfactual
2. Have factory use initcontainer_hash in the salt and include metadata - making the new_address dependent on metadata, keeping the deployment counterfactual otherwise
3. Have factory not use initcontainer_hash in the salt and include metadata - disabling counterfactual

This is to my understanding not a diminishment compared to how legacy works. Just not as good as we could wish for.

---

**cameel** (2025-02-20):

I’d say this is actually an argument in favor of having a metadata section.

Note that the problem exists regardless of whether EOF provides a dedicated section or not. If it does not, the metadata will still be there, affecting the hash. It will just sit in the data section (unless disabled by the user).

Having a dedicated section actually improves the situation slightly by opening up a potential solution: excising the metadata from the container before hashing. I’m not saying this is necessarily better than the other options or even worth it - it adds complexity and having metadata affect the hash like on legacy may not be such a big issue in practice - but that option is completely off the table when the skippable metadata is mixed with data that may affect execution. With a metadata section we can choose to do it if it turns out that keeping the metadata in what we hash is enough of a problem.

---

**pdobacz** (2025-02-20):

Agreed, with a caveat here:

> excising the metadata from the container before hashing

This isn’t easy. The metadata sections might be present in all subcontainers in the initcontainer hierarchy, so it would take quite a bit of complex logic to excise (including modify the sizes etc etc). It is of course more available than compared to not having metadata section at all, but still very unlikely.

