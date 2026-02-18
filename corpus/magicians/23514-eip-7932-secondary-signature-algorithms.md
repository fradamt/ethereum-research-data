---
source: magicians
topic_id: 23514
title: "EIP-7932: Secondary Signature Algorithms"
author: SirSpudlington
date: "2025-04-13"
category: EIPs > EIPs core
tags: [evm, wallet]
url: https://ethereum-magicians.org/t/eip-7932-secondary-signature-algorithms/23514
views: 540
likes: 4
posts_count: 8
---

# EIP-7932: Secondary Signature Algorithms

Discussion topic for [EIP-7932](https://eips.ethereum.org/EIPS/eip-7932)

This EIP introduces a new registry & standarized interface for handling alternative signature algorithms & introduces a precompile for account abstraction purposes.

This allows proposals such as [EIP-6404](https://eips.ethereum.org/EIPS/eip-6404) to use this registry without implementing their own version.


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7932)





###



Introduces a precompile and registry for handling alternative signature algorithms










#### Update Log

- 2025-04-12: initial draft PR
- 2025-06-03: Move to review state: PR
- 2025-06-21: Identified an issue where the additional_info is not signed and can be modified. Fixed via setting r to 0, but s to keccak256(alg_type || signature_info).
- 2025-08-06: Reworked the abstract and the title to be more descriptive
- 2025-08-07: Huge rework to be EIP-6404 based rather than RLP (moved back to draft)
- 2025-10-04: Reintroduced RLP support and made several smaller modifications to fix some malleability concerns
- 2025-11-05: Removed SSZ support (as it may be handled natively by EIP-6404) and clarified some missing details PR
- 2025-12-02: Fully removed TX support & introduced a pythonic version of the registry
- 2025-12-05: Moved to a more modern registry design

#### External Reviews

- 2025-04-12: Several PR reviews
- Reddit post

#### Outstanding Issues

None as of 2025-04-12.

## Replies

**SamWilsn** (2025-04-15):

[EIP-7702](https://eips.ethereum.org/EIPS/eip-7702#set-code-transaction) defines a transaction type with nested signatures. You should probably explain how 7702 and this proposal interact.

---

**SamWilsn** (2025-04-15):

I’d extend this proposal with support for patching `ecrecover` as well. Fixing the outer transaction signature without fixing `ecrecover` will only solve part of the PQ problem.

One approach that’s been tossed around is to embed a list of tuples in the transaction that contain a mapping from the `ecrecover` arguments to the real signature/algorithm data. I haven’t thought that through entirely, but hopefully it’s a starting point.

---

**SirSpudlington** (2025-04-15):

The [EIP-7702](http://eips.ethereum.org/EIPS/eip-7702) problem was solved by adding space for additional signatures after the transaction, I don’t know how practical this would be but it was one of my better solutions. (edit: I also added the `NULL algorithm` for edge cases where the initial signature is secp256k1 but the others are not)

~~I also patched `ecrecover` instead of using a mapping as that seemed a bit too complex, I made any `v` recovery value `v > 0xFF && v <= 0xFFFF` trigger the contract to be treated as an `Algorithmic`. Might still need to work on the name, but for now `Algorithmic transaction rolls of the tounge`.~~ I am going to introduce a new precompile, with a name similar to `sigrecover` as the “overload the `v` value” seemed somewhat hacky and may break some implementations.

---

**SirSpudlington** (2025-06-03):

I have moved this EIP to it’s review state, [PR](https://github.com/ethereum/EIPs/pull/9853) for anyone interested (also specified in update log above).

---

**SirSpudlington** (2025-08-07):

After a conversation with a member of the Ethereum Foundation, I have rebased this EIP onto EIP-6404. I’d like some feedback on the [newer version](https://github.com/SirSpudlington/EIPs/blob/eip-6404-7932-integration/EIPS/eip-7932.md) before merging it into the main repo.

---

**Amxx** (2025-09-12):

If the length of the input is already known, we don’t need to encode the length of the signature part. You can just assume that `input[33:]` is the signature.

```auto
def sigrecover_precompile(input: Bytes) -> Bytes:
  # Recover signature length and type
  assert(len(input) >= 33)
  hash: Hash32 = input[:32]
  algorithm_type: uint8 = input[32]
  signature: Bytes = input[33:] # len(signature) == len(input) - 33

  # Ensure the algorithm exists and signature is correct size
  if algorithm_type not in Algorithms:
    return ExecutionAddress(0x0)

  alg = Algorithms[algorithm_type]

  # Sig length must be smaller than alg.MAX_SIZE and
  # equal to the remaining call data
  if len(signature) > alg.MAX_SIZE:
    return ExecutionAddress(0x0)

  # Run verify function
  try:
    return alg.verify(signature, hash)
  except:
    return ExecutionAddress(0x0)
```

---

**SirSpudlington** (2025-09-12):

This would be a better idea. I believe I initally put in the checks as a sort of anti-DOS measure, but that is obtained via memory and calldata costs. I’ll redo the sigrecover section.

