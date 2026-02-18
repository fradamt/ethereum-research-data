---
source: magicians
topic_id: 21798
title: "EIP-7823: Set upper bounds for MODEXP"
author: axic
date: "2024-11-23"
category: EIPs > EIPs core
tags: [precompile]
url: https://ethereum-magicians.org/t/eip-7823-set-upper-bounds-for-modexp/21798
views: 377
likes: 8
posts_count: 13
---

# EIP-7823: Set upper bounds for MODEXP

Discussion topic for [EIP-7823](https://eips.ethereum.org/EIPS/eip-7823)

#### Update Log

- 2025-01-27: updated EIP with analysis, clarified Backwards Compatibility and Security Considerations sections
- 2024-11-26: merged as EIP: EIP-7823: Set upper bounds for MODEXP
- 2024-11-11: initial draft Add EIP: Set upper bounds for MODEXP by axic · Pull Request #9046 · ethereum/EIPs · GitHub

#### External Reviews

None as of 2024-11-11.

#### Outstanding Issues

- Need to run a full sync to extract edge cases / uses outside the limits. Done.
- Verify that no reasonable use case exists outside of the limits.

## Replies

**krlosmata** (2024-11-28):

We set the exactly same limit on the zkEVM: [zkevm-rom/main/precompiled/pre-modexp.zkasm at v9.0.0-rc.2-fork.13 · 0xPolygonHermez/zkevm-rom · GitHub](https://github.com/0xPolygonHermez/zkevm-rom/blob/v9.0.0-rc.2-fork.13/main/precompiled/pre-modexp.zkasm#L11)

More context on why we decided to set up that limit is explained in this issue: [Computing the maximum ModExp input length · Issue #419 · 0xPolygonHermez/zkevm-rom · GitHub](https://github.com/0xPolygonHermez/zkevm-rom/issues/419)

This EIP will also make life easier to Rollups in order to be fully compliant with Ethereum.

---

**axic** (2024-11-28):

Thank you [@krlosmata](/u/krlosmata), that is very useful feedback. Will incorporate some of this into the EIP.

---

**hugo-dc** (2025-01-16):

The following is an analysis of MODEXP precompile calls, the dataset was collected by tracing calls to the MODEXP precompile since ~Byzantium Hard Fork until Block 21550926 (January 4th, 2025), the analysis contains the different input sizes used in all MODEXP calls and its frequency, being size 32 the most commonly used base/exponent/mod size, and 512 the maximum observed size (with the exception of a couple of transactions using size 513 for baseLen):



      [github.com](https://github.com/hugo-dc/modexp_analysis/blob/master/modexp.ipynb)





####



```ipynb
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "1d7aca17-4c1f-482a-8aa5-e7d2b425e03d",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "42d5e60e-b058-4df0-b21d-5583b2ee4c37",
   "metadata": {},
   "outputs": [],
   "source": [
```

  This file has been truncated. [show original](https://github.com/hugo-dc/modexp_analysis/blob/master/modexp.ipynb)

---

**jochem-brouwer** (2025-01-20):

Could this analysis be updated to explicitly define if these are bits or bytes? Even though the max bits/bytes reported seem to be 513 (2 entries in `base_len`), it is not clear to me if those are bits or bytes. (The 513 would fit in the EIP requirement of < 8192 bits / 1024 bytes, but would be nice to know by the analysis if the current “max” usage is 513 bits or bytes (likely: bytes?))

---

**Arvolear** (2025-01-20):

> If any of these inputs are larger than the limit, the precompile execution stops, returns an error, and consumes all gas.

A quick note that current precompiles *do not* return any errors. They leave empty `returndata` which indicates there has been an error.

---

**hugo-dc** (2025-01-20):

Yes, the values in the analysis results are given in bytes. I have updated the document to make it explicit. Thanks!.

---

**chfast** (2025-01-27):

I’m interested in two more restrictions:

1. How often the modulus is even? If is, how often is it a power of 2? If this is not often used I’d restrict the modulus to odd or power-of-two values.
2. How often the base >= modulus? Requiring base < modulus saves us from complicated initial base reduction.

---

**axic** (2025-01-27):

Updated the EIP with the result of analysis.

---

**axic** (2025-01-30):

Note: Scroll sets an upper bound of 32 bytes.

---

**jochem-brouwer** (2025-05-13):

Can a note be added that the precompile inputs `<length_of_BASE> <length_of_EXPONENT> <length_of_MODULUS>` are expressed in bytes, not in bits?

EIP reads this:

> We introduce an upper bound to the inputs of the precompile, each of the length inputs (length_of_BASE , length_of_EXPONENT and length_of_MODULUS ) MUST be less than or equal to 8192 bits (1024 bytes).

For a quick implementation of this EIP, people are likely going to check if these lengths are less than or equal to 8192. (This should be 1024)

---

**jochem-brouwer** (2025-05-13):

EIP 7883 (the price changes to MODEXP (fun side note, that EIP uses `ModExp`)) will likely be shipped with this one.

It has a test cases section [EIP-7883: ModExp Gas Cost Increase](https://eips.ethereum.org/EIPS/eip-7883#test-cases) which covers most (all?) test cases from `ethereum-tests`. Looking at the names it seems that some of those are now invalid. I don’t think this is a problem (they are likely benchmark/stress tests for some specific values?) but it might be handy to add this also in the EIP as note.

This EIP mentions:

> While we don’t suggest to rework the pricing function, it may be possible in a future upgrade once the limits are in place.

Are you happy with the price changes from 7883?

---

**axic** (2025-05-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> This EIP mentions:
>
>
>
> While we don’t suggest to rework the pricing function, it may be possible in a future upgrade once the limits are in place.

Are you happy with the price changes from 7883?

Yes, just the scope of the EIP was limited to exclude repricing. The repricing EIP can make use of these new limits when considering the pricing formula.

