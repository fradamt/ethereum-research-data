---
source: magicians
topic_id: 6079
title: EIP Proposal - Allow the elliptic curve precompiles to accept an x-coordinate and a 'sign'
author: iAmMichaelConnor
date: "2021-04-23"
category: EIPs
tags: [precompile, cryptography]
url: https://ethereum-magicians.org/t/eip-proposal-allow-the-elliptic-curve-precompiles-to-accept-an-x-coordinate-and-a-sign/6079
views: 838
likes: 0
posts_count: 1
---

# EIP Proposal - Allow the elliptic curve precompiles to accept an x-coordinate and a 'sign'

I’ve just thought of this, so sorry if there’s an obvious reason for why it’s stupid.

I’ve been pondering how to reduce calldata / memory costs for zk-snark projects like zkopru etc, where a batched transaction contains lots of elliptic curve points as calldata.

Currently the precompiles for ECADD, ECMUL ([EIP 196](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-196.md)) and Pairings ([EIP 197](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-197.md)) only accept elliptic curve point parameters as (x, y) affine coordinate pairs.

To save on calldata/memory costs, perhaps we could modify these precompile specifications so that a y-coordinate doesn’t need to be explicitly passed to these functions. The y-coordinate would instead be derived within the precompile operation. A point on the AltBN-254 curve can be expressed uniquely as an x-coordinate and a sign (positive or negative).

The first 2 bits of the `uint256` that an x-coordinate occupies are unused. So perhaps a prefix of `01` could imply ‘positive y-coordinate’ and a prefix of `10` could imply ‘negative y-coordinate’. I’ll lazily write `(sign, x)` to mean a 2-bit sign followed by a 254-bit x-value.

For G2 points of the form `(x, y)` where `x = a + ib`, only the first two bits of `a` would need to be prefixed to imply the sign of `y`.

We’d retain backwards compatibility with the current precompiles for (x, y) inputs which actually exist on the curve. But clearly, an error would no-longer necessarily be thrown for x-coordinates prefixed with a sign, whereas previously such formatting would have always been rejected as the user specifying an invalid field element.

For ADD:

To calculate `P1 + P2`, pass either `[(x1, y1), (x2, y2)]` (old format occupying 128 bytes) or `[(sign, x1), (sign, x2)]` (new format occupying 64 bytes).

The output formatting is up for debate. I suppose if a ‘sign’ is specified for the inputs, then the precompile should return the point `P3 = P1 + P2` formatted as `(sign, x3)`.

For MUL:

To calculate `s * P`, pass either `[(x, y), s]` (old format occupying 96 bytes) or `[(sign, x), s]` (new format occupying 64 bytes).

Output format should mirror the ADD case.

For Pairings, encode the inputs and outputs in a similar fashion. (I won’t write it out unless this idea gains some traction).

Since the precompiles already include a check to ensure a point is on the curve (and is a member of the correct subgroup), I’d argue the cost of evaluating `y` from `(sign, x)` might not result in much extra overhead.

Cheers!
