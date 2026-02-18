---
source: ethresearch
topic_id: 23895
title: Worst-Case Block Size and Calldata Repricing for Glamsterdam
author: Nero_eth
date: "2026-01-20"
category: Execution Layer Research
tags: [scaling]
url: https://ethresear.ch/t/worst-case-block-size-and-calldata-repricing-for-glamsterdam/23895
views: 123
likes: 6
posts_count: 3
---

# Worst-Case Block Size and Calldata Repricing for Glamsterdam

# Worst-Case Block Size and Calldata Repricing for Glamsterdam

Ethereum’s worst-case block size keeps surfacing as an issue, typically via adversarial constructions rather than honest usage. Average blocks are small; worst-cases are not.

## Background

Pre-Pectra, worst-case block size was driven by Snappy compression inefficiencies and cheap calldata (4/16 gas for zero/non-zero bytes).

**[EIP-7623](https://eips.ethereum.org/EIPS/eip-7623)** (Pectra) addressed this by raising calldata costs to **10/40 gas** for calldata-heavy transactions. This introduced a new worst-case construction:

- ~3/5 of block gas spent on EIP-2930 Access Lists
- ~2/5 spent on calldata
- Structured to avoid triggering the EIP-7623 floor → “just enough execution gas to keep paying the lower price”

The issue: access list data is essentially free. This circumvents EIP-7623 and inflates worst-case block size again.

## Why This Matters Now

Rising block gas limits and blob counts will further stress propagation. While **[ePBS](https://eips.ethereum.org/EIPS/eip-7732)** (shipping with Glamsterdam) extends propagation time, **[BALs](https://eips.ethereum.org/EIPS/eip-7928) increase raw block data**: counterproductive on this front.

### Proposed Repricings (Both EIPs are CFI’d for Glamsterdam)

#### : Increase Access List Cost

Applies calldata costs to transaction access lists. This closes the circumvention path: gas payment now tracks actual data as if it was calldata.

#### : Increase Calldata Floor Cost

Two options under discussion:

1. As spec’ed: raise pricing from 10/40 → 15/60 gas for calldata-heavy transactions; simple 50% price increase
2. Alternative: flat 64/64 gas per byte, eliminating the zero/non-zero distinction

### Interaction with ePBS

[ePBS](https://eips.ethereum.org/EIPS/eip-7732) might come with a **dynamic payload deadline**: the PTC enforces tighter deadlines for smaller payloads.

The CL does not want to enshrine a specific Snappy encoding. Flat per-byte pricing (option 2) is better here: the worst-case size becomes more predictable when using the **uncompressed payload size**.

## A possible way forward

With EIP-7976, as-is (15/60 for zero and non-zero bytes), we can get to a block gas limit of 150 million without exceeding a worst-case block size of 4 MiB. The alternative, arguably, the more aggressive repricing (64/64; no distinction between zero and non-zero bytes), would get us down to a worst-case block size of 2.25 MiB, leaving room for further gas limit increases toward 300 million in the future.

[![calldata pricing vs block size](https://ethresear.ch/uploads/default/optimized/3X/a/d/adfaaf4faa6d8ef1db6a28f9b7e0f6d7b372521f_2_690x368.png)calldata pricing vs block size1128×603 73.3 KB](https://ethresear.ch/uploads/default/adfaaf4faa6d8ef1db6a28f9b7e0f6d7b372521f)

Feedback welcome!

## Replies

**CPerezz** (2026-01-21):

Hey nice post!! Definitely interesting to see the numbers and a nice summary that’s easy to digest!

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> would get us down to a worst-case block size of 2.25 MiB,

Wondering here if this also considers worst-case BAL too? ie. Is this BAL + Block or just Block data?

---

Another question I have is regarding the network in general. How are the numbers on propagation for 2.3MiB blocks? IIRC, over 1MB we are already seeing propagation times that degrade. Unsure if we have in sight any improvements on p2p layer that can make this manageable? cc: [@cskiraly](/u/cskiraly) ?

---

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> EIP-7981: Increase Access List Cost

Also, on this topic, what’s your take on just getting rid of Access Lists completely? Doesn’t it just feel easier? Are they really needed to keep compatibility at this point? Considering all the stuff we will likely break with repricings?

Thanks for the post!

---

**Nero_eth** (2026-01-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> Wondering here if this also considers worst-case BAL too? ie. Is this BAL + Block or just Block data?

Regarding the worst case: the largest Snappy-compressed blocks occur when *all* available gas is spent on calldata. In that scenario, the BAL is empty. Large BALs and large calldata are therefore mutually exclusive. Moreover, calldata produces strictly worse (i.e., larger) blocks than BALs, since everything declared in a BAL must actually be accessed or modified—otherwise the block is invalid.

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> Are they really needed to keep compatibility at this point?

As for compatibility: basically, yes. At a minimum, they must be repriced to properly account for their data cost and not contribute to the worst-case block size anymore. Fairly repricing them is simpler and safer than attempting full deprecation, at least for the short/medium term.

