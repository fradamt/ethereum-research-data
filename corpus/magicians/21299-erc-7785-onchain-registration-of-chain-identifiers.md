---
source: magicians
topic_id: 21299
title: "ERC-7785: Onchain registration of chain identifiers"
author: SamWilsn
date: "2024-10-08"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7785-onchain-registration-of-chain-identifiers/21299
views: 778
likes: 10
posts_count: 10
---

# ERC-7785: Onchain registration of chain identifiers

https://github.com/ethereum/ERCs/pull/669

## Replies

**yuliyaalexiev** (2024-10-09):

Moved the PR to the ERCs repo - please update to …/ethereum/ERCs/pull/669

---

**abcoathup** (2024-10-09):

https://github.com/ethereum/ERCs/pull/669

---

**0xMims** (2025-02-05):

Just curious if there are any updates to this EIP? Will this be added as a draft to the EIP website?

---

**u59149403** (2025-04-20):

ERC-7785 says:

> We propose to extend the size of identifiers to 32 bytes

According to [EIP-2294: Explicit bound to Chain ID size](https://eips.ethereum.org/EIPS/eip-2294) , safe size of chain id is 31 (sic!) bytes. From that EIP:

> (1, 2^31 - 1): “Safe Range”, the higher bound is decided by Javascript number

---

**SamWilsn** (2025-04-28):

ERC-7785 may or may not be adopted. It’s just a proposal currently.

---

**adraffy** (2025-05-13):

A desirable property of a chain id is that it can be embedded in a coin type.  A wide (256-bit) chain id makes this impossible (assuming a coin type is a `uint256`).

Currently, small chain ids embed with `1 << 31 | <chain id>`

If we’re fixated on 256 bits, could we modify this proposal such that bit 31 is always set if it is generated via 7785 with a comment that the same bit should be clear if the coin type is non-EVM?

IMO, a smaller bit width should be chosen so there still is room in the coin type space to embed other tagged information.

---

**teddy** (2025-05-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adraffy/48/15245_2.png) adraffy:

> Currently, small chain ids embed with 1

I’ve pushed a proposal to expand ENS to support an extensible chain format, which could allow for arbitrary-length chainids and possibly adding some metadata as well in the future: [Use caip 350 in ENSIP-11 and ENSIP-19 by 0xteddybear · Pull Request #30 · ensdomains/ensips · GitHub](https://github.com/ensdomains/ensips/pull/30)

While that’d make the way re refer to chains potentially more consistent across different kind of usages. It wouldn’t be actually necessary to make 7785 work at a technical level:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adraffy/48/15245_2.png) adraffy:

> If we’re fixated on 256 bits, could we modify this proposal such that bit 31 is always set if it is generated via 7785 with a comment that the same bit should be clear if the coin type is non-EVM?

Assuming the large chainids are the output of a hash function, the higher 28 bytes could be used to tell them apart from short chainids/cointypes. e.g currently ENSIP-11 compliant resolvers take a `uint256` where the first 28 bytes are zero and the least significant 4 ones have their meaning determined by ENSIP-11 and ENSIP-9.

---

**adraffy** (2025-05-14):

Currently, small chain ids are embedded as you say `<224 zeros>1<31 bits of chain id>`, but if we assume every coin type with upper bits set (>= 2^32) is EVM, there’s no room left for future ideas that want to carve out some part of this space.

The minimal suggestion is that 7785 chain ids have bit 31 force set: `keccak256(...) | EVM_BIT`, such that if any part of the upper <224 bits> is non-zero, it’s a wide coin type.

This restores the `EVM_BIT` but we’ve still lost the ability to embed further tags into a coin type.  And if another ecosystem wants to expand beyond SLIP-44 and decide to use large coin types, then they have a 50% chance of setting `EVM_BIT` by accident and appearing like “oh, this is an EVM coin type”.

A better suggestion would be to truncate 7785 to a smaller number of bits, like 128 or 160, so there is ample space for future tagging.

The only oddity is that the `EVM_BIT` appears in the middle of this hash if we continue that convention.

I can see the following options assuming 160 bits:

1. 1
(eg. keccak256(...)[:20] | EVM_BIT w/bit 31 ignored)
2. 1
(keep EVM_BIT logic, shift right by 32 to extract chain id)
3. 1
(new WIDE_EVM_BIT = 1 << 160)

In all cases, the upper 64-96 bits are available for future use.

---

**ndeto** (2025-08-29):

We’ve been working on a POC for the ERC-7785 registry at [unruggable.com](http://unruggable.com) and a few points have come up for broader discussion.

### 1. Interop Between Standards

The registry is meant to support two interop standards: [ERC-7930](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7930.md) and [ERC-7828](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7828.md).

- ERC-7828: human-friendly names resolve to the 7785 identifier.
- ERC-7930: binary format.

**Suggestion:** Incorporate the CAIP-2 attributes already present in a 7930 address into the derivation of a 7785 identifier.

**ERC-7930 address format:**

```auto
┌─────────┬───────────┬──────────────────────┬────────────────┬───────────────┬─────────┐
│ Version │ ChainType │ ChainReferenceLength │ ChainReference │ AddressLength │ Address │
└─────────┴───────────┴──────────────────────┴────────────────┴───────────────┴─────────┘
```

- A 7930 address already includes the CAIP-2 namespace as chainType and chainReference (with the EVM chain Id encoded in chainReference). The proposal is that these can be carried into the derivation of the 7785 chain identifier.
- Benefits:

A binary address can be mapped directly to the registry via its CAIP-2 attributes.
- The approach extends naturally to non-EVM chains, since CAIP-2 is not EVM-specific.

### 2. ENS-Specific Logic

On the ENS side, we will be proposing an ENSIP for resolving `chain-id` text records. This allows human-friendly names like `base.l2.eth` to resolve deterministically to a 7785 chain identifier.

- Draft ENSIP: https://github.com/nxt3d/ensips/blob/ensip-ideas/ensips/ensip-TBD-18.md

### 3. POC Update

- We have built a POC registry that resolves human-friendly chain names (base.l2.eth) to 7785 chain identifiers.
- This POC already incorporates CAIP-2 attributes into the derivation.
- The chain-id text-record ENSIP is also implemented.

POC Repo: https://github.com/unruggable-labs/erc-7785-registry

**Future Use cases:**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adraffy/48/15245_2.png) adraffy:

> I can see the following options assuming 160 bits:
>
>
> 1
> (eg. keccak256(...)[:20] | EVM_BIT w/bit 31 ignored)
> 1
> (keep EVM_BIT logic, shift right by 32 to extract chain id)
> 1
> (new WIDE_EVM_BIT = 1
>
> In all cases, the upper 64-96 bits are available for future use.

Regarding this point about using a 160-bit truncated hash, an equally important question is: Which derivation attributes should be used to standardize the interplay between 7828, 7930, and ENS. On our side (Unruggable), we’ll also be pursuing the ENSIP since that is directly within the ENS domain.

